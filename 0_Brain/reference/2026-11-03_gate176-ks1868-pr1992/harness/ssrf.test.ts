// Gate 176 recorder, Q1: drives the REAL security/ssrf-guard.ts (whichever blob swap.sh wrote) with a stand-in DNS
// lookup (dns/promises) and a stand-in request layer (http + https request()). One JSON line per cell to $GATE176_OUT.
// Nothing leaves the process: the stand-in request() never opens a socket; it counts the call (= "a request was
// constructed for sending") and then throws, so the guard reports request_failed.
import { describe, it, vi } from 'vitest';
import fs from 'node:fs';
import { VALUES, capture, kind, hits, SENT } from './values';

const OUT = process.env.GATE176_OUT as string;
const TAG = process.env.GATE176_TAG as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');

const h = vi.hoisted(() => ({
  dnsMode: 'throw' as 'throw' | 'addrs',
  dnsThrow: undefined as unknown,
  addrs: [] as Array<{ address: string; family: number }>,
  dnsCalls: 0,
  reqMode: 'record' as 'record' | 'throw',
  reqThrow: undefined as unknown,
  reqCalls: 0,
}));

vi.mock('dns/promises', () => {
  const lookup = () => {
    h.dnsCalls++;
    return h.dnsMode === 'throw' ? Promise.reject(h.dnsThrow) : Promise.resolve(h.addrs);
  };
  return { lookup, default: { lookup } };
});

const fakeRequest = () => {
  h.reqCalls++;
  if (h.reqMode === 'throw') throw h.reqThrow;
  // "record": the request WAS constructed (the instrument's positive arm). End it as an ordinary failure.
  throw new Error('gate176 stand-in: request constructed (not sent on the wire)');
};
vi.mock('https', async (importOriginal) => {
  const actual = await importOriginal<typeof import('https')>();
  return { ...actual, default: { ...actual, request: fakeRequest }, request: fakeRequest };
});
vi.mock('http', async (importOriginal) => {
  const actual = await importOriginal<typeof import('http')>();
  return { ...actual, default: { ...actual, request: fakeRequest }, request: fakeRequest };
});

const HOST = 'gate176.example.test';

function describeResult(r: unknown): Record<string, unknown> {
  if (r === null) return { out: 'returned null (ALLOWED)' };
  if (typeof r === 'string') return { out: 'returned refusal string', constant: r.includes('unreadable thrown value') };
  const o = r as any;
  const d: Record<string, unknown> = { out: `returned ok=${o.ok}` };
  if ('reason' in o) d.reason = o.reason;
  if ('addresses' in o) d.addresses = o.addresses;
  if ('error' in o) {
    d.errorType = typeof o.error;
    d.constant = typeof o.error === 'string' && o.error.includes('unreadable thrown value');
    d.errorHasSentinel = typeof o.error === 'string' && o.error.includes(SENT);
  }
  return d;
}

async function cell(fn: () => Promise<unknown>, v: unknown) {
  h.dnsCalls = 0;
  h.reqCalls = 0;
  const { result, lines } = await capture(async () => {
    try {
      return describeResult(await fn());
    } catch (e) {
      return { out: 'REJECTED ' + kind(e, v) };
    }
  });
  return { ...result, dnsCalls: h.dnsCalls, requestsConstructed: h.reqCalls, sentinelLines: hits(lines) };
}

