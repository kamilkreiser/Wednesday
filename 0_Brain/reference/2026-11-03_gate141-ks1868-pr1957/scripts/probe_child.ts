// usage: tsx probe_child.ts <svc> <variant base|head> <site pool|hook_boot|hook_retry> <case>
import * as fs from 'fs';
const Module = require('module');
const EventEmitter = require('events');
const [svc, variant, site, kase] = process.argv.slice(2);
const D = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957/repo/Blockchain/Dev/services/' + svc + '/src/';
const out: string[] = [];
const realLog = console.log;
console.log = (...a: unknown[]) => { if (typeof a[0] === 'string') out.push(a[0]); };
const ev: string[] = [];
let probeCalls = 0;
class FakePool extends EventEmitter {
  constructor(_o: unknown) { super(); (globalThis as any).__pool = this; }
  async query() {
    probeCalls++;
    if (site === 'hook_retry' && probeCalls === 1) throw new Error('db down at boot');
    return { rows: [{ ok: 1 }] };
  }
  async end() {}
  async connect() { return { query: async () => ({ rows: [{ ok: 1 }] }), release() {} }; }
}
const origLoad = Module._load;
Module._load = function (req: string, ...rest: unknown[]) {
  if (req === 'pg') return { Pool: FakePool };
  return origLoad.call(this, req, ...rest);
};
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('boom'),
  revokedProxy: revoked,
  getterThrows: () => withMsg(null) && Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  msg42: () => withMsg(42),
  msgUndefined: () => ({ nothing: 1 }),
  msgNull: () => withMsg(null),
  msgSymbol: () => withMsg(Symbol('s')),
  msgObjToStringThrows: () => withMsg({ toString() { throw new Error('ts'); } }),
  msgObjToString: () => withMsg({ toString() { return 'custom-string'; } }),
  nullValue: () => null,
  undefinedValue: () => undefined,
  plainString: () => 'plain',
};
let uncaught: string | null = null;
let unhandled: string | null = null;
process.on('uncaughtException', (e) => { uncaught = 'uncaughtException:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e); });
process.on('unhandledRejection', (e) => { unhandled = 'unhandledRejection:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e); });
(async () => {
  process.env.DATABASE_URL = 'postgresql://t:t@127.0.0.1:1/t';
  const db = require(D + (variant === 'base' ? 'db_base' : 'db'));
  const v = VALUES[kase]();
  let res: unknown = 'n/a', flag: unknown = 'n/a';
  if (site === 'pool') {
    db.getPool();
    setImmediate(() => { (globalThis as any).__pool.emit('error', v); });
    await new Promise((r) => setTimeout(r, 50));
  } else if (site === 'hook_boot') {
    try { res = await db.initDb(async () => { throw v; }); flag = 'resolved'; } catch (e) { flag = 'REJECTED:' + (e instanceof Error ? e.constructor.name : typeof e); }
    await new Promise((r) => setTimeout(r, 50));
  } else {
    res = await db.initDb(async () => { throw v; }); // first probe fails -> retry timer
    await new Promise((r) => setTimeout(r, 1600));
  }
  const lines = out.map((l) => { try { const o = JSON.parse(l); return { message: o.message, error: o.error, errType: typeof o.error, level: o.level, hasErrorKey: 'error' in o }; } catch { return { raw: l.slice(0, 80) }; } })
    .filter((o: any) => /unexpected error|boot work failed|unavailable/.test(o.message || ''));
  const dbAvail = db.isDbAvailable ? db.isDbAvailable() : 'n/a';
  realLog(JSON.stringify({ svc, variant, site, kase, initDb: res, initDbFlag: flag, isDbAvailable: dbAvail, uncaught, unhandled, lines }));
  process.exit(0);
})();
