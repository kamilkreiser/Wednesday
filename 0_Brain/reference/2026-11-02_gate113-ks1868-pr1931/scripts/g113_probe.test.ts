// GATE 113 probe (QA, not product). Real routers (auth, internal, oauth, issuerCerts), real passwordLoginGate,
// real errorHandler, REAL winston logger (wrapped call-through: a throw from winston propagates). Replaced: the
// persistence/crypto collaborators, by stateful recorders that count what would be PERSISTED or ISSUED.
// Writes one JSON line per scenario to process.env.G113_OUT.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import fs from 'node:fs';
import net from 'node:net';
import express from 'express';

if (process.env.G113_FMT === 'production') process.env.NODE_ENV = 'production';

const h = vi.hoisted(() => ({
  fail: {} as Record<string, string>,      // site -> shape
  cfg: {} as Record<string, unknown>,
  st: null as any,
  logs: [] as any[],
  unhandled: 0,
  connects: [] as string[],
}));
const fresh = () => ({
  sessions: 0, revokedSessions: 0, tokenPairs: 0, connectorTokens: 0, authCodes: 0, codeExchanges: 0,
  pwHashWrites: 0, lastLoginWrites: 0, denylisted: 0, lockFail: 0, lockSuccess: 0, certRevokes: 0, events: [] as string[],
});

function mk(shape: string): unknown {
  switch (shape) {
    case 'ordinary': return new Error('db down at 10.0.0.7 password=hunter2');
    case 'revoked': { const p = Proxy.revocable({}, {}); p.revoke(); return p.proxy; }
    case 'getter': { const e = new Error('x'); Object.defineProperty(e, 'message', { get() { throw new Error('getter boom'); } }); return e; }
    case 'nullproto': return Object.create(null);
    case 'string': return 'plain string secret=abc';
    case 'undef': return undefined;
    case 'msgProxy': { const p = Proxy.revocable({}, {}); p.revoke(); const e = new Error('x'); Object.defineProperty(e, 'message', { value: p.proxy }); return e; }
    case 'msgSymbol': { const e = new Error('x'); Object.defineProperty(e, 'message', { value: Symbol('s') }); return e; }
    case 'msgToStr': { const e = new Error('x'); Object.defineProperty(e, 'message', { value: { toString() { throw new Error('ts boom'); } } }); return e; }
    case 'msgNullProto': { const e = new Error('x'); Object.defineProperty(e, 'message', { value: Object.create(null) }); return e; }
  }
  throw new Error('unknown shape ' + shape);
}
(globalThis as any).__g113mk = mk;
function maybeFail(site: string): Promise<never> | null {
  const s = h.fail[site];
  return s ? Promise.reject((globalThis as any).__g113mk(s)) : null;
}

function describeVal(v: unknown): unknown {
  const t = typeof v;
  if (t === 'string') return v;
  if (t === 'undefined') return 'undefined';
  return '<' + t + '>';
}
vi.mock('../utils/logger', async (orig) => {
  const real: any = await orig();
  const wrap = (lvl: string) => (msg: unknown, meta?: Record<string, unknown>) => {
    const rec: any = { lvl, msg: typeof msg === 'string' ? msg : '<' + typeof msg + '>' };
    if (meta && typeof meta === 'object') {
      rec.keys = Object.keys(meta);
      rec.vals = Object.fromEntries(rec.keys.map((k: string) => [k, describeVal((meta as any)[k])]));
    }
    try { real.logger[lvl](msg, meta); rec.threw = false; } catch (e) { rec.threw = true; rec.thrown = String((e as Error)?.message).slice(0, 80); h.logs.push(rec); throw e; }
    h.logs.push(rec);
    return real.logger;
  };
  const logger = { error: wrap('error'), warn: wrap('warn'), info: wrap('info'), debug: wrap('debug'), log: (...a: any[]) => real.logger.log(...a) };
  return { ...real, logger, createLogger: () => logger };
});

