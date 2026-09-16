/**
 * qa1017-drafter-probe.test.ts — Wednesday's #1017 (KS-1195) gate DRAFTER probe. Copied into a drafter clone's api-gateway src/__tests__,
 * run SOLO, quarantined by rename. Rows -> process.env.QA_OUT (JSON). PREDICTIONS ONLY: the gate re-measures every row.
 *
 * Stages (QA_STAGES, comma list; default all but 'order'):
 *   census    — every literal route path in index.ts / routes/*.ts / services/health.ts on the REAL index.ts app; per route:
 *               K = a FRESH key (own connectorId, limit 2 / 60 s) x 3 sequential requests (status, X-RateLimit-*, Retry-After,
 *               upstream hits by marker), J = an RS256 JWT authMethod email x 2 (X-RateLimit-Limit present?), N = no credential x 1,
 *               I = an unknown sk_ key x 1. Remaining after request 1: 1 = counted once, 0 = counted twice (double authentication).
 *   principals— GET /api/anchors/<m> x 4 per principal: JWT authMethod email/wallet/federated/social/jwt/oauth/(absent)/api_key/oauth_app/API_KEY,
 *               a connector JWT (type connector, no authMethod), a test token (email / api_key), key, unknown key, non-sk key, none.
 *   a4        — which allowance a key gets: the validate response's rateLimit / rateLimitWindow variants.
 *   keyscope  — two keys one connectorId; two keys with NO connectorId in different tenants; different connectorIds (control).
 *   erasure   — POST /api/gdpr/erasures (KS-870 admitted double authentication) x 4, limit 2.
 *   bare      — the REAL authenticateToken on a bare express app: sync throw / async reject downstream (A1), tenant context (A2),
 *               interleaved keys under latency (A2 under 429).
 *   order     — (QA_AUDIT=1 mocks ../db isDbAvailable true + captures audit INSERTs) validate / token exchange / originate / audit per
 *               allowed vs refused request, two keys sharing one connectorId.
 * QA_FAKE_REDIS=1: vi.mock('../services/redis') getRedisClient -> an in-process async fake with status 'ready' (NOT the real ioredis client).
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
const STAGES = (process.env.QA_STAGES || 'census,principals,a4,keyscope,erasure,bare').split(',');

const fakeRedis = { calls: 0, store: new Map<string, { n: number; exp: number }>(), status: 'ready' as string,
  async incr(k: string) { this.calls++; await new Promise((r) => setTimeout(r, 3)); const e = this.store.get(k); const now = Date.now();
    if (!e || (e.exp && now > e.exp)) { this.store.set(k, { n: 1, exp: 0 }); return 1; } e.n++; return e.n; },
  async pexpire(k: string, ms: number) { this.calls++; await new Promise((r) => setTimeout(r, 2)); const e = this.store.get(k); if (e) e.exp = Date.now() + ms; return 1; },
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
    if (/INSERT INTO audit_logs/i.test(sql)) (globalThis as any).__qaAuditRows.push({ params, at: Date.now() });
    return { rows: [], rowCount: 0 };
  } };
});

type Rec = { method: string; url: string; headers: http.IncomingHttpHeaders; body: string };
const seen: Rec[] = [];
const logged: string[] = [];
const KEYS = new Map<string, Record<string, unknown>>();
let ALL_SCOPES: string[] = [];

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
type Res = { status: number; code: string | null; h: Record<string, string | null>; json: any };
const H = ['x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset', 'retry-after', 'ratelimit-limit', 'ratelimit'];
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
const hits = (marker: string) => seen.filter((r) => r.url !== '/api/keys/validate' && r.url !== '/internal/connector-token' && (r.url.includes(marker) || r.body.includes(marker))).length;
const calls = (url: string, bodyIncludes: string) => seen.filter((r) => r.url === url && r.body.includes(bodyIncludes)).length;
function key(name: string, spec: Record<string, unknown>) { KEYS.set(name, spec); return name; }

let stub: http.Server; let stubUrl = '';
let gw: http.Server; let gwUrl = '';
let bare: http.Server; let bareUrl = '';
const rows: Record<string, any> = { meta: {}, census: [], principals: [], a4: [], keyscope: [], erasure: [], bare: [], order: [] };
const bareHits: Record<string, number> = { sync: 0, async: 0, tenant: 0 };
const rejections: string[] = [];
let redisMod: any; let shared: any;

beforeAll(async () => {
  expect(PRIV.length).toBeGreaterThan(100);
  stub = http.createServer(async (req, res) => {
    const body = await readBody(req);
    seen.push({ method: req.method || '', url: req.url || '', headers: { ...req.headers }, body });
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
  vi.stubEnv('RATE_LIMIT_MAX_REQUESTS', '1000000');
  vi.stubEnv('VERIFICATION_RATE_LIMIT_MAX', '1000000');
  for (const n of ['ORIGINATE', 'WALLET', 'AUTH', 'SECURITY', 'ANCHORING', 'TIMESTAMPING', 'PRISM', 'VC_ISSUER', 'STAKING', 'REFERRAL', 'TRANSFER', 'KYC', 'GOVERNANCE', 'NFT', 'BILLING', 'ANALYTICS', 'NOTIFICATION']) vi.stubEnv(`${n}_SERVICE_URL`, stubUrl);
  vi.stubEnv('TENANT_PROVISIONING_URL', stubUrl); vi.stubEnv('TOKENISATION_URL', stubUrl); vi.stubEnv('MCP_SERVER_URL', stubUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;
  process.on('unhandledRejection', (r) => { rejections.push(String((r as Error)?.message || r).slice(0, 120)); });

  const app = (await import('../index')).default;
  redisMod = await import('../services/redis');
  const auth = await import('../middleware/auth');
  shared = await import('@secuura/shared');
  const { logger } = await import('../utils/logger');
  for (const level of ['error', 'warn'] as const) {
    vi.spyOn(logger, level).mockImplementation(((...a: unknown[]) => { logged.push(a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); return logger; }) as any);
  }
  vi.spyOn(console, 'error').mockImplementation((...a: unknown[]) => { logged.push(a.map(String).join(' ')); });
  vi.spyOn(console, 'warn').mockImplementation((...a: unknown[]) => { logged.push(a.map(String).join(' ')); });
  gw = http.createServer(app as http.RequestListener);
  gwUrl = await listen(gw);

  const b = express();
  b.get('/sync-throw', auth.authenticateToken(true), () => { bareHits.sync += 1; throw new Error('qa1017 sync throw downstream'); });
  b.get('/async-reject', auth.authenticateToken(true), (async () => { bareHits.async += 1; await new Promise((r) => setTimeout(r, 5)); throw new Error('qa1017 async reject downstream'); }) as any);
  b.get('/tenant', auth.authenticateToken(true), async (req: any, s) => { bareHits.tenant += 1; await new Promise((r) => setTimeout(r, 4)); s.status(200).json({ tenant: shared.currentTenantId() ?? null, user: req.user?.userId ?? null }); });
  b.get('/twice', auth.authenticateToken(true), auth.authenticateToken(false), (_q, s) => { s.status(200).json({ ok: true }); });
  bare = http.createServer(b);
  bareUrl = await listen(bare);

  const src = path.resolve(__dirname, '..');
  const scopeSet = new Set<string>();
  for (const f of [src + '/index.ts', ...fs.readdirSync(src + '/routes').map((x) => src + '/routes/' + x), src + '/services/health.ts']) {
    for (const m of fs.readFileSync(f, 'utf8').matchAll(/'([a-z_]+:[a-z_*]+)'/g)) scopeSet.add(m[1]);
  }
  ALL_SCOPES = [...scopeSet].sort();
  rows.meta = { stubUrl: 'loopback', redisAvailable: redisMod.isRedisAvailable(), fakeRedis: process.env.QA_FAKE_REDIS === '1', audit: process.env.QA_AUDIT === '1', scopes: ALL_SCOPES.length, stages: STAGES,
    at: new Date().toISOString() };
}, 60000);

afterAll(async () => {
  rows.meta.logged_headers_sent = logged.filter((l) => /ERR_HTTP_HEADERS_SENT|headers after they are sent/i.test(l)).length;
  rows.meta.logged_degraded = logged.filter((l) => l.includes('DEGRADED')).length;
  rows.meta.logged_no_ratelimit_warn = logged.filter((l) => l.includes('has no rateLimit')).length;
  rows.meta.rejections = rejections;
  rows.meta.fakeRedisCalls = fakeRedis.calls;
  rows.meta.bareHits = bareHits;
  rows.meta.auditRows = auditRows.length;
  if (OUT) fs.writeFileSync(OUT, JSON.stringify(rows, null, 1));
  await close(gw); await close(bare); await close(stub);
  vi.restoreAllMocks(); vi.unstubAllEnvs();
}, 30000);

type Route = { file: string; line: number; verb: string; path: string; url: string; authSites: number; optional: boolean; requireAdmin: boolean; idx: number };
function extractRoutes(): Route[] {
  const src = path.resolve(__dirname, '..');
  const files = [src + '/index.ts', ...fs.readdirSync(src + '/routes').filter((x) => x.endsWith('.ts')).map((x) => src + '/routes/' + x), src + '/services/health.ts'];
  const PREFIX: Record<string, string> = { 'notifications.ts': '/api/notifications', 'batch.ts': '/api/batch', 'audit-export.ts': '/api/admin/audit' };
  const SKIP = new Set(['system-status.ts', 'health-dashboard.ts', 'versioning.ts']);
  const out: Route[] = []; const seenKey = new Set<string>();
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
        let full = (pre + (lit === '/' && pre ? '/' : lit)).replace(/\/\/+/g, '/');
        const verb = (m[2] === 'use' || m[2] === 'all') ? 'GET' : m[2].toUpperCase();
        const idx = out.length;
        const url = full.replace(/:([A-Za-z_]+)(\([^)]*\))?\??/g, `qam${idx}x`).replace(/\*/g, `qam${idx}x`);
        if (/[()?+]/.test(url)) continue;
        const k = verb + ' ' + url.replace(/qam\d+x/g, 'P');
        if (seenKey.has(k)) continue; seenKey.add(k);
        out.push({ file: base, line, verb, path: full, url, authSites: (stmt.match(/authenticateToken\(/g) || []).length, optional: /authenticateToken\(false\)/.test(stmt), requireAdmin: /requireAdmin/.test(stmt), idx });
      }
    }
  }
  return out;
}
async function pool<T>(items: T[], n: number, fn: (x: T) => Promise<void>) {
  let i = 0; await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) { const x = items[i++]; await fn(x); } }));
}

