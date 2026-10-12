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


import { shouldSkipGlobalRateLimit } from '../middleware/rateLimitSkip';
describe('probe_b', () => {
  it('D: production default cap 300, 330 GETs straight to /api/v1/ alias', async () => {
    const g = await boot(PROD);
    const st = await burst(330, () => req(g.url, '/api/v1/platform/document-lookup?hash=abc'));
    const ctx = g.lines.filter((l) => l.msg === CTX);
    emit(`D statuses ${tally(st)} ctx-lines=${ctx.length} all-lines=${g.lines.length} msgs=${JSON.stringify([...new Set(g.lines.map((l) => l.lvl + ':' + l.msg.slice(0, 50)))])}`);
    emit(`D first ctx line meta=${JSON.stringify(ctx[0]?.meta)}`);
  }, 300000);
  it('E: 330 unversioned GETs each followed through the 307 (what a browser/fetch client does)', async () => {
    const g = await boot(PROD);
    const st = await burst(330, async () => { const a = await req(g.url, '/api/platform/document-lookup?hash=abc'); if (a === 307) return await req(g.url, '/api/v1/platform/document-lookup?hash=abc'); return a; });
    emit(`E (follow) final statuses ${tally(st)} ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`);
  }, 300000);
  const vs: Array<[string, string, string]> = [
    ['v1 control', 'GET', '/api/v1/platform/document-lookup?hash=abc'],
    ['V1 upper', 'GET', '/API/V1/PLATFORM/DOCUMENT-LOOKUP?hash=abc'],
    ['v1 trailing-slash', 'GET', '/api/v1/platform/document-lookup/?hash=abc'],
    ['v1 double-slash', 'GET', '/api/v1//platform/document-lookup?hash=abc'],
    ['v1 lead dbl-slash', 'GET', '//api/v1/platform/document-lookup?hash=abc'],
    ['v1 verif-dotdot', 'GET', '/api/v1/verification/../platform/document-lookup?hash=abc'],
    ['v1 verif-pct-dotdot', 'GET', '/api/v1/verification%2F..%2Fplatform/document-lookup?hash=abc'],
    ['v1 health-dotdot', 'GET', '/health/../api/v1/platform/document-lookup?hash=abc'],
    ['v1 HEAD', 'HEAD', '/api/v1/platform/document-lookup?hash=abc'],
    ['v1 OPTIONS', 'OPTIONS', '/api/v1/platform/document-lookup?hash=abc'],
    ['v1 abs-form', 'GET', 'http://x.example/api/v1/platform/document-lookup?hash=abc'],
    ['v1 abs-form verif path', 'GET', 'http://x.example/api/verification/api/v1/platform/document-lookup?hash=abc'],
    ['verif then v1 (rewrite mid)', 'GET', '/api/verification/api/v1/platform/document-lookup?hash=abc'],
    ['health then v1 (rewrite mid)', 'GET', '/health/api/v1/platform/document-lookup?hash=abc'],
    ['developers then v1', 'GET', '/developers/api/v1/platform/document-lookup?hash=abc'],
    ['v1 documentId', 'GET', '/api/v1/platform/document-lookup?documentId=%00x'],
  ];
  for (const [name, method, path] of vs) {
    it('F: ' + name, async () => {
      const g = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' });
      const st = await burst(12, () => req(g.url, path, method), 1);
      emit(`F ${name.padEnd(28)} ${method.padEnd(7)} ${path.padEnd(72)} -> ${st.join(',')} ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`);
    }, 120000);
  }
  it('G: XFF rotation on v1 path, production cap 5', async () => {
    const mk = async (f: (i: number) => string) => { const g = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' }); const st = await burst(40, (i) => req(g.url, '/api/v1/platform/document-lookup?hash=abc', 'GET', { 'x-forwarded-for': f(i) }), 1); return `${tally(st)} ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`; };
    emit('G1 direct, rotating XFF (single value): ' + await mk((i) => `10.9.0.${i}`));
    emit('G2 behind appending proxy (spoof,REAL): ' + await mk((i) => `10.9.0.${i}, 203.0.113.9`));
    emit('G3 rotating in LAST slot: ' + await mk((i) => `203.0.113.9, 10.9.0.${i}`));
    emit('G4 X-Real-IP rotating (nginx sets it too; gateway ignores?): ' + await (async () => { const g = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5' }); const st = await burst(40, (i) => req(g.url, '/api/v1/platform/document-lookup?hash=abc', 'GET', { 'x-real-ip': `10.8.0.${i}` }), 1); return `${tally(st)} ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`; })());
  }, 300000);
  it('H: production env levers cannot lift the cap on the route (cap 5): DISABLE_RATE_LIMIT, ENABLE_TEST_TOKENS + Bearer test_token_', async () => {
    const g = await boot({ ...PROD, RATE_LIMIT_MAX_REQUESTS: '5', DISABLE_RATE_LIMIT: 'true', ENABLE_TEST_TOKENS: 'true' });
    const st = await burst(12, () => req(g.url, '/api/v1/platform/document-lookup?hash=abc', 'GET', { authorization: 'Bearer test_token_admin' }), 1);
    emit(`H ${tally(st)} ctx-lines=${g.lines.filter((l) => l.msg === CTX).length}`);
  }, 120000);
  it('I: real predicate with positive control', () => {
    const a = (path: string, nodeEnv = 'production', authHeader = '', disableEnv: string | undefined = undefined) => shouldSkipGlobalRateLimit({ authHeader, path, nodeEnv, disableEnv });
    emit(`I subject doc-lookup prod -> ${a('/api/platform/document-lookup')}; v1 -> ${a('/api/v1/platform/document-lookup')}`);
    emit(`I POSITIVE CONTROL /api/verification/anything prod -> ${a('/api/verification/anything')}`);
    emit(`I DISABLE_RATE_LIMIT=true prod -> ${a('/api/platform/document-lookup', 'production', '', 'true')} ; control same in staging -> ${a('/api/platform/document-lookup', 'staging', '', 'true')}`);
    emit(`I Bearer test_token_ prod -> ${a('/api/platform/document-lookup', 'production', 'Bearer test_token_x')}`);
  });
});
