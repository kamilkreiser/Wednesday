// QA GATE 93 probe Q1 (NOT part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Drives the REAL auth app (src/index.ts default export, every middleware) -> REAL POST /api/auth/reset-password ->
// REAL userRepo / db.ts / @secuura/shared queryWithTenantGuc / services/password (argon2) / services/session.ts /
// errorHandler. Only the drivers are replaced: `pg` by a recording Pool over a two-table store (users,
// password_reset_tokens; writes staged per transaction and applied on COMMIT), and the ioredis client by an in-memory
// fake injected through session.ts's own __setRedisForTesting. The fake Redis rejects at one command
// (smembers = before any session is touched; get = inside the per-session loop after one revoke; del = after every
// session was revoked) with an ordinary Error or an unreadable value. Logger: the real winston logger, spied (calls through).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import { createHash } from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';

process.env.DATABASE_URL = 'postgres://gate93:stub@127.0.0.1:1/gate93';
const OUT = process.env.PROBE_OUT as string;
const USER = 'a9300000-0000-4000-8000-000000009393';
const TENANT = 'c9300000-0000-4000-8000-000000009393';
const TOKEN = 'gate93-reset-token';
const TOKEN_HASH = createHash('sha256').update(TOKEN).digest('hex');
const NEW_PASSWORD = 'Gate93-Str0ng-Passw0rd!xq';

const h = vi.hoisted(() => ({
  users: new Map<string, any>(),
  tokens: new Map<string, { user_id: string; expires_at: Date; used_at: Date | null }>(),
  sql: [] as string[],
  unknown: [] as string[],
}));

vi.mock('pg', () => {
  const norm = (s: string) => String(s).replace(/\s+/g, ' ').trim();
  type W = () => void;
  function exec(text: string, values: unknown[] | undefined, pending: W[] | null): Promise<any> {
    const n = norm(text);
    const v = (values ?? []) as any[];
    const stage = (w: W) => (pending ? pending.push(w) : w());
    if (/set_config/i.test(n)) { h.sql.push('set_config'); return Promise.resolve({ rows: [{}], rowCount: 1 }); }
    if (/FROM auth_find_user_by_id\(\$1\)/.test(n) || /FROM users WHERE id = \$1/.test(n)) {
      h.sql.push(/auth_find_user_by_id/.test(n) ? 'SELECT user (preauth)' : 'SELECT user');
      const r = h.users.get(String(v[0]));
      return Promise.resolve({ rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 });
    }
    if (/^UPDATE users SET /i.test(n)) {
      const m = n.match(/WHERE id = \$(\d+)/); const id = String(v[Number(m![1]) - 1]);
      const cols = n.replace(/^UPDATE users SET /i, '').replace(/ WHERE.*$/, '').split(', ').map((c) => c.split(' = '));
      h.sql.push('UPDATE users ' + cols.map((c) => c[0]).join(','));
      if (!h.users.has(id)) return Promise.resolve({ rows: [], rowCount: 0 });
      stage(() => { const r = h.users.get(id); for (const [c, p] of cols) { if (/^\$\d+$/.test(p)) r[c] = v[Number(p.slice(1)) - 1]; } r.updated_at = new Date(); });
      return Promise.resolve({ rows: [], rowCount: 1 });
    }
    if (/FROM password_reset_tokens WHERE token_hash = \$1 AND used_at IS NULL/.test(n)) {
      h.sql.push('SELECT reset token');
      const t = h.tokens.get(String(v[0]));
      return Promise.resolve(t && !t.used_at ? { rows: [{ user_id: t.user_id, expires_at: t.expires_at }], rowCount: 1 } : { rows: [], rowCount: 0 });
    }
    if (/^UPDATE password_reset_tokens SET used_at = NOW\(\) WHERE token_hash = \$1/.test(n)) {
      h.sql.push('BURN reset token');
      const t = h.tokens.get(String(v[0]));
      stage(() => { if (t) t.used_at = new Date(); });
      return Promise.resolve({ rows: [], rowCount: t ? 1 : 0 });
    }
    h.unknown.push(n.slice(0, 80));
    return Promise.resolve({ rows: [], rowCount: 0 });
  }
  class Client {
    pending: W[] | null = null;
    query(text: string, values?: unknown[]) {
      const n = norm(text);
      if (n === 'BEGIN') { this.pending = []; return Promise.resolve({ rows: [] }); }
      if (n === 'COMMIT') { for (const w of this.pending ?? []) w(); this.pending = null; return Promise.resolve({ rows: [] }); }
      if (n === 'ROLLBACK') { h.sql.push('ROLLBACK'); this.pending = null; return Promise.resolve({ rows: [] }); }
      return exec(text, values, this.pending);
    }
    release() {}
  }
  class Pool {
    constructor(_o?: unknown) {}
    on() { return this; }
    connect() { return Promise.resolve(new Client()); }
    query(text: string, values?: unknown[]) { return exec(text, values, null); }
    end() { return Promise.resolve(); }
  }
  return { Pool, default: { Pool } };
});

