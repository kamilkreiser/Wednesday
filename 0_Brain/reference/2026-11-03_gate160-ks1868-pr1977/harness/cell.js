// G160 recorder cell: one process per (version, path, kind, env, mode).
// argv: version(base|head) path(listener|connect|pool|migrate|up) kind mode(default|survive)
// NODE_ENV comes from the parent (development|production). Real auth logger (winston), real session/db/
// refreshDenylist/accountLockout. Replaced: ioredis, pg, @secuura/shared only (Module._load stub).
const path = require('path');
const Module = require('module');
const { EventEmitter } = require('events');
const [, , version, cellPath, kind, mode = 'default'] = process.argv;
const W = path.resolve(__dirname, '..');
const AUTH = path.join(W, 'repo/Blockchain/Dev/services/auth');
const BUILD = process.env.G160_BUILD || path.join(__dirname, 'build_' + version);
const out = { version, path: cellPath, kind, mode, env: process.env.NODE_ENV, steps: [] };
const uncaught = [];
if (mode === 'survive') {
  process.on('uncaughtException', (e) => { uncaught.push(safeDesc(e)); });
  process.on('unhandledRejection', (e) => { uncaught.push('rej:' + safeDesc(e)); });
}
function safeDesc(e) { try { return String(e && e.message !== undefined ? e.message : e).slice(0, 80); } catch { return '<undescribable>'; } }

// ---- values ----
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMessage = (m) => Object.create(Error.prototype, { message: { get() { return m; } } });
const KINDS = {
  ordinaryError: () => new Error('g160 boom'),
  plainString: () => 'g160 boom',
  number42: () => 42,
  null: () => null,
  undefined: () => undefined,
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => withMessage(Symbol('g160')),
  bigintMessage: () => withMessage(10n),
  bigintValue: () => 10n,
  messageToJSONThrows: () => withMessage({ toJSON() { throw new Error('toJSON boom'); } }),
  errToJSONThrows: () => { const e = new Error('g160 boom'); e.toJSON = () => { throw new Error('toJSON boom'); }; return e; },
  objToStringThrows: () => ({ toString() { throw new Error('toString boom'); } }),
  messageToStringThrows: () => withMessage({ toString() { throw new Error('toString boom'); } }),
  messageIsRevokedProxy: () => withMessage(revoked()),
  cyclicMessage: () => { const o = { a: 1 }; o.self = o; return withMessage(o); },
  numberMessage: () => withMessage(42),
};

// ---- stubs ----
const store = new Map();
let redisDown = false;
let redisClient = null;
class RedisStub extends EventEmitter {
  constructor() { super(); this.status = 'wait'; redisClient = this; }
  async connect() { if (cellPath === 'connect') throw KINDS[kind](); this.status = 'ready'; }
  _c() { if (redisDown) throw new Error('Connection is closed.'); }
  async ping() { this._c(); return 'PONG'; }
  async get(k) { this._c(); return store.has(k) ? store.get(k) : null; }
  async set(k, v) { this._c(); store.set(k, v); return 'OK'; }
  async setex(k, t, v) { this._c(); store.set(k, v); return 'OK'; }
  async exists(k) { this._c(); return store.has(k) ? 1 : 0; }
  async smembers(k) { this._c(); return [...(store.get(k) || [])]; }
  async sadd(k, m) { this._c(); const s = store.get(k) || new Set(); s.add(m); store.set(k, s); return 1; }
  async srem(k, m) { this._c(); const s = store.get(k); if (s) s.delete(m); return 1; }
  async expire() { this._c(); return 1; }
  async del(...ks) { this._c(); ks.forEach((k) => store.delete(k)); return 1; }
  async incr(k) { this._c(); const n = Number(store.get(k) || 0) + 1; store.set(k, String(n)); return n; }
  async mget(...ks) { this._c(); return ks.map((k) => (store.has(k) ? store.get(k) : null)); }
  disconnect() {}
}
let poolInst = null;
let ddlAttempts = 0;
class PoolStub extends EventEmitter {
  constructor() { super(); poolInst = this; }
  async query(sql) {
    if (sql.indexOf('SELECT 1') === 0) return { rows: [{ ok: 1 }] };
    ddlAttempts += 1;
    if (cellPath === 'migrate') throw KINDS[kind]();
    return { rows: [] };
  }
  async end() {}
  async connect() { return { query: async () => ({ rows: [] }), release() {} }; }
}
const shared = {
  applyTenantGuc: async () => undefined,
  runWithTenantId: (_id, fn) => fn(),
  queryWithTenantGuc: (pool, text, params) => pool.query(text, params),
};
const origLoad = Module._load;
Module._load = function (req, parent, isMain) {
  if (req === 'ioredis') return RedisStub;
  if (req === 'pg') return { Pool: PoolStub };
  if (req === '@secuura/shared') return shared;
  if (req === 'winston') return origLoad.call(this, require.resolve('winston', { paths: [AUTH] }), parent, isMain);
  return origLoad.apply(this, arguments);
};

