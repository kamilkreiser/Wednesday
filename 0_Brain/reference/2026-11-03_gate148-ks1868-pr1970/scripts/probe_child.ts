// QA gate 148 probe. usage: tsx probe_child.ts <base|head> <cell> <value> [env]
// Real security.ts / rateLimitEnforce.ts / audit.ts / services/redis.ts / utils/logger (winston) / middleware/errorHandler and the
// real @secuura/shared unhandledRejection handler (mode survive, as compose + bicep set it; shutdown RECORDED, not executed).
// Replaced: 'ioredis' (EventEmitter stand-in over one Map; a command can reject with the cell's value) and the audit DB query.
// The limiter is mounted behind a stand-in for authenticateToken that sets req.user and calls it exactly as
// auth.ts continueThroughLimiter does: clientRateLimit(req, res, next).catch(next).
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970';
process.chdir(W + '/logs/child_cwd'); // production logger File transports write logs/*.log relative to cwd (G144-F7)
const Module = require('module');
const EventEmitter = require('events');
const [variant, cell, valName, envName] = process.argv.slice(2);
process.env.NODE_ENV = envName === 'production' ? 'production' : 'test';
process.env.LOG_LEVEL = 'debug';
const SRC = W + '/repo/Blockchain/Dev/services/api-gateway/src/';
const outLines: string[] = [];
const realWrite = process.stdout.write.bind(process.stdout);
(process.stdout as any).write = (chunk: any) => { outLines.push(String(chunk)); return true; };
const realErr = process.stderr.write.bind(process.stderr);
(process.stderr as any).write = (chunk: any) => { outLines.push('STDERR:' + String(chunk)); return true; };
setTimeout(() => { realErr('WATCHDOG ' + cell + ' ' + valName + ': ' + outLines.slice(-10).join('') + '\n'); process.exit(3); }, 25000).unref();
const G: any = globalThis;
G.__store = new Map<string, string>();
G.__fail = {} as Record<string, () => unknown>; // command -> value factory to reject with
class FakeRedis extends EventEmitter {
  status = 'wait';
  constructor() { super(); G.__client = this; }
  private gate(cmd: string) { const f = G.__fail[cmd]; return f ? Promise.reject(f()) : null; }
  async connect() { this.status = 'ready'; this.emit('connect'); }
  async get(k: string) { G.__lastGetKey = k; return this.gate('get') ?? (G.__store.has(k) ? G.__store.get(k) : null); }
  async setex(k: string, _t: number, v: string) { return this.gate('setex') ?? (G.__store.set(k, v), 'OK'); }
  async del(k: string) { return this.gate('del') ?? (G.__store.delete(k) ? 1 : 0); }
  async incr(k: string) { const g = this.gate('incr'); if (g) return g; const n = Number(G.__store.get(k) || 0) + 1; G.__store.set(k, String(n)); return n; }
  async pexpire() { return this.gate('pexpire') ?? 1; }
  async pttl() { return this.gate('pttl') ?? 60000; }
  async quit() { return 'OK'; }
  async ping() { return 'PONG'; }
}
const origLoad = Module._load;
Module._load = function (req: string, ...rest: unknown[]) {
  if (req === 'ioredis') return { __esModule: true, default: FakeRedis };
  return origLoad.call(this, req, ...rest);
};
const BASE_SWAP: Record<string, string> = {};
for (const f of ['security', 'rateLimitEnforce', 'audit']) BASE_SWAP[SRC + 'middleware/' + f + '.ts'] = SRC + 'middleware/' + f + '.gate_base.ts';
const origResolve = Module._resolveFilename;
Module._resolveFilename = function (req: string, ...rest: unknown[]) {
  const r = origResolve.call(this, req, ...rest);
  if (variant === 'base' && BASE_SWAP[r]) return BASE_SWAP[r];
  return r;
};
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('boom'),
  revokedProxy: revoked,
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  msgNullProto: () => withMsg(Object.create(null)),
  msgSymbol: () => withMsg(Symbol('s')),
  plainString: () => 'plain',
  none: () => undefined,
};
const short = (e: unknown) => { try { return e instanceof Error ? e.constructor.name + ':' + e.message : typeof e; } catch { return 'unprintable'; } };
let uncaught: string | null = null;
const unhandled: string[] = [];
const shutdowns: string[] = [];
process.on('uncaughtException', (e) => { uncaught = short(e); if (process.env.G148_DEBUG) require('fs').writeSync(2, 'UNCAUGHT ' + (e as any)?.stack + '\n'); });
process.on('exit', () => { if (!(G as any).__done) require('fs').writeSync(1, JSON.stringify({ variant, cell, val: valName, harnessError: 'exited before done', uncaught }) + '\n'); });
const svcRequire = Module.createRequire(SRC + 'index.ts');
const express = svcRequire('express');
const shared = svcRequire('@secuura/shared');
const { logger: winstonLogger } = require(SRC + 'utils/logger');
const rejHandler = shared.createUnhandledRejectionHandler({ serviceName: 'api-gateway', mode: 'survive', logger: (m: string) => winstonLogger.log('error', m), shutdown: (s: string) => shutdowns.push(s) });
process.on('unhandledRejection', (r: unknown, p: Promise<unknown>) => { unhandled.push(short(r)); rejHandler(r, p); });
const { errorHandler } = require(SRC + 'middleware/errorHandler');
const redisSvc = require(SRC + 'services/redis');
const { createBruteForceProtection } = require(SRC + 'middleware/security');
const { enforceClientRateLimit } = require(SRC + 'middleware/rateLimitEnforce');
const { createAuditMiddleware } = require(SRC + 'middleware/audit');
const CONFIG = { bruteForce: { freeRetries: 2, minWait: 1000, maxWait: 60000, lifetime: 900000 }, suspiciousPatterns: [] };
const V = VALUES[valName];
async function hit(base: string, path: string, headers: Record<string, string> = {}) {
  try {
    const r = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: '{"email":"a@b.c","password":"x"}', signal: AbortSignal.timeout(1500) });
    const t = await r.text();
    return { status: r.status, rl: r.headers.get('x-ratelimit-remaining'), body: t.slice(0, 120) };
  } catch (e) { return { status: 0, rl: null, body: 'NO ANSWER (' + short(e) + ')' }; }
}
function listen(app: any): Promise<{ base: string; srv: any }> {
  return new Promise((res) => { const srv = app.listen(0, '127.0.0.1', () => res({ base: 'http://127.0.0.1:' + srv.address().port, srv })); });
}
function done(o: Record<string, unknown>) {
  G.__done = true;
  setTimeout(() => {
    const logs = outLines.join('').split('\n').filter((l) => /BruteForce|rateLimit|audit|UNHANDLED|Unhandled|STDERR|BRUTE/.test(l)).map((l) => l.replace(/\x1b\[[0-9;]*m/g, '').replace(/^\d{4}-\d\d-\d\d \S+ /, '').slice(0, 400));
    require("fs").writeSync(1, JSON.stringify({ variant, cell, val: valName, env: process.env.NODE_ENV, ...o, uncaught, unhandled, shutdowns, logs }) + '\n');
    process.exit(0);
  }, 400);
}
(async () => {
  const mark = (s: string) => { if (process.env.G148_DEBUG) require('fs').writeSync(2, 'MARK ' + s + '\n'); };
  mark('init'); await redisSvc.initRedis(); mark('inited');
  const app = express();
  app.use(express.json());
  const result: Record<string, unknown> = { redisAvailable: redisSvc.isRedisAvailable() };
  if (cell === 'bf') {
    if (valName !== 'none') G.__fail.get = V;
    app.use(createBruteForceProtection(CONFIG));
    app.use((req: any, res: any) => res.status(200).json({ helper: Boolean(req.bruteForce) }));
    app.use(errorHandler);
    const { base, srv } = await listen(app);
    result.login = await hit(base, '/api/auth/login');
    srv.closeAllConnections(); srv.close();
  } else if (cell === 'bf_arm') {
    // Does the guard ever arm? Downstream answers 401 like a failed login proxied to auth; nothing in the gateway calls recordFailure.
    app.use(createBruteForceProtection(CONFIG));
    app.use((req: any, res: any) => res.status(401).json({ helper: Boolean(req.bruteForce) }));
    const { base, srv } = await listen(app);
    const seq: number[] = [];
    for (let i = 0; i < 12; i++) seq.push((await hit(base, '/api/auth/login')).status);
    result.twelveFailedLogins = seq;
    result.bfKeysAfter = [...G.__store.keys()].filter((k: string) => k.includes('bf:'));
    // Planted lockout (what recordFailure WOULD write): the guard enforces it, then the same lockout under a Redis fault.
    const k = [...G.__store.keys()][0];
    const key = G.__lastGetKey;
    G.__store.set(key, JSON.stringify({ attempts: 9, blockedUntil: Date.now() + 600000 }));
    result.plantedKey = key; result.plantedLockout = (await hit(base, '/api/auth/login')).status;
    G.__fail.get = VALUES.ordinary; result.plantedLockoutRedisOrdinaryError = (await hit(base, '/api/auth/login')).status;
    G.__fail.get = VALUES.revokedProxy; result.plantedLockoutRedisRevokedProxy = (await hit(base, '/api/auth/login')).status;
    void k;
    srv.closeAllConnections(); srv.close();
  } else if (cell === 'rl_redis' || cell === 'rl_hdr' || cell === 'rl_hdr_committed' || cell === 'rl_hdr_badmeta') {
    const limiter = enforceClientRateLimit();
    if (cell === 'rl_redis' && valName !== 'none') G.__fail.incr = V;
    app.use((req: any, res: any, next: any) => {
      req.user = { userId: 'connector:c1', authMethod: 'api_key', tenantId: 't1', connectorId: 'c1', rateLimit: cell === 'rl_hdr_badmeta' ? '1\n' : 1, rateLimitWindow: 60 };
      if (cell === 'rl_hdr' && valName !== 'none') {
        const orig = res.setHeader.bind(res);
        res.setHeader = (n: string, v: unknown) => { if (n === 'X-RateLimit-Limit') throw V(); return orig(n, v); };
      }
      if (cell === 'rl_hdr_committed') { res.status(202).end('early'); } // a response already committed before the limiter runs
      limiter(req, res, next).catch(next); // = auth.ts continueThroughLimiter
    });
    let reached = 0;
    app.use((req: any, res: any) => { reached++; if (!res.headersSent) res.status(200).json({ ok: true }); });
    app.use(errorHandler);
    const { base, srv } = await listen(app);
    const seq: unknown[] = [];
    for (let i = 0; i < 3; i++) seq.push(await hit(base, '/api/things'));
    result.three = seq; result.handlerReached = reached;
    result.redisCounter = G.__store.get('ratelimit:jwt:t1:c1') ?? null;
    srv.closeAllConnections(); srv.close();
  } else if (cell === 'audit') {
    let calls = 0;
    const log = (level: string, message: string, meta?: object) => winstonLogger.log(level, message, meta);
    app.use(createAuditMiddleware({ query: async () => { calls++; if (valName !== 'none') throw V(); return { rows: [] }; }, isDbAvailable: () => true, log }));
    app.use((req: any, res: any) => res.status(200).json({ ok: true }));
    app.use(errorHandler);
    const { base, srv } = await listen(app);
    result.post = await hit(base, '/api/things');
    await new Promise((r) => setTimeout(r, 200));
    result.post2 = await hit(base, '/api/things'); // gateway still serving after the rejection
    result.queryCalls = calls;
    srv.closeAllConnections(); srv.close();
  }
  done(result);
})().catch((e) => { realErr('probe error ' + short(e) + '\n'); process.exit(2); });
