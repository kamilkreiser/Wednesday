/**
 * qa1017-gate-probe.test.ts — QA gate #1017 (KS-1195) round 1. Copied into the GATE's own clone (api-gateway src/__tests__), run SOLO,
 * quarantined by rename. Rows -> process.env.QA_OUT. Derived in shape from the drafter's probe (a starting point, not evidence); the
 * detectors below are the gate's own.
 *
 * QA_STAGES (comma list):
 *   census     — every literal route in index.ts / routes/*.ts / services/health.ts (+ for every router.use/all prefix: GET <prefix>/<sub> and
 *                POST <prefix>) on the REAL index.ts app. Per route: K fresh key (own connectorId, 2/60) x3 with upstream hits after each;
 *                N none, I unknown sk_, M malformed Bearer; then D fresh key (own connectorId, 1000/60) x1 -> Remaining 999 once / 998 twice;
 *                P every non-machine principal x1 (header? 429?); C a machine control on the SAME instrument (JWT authMethod api_key, own userId).
 *   principals — GET /api/anchors/<m> x4 per principal (incl. machine spellings).
 *   a4 / keyscope / erasure / bare / plant / order / redisthrow / perip — see each it().
 * QA_FAKE_REDIS=1: LABELLED SUBSTITUTE — vi.mock('../services/redis') getRedisClient -> in-process async fake (NOT the real ioredis client).
 * QA_AUDIT=1: vi.mock('../db') isDbAvailable true + capture audit INSERT params. QA_PERIP=1: per-IP limiters left at their DEFAULT maxima.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import express from 'express';
import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';
import type { AddressInfo } from 'net';

const OUT = process.env.QA_OUT || '';
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';
const STAGES = (process.env.QA_STAGES || 'census,principals,a4,keyscope,erasure,bare,plant').split(',');
const PERIP = process.env.QA_PERIP === '1';

const fakeRedis = { calls: 0, throws: 0, store: new Map<string, { n: number; exp: number }>(), status: 'ready' as string,
  async incr(k: string) { this.calls++; await new Promise((r) => setTimeout(r, 2)); if (k.includes('qa-throw')) { this.throws++; throw new Error('qa fake redis mid-command ECONNRESET'); }
    const e = this.store.get(k); const now = Date.now(); if (!e || (e.exp && now > e.exp)) { this.store.set(k, { n: 1, exp: 0 }); return 1; } e.n++; return e.n; },
  async pexpire(k: string, ms: number) { this.calls++; this.pexpireAt.push(this.store.get(k)?.n ?? -1); await new Promise((r) => setTimeout(r, 1)); const e = this.store.get(k); if (e) e.exp = Date.now() + ms; return 1; },
  pexpireAt: [] as number[],
  async pttl(k: string) { this.calls++; const e = this.store.get(k); return e && e.exp ? e.exp - Date.now() : -1; } };
(globalThis as any).__qaFakeRedis = fakeRedis;
const auditRows: any[] = [];
(globalThis as any).__qaAuditRows = auditRows;

vi.mock('../services/redis', async (importOriginal) => {
  const m: any = await importOriginal();
  if (process.env.QA_FAKE_REDIS !== '1') return m;
  return { ...m, getRedisClient: () => (globalThis as any).__qaFakeRedis };
});
vi.mock('../db', async (importOriginal) => {
  const m: any = await importOriginal();
  if (process.env.QA_AUDIT !== '1') return m;
  return { ...m, isDbAvailable: () => true, query: async (sql: string, params: unknown[]) => {
    if (/INSERT INTO audit_logs/i.test(sql)) (globalThis as any).__qaAuditRows.push({ sql: sql.replace(/\s+/g, ' ').slice(0, 300), params, at: Date.now() });
    return { rows: [], rowCount: 0 };
  } };
});

type Rec = { method: string; url: string; headers: http.IncomingHttpHeaders; body: string };
const seen: Rec[] = [];
const markerHits = new Map<string, number>();
const logged: string[] = [];
const KEYS = new Map<string, Record<string, unknown>>();
let ALL_SCOPES: string[] = [];

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
type Res = { status: number; code: string | null; h: Record<string, string | null>; json: any };
const H = ['x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset', 'retry-after', 'ratelimit-limit', 'ratelimit-remaining', 'ratelimit', 'ratelimit-policy'];
function send(base: string, method: string, p: string, headers: Record<string, string>, body?: string, timeoutMs = 3000): Promise<Res> {
  return new Promise((resolve) => {
    const u = new URL(base);
    const hh: Record<string, string> = { ...headers };
    if (body !== undefined) { hh['content-type'] = 'application/json'; hh['content-length'] = String(Buffer.byteLength(body)); }
    const req = http.request({ hostname: u.hostname, port: u.port, path: p, method, headers: hh, agent: false }, (res) => {
      const c: Buffer[] = []; res.on('data', (d) => c.push(d));
      res.on('end', () => {
        let json: any = null;
        try { json = JSON.parse(Buffer.concat(c).toString()); } catch { json = null; }
        const h: Record<string, string | null> = {};
        for (const k of H) h[k] = (res.headers[k] as string) ?? null;
        resolve({ status: res.statusCode || 0, code: json?.error?.code ?? null, h, json });
      });
    });
    req.setTimeout(timeoutMs, () => { req.destroy(); resolve({ status: -1, code: 'CLIENT_TIMEOUT', h: {}, json: null }); });
    req.on('error', (e) => resolve({ status: -2, code: 'CLIENT_ERROR ' + (e as Error).message.slice(0, 60), h: {}, json: null }));
    if (body !== undefined) req.end(body); else req.end();
  });
}
async function listen(s: http.Server): Promise<string> {
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
}
async function close(s?: http.Server): Promise<void> {
  if (!s) return;
  (s as any).closeAllConnections?.();
  await new Promise<void>((r) => s.close(() => r()));
}
const sign = (claims: Record<string, unknown>) => jwt.sign({ userId: 'u-qa1017', email: 'qa1017@example.test', role: 'issuer', tenantId: 't-qa1017-jwt', verificationLevel: 'standard', ...claims }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
const testToken = (p: Record<string, unknown>) => 'test_token_' + Buffer.from(JSON.stringify(p)).toString('base64');
const hits = (marker: string) => markerHits.get(marker) || 0;
const calls = (url: string, bodyIncludes: string) => seen.filter((r) => r.url === url && r.body.includes(bodyIncludes)).length;
function key(name: string, spec: Record<string, unknown>) { KEYS.set(name, spec); return name; }
const hdrs = (r: Res) => [r.status, r.code, r.h['x-ratelimit-limit'], r.h['x-ratelimit-remaining'], r.h['retry-after']];

let stub: http.Server; let stubUrl = '';
let gw: http.Server; let gwUrl = '';
let bare: http.Server; let bareUrl = '';
const rows: Record<string, any> = { meta: {}, census: [], principals: [], a4: [], keyscope: [], erasure: [], bare: [], plant: [], order: [], redisthrow: [], perip: [] };
const bareHits: Record<string, number> = { sync: 0, async: 0, tenant: 0, plantNext: 0, plantHandler: 0 };
const rejections: string[] = [];
const uncaught: string[] = [];
let shared: any; let auth: any; let rle: any;

beforeAll(async () => {
  expect(PRIV.length).toBeGreaterThan(100);
  stub = http.createServer(async (req, res) => {
    const body = await readBody(req);
    seen.push({ method: req.method || '', url: req.url || '', headers: { ...req.headers }, body });
    if (req.url !== '/api/keys/validate' && req.url !== '/internal/connector-token') {
      for (const m of new Set([...(req.url || '').matchAll(/qa[a-z0-9]+-[A-Za-z0-9_-]+?(?=[/?&"]|$)/g), ...body.matchAll(/qa[a-z0-9]+-[A-Za-z0-9_-]+?(?=[/?&"]|$)/g)].map((x) => x[0]))) markerHits.set(m, (markerHits.get(m) || 0) + 1);
    }
    const j = (s: number, o: unknown) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
    if (req.url === '/api/keys/validate') {
      const m = KEYS.get(JSON.parse(body || '{}').key);
      return j(200, m ? { success: true, data: { valid: true, ...m } } : { success: true, data: { valid: false } });
    }
    if (req.url === '/internal/connector-token') {
      const m = KEYS.get(JSON.parse(body || '{}').apiKey);
      if (!m) return j(401, { success: false });
      const token = jwt.sign({ userId: `connector:${String(m.connectorId || 'api-key')}`, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: m.tenantId, scopes: m.scopes }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
      return j(200, { success: true, data: { token, expiresIn: 600 } });
    }
    if (req.url === '/.well-known/jwks.json') return j(404, {});
    if (req.method === 'POST') return j(201, { success: true, data: { id: 'doc-qa1017' } });
    return j(200, { success: true, data: [] });
  });
  stubUrl = await listen(stub);

  vi.resetModules();
  vi.stubEnv('NODE_ENV', 'test');
  vi.stubEnv('ENABLE_TEST_TOKENS', 'true');
  vi.stubEnv('UNHANDLED_REJECTION_MODE', 'survive');
  if (!PERIP) { vi.stubEnv('RATE_LIMIT_MAX_REQUESTS', '1000000'); vi.stubEnv('VERIFICATION_RATE_LIMIT_MAX', '1000000'); }
  else { delete process.env.RATE_LIMIT_MAX_REQUESTS; delete process.env.VERIFICATION_RATE_LIMIT_MAX; delete process.env.DISABLE_RATE_LIMIT; }
  for (const n of ['ORIGINATE', 'WALLET', 'AUTH', 'SECURITY', 'ANCHORING', 'TIMESTAMPING', 'PRISM', 'VC_ISSUER', 'STAKING', 'REFERRAL', 'TRANSFER', 'KYC', 'GOVERNANCE', 'NFT', 'BILLING', 'ANALYTICS', 'NOTIFICATION', 'TENANT', 'M365', 'QUEUE', 'GUARDIAN']) vi.stubEnv(`${n}_SERVICE_URL`, stubUrl);
  vi.stubEnv('TENANT_PROVISIONING_URL', stubUrl); vi.stubEnv('TOKENISATION_URL', stubUrl); vi.stubEnv('MCP_SERVER_URL', stubUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL; delete process.env.SUBJECTS_ERASE_SCOPE_ENFORCED;
  process.on('unhandledRejection', (r) => { rejections.push(String((r as Error)?.message || r).slice(0, 160)); });
  process.on('uncaughtException', (e) => { uncaught.push(String((e as Error)?.message || e).slice(0, 160)); });

  const app = (await import('../index')).default;
  auth = await import('../middleware/auth');
  rle = await import('../middleware/rateLimitEnforce');
  shared = await import('@secuura/shared');
  const redisMod: any = await import('../services/redis');
  const { logger } = await import('../utils/logger');
  for (const level of ['error', 'warn'] as const) {
    vi.spyOn(logger, level).mockImplementation(((...a: unknown[]) => { logged.push(a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); return logger; }) as any);
  }
  vi.spyOn(console, 'error').mockImplementation((...a: unknown[]) => { logged.push(a.map((x) => (typeof x === 'string' ? x : (x as Error)?.message ?? JSON.stringify(x))).join(' ')); });
  vi.spyOn(console, 'warn').mockImplementation((...a: unknown[]) => { logged.push(a.map(String).join(' ')); });
  gw = http.createServer(app as http.RequestListener);
  gwUrl = await listen(gw);

  const b = express();
  b.get('/sync-throw', auth.authenticateToken(true), () => { bareHits.sync += 1; throw new Error('qa1017 sync throw downstream'); });
  b.get('/async-reject', auth.authenticateToken(true), (async () => { bareHits.async += 1; await new Promise((r) => setTimeout(r, 5)); throw new Error('qa1017 async reject downstream'); }) as any);
  b.get('/tenant', auth.authenticateToken(true), async (req: any, s) => { bareHits.tenant += 1; await new Promise((r) => setTimeout(r, 4)); s.status(200).json({ tenant: shared.currentTenantId() ?? null, user: req.user?.userId ?? null }); });
  b.get('/twice', auth.authenticateToken(true), auth.authenticateToken(false), (_q, s) => { s.status(200).json({ ok: true }); });
  // PLANT: a next() that throws synchronously on its FIRST call per request (Express's own next never does; this is a plant).
  b.get('/plant', (req: any, s) => {
    let n = 0;
    auth.authenticateToken(true)(req, s, () => { n += 1; bareHits.plantNext += 1; req.__qaNextCalls = n; if (n === 1) throw new Error('qa1017 plant: next throws synchronously'); bareHits.plantHandler += 1; if (!s.headersSent) s.status(200).json({ nextCalls: n }); });
  });
  bare = http.createServer(b);
  bareUrl = await listen(bare);

  const src = path.resolve(__dirname, '..');
  const scopeSet = new Set<string>();
  for (const f of [src + '/index.ts', ...fs.readdirSync(src + '/routes').map((x) => src + '/routes/' + x), src + '/services/health.ts']) {
    for (const m of fs.readFileSync(f, 'utf8').matchAll(/'([a-z_]+:[a-z_*]+)'/g)) scopeSet.add(m[1]);
  }
  ALL_SCOPES = [...scopeSet].sort();
  rows.meta = { redisAvailable: redisMod.isRedisAvailable(), fakeRedis: process.env.QA_FAKE_REDIS === '1', audit: process.env.QA_AUDIT === '1', perip: PERIP, scopes: ALL_SCOPES.length, stages: STAGES, at: new Date().toISOString() };
}, 60000);

afterAll(async () => {
  rows.meta.logged_headers_sent = logged.filter((l) => /ERR_HTTP_HEADERS_SENT|headers after they are sent|Cannot set headers/i.test(l)).length;
  rows.meta.logged_degraded_not_ready = logged.filter((l) => l.includes('DEGRADED') && l.includes('redis-not-ready')).length;
  rows.meta.logged_degraded_any = logged.filter((l) => l.includes('DEGRADED')).length;
  rows.meta.logged_command_failed = logged.filter((l) => l.includes('redis-command-failed')).length;
  rows.meta.logged_fallback_also_failed = logged.filter((l) => l.includes('ALSO failed')).length;
  rows.meta.logged_no_ratelimit_warn = logged.filter((l) => l.includes('has no rateLimit')).length;
  rows.meta.logged_plant = logged.filter((l) => l.includes('qa1017 plant')).length;
  rows.meta.rejections = rejections; rows.meta.uncaught = uncaught;
  rows.meta.fakeRedis = { calls: fakeRedis.calls, throws: fakeRedis.throws, pexpireAtCounts: [...new Set(fakeRedis.pexpireAt)] };
  rows.meta.bareHits = bareHits;
  rows.meta.auditRows = auditRows.length;
  if (OUT) fs.writeFileSync(OUT, JSON.stringify(rows, null, 1));
  await close(gw); await close(bare); await close(stub);
  vi.restoreAllMocks(); vi.unstubAllEnvs();
}, 30000);

type Route = { file: string; line: number; verb: string; path: string; url: string; authSites: number; optional: boolean; requireAdmin: boolean; idx: number; fromUse: boolean };
function extractRoutes(): Route[] {
  const src = path.resolve(__dirname, '..');
  const files = [src + '/index.ts', ...fs.readdirSync(src + '/routes').filter((x) => x.endsWith('.ts')).map((x) => src + '/routes/' + x), src + '/services/health.ts'];
  const PREFIX: Record<string, string> = { 'notifications.ts': '/api/notifications', 'batch.ts': '/api/batch', 'audit-export.ts': '/api/admin/audit' };
  const SKIP = new Set(['system-status.ts', 'health-dashboard.ts', 'versioning.ts']);
  const out: Route[] = []; const seenKey = new Set<string>();
  const push = (r: Omit<Route, 'idx' | 'url'>) => {
    const idx = out.length;
    const url = r.path.replace(/:([A-Za-z_]+)(\([^)]*\))?\??/g, `qam${idx}x`).replace(/\*/g, `qam${idx}x`);
    if (/[()?+]/.test(url)) return;
    const k = r.verb + ' ' + url.replace(/qam\d+x/g, 'P');
    if (seenKey.has(k)) return; seenKey.add(k);
    out.push({ ...r, url, idx });
  };
  for (const f of files) {
    const base = path.basename(f); if (SKIP.has(base)) continue;
    const text = fs.readFileSync(f, 'utf8');
    const re = /\b(router|app|erasureDoor)\.(get|post|put|patch|delete|all|use)\(\s*('([^']*)'|\[([^\]]*)\])/g;
    for (const m of text.matchAll(re)) {
      const lits = m[4] !== undefined ? [m[4]] : [...(m[5] || '').matchAll(/'([^']*)'/g)].map((x) => x[1]);
      const stmt = text.slice(m.index!, m.index! + 700).split(/\n\s*(?:router|app|erasureDoor)\.(?:get|post|put|patch|delete|all|use)\(/)[0];
      const line = text.slice(0, m.index!).split('\n').length;
      for (const lit of lits) {
        if (!lit.startsWith('/')) continue;
        let pre = PREFIX[base] || '';
        if (m[1] === 'erasureDoor') pre = '/api/gdpr';
        const full = (pre + (lit === '/' && pre ? '/' : lit)).replace(/\/\/+/g, '/');
        const common = { file: base, line, authSites: (stmt.match(/authenticateToken\(/g) || []).length, optional: /authenticateToken\(false\)/.test(stmt), requireAdmin: /requireAdmin/.test(stmt) };
        if (m[2] === 'use' || m[2] === 'all') {
          // a REAL method and sub-path for every prefix (GET-on-prefix can 405 at the spec method map)
          push({ ...common, verb: 'GET', path: full, fromUse: true });
          push({ ...common, verb: 'GET', path: (full + '/:sub').replace(/\/\/+/g, '/'), fromUse: true });
          push({ ...common, verb: 'POST', path: full, fromUse: true });
        } else {
          push({ ...common, verb: m[2].toUpperCase(), path: full, fromUse: false });
        }
      }
    }
  }
  return out;
}
async function pool<T>(items: T[], n: number, fn: (x: T) => Promise<void>) {
  let i = 0; await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) { const x = items[i++]; await fn(x); } }));
}
const NONMACHINE: Array<[string, () => Record<string, string>]> = [
  ...['email', 'wallet', 'federated', 'social', 'jwt', 'oauth'].map((am) => [`jwt_${am}`, () => ({ authorization: `Bearer ${sign({ authMethod: am })}` })] as [string, () => Record<string, string>]),
  ['jwt_no_authMethod', () => ({ authorization: `Bearer ${sign({})}` })],
  ['connector_jwt_as_bearer', () => ({ authorization: `Bearer ${jwt.sign({ userId: 'connector:qa1017-cj', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: 't-qa1017-cj' }, PRIV, { algorithm: 'RS256', expiresIn: 600 })}` })],
  ['test_token_email', () => ({ authorization: `Bearer ${testToken({ userId: 'tt-1', role: 'issuer', email: 'tt@example.test', authMethod: 'email', verificationLevel: 'standard' })}` })],
  ['non_sk_key_with_jwt_email', () => ({ 'x-api-key': 'pk_qa1017_notsk', authorization: `Bearer ${sign({ authMethod: 'email', userId: 'u-nonsk' })}` })],
];

