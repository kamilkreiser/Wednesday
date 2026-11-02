// usage: tsx probe_child.ts <site status|conf_recover|conf_always|conf_nocb> <variant base|head> <case>
import * as fs from 'fs';
const Module = require('module');
const [site, variant, kase] = process.argv.slice(2);
const SRC = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958/repo/Blockchain/Dev/services/anchoring/src/';
const out: string[] = [];
const realLog = console.log;
console.log = (...a: unknown[]) => { if (typeof a[0] === 'string') out.push(a[0]); };
// the REAL logger: extracted from index.ts source text and compiled
const idx = fs.readFileSync(SRC + 'index.ts', 'utf8');
const m = idx.match(/function log\(level[^)]*\)[^{]*\{([\s\S]*?)\n\}/);
if (!m) throw new Error('log fn not found');
const log: (l: string, msg: string, meta?: object) => void = new Function('level', 'message', 'meta', m[1])  as any;
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (x: unknown) => Object.create(Error.prototype, { message: { get() { return x; } } });
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
  msgBigInt: () => withMsg(BigInt(12)),
  msgCyclic: () => { const c: any = {}; c.self = c; return withMsg(c); },
  nullValue: () => null,
  undefinedValue: () => undefined,
  plainString: () => 'plain',
};
let uncaught: string | null = null, unhandled: string | null = null;
process.on('uncaughtException', (e) => { uncaught = String(e instanceof Error ? e.constructor.name + ':' + e.message : typeof e); });
process.on('unhandledRejection', (e) => { unhandled = String(e instanceof Error ? e.constructor.name + ':' + e.message : typeof e); });
const crypto = require('crypto'); crypto.randomInt = () => 0;
let getTxCalls = 0;
const v = VALUES[kase]();
const origLoad = Module._load;
Module._load = function (req: string, ...rest: unknown[]) {
  if (req === './provider') return { getTransaction: async () => {
    getTxCalls++;
    if (site === 'conf_always') throw v;
    if (site === 'conf_recover' && getTxCalls === 1) throw v;
    if (site === 'conf_recover' || site === 'conf_nocb') { if (site === 'conf_nocb' && getTxCalls === 1) throw v; return { block: 'BLK', block_height: 7, slot: 9 }; }
    return null;
  } };
  return origLoad.call(this, req, ...rest);
};
(async () => {
  const sfx = variant === 'base' ? '_base' : '';
  let result: any = 'n/a', outcome = 'n/a';
  const statuses: string[] = [];
  const row = { id: 'A1', status: 'submitted', transaction_hash: 'abc', error_message: null as string | null };
  let queryCalls = 0;
  if (site === 'status') {
    const mod = require(SRC + 'anchorStatusUpdate' + sfx);
    const deps = { isDbAvailable: () => true, ensureTables: async () => {}, log,
      query: async (_s: string, _p?: unknown[]) => { queryCalls++; throw v; } };
    try { result = await mod.runAnchorStatusUpdate(deps, 'A1', { status: 'confirmed', confirmations: 1 }); outcome = 'resolved'; }
    catch (e) { outcome = 'REJECTED:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e); }
  } else {
    const mod = require(SRC + 'cardano/confirmation' + sfx);
    const cb = site === 'conf_nocb' ? undefined : (a: number, s: string) => { statuses.push(a + '|' + s); log('info', 'Anchor confirmation poll', { anchorId: 'A1', attempt: a, status: s }); };
    try { result = await mod.waitForConfirmation('tx1', 3, 0, 0, cb); outcome = 'resolved'; }
    catch (e) { outcome = 'REJECTED:' + (e instanceof Error ? e.constructor.name + ':' + String((e as Error).message) : typeof e); }
  }
  const lines = out.map((l) => { try { const o = JSON.parse(l); delete o.timestamp; return { ...o, hasErrorKey: 'error' in o }; } catch { return { raw: l.slice(0, 80) }; } });
  realLog(JSON.stringify({ site, variant, kase, outcome, result, getTxCalls, queryCalls, statuses, row, uncaught, unhandled, lines }, (k, x) => typeof x === 'symbol' ? x.toString() : x));
  process.exit(0);
})();
