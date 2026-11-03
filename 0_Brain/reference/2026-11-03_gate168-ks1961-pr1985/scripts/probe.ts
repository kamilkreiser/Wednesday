// QA gate 168 probe. usage: node --import tsx probe.ts <base|head> <cell> <val>
// Real security.ts / rateLimitEnforce.ts / services/redis.ts / utils/logger (winston), express over real HTTP.
// Replaced: 'ioredis' by a Map-backed stand-in that honours TTLs like Redis (PEXPIRE <=0 deletes the key; a non-integer or
// out-of-range PEXPIRE rejects with Redis's own error text; INCR/GET respect expiry). A command can reject with the cell's value.
// Base = develop's two middleware files resolved in place of head's (same directory, so their relative imports are the real ones).
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985';
process.chdir(W + '/logs/child_cwd');
const Module = require('module');
const EventEmitter = require('events');
const fs = require('fs');
const [variant, cell, valName] = process.argv.slice(2);
process.env.NODE_ENV = 'test';
process.env.LOG_LEVEL = 'debug';
const PLANT = 'G168PLANT-' + 'q9x7Kz'; // planted "secret" text; must never appear in a head log line
const SRC = W + '/repo/Blockchain/Dev/services/api-gateway/src/';
const outLines: string[] = [];
const realErr = process.stderr.write.bind(process.stderr);
(process.stdout as any).write = (c: any) => { outLines.push(String(c)); return true; };
(process.stderr as any).write = (c: any) => { outLines.push('STDERR:' + String(c)); return true; };
const origWarn = console.warn; console.warn = (...a: unknown[]) => { outLines.push('CONSOLE.WARN:' + a.map(String).join(' ') + '\n'); };
setTimeout(() => { realErr('WATCHDOG ' + cell + ' ' + valName + '\n'); process.exit(3); }, 150000).unref();
const G: any = globalThis;
G.__store = new Map<string, string>(); G.__exp = new Map<string, number>();
G.__fail = {} as Record<string, () => unknown>; G.__calls = [] as string[];
const live = (k: string) => { const e = G.__exp.get(k); if (e !== undefined && Date.now() >= e) { G.__store.delete(k); G.__exp.delete(k); } return G.__store.has(k); };
class FakeRedis extends EventEmitter {
  status = 'wait';
  constructor() { super(); G.__client = this; }
  private gate(cmd: string) { G.__calls.push(cmd); const f = G.__fail[cmd]; if (f === undefined) return null; const v = f(); return v === '__HANG__' ? new Promise(() => {}) : Promise.reject(v); }
  async connect() { if (G.__noConnect) throw new Error('ECONNREFUSED'); this.status = 'ready'; this.emit('connect'); this.emit('ready'); }
  async get(k: string) { G.__lastGetKey = k; return this.gate('get') ?? (live(k) ? G.__store.get(k) : null); }
  async setex(k: string, _t: number, v: string) { return this.gate('setex') ?? (G.__store.set(k, v), 'OK'); }
  async set(k: string, v: string) { return this.gate('set') ?? (G.__store.set(k, v), 'OK'); }
  async del(k: string) { return this.gate('del') ?? (G.__store.delete(k) ? 1 : 0); }
  async incr(k: string) { const g = this.gate('incr'); if (g) return g; const n = Number(live(k) ? G.__store.get(k) : 0) + 1; G.__store.set(k, String(n)); return n; }
  async pexpire(k: string, ms: unknown) {
    const g = this.gate('pexpire'); if (g) return g;
    const s = String(ms);
    if (!/^-?\d+$/.test(s) || Math.abs(Number(s)) > 9.2e18) throw new Error('ERR value is not an integer or out of range');
    if (!live(k)) return 0;
    if (Number(s) <= 0) { G.__store.delete(k); G.__exp.delete(k); return 1; }
    G.__exp.set(k, Date.now() + Number(s)); return 1;
  }
  async pttl(k: string) { const g = this.gate('pttl'); if (g) return g; if (!live(k)) return -2; const e = G.__exp.get(k); return e === undefined ? -1 : e - Date.now(); }
  async quit() { return 'OK'; }
  async ping() { return 'PONG'; }
}
const origLoad = Module._load;
Module._load = function (req: string, ...rest: unknown[]) {
  if (req === 'ioredis') return { __esModule: true, default: FakeRedis, Redis: FakeRedis };
  return origLoad.call(this, req, ...rest);
};
const SWAP: Record<string, string> = {};
for (const f of ['security', 'rateLimitEnforce']) SWAP[SRC + 'middleware/' + f + '.ts'] = SRC + 'middleware/' + f + '.g168base.ts';
const origResolve = Module._resolveFilename;
Module._resolveFilename = function (req: string, ...rest: unknown[]) {
  const r = origResolve.call(this, req, ...rest);
  return variant === 'base' && SWAP[r] ? SWAP[r] : r;
};
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('boom'),
  secretError: () => new Error('ECONNRESET auth=' + PLANT),
  secretString: () => 'redis said ' + PLANT,
  revokedProxy: revoked,
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  secretObject: () => ({ code: 'X', password: PLANT }),
  hang: () => '__HANG__',
};
const short = (e: unknown) => { try { return e instanceof Error ? e.constructor.name + ':' + e.message : typeof e; } catch { return 'unprintable'; } };
const unhandled: string[] = [];
process.on('unhandledRejection', (r: unknown) => { unhandled.push(short(r)); });
process.on('uncaughtException', (e) => { unhandled.push('UNCAUGHT ' + short(e)); });
const svcRequire = Module.createRequire(SRC + 'index.ts');
const express = svcRequire('express');
const winston = require(SRC + 'utils/logger');
const redisSvc = require(SRC + 'services/redis');
const { createBruteForceProtection } = require(SRC + 'middleware/security');
const { enforceClientRateLimit } = require(SRC + 'middleware/rateLimitEnforce');
const CONFIG = { bruteForce: { freeRetries: 2, minWait: 1000, maxWait: 60000, lifetime: 900000 }, suspiciousPatterns: [] };
async function hit(base: string, path: string) {
  const t0 = Date.now();
  try {
    const r = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{"email":"a@b.c","password":"x"}', signal: AbortSignal.timeout(4000) });
    const t = await r.text();
    return { status: r.status, ms: Date.now() - t0, limit: r.headers.get('x-ratelimit-limit'), retryAfter: r.headers.get('retry-after'), body: t.slice(0, 220) };
  } catch (e) { return { status: 0, ms: Date.now() - t0, body: 'NO ANSWER (' + short(e) + ')' }; }
}
function listen(app: any): Promise<{ base: string; srv: any }> {
  return new Promise((res) => { const srv = app.listen(0, '127.0.0.1', () => res({ base: 'http://127.0.0.1:' + srv.address().port, srv })); });
}
function parseVal(s: string): unknown {
  const T: Record<string, unknown> = { NL1: '1\n', NaN: NaN, Infinity: Infinity, negInfinity: -Infinity, obj: {}, true: true, arr5: [5], str100: '100', str5: '5', str99: '99', str1e3: '1e3', str120: '120', str30: '30', empty: '', missing: undefined, null: null, pow53: 2 ** 53, '1e300': 1e300 };
  return s in T ? T[s] : Number(s);
}
function done(o: Record<string, unknown>) {
  setTimeout(() => {
    const text = outLines.join('');
    const logs = text.split('\n').filter((l) => /BruteForce|rateLimit|BRUTE|STDERR|CONSOLE/.test(l)).map((l) => l.replace(/\x1b\[[0-9;]*m/g, '').replace(/^\d{4}-\d\d-\d\d \S+ /, '').slice(0, 300));
    fs.writeSync(1, JSON.stringify({ variant, cell, val: valName, ...o, unhandled, plantInLogs: text.split(PLANT).length - 1, logs }) + '\n');
    process.exit(0);
  }, 300);
}
(async () => {
  if (cell === 'rl_notconnected' || cell === 'rl_window_mem') G.__noConnect = true;
  try { await redisSvc.initRedis(); } catch { /* KS-617: not connected */ }
  const app = express();
  app.use(express.json());
  const r: Record<string, unknown> = { redisAvailable: redisSvc.isRedisAvailable() };
  let reached = 0;
  if (cell.startsWith('bf')) {
    // ---------------- brute-force guard ----------------
    const guard = createBruteForceProtection(CONFIG);
    app.use((req: any, res: any, next: any) => {
      if (cell === 'bf_429throw') { const o = res.setHeader.bind(res); res.setHeader = (n: string, v: unknown) => { if (n === 'Retry-After') throw new Error('hdr ' + PLANT); return o(n, v); }; }
      guard(req, res, next);
    });
    app.use((req: any, res: any) => { reached++; res.status(401).json({ downstream: true, helper: Boolean(req.bruteForce) }); });
    const { base, srv } = await listen(app);
    await hit(base, '/api/auth/login'); // prime: learn the real key the guard reads (no fault)
    const key = G.__lastGetKey; r.key = key; reached = 0;
    const before = JSON.stringify([...G.__store.entries()]);
    if (cell === 'bf_fault') { G.__fail.get = VALUES[valName]; }
    if (cell === 'bf_record') { G.__store.set(key, ({ corrupt: 'not json{', five: '5', arr: '[]', soonStr: '{"blockedUntil":"soon"}', attemptsStr: '{"attempts":"x"}', blockedNoAttempts: JSON.stringify({ blockedUntil: Date.now() + 600000 }), blockedNumStr: JSON.stringify({ attempts: 9, blockedUntil: String(Date.now() + 600000) }), blockedNull: '{"attempts":1,"blockedUntil":null}', nullStr: 'null', strRec: '"x"', clean: '{"attempts":1}', proto: '{"attempts":1,"__proto__":{"blockedUntil":99999999999999}}' } as Record<string, string>)[valName]); }
    if (cell === 'bf_lockout' || cell === 'bf_429throw') {
      G.__store.set(key, JSON.stringify({ attempts: 9, blockedUntil: Date.now() + 600000 }));
      if (valName !== 'none') G.__fail.get = VALUES[valName];
    }
    const writesBefore = G.__calls.filter((c: string) => c === 'setex' || c === 'del').length;
    r.resp = await hit(base, '/api/auth/login');
    r.downstream = reached;
    r.storeChanged = JSON.stringify([...G.__store.entries()]) !== before && cell !== 'bf_record' && cell !== 'bf_lockout' && cell !== 'bf_429throw' ? true : 'n/a-or-false';
    r.storeAfter = G.__store.get(key) ?? null;
    r.writes = G.__calls.filter((c: string) => c === 'setex' || c === 'del').length - writesBefore;
    srv.closeAllConnections(); srv.close();
  } else {
    // ---------------- per-client limiter ----------------
    const limiter = enforceClientRateLimit();
    const [rlRaw, winRaw, nRaw, waitRaw] = (valName || '').split('~');
    const rateLimit = cell === 'rl_value' || cell === 'rl_time' ? parseVal(rlRaw) : cell === 'rl_window' || cell === 'rl_window_mem' ? 3 : 2;
    const rateLimitWindow = cell === 'rl_window' || cell === 'rl_window_mem' || cell === 'rl_time' ? parseVal(winRaw ?? rlRaw) : 60;
    const N = Number(nRaw || (cell === 'rl_value' ? 105 : 6));
    // rl_window_mem: KS-617 not-connected path (G.__noConnect above)
    if (cell === 'rl_degrade') G.__fail.incr = VALUES[valName] ?? VALUES.ordinary;
    if (cell === 'rl_fallback') {
      G.__fail.incr = VALUES.ordinary;
      const ow = winston.logger.warn.bind(winston.logger);
      winston.logger.warn = (m: string, ...a: unknown[]) => { if (/degrad|Degrad|in-memory|rateLimit/.test(String(m))) throw (valName === 'secretString' ? 'logger ' + PLANT : new Error('logger broke ' + PLANT)); return ow(m, ...a); };
    }
    app.use((req: any, res: any, next: any) => {
      req.user = { userId: 'connector:c1', authMethod: 'api_key', tenantId: 't1', connectorId: 'c1', rateLimit, rateLimitWindow };
      if (cell === 'rl_hdr' && valName !== 'none') { const o = res.setHeader.bind(res); res.setHeader = (n: string, v: unknown) => { if (n === 'X-RateLimit-Limit') throw VALUES[valName](); return o(n, v); }; }
      if (cell === 'rl_429write') { const o = res.setHeader.bind(res); res.setHeader = (n: string, v: unknown) => { if (n === 'Retry-After') throw new Error('retry ' + PLANT); return o(n, v); }; }
      if (cell === 'rl_committed') res.status(202).end('early');
      limiter(req, res, next).catch(next); // = auth.ts continueThroughLimiter
    });
    app.use((req: any, res: any) => { reached++; if (!res.headersSent) res.status(200).json({ ok: true }); });
    app.use((err: any, _req: any, res: any, _n: any) => { if (!res.headersSent) res.status(500).json({ err: 'errorHandler' }); });
    const { base, srv } = await listen(app);
    const seq: any[] = [];
    for (let i = 0; i < N; i++) seq.push(await hit(base, '/api/things'));
    if (cell === 'rl_time') { // second burst after waitRaw seconds: is the count reset?
      const firstAllowed = reached; await new Promise((z) => setTimeout(z, Number(waitRaw) * 1000));
      for (let i = 0; i < N; i++) seq.push(await hit(base, '/api/things'));
      r.allowedFirstBurst = firstAllowed; r.allowedSecondBurst = reached - firstAllowed; r.waitS = Number(waitRaw);
    }
    r.statuses = seq.map((s) => s.status).join(',');
    r.allowed = reached; r.N = N;
    const firstRefused = seq.find((s) => s.status === 429);
    r.firstRefused = firstRefused ? firstRefused.body : null;
    r.hint = firstRefused ? (/per (\S+)s/.exec(firstRefused.body) || [])[1] ?? null : null;
    r.limitHdr = seq[0]?.limit ?? null;
    r.bodies = [...new Set(seq.map((s) => s.status + ' ' + s.body.slice(0, 120)))].slice(0, 4);
    r.redisCounter = G.__store.get('ratelimit:jwt:t1:c1') ?? null;
    r.pexpireCalls = G.__calls.filter((c: string) => c === 'pexpire').length;
    srv.closeAllConnections(); srv.close();
  }
  done(r);
})().catch((e) => { realErr('probe error ' + short(e) + '\n'); process.exit(2); });
void origWarn;
