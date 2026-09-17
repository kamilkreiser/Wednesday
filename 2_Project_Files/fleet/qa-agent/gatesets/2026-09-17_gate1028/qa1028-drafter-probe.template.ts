/**
 * qa1028-drafter-probe (TEMPLATE) — QA DRAFTER probe for PR #1028 (KS-744). NOT a product test. The runner writes it, with __GW_SRC__ replaced by the
 * tree's absolute services/api-gateway/src path, to <tree>/Blockchain/Dev/qa_probe_1028/ — OUTSIDE services/api-gateway (the #1018 r2 gate's F-3: a probe
 * under src/ is inside the service's tsc include and vitest's default include) — runs it SOLO through a scratch vitest config whose include names only this
 * file, and quarantines the directory by rename afterwards.
 * Harness (the #1023 gate style): the REAL index.ts app in-process, ../db mocked, the session store stubbed (qa1028-live -> true), every *_SERVICE_URL =
 * ONE loopback recorder that also answers /api/keys/validate ({valid:false} for sk_qa1028_junk_*, valid for sk_qa1028_valid_*) and
 * /internal/connector-token. The recorder stores, per upstream hit, the forwarded value (and typeof / raw line count) of every identity-ish header below.
 * Every listener binds 127.0.0.1:0 and is closed in afterAll. Rows -> QA_OUT.
 */
import { describe, it, expect, afterAll, vi } from 'vitest';
import http from 'http';
import jwt from 'jsonwebtoken';
import crypto, { randomUUID } from 'crypto';
import { writeFileSync } from 'fs';

vi.mock('__GW_SRC__/db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
});
const SESSION: string[] = [];
vi.mock('@secuura/shared', async (orig) => {
  const real = (await orig()) as Record<string, any>;
  return { ...real, isSessionActive: async (sid: string) => { SESSION.push(sid); return sid === 'qa1028-live' ? true : sid === 'qa1028-revoked' ? false : null; } };
});

const OUT: any = { test: [], prod: [] };
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
const OTHER = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const WATCH = ['x-verification-level', 'x-user-email', 'x-user-id', 'x-user-role', 'x-organization-id', 'x-tenant-id', 'x-tenant-slug', 'x-wallet-address',
  'x-auth-method', 'x-mfa-enabled', 'x-session-id', 'x-scopes', 'x-connector-id', 'x-api-key-scopes', 'x-verified', 'x-kyc-level', 'x-tenant-override'];
