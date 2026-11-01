// gate 97 probe: REAL router (routes/nft.routes.ts) + REAL IPFSService singleton (pinata provider => HTTP gateway path, no provider.read)
// + REAL shared errorHandler. Only replaced: ../db, ../cardano, logger (recording), and global fetch for the gateway URL.
import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest';
import * as fs from 'fs';
const h = vi.hoisted(() => {
  process.env.IPFS_PROVIDER = 'pinata'; process.env.PINATA_API_KEY = 'k'; process.env.PINATA_SECRET_KEY = 's';
  process.env.IPFS_GATEWAY = 'http://gateway.invalid/ipfs';
  return { logs: [] as any[], fetchCalls: 0 };
});
vi.mock('../db', () => ({ isDbAvailable: () => false, query: () => Promise.resolve({ rows: [] }) }));
vi.mock('../cardano', () => ({
  isCardanoNFTReady: () => false, mintNFTOnChain: () => Promise.resolve({}), getPolicyId: () => null, waitForNFTConfirmation: () => Promise.resolve({}),
}));
vi.mock('../utils/logger', () => {
  const rec = (lvl: string) => (m: string, meta?: any) => { h.logs.push({ lvl, m, meta }); };
  return { logger: { info: rec('info'), warn: rec('warn'), error: rec('error'), debug: rec('debug') } };
});
import express from 'express';
import type { AddressInfo } from 'net';
import { createServer, Server } from 'http';
import { errorHandler } from '@secuura/shared';
import router from '../routes/nft.routes';
import { ipfsService } from '../services/ipfs.service';

const realFetch = globalThis.fetch;
let server: Server; let base = '';
const out: any[] = [];
const CID = 'QmGate97Probe';

function mk(kind: string): unknown {
  if (kind === 'ordinary') return new Error('gateway down');
  if (kind === 'proxy') { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
  return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
}
const pkg = Buffer.from(JSON.stringify({ encrypted: true, encryptionMethod: 'aes', originalMimeType: 'text/plain', data: Buffer.from('secret').toString('base64') }));
const plain = Buffer.from('hello gate97');

beforeAll(async () => {
  const app = express(); app.use(express.json());
  app.use('/api/nft', router);
  app.use(errorHandler);
  server = createServer(app); await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => { server.close(); fs.writeFileSync(process.env.PROBE_OUT as string, JSON.stringify(out, null, 1)); });
beforeEach(() => { h.logs = []; h.fetchCalls = 0; });

type Mode = { stage: 'request' | 'body' | 'ok' | 'status'; kind?: string; status?: number; buf?: Buffer };
function stub(m: Mode) {
  const thrown = m.kind ? mk(m.kind) : undefined;
  vi.stubGlobal('fetch', (u: any, i: any) => {
    if (!String(u).startsWith('http://gateway.invalid/')) return realFetch(u, i);
    h.fetchCalls++;
    if (m.stage === 'request') return Promise.reject(thrown);
    if (m.stage === 'body') return Promise.resolve({ status: 200, ok: true, arrayBuffer: () => Promise.reject(thrown) });
    if (m.stage === 'status') return Promise.resolve({ status: m.status, ok: (m.status as number) < 400, arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)) });
    const b = m.buf as Buffer;
    return Promise.resolve({ status: 200, ok: true, arrayBuffer: () => Promise.resolve(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength)) });
  });
}
const cells: { name: string; mode: Mode }[] = [];
for (const stage of ['request', 'body'] as const) for (const kind of ['ordinary', 'proxy', 'getter']) cells.push({ name: stage + '/' + kind, mode: { stage, kind } });
cells.push({ name: 'status/404', mode: { stage: 'status', status: 404 } }, { name: 'status/502', mode: { stage: 'status', status: 502 } });
cells.push({ name: 'ok/plain', mode: { stage: 'ok', buf: plain } }, { name: 'ok/encpkg', mode: { stage: 'ok', buf: pkg } });
cells.push({ name: 'ok/notjson', mode: { stage: 'ok', buf: plain } });

for (const route of ['', '/encrypted']) for (const c of cells) {
  it('GET /ipfs/:cid' + route + ' ' + c.name, async () => {
    stub(c.mode);
    const unhandled: any[] = []; const uh = (e: any) => unhandled.push(String(e)); process.on('unhandledRejection', uh);
    try {
      const r = await realFetch(base + '/api/nft/ipfs/' + CID + route);
      const txt = await r.text();
      await new Promise((x) => setTimeout(x, 20));
      out.push({ cell: (route || '/plain') + ' ' + c.name, status: r.status, body: txt, fetchCalls: h.fetchCalls,
        logs: h.logs.filter((l) => l.lvl === 'error' || l.lvl === 'warn').map((l) => ({ lvl: l.lvl, m: l.m, meta: l.meta })), unhandled });
    } finally { process.off('unhandledRejection', uh); vi.unstubAllGlobals(); }
  });
}
it('sanity: provider has no read (HTTP path)', () => { expect((ipfsService as any).provider.read).toBeUndefined(); });
