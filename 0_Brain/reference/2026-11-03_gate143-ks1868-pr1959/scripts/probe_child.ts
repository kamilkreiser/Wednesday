// usage: tsx probe_child.ts <variant base|head> <site ctor|listener> <case>   (env NODE_ENV decides format/level; real logger)
const Module = require('module');
const EventEmitter = require('events');
const [variant, site, kase] = process.argv.slice(2);
const SRC = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959/repo/Blockchain/Dev/services/auth/src/';
const out: string[] = [];
const origWrite = process.stdout.write.bind(process.stdout);
(process.stdout as any).write = (c: any) => { out.push(String(c)); return true; };
let xadds = 0;
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('boom'),
  revokedProxy: revoked,
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  msg42: () => withMsg(42),
  msgUndefined: () => ({ nothing: 1 }),
  msgNull: () => withMsg(null),
  msgSymbol: () => withMsg(Symbol('s')),
  msgObjToStringThrows: () => withMsg({ toString() { throw new Error('ts'); } }),
  msgObjToString: () => withMsg({ toString() { return 'custom-string'; } }),
  nullValue: () => null,
  undefinedValue: () => undefined,
  plainString: () => 'plain',
  num42: () => 42,
  symbolValue: () => Symbol('sv'),
};
let value: unknown;
class FakeRedis extends EventEmitter {
  status = 'wait';
  constructor(_u: unknown, _o: unknown) { super(); if (site === 'ctor') throw value; (globalThis as any).__r = this; }
  async connect() {}
  disconnect() {}
  async xadd() { xadds++; return '1-0'; }
}
const origLoad = Module._load;
Module._load = function (req: string, ...rest: unknown[]) {
  if (req === 'ioredis') return { __esModule: true, default: FakeRedis };
  return origLoad.call(this, req, ...rest);
};
let uncaught: string | null = null;
process.on('uncaughtException', (e) => { uncaught = 'uncaughtException:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e); });
(async () => {
  value = VALUES[kase]();
  const ev = require(SRC + (variant === 'base' ? 'events_base' : 'events'));
  let res: unknown = 'n/a', threw: string | null = null, boot = 'n/a';
  if (site === 'ctor') {
    // replica of src/index.ts:256 (bare call, return ignored) inside an async start() awaited with .catch -> exit(1)
    const start = async () => { res = ev.initEventBus('redis://x:6379'); };
    try { await start(); boot = 'boot continues'; } catch (e) { threw = 'THREW:' + (e instanceof Error ? e.constructor.name : typeof e); boot = 'start() rejects -> logger.error + process.exit(1)'; }
  } else {
    res = ev.initEventBus('redis://x:6379');
    setImmediate(() => { (globalThis as any).__r.emit('error', value); });
    await new Promise((r) => setTimeout(r, 60));
  }
  await ev.publishEvent('user.login', {}).catch(() => {});
  await new Promise((r) => setTimeout(r, 20));
  const lines = out.join('').split('\n').filter(Boolean).map((l) => {
    try { const o = JSON.parse(l); return { level: o.level, message: o.message, error: o.error, errType: typeof o.error, hasErrorKey: 'error' in o }; }
    catch { return { raw: l.replace(/\u001b\[[0-9;]*m/g, '').slice(0, 160) }; }
  }).filter((o: any) => /Redis error|Failed to initialise|EventBus initialised|raw/.test(JSON.stringify(o)) );
  origWrite(JSON.stringify({ variant, site, kase, nodeEnv: process.env.NODE_ENV || 'dev', returned: res, threw, boot, uncaught, publishXadds: xadds, lines }) + '\n');
  process.exit(0);
})();
