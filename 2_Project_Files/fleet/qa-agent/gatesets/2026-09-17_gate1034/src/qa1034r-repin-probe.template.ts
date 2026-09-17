/**
 * qa1034r-repin-probe (TEMPLATE) — RE-PIN copy of qa1034-drafter-probe.template.ts (head e4624218b): the SAME 3,258-cell matrix, plus ONE extra `it`
 * (OUT.admin) driving register-connector with a JWT-only SYSTEM_ADMIN caller (live / revoked) and the same admin beside an OK / REFUSED key.
 * Original header: QA DRAFTER probe for PR #1034 (KS-1215). NOT a product test. The runner writes it, with __GW_SRC__ replaced by the tree's
 * absolute services/api-gateway/src path, to <tree>/Blockchain/Dev/qa_probe_1034/ — OUTSIDE services/api-gateway (the #1018 r2 gate's F-3) — runs it SOLO
 * through a scratch vitest config, and quarantines the directory by MOVE afterwards.
 * Harness (the #1023 / #1028 gate style, the ks1207 / ks1215 pattern): the REAL index.ts app in-process (its real mount order), ../db mocked (SQL-aware:
 * INSERT INTO organizations returns one row), the session store stubbed (qa1034-live -> true, qa1034-revoked -> false), every *_SERVICE_URL and
 * TENANT_PROVISIONING_URL = ONE loopback recorder that also answers key validation (scopes ['*'] — an instrument: maximal reach), the connector-token
 * exchange per key outcome (OK 200 / REFUSED 401 / DROPPED socket destroyed / NONJSON 200 unparseable / HANG never answers), GET /api/tenants and the
 * security key mint. Per upstream hit: url, method, the Authorization class and whether it EQUALS the caller's Authorization byte for byte.
 * Routes: every route where authenticateToken runs (out/mounts_<tree>.json, READ census) plus /api/batch/verify (no authenticateToken: a control).
 * Every listener binds 127.0.0.1:0 and is closed in afterAll. Rows -> QA_OUT.
 */
import { describe, it, expect, afterAll, vi } from 'vitest';
import http from 'http';
import jwt from 'jsonwebtoken';
import { randomUUID } from 'crypto';
import { readFileSync, writeFileSync } from 'fs';

vi.mock('__GW_SRC__/db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async (sql: string) => (/INSERT INTO organizations/i.test(String(sql)) ? { rows: [{ id: 'org-qa1034', slug: 'qa1034-org' }], rowCount: 1 } : { rows: [], rowCount: 0 }) };
});
const SESSION: string[] = [];
vi.mock('@secuura/shared', async (orig) => {
  const real = (await orig()) as Record<string, any>;
  return { ...real, isSessionActive: async (sid: string) => { SESSION.push(sid); return sid === 'qa1034-live' ? true : sid === 'qa1034-revoked' ? false : null; } };
});

