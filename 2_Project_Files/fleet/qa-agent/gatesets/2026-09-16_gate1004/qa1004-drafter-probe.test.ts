/**
 * qa1004-drafter-probe.test.ts — DRAFTER feasibility harness for the #1004 (KS-932) tier-1 gate. RECORDS rows; the
 * gate's own file must ASSERT. Lives only in a scratch clone's packages/shared/src/__tests__/, quarantined by rename.
 * Loopback only: every socket connect the guard attempts is COUNTED by a wrapper on net.Socket.prototype.connect and,
 * when a row asks, REDIRECTED to a 127.0.0.1 listener (silent = deterministic hang; closed port = deterministic fast RST).
 * No row lets a SYN leave the host: rows that reach the socket layer always redirect.
 */
import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import * as net from 'net';
import * as fs from 'fs';

const lookupMock = vi.fn();
vi.mock('dns/promises', () => ({ lookup: (...a: unknown[]) => lookupMock(...a) }));
const guard = await import('../security/ssrf-guard');

const OUT = process.env.QA1004_OUT || '/dev/null';
const rows: Record<string, unknown>[] = [];
const unhandled: string[] = [];
const onUnhandled = (e: unknown) => unhandled.push(String((e as Error)?.message ?? e));

const attempts: { host?: string; port?: number }[] = [];
let redirect: number | null = null;
const origConnect = net.Socket.prototype.connect;
let silent: net.Server; let silentPort = 0; let closedPort = 0; const held: net.Socket[] = [];

beforeAll(async () => {
  process.on('unhandledRejection', onUnhandled);
  (net.Socket.prototype as any).connect = function (...args: any[]) {
    const o = Array.isArray(args[0]) ? args[0][0] : args[0];
    if (o && typeof o === 'object') {
      attempts.push({ host: o.host, port: o.port });
      if (redirect === null) { o.host = '127.0.0.1'; o.port = closedPort; } // never let a SYN leave: default = fast RST
      else { o.host = '127.0.0.1'; o.port = redirect; }
      delete o.lookup;
    }
    return (origConnect as any).apply(this, args);
  };
  silent = net.createServer((s) => { held.push(s); });
  await new Promise<void>((r) => silent.listen(0, '127.0.0.1', () => r()));
  silentPort = (silent.address() as net.AddressInfo).port;
  const tmp = net.createServer();
  await new Promise<void>((r) => tmp.listen(0, '127.0.0.1', () => r()));
  closedPort = (tmp.address() as net.AddressInfo).port;
  await new Promise<void>((r) => tmp.close(() => r()));
});
afterAll(async () => {
  (net.Socket.prototype as any).connect = origConnect;
  process.off('unhandledRejection', onUnhandled);
  held.forEach((s) => s.destroy());
  await new Promise<void>((r) => silent.close(() => r()));
  fs.writeFileSync(OUT, JSON.stringify({ rows, unhandled }, null, 1));
});

const later = <T>(ms: number, v: () => T) => new Promise<T>((res) => setTimeout(() => res(v()), ms));
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
async function row(id: string, url: string, init: any, setup: () => void, opts: any = {}, waitAfter = 0) {
  lookupMock.mockReset(); setup();
  const a0 = attempts.length; const t0 = Date.now();
  let result: any; let threw: string | undefined;
  try { result = await guard.safeOutboundRequest(url, init, opts); } catch (e) { threw = String((e as Error).message); }
  const elapsed = Date.now() - t0; const aAtReturn = attempts.length - a0;
  if (waitAfter) await sleep(waitAfter);
  const r = { id, url, timeoutMs: init?.timeoutMs, elapsed, ok: result?.ok, reason: result?.reason, error: result?.error ?? threw, threw: !!threw,
    connectsAtReturn: aAtReturn, connectsAfterWait: attempts.length - a0, lookupCalls: lookupMock.mock.calls.length,
    lookupArgs: lookupMock.mock.calls[0]?.[1], activeTimeoutsAfter: process.getActiveResourcesInfo().filter((x) => x === 'Timeout').length };
  rows.push(r); return r;
}
const prompt = (addrs: [string, number][]) => () => lookupMock.mockImplementation(async () => addrs.map(([address, family]) => ({ address, family })));
const lateAddrs = (ms: number, addrs: [string, number][]) => () => lookupMock.mockImplementation(() => later(ms, () => addrs.map(([address, family]) => ({ address, family }))));