// ---- capture console output of the real logger (winston Console transport writes via console._stdout / process.stdout) ----
const logLines = [];
const origOut = process.stdout.write.bind(process.stdout);
const origErr = process.stderr.write.bind(process.stderr);
process.stdout.write = (c, ...a) => { logLines.push(String(c)); return true; };
process.stderr.write = (c, ...a) => { logLines.push(String(c)); return true; };
function emitResult() {
  out.uncaught = uncaught;
  out.logs = logLines.map((l) => l.replace(/\u001b\[[0-9;]*m/g, '').trim()).filter(Boolean).map((l) => l.slice(0, 300));
  origOut('G160RESULT ' + JSON.stringify(out) + '\n');
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function tryStep(name, fn) {
  try { const v = await fn(); out[name] = v; } catch (e) { out[name] = 'THREW:' + safeDesc(e); }
}

async function sessionCell() {
  process.env.REDIS_URL = 'redis://stub:6379';
  const sess = require(path.join(BUILD, 'services/session.js'));
  const deny = require(path.join(BUILD, 'services/refreshDenylist.js'));
  const lock = require(path.join(BUILD, 'services/accountLockout.js'));
  // Mirror index.ts:256 + :309-314 (start().catch -> logger.error + process.exit(1)).
  const { logger } = require(path.join(BUILD, 'utils/logger.js'));
  let initOutcome;
  try { await sess.initRedisSession(); initOutcome = 'resolved'; } catch (err) {
    initOutcome = 'REJECTED';
    out.initOutcome = initOutcome;
    try { logger.error('Failed to start auth service', { error: err }); } catch (e2) { out.startCatchThrew = safeDesc(e2); }
    await sleep(30);
    out.wouldExit1 = true; // index.ts calls process.exit(1) here
    out.flagAfter = sess.isRedisAvailable();
    emitResult();
    process.exit(1);
  }
  out.initOutcome = initOutcome;
  out.flagAfterInit = sess.isRedisAvailable();
  // seed state (only possible if a client is live)
  if (redisClient && sess.isRedisAvailable()) {
    const now = Date.now();
    store.set('sess:sess_A', JSON.stringify({ id: 'sess_A', userId: 'u1', token: 't', refreshToken: 'r', expiresAt: new Date(now + 3600e3), lastActivityAt: new Date(now), createdAt: new Date(now), isActive: true }));
    store.set('user_sessions:u1', new Set(['sess_A']));
    store.set('lockout:locked:victim@x.io:1.2.3.0/24', '1');
    store.set('refresh_denylist:J1', '1');
  }
  if (cellPath === 'listener') {
    // ioredis emits 'error' from socket/event-loop callbacks, outside any caller's try.
    await new Promise((resolve) => setImmediate(() => {
      redisDown = true;
      try { redisClient.emit('error', KINDS[kind]()); out.emitReturned = true; }
      catch (e) { out.emitReturned = false; throw e; } // re-throw: as from the event loop -> uncaught
      finally { resolve(); }
    }));
    await sleep(30);
  }
  out.flagAfter = sess.isRedisAvailable();
  out.alive = true;
  await tryStep('getSession', async () => { const s = await sess.getSession('sess_A'); return s ? 'ACCEPTED' : 'null'; });
  await tryStep('createSession', async () => { await sess.createSession({ id: 'u2' }); return 'created'; });
  out.passwordChange = sess.isRedisAvailable() ? 'proceeds-to-write' : '503';
  out.passwordReset = sess.isRedisAvailable() ? 'proceeds-to-write' : '503';
  await tryStep('denylistRevokedJ1', () => deny.isRefreshJtiDenylisted('J1'));
  await tryStep('denylistFreshJ2', () => deny.isRefreshJtiDenylisted('J2'));
  await tryStep('lockoutLockedVictim', () => lock.isLockedOut(sess.getRedisClient(), 'victim@x.io', '1.2.3.4'));
  out.health = sess.getRedisClient() ? 'client-present' : 'degraded';
  await sleep(20);
  emitResult();
}

async function dbCell() {
  process.env.DATABASE_URL = 'postgresql://stub/stub';
  const db = require(path.join(BUILD, 'db.js'));
  const { logger } = require(path.join(BUILD, 'utils/logger.js'));
  let initResult;
  try { initResult = await db.initDb(); out.initOutcome = 'resolved'; } catch (err) {
    out.initOutcome = 'REJECTED';
    try { logger.error('Failed to start auth service', { error: err }); } catch (e2) { out.startCatchThrew = safeDesc(e2); }
    await sleep(30);
    out.wouldExit1 = true; out.flagAfter = db.isDbAvailable(); out.ddlAttempts = ddlAttempts;
    emitResult(); process.exit(1);
  }
  out.initResult = initResult;
  out.ddlAttempts = ddlAttempts;
  if (cellPath === 'pool') {
    await new Promise((resolve) => setImmediate(() => {
      try { poolInst.emit('error', KINDS[kind]()); out.emitReturned = true; }
      catch (e) { out.emitReturned = false; throw e; }
      finally { resolve(); }
    }));
    await sleep(30);
  }
  out.flagAfter = db.isDbAvailable();
  out.alive = true;
  await sleep(20);
  emitResult();
}

(cellPath === 'pool' || cellPath === 'migrate' ? dbCell() : sessionCell()).catch((e) => {
  out.harnessError = safeDesc(e); emitResult(); process.exit(3);
});