const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
const TENANT = 'a0000000-0000-4000-8000-000000000001';
const ROUTES: Array<{ file: string; line: number; verb: string; path: string; required: boolean }> = JSON.parse(readFileSync(process.env.QA_ROUTES as string, 'utf8'));
const OUT: any = { rows: [], hang: [], meta: {}, admin: [] };
type Hit = { url: string; method: string; auth: string | null; cls: string; userId: string | null };
const hits: Hit[] = [];
const held: http.ServerResponse[] = [];
function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
function listen(s: http.Server): Promise<string> {
  return new Promise((resolve) => s.listen(0, '127.0.0.1', () => resolve(`http://127.0.0.1:${(s.address() as any).port}`)));
}
async function closeServer(s: http.Server | undefined) { if (!s) return; (s as any).closeAllConnections?.(); await new Promise<void>((r) => s.close(() => r())); }
function cls(a: string | undefined): string {
  if (a === undefined) return 'absent';
  if (a === '') return 'empty';
  const t = a.replace(/^bearer\s+/i, '');
  const d = jwt.decode(t) as any;
  if (!d) return 'other:' + a.slice(0, 12);
  return d.type === 'connector' ? 'connector-jwt' : `user:${d.sessionId}`;
}
function outcomeOf(key: string): string { const m = /^sk_qa1034_([a-z]+)_/.exec(key || ''); return m ? m[1] : 'none'; }
const VALID = new Set(['ok', 'refused', 'dropped', 'nonjson', 'hang']);
const recorder = http.createServer(async (req, res) => {
  const body = await readBody(req);
  const json = (st: number, p: unknown) => { res.writeHead(st, { 'content-type': 'application/json' }); res.end(JSON.stringify(p)); };
  const url = req.url || '';
  if (url === '/api/keys/validate') {
    const key = String(JSON.parse(body || '{}').key || '');
    if (VALID.has(outcomeOf(key))) return json(200, { data: { valid: true, connectorId: 'qa1034-' + outcomeOf(key), scopes: ['*'], organizationId: 'org-qa1034', tenantId: TENANT, rateLimit: 1000000, rateLimitWindow: 60 } });
    return json(200, { data: { valid: false } });
  }
  if (url === '/internal/connector-token') {
    const o = outcomeOf(String(JSON.parse(body || '{}').apiKey || ''));
    if (o === 'dropped') { req.socket.destroy(); return; }
    if (o === 'hang') { held.push(res); return; }
    if (o === 'nonjson') { res.writeHead(200, { 'content-type': 'application/json' }); res.end('<html>not json</html>'); return; }
    if (o !== 'ok') return json(401, { success: false });
    return json(200, { success: true, data: { token: jwt.sign({ userId: 'connector:qa1034-ok', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' }, PRIV, { algorithm: 'RS256', expiresIn: 600 }), expiresIn: 600 } });
  }
  if (url.startsWith('/.well-known/')) return json(404, {});
  hits.push({ url, method: req.method || '', auth: (req.headers.authorization as string | undefined) ?? null, cls: cls(req.headers.authorization as string | undefined), userId: (req.headers['x-user-id'] as string) ?? null });
  if (req.method === 'GET' && url.startsWith('/api/tenants')) return json(200, { tenants: [{ id: TENANT, slug: 'qa1034' }] });
  if (req.method === 'POST' && url === '/api/keys') return json(201, { data: { id: 'key-qa1034', key: 'sk_qa1034_minted_not_a_key', prefix: 'sk_qa1034' } });
  return json(200, { success: true, data: { recorder: true } });
});
let recorderUrl = '';

function userJwt(sid: string): string {
  return 'Bearer ' + jwt.sign({ userId: 'u-qa1034', email: 'qa1034@secuura.invalid', role: 'user', verificationLevel: 'basic', authMethod: 'email', tenantId: TENANT, sessionId: sid }, PRIV, { algorithm: 'RS256', expiresIn: '10m' });
}
function adminJwt(sid: string): string {
  return 'Bearer ' + jwt.sign({ userId: 'u-qa1034-admin', email: 'qa1034-admin@secuura.invalid', role: 'SYSTEM_ADMIN', verificationLevel: 'email', authMethod: 'email', tenantId: TENANT, sessionId: sid }, PRIV, { algorithm: 'RS256', expiresIn: '10m' });
}
function concrete(path: string): string { return path.replace(/:[A-Za-z]+/g, 'qa1034id').replace(/\*$/, 'qa1034').replace(/\/$/, '/qa1034'); }
function bodyFor(path: string): string | null {
  if (path.endsWith('register-connector')) return JSON.stringify({ externalRef: 'qa1034-ext', tenantSlug: 'qa1034' });
  if (path.startsWith('/api/batch/verify')) return JSON.stringify({ hashes: ['qa1034'] });
  return JSON.stringify({});
}
function send(base: string, method: string, path: string, headers: Record<string, string>, body: string | null, timeoutMs = 8000, settleMs = 15): Promise<any> {
  return new Promise((resolve) => {
    const t = new URL(base); const h0 = hits.length; const s0 = SESSION.length;
    const hdrs: Record<string, string> = { ...headers };
    const withBody = !['GET', 'DELETE'].includes(method) && body !== null;
    if (withBody) { hdrs['content-type'] = 'application/json'; hdrs['content-length'] = String(Buffer.byteLength(body as string)); }
    const req = http.request({ hostname: t.hostname, port: t.port, path, method, agent: false, headers: hdrs }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const text = Buffer.concat(c).toString(); let code: string | null = null;
        try { code = JSON.parse(text)?.error?.code ?? null; } catch { /* non-JSON */ }
        setTimeout(() => {
          const fwd = hits.slice(h0);
          resolve({ status: res.statusCode, code, loc: res.headers.location ?? null, sessions: SESSION.length - s0, fwd: fwd.map((h) => ({ url: h.url.slice(0, 70), method: h.method, cls: h.cls, eqCaller: headers.authorization !== undefined && h.auth === headers.authorization, userId: h.userId })) });
        }, settleMs);
      });
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error('QA-CLIENT-TIMEOUT')));
    req.on('error', (e) => resolve({ status: -1, code: String(e.message).includes('QA-CLIENT-TIMEOUT') ? 'NO-RESPONSE' : 'CLIENT_ERROR', msg: String(e).slice(0, 80), sessions: SESSION.length - s0, fwd: hits.slice(h0).map((h) => ({ url: h.url.slice(0, 70), cls: h.cls, eqCaller: headers.authorization !== undefined && h.auth === headers.authorization })) }));
    if (withBody) req.write(body as string);
    req.end();
  });
}
const SVC = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM', 'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET', 'VERIFICATION', 'M365', 'MCP', 'GUARDIAN', 'QUEUE', 'TOKENISATION', 'WALLET_CONNECTOR', 'IDENTITY', 'SYSTEM_ERRORS'];
async function bootApp(env: Record<string, string>) {
  if (!recorderUrl) recorderUrl = await listen(recorder);
  vi.resetModules();
  for (const [kk, v] of Object.entries(env)) vi.stubEnv(kk, v);
  for (const s of SVC) vi.stubEnv(`${s}_SERVICE_URL`, recorderUrl);
  vi.stubEnv('TENANT_PROVISIONING_URL', recorderUrl);
  delete process.env.JWT_JWKS_URL;
  const app = (await import('__GW_SRC__/index')).default;
  const server = http.createServer(app as any);
  return { server, url: await listen(server) };
}
const testEnv = () => ({ NODE_ENV: 'test', GATEWAY_VOUCH_SECRET: '', UNHANDLED_REJECTION_MODE: 'survive' });
const prodEnv = () => ({ NODE_ENV: 'production', CSRF_SECRET: 'qa1034-drafter-stub-not-a-secret', DATABASE_URL: 'postgres://qa:qa@127.0.0.1:1/qa', REDIS_URL: 'redis://127.0.0.1:1',
  ENABLE_TEST_TOKENS: '', ENABLE_MOCK_ENDPOINTS: '', GATEWAY_VOUCH_SECRET: '', UNHANDLED_REJECTION_MODE: 'survive', RATE_LIMIT_MAX_REQUESTS: '1000000' }); // instrument: 300/min global limiter
const KEYS = ['NOKEY', 'JUNK', 'OK', 'REFUSED', 'DROPPED', 'NONJSON'];
const CALLERS = ['NONE', 'LIVE', 'REVOKED'];
function keyHeader(k: string): Record<string, string> {
  if (k === 'NOKEY') return {};
  if (k === 'JUNK') return { 'x-api-key': `sk_qa1034_junk_${randomUUID().replace(/-/g, '')}` };
  return { 'x-api-key': `sk_qa1034_${k.toLowerCase()}_${randomUUID().replace(/-/g, '')}` };
}
function callerHeader(c: string): Record<string, string> { return c === 'NONE' ? {} : { authorization: userJwt(c === 'LIVE' ? 'qa1034-live' : 'qa1034-revoked') }; }
async function matrix(url: string, mode: string, prefix: string, routes: typeof ROUTES) {
  for (const r of routes) {
    const method = r.verb === 'use' || r.verb === 'all' ? 'GET' : r.verb.toUpperCase();
    const sub = concrete(r.path).replace(/^\/api/, prefix);
    const settle = r.file === 'platform.ts' ? 60 : 15;
    for (const k of KEYS) for (const c of CALLERS) {
      const res = await send(url, method, sub, { ...keyHeader(k), ...callerHeader(c) }, bodyFor(r.path), 8000, settle);
      OUT.rows.push({ mode, prefix, route: `${method} ${r.path}`, src: `${r.file}:${r.line}`, required: r.required, key: k, caller: c, ...res });
    }
  }
}
const BATCH = [{ file: 'batch.ts', line: 174, verb: 'post', path: '/api/batch/verify', required: false }];
const V1SUBSET = (routes: typeof ROUTES) => routes.filter((r) => ['/api/credentials', '/api/documents', '/api/certifications', '/api/settings/notifications', '/api/signatories', '/api/platform/organizations/register-connector'].includes(r.path));
afterAll(async () => { for (const r of held) { try { r.destroy(); } catch { /* */ } } await closeServer(recorder); vi.unstubAllEnvs(); writeFileSync(process.env.QA_OUT as string, JSON.stringify(OUT, null, 1)); });

describe('qa1034 drafter probe', () => {
  it('test mode: /api every route + /api/batch; /api/v1 subset; exchange HANG rows', async () => {
    const g = await bootApp(testEnv());
    try {
      await matrix(g.url, 'test', '/api', [...ROUTES, ...BATCH]);
      await matrix(g.url, 'test', '/api/v1', [...V1SUBSET(ROUTES), ...BATCH]);
      for (const p of ['/api/credentials/qa1034id', '/api/documents/qa1034id']) {
        const k = { 'x-api-key': `sk_qa1034_hang_${randomUUID().replace(/-/g, '')}` };
        OUT.hang.push({ mode: 'test', path: p, what: 'exchange never answers, LIVE caller, client timeout 3 s', ...(await send(g.url, 'GET', p, { ...k, ...callerHeader('LIVE') }, null, 3000)) });
        OUT.hang.push({ mode: 'test', path: p, what: 'AFTER: OK key + LIVE caller (is the app still serving?)', ...(await send(g.url, 'GET', p, { ...keyHeader('OK'), ...callerHeader('LIVE') }, null)) });
      }
    } finally { await closeServer(g.server); }
    expect(OUT.rows.length).toBeGreaterThan(1000);
  }, 1200000);
  it('RE-PIN admin cells: register-connector with a JWT-only SYSTEM_ADMIN, test /api + production /api/v1', async () => {
    const RC = '/api/platform/organizations/register-connector';
    for (const [mode, env, prefix] of [['test', testEnv(), '/api'], ['production', prodEnv(), '/api/v1']] as Array<[string, Record<string, string>, string]>) {
      const g = await bootApp(env);
      try {
        const cells: Array<[string, Record<string, string>]> = [
          ['ADMIN-LIVE alone', { authorization: adminJwt('qa1034-live') }],
          ['ADMIN-REVOKED alone', { authorization: adminJwt('qa1034-revoked') }],
          ['ADMIN-LIVE + OK key', { ...keyHeader('OK'), authorization: adminJwt('qa1034-live') }],
          ['ADMIN-LIVE + REFUSED key', { ...keyHeader('REFUSED'), authorization: adminJwt('qa1034-live') }],
          ['ADMIN-REVOKED + OK key', { ...keyHeader('OK'), authorization: adminJwt('qa1034-revoked') }],
          ['ADMIN-REVOKED + REFUSED key', { ...keyHeader('REFUSED'), authorization: adminJwt('qa1034-revoked') }],
        ];
        for (const [what, h] of cells) OUT.admin.push({ mode, prefix, what, ...(await send(g.url, 'POST', RC.replace(/^\/api/, prefix), h, bodyFor(RC), 8000, 60)) });
      } finally { await closeServer(g.server); }
    }
    expect(OUT.admin.length).toBe(12);
  }, 600000);
  it('production mode: /api/v1 every route + /api/batch; unversioned 307', async () => {
    const g = await bootApp(prodEnv());
    try {
      OUT.meta.prod307 = await send(g.url, 'GET', '/api/credentials/qa1034id', { ...keyHeader('REFUSED'), ...callerHeader('REVOKED') }, null);
      await matrix(g.url, 'production', '/api/v1', [...ROUTES, ...BATCH]);
    } finally { await closeServer(g.server); }
    expect(OUT.rows.length).toBeGreaterThan(2000);
  }, 1200000);
});
