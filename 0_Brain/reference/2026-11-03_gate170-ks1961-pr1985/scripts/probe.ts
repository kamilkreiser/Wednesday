// QA gate 170 probe (adapted from gate 168's scripts/probe.ts, read not edited there).
// usage: node --require <tsx cjs> probe.ts <dev|r1|head> <cell> <val>
// Real security.ts / rateLimitEnforce.ts / services/redis.ts / utils/logger (winston), express over real HTTP.
// Replaced: 'ioredis' by gate 168's Map-backed stand-in (PEXPIRE <=0 deletes; non-integer PEXPIRE rejects with Redis's text).
// dev = develop ca2b2aa's two middleware files, r1 = round-1 head 1e8c43fc's, both resolved in place of head's
// (same directory, so their relative imports are the real ones). head = the checked-out a0a91f65 files.
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985';
process.chdir(W + '/logs/child_cwd');
const Module = require('module');
const EventEmitter = require('events');
const fs = require('fs');
const [variant, cell, valName] = process.argv.slice(2);
process.env.NODE_ENV = 'test';
process.env.LOG_LEVEL = 'debug';
const PLANT = 'G170PLANT-' + 'w3rT8b'; // planted "secret" text
const SRC = W + '/repo/Blockchain/Dev/services/api-gateway/src/';
const outLines: string[] = [];
const realErr = process.stderr.write.bind(process.stderr);
(process.stdout as any).write = (c: any) => { outLines.push(String(c)); return true; };
(process.stderr as any).write = (c: any) => { outLines.push('STDERR:' + String(c)); return true; };
console.warn = (...a: unknown[]) => { outLines.push('CONSOLE.WARN:' + a.map(String).join(' ') + '\n'); };
console.error = (...a: unknown[]) => { outLines.push('CONSOLE.ERROR:' + a.map(String).join(' ') + '\n'); };
setTimeout(() => { realErr('WATCHDOG ' + cell + ' ' + valName + '\n'); process.exit(3); }, 150000).unref();
const G: any = globalThis;
G.__store = new Map<string, string>(); G.__exp = new Map<string, number>();
G.__fail = {} as Record<string, () => unknown>; G.__calls = [] as string[];
const live = (k: string) => { const e = G.__exp.get(k); if (e !== undefined && Date.now() >= e) { G.__store.delete(k); G.__exp.delete(k); } return G.__store.has(k); };
class FakeRedis extends EventEmitter {
  status = 'wait';
  constructor() { super(); G.__client = this; }
  private gate(cmd: string, arg?: unknown) { G.__calls.push(arg === undefined ? cmd : cmd + '(' + String(arg) + ')'); const f = G.__fail[cmd]; if (f === undefined) return null; const v = f(); return v === '__HANG__' ? new Promise(() => {}) : Promise.reject(v); }
  async connect() { if (G.__noConnect) throw new Error('ECONNREFUSED'); this.status = 'ready'; this.emit('connect'); this.emit('ready'); }
  async get(k: string) { G.__lastGetKey = k; return this.gate('get') ?? (live(k) ? G.__store.get(k) : null); }
  async setex(k: string, _t: number, v: string) { return this.gate('setex') ?? (G.__store.set(k, v), 'OK'); }
  async set(k: string, v: string) { return this.gate('set') ?? (G.__store.set(k, v), 'OK'); }
  async del(k: string) { return this.gate('del') ?? (G.__store.delete(k) ? 1 : 0); }
  async incr(k: string) { const g = this.gate('incr'); if (g) return g; const n = Number(live(k) ? G.__store.get(k) : 0) + 1; G.__store.set(k, String(n)); return n; }
  async pexpire(k: string, ms: unknown) {
    const g = this.gate('pexpire', ms); if (g) return g;
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
const SUFFIX: Record<string, string> = { dev: '.g170dev.ts', r1: '.g170r1.ts' };
const SWAP: Record<string, string> = {};
if (SUFFIX[variant]) for (const f of ['security', 'rateLimitEnforce']) SWAP[SRC + 'middleware/' + f + '.ts'] = SRC + 'middleware/' + f + SUFFIX[variant];
if (variant !== 'head' && !SUFFIX[variant]) { realErr('bad variant\n'); process.exit(2); }
const origResolve = Module._resolveFilename;
Module._resolveFilename = function (req: string, ...rest: unknown[]) {
  const r = origResolve.call(this, req, ...rest);
  return SWAP[r] ?? r;
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
  const T: Record<string, unknown> = {
    NL1: '1\n', NaN: NaN, Infinity: Infinity, negInfinity: -Infinity, obj: {}, true: true, false: false, arr5: [5], arr: [],
    str100: '100', str500: '500', str5: '5', str99: '99', str1e3: '1e3', str120: '120', str30: '30', str0: '0', strSp5: ' 5', strHex: '0x10', strAbc: 'abc', strSpace: ' ',
    empty: '', missing: undefined, null: null, pow53: 2 ** 53, '1e300': 1e300, negZero: -0, big5: BigInt(5), big0: BigInt(0),
    numObj5: new Number(5), valueOf5: { valueOf: () => 5 }, date: new Date(0),
  };
  return s in T ? T[s] : Number(s);
}
function done(o: Record<string, unknown>) {
  setTimeout(() => {
    const text = outLines.join('');
    const logs = text.split('\n').filter((l) => /BruteForce|BRUTE|rateLimit|STDERR|CONSOLE/.test(l)).map((l) => l.replace(/\x1b\[[0-9;]*m/g, '').replace(/^\d{4}-\d\d-\d\d \S+ /, '').slice(0, 400));
    fs.writeSync(1, JSON.stringify({ variant, cell, val: valName, ...o, unhandled, plantInLogs: text.split(PLANT).length - 1, logs }) + '\n');
    process.exit(0);
  }, 300);
}
(async () => {
  if (cell === 'rl_notconnected' || cell === 'rl_window_mem' || cell === 'rl_value_mem') G.__noConnect = true;
  try { await redisSvc.initRedis(); } catch { /* KS-617: not connected */ }
  const app = express();
  app.use(express.json());
  const r: Record<string, unknown> = { redisAvailable: redisSvc.isRedisAvailable() };
  let reached = 0;
  if (cell.startsWith('bf')) {
    const guard = createBruteForceProtection(CONFIG);
    let armed = false;
    app.use((req: any, res: any, next: any) => {
      if (armed && cell === 'bf_429throw') {
        const o = res.setHeader.bind(res);
        if (valName === 'hdrError') res.setHeader = (n: string, v: unknown) => { if (n === 'Retry-After') throw new Error('hdr ' + PLANT); return o(n, v); };
        if (valName === 'hdrString') res.setHeader = (n: string, v: unknown) => { if (n === 'Retry-After') throw 'hdr ' + PLANT; return o(n, v); };
        if (valName === 'hdrObject') res.setHeader = (n: string, v: unknown) => { if (n === 'Retry-After') throw { password: PLANT }; return o(n, v); };
        if (valName === 'hdrRevoked') res.setHeader = (n: string, v: unknown) => { if (n === 'Retry-After') throw revoked(); return o(n, v); };
        if (valName === 'jsonThrows') { const oj = res.json.bind(res); res.json = (b: any) => { if (b && b.retryAfter !== undefined) throw new Error('json ' + PLANT); return oj(b); }; }
        if (valName === 'statusThrows') res.status = () => { throw new Error('status ' + PLANT); };
        if (valName === 'committed') { res.status(202); res.write('early'); }
        if (valName === 'logThrows') { const ow = winston.logger.warn.bind(winston.logger); winston.logger.warn = (m: string, ...a: unknown[]) => { if (String(m) === 'BRUTE_FORCE_BLOCKED') throw new Error('logger ' + PLANT); return ow(m, ...a); }; }
        if (valName === 'logThrowsAll') { winston.logger.warn = () => { throw new Error('warn ' + PLANT); }; winston.logger.error = () => { throw new Error('error ' + PLANT); }; }
      }
      guard(req, res, next);
    });
    app.use((req: any, res: any) => { reached++; if (!res.headersSent) res.status(401).json({ downstream: true }); else res.end(); });
    const { base, srv } = await listen(app);
    await hit(base, '/api/auth/login'); // prime: learn the real key the guard reads (no fault)
    const key = G.__lastGetKey; r.key = key; reached = 0;
    if (cell === 'bf_429throw' || cell === 'bf_lockout') {
      G.__store.set(key, JSON.stringify({ attempts: 9, blockedUntil: Date.now() + 600000 }));
      if (cell === 'bf_lockout' && valName !== 'none') G.__fail.get = VALUES[valName];
    }
    if (cell === 'bf_fault' && valName !== 'none') G.__fail.get = VALUES[valName];
    armed = true;
    r.resp = await hit(base, '/api/auth/login');
    r.downstream = reached;
    srv.closeAllConnections(); srv.close();
  } else {
    const limiter = enforceClientRateLimit();
    const [rlRaw, winRaw, nRaw, waitRaw] = (valName || '').split('~');
    // rl_value / rl_value_mem / rl_time / rl_window*: "<rateLimit>~<window>~<N>[~<waitS>]"
    // rl_mixed: "<cleanRateLimit>~<malformedRateLimit>~<N>": alternate requests in ONE bucket, clean then malformed
    const rateLimit = parseVal(rlRaw);
    const rateLimitWindow = cell === 'rl_mixed' ? 60 : parseVal(winRaw);
    const mixedVal = cell === 'rl_mixed' ? parseVal(winRaw) : undefined;
    const N = Number(nRaw);
    if (cell === 'rl_degrade') G.__fail.incr = VALUES[waitRaw] ?? VALUES.ordinary;
    const perKind = { clean: 0, mal: 0 } as Record<string, number>;
    let i = 0;
    app.use((req: any, res: any, next: any) => {
      const mal = cell === 'rl_mixed' && (i++ % 2 === 1);
      req.__kind = mal ? 'mal' : 'clean';
      req.user = { userId: 'connector:c1', authMethod: 'api_key', tenantId: 't1', connectorId: 'c1', rateLimit: mal ? mixedVal : rateLimit, rateLimitWindow };
      limiter(req, res, next).catch(next); // = auth.ts continueThroughLimiter
    });
    app.use((req: any, res: any) => { reached++; perKind[req.__kind]++; if (!res.headersSent) res.status(200).json({ ok: true }); });
    app.use((err: any, _req: any, res: any, _n: any) => { if (!res.headersSent) res.status(500).json({ err: 'errorHandler' }); });
    const { base, srv } = await listen(app);
    const seq: any[] = [];
    for (let k = 0; k < N; k++) seq.push(await hit(base, '/api/things'));
    if (cell === 'rl_time') {
      const firstAllowed = reached; await new Promise((z) => setTimeout(z, Number(waitRaw) * 1000));
      for (let k = 0; k < N; k++) seq.push(await hit(base, '/api/things'));
      r.allowedFirstBurst = firstAllowed; r.allowedSecondBurst = reached - firstAllowed; r.waitS = Number(waitRaw);
    }
    r.statuses = seq.map((s) => s.status).join(',');
    r.allowed = reached; r.N = seq.length; r.perKind = perKind;
    const firstRefused = seq.find((s) => s.status === 429);
    r.hint = firstRefused ? (/per (\S+)s/.exec(firstRefused.body) || [])[1] ?? null : null;
    r.limitHdr = seq[0]?.limit ?? null;
    r.bodies = [...new Set(seq.map((s) => s.status + ' ' + s.body.slice(0, 160)))].slice(0, 5);
    r.redisCounter = G.__store.get('ratelimit:jwt:t1:c1') ?? null;
    r.calls = G.__calls.join(' ');
    srv.closeAllConnections(); srv.close();
  }
  done(r);
})().catch((e) => { realErr('probe error ' + short(e) + '\n'); process.exit(2); });
