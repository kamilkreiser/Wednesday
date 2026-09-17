/**
 * qa1023-drafter-probe.test.ts — QA DRAFTER probe for PR #1023 (KS-1207). NOT a product test: copied into the drafter's OWN clone, run SOLO,
 * quarantined by rename. Same harness style as the seat's ks1207 test and the #1019 gate probe: the REAL index.ts app in-process, `../db`
 * mocked, every *_SERVICE_URL = ONE loopback recorder (it also answers /api/keys/validate and /internal/connector-token), the session store
 * stubbed (qa1023-revoked -> false, qa1023-live -> true, qa1023-storedown -> null), runWithTenantId wrapped to RECORD its tenant argument,
 * getRedisClient swappable for a recording fake (limiter stage only). Stages via QA_STAGES (test,prod,limiter). Rows -> QA_OUT.
 * Key classes the recorder answers: sk_qa1023_valid_* valid (rl<N> in the name = rateLimit N), sk_qa1023_down500_* HTTP 500,
 * sk_qa1023_destroy_* socket destroyed (fetch throws), sk_qa1023_validnoex_* valid but the connector-token exchange answers 401, anything else {valid:false}. Unique key per request except the limiter stage.
 * Every listener binds 127.0.0.1:0 and is closed in finally/afterAll.
 */
import { describe, it, expect, afterAll, vi } from 'vitest';
import http from 'http';
import jwt from 'jsonwebtoken';
import crypto, { randomUUID } from 'crypto';
import { writeFileSync } from 'fs';

vi.mock('../db', async (orig) => {
  const real = (await orig()) as Record<string, unknown>;
  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
});
const SESSION: string[] = [];
const TENANT: Array<string | null> = [];
vi.mock('@secuura/shared', async (orig) => {
  const real = (await orig()) as Record<string, any>;
  return {
    ...real,
    isSessionActive: async (sid: string) => { SESSION.push(sid); return sid === 'qa1023-revoked' ? false : sid === 'qa1023-live' ? true : null; },
    runWithTenantId: (t: any, fn: any) => { TENANT.push(t ?? null); return real.runWithTenantId(t, fn); },
  };
});
const FAKE = { on: false, incr: [] as string[] };
const counters = new Map<string, number>();
vi.mock('../services/redis', async (orig) => {
  const real = (await orig()) as Record<string, any>;
  const fake: any = new Proxy({ status: 'ready',
    incr: async (k: string) => { FAKE.incr.push(k); const n = (counters.get(k) || 0) + 1; counters.set(k, n); return n; },
    pexpire: async () => 1, pttl: async () => 60000 }, { get: (t: any, p: string) => (p in t ? t[p] : async () => null) });
  return { ...real, getRedisClient: () => (FAKE.on ? fake : real.getRedisClient()) };
});

const STAGES = (process.env.QA_STAGES || 'test,prod,limiter').split(',');
const OUT: any = { stages: STAGES, test: [], prod: [], limiter: [] };
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
const OTHER = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const KEY_TENANT = 'b0000000-0000-4000-8000-00000000c0de';
const JWT_TENANT = 'a0000000-0000-4000-8000-000000000001';