const USER = () => ({
  id: 'u-113', email: 'g113@secuura.local', status: (h.cfg.status as string) || 'ACTIVE', role: 'OWNER',
  verificationLevel: 'BASIC', mfaEnabled: !!h.cfg.mfa, mfaSecret: h.cfg.mfa ? 'enc' : null, mfaBackupCodes: null,
  passwordHash: '$2b$10$bcryptstub', tenantId: 'ten-1', organizationId: 'org-1',
});
vi.mock('../db', () => ({ query: async () => ({ rows: [], rowCount: 0 }) }));
vi.mock('../repositories/userRepo', () => ({
  seedDemoUsers: async () => undefined,
  getPlatformAdmin: async () => null,
  getUserByEmail: async (e: string) => (h.cfg.unknown ? null : e.toLowerCase().trim() === 'g113@secuura.local' ? USER() : null),
  getUserById: async () => USER(),
  getUserByIdPreAuth: (_id: string) => maybeFail('userById') ?? Promise.resolve(USER()),
  getUserBySocialId: async () => null,
  createUser: async () => null,
  updateUser: (_id: string, patch: Record<string, unknown>) => {
    if (patch && 'passwordHash' in patch) { const f = maybeFail('rehash'); if (f) return f; h.st.pwHashWrites++; }
    if (patch && 'lastLoginAt' in patch) h.st.lastLoginWrites++;
    return Promise.resolve(USER());
  },
  updateUserOrThrow: async () => USER(),
  updateUserPlatformScope: async () => null,
  updatePlatformAdminPassword: async () => undefined,
  reencryptMfaSecretIfLegacy: async () => undefined,
  reencryptPlatformAdminMfaSecretIfLegacy: async () => undefined,
  consumeBackupCode: async () => ({ consumed: false }),
}));
vi.mock('../services/password', () => ({
  verifyPassword: () => maybeFail('verify') ?? Promise.resolve(h.cfg.badpw ? false : true),
  hashPassword: async () => '$argon2id$stub',
  checkPasswordStrength: () => ({ ok: true }),
  generateResetToken: () => ({ token: 't', hash: 'h', expiresAt: new Date() }),
  shouldRehashAfterVerify: () => true,
}));
vi.mock('../services/session', () => ({
  createSession: (u: any) => maybeFail('session') ?? (h.st.sessions++, Promise.resolve({ id: 'sess-' + h.st.sessions })),
  revokeSession: () => maybeFail('revokeSession') ?? (h.st.revokedSessions++, Promise.resolve(undefined)),
  revokeAllUserSessions: async () => 0,
  getSession: async () => null,
  rotateSessionRefreshToken: async () => undefined,
  getRedisClient: () => null,
  validateSession: async () => true,
  updateSessionActivity: async () => undefined,
  isRedisAvailable: () => true,
}));
vi.mock('../services/jwt', () => ({
  generateTokenPair: () => { h.st.tokenPairs++; return { accessToken: 'AT_' + h.st.tokenPairs, refreshToken: 'RT_' + h.st.tokenPairs, expiresIn: 900 }; },
  generateConnectorToken: () => { const s = h.fail.mint; if (s) throw (globalThis as any).__g113mk(s); h.st.connectorTokens++; return { token: 'CT_' + h.st.connectorTokens, expiresIn: 300 }; },
  verifyRefreshToken: () => { if (h.fail.verifyRefresh) throw (globalThis as any).__g113mk(h.fail.verifyRefresh); return { userId: 'u-113', jti: 'jti-1', client_id: 'app1', scopes: [] }; },
  decodeToken: () => ({ jti: 'jti-logout', exp: Math.floor(Date.now() / 1000) + 3600 }),
}));
vi.mock('../services/refreshDenylist', () => ({
  isRefreshJtiDenylisted: () => maybeFail('isDenied') ?? Promise.resolve(!!h.cfg.denied),
  denylistRefreshJti: () => maybeFail('denylist') ?? (h.st.denylisted++, Promise.resolve(undefined)),
}));
vi.mock('../services/accountLockout', () => ({
  isLockedOut: async () => !!h.cfg.locked,
  recordFailure: async () => { h.st.lockFail++; return 1; },
  recordSuccess: async () => { h.st.lockSuccess++; },
  clearFailures: async () => undefined,
}));
vi.mock('../services/email', () => ({ sendVerificationEmail: async () => undefined, sendPasswordResetEmail: async () => undefined }));
vi.mock('../events', () => ({
  publishEvent: (t: string) => { h.st.events.push(t); return Promise.resolve(undefined); },
  EventTypes: { USER_LOGIN: 'user.login', ISSUER_CERT_REVOKED: 'issuer_cert.revoked', ISSUER_CERT_UPLOADED: 'issuer_cert.uploaded' },
}));
vi.mock('../services/oauth', async (orig) => {
  const real: any = await orig();
  return {
    ...real,
    getAppByClientId: (id: string) => maybeFail('app') ?? Promise.resolve(id === 'app1' ? {
      id: 'a1', name: 'A', clientId: 'app1', redirectUris: ['https://app.test/cb'], allowedScopes: ['profile'],
      appType: 'confidential', isActive: true, createdAt: new Date(),
    } : null),
    verifyClientSecret: () => maybeFail('secret') ?? Promise.resolve(!h.cfg.badsecret),
    createAuthorizationCode: () => maybeFail('mintCode') ?? (h.st.authCodes++, Promise.resolve('CODE_' + h.st.authCodes)),
    exchangeCode: () => maybeFail('exchange') ?? (h.st.codeExchanges++, Promise.resolve({ userId: 'u-113', scope: 'profile' })),
  };
});
const SUMMARY = (status = 'active') => ({
  id: 'c1', name: 'n', organizationId: 'org-1', fingerprintSha256: 'fp', subject: 's', issuer: 'i', serialNumber: '1',
  validFrom: new Date(0), validUntil: new Date(4102444800000), keyAlgorithm: 'RSA', keySizeBits: 2048, trustLevel: 'x',
  status, uploadedAt: new Date(0), uploadedById: 'u', revokedAt: status === 'revoked' ? new Date(0) : null, revokedById: null,
  revocationReason: null, previousCertId: null, certPem: 'PEM',
});
vi.mock('../repositories/issuerCertRepo', () => ({
  createIssuerCert: async () => SUMMARY(), findIssuerCertByFingerprint: async () => null,
  findActiveIssuerCertForTenant: async () => null, rotateIssuerCert: async () => null,
  getIssuerCertById: () => maybeFail('certGet') ?? Promise.resolve(SUMMARY()),
  listIssuerCerts: () => maybeFail('certList') ?? Promise.resolve({ certs: [SUMMARY()], total: 1 }),
  revokeIssuerCert: () => maybeFail('certRevoke') ?? (h.st.certRevokes++, Promise.resolve(SUMMARY('revoked'))),
  toSummary: (c: any) => c,
}));
const passThrough = (...args: unknown[]) => {
  const set = (req: any, next: () => void) => { req.user = h.cfg.user ?? { userId: 'u-113', role: 'ORG_ADMIN', tenantId: 'ten-1', scopes: [] }; req.sessionId = 'sess-live'; next(); };
  if (args.length >= 3 && typeof args[2] === 'function') return set(args[0], args[2] as () => void);
  return (req: any, _s: unknown, n: () => void) => set(req, n);
};
vi.mock('../middleware/authenticate', () => ({
  authenticate: passThrough, authenticateToken: passThrough, authenticateAccessOrConnector: passThrough,
  optionalAuthenticate: passThrough, requireRole: passThrough,
}));
vi.mock('../middleware/tenantGuc', () => ({ seedTenantGuc: (_r: unknown, _s: unknown, n: () => void) => n() }));