describe('A — refusal classes through the REAL safeOutboundRequest', () => {
  const literal = ['https://10.0.0.1/', 'https://127.0.0.1/', 'https://169.254.169.254/latest/meta-data/', 'https://2130706433/', 'https://0x7f000001/',
    'https://0/', 'https://[::1]/', 'https://[::ffff:127.0.0.1]/', 'https://[::ffff:a9fe:a9fe]/', 'https://[64:ff9b::a9fe:a9fe]/', 'https://[fe80::1]/', 'https://[fc00::1]/',
    'https://100.64.0.1/', 'https://198.18.0.1/', 'https://224.0.0.1/', 'http://203.0.113.7/', 'https://localhost./', 'https://metadata.internal/', 'https://intranet/', 'https://printer.local/', 'file:///etc/passwd'];
  it.each(literal)('A-L %s', async (u) => { await row('A-L ' + u, u, { timeoutMs: 300 }, () => lookupMock.mockImplementation(async () => [{ address: '203.0.113.7', family: 4 }])); expect(1).toBe(1); });
  const resolved: [string, [string, number][]][] = [['10.0.0.5', [['10.0.0.5', 4]]], ['127.0.0.1', [['127.0.0.1', 4]]], ['169.254.169.254', [['169.254.169.254', 4]]],
    ['::1', [['::1', 6]]], ['::ffff:127.0.0.1', [['::ffff:127.0.0.1', 6]]], ['::ffff:a9fe:a9fe', [['::ffff:a9fe:a9fe', 6]]], ['fe80::1', [['fe80::1', 6]]], ['fd00::1', [['fd00::1', 6]]],
    ['100.64.1.1', [['100.64.1.1', 4]]], ['0.0.0.0', [['0.0.0.0', 4]]], ['public+private', [['203.0.113.7', 4], ['192.168.1.1', 4]]], ['private+public', [['192.168.1.1', 4], ['203.0.113.7', 4]]]];
  it.each(resolved)('A-R %s', async (name, addrs) => { await row('A-R ' + name, 'https://rebind.example.com/x', { timeoutMs: 300 }, prompt(addrs)); expect(1).toBe(1); });
  it('A-R lookup rejects ENOTFOUND', async () => { await row('A-R ENOTFOUND', 'https://nx.example.com/', { timeoutMs: 300 }, () => lookupMock.mockRejectedValue(Object.assign(new Error('getaddrinfo ENOTFOUND nx.example.com'), { code: 'ENOTFOUND' }))); });
  it('A-R lookup resolves []', async () => { await row('A-R empty', 'https://empty.example.com/', { timeoutMs: 300 }, () => lookupMock.mockResolvedValue([])); });
  it('A-AL allowlist refuses', async () => { process.env.WEBHOOK_URL_ALLOWLIST = 'example.com'; try { await row('A-AL evil.net', 'https://evil.net/x', { timeoutMs: 300 }, prompt([['203.0.113.7', 4]])); } finally { delete process.env.WEBHOOK_URL_ALLOWLIST; } });
  it('A-CTRL a public answer DOES reach the socket layer (redirected to a closed loopback port)', async () => { redirect = null; await row('A-CTRL public', 'https://ok.example.com/', { timeoutMs: 300 }, prompt([['203.0.113.7', 4]])); });
});

describe('B — the race: late answers, rejections, timers', () => {
  it('B1 PRIVATE answer arrives AFTER the timer', async () => { await row('B1 late private', 'https://late.example.com/', { timeoutMs: 200 }, lateAddrs(400, [['10.0.0.5', 4]]), {}, 500); });
  it('B2 PUBLIC answer arrives AFTER the timer', async () => { await row('B2 late public', 'https://late.example.com/', { timeoutMs: 200 }, lateAddrs(400, [['203.0.113.7', 4]]), {}, 500); });
  it('B3 PRIVATE answer just BEFORE the timer', async () => { await row('B3 private before', 'https://late.example.com/', { timeoutMs: 200 }, lateAddrs(150, [['10.0.0.5', 4]])); });
  it('B4 lookup REJECTS after the timer', async () => { await row('B4 late reject', 'https://late.example.com/', { timeoutMs: 200 }, () => lookupMock.mockImplementation(() => new Promise((_, rej) => setTimeout(() => rej(new Error('late EAI_AGAIN')), 400))), {}, 500); });
  it('B5 malformed answer ({}) AFTER the timer -> resolvePublicAddresses rejects late', async () => { await row('B5 late malformed', 'https://late.example.com/', { timeoutMs: 200 }, () => lookupMock.mockImplementation(() => later(400, () => ({}) as any)), {}, 500); });
  it('B6 malformed answer ({}) PROMPTLY -> the race rejects; is the DNS timer left armed?', async () => { await row('B6 prompt malformed', 'https://late.example.com/', { timeoutMs: 1500 }, () => lookupMock.mockImplementation(async () => ({}) as any)); });
  it('B7 timer cleared when DNS wins (prompt public, silent loopback, 250ms)', async () => { redirect = silentPort; try { await row('B7 prompt public silent', 'https://ok.example.com/', { timeoutMs: 250 }, prompt([['203.0.113.7', 4]]), {}, 50); } finally { redirect = null; } });
  it.each([0, -5, Number.NaN, 1])('B8 timeoutMs=%s never opens an unvetted path', async (t) => { redirect = silentPort; try { await row('B8 timeoutMs=' + t, 'https://edge.example.com/', { timeoutMs: t }, prompt([['10.0.0.9', 4]])); await row('B8p timeoutMs=' + t, 'https://edge.example.com/', { timeoutMs: t }, prompt([['203.0.113.7', 4]])); } finally { redirect = null; } });
});

describe('C — one budget (deterministic hang = a silent 127.0.0.1 listener)', () => {
  it.each([[0, 400], [200, 400], [350, 400], [390, 400], [450, 400]])('C dns=%sms timeoutMs=%s', async (d, t) => {
    redirect = silentPort;
    try { await row(`C dns=${d} t=${t}`, 'https://budget.example.com/', { timeoutMs: t }, d ? lateAddrs(d, [['203.0.113.7', 4]]) : prompt([['203.0.113.7', 4]])); } finally { redirect = null; }
  });
});

describe('D — the seat cells\' shapes under a FAST RST (closed 127.0.0.1 port)', () => {
  it('D2 seat cell 2 shape: dns 200ms, timeoutMs 400', async () => { redirect = null; await row('D2 fastRST cell2', 'https://slow.example/', { timeoutMs: 400 }, lateAddrs(200, [['203.0.113.7', 4]])); });
  it('D3 seat cell 3 shape: prompt, timeoutMs 300', async () => { redirect = null; await row('D3 fastRST cell3', 'https://fast.example/', { timeoutMs: 300 }, prompt([['203.0.113.7', 4]])); });
});

describe('E — unhandled rejections across the file', () => {
  it('E1 settle window, then count', async () => { await sleep(1700); rows.push({ id: 'E1 unhandled', count: unhandled.length, messages: unhandled }); });
});