type Hit = { url: string; h: Record<string, string | null>; raw: Record<string, number>; bearerSub: string | null };
const hits: Hit[] = [];
function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
function listen(s: http.Server): Promise<string> {
  return new Promise((resolve) => s.listen(0, '127.0.0.1', () => resolve(`http://127.0.0.1:${(s.address() as any).port}`)));
}
async function closeServer(s: http.Server | undefined) { if (!s) return; (s as any).closeAllConnections?.(); await new Promise<void>((r) => s.close(() => r())); }
const recorder = http.createServer(async (req, res) => {
  const body = await readBody(req);
  const json = (st: number, p: unknown) => { res.writeHead(st, { 'content-type': 'application/json' }); res.end(JSON.stringify(p)); };
  const url = req.url || '';
  if (url === '/api/keys/validate') {
    const key = String(JSON.parse(body || '{}').key || '');
    if (key.startsWith('sk_qa1028_valid_')) return json(200, { data: { valid: true, connectorId: 'qa1028-conn', scopes: ['documents:read', 'certifications:read'], organizationId: 'org-qa1028', tenantId: 'b0000000-0000-4000-8000-00000000c0de', rateLimit: 100000, rateLimitWindow: 60 } });
    return json(200, { data: { valid: false } });
  }
  if (url === '/internal/connector-token') {
    return json(200, { success: true, data: { token: jwt.sign({ userId: 'connector:qa1028-conn', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key' }, PRIV, { algorithm: 'RS256', expiresIn: 600 }), expiresIn: 600 } });
  }
  if (url.startsWith('/.well-known/')) return json(404, {});
  const h: Record<string, string | null> = {}; const raw: Record<string, number> = {};
  for (const n of WATCH) h[n] = (req.headers[n] as string) ?? null;
  for (let i = 0; i < req.rawHeaders.length; i += 2) { const n = req.rawHeaders[i].toLowerCase(); if (WATCH.includes(n)) raw[n] = (raw[n] || 0) + 1; }
  const a = String(req.headers.authorization || '');
  hits.push({ url, h, raw, bearerSub: a.startsWith('Bearer ') ? ((jwt.decode(a.slice(7)) as any)?.userId ?? 'undecodable') : null });
  return json(200, { success: true, data: { recorder: true } });
});
let recorderUrl = '';

const BASE: Record<string, unknown> = { userId: 'u-qa1028', email: 'qa1028-user@secuura.invalid', role: 'user', verificationLevel: 'basic', authMethod: 'email', tenantId: 'a0000000-0000-4000-8000-000000000001', sessionId: 'qa1028-live' };
function tok(mut: Record<string, unknown>, drop: string[] = [], priv = PRIV): string {
  const p: Record<string, unknown> = { ...BASE, ...mut }; for (const d of drop) delete p[d];
  return 'Bearer ' + jwt.sign(p, priv, { algorithm: 'RS256', expiresIn: '10m' });
}
// token classes: the claim shapes the fix's truthiness guard sees
const TOKENS: Record<string, () => string> = {
  FULL: () => tok({}), NO_EMAIL: () => tok({}, ['email']), NO_VLEVEL: () => tok({}, ['verificationLevel']), NO_BOTH: () => tok({}, ['email', 'verificationLevel']),
  EMPTY_EMAIL: () => tok({ email: '' }), EMPTY_VLEVEL: () => tok({ verificationLevel: '' }), NULL_EMAIL: () => tok({ email: null }), NULL_VLEVEL: () => tok({ verificationLevel: null }),
  ZERO_VLEVEL: () => tok({ verificationLevel: 0 }), FALSE_VLEVEL: () => tok({ verificationLevel: false }), NUM_VLEVEL: () => tok({ verificationLevel: 3 }),
  TRUE_VLEVEL: () => tok({ verificationLevel: true }), OBJ_VLEVEL: () => tok({ verificationLevel: { level: 'enhanced' } }), ARR_VLEVEL: () => tok({ verificationLevel: ['basic', 'enhanced'] }),
  EMPTYARR_VLEVEL: () => tok({ verificationLevel: [] }), NUM_EMAIL: () => tok({ email: 7 }), ARR_EMAIL: () => tok({ email: ['a@qa1028.invalid', 'b@qa1028.invalid'] }),
  NO_ROLE_KS1208: () => tok({}, ['role']), NO_USERID_KS1208: () => tok({}, ['userId']),
};
const SPOOF: Record<string, string> = {
  'x-verification-level': 'enhanced', 'x-user-email': 'spoof@qa1028.invalid', 'x-user-id': 'spoof-user', 'x-user-role': 'super_admin', 'x-organization-id': 'spoof-org',
  'x-tenant-id': 'spoof-tenant', 'x-tenant-slug': 'spoof', 'x-wallet-address': 'addr_spoof_qa1028', 'x-auth-method': 'spoof', 'x-mfa-enabled': 'true',
  'x-session-id': 'spoof', 'x-scopes': 'admin:*', 'x-connector-id': 'spoof', 'x-api-key-scopes': 'admin:*', 'x-verified': 'true', 'x-kyc-level': 'enhanced',
};
const MOUNTS: Array<[string, string, string]> = [
  ['credentials', '/credentials/cred-qa1028', 'optional-proxy'], ['documents', '/documents', 'required-proxy'], ['settings-notifications', '/settings/notifications', 'optional-local'],
];
const junk = () => `sk_qa1028_junk_${randomUUID().replace(/-/g, '')}`;
const valid = () => `sk_qa1028_valid_${randomUUID().replace(/-/g, '')}`;

function send(base: string, path: string, headers: Record<string, string>): Promise<any> {
  return new Promise((resolve) => {
    const t = new URL(base); const h0 = hits.length; const s0 = SESSION.length;
    const req = http.request({ hostname: t.hostname, port: t.port, path, method: 'GET', agent: false, headers }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const text = Buffer.concat(c).toString(); let code: string | null = null; let msg: string | null = null;
        try { const j = JSON.parse(text); code = j?.error?.code ?? null; msg = j?.error?.message ? String(j.error.message).slice(0, 120) : null; } catch { /* non-JSON */ }
        setTimeout(() => resolve({ status: res.statusCode, code, msg, leaksInvalidValue: /Invalid value|ERR_HTTP_INVALID_HEADER/i.test(text), fwd: hits.slice(h0), sessions: SESSION.length - s0 }), 40);
      });
    });
    req.setTimeout(8000, () => req.destroy(new Error('QA-CLIENT-TIMEOUT 8s')));
    req.on('error', (e) => resolve({ status: -1, code: 'CLIENT_ERROR', msg: String(e).slice(0, 80), fwd: hits.slice(h0) }));
    req.end();
  });
}
const SVC = ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM', 'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET', 'VERIFICATION'];
async function bootApp(env: Record<string, string>) {
  if (!recorderUrl) recorderUrl = await listen(recorder);
  vi.resetModules();
  for (const [kk, v] of Object.entries(env)) vi.stubEnv(kk, v);
  for (const s of SVC) vi.stubEnv(`${s}_SERVICE_URL`, recorderUrl);
  delete process.env.JWT_JWKS_URL;
  const app = (await import('__GW_SRC__/index')).default;
  const server = http.createServer(app as any);
  return { server, url: await listen(server) };
}
const testEnv = () => ({ NODE_ENV: 'test', GATEWAY_VOUCH_SECRET: '', UNHANDLED_REJECTION_MODE: 'survive' });
const prodEnv = () => ({ NODE_ENV: 'production', CSRF_SECRET: 'qa1028-drafter-stub-not-a-secret', DATABASE_URL: 'postgres://qa:qa@127.0.0.1:1/qa', REDIS_URL: 'redis://127.0.0.1:1',
  ENABLE_TEST_TOKENS: '', ENABLE_MOCK_ENDPOINTS: '', GATEWAY_VOUCH_SECRET: '', UNHANDLED_REJECTION_MODE: 'survive', RATE_LIMIT_MAX_REQUESTS: '100000' }); // instrument: 300/min global limiter

async function matrix(url: string, prefix: string, into: any[]) {
  for (const [mount, sub, kind] of MOUNTS) {
    for (const [tid, mk] of Object.entries(TOKENS)) for (const sp of ['NONE', 'SPOOF']) {
      const extra = sp === 'SPOOF' ? SPOOF : {};
      into.push({ mount, kind, prefix, ctx: 'BEARER', token: tid, spoof: sp, ...(await send(url, prefix + sub, { authorization: mk(), ...extra })) });
      if (kind.startsWith('optional')) into.push({ mount, kind, prefix, ctx: 'BEARER+JUNKKEY', token: tid, spoof: sp, ...(await send(url, prefix + sub, { authorization: mk(), 'x-api-key': junk(), ...extra })) });
    }
    into.push({ mount, kind, prefix, ctx: 'ANON', token: '-', spoof: 'SPOOF', ...(await send(url, prefix + sub, { ...SPOOF })) });
    into.push({ mount, kind, prefix, ctx: 'JUNKKEY', token: '-', spoof: 'SPOOF', ...(await send(url, prefix + sub, { 'x-api-key': junk(), ...SPOOF })) });
    into.push({ mount, kind, prefix, ctx: 'VALIDKEY', token: '-', spoof: 'SPOOF', ...(await send(url, prefix + sub, { 'x-api-key': valid(), ...SPOOF })) });
    into.push({ mount, kind, prefix, ctx: 'BADSIG', token: 'NO_VLEVEL', spoof: 'SPOOF', ...(await send(url, prefix + sub, { authorization: tok({}, ['verificationLevel'], OTHER), ...SPOOF })) });
    into.push({ mount, kind, prefix, ctx: 'REVOKED', token: 'NO_VLEVEL', spoof: 'SPOOF', ...(await send(url, prefix + sub, { authorization: tok({ sessionId: 'qa1028-revoked' }, ['verificationLevel']), ...SPOOF })) });
  }
}
afterAll(async () => { await closeServer(recorder); vi.unstubAllEnvs(); writeFileSync(process.env.QA_OUT as string, JSON.stringify(OUT, null, 1)); });

describe('qa1028 drafter probe', () => {
  it('test mode, /api', async () => {
    const g = await bootApp(testEnv());
    try { await matrix(g.url, '/api', OUT.test); } finally { await closeServer(g.server); }
    expect(OUT.test.length).toBeGreaterThan(100);
  }, 240000);
  it('production mode, /api/v1', async () => {
    const g = await bootApp(prodEnv());
    try { await matrix(g.url, '/api/v1', OUT.prod); } finally { await closeServer(g.server); }
    expect(OUT.prod.length).toBe(OUT.test.length);
  }, 240000);
});
