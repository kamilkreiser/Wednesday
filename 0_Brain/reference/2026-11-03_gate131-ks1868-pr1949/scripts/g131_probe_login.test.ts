// QA gate 131 probe (NOT part of the PR). Real routes/auth.ts, real passwordLoginGate, real password (bcrypt/argon2),
// real accountLockout, real session, real refreshDenylist, real jwt, real totp, real authenticate middleware, real
// errorHandler, real userRepo, REAL winston logger (the auth logger module, unmocked; a capture transport is added).
// Stubbed: ../db query (SQL responder + recorder), redis (in-memory fake injected via __setRedisForTesting),
// ../events (the redis bus; publish calls recorded = the audit event).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import fs from 'node:fs';
import crypto from 'node:crypto';
import express from 'express';
import cookieParser from 'cookie-parser';
import Transport from 'winston-transport';

process.env.PII_ENCRYPTION_KEY = crypto.randomBytes(32).toString('hex');
process.env.PII_ENCRYPTION_KEY_VERSION = '1';
process.env.PII_LOOKUP_HMAC_KEY = crypto.randomBytes(32).toString('hex');
delete process.env.PLATFORM_DATABASE_URL;

const h = vi.hoisted(() => ({
  sql: [] as Array<{ sql: string; failed: boolean }>,
  row: null as any,
  rehashRejects: false,
  denylistRejects: false,
  toThrow: undefined as unknown,
  events: [] as string[],
}));

vi.mock('../db', async () => {
  const actual: any = await vi.importActual('../db');
  const query = async (sql: string, params?: unknown[]) => {
    const s = sql.replace(/\s+/g, ' ').trim();
    if (/^UPDATE users SET password_hash/i.test(s) && h.rehashRejects) {
      h.sql.push({ sql: s.slice(0, 60), failed: true });
      return Promise.reject(h.toThrow);
    }
    h.sql.push({ sql: s.slice(0, 60), failed: false });
    if (/subject_deks|subject_key/i.test(s)) return { rows: [], rowCount: 0 };
    if (/^UPDATE/i.test(s)) return { rows: [], rowCount: 1 };
    if (/^SELECT/i.test(s)) return { rows: h.row ? [{ ...h.row }] : [], rowCount: h.row ? 1 : 0 };
    return { rows: [], rowCount: 0 };
  };
  return { ...actual, query, getClient: async () => { throw new Error('probe: no client'); }, transaction: async () => { throw new Error('probe: no tx'); }, isDbAvailable: () => true };
});
vi.mock('../events', async () => {
  const actual: any = await vi.importActual('../events');
  return { ...actual, publishEvent: async (t: string) => { h.events.push(t); } };
});

class FakeRedis {
  m = new Map<string, string>();
  s = new Map<string, Set<string>>();
  async get(k: string) { return this.m.has(k) ? this.m.get(k)! : null; }
  async set(k: string, v: string) { this.m.set(k, String(v)); return 'OK'; }
  async setex(k: string, _t: number, v: string) {
    if (k.startsWith('refresh_denylist:') && h.denylistRejects) return Promise.reject(h.toThrow);
    this.m.set(k, String(v)); return 'OK';
  }
  async del(...ks: string[]) { let n = 0; for (const k of ks.flat()) { if (this.m.delete(k)) n++; if (this.s.delete(k)) n++; } return n; }
  async incr(k: string) { const v = parseInt(this.m.get(k) || '0', 10) + 1; this.m.set(k, String(v)); return v; }
  async expire() { return 1; }
  async exists(k: string) { return this.m.has(k) || this.s.has(k) ? 1 : 0; }
  async sadd(k: string, ...v: string[]) { const x = this.s.get(k) || new Set(); v.flat().forEach((i) => x.add(i)); this.s.set(k, x); return v.length; }
  async srem(k: string, ...v: string[]) { const x = this.s.get(k); v.flat().forEach((i) => x?.delete(i)); return 1; }
  async smembers(k: string) { return [...(this.s.get(k) || [])]; }
  async mget(...ks: string[]) { return ks.flat().map((k) => (this.m.has(k) ? this.m.get(k)! : null)); }
  async ttl() { return 100; }
  async ping() { return 'PONG'; }
  on() { return this; }
}