type Hit = { url: string; userId: string | null; bearerSub: string | null; apiKeyFwd: boolean; tenant: string | null };
const hits: Hit[] = [];
let validates = 0; let exchanges = 0;
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
    validates++;
    const key = String(JSON.parse(body || '{}').key || '');
    if (key.startsWith('sk_qa1023_down500_')) return json(500, { error: 'qa down' });
    if (key.startsWith('sk_qa1023_destroy_')) { req.socket.destroy(); return; }
    if (key.startsWith('sk_qa1023_valid_') || key.startsWith('sk_qa1023_validnoex_')) {
      const rl = /_rl(\d+)_/.exec(key);
      return json(200, { data: { valid: true, connectorId: 'qa1023-conn', scopes: ['certifications:read', 'documents:read'], organizationId: 'org-qa1023', tenantId: KEY_TENANT, rateLimit: rl ? Number(rl[1]) : 1000, rateLimitWindow: 60 } });
    }
    return json(200, { data: { valid: false } });
  }
  if (url === '/internal/connector-token') {
    exchanges++;
    const k = String(JSON.parse(body || '{}').apiKey || '');
    if (!k.startsWith('sk_qa1023_valid_')) return json(401, { success: false });
    return json(200, { success: true, data: { token: jwt.sign({ userId: 'connector:qa1023-conn', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' }, PRIV, { algorithm: 'RS256', expiresIn: 600 }), expiresIn: 600 } });
  }
  if (url.startsWith('/.well-known/')) return json(404, {});
  const a = String(req.headers.authorization || '');
  hits.push({ url, userId: (req.headers['x-user-id'] as string) ?? null, bearerSub: a.startsWith('Bearer ') ? ((jwt.decode(a.slice(7)) as any)?.userId ?? 'undecodable') : null,
    apiKeyFwd: req.headers['x-api-key'] !== undefined, tenant: (req.headers['x-tenant-id'] as string) ?? null });
  return json(200, { success: true, data: { recorder: true } });
});
let recorderUrl = '';

function userJwt(sid: string, priv = PRIV): string {
  return 'Bearer ' + jwt.sign({ userId: 'u-qa1023', email: 'qa1023-user@secuura.invalid', role: 'user', verificationLevel: 'email', authMethod: 'email', tenantId: JWT_TENANT, sessionId: sid }, priv, { algorithm: 'RS256', expiresIn: '10m' });
}
const k = (cls: string) => `sk_qa1023_${cls}_${randomUUID().replace(/-/g, '')}`;
const CASES: Record<string, () => Record<string, string>> = {
  ANON: () => ({}),
  JUNK: () => ({ 'x-api-key': k('junk') }),
  REVOKED: () => ({ authorization: userJwt('qa1023-revoked') }),
  LIVE: () => ({ authorization: userJwt('qa1023-live') }),
  VALID: () => ({ 'x-api-key': k('valid') }),
  REVOKED_JUNK: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': k('junk') }),
  LIVE_JUNK: () => ({ authorization: userJwt('qa1023-live'), 'x-api-key': k('junk') }),
  LIVE_VALID: () => ({ authorization: userJwt('qa1023-live'), 'x-api-key': k('valid') }),
  REVOKED_VALID: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': k('valid') }),
  BADSIG_JUNK: () => ({ authorization: userJwt('qa1023-live', OTHER), 'x-api-key': k('junk') }),
  STOREDOWN_JUNK: () => ({ authorization: userJwt('qa1023-storedown'), 'x-api-key': k('junk') }),
  REVOKED_NONSK: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': 'pk_qa1023_not_sk' }),
  REVOKED_UPPERSK: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': 'SK_qa1023_upper' }),
  DOWN500: () => ({ 'x-api-key': k('down500') }),
  DOWN500_LIVE: () => ({ authorization: userJwt('qa1023-live'), 'x-api-key': k('down500') }),
  DOWN500_REVOKED: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': k('down500') }),
  DESTROY: () => ({ 'x-api-key': k('destroy') }),
  DESTROY_LIVE: () => ({ authorization: userJwt('qa1023-live'), 'x-api-key': k('destroy') }),
  DESTROY_REVOKED: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': k('destroy') }),
  VALIDNOEX: () => ({ 'x-api-key': k('validnoex') }),
  REVOKED_VALIDNOEX: () => ({ authorization: userJwt('qa1023-revoked'), 'x-api-key': k('validnoex') }),
};
// census: every authenticateToken(false) mount at the head (proxy.ts x6, admin.ts GET x2) + two REQUIRED controls
const MOUNTS: Array<[string, string, string]> = [
  ['credentials', '/credentials/cred-qa1023', 'optional'], ['referrals', '/referrals/CODEQA1023', 'optional'], ['governance', '/governance/proposals', 'optional'],
  ['nft', '/nft/tiers', 'optional'], ['billing', '/billing/config', 'optional'], ['certifications', '/certifications', 'optional+requireScope'],
  ['settings-notifications', '/settings/notifications', 'optional-local'], ['privacy-settings', '/privacy/settings', 'optional-local'],
  ['documents', '/documents', 'REQUIRED'], ['milestones', '/milestones', 'REQUIRED'],
];

function send(base: string, path: string, headers: Record<string, string>): Promise<any> {
  return new Promise((resolve) => {
    const t = new URL(base); const h0 = hits.length; const s0 = SESSION.length; const t0 = TENANT.length; const v0 = validates; const e0 = exchanges; const i0 = FAKE.incr.length;
    const req = http.request({ hostname: t.hostname, port: t.port, path, method: 'GET', agent: false, headers }, (res) => {
      const c: Buffer[] = [];
      res.on('data', (d) => c.push(d));
      res.on('end', () => {
        let code: string | null = null; let msg: string | null = null;
        try { const j = JSON.parse(Buffer.concat(c).toString()); code = j?.error?.code ?? null; msg = j?.error?.message ? String(j.error.message).slice(0, 80) : null; } catch { /* non-JSON */ }
        setTimeout(() => resolve({ status: res.statusCode, code, msg, fwd: hits.slice(h0), sessions: SESSION.slice(s0), tenants: TENANT.slice(t0), validates: validates - v0,
          exchanges: exchanges - e0, rlRemaining: res.headers['x-ratelimit-remaining'] ?? null, location: res.headers.location ?? null, incr: FAKE.incr.slice(i0).map((x) => x.slice(0, 22)) }), 50);
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
  const app = (await import('../index')).default;
  const server = http.createServer(app as any);
  return { server, url: await listen(server) };
}
const testEnv = () => ({ NODE_ENV: 'test', GATEWAY_VOUCH_SECRET: '', UNHANDLED_REJECTION_MODE: 'survive' });
const prodEnv = () => ({ NODE_ENV: 'production', CSRF_SECRET: 'qa1023-drafter-stub-not-a-secret', DATABASE_URL: 'postgres://qa:qa@127.0.0.1:1/qa', REDIS_URL: 'redis://127.0.0.1:1',
  ENABLE_TEST_TOKENS: '', ENABLE_MOCK_ENDPOINTS: '', GATEWAY_VOUCH_SECRET: '', UNHANDLED_REJECTION_MODE: 'survive',
  RATE_LIMIT_MAX_REQUESTS: '100000' }); // instrument: the production global per-IP limiter (300/min) would 429 the census tail

async function matrix(url: string, prefixes: string[], into: any[]) {
  for (const prefix of prefixes) for (const [mount, sub, kind] of MOUNTS) for (const [cid, mk] of Object.entries(CASES)) {
    into.push({ mount, kind, prefix, case: cid, ...(await send(url, prefix + sub, mk())) });
  }
}

afterAll(async () => { await closeServer(recorder); vi.unstubAllEnvs(); writeFileSync(process.env.QA_OUT as string, JSON.stringify(OUT, null, 1)); });

describe('qa1023 drafter probe', () => {
  it('test mode: census x cases under /api and /api/v1', async () => {
    if (!STAGES.includes('test')) return;
    const g = await bootApp(testEnv());
    try { await matrix(g.url, ['/api', '/api/v1'], OUT.test); } finally { await closeServer(g.server); }
    expect(OUT.test.length).toBe(2 * MOUNTS.length * Object.keys(CASES).length);
  }, 240000);

  it('production mode: census x cases under /api/v1 (and /api for the 307 shape)', async () => {
    if (!STAGES.includes('prod')) return;
    const g = await bootApp(prodEnv());
    try { await matrix(g.url, ['/api/v1', '/api'], OUT.prod); } finally { await closeServer(g.server); }
    expect(OUT.prod.length).toBe(2 * MOUNTS.length * Object.keys(CASES).length);
  }, 240000);

  it('limiter: a recording fake Redis — bucket keys per request class', async () => {
    if (!STAGES.includes('limiter')) return;
    const g = await bootApp(testEnv());
    FAKE.on = true;
    try {
      const valid = k('valid_rl3');
      for (let i = 1; i <= 5; i++) OUT.limiter.push({ id: 'L-VALID-rl3 #' + i, ...(await send(g.url, '/api/credentials/cred-qa1023', { 'x-api-key': valid })) });
      for (let i = 1; i <= 5; i++) OUT.limiter.push({ id: 'L-VALID-rl3 on certifications #' + i, ...(await send(g.url, '/api/certifications', { 'x-api-key': k('valid_rl3') })) });
      const junk = k('junk');
      for (let i = 1; i <= 4; i++) OUT.limiter.push({ id: 'L-LIVE+JUNK #' + i, ...(await send(g.url, '/api/credentials/cred-qa1023', { authorization: userJwt('qa1023-live'), 'x-api-key': junk })) });
      for (let i = 1; i <= 4; i++) OUT.limiter.push({ id: 'L-JUNK #' + i, ...(await send(g.url, '/api/credentials/cred-qa1023', { 'x-api-key': junk })) });
      const lv = k('valid_rl3');
      for (let i = 1; i <= 5; i++) OUT.limiter.push({ id: 'L-LIVE+VALID-rl3 #' + i, ...(await send(g.url, '/api/credentials/cred-qa1023', { authorization: userJwt('qa1023-live'), 'x-api-key': lv })) });
      const dv = k('down500');
      for (let i = 1; i <= 3; i++) OUT.limiter.push({ id: 'L-LIVE+DOWN500 #' + i, ...(await send(g.url, '/api/credentials/cred-qa1023', { authorization: userJwt('qa1023-live'), 'x-api-key': dv })) });
    } finally { FAKE.on = false; await closeServer(g.server); }
    expect(OUT.limiter.length).toBe(26);
  }, 120000);
});