type Scn = { id: string; site: string; shape?: string; fail?: Record<string, string>; cfg?: Record<string, unknown>; method: string; path: string; body?: any; headers?: Record<string, string> };
const SH = ['ordinary', 'revoked', 'getter', 'nullproto', 'string', 'undef', 'msgProxy', 'msgSymbol', 'msgToStr', 'msgNullProto'];
const LOGIN = { method: 'POST', path: '/api/auth/login', body: { email: 'g113@secuura.local', password: 'pw' } };
const LOGOUT = { method: 'POST', path: '/api/auth/logout', body: {} };
const CONN = { method: 'POST', path: '/internal/connector-token', body: { apiKey: 'sk_0123456789abcdef' } };
const AZ = { method: 'POST', path: '/api/oauth/authorize', body: { email: 'g113@secuura.local', password: 'pw', client_id: 'app1', redirect_uri: 'https://app.test/cb', state: 'st' } };
const TK = { method: 'POST', path: '/api/oauth/token', body: { grant_type: 'authorization_code', code: 'c', client_id: 'app1', redirect_uri: 'https://app.test/cb', client_secret: 'sec' } };
const RF = { method: 'POST', path: '/api/oauth/token', body: { grant_type: 'refresh_token', refresh_token: 'rt', client_id: 'app1', client_secret: 'sec' } };
const IL = { method: 'GET', path: '/ic/' };
const IR = { method: 'POST', path: '/ic/c1/revoke', body: {} };
const S: Scn[] = [];
const add = (id: string, site: string, req: any, fail: Record<string, string> = {}, cfg: Record<string, unknown> = {}, shape?: string) => S.push({ id, site, shape, fail, cfg, ...req });
// LOGIN (changed site: rehash catch)
add('login_ok', 'login', LOGIN);
for (const s of SH) add('login_rehash_' + s, 'login', LOGIN, { rehash: s }, {}, s);
for (const s of ['ordinary', 'revoked']) {
  add('login_badpw_rehash_' + s, 'login-refused', LOGIN, { rehash: s }, { badpw: true }, s);
  add('login_mfa_rehash_' + s, 'login-refused', LOGIN, { rehash: s }, { mfa: true }, s);
  add('login_suspended_rehash_' + s, 'login-refused', LOGIN, { rehash: s }, { status: 'SUSPENDED' }, s);
  add('login_locked_rehash_' + s, 'login-refused', LOGIN, { rehash: s }, { locked: true }, s);
  add('login_unknown_rehash_' + s, 'login-refused', LOGIN, { rehash: s }, { unknown: true }, s);
}
for (const s of ['ordinary', 'revoked', 'getter']) {
  add('login_verify_' + s, 'login-unchanged', LOGIN, { verify: s }, {}, s);
  add('login_session_' + s, 'login-unchanged', LOGIN, { session: s }, {}, s);
}
// LOGOUT (changed site: denylist catch)
add('logout_ok', 'logout', LOGOUT);
for (const s of SH) add('logout_denylist_' + s, 'logout', LOGOUT, { denylist: s }, {}, s);
for (const s of ['ordinary', 'revoked']) add('logout_revokesession_' + s, 'logout-unchanged', LOGOUT, { revokeSession: s }, {}, s);
// CONNECTOR
add('conn_ok', 'conn', CONN, {}, { upstream: 'valid' });
add('conn_invalid', 'conn', CONN, {}, { upstream: 'invalid' });
add('conn_non2xx', 'conn', CONN, {}, { upstream: 'non2xx' });
for (const s of SH) {
  add('conn_fetch_' + s, 'conn', CONN, { fetch: s }, { upstream: 'valid' }, s);
  add('conn_json_' + s, 'conn', CONN, { json: s }, { upstream: 'valid' }, s);
  add('conn_mint_' + s, 'conn', CONN, { mint: s }, { upstream: 'valid' }, s);
}
// AUTHORIZE POST
add('az_ok', 'az', AZ);
add('az_badpw', 'az', AZ, {}, { badpw: true });
add('az_mfa', 'az', AZ, {}, { mfa: true });
for (const s of SH) {
  add('az_app_' + s, 'az', AZ, { app: s }, {}, s);
  add('az_verify_' + s, 'az', AZ, { verify: s }, {}, s);
  add('az_mintcode_' + s, 'az', AZ, { mintCode: s }, {}, s);
  add('az_deny_app_' + s, 'az', { ...AZ, body: { ...AZ.body, action: 'deny' } }, { app: s }, {}, s);
}
// TOKEN
add('tk_ok', 'tk', TK);
add('tk_badsecret', 'tk', TK, {}, { badsecret: true });
add('rf_ok', 'tk', RF);
add('rf_denied', 'tk', RF, {}, { denied: true });
add('rf_badsecret', 'tk', RF, {}, { badsecret: true });
for (const s of SH) {
  add('tk_app_' + s, 'tk', TK, { app: s }, {}, s);
  add('tk_secret_' + s, 'tk', TK, { secret: s }, {}, s);
  add('tk_exchange_' + s, 'tk', TK, { exchange: s }, {}, s);
  add('tk_user_' + s, 'tk', TK, { userById: s }, {}, s);
  add('tk_session_' + s, 'tk', TK, { session: s }, {}, s);
  add('rf_secret_' + s, 'tk', RF, { secret: s }, {}, s);
  add('rf_isdenied_' + s, 'tk', RF, { isDenied: s }, {}, s);
  add('rf_verify_' + s, 'tk', RF, { verifyRefresh: s }, {}, s);
}
// ISSUER CERTS
add('il_ok', 'ic', IL);
add('ir_ok', 'ic', IR);
add('ir_forbidden_revoke_revoked', 'ic', IR, { certRevoke: 'revoked' }, { user: { userId: 'u', role: 'USER', tenantId: 'ten-1', scopes: [] } }, 'revoked');
for (const s of SH) {
  add('il_list_' + s, 'ic', IL, { certList: s }, {}, s);
  add('ir_get_' + s, 'ic', IR, { certGet: s }, {}, s);
  add('ir_revoke_' + s, 'ic', IR, { certRevoke: s }, {}, s);
}

