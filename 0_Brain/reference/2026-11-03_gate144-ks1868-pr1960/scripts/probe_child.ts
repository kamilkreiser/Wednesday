// QA gate 144 probe. usage:
//   tsx probe_child.ts site <base|head> <listener|connect_dev|connect_prod> <case>
//   tsx probe_child.ts family <base|head> <trigger: ordinary|revokedProxy|getterThrows|none> <redisDown 0|1>
// Real redis.ts / security.ts / rateLimitEnforce.ts / utils/logger (winston); only 'ioredis' is replaced by an
// EventEmitter stand-in whose commands hit ONE shared Map (= one shared Redis across replicas) or reject when "down".
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960';
process.chdir(W + '/logs/child_cwd'); // production logger writes logs/*.log relative to cwd: keep it in the workdir
const Module = require('module');
const EventEmitter = require('events');
const path = require('path');
const [mode, variant, a3, a4] = process.argv.slice(2);
const SRC = W + '/repo/Blockchain/Dev/services/api-gateway/src/';
const outLines: string[] = [];
const realWrite = process.stdout.write.bind(process.stdout);
(process.stdout as any).write = (chunk: any, ...rest: any[]) => { outLines.push(String(chunk)); return true; };
const realErr = process.stderr.write.bind(process.stderr);
(process.stderr as any).write = (chunk: any) => { outLines.push('STDERR:' + String(chunk)); return true; };
setTimeout(() => { realErr('WATCHDOG fired; captured tail: ' + outLines.slice(-20).join('') + '\n'); process.exit(3); }, 20000).unref();
const G: any = globalThis;
G.__store = new Map<string, string>();
G.__down = false;
G.__failConnect = undefined as undefined | { v: unknown };
class FakeRedis extends EventEmitter {
  status = 'wait';
  constructor(_u: unknown, _o: unknown) { super(); (G.__clients ||= []).push(this); }
  private gate() { if (G.__down) return Promise.reject(new Error('Connection is closed.')); return null; }
  async connect() { if (G.__failConnect) throw G.__failConnect.v; this.status = 'ready'; this.emit('connect'); }
  async ping() { return this.gate() ?? 'PONG'; }
  async get(k: string) { return this.gate() ?? (G.__store.has(k) ? G.__store.get(k) : null); }
  async setex(k: string, _t: number, v: string) { return this.gate() ?? (G.__store.set(k, v), 'OK'); }
  async set(k: string, v: string) { return this.gate() ?? (G.__store.set(k, v), 'OK'); }
  async del(k: string) { return this.gate() ?? (G.__store.delete(k) ? 1 : 0); }
  async incr(k: string) { const g = this.gate(); if (g) return g; const n = Number(G.__store.get(k) || 0) + 1; G.__store.set(k, String(n)); return n; }
  async pexpire() { return this.gate() ?? 1; }
  async pttl() { return this.gate() ?? 60000; }
  async quit() { return 'OK'; }
  async keys(pat: string) { const g = this.gate(); if (g) return g; const pre = pat.replace(/\*$/, ''); return [...G.__store.keys()].filter((k: string) => k.startsWith(pre)); }
  pipeline() { const ks: string[] = []; const self = this; return { get(k: string) { ks.push(k); return this; }, async exec() { const g = self.gate(); if (g) return g; return ks.map((k) => [null, G.__store.has(k) ? G.__store.get(k) : null]); } }; }
}
const origLoad = Module._load;
Module._load = function (req: string, ...rest: unknown[]) {
  if (req === 'ioredis') return { __esModule: true, default: FakeRedis };
  return origLoad.call(this, req, ...rest);
};
const origResolve = Module._resolveFilename;
Module._resolveFilename = function (req: string, ...rest: unknown[]) {
  const r = origResolve.call(this, req, ...rest);
  if (variant === 'base' && r === SRC + 'services/redis.ts') return SRC + 'services/redis.gate_base.ts';
  return r;
};
function freshReplica() {
  for (const k of Object.keys(require.cache)) if (k.startsWith(SRC)) delete require.cache[k];
  const before = (G.__clients || []).length;
  const redis = require(SRC + 'services/redis');
  const sec = require(SRC + 'middleware/security');
  const rle = require(SRC + 'middleware/rateLimitEnforce');
  return { redis, sec, rle, clientIndex: before };
}
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('boom'),
  revokedProxy: revoked,
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  msg42: () => withMsg(42),
  msgNull: () => withMsg(null),
  msgUndefinedObj: () => ({ nothing: 1 }),
  msgSymbol: () => withMsg(Symbol('s')),
  msgObjToStringThrows: () => withMsg({ toString() { throw new Error('ts'); } }),
  nullValue: () => null,
  undefinedValue: () => undefined,
  plainString: () => 'plain',
};
const short = (e: unknown) => { try { return e instanceof Error ? e.constructor.name + ':' + e.message : typeof e; } catch { return 'unprintable'; } };
let uncaught: string | null = null, unhandled: string | null = null;
process.on('uncaughtException', (e) => { uncaught = short(e); });
process.on('unhandledRejection', (e) => { unhandled = short(e); });
function done(o: Record<string, unknown>) {
  try {
  const logs = outLines.join('').split('\n').filter((l) => /Redis|BruteForce|BRUTE|rate|STDERR/i.test(l)).map((l) => l.replace(/\x1b\[[0-9;]*m/g, '').replace(/^(?!\{)\S+ /, ''));
  realWrite(JSON.stringify({ mode, variant, a3, a4, ...o, uncaught, unhandled, logs }) + '\n');
  } catch (e) { realErr('done failed: ' + short(e) + '\n'); }
  process.exit(0);
}
(async () => {
  if (mode === 'site') {
    const site = a3, kase = a4;
    process.env.NODE_ENV = site === 'connect_prod' ? 'production' : 'test';
    const v = VALUES[kase]();
    if (site.startsWith('connect')) G.__failConnect = { v };
    const r = freshReplica();
    let init: string;
    try { init = 'resolved:' + String(await r.redis.initRedis()); } catch (e) { init = 'REJECTED:' + short(e); }
    const flagBefore = r.redis.isRedisAvailable();
    let emitThrew: string | null = null;
    if (site === 'listener') {
      try { G.__clients[r.clientIndex].emit('error', v); } catch (e) { emitThrew = short(e); }
    }
    if (site === 'listener_async') {
      // as ioredis does: the emit runs from a socket event callback, so a listener throw has no caller to catch it
      setImmediate(() => { G.__clients[r.clientIndex].emit('error', v); });
    }
    await new Promise((res) => setTimeout(res, 30));
    return done({ init, flagBefore, emitThrew, flagAfter: r.redis.isRedisAvailable() });
  }
  if (mode === 'enforce') {
    // enforceDocumentTypeRules on replica A and B; doc type (requireMFA) registered while Redis is UP
    process.env.NODE_ENV = 'test';
    const trigger = a3, down = a4 === '1';
    const A = freshReplica(); await A.redis.initRedis();
    const Aenf = require(SRC + 'services/enforcement');
    const B = freshReplica(); await B.redis.initRedis();
    const Benf = require(SRC + 'services/enforcement');
    await A.redis.setDocumentType('dt-mfa', { id: 'dt-mfa', code: 'MFA_DOC', name: 'mfa doc', isActive: true, requireMFA: true, creatorVerificationLevel: 'none' });
    const emitThrew: Record<string, string | null> = {};
    if (trigger !== 'none') for (const [n, R] of [['A', A], ['B', B]] as const) {
      try { G.__clients[R.clientIndex].emit('error', VALUES[trigger]()); emitThrew[n] = null; } catch (e) { emitThrew[n] = short(e); }
    }
    if (down) { G.__down = true; for (const c of G.__clients) c.status = 'reconnecting'; }
    const user = { userId: 'u', email: 'e', role: 'user', verificationLevel: 'none', mfaEnabled: false };
    const run = async (enf: any) => { try { const r = await enf.enforceDocumentTypeRules({ documentType: 'MFA_DOC' }, user); return r.ok ? 'ALLOWED ok:true docType=' + JSON.stringify(r.docType) : 'REFUSED ' + r.status + ' ' + r.code; } catch (e) { return 'REJECT:' + short(e); } };
    return done({ emitThrew, flagA: A.redis.isRedisAvailable(), flagB: B.redis.isRedisAvailable(), A: await run(Aenf), B: await run(Benf) });
  }
  // family: two replicas sharing one Redis
  process.env.NODE_ENV = 'test';
  const trigger = a3, down = a4 === '1';
  const A = freshReplica(); await A.redis.initRedis();
  const B = freshReplica(); await B.redis.initRedis();
  const now = Date.now();
  // planted while Redis is UP (lands in the shared store)
  await A.redis.setBruteForceData('9.9.9.9', { attempts: 9, blockedUntil: now + 600000 });
  await A.redis.setRateLimitData('client-x', { count: 99, resetAt: now + 60000 });
  await A.redis.setDocumentSignature('doc-1', { address: '0xabc', signature: 'sig', signedAt: 't' });
  await A.redis.setRejectedDocument('doc-r', { status: 'rejected', rejectionReason: 'r', rejectedAt: 't', rejectedBy: 'u' });
  await A.redis.setNotificationSettings('platform-settings', { integrations: [{ id: 'conn-1', config: { allowedDocumentTypes: ['a'] } }] });
  const emitThrew: Record<string, string | null> = {};
  if (trigger !== 'none') {
    for (const [n, R] of [['A', A], ['B', B]] as const) {
      try { G.__clients[R.clientIndex].emit('error', VALUES[trigger]()); emitThrew[n] = null; } catch (e) { emitThrew[n] = short(e); }
    }
  }
  if (down) { G.__down = true; for (const c of G.__clients) c.status = 'reconnecting'; }
  const cfg = { bruteForce: { freeRetries: 3, minWait: 1000, maxWait: 60000, lifetime: 3600 }, suspiciousPatterns: [] };
  async function bf(R: any) {
    const mw = R.sec.createBruteForceProtection(cfg);
    const res: any = { code: 0, setHeader() {}, status(c: number) { this.code = c; return this; }, json() { return this; } };
    let next = false;
    const req: any = { path: '/api/auth/login', ip: '9.9.9.9', method: 'POST', get: () => 'ua', headers: {} };
    await mw(req, res, () => { next = true; });
    return res.code === 429 ? 'BLOCKED_429' : next ? 'ALLOWED_next' : 'none';
  }
  async function safe(f: () => Promise<unknown>) { try { return JSON.stringify(await f()); } catch (e) { return 'REJECT:' + short(e); } }
  async function machine(R: any) {
    const mw = R.rle.enforceClientRateLimit();
    const res: any = { code: 0, headers: {} as any, setHeader(k: string, v: unknown) { this.headers[k] = v; }, set(k: string, v: unknown) { this.headers[k] = v; }, status(c: number) { this.code = c; return this; }, json() { return this; } };
    let next = false;
    const req: any = { user: { authMethod: 'api_key', userId: 'm1', tenantId: 't1', rateLimit: 1, rateLimitWindow: 60 }, headers: {}, ip: '1.1.1.1', path: '/x', get: () => '' };
    await mw(req, res, () => { next = true; });
    return (res.code === 429 ? '429' : next ? 'next' : 'none') + ' remaining=' + String(res.headers['X-RateLimit-Remaining']);
  }
  const out: Record<string, unknown> = { emitThrew };
  for (const [n, R] of [['A', A], ['B', B]] as const) {
    out[n] = {
      flag: R.redis.isRedisAvailable(),
      bfData: await safe(() => R.redis.getBruteForceData('9.9.9.9')),
      bfMiddleware: await bf(R),
      rlData: await safe(() => R.redis.getRateLimitData('client-x')),
      sig: await safe(() => R.redis.getDocumentSignature('doc-1')),
      rejected: await safe(() => R.redis.getRejectedDocument('doc-r')),
      platformSettings: await safe(() => R.redis.getNotificationSettings('platform-settings')),
      health: await safe(() => R.redis.getRedisHealth()),
    };
  }
  // writes AFTER the trigger: a new lockout / counter recorded on A, read on B
  out.newLockoutA = await safe(() => A.redis.setBruteForceData('8.8.8.8', { attempts: 9, blockedUntil: now + 600000 }));
  out.newLockoutReadB = await safe(() => B.redis.getBruteForceData('8.8.8.8'));
  out.newRlA = await safe(() => A.redis.setRateLimitData('client-y', { count: 50, resetAt: now + 60000 }));
  out.newRlReadB = await safe(() => B.redis.getRateLimitData('client-y'));
  // machine limiter (rateLimit 1/window): two calls on A then one on B
  out.machine = [await machine(A), await machine(A), await machine(B)];
  done(out);
})().catch((e) => done({ harnessError: short(e) }));