// In-memory Redis driver (the subset session.ts uses), with a one-command failure switch.
const r = { kv: new Map<string, string>(), sets: new Map<string, Set<string>>(), failAt: '' as string, toThrow: undefined as unknown, getCalls: 0 };
const fail = (cmd: string) => {
  if (r.failAt === cmd) { if (cmd !== 'get' || r.getCalls++ >= 1) return Promise.reject(r.toThrow); }
  return null;
};
const fakeRedis = {
  smembers: (k: string) => fail('smembers') ?? Promise.resolve([...(r.sets.get(k) ?? [])]),
  get: (k: string) => fail('get') ?? Promise.resolve(r.kv.get(k) ?? null),
  setex: (k: string, _t: number, val: string) => { r.kv.set(k, val); return Promise.resolve('OK'); },
  srem: (k: string, m: string) => { r.sets.get(k)?.delete(m); return Promise.resolve(1); },
  sadd: (k: string, m: string) => { if (!r.sets.has(k)) r.sets.set(k, new Set()); r.sets.get(k)!.add(m); return Promise.resolve(1); },
  expire: () => Promise.resolve(1),
  del: (k: string) => fail('del') ?? (r.sets.delete(k), Promise.resolve(1)),
  mget: (...ks: string[]) => Promise.resolve(ks.map((k) => r.kv.get(k) ?? null)),
};

const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('redis command rejected'),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};

let server: Server; let base: string; let errSpy: any; let infoSpy: any;
const SAVED = process.listeners('unhandledRejection');
let unhandled = 0; const onUnhandled = () => { unhandled += 1; };

function seed() {
  h.users.clear(); h.tokens.clear(); h.sql.length = 0; r.kv.clear(); r.sets.clear(); r.getCalls = 0;
  const now = new Date();
  h.users.set(USER, { id: USER, email: 'gate93@example.test', password_hash: 'OLD-HASH', role: 'user', status: 'active',
    email_verified: true, tenant_id: TENANT, auth_method: 'email', created_at: now, updated_at: now });
  h.tokens.set(TOKEN_HASH, { user_id: USER, expires_at: new Date(Date.now() + 600_000), used_at: null });
  for (const sid of ['s-a', 's-b']) {
    r.kv.set('sess:' + sid, JSON.stringify({ id: sid, userId: USER, isActive: true }));
    if (!r.sets.has('user_sessions:' + USER)) r.sets.set('user_sessions:' + USER, new Set());
    r.sets.get('user_sessions:' + USER)!.add(sid);
  }
}
function sessionsState() {
  return ['s-a', 's-b'].map((sid) => { const raw = r.kv.get('sess:' + sid); return sid + ':' + (raw ? (JSON.parse(raw).isActive ? 'ACTIVE' : 'revoked') : 'gone'); })
    .concat(['set:' + (r.sets.has('user_sessions:' + USER) ? [...r.sets.get('user_sessions:' + USER)!].join('|') || '(empty)' : 'deleted')]);
}

beforeAll(async () => {
  const session: any = await import('../services/session');
  session.__setRedisForTesting(fakeRedis);
  const { logger } = await import('../utils/logger');
  errSpy = vi.spyOn(logger as any, 'error'); infoSpy = vi.spyOn(logger as any, 'info');
  const mod: any = await import('../index');
  await new Promise<void>((res) => { server = mod.default.listen(0, '127.0.0.1', res); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  appendFileSync(OUT, JSON.stringify({ positive_control: { isRedisAvailable: session.isRedisAvailable() } }) + '\n');
}, 120000);
afterAll(async () => {
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  if (server) await new Promise<void>((res) => server.close(() => res()));
});

const CASES: [string, string][] = [['none', 'control'], ...['smembers', 'get', 'del'].flatMap((c) => Object.keys(KINDS).map((k) => [c, k] as [string, string]))];
describe('gate93 probe reset-password', () => {
  for (const [failAt, kind] of CASES) {
    it(`${failAt}/${kind}`, async () => {
      seed(); unhandled = 0; errSpy.mockClear(); infoSpy.mockClear();
      r.failAt = failAt === 'none' ? '' : failAt; r.toThrow = kind === 'control' ? undefined : KINDS[kind]();
      const res = await fetch(base + '/api/auth/reset-password', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: TOKEN, password: NEW_PASSWORD }) });
      const body = await res.json().catch(() => null);
      await new Promise((z) => setTimeout(z, 50));
      const u = h.users.get(USER); const t = h.tokens.get(TOKEN_HASH)!;
      const errLines = errSpy.mock.calls.map((c: any[]) => {
        let meta: any = c[1]; try { meta = JSON.parse(JSON.stringify(meta, (k, v) => (k === 'stack' ? '<stack>' : v))); } catch { meta = '<unserialisable>'; }
        return [c[0], meta];
      });
      const snap = { password_changed: u.password_hash !== 'OLD-HASH', password_is_argon2: /^\$argon2/.test(String(u.password_hash)),
        token_used: !!t.used_at, sessions: sessionsState(), sql: [...h.sql], unhandled };
      h.sql.length = 0;
      // second attempt with the same link (is the link still usable for a retry?)
      r.failAt = ''; r.getCalls = 0;
      const retry = await fetch(base + '/api/auth/reset-password', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: TOKEN, password: NEW_PASSWORD }) });
      const rec = {
        case: `${failAt}/${kind}`, status: res.status, body, ...snap,
        error_lines: errLines, unknown_sql: [...h.unknown], retry_sql: [...h.sql],
        retry_status: retry.status, sessions_after_retry: sessionsState(), token_used_after_retry: !!h.tokens.get(TOKEN_HASH)!.used_at,
      };
      appendFileSync(OUT, JSON.stringify(rec) + '\n');
    }, 30000);
  }
});