const SAVED = process.listeners('unhandledRejection');
const onUnh = () => { h.unhandled++; };
let server: Server; let base = '';
const realFetch = globalThis.fetch;
const realConnect = net.Socket.prototype.connect;

beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnh);
  (net.Socket.prototype as any).connect = function (...a: any[]) {
    const o = a[0]; const host = Array.isArray(o) ? String((o[0] as any)?.host ?? (o[0] as any)?.hostname ?? (o[0] as any)?.path ?? 'arr?' + Object.keys(o[0] ?? {}).join('/')) : typeof o === 'object' && o ? String(o.host ?? o.hostname ?? o.path ?? 'obj?' + Object.keys(o).join('/')) : String(a[1] ?? a[0]);
    h.connects.push(String(host)); return (realConnect as any).apply(this, a);
  };
  const { authRoutes } = await import('../routes/auth');
  const { internalRoutes } = await import('../routes/internal');
  const { oauthRouter } = await import('../routes/oauth');
  const { issuerCertsRoutes } = await import('../routes/issuerCerts');
  const { errorHandler } = await import('../middleware/errorHandler');
  const app = express();
  app.use(express.json());
  app.use((req, _r, n) => { (req as any).cookies = { refresh_token: 'RT_cookie' }; n(); });
  app.use('/api/auth', authRoutes);
  app.use('/internal', internalRoutes);
  app.use('/api/oauth', oauthRouter);
  app.use('/ic', issuerCertsRoutes);
  app.use(errorHandler);
  server = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
});
afterAll(async () => {
  server.closeAllConnections();
  await new Promise<void>((r) => server.close(() => r()));
  process.removeListener('unhandledRejection', onUnh);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  (net.Socket.prototype as any).connect = realConnect;
});

