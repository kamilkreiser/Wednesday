// GATE PROBE (scratch only) - real app, NODE_ENV=production, document-lookup log volume
import { describe, it, afterAll, beforeAll, vi } from 'vitest';
import http from 'http';
import type { AddressInfo } from 'net';
import * as fs from 'fs';

const SERVICE_URLS = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
  'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET'].map((n) => `${n}_SERVICE_URL`);
const CTX = 'Document lookup failed (GET /api/platform/document-lookup)';
let recorder: http.Server; let recorderUrl = '';
const open: http.Server[] = [];
const OUT = process.env.PROBE_OUT as string;
const emit = (s: string) => { fs.appendFileSync(OUT, s + '\n'); };

async function listen(server: http.Server): Promise<string> {
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  return `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}
async function boot(env: Record<string, string>) {
  for (const key of SERVICE_URLS) vi.stubEnv(key, recorderUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://u:p@127.0.0.1:1/platform');
  for (const [k, v] of Object.entries(env)) vi.stubEnv(k, v);
  vi.resetModules();
  const app = (await import('../index')).default;
  const { logger } = await import('../utils/logger');
  const lines: Array<{ lvl: string; msg: string; meta: unknown }> = [];
  for (const lvl of ['error', 'warn', 'info', 'debug', 'http', 'verbose', 'silly'] as const) {
    vi.spyOn(logger as any, lvl).mockImplementation(((msg: any, meta: any) => { lines.push({ lvl, msg: String(msg), meta }); return logger; }) as never);
  }
  vi.spyOn(logger as any, 'log').mockImplementation(((lvl: any, msg: any, meta: any) => { lines.push({ lvl: 'log:' + lvl, msg: String(msg), meta }); return logger; }) as never);
  const server = http.createServer(app as http.RequestListener);
  open.push(server);
  return { server, url: await listen(server), lines };
}
const PROD = { NODE_ENV: 'production', CSRF_SECRET: 'probe-stub-csrf-not-a-real-secret', DATABASE_URL: 'postgres://p:p@127.0.0.1:1/p',
  REDIS_URL: 'redis://127.0.0.1:1', ENABLE_TEST_TOKENS: '', ENABLE_MOCK_ENDPOINTS: '' };

function req(url: string, path: string, method = 'GET', headers: Record<string, string> = {}): Promise<number> {
  const t = new URL(url);
  return new Promise((resolve) => {
    const r = http.request({ hostname: t.hostname, port: t.port, path, method, agent: false, headers }, (res) => { res.resume(); res.on('end', () => resolve(res.statusCode ?? 0)); });
    r.on('error', () => resolve(-1)); r.end();
  });
}
const tally = (a: number[]) => { const m: Record<string, number> = {}; for (const s of a) m[s] = (m[s] ?? 0) + 1; return JSON.stringify(m); };
async function burst(n: number, f: (i: number) => Promise<number>, conc = 10) {
  const out: number[] = []; let i = 0;
  await Promise.all(Array.from({ length: conc }, async () => { while (i < n) { const k = i++; out[k] = await f(k); } }));
  return out;
}

beforeAll(async () => {
  recorder = http.createServer((q, s) => { q.resume(); q.on('end', () => { s.writeHead(200, { 'content-type': 'application/json' }); s.end('{}'); }); });
  recorderUrl = await listen(recorder);
});
afterAll(async () => { for (const s of open) { s.closeAllConnections(); s.close(); } recorder.close(); vi.unstubAllEnvs(); });

describe('probe', () => {
  it('A: production default cap, 330 GETs, single source', async () => {
    const g = await boot(PROD);
    emit('A env: ' + JSON.stringify({ NODE_ENV: process.env.NODE_ENV, RATE: process.env.RATE_LIMIT_MAX_REQUESTS ?? '(unset)' }));
    const st = await burst(330, () => req(g.url, '/api/platform/document-lookup?hash=abc'));
    const ours = g.lines.filter((l) => l.msg === CTX).length;
    emit(`A statuses ${tally(st)}  ctx-lines=${ours}  all-lines=${g.lines.length}  other-msgs=${JSON.stringify([...new Set(g.lines.filter((l) => l.msg !== CTX).map((l) => l.lvl + ':' + l.msg.slice(0, 60)))])}`);
    const g2 = await boot(PROD);
    const s1 = await req(g2.url, '/api/platform/document-lookup?hash=abc');
    emit(`A1 one request status ${s1} -> lines ${JSON.stringify(g2.lines.map((l) => l.lvl + ':' + l.msg.slice(0, 70)))}`);
    const g3 = await boot(PROD);
    const s0 = await req(g3.url, '/api/platform/zz-nonexistent');
    emit(`A0 control (404 path) status ${s0} -> lines ${JSON.stringify(g3.lines.map((l) => l.lvl + ':' + l.msg.slice(0, 70)))}`);
  }, 300000);

  it('B: XFF spoof, direct vs behind an appending proxy (cap 5, production)', async () => {
    const g = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' });
    const st = await burst(40, (i) => req(g.url, '/api/platform/document-lookup?hash=abc', 'GET', { 'x-forwarded-for': `10.9.${i >> 8}.${i & 255}` }), 1);
    emit(`B1 direct, XFF rotating single value: ${tally(st)} ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`);
    const g2 = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' });
    const st2 = await burst(40, (i) => req(g2.url, '/api/platform/document-lookup?hash=abc', 'GET', { 'x-forwarded-for': `10.9.${i >> 8}.${i & 255}, 203.0.113.9` }), 1);
    emit(`B2 appending-proxy shape (spoof, then REAL-appended last): ${tally(st2)} ctx-lines=${g2.lines.filter((l) => l.msg === CTX).length}`);
    const g3 = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' });
    const st3 = await burst(40, (i) => req(g3.url, '/api/platform/document-lookup?hash=abc', 'GET', { 'x-forwarded-for': `203.0.113.9, 10.9.${i >> 8}.${i & 255}` }), 1);
    emit(`B3 rotating value in the LAST slot (gateway directly reachable): ${tally(st3)} ctx-lines=${g3.lines.filter((l) => l.msg === CTX).length}`);
  }, 300000);

  const variants: Array<[string, string, string]> = [
    ['control', 'GET', '/api/platform/document-lookup?hash=abc'],
    ['verif-dotdot', 'GET', '/api/verification/../platform/document-lookup?hash=abc'],
    ['health-dotdot', 'GET', '/health/../api/platform/document-lookup?hash=abc'],
    ['developers-dotdot', 'GET', '/developers/../api/platform/document-lookup?hash=abc'],
    ['apidocs-dotdot', 'GET', '/api/docs/../platform/document-lookup?hash=abc'],
    ['trailing-slash', 'GET', '/api/platform/document-lookup/?hash=abc'],
    ['upper-case', 'GET', '/API/PLATFORM/DOCUMENT-LOOKUP?hash=abc'],
    ['double-slash-mid', 'GET', '/api//platform/document-lookup?hash=abc'],
    ['double-slash-lead', 'GET', '//api/platform/document-lookup?hash=abc'],
    ['pct-encoded-p', 'GET', '/api/%70latform/document-lookup?hash=abc'],
    ['pct-encoded-slash', 'GET', '/api%2Fplatform/document-lookup?hash=abc'],
    ['pct-verif-dotdot', 'GET', '/api/verification%2F..%2Fplatform/document-lookup?hash=abc'],
    ['semicolon', 'GET', '/api/platform/document-lookup;x=1?hash=abc'],
    ['v1-alias', 'GET', '/api/v1/platform/document-lookup?hash=abc'],
    ['v2-alias', 'GET', '/api/v2/platform/document-lookup?hash=abc'],
    ['query-has-skip', 'GET', '/api/platform/document-lookup?hash=abc&p=/api/verification'],
    ['HEAD', 'HEAD', '/api/platform/document-lookup?hash=abc'],
    ['OPTIONS', 'OPTIONS', '/api/platform/document-lookup?hash=abc'],
    ['absolute-form', 'GET', 'http://x.example/api/platform/document-lookup?hash=abc'],
    ['absolute-form-verif', 'GET', 'http://x.example/api/verification/x/../../platform/document-lookup?hash=abc'],
    ['verif-prefix-sibling', 'GET', '/api/verificationX/../platform/document-lookup?hash=abc'],
    ['other-mount', 'GET', '/api/verification/api/platform/document-lookup?hash=abc'],
  ];
  for (const [name, method, path] of variants) {
    it('C: ' + name, async () => {
      const g = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' });
      const st = await burst(12, () => req(g.url, path, method), 1);
      emit(`C ${name.padEnd(22)} ${method.padEnd(7)} ${path.padEnd(70)} -> ${st.join(',')}  ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`);
    }, 120000);
  }
});