describe('gate176 Q1 ssrf-guard recorder', () => {
  it('Q1 value classes', async () => {
    const g = await import('../security/ssrf-guard');
    for (const [name, make] of VALUES) {
      // (a) DNS lookup throws the value
      h.dnsMode = 'throw';
      h.reqMode = 'record';
      let v = make();
      h.dnsThrow = v;
      rec({ q: 'Q1', site: 'resolvePublicAddresses dns-throws', value: name, ...(await cell(() => g.resolvePublicAddresses(HOST), v)) });
      v = make();
      h.dnsThrow = v;
      rec({ q: 'Q1', site: 'assertResolvedHostPublic dns-throws', value: name, ...(await cell(() => g.assertResolvedHostPublic(HOST), v)) });
      v = make();
      h.dnsThrow = v;
      rec({ q: 'Q1', site: 'assertSafeOutboundUrl dns-throws', value: name, ...(await cell(() => g.assertSafeOutboundUrl(`https://${HOST}/`), v)) });
      v = make();
      h.dnsThrow = v;
      rec({ q: 'Q1', site: 'safeOutboundRequest dns-throws', value: name, ...(await cell(() => g.safeOutboundRequest(`https://${HOST}/`, { timeoutMs: 2000 }), v)) });
      // (b) DNS resolves to a public address; request() throws the value (hostname URL and IP-literal URL)
      h.dnsMode = 'addrs';
      h.addrs = [{ address: '203.0.113.7', family: 4 }];
      h.reqMode = 'throw';
      v = make();
      h.reqThrow = v;
      rec({ q: 'Q1', site: 'safeOutboundRequest request-throws (hostname)', value: name, ...(await cell(() => g.safeOutboundRequest(`https://${HOST}/`, { timeoutMs: 2000, method: 'POST', body: 'x' }), v)) });
      v = make();
      h.reqThrow = v;
      rec({ q: 'Q1', site: 'safeOutboundRequest request-throws (ip literal)', value: name, ...(await cell(() => g.safeOutboundRequest('https://203.0.113.7/', { timeoutMs: 2000 }), v)) });
    }
  });

  it('Q1h hostile addresses with ordinary errors (the guard own refusals)', async () => {
    const g = await import('../security/ssrf-guard');
    const sets: Array<[string, Array<{ address: string; family: number }>]> = [
      ['CONTROL public 203.0.113.7', [{ address: '203.0.113.7', family: 4 }]],
      ['CONTROL public 8.8.8.8 + 2001:4860:4860::8888', [{ address: '8.8.8.8', family: 4 }, { address: '2001:4860:4860::8888', family: 6 }]],
      ['private 10.0.0.5', [{ address: '10.0.0.5', family: 4 }]],
      ['private 192.168.1.1', [{ address: '192.168.1.1', family: 4 }]],
      ['private 172.16.0.1', [{ address: '172.16.0.1', family: 4 }]],
      ['loopback 127.0.0.1', [{ address: '127.0.0.1', family: 4 }]],
      ['loopback ::1', [{ address: '::1', family: 6 }]],
      ['link-local IMDS 169.254.169.254', [{ address: '169.254.169.254', family: 4 }]],
      ['link-local fe80::1', [{ address: 'fe80::1', family: 6 }]],
      ['unique-local fd00::1', [{ address: 'fd00::1', family: 6 }]],
      ['v4-mapped ::ffff:10.0.0.1', [{ address: '::ffff:10.0.0.1', family: 6 }]],
      ['v4-mapped ::ffff:127.0.0.1', [{ address: '::ffff:127.0.0.1', family: 6 }]],
      ['v4-mapped ::ffff:169.254.169.254', [{ address: '::ffff:169.254.169.254', family: 6 }]],
      ['v4-mapped hex ::ffff:a9fe:a9fe', [{ address: '::ffff:a9fe:a9fe', family: 6 }]],
      ['unspecified 0.0.0.0', [{ address: '0.0.0.0', family: 4 }]],
      ['mix public-first 8.8.8.8 + 10.0.0.1', [{ address: '8.8.8.8', family: 4 }, { address: '10.0.0.1', family: 4 }]],
      ['mix private-first 10.0.0.1 + 8.8.8.8', [{ address: '10.0.0.1', family: 4 }, { address: '8.8.8.8', family: 4 }]],
      ['mix public + v4-mapped IMDS', [{ address: '203.0.113.7', family: 4 }, { address: '::ffff:169.254.169.254', family: 6 }]],
      ['empty answer []', []],
    ];
    for (const [name, addrs] of sets) {
      h.dnsMode = 'addrs';
      h.addrs = addrs;
      h.reqMode = 'record';
      const v = new Error(`${SENT}-ord`);
      rec({ q: 'Q1h', site: 'resolvePublicAddresses', value: name, ...(await cell(() => g.resolvePublicAddresses(HOST), v)) });
      rec({ q: 'Q1h', site: 'assertResolvedHostPublic', value: name, ...(await cell(() => g.assertResolvedHostPublic(HOST), v)) });
      rec({ q: 'Q1h', site: 'safeOutboundRequest', value: name, ...(await cell(() => g.safeOutboundRequest(`https://${HOST}/`, { timeoutMs: 2000 }), v)) });
    }
    // IP-literal URLs (no DNS): the literal layer
    for (const u of ['https://203.0.113.7/', 'https://10.0.0.5/', 'https://127.1/', 'https://0x7f000001/', 'https://[::1]/', 'https://[::ffff:169.254.169.254]/', 'https://169.254.169.254/', 'http://203.0.113.7/', 'https://localhost/', 'https://x.internal/']) {
      h.reqMode = 'record';
      const v = new Error(`${SENT}-ord`);
      rec({ q: 'Q1h', site: 'safeOutboundRequest literal', value: u, ...(await cell(() => g.safeOutboundRequest(u, { timeoutMs: 2000 }), v)) });
    }
    // DNS throws an ordinary error: refusal, and nothing constructed
    h.dnsMode = 'throw';
    h.dnsThrow = new Error(`${SENT}-enotfound`);
    rec({ q: 'Q1h', site: 'safeOutboundRequest', value: 'dns ordinary ENOTFOUND', ...(await cell(() => g.safeOutboundRequest(`https://${HOST}/`, { timeoutMs: 2000 }), h.dnsThrow)) });
  });
});