describe('g113', () => {
  it('records', async () => {
    const out = process.env.G113_OUT!;
    fs.writeFileSync(out, '');
    const outbound: string[] = [];
    for (const sc of S) {
      h.fail = sc.fail || {}; h.cfg = sc.cfg || {}; h.st = fresh(); h.logs.length = 0; h.unhandled = 0; h.connects.length = 0;
      // stub the upstream security service for the connector route only (any other URL is recorded as outbound)
      globalThis.fetch = (async (url: any, init?: any) => {
        const u = String(url);
        if (u.startsWith(base)) return realFetch(url, init);
        if (!u.includes('/api/keys/validate')) { outbound.push(u); throw new Error('outbound blocked ' + u); }
        if (h.fail.fetch) throw mk(h.fail.fetch);
        const up = h.cfg.upstream;
        return {
          ok: up !== 'non2xx', status: up === 'non2xx' ? 503 : 200,
          json: async () => { if (h.fail.json) throw mk(h.fail.json); return { data: { valid: up === 'valid', organizationId: 'o', tenantId: 't', scopes: ['a'], connectorId: null } }; },
        } as any;
      }) as any;
      let rec: any = { id: sc.id, site: sc.site, shape: sc.shape ?? null };
      try {
        const res = await realFetch(base + sc.path, {
          method: sc.method, headers: { 'Content-Type': 'application/json', ...(sc.headers || {}) },
          body: sc.method === 'GET' ? undefined : JSON.stringify(sc.body ?? {}), redirect: 'manual', signal: AbortSignal.timeout(1500),
        });
        const text = await res.text();
        let body: any = null; try { body = JSON.parse(text); } catch { body = text.slice(0, 60); }
        const loc = res.headers.get('location');
        const sc2 = res.headers.get('set-cookie');
        rec.status = res.status;
        rec.success = body && typeof body === 'object' ? body.success ?? null : null;
        rec.errCode = body?.error?.code ?? (typeof body?.error === 'string' ? body.error : null);
        rec.tokenInBody = /AT_|RT_\d|CT_|CODE_/.test(text);
        rec.codeInLocation = !!(loc && /code=/.test(loc));
        rec.cookie = sc2 ? (/refresh_token=;/.test(sc2) ? 'cleared' : /refresh_token=RT_/.test(sc2) ? 'set' : 'other') : 'none';
        rec.bodyLeaks = /hunter2|10\.0\.0\.7|secret=abc|getter boom/.test(text);
      } catch (e) {
        rec.status = 'NO_RESPONSE'; rec.success = null; rec.errCode = null; rec.tokenInBody = false; rec.codeInLocation = false; rec.cookie = 'none'; rec.bodyLeaks = false;
      }
      await new Promise((r) => setTimeout(r, 30));
      rec.st = h.st; rec.unhandled = h.unhandled;
      rec.logs = h.logs.filter((l) => l.lvl !== 'debug').map((l) => ({ ...l }));
      rec.connects = [...h.connects];
      fs.appendFileSync(out, JSON.stringify(rec) + '\n');
    }
    globalThis.fetch = realFetch;
    fs.appendFileSync(out, JSON.stringify({ id: '__outbound', outbound }) + '\n');
  }, 600000);
});