const logs: Array<{ level: string; message: string; metaKeys: string[]; error: string }> = [];
class Cap extends Transport {
  log(info: any, cb: () => void) {
    let err = '<absent>';
    try { const e = info.error; err = e === undefined ? '<absent>' : typeof e === 'string' ? JSON.stringify(e) : '<' + typeof e + '>'; } catch { err = '<threw>'; }
    let keys: string[] = [];
    try { keys = Object.keys(info).filter((k) => !['level', 'message', 'timestamp', 'service'].includes(k)); } catch { keys = ['<threw>']; }
    logs.push({ level: String(info.level), message: String(info.message), metaKeys: keys, error: err });
    cb();
  }
}

let server: Server; let base = ''; let redis: FakeRedis; let unhandled = 0;
const onUnh = () => { unhandled += 1; };
const PW = 'pw-correct-horse-ks1868';
const EMAIL = 'g131-login@secuura.local';
let bcryptHash = '';
let totpSecret = '';
let totp: any;

beforeAll(async () => {
  process.on('unhandledRejection', onUnh);
  const shared: any = await import('@secuura/shared');
  shared.initFromEnv();
  const bcrypt: any = (await import('bcryptjs')).default;
  bcryptHash = await bcrypt.hash(PW, 4);
  totp = await import('../services/totp');
  totpSecret = totp.generateTotpSecret();
  const jwt: any = await import('../services/jwt');
  await jwt.initJwtKeys();
  const session: any = await import('../services/session');
  redis = new FakeRedis();
  session.__setRedisForTesting(redis);
  const { logger } = await import('../utils/logger');
  logger.add(new Cap());
  const { authRoutes } = await import('../routes/auth');
  const { errorHandler } = await import('../middleware/errorHandler');
  const app = express();
  app.use(express.json());
  app.use(cookieParser());
  app.use('/api/auth', authRoutes);
  app.use(errorHandler);
  server = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
});
afterAll(async () => { process.removeListener('unhandledRejection', onUnh); await new Promise<void>((r) => server.close(() => r())); });

const mkRow = (mfa: boolean) => ({
  id: '11111111-1111-4111-8111-111111111111', email: EMAIL, email_verified: true, password_hash: bcryptHash,
  status: 'active', role: 'owner', verification_level: 'basic', mfa_enabled: mfa, mfa_secret: mfa ? totpSecret : null,
  mfa_backup_codes: null, tenant_id: 'a0000000-0000-4000-8000-000000000001', organization_id: null,
  created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
});
const revokedProxy = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const withMessage = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const KINDS: Record<string, () => unknown> = {
  'ordinary Error': () => new Error('db down'),
  'Error, message undefined': () => Object.create(Error.prototype),
  'thrown string': () => 'plain boom',
  'message = revoked Proxy': () => withMessage(revokedProxy()),
  'message = toString throws': () => withMessage({ toString() { throw new Error('x'); } }),
  'message = null-proto object': () => withMessage(Object.create(null)),
  'message = Symbol': () => withMessage(Symbol('ks1868')),
  'err = revoked Proxy': () => revokedProxy(),
  'message getter throws': () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } }),
};

function snapshot() {
  const sessions = [...redis.m.entries()].filter(([k]) => k.startsWith('sess:')).map(([, v]) => { try { return JSON.parse(v).isActive; } catch { return '?'; } });
  const lock = [...redis.m.entries()].filter(([k]) => k.startsWith('lockout:')).map(([k, v]) => k.split(':')[1] + '=' + v);
  const deny = [...redis.m.keys()].filter((k) => k.startsWith('refresh_denylist:')).length;
  return { sessionsActive: sessions.filter((x) => x === true).length, sessionsInactive: sessions.filter((x) => x === false).length, lockout: lock, denylistKeys: deny };
}
async function call(path: string, body: unknown, headers: Record<string, string> = {}) {
  try {
    const res = await fetch(base + path, { method: 'POST', headers: { 'Content-Type': 'application/json', ...headers }, body: JSON.stringify(body), signal: AbortSignal.timeout(4000) });
    const text = await res.text();
    let j: any = null; try { j = JSON.parse(text); } catch { /* */ }
    return { status: res.status, setCookie: res.headers.get('set-cookie') || '', j, text };
  } catch (e) { return { status: 'NO ANSWER (' + String((e as Error).name) + ')', setCookie: '', j: null, text: '' }; }
}
const out: any[] = [];
function summarise(name: string, r: any, before: number) {
  const L = logs.slice(before);
  out.push({
    case: name,
    status: r.status,
    errCode: r.j?.error?.code ?? null,
    errMsg: r.j?.error?.message ?? null,
    accessToken: Boolean(r.j?.data?.accessToken),
    refreshCookieSet: /refresh_token=[^;]+;/.test(r.setCookie) && !/refresh_token=;/.test(r.setCookie),
    refreshCookieCleared: /refresh_token=;/.test(r.setCookie),
    ...snapshot(),
    rehashAttempted: h.sql.filter((q) => /password_hash/i.test(q.sql)).length,
    lastLoginWrite: h.sql.filter((q) => /last_login_at/i.test(q.sql)).length,
    mfaReencryptWrite: h.sql.filter((q) => /mfa_secret =/i.test(q.sql)).length,
    events: [...h.events],
    logs: L.filter((l) => /UPGRADE|denylist|logged|lockout|MFA|failed|error/i.test(l.message)).map((l) => `${l.level}|${l.message}|keys=${l.metaKeys.join(',')}|error=${l.error}`),
    unhandled,
  });
}
function reset(mfa: boolean) { redis.m.clear(); redis.s.clear(); h.sql = []; h.events = []; h.rehashRejects = false; h.denylistRejects = false; h.toThrow = undefined; h.row = mkRow(mfa); unhandled = 0; redis.m.set('lockout:counter:' + EMAIL + ':127.0.0.0/24', '2'); }

