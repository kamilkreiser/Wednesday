// KS-1240 part 3 (scope extended by the coordinator's brief, not by the ticket; the ticket text names only the
// api-gateway key-validate fetch): the IPFS service made eight outbound fetches with no timeout, so a provider or
// gateway that accepted the connection and then went quiet held the caller for as long as the socket lived. Each
// call is now bounded by AbortSignal.timeout. The part that needs care is the gateway read: IPFSService.fetch()
// promises a 503 for an unreachable gateway, but its body read (response.arrayBuffer()) sat outside the try that
// makes that promise, so a gateway that sent its headers and then stalled the body (or dropped the connection mid
// body) would have surfaced as the raw abort error, an unmapped 500. The body read now maps to the same 503.
//
// The gateway read is driven through a REAL local http server and the real fetch (undici): the bound is shortened by
// wrapping AbortSignal.timeout, and everything else is the production path. The seven provider calls (upload, pin,
// unpin on Pinata and Infura, upload on Web3.Storage) go to fixed hostnames, so they are driven through a stubbed
// global fetch that honours init.signal and never answers when there is none (the hang the fix removes). No
// network, no database. Assertions read statusCode and code, as ipfs.service.test.ts does, because vitest can
// resolve @secuura/shared to a different module copy than the source (instanceof is not reliable here).
import { describe, it, expect, vi, afterEach } from 'vitest';
import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http';
import type { AddressInfo, Socket } from 'node:net';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { IPFSService } from '../services/ipfs.service';
import { logger } from '../utils/logger';

const SERVICE_SRC = readFileSync(join(__dirname, '..', 'services', 'ipfs.service.ts'), 'utf8');
const KEYS = { apiKey: 'key-ks1240', secretKey: 'secret-ks1240' };
const REQUEST = { data: Buffer.from('abc'), filename: 'a.txt', mimeType: 'text/plain', encrypted: false };
const BOUND_MS = 150;

type Handler = (req: IncomingMessage, res: ServerResponse) => void;
const open: Array<{ server: Server; sockets: Set<Socket> }> = [];