describe('qa1017 drafter probe', () => {
  it('census: every literal route x {fresh key x3, JWT x2, none, unknown key}', async () => {
    if (!STAGES.includes('census')) return;
    const routes = extractRoutes();
    rows.meta.routes = routes.length;
    await pool(routes, 12, async (r) => {
      const mk = (p: string) => (r.url.includes(`qam${r.idx}x`) ? r.url.replace(new RegExp(`qam${r.idx}x`, 'g'), `qam${r.idx}${p}`) : r.url + (r.url.includes('?') ? '&' : '?') + `qamark=qam${r.idx}${p}`);
      const body = (p: string) => (r.verb === 'GET' || r.verb === 'DELETE' ? undefined : JSON.stringify({ title: `qam${r.idx}${p}`, documentType: 'DOCUMENT', qam: `qam${r.idx}${p}` }));
      const k = key(`sk_qa1017_c${r.idx}`, { connectorId: `qa1017-c${r.idx}`, scopes: ALL_SCOPES, organizationId: 'org-qa1017', tenantId: `t-qa1017-c${r.idx}`, rateLimit: 2, rateLimitWindow: 60 });
      const K: Res[] = [];
      for (let i = 0; i < 3; i++) K.push(await send(gwUrl, r.verb, mk('K'), { 'x-api-key': k }, body('K')));
      const tok = sign({ authMethod: 'email' });
      const J: Res[] = [];
      for (let i = 0; i < 2; i++) J.push(await send(gwUrl, r.verb, mk('J'), { authorization: `Bearer ${tok}` }, body('J')));
      const N = await send(gwUrl, r.verb, mk('N'), {}, body('N'));
      const I = await send(gwUrl, r.verb, mk('I'), { 'x-api-key': `sk_qa1017_unknown_${r.idx}` }, body('I'));
      const tenantFwd = [...new Set(seen.filter((x) => x.url.includes(`qam${r.idx}K`)).map((x) => String(x.headers['x-tenant-id'] ?? '')))];
      rows.census.push({ ...r, K: K.map((x) => [x.status, x.code, x.h['x-ratelimit-limit'], x.h['x-ratelimit-remaining'], x.h['retry-after'] ? 'RA' : null]), Khits: hits(`qam${r.idx}K`), KtenantFwd: tenantFwd,
        J: J.map((x) => [x.status, x.h['x-ratelimit-limit']]), Jhits: hits(`qam${r.idx}J`), N: [N.status, N.h['x-ratelimit-limit']], Nhits: hits(`qam${r.idx}N`), I: [I.status, I.h['x-ratelimit-limit']], Ihits: hits(`qam${r.idx}I`) });
    });
    expect(rows.census.length).toBeGreaterThan(50);
  }, 600000);

  it('principals on GET /api/anchors (x4 each)', async () => {
    if (!STAGES.includes('principals')) return;
    const P: Array<[string, Record<string, string>]> = [];
    for (const am of ['email', 'wallet', 'federated', 'social', 'jwt', 'oauth', 'api_key', 'oauth_app', 'API_KEY']) P.push([`jwt_${am}`, { authorization: `Bearer ${sign({ authMethod: am })}` }]);
    P.push(['jwt_no_authMethod', { authorization: `Bearer ${sign({})}` }]);
    P.push(['connector_jwt_as_bearer', { authorization: `Bearer ${jwt.sign({ userId: 'connector:qa1017-cj', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: 't-qa1017-cj' }, PRIV, { algorithm: 'RS256', expiresIn: 600 })}` }]);
    P.push(['test_token_email', { authorization: 'Bearer test_token_' + Buffer.from(JSON.stringify({ userId: 'tt-1', role: 'issuer', email: 'tt@example.test', authMethod: 'email', verificationLevel: 'standard' })).toString('base64') }]);
    P.push(['test_token_api_key', { authorization: 'Bearer test_token_' + Buffer.from(JSON.stringify({ userId: 'tt-2', role: 'connector', email: 'tt2@example.test', authMethod: 'api_key', verificationLevel: 'api_key' })).toString('base64') }]);
    P.push(['api_key_limit2', { 'x-api-key': key('sk_qa1017_pr_key', { connectorId: 'qa1017-pr', scopes: ALL_SCOPES, tenantId: 't-qa1017-pr', rateLimit: 2, rateLimitWindow: 60 }) }]);
    P.push(['unknown_sk_key', { 'x-api-key': 'sk_qa1017_nope_pr' }]);
    P.push(['non_sk_key_with_jwt_email', { 'x-api-key': 'pk_qa1017_notsk', authorization: `Bearer ${sign({ authMethod: 'email', userId: 'u-nonsk' })}` }]);
    P.push(['no_credential', {}]);
    for (const [name, hdr] of P) {
      const rs: Res[] = [];
      for (let i = 0; i < 4; i++) rs.push(await send(gwUrl, 'GET', `/api/anchors/qapr-${name}-${i}`, hdr));
      rows.principals.push({ name, statuses: rs.map((x) => x.status), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), fwd: hits(`qapr-${name}-`) });
    }
    expect(rows.principals.length).toBe(P.length);
  }, 120000);

  it('a4: allowance variants from the validate response', async () => {
    if (!STAGES.includes('a4')) return;
    const V: Array<[string, Record<string, unknown>]> = [
      ['rl_absent_w_absent', {}], ['rl_null', { rateLimit: null, rateLimitWindow: 60 }], ['rl_0_column_null_via_Number', { rateLimit: 0, rateLimitWindow: 0 }],
      ['rl_2_w60', { rateLimit: 2, rateLimitWindow: 60 }], ['rl_1000_w3600_column_default', { rateLimit: 1000, rateLimitWindow: 3600 }], ['rl_neg1', { rateLimit: -1, rateLimitWindow: 60 }],
      ['rl_1.5', { rateLimit: 1.5, rateLimitWindow: 60 }], ['rl_string_2', { rateLimit: '2', rateLimitWindow: 60 }], ['rl_string_abc', { rateLimit: 'abc', rateLimitWindow: 60 }],
      ['rl_true', { rateLimit: true, rateLimitWindow: 60 }], ['rl_2_w_null', { rateLimit: 2, rateLimitWindow: null }], ['rl_2_w_neg5', { rateLimit: 2, rateLimitWindow: -5 }],
      ['rl_2_w_string_abc', { rateLimit: 2, rateLimitWindow: 'abc' }], ['rl_1_w_0.001s', { rateLimit: 1, rateLimitWindow: 0.001 }],
    ];
    let n = 0;
    for (const [name, spec] of V) {
      n++;
      const k = key(`sk_qa1017_a4_${n}`, { connectorId: `qa1017-a4-${n}`, scopes: ALL_SCOPES, tenantId: 't-qa1017-a4', ...spec });
      const rs: Res[] = [];
      for (let i = 0; i < 4; i++) { rs.push(await send(gwUrl, 'GET', `/api/anchors/qaa4-${n}-${i}`, { 'x-api-key': k })); if (name.startsWith('rl_1_w_0.001')) await new Promise((r) => setTimeout(r, 20)); }
      rows.a4.push({ name, spec, statuses: rs.map((x) => x.status), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), retryAfter: rs.map((x) => x.h['retry-after']), fwd: hits(`qaa4-${n}-`) });
    }
    expect(rows.a4.length).toBe(V.length);
  }, 120000);

  it('keyscope: which requests share a bucket', async () => {
    if (!STAGES.includes('keyscope')) return;
    const seq = async (label: string, steps: Array<[string, string]>) => {
      const out: any[] = [];
      for (const [k, tag] of steps) { const r = await send(gwUrl, 'GET', `/api/anchors/qaks-${label}-${out.length}`, { 'x-api-key': k }); out.push([tag, r.status, r.h['x-ratelimit-limit'], r.h['x-ratelimit-remaining']]); }
      rows.keyscope.push({ label, steps: out });
    };
    const a1 = key('sk_qa1017_ks_sameconn_A', { connectorId: 'qa1017-ks-shared', scopes: ALL_SCOPES, tenantId: 't-ks-a', rateLimit: 2, rateLimitWindow: 60 });
    const b1 = key('sk_qa1017_ks_sameconn_B', { connectorId: 'qa1017-ks-shared', scopes: ALL_SCOPES, tenantId: 't-ks-a', rateLimit: 5, rateLimitWindow: 60 });
    await seq('KS1_two_keys_one_connectorId_limits_2_and_5', [[a1, 'A'], [a1, 'A'], [a1, 'A'], [b1, 'B'], [b1, 'B'], [b1, 'B']]);
    const a2 = key('sk_qa1017_ks_noconn_tenantX', { scopes: ALL_SCOPES, tenantId: 't-ks-x', rateLimit: 2, rateLimitWindow: 60 });
    const b2 = key('sk_qa1017_ks_noconn_tenantY', { scopes: ALL_SCOPES, tenantId: 't-ks-y', rateLimit: 2, rateLimitWindow: 60 });
    const c2 = key('sk_qa1017_ks_emptyconn_tenantZ', { connectorId: '', scopes: ALL_SCOPES, tenantId: 't-ks-z', rateLimit: 1000, rateLimitWindow: 3600 });
    const d2 = key('sk_qa1017_ks_nullconn_tenantW', { connectorId: null, scopes: ALL_SCOPES, tenantId: 't-ks-w', rateLimit: 2, rateLimitWindow: 60 });
    await seq('KS2_keys_without_connectorId_in_different_tenants', [[a2, 'X'], [a2, 'X'], [b2, 'Y'], [c2, 'Z1000'], [d2, 'W']]);
    const a3 = key('sk_qa1017_ks_diffconn_A', { connectorId: 'qa1017-ks-p', scopes: ALL_SCOPES, tenantId: 't-ks-p', rateLimit: 2, rateLimitWindow: 60 });
    const b3 = key('sk_qa1017_ks_diffconn_B', { connectorId: 'qa1017-ks-q', scopes: ALL_SCOPES, tenantId: 't-ks-q', rateLimit: 2, rateLimitWindow: 60 });
    await seq('KS3_control_distinct_connectorIds_same_ip', [[a3, 'P'], [a3, 'P'], [a3, 'P'], [b3, 'Q'], [b3, 'Q']]);
    expect(rows.keyscope.length).toBe(3);
  }, 120000);

  it('erasure: POST /api/gdpr/erasures (KS-870 admitted double authentication)', async () => {
    if (!STAGES.includes('erasure')) return;
    for (const [label, limit] of [['limit2', 2], ['limit1000', 1000]] as Array<[string, number]>) {
      const k = key(`sk_qa1017_er_${label}`, { connectorId: `qa1017-er-${label}`, scopes: ALL_SCOPES, tenantId: 't-qa1017-er', rateLimit: limit, rateLimitWindow: 60 });
      const rs: Res[] = [];
      for (let i = 0; i < 4; i++) rs.push(await send(gwUrl, 'POST', '/api/gdpr/erasures', { 'x-api-key': k }, JSON.stringify({ externalRef: `qaer-${label}-${i}`, reason: 'qa' })));
      const noScope = key(`sk_qa1017_er_noscope_${label}`, { connectorId: `qa1017-er-ns-${label}`, scopes: [], tenantId: 't-qa1017-er', rateLimit: limit, rateLimitWindow: 60 });
      const ns = await send(gwUrl, 'POST', '/api/gdpr/erasures', { 'x-api-key': noScope }, JSON.stringify({ externalRef: `qaerns-${label}`, reason: 'qa' }));
      rows.erasure.push({ label, statuses: rs.map((x) => x.status), codes: rs.map((x) => x.code), xrlLimit: rs.map((x) => x.h['x-ratelimit-limit']), remaining: rs.map((x) => x.h['x-ratelimit-remaining']), fwd: hits(`qaer-${label}-`),
        noScopeGraceRole: [ns.status, ns.code, ns.h['x-ratelimit-remaining'], hits(`qaerns-${label}`)] });
    }
    expect(rows.erasure.length).toBe(2);
  }, 120000);

  it('bare: A1 sync throw / async reject, A2 tenant (incl. interleaved under 429), double authentication control', async () => {
    if (!STAGES.includes('bare')) return;
    const ks = key('sk_qa1017_bare_sync', { connectorId: 'qa1017-bare-sync', scopes: [], tenantId: 't-bare', rateLimit: 1, rateLimitWindow: 60 });
    const s1 = await send(bareUrl, 'GET', '/sync-throw', { 'x-api-key': ks }); const s2 = await send(bareUrl, 'GET', '/sync-throw', { 'x-api-key': ks });
    rows.bare.push({ cell: 'A1_sync_throw_limit1', statuses: [s1.status, s2.status], xrl: [s1.h['x-ratelimit-remaining'], s2.h['x-ratelimit-remaining']], handlerHits: bareHits.sync });
    const tokS = sign({ authMethod: 'email', userId: 'u-bare-jwt' });
    const sj = await send(bareUrl, 'GET', '/sync-throw', { authorization: `Bearer ${tokS}` });
    rows.bare.push({ cell: 'A1_sync_throw_jwt', statuses: [sj.status], handlerHitsAfter: bareHits.sync });
    const ka = key('sk_qa1017_bare_async', { connectorId: 'qa1017-bare-async', scopes: [], tenantId: 't-bare', rateLimit: 1, rateLimitWindow: 60 });
    const a1 = await send(bareUrl, 'GET', '/async-reject', { 'x-api-key': ka }, undefined, 1500); const a2 = await send(bareUrl, 'GET', '/async-reject', { 'x-api-key': ka }, undefined, 1500);
    await new Promise((r) => setTimeout(r, 50));
    rows.bare.push({ cell: 'A1_async_reject_limit1', statuses: [a1.status, a2.status], codes: [a1.code, a2.code], handlerHits: bareHits.async, rejections: rejections.length });
    const kt = key('sk_qa1017_bare_tenant', { connectorId: 'qa1017-bare-tenant', scopes: [], tenantId: 't-bare-als', rateLimit: 50, rateLimitWindow: 60 });
    const t1 = await send(bareUrl, 'GET', '/tenant', { 'x-api-key': kt });
    const tj = await send(bareUrl, 'GET', '/tenant', { authorization: `Bearer ${sign({ authMethod: 'email', tenantId: 't-bare-jwt' })}` });
    rows.bare.push({ cell: 'A2_tenant_key_and_jwt', key: [t1.status, t1.json], jwt: [tj.status, tj.json] });
    const k3 = key('sk_qa1017_bare_il3', { connectorId: 'qa1017-bare-il3', scopes: [], tenantId: 't-il-3', rateLimit: 3, rateLimitWindow: 60 });
    const k100 = key('sk_qa1017_bare_il100', { connectorId: 'qa1017-bare-il100', scopes: [], tenantId: 't-il-100', rateLimit: 100, rateLimitWindow: 60 });
    await send(bareUrl, 'GET', '/tenant', { 'x-api-key': k3 }); await send(bareUrl, 'GET', '/tenant', { 'x-api-key': k100 });
    const par = await Promise.all(Array.from({ length: 16 }, (_, i) => send(bareUrl, 'GET', '/tenant', { 'x-api-key': i % 2 ? k100 : k3 }).then((r) => ({ k: i % 2 ? 't-il-100' : 't-il-3', status: r.status, tenant: r.json?.tenant ?? null }))));
    rows.bare.push({ cell: 'A2_interleaved_parallel_16', statusByKey: par.reduce((a: any, x) => { (a[x.k] ||= []).push(x.status); return a; }, {}),
      tenantMismatch: par.filter((x) => x.status === 200 && x.tenant !== x.k).length, allowed: par.filter((x) => x.status === 200).length });
    const kw = key('sk_qa1017_bare_twice', { connectorId: 'qa1017-bare-twice', scopes: [], tenantId: 't-bare', rateLimit: 2, rateLimitWindow: 60 });
    const tw: Res[] = []; for (let i = 0; i < 3; i++) tw.push(await send(bareUrl, 'GET', '/twice', { 'x-api-key': kw }));
    rows.bare.push({ cell: 'R3_twice_required_then_optional', statuses: tw.map((x) => x.status), remaining: tw.map((x) => x.h['x-ratelimit-remaining']) });
    expect(rows.bare.length).toBe(6); // QA-EDIT-BARE-ROWS-6
  }, 120000);

  it('order: validate / exchange / forward / audit per allowed vs refused request (two keys, one connectorId)', async () => {
    if (!STAGES.includes('order')) return;
    const A = key('sk_qa1017_ord_A', { connectorId: 'qa1017-ord', scopes: ALL_SCOPES, tenantId: 't-ord', organizationId: 'org-ord', rateLimit: 1, rateLimitWindow: 60 });
    const B = key('sk_qa1017_ord_B', { connectorId: 'qa1017-ord', scopes: ALL_SCOPES, tenantId: 't-ord', organizationId: 'org-ord', rateLimit: 1, rateLimitWindow: 60 });
    const step = async (label: string, k: string, method: string, p: string, body?: string) => {
      const a0 = auditRows.length; const v0 = calls('/api/keys/validate', k); const t0 = calls('/internal/connector-token', k);
      const r = await send(gwUrl, method, p, { 'x-api-key': k }, body);
      await new Promise((res) => setTimeout(res, 60));
      rows.order.push({ label, status: r.status, code: r.code, validateCalls: calls('/api/keys/validate', k) - v0, exchangeCalls: calls('/internal/connector-token', k) - t0,
        forwarded: hits(label), auditRowsAdded: auditRows.length - a0, auditLast: auditRows.length > a0 ? String(auditRows[auditRows.length - 1].params[9]).slice(0, 200) : null });
    };
    await step('qaord-A-post-1', A, 'POST', '/api/documents', JSON.stringify({ title: 'qaord-A-post-1', documentType: 'DOCUMENT' }));
    await step('qaord-A-post-2', A, 'POST', '/api/documents', JSON.stringify({ title: 'qaord-A-post-2', documentType: 'DOCUMENT' }));
    await step('qaord-B-post-1-fresh-key-same-connector', B, 'POST', '/api/documents', JSON.stringify({ title: 'qaord-B-post-1-fresh-key-same-connector', documentType: 'DOCUMENT' }));
    await step('qaord-A-get-anchors', A, 'GET', '/api/anchors/qaord-A-get-anchors');
    expect(rows.order.length).toBe(4);
  }, 120000);
});