describe('qa1017 gate probe', () => {
  it('census', async () => {
    if (!STAGES.includes('census')) return;
    const routes = extractRoutes();
    rows.meta.routes = routes.length;
    const tokens = Object.fromEntries(NONMACHINE.map(([n, f]) => [n, f()]));
    await pool(routes, 10, async (r) => {
      const mk = (p: string) => (r.url.includes(`qam${r.idx}x`) ? r.url.replace(new RegExp(`qam${r.idx}x`, 'g'), `qam${r.idx}-${p}`) : r.url + (r.url.includes('?') ? '&' : '?') + `qamark=qam${r.idx}-${p}`);
      const body = (p: string) => (r.verb === 'GET' || r.verb === 'DELETE' ? undefined : JSON.stringify({ title: `qam${r.idx}-${p}`, documentType: 'DOCUMENT', qam: `qam${r.idx}-${p}` }));
      const k = key(`sk_qa1017_c${r.idx}`, { connectorId: `qa1017-c${r.idx}`, scopes: ALL_SCOPES, organizationId: 'org-qa1017', tenantId: `t-qa1017-c${r.idx}`, rateLimit: 2, rateLimitWindow: 60 });
      const K: any[] = []; const Khits: number[] = [];
      for (let i = 0; i < 3; i++) { K.push(hdrs(await send(gwUrl, r.verb, mk('K'), { 'x-api-key': k }, body('K')))); Khits.push(hits(`qam${r.idx}-K`)); }
      const N = await send(gwUrl, r.verb, mk('N'), {}, body('N'));
      const I = await send(gwUrl, r.verb, mk('I'), { 'x-api-key': `sk_qa1017_unknown_${r.idx}` }, body('I'));
      const M = await send(gwUrl, r.verb, mk('M'), { authorization: 'Bearer not.a.jwt' }, body('M'));
      const d = key(`sk_qa1017_d${r.idx}`, { connectorId: `qa1017-d${r.idx}`, scopes: ALL_SCOPES, organizationId: 'org-qa1017', tenantId: `t-qa1017-d${r.idx}`, rateLimit: 1000, rateLimitWindow: 60 });
      const D = await send(gwUrl, r.verb, mk('D'), { 'x-api-key': d }, body('D'));
      const P: Record<string, any> = {};
      for (const [n] of NONMACHINE) { const x = await send(gwUrl, r.verb, mk('P' + n.replace(/_/g, '')), tokens[n], body('P' + n.replace(/_/g, ''))); P[n] = [x.status, x.h['x-ratelimit-limit'], x.h['x-ratelimit-remaining']]; }
      const C = await send(gwUrl, r.verb, mk('C'), { authorization: `Bearer ${sign({ authMethod: 'api_key', userId: `u-ctl-${r.idx}` })}` }, body('C'));
      const tenantFwd = [...new Set(seen.filter((x) => x.url.includes(`qam${r.idx}-K`) || x.body.includes(`qam${r.idx}-K`)).map((x) => String(x.headers['x-tenant-id'] ?? '')))];
      rows.census.push({ ...r, K, Khits, KtenantFwd: tenantFwd, N: [N.status, N.h['x-ratelimit-limit']], Nhits: hits(`qam${r.idx}-N`), I: [I.status, I.h['x-ratelimit-limit']], Ihits: hits(`qam${r.idx}-I`),
        M: [M.status, M.h['x-ratelimit-limit']], D: hdrs(D), Dhits: hits(`qam${r.idx}-D`), P, C: [C.status, C.h['x-ratelimit-limit'], C.h['x-ratelimit-remaining']] });
    });
    expect(rows.census.length).toBeGreaterThan(50);
  }, 600000);

  it('principals on GET /api/anchors (x4 each)', async () => {
    if (!STAGES.includes('principals')) return;
    const P: Array<[string, Record<string, string>]> = NONMACHINE.map(([n, f]) => [n, f()]);
    for (const am of ['api_key', 'oauth_app', 'API_KEY']) P.push([`jwt_${am}`, { authorization: `Bearer ${sign({ authMethod: am, userId: `u-pr-${am}` })}` }]);
    P.push(['test_token_api_key', { authorization: `Bearer ${testToken({ userId: 'tt-2', role: 'connector', email: 'tt2@example.test', authMethod: 'api_key', verificationLevel: 'api_key' })}` }]);
    P.push(['test_token_oauth_app', { authorization: `Bearer ${testToken({ userId: 'tt-3', role: 'connector', email: 'tt3@example.test', authMethod: 'oauth_app', verificationLevel: 'api_key' })}` }]);
    P.push(['api_key_limit2', { 'x-api-key': key('sk_qa1017_pr_key', { connectorId: 'qa1017-pr', scopes: ALL_SCOPES, tenantId: 't-qa1017-pr', rateLimit: 2, rateLimitWindow: 60 }) }]);
    P.push(['unknown_sk_key', { 'x-api-key': 'sk_qa1017_nope_pr' }]);
    P.push(['malformed_bearer', { authorization: 'Bearer not.a.jwt' }]);
    P.push(['no_credential', {}]);
    for (const [name, hdr] of P) {
      const rs: Res[] = [];
      for (let i = 0; i < 4; i++) rs.push(await send(gwUrl, 'GET', `/api/anchors/qapr-${name.replace(/_/g, '')}${i}`, hdr));
      let fwd = 0; for (let i = 0; i < 4; i++) fwd += hits(`qapr-${name.replace(/_/g, '')}${i}`);
      rows.principals.push({ name, statuses: rs.map((x) => x.status), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), stdRateLimit: rs.map((x) => x.h['ratelimit-limit'] ?? x.h['ratelimit']), fwd });
    }
    expect(rows.principals.length).toBe(P.length);
  }, 120000);

  it('a4: allowance variants', async () => {
    if (!STAGES.includes('a4')) return;
    const V: Array<[string, Record<string, unknown>]> = [
      ['rl_absent_w_absent', {}], ['rl_null', { rateLimit: null, rateLimitWindow: 60 }], ['rl_0_w_0', { rateLimit: 0, rateLimitWindow: 0 }], ['rl_NaN_via_json_null', { rateLimit: null, rateLimitWindow: null }],
      ['rl_2_w60', { rateLimit: 2, rateLimitWindow: 60 }], ['rl_1000_w3600_column_default', { rateLimit: 1000, rateLimitWindow: 3600 }], ['rl_1_schema_min', { rateLimit: 1, rateLimitWindow: 60 }], ['rl_10000_schema_max', { rateLimit: 10000, rateLimitWindow: 86400 }],
      ['rl_neg1', { rateLimit: -1, rateLimitWindow: 60 }], ['rl_1.5', { rateLimit: 1.5, rateLimitWindow: 60 }], ['rl_string_2', { rateLimit: '2', rateLimitWindow: 60 }], ['rl_string_abc', { rateLimit: 'abc', rateLimitWindow: 60 }],
      ['rl_true', { rateLimit: true, rateLimitWindow: 60 }], ['rl_2_w_null', { rateLimit: 2, rateLimitWindow: null }], ['rl_2_w_neg5', { rateLimit: 2, rateLimitWindow: -5 }],
      ['rl_2_w_string_abc', { rateLimit: 2, rateLimitWindow: 'abc' }], ['rl_1_w_0.001s', { rateLimit: 1, rateLimitWindow: 0.001 }],
    ];
    let n = 0;
    for (const [name, spec] of V) {
      n++;
      const k = key(`sk_qa1017_a4_${n}`, { connectorId: `qa1017-a4-${n}`, scopes: ALL_SCOPES, tenantId: 't-qa1017-a4', ...spec });
      const rs: Res[] = [];
      for (let i = 0; i < 4; i++) { rs.push(await send(gwUrl, 'GET', `/api/anchors/qaafour-n${n}i${i}`, { 'x-api-key': k })); if (name.startsWith('rl_1_w_0.001')) await new Promise((r) => setTimeout(r, 20)); }
      let fwd = 0; for (let i = 0; i < 4; i++) fwd += hits(`qaafour-n${n}i${i}`);
      rows.a4.push({ name, spec, statuses: rs.map((x) => x.status), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), retryAfter: rs.map((x) => x.h['retry-after']), fwd });
    }
    expect(rows.a4.length).toBe(V.length);
  }, 120000);

  it('keyscope: which requests share a bucket', async () => {
    if (!STAGES.includes('keyscope')) return;
    let s = 0;
    const seq = async (label: string, steps: Array<[string, string]>) => {
      const out: any[] = [];
      for (const [k, tag] of steps) { s++; const r = await send(gwUrl, 'GET', `/api/anchors/qaks-s${s}`, { 'x-api-key': k }); out.push([tag, r.status, r.h['x-ratelimit-limit'], r.h['x-ratelimit-remaining'], hits(`qaks-s${s}`)]); }
      rows.keyscope.push({ label, steps: out });
    };
    const a1 = key('sk_qa1017_ks_sameconn_A', { connectorId: 'qa1017-ks-shared', scopes: ALL_SCOPES, tenantId: 't-ks-a', rateLimit: 2, rateLimitWindow: 60 });
    const b1 = key('sk_qa1017_ks_sameconn_B', { connectorId: 'qa1017-ks-shared', scopes: ALL_SCOPES, tenantId: 't-ks-a', rateLimit: 5, rateLimitWindow: 60 });
    await seq('KS1_two_keys_one_connectorId_limits_2_and_5', [[a1, 'A'], [a1, 'A'], [a1, 'A'], [b1, 'B'], [b1, 'B'], [b1, 'B']]);
    const a2 = key('sk_qa1017_ks_noconn_tenantX', { scopes: ALL_SCOPES, tenantId: 't-ks-x', rateLimit: 2, rateLimitWindow: 60 });
    const b2 = key('sk_qa1017_ks_noconn_tenantY', { scopes: ALL_SCOPES, tenantId: 't-ks-y', rateLimit: 2, rateLimitWindow: 60 });
    const c2 = key('sk_qa1017_ks_emptyconn_tenantZ', { connectorId: '', scopes: ALL_SCOPES, tenantId: 't-ks-z', rateLimit: 1000, rateLimitWindow: 3600 });
    const d2 = key('sk_qa1017_ks_nullconn_tenantW', { connectorId: null, scopes: ALL_SCOPES, tenantId: 't-ks-w', rateLimit: 2, rateLimitWindow: 60 });
    await seq('KS2_keys_without_connectorId_in_different_tenants', [[a2, 'X'], [a2, 'X'], [b2, 'Y-first'], [c2, 'Z1000-first'], [d2, 'W-first']]);
    const a3 = key('sk_qa1017_ks_diffconn_A', { connectorId: 'qa1017-ks-p', scopes: ALL_SCOPES, tenantId: 't-ks-p', rateLimit: 2, rateLimitWindow: 60 });
    const b3 = key('sk_qa1017_ks_diffconn_B', { connectorId: 'qa1017-ks-q', scopes: ALL_SCOPES, tenantId: 't-ks-q', rateLimit: 2, rateLimitWindow: 60 });
    await seq('KS3_control_distinct_connectorIds_same_ip', [[a3, 'P'], [a3, 'P'], [a3, 'P'], [b3, 'Q'], [b3, 'Q']]);
    // KS4: a keyless key's bucket name collides with a JWT principal whose userId is literally connector:api-key? (clientId = connectorId || userId)
    const tokCollide = sign({ authMethod: 'api_key', userId: 'connector:api-key', tenantId: 't-ks-jwt' });
    const e2 = key('sk_qa1017_ks_noconn_tenantV', { scopes: ALL_SCOPES, tenantId: 't-ks-v', rateLimit: 3, rateLimitWindow: 60 });
    const out: any[] = [];
    for (let i = 0; i < 2; i++) { s++; const r = await send(gwUrl, 'GET', `/api/anchors/qaks-s${s}`, { authorization: `Bearer ${tokCollide}` }); out.push(['JWT-api_key-userId-connector:api-key', r.status, r.h['x-ratelimit-limit'], r.h['x-ratelimit-remaining']]); }
    s++; { const r = await send(gwUrl, 'GET', `/api/anchors/qaks-s${s}`, { 'x-api-key': e2 }); out.push(['V-keyless-first', r.status, r.h['x-ratelimit-limit'], r.h['x-ratelimit-remaining']]); }
    rows.keyscope.push({ label: 'KS4_bucket_name_after_KS2_state', steps: out });
    expect(rows.keyscope.length).toBe(4);
  }, 120000);

  it('erasure: real gdpr routes (KS-870), subjects:erase key and connector grace-role key', async () => {
    if (!STAGES.includes('erasure')) return;
    let s = 0;
    for (const [label, scopes] of [['scope_subjects_erase', ['subjects:erase']], ['grace_role_connector_no_scope', []]] as Array<[string, string[]]>) {
      for (const [route, method] of [['/api/gdpr/erasures', 'POST'], ['/api/gdpr/erasures/:ref', 'GET']] as Array<[string, string]>) {
        for (const limit of [2, 1000]) {
          s++;
          const k = key(`sk_qa1017_er_${s}`, { connectorId: `qa1017-er-${s}`, scopes, tenantId: 't-qa1017-er', rateLimit: limit, rateLimitWindow: 60 });
          const rs: Res[] = []; const hitsAfter: number[] = [];
          const n = limit === 2 ? 4 : 1;
          for (let i = 0; i < n; i++) {
            const mark = `qaer-s${s}i${i}`;
            const p = method === 'GET' ? `/api/gdpr/erasures/${mark}` : '/api/gdpr/erasures';
            rs.push(await send(gwUrl, method, p, { 'x-api-key': k }, method === 'POST' ? JSON.stringify({ externalRef: mark, reason: 'qa' }) : undefined));
            let t = 0; for (let j = 0; j <= i; j++) t += hits(`qaer-s${s}i${j}`); hitsAfter.push(t);
          }
          rows.erasure.push({ label, route: `${method} ${route}`, limit, statuses: rs.map((x) => x.status), codes: rs.map((x) => x.code), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), hitsAfter });
        }
      }
    }
    expect(rows.erasure.length).toBe(8);
  }, 120000);

  it('bare: A1 sync throw / async reject (key + JWT), A2 tenant (key, test token, JWT, super-admin override, interleaved), twice', async () => {
    if (!STAGES.includes('bare')) return;
    const ks = key('sk_qa1017_bare_sync', { connectorId: 'qa1017-bare-sync', scopes: [], tenantId: 't-bare', rateLimit: 1, rateLimitWindow: 60 });
    const s1 = await send(bareUrl, 'GET', '/sync-throw', { 'x-api-key': ks }); const s2 = await send(bareUrl, 'GET', '/sync-throw', { 'x-api-key': ks });
    rows.bare.push({ cell: 'A1_sync_throw_key_limit1', statuses: [s1.status, s2.status], remaining: [s1.h['x-ratelimit-remaining'], s2.h['x-ratelimit-remaining']], handlerHits: bareHits.sync });
    const sjTok = sign({ authMethod: 'api_key', userId: 'u-bare-jwt-machine' });
    const sj = await send(bareUrl, 'GET', '/sync-throw', { authorization: `Bearer ${sjTok}` });
    const sje = await send(bareUrl, 'GET', '/sync-throw', { authorization: `Bearer ${sign({ authMethod: 'email' })}` });
    rows.bare.push({ cell: 'A1_sync_throw_jwt_machine_and_email', statuses: [sj.status, sje.status], limit: [sj.h['x-ratelimit-limit'], sje.h['x-ratelimit-limit']], handlerHitsAfter: bareHits.sync });
    const ka = key('sk_qa1017_bare_async', { connectorId: 'qa1017-bare-async', scopes: [], tenantId: 't-bare', rateLimit: 1, rateLimitWindow: 60 });
    const r0 = rejections.length;
    const a1 = await send(bareUrl, 'GET', '/async-reject', { 'x-api-key': ka }, undefined, 1200); const a2 = await send(bareUrl, 'GET', '/async-reject', { 'x-api-key': ka }, undefined, 1200);
    await new Promise((r) => setTimeout(r, 50));
    rows.bare.push({ cell: 'A1_async_reject_key_limit1', statuses: [a1.status, a2.status], codes: [a1.code, a2.code], handlerHits: bareHits.async, rejectionsAdded: rejections.length - r0 });
    const r1 = rejections.length; const h1 = bareHits.async;
    const aj = await send(bareUrl, 'GET', '/async-reject', { authorization: `Bearer ${sign({ authMethod: 'email', userId: 'u-async-jwt' })}` }, undefined, 1200);
    await new Promise((r) => setTimeout(r, 50));
    rows.bare.push({ cell: 'A1_async_reject_jwt_email', statuses: [aj.status], handlerHitsAdded: bareHits.async - h1, rejectionsAdded: rejections.length - r1 });
    const kt = key('sk_qa1017_bare_tenant', { connectorId: 'qa1017-bare-tenant', scopes: [], tenantId: 't-bare-als', rateLimit: 50, rateLimitWindow: 60 });
    const t1 = await send(bareUrl, 'GET', '/tenant', { 'x-api-key': kt });
    const tj = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${sign({ authMethod: 'email', tenantId: 't-bare-jwt' })}` });
    const tjm = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${sign({ authMethod: 'api_key', userId: 'u-tenant-machine', tenantId: 't-bare-jwt-machine' })}` });
    const tt = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${testToken({ userId: 'tt-ten', role: 'issuer', email: 'tt@example.test', authMethod: 'email', verificationLevel: 'standard', tenantId: 't-bare-tt' })}` });
    const ttm = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${testToken({ userId: 'tt-ten-m', role: 'connector', email: 'tt@example.test', authMethod: 'api_key', verificationLevel: 'api_key', tenantId: 't-bare-tt-machine' })}` });
    const so = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${sign({ authMethod: 'email', role: 'super_admin', tenantId: 't-bare-sa-own' })}`, 'x-tenant-override': 't-bare-override' });
    const nso = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${sign({ authMethod: 'email', role: 'issuer', tenantId: 't-bare-issuer-own' })}`, 'x-tenant-override': 't-bare-override-refused' });
    rows.bare.push({ cell: 'A2_tenant', key: [t1.status, t1.json?.tenant, t1.h['x-ratelimit-limit']], jwt_email: [tj.status, tj.json?.tenant], jwt_machine: [tjm.status, tjm.json?.tenant, tjm.h['x-ratelimit-limit']], test_token_email: [tt.status, tt.json?.tenant],
      test_token_machine: [ttm.status, ttm.json?.tenant, ttm.h['x-ratelimit-limit']], super_admin_override: [so.status, so.json?.tenant], issuer_override_ignored: [nso.status, nso.json?.tenant] });
    const k3 = key('sk_qa1017_bare_il3', { connectorId: 'qa1017-bare-il3', scopes: [], tenantId: 't-il-3', rateLimit: 3, rateLimitWindow: 60 });
    const k100 = key('sk_qa1017_bare_il100', { connectorId: 'qa1017-bare-il100', scopes: [], tenantId: 't-il-100', rateLimit: 100, rateLimitWindow: 60 });
    await send(bareUrl, 'GET', '/tenant', { 'x-api-key': k3 }); await send(bareUrl, 'GET', '/tenant', { 'x-api-key': k100 });
    const par = await Promise.all(Array.from({ length: 24 }, (_, i) => send(bareUrl, 'GET', '/tenant', { 'x-api-key': i % 2 ? k100 : k3 }).then((r) => ({ k: i % 2 ? 't-il-100' : 't-il-3', status: r.status, tenant: r.json?.tenant ?? null }))));
    rows.bare.push({ cell: 'A2_interleaved_parallel_24', statusByKey: par.reduce((a: any, x) => { (a[x.k] ||= []).push(x.status); return a; }, {}),
      tenantMismatch: par.filter((x) => x.status === 200 && x.tenant !== x.k).length, allowed: par.filter((x) => x.status === 200).length, refused: par.filter((x) => x.status === 429).length });
    const kw = key('sk_qa1017_bare_twice', { connectorId: 'qa1017-bare-twice', scopes: [], tenantId: 't-bare', rateLimit: 2, rateLimitWindow: 60 });
    const tw: Res[] = []; for (let i = 0; i < 3; i++) tw.push(await send(bareUrl, 'GET', '/twice', { 'x-api-key': kw }));
    rows.bare.push({ cell: 'R3_twice_required_then_optional', statuses: tw.map((x) => x.status), remaining: tw.map((x) => x.h['x-ratelimit-remaining']) });
    expect(rows.bare.length).toBe(7);
  }, 120000);

  it('plant: next() throws synchronously on its first call (bare /plant) — API key and JWT branches; direct limiter call', async () => {
    if (!STAGES.includes('plant')) return;
    const kp = key('sk_qa1017_plant_key', { connectorId: 'qa1017-plant-key', scopes: [], tenantId: 't-plant', rateLimit: 5, rateLimitWindow: 60 });
    const n0 = bareHits.plantNext; const hd0 = bareHits.plantHandler; const r0 = rejections.length; const u0 = uncaught.length;
    const p1 = await send(bareUrl, 'GET', '/plant', { 'x-api-key': kp }, undefined, 1200);
    await new Promise((r) => setTimeout(r, 50));
    const p2 = await send(bareUrl, 'GET', '/plant', { 'x-api-key': kp }, undefined, 1200);
    await new Promise((r) => setTimeout(r, 50));
    rows.plant.push({ cell: 'plant_key_limit5_two_requests', statuses: [p1.status, p2.status], remaining: [p1.h['x-ratelimit-remaining'], p2.h['x-ratelimit-remaining']], bodies: [p1.json, p2.json], nextCallsAdded: bareHits.plantNext - n0, handlerRunsAdded: bareHits.plantHandler - hd0, rejectionsAdded: rejections.length - r0, uncaughtAdded: uncaught.length - u0 });
    for (const [label, tok] of [['jwt_email', sign({ authMethod: 'email', userId: 'u-plant-e' })], ['jwt_api_key', sign({ authMethod: 'api_key', userId: 'u-plant-m' })]] as Array<[string, string]>) {
      const n1 = bareHits.plantNext; const hd1 = bareHits.plantHandler; const r1 = rejections.length; const u1 = uncaught.length;
      const pj = await send(bareUrl, 'GET', '/plant', { authorization: `Bearer ${tok}` }, undefined, 1200);
      await new Promise((r) => setTimeout(r, 50));
      rows.plant.push({ cell: `plant_${label}`, status: pj.status, code: pj.code, limit: pj.h['x-ratelimit-limit'], remaining: pj.h['x-ratelimit-remaining'], body: pj.json, nextCallsAdded: bareHits.plantNext - n1, handlerRunsAdded: bareHits.plantHandler - hd1, rejectionsAdded: rejections.length - r1, uncaughtAdded: uncaught.length - u1 });
    }
    // Direct call of a fresh limiter instance, in-memory path, fake req/res.
    const lim = rle.enforceClientRateLimit(null);
    const hset: Record<string, string> = {}; let statusSet: number | null = null; let jsonCalls = 0;
    const res: any = { setHeader: (k: string, v: string) => { hset[k] = v; }, status: (s: number) => { statusSet = s; return res; }, json: () => { jsonCalls++; return res; }, headersSent: false };
    const req: any = { user: { authMethod: 'api_key', connectorId: 'qa1017-plant-direct', rateLimit: 10, rateLimitWindow: 60 } };
    let nc = 0; let threwOut = false;
    try { await lim(req, res, () => { nc++; if (nc === 1) throw new Error('qa1017 plant direct'); }); } catch { threwOut = true; }
    rows.plant.push({ cell: 'plant_direct_limiter_in_memory', nextCalls: nc, remainingHeader: hset['X-RateLimit-Remaining'], statusSet, jsonCalls, threwOut });
    expect(rows.plant.length).toBe(4);
  }, 60000);

  it('redisthrow: mid-command throw on the fake client (KS-616) through the continuation', async () => {
    if (!STAGES.includes('redisthrow')) return;
    const k = key('sk_qa1017_rt', { connectorId: 'qa-throw-conn', scopes: ALL_SCOPES, tenantId: 't-rt', rateLimit: 2, rateLimitWindow: 60 });
    const rs: Res[] = []; const hitsAfter: number[] = [];
    for (let i = 0; i < 4; i++) { rs.push(await send(gwUrl, 'GET', `/api/anchors/qart-i${i}`, { 'x-api-key': k })); let t = 0; for (let j = 0; j <= i; j++) t += hits(`qart-i${j}`); hitsAfter.push(t); }
    rows.redisthrow.push({ statuses: rs.map((x) => x.status), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), hitsAfter, fakeThrows: fakeRedis.throws });
    expect(rows.redisthrow.length).toBe(1);
  }, 60000);

  it('order: validate / exchange / forward / audit per allowed vs refused, cached vs uncached (two keys, one connectorId); two tenants interleaved', async () => {
    if (!STAGES.includes('order')) return;
    const A = key('sk_qa1017_ord_A', { connectorId: 'qa1017-ord', scopes: ALL_SCOPES, tenantId: 't-ord-a', organizationId: 'org-ord', rateLimit: 1, rateLimitWindow: 60 });
    const B = key('sk_qa1017_ord_B', { connectorId: 'qa1017-ord', scopes: ALL_SCOPES, tenantId: 't-ord-b', organizationId: 'org-ord', rateLimit: 1, rateLimitWindow: 60 });
    let s = 0;
    const step = async (label: string, k: string, method: string, p: (m: string) => string, withBody: boolean) => {
      s++; const mark = `qaord-s${s}`;
      const a0 = auditRows.length; const v0 = calls('/api/keys/validate', k); const t0 = calls('/internal/connector-token', k);
      const r = await send(gwUrl, method, p(mark), { 'x-api-key': k }, withBody ? JSON.stringify({ title: mark, documentType: 'DOCUMENT' }) : undefined);
      await new Promise((res) => setTimeout(res, 80));
      const added = auditRows.slice(a0);
      rows.order.push({ label, status: r.status, code: r.code, remaining: r.h['x-ratelimit-remaining'], validateCalls: calls('/api/keys/validate', k) - v0, exchangeCalls: calls('/internal/connector-token', k) - t0,
        forwarded: hits(mark), auditRowsAdded: added.length, auditParams: added.map((x) => JSON.stringify(x.params).slice(0, 600)) });
    };
    await step('A_post_1_uncached_allowed', A, 'POST', () => '/api/documents', true);
    await step('A_post_2_cached_refused', A, 'POST', () => '/api/documents', true);
    await step('B_post_1_uncached_refused_same_connector', B, 'POST', () => '/api/documents', true);
    await step('B_post_2_cached_refused', B, 'POST', () => '/api/documents', true);
    await step('A_get_anchors_refused', A, 'GET', (m) => `/api/anchors/${m}`, false);
    expect(rows.order.length).toBe(5);
  }, 120000);

  it('perip: the per-IP limiters at their DEFAULT maxima (QA_PERIP=1 only)', async () => {
    if (!STAGES.includes('perip')) return;
    expect(PERIP).toBe(true);
    // verification limiter: no credential, public path; default non-prod 600/min per IP
    let first429 = -1; let last: Res | null = null; const statusCounts: Record<string, number> = {};
    for (let i = 1; i <= 605; i++) {
      const r = await send(gwUrl, 'GET', `/api/verification/qaperip-v${i}`, {});
      statusCounts[r.status] = (statusCounts[r.status] || 0) + 1;
      if (r.status === 429 && first429 < 0) { first429 = i; last = r; }
    }
    rows.perip.push({ limiter: 'verification (index.ts:509-520)', requests: 605, first429, statusCounts, headersAt429: last ? last.h : null, code: last?.code ?? null });
    // global limiter: an authenticated-looking machine key on a proxied GET (default non-prod 10000/min)
    const kg = key('sk_qa1017_perip_g', { connectorId: 'qa1017-perip-g', scopes: ALL_SCOPES, tenantId: 't-perip', rateLimit: 1000000, rateLimitWindow: 60 });
    let g429 = -1; let gl: Res | null = null; const gCounts: Record<string, number> = {}; let firstStd: string | null = null; let firstX: string | null = null;
    const N = 10003; let i = 0;
    await pool(Array.from({ length: N }, (_, j) => j + 1), 24, async (j) => {
      const r = await send(gwUrl, 'GET', `/api/anchors/qaperip-g${j}`, { 'x-api-key': kg });
      i++; gCounts[r.status] = (gCounts[r.status] || 0) + 1;
      if (j === 1) { firstStd = r.h['ratelimit-limit'] ?? r.h['ratelimit'] ?? null; firstX = r.h['x-ratelimit-limit']; }
      if (r.status === 429 && g429 < 0) { g429 = i; gl = r; }
    });
    rows.perip.push({ limiter: 'global (index.ts:490-502), sk_ key on GET /api/anchors/*', requests: N, first429AtCompletedCount: g429, statusCounts: gCounts, firstStdHeader: firstStd, firstXRateLimit: firstX, headersAt429: gl ? (gl as Res).h : null, code: gl ? (gl as Res).code : null });
  }, 300000);
});