/** A real http server on an ephemeral loopback port; returns the gateway base URL the service is pointed at. */
async function gateway(handler: Handler): Promise<string> {
  const sockets = new Set<Socket>();
  const server = createServer(handler);
  server.on('connection', (s) => { sockets.add(s); s.on('close', () => sockets.delete(s)); });
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
  open.push({ server, sockets });
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}/ipfs`;
}

afterEach(async () => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
  for (const { server, sockets } of open.splice(0)) {
    for (const s of sockets) s.destroy();
    await new Promise<void>((resolve) => server.close(() => resolve()));
  }
});

/** Wrap AbortSignal.timeout: record the bound the service asked for, hand back a real signal that fires after ms. */
function shortenBounds(ms: number = BOUND_MS): number[] {
  const asked: number[] = [];
  const real = AbortSignal.timeout.bind(AbortSignal);
  vi.spyOn(AbortSignal, 'timeout').mockImplementation((requested: number) => { asked.push(requested); return real(ms); });
  return asked;
}

type Settled = { state: 'resolved'; value: unknown } | { state: 'rejected'; error: any } | { state: 'hung' };

/** Settles the call, or reports 'hung' after waitMs, so a hang is a red assertion and not a timed-out run. */
async function settle(run: () => Promise<unknown>, waitMs = 2000): Promise<Settled> {
  return Promise.race([
    run().then((value): Settled => ({ state: 'resolved', value }), (error): Settled => ({ state: 'rejected', error })),
    new Promise<Settled>((resolve) => setTimeout(() => resolve({ state: 'hung' }), waitMs)),
  ]);
}

/** The thrown error as the shared errorHandler would see it: status and code only. */
function answer(s: Settled): unknown {
  if (s.state === 'rejected') return { state: 'rejected', statusCode: s.error?.statusCode, code: s.error?.code };
  return s.state === 'resolved' ? { state: 'resolved' } : { state: 'hung' };
}

/** What came back, in words, so a red names the raw error instead of "expected {..} to deeply equal {..}". */
function why(s: Settled): string {
  return s.state === 'rejected'
    ? `rejected with ${s.error?.name}: ${s.error?.message} (statusCode ${s.error?.statusCode}, code ${s.error?.code})`
    : s.state;
}

const SERVICE_UNAVAILABLE = { state: 'rejected', statusCode: 503, code: 'SERVICE_UNAVAILABLE' };

describe('KS-1240 part 3: the gateway read answers 503 when the gateway goes quiet', () => {
  const service = (url: string): IPFSService => new IPFSService('pinata', { ...KEYS, gateway: url });

  it('RED KS-1240 IB1: a gateway that accepts the connection and never sends headers answers 503, not a hang', async () => {
    shortenBounds();
    const url = await gateway(() => { /* accept, say nothing */ });
    const settled = await settle(() => service(url).fetch('QmQuiet'));
    expect(answer(settled), why(settled)).toEqual(SERVICE_UNAVAILABLE);
  });

  it('RED KS-1240 IB2: a gateway that sends its headers and a first chunk and then stalls the body answers 503', async () => {
    shortenBounds();
    const url = await gateway((_req, res) => {
      res.writeHead(200, { 'content-type': 'application/octet-stream', 'content-length': '1000' });
      res.write('abc'); // 3 of the 1000 promised bytes, then silence
    });
    const warn = vi.spyOn(logger, 'warn');
    const settled = await settle(() => service(url).fetch('QmStall'));
    expect(answer(settled), why(settled)).toEqual(SERVICE_UNAVAILABLE);
    expect(warn).toHaveBeenCalledWith('IPFS gateway body read failed', expect.objectContaining({ cid: 'QmStall' }));
  });

  it('RED KS-1240 IB3: a gateway that drops the connection part-way through the body answers 503 too', async () => {
    shortenBounds();
    const url = await gateway((_req, res) => {
      res.writeHead(200, { 'content-type': 'application/octet-stream', 'content-length': '1000' });
      res.write('abc');
      setTimeout(() => res.destroy(), 20);
    });
    const settled = await settle(() => service(url).fetch('QmDrop'));
    expect(answer(settled), why(settled)).toEqual(SERVICE_UNAVAILABLE);
  });

  it('control KS-1240 IBC1: a body that arrives inside the bound is returned unchanged', async () => {
    shortenBounds(5000);
    const url = await gateway((_req, res) => { res.writeHead(200, { 'content-length': '5' }); res.end('hello'); });
    const settled = await settle(() => service(url).fetch('QmOk'));
    expect(settled.state).toBe('resolved');
    expect(Buffer.from((settled as { value: Buffer }).value).toString()).toBe('hello');
  });

  it('control KS-1240 IBC2: a gateway 404 is still a 404 and a 502 is still a 503 (the status mapping is untouched)', async () => {
    shortenBounds(5000);
    const url = await gateway((req, res) => { res.writeHead(req.url?.endsWith('/QmGone') ? 404 : 502); res.end(); });
    const gone = await settle(() => service(url).fetch('QmGone'));
    expect(answer(gone), why(gone)).toEqual({ state: 'rejected', statusCode: 404, code: 'NOT_FOUND' });
    const bad = await settle(() => service(url).fetch('QmBad'));
    expect(answer(bad), why(bad)).toEqual(SERVICE_UNAVAILABLE);
  });
});

type Site = { name: string; run: () => Promise<unknown>; expected: unknown };
const UPLOAD_FAILED = (provider: string) => ({ state: 'resolved', value: { success: false, error: expect.stringContaining(`${provider} upload error`) } });
const SITES: Site[] = [
  { name: 'pinata upload', run: () => new IPFSService('pinata', KEYS).upload(REQUEST), expected: UPLOAD_FAILED('Pinata') },
  { name: 'pinata pin', run: () => new IPFSService('pinata', KEYS).pin('QmX'), expected: { state: 'resolved', value: false } },
  { name: 'pinata unpin', run: () => new IPFSService('pinata', KEYS).unpin('QmX'), expected: { state: 'resolved', value: false } },
  { name: 'infura upload', run: () => new IPFSService('infura', KEYS).upload(REQUEST), expected: UPLOAD_FAILED('Infura') },
  { name: 'infura pin', run: () => new IPFSService('infura', KEYS).pin('QmX'), expected: { state: 'resolved', value: false } },
  { name: 'infura unpin', run: () => new IPFSService('infura', KEYS).unpin('QmX'), expected: { state: 'resolved', value: false } },
  { name: 'web3.storage upload', run: () => new IPFSService('web3storage', { apiKey: 'token-ks1240' }).upload(REQUEST), expected: UPLOAD_FAILED('Web3.Storage') },
];

/** Every call honours its signal; a call with NO signal never settles (the hang the fix removes). */
function stubFetchThatNeverAnswers(): void {
  vi.stubGlobal('fetch', vi.fn((_url: unknown, init?: { signal?: AbortSignal }) =>
    new Promise<Response>((_resolve, reject) => {
      const signal = init?.signal;
      if (!signal) return;
      if (signal.aborted) reject(signal.reason);
      else signal.addEventListener('abort', () => reject(signal.reason), { once: true });
    })));
}

describe('KS-1240 part 3: each provider call is bounded and keeps the failure answer it already had', () => {
  it.each(SITES)('RED KS-1240 IB4: a $name endpoint that never answers ends in its existing failure answer, not a hang', async ({ run, expected }) => {
    shortenBounds();
    stubFetchThatNeverAnswers();
    const settled = await settle(run);
    expect(settled, why(settled)).toMatchObject(expected as object);
  });

  it('RED KS-1240 IB5: the eight calls ask for 3 x 60 s (upload), 4 x 15 s (pin, unpin) and 1 x 30 s (gateway read)', async () => {
    const asked: number[] = [];
    vi.spyOn(AbortSignal, 'timeout').mockImplementation((ms: number) => { asked.push(ms); return new AbortController().signal; });
    const body = { IpfsHash: 'QmP', PinSize: 3, Hash: 'QmI', Size: '3', cid: 'bafyW' };
    vi.stubGlobal('fetch', vi.fn(async () => ({
      ok: true, status: 200,
      json: async () => body, text: async () => JSON.stringify(body), arrayBuffer: async () => new ArrayBuffer(3),
    })));
    for (const site of SITES) await site.run();
    await new IPFSService('pinata', KEYS).fetch('QmX');
    expect(asked.sort((a, b) => a - b)).toEqual([15000, 15000, 15000, 15000, 30000, 60000, 60000, 60000]);
  });
});

/** Every `await fetch(` call in the source with its argument text (parentheses matched), as { line, text }. */
function outboundFetchCalls(src: string): Array<{ line: number; text: string }> {
  const calls: Array<{ line: number; text: string }> = [];
  const needle = 'await fetch(';
  for (let at = src.indexOf(needle); at !== -1; at = src.indexOf(needle, at + 1)) {
    let depth = 0;
    let end = at + needle.length - 1;
    for (; end < src.length; end++) {
      if (src[end] === '(') depth++;
      else if (src[end] === ')' && --depth === 0) break;
    }
    calls.push({ line: src.slice(0, at).split('\n').length, text: src.slice(at, end + 1) });
  }
  return calls;
}

describe('KS-1240 part 3: the source carries a bound at every outbound fetch', () => {
  it('RED KS-1240 IB6: all eight `await fetch(` calls in ipfs.service.ts pass a signal built by AbortSignal.timeout', () => {
    const calls = outboundFetchCalls(SERVICE_SRC);
    expect(calls).toHaveLength(8);
    const unbounded = calls.filter((c) => !/signal:\s*AbortSignal\.timeout\(\s*IPFS_[A-Z_]+_TIMEOUT_MS\s*\)/.test(c.text));
    expect(unbounded.map((c) => c.line)).toEqual([]);
  });

  it('control KS-1240 IBC3: the scanner flags a planted unbounded call and passes a planted bounded one', () => {
    const planted = [
      'const a = await fetch(`https://x/${cid}`, { method: "POST", body: JSON.stringify({ a: 1 }) });',
      'const b = await fetch(url, { signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS) });',
    ].join('\n');
    const calls = outboundFetchCalls(planted);
    expect(calls.map((c) => c.line)).toEqual([1, 2]);
    const flagged = calls.filter((c) => !/signal:\s*AbortSignal\.timeout\(\s*IPFS_[A-Z_]+_TIMEOUT_MS\s*\)/.test(c.text));
    expect(flagged.map((c) => c.line)).toEqual([1]);
  });
});