describe('G131 probe: login + logout through the real auth stack', () => {
  it('runs every case and writes the table', async () => {
    // L0 control
    reset(false); let b = logs.length;
    summarise('L0 login, no failure (MFA off)', await call('/api/auth/login', { email: EMAIL, password: PW }), b);
    for (const [k, mk] of Object.entries(KINDS)) {
      reset(false); h.rehashRejects = true; h.toThrow = mk(); b = logs.length;
      summarise('L1 login MFA off, rehash write rejects: ' + k, await call('/api/auth/login', { email: EMAIL, password: PW }), b);
    }
    // credential / MFA / lockout gates, rehash armed with the worst value
    const worst = KINDS['message = revoked Proxy'];
    reset(false); h.rehashRejects = true; h.toThrow = worst(); b = logs.length;
    summarise('G1 wrong password, rehash armed (revoked Proxy msg)', await call('/api/auth/login', { email: EMAIL, password: 'wrong-pw-xx' }), b);
    reset(false); h.rehashRejects = true; h.toThrow = worst(); b = logs.length;
    await redis.set('lockout:locked:' + EMAIL + ':127.0.0.0/24', '1');
    summarise('G2 locked out + correct password, rehash armed', await call('/api/auth/login', { email: EMAIL, password: PW }), b);
    reset(true); h.rehashRejects = true; h.toThrow = worst(); b = logs.length;
    summarise('G3 MFA on, no code, rehash armed', await call('/api/auth/login', { email: EMAIL, password: PW }), b);
    reset(true); h.rehashRejects = true; h.toThrow = worst(); b = logs.length;
    const bad = totp.generateTotpCode(totpSecret) === '000000' ? '111111' : '000000';
    summarise('G4 MFA on, wrong code, rehash armed', await call('/api/auth/login', { email: EMAIL, password: PW, mfaCode: bad }), b);
    for (const k of ['ordinary Error', 'message = revoked Proxy', 'message = toString throws']) {
      reset(true); h.rehashRejects = true; h.toThrow = KINDS[k](); b = logs.length;
      summarise('G5 MFA on, right code, rehash write rejects: ' + k, await call('/api/auth/login', { email: EMAIL, password: PW, mfaCode: totp.generateTotpCode(totpSecret) }), b);
    }
    // logout: a real login first, then logout with the real token + refresh cookie; the denylist setex rejects.
    for (const [k, mk] of [['no failure', null], ...Object.entries(KINDS)] as Array<[string, (() => unknown) | null]>) {
      reset(false);
      const li = await call('/api/auth/login', { email: EMAIL, password: PW });
      const at = li.j?.data?.accessToken; const rt = (/refresh_token=([^;]+);/.exec(li.setCookie) || [])[1];
      if (mk) { h.denylistRejects = true; h.toThrow = mk(); }
      b = logs.length;
      summarise('O logout, denylist write ' + (mk ? 'rejects: ' + k : k), await call('/api/auth/logout', {}, { Authorization: 'Bearer ' + at, Cookie: 'refresh_token=' + rt }), b);
    }
    fs.writeFileSync(process.env.G131_OUT || '/dev/null', JSON.stringify(out, null, 1));
  }, 120000);
});
