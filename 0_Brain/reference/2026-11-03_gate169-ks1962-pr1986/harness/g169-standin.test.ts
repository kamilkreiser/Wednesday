// Gate 169: the REAL threadTokenIndex + REAL @secuura/shared + REAL winston logger (capture transport added); the db module
// is a stand-in whose query() rejects with / throws / resolves exactly what each cell names. A logger-throws switch wraps the
// real logger. STRICT_MODE is read at module load: each cell loads a fresh copy.
import { describe, it, vi, beforeAll } from 'vitest';
import { NET, PID, GENUINE, FOREIGN, lines, Cap, typeName, race, record, reset } from './g169-common';
const OUT = process.env.G169_OUT as string;
const h = vi.hoisted(() => ({ q: (() => Promise.resolve({ rows: [] })) as () => unknown, loggerThrows: false }));
vi.mock('../db', () => ({ query: () => h.q() }));
vi.mock('../utils/logger', async (orig) => {
  const real: any = await orig();
  const wrap = new Proxy(real.logger, {
    get(t, k) {
      const v = Reflect.get(t, k);
      if (typeof v === 'function' && ['debug', 'info', 'warn', 'error'].includes(String(k)))
        return (...a: unknown[]) => { if (h.loggerThrows) throw new Error('logger down'); return v.apply(t, a); };
      return typeof v === 'function' ? v.bind(t) : v;
    },
  });
  return { ...real, logger: wrap, __real: real.logger };
});
beforeAll(async () => { reset(OUT); const lg: any = await import('../utils/logger'); lg.__real.add(new Cap()); }, 60_000);
const SECRET = 'PLANTED-g169-s3cr3t-value';
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const protoTrap = () => new Proxy({}, { getPrototypeOf() { throw new Error(SECRET); } });
const ctorGetterThrows = () => Object.create(Object.create(Object.prototype, { constructor: { get() { throw new Error(SECRET); } } }));
const nameGetterThrows = () => { class X {} Object.defineProperty(X, 'name', { get() { throw new Error(SECRET); } }); return new X(); };
const msgGetterThrows = () => Object.create(Error.prototype, { message: { get() { throw new Error(SECRET); } } });
const pgLike = () => Object.assign(new Error(`password for user "x" is ${SECRET}`), { code: '28P01', detail: SECRET, severity: 'FATAL' });
const rej = (v: () => unknown) => () => Promise.reject(v());
type K = [string, () => unknown];
const kinds: K[] = [
  ['ok-populated (control)', () => Promise.resolve({ rows: [{ document_id: 'doc-1', policy_id: PID, network: 'preprod', status: 'active' }] })],
  ['ok-empty (control)', () => Promise.resolve({ rows: [] })],
  ['ordinary Error with planted message', rej(() => new Error(SECRET))],
  ['pg-like Error (code/detail planted)', rej(pgLike)],
  ['plain string (planted)', rej(() => SECRET)],
  ['null', rej(() => null)],
  ['undefined', rej(() => undefined)],
  ['number 0', rej(() => 0)],
  ['Symbol', rej(() => Symbol(SECRET))],
  ['revoked Proxy', rej(revoked)],
  ['Proxy getPrototypeOf trap throws', rej(protoTrap)],
  ['constructor getter throws', rej(ctorGetterThrows)],
  ['constructor.name getter throws', rej(nameGetterThrows)],
  ['Error message getter throws', rej(msgGetterThrows)],
  ['missing table 42P01 (pg-shaped)', rej(() => Object.assign(new Error('relation "state_thread_registry" does not exist'), { code: '42P01' }))],
  ['AggregateError', rej(() => new AggregateError([new Error(SECRET)], SECRET))],
  ['thrown thenable', rej(() => ({ then(r: (v: unknown) => void) { r({ rows: [] }); } }))],
  ['query throws synchronously', () => { throw new Error(SECRET); }],
  ['resolves rows:null (malformed)', () => Promise.resolve({ rows: null })],
  ['resolves rows getter throws', () => Promise.resolve(Object.defineProperty({}, 'rows', { get() { throw new Error(SECRET); } }))],
  ['resolves rows [null]', () => Promise.resolve({ rows: [null] })],
  ['resolves undefined', () => Promise.resolve(undefined)],
];
const summ = (r: { s: string; v?: unknown; ms: number }) =>
  r.s === 'resolved' ? { s: r.s, v: Array.isArray(r.v) ? { len: r.v.length, attributed: r.v.map((x: any) => x?.documentId ?? x?.policyId ?? null) } : r.v, ms: r.ms }
  : r.s === 'rejected' ? { s: r.s, type: typeName(r.v), ms: r.ms } : { s: r.s, ms: r.ms };
async function cell(kind: string, strict: boolean, q: () => unknown, loggerThrows: boolean) {
  process.env.STRICT_THREAD_TOKEN_INDEX = strict ? 'true' : 'false';
  vi.resetModules();
  const idx = await import('../cardano/threadTokenIndex');
  h.q = q; h.loggerThrows = loggerThrows; lines.length = 0;
  const tF = summ(await race(idx.utxoIsTrusted(FOREIGN, NET), 3000));
  const tG = summ(await race(idx.utxoIsTrusted(GENUINE, NET), 3000));
  const f = summ(await race(idx.filterUtxosByRegistry([GENUINE, FOREIGN], NET), 3000));
  const l = summ(await race(idx.loadActiveRegistry(NET), 3000));
  h.loggerThrows = false;
  record(OUT, { kind: kind + (loggerThrows ? ' +logger-throws' : ''), strict, trustedForeign: tF, trustedGenuine: tG, filter: f, load: l,
    logs: lines.filter((x) => x.includes('state_thread_registry')), secretInLogs: lines.some((x) => x.includes('s3cr3t')) });
}
describe('gate169 stand-in matrix', () => {
  for (const strict of [false, true]) for (const lt of [false, true]) for (const [k, q] of kinds) {
    if (lt && !['ordinary Error with planted message', 'revoked Proxy', 'ok-empty (control)'].includes(k)) continue;
    it(`${strict ? 'strict' : 'non-strict'} ${k}${lt ? ' logger-throws' : ''}`, async () => { await cell(k, strict, q, lt); }, 30_000);
  }
});
