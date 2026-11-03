import { it, vi } from 'vitest';
import * as fs from 'fs';
const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));
vi.mock('../db', () => ({ isDbAvailable: () => true, query: (..._a: unknown[]) => Promise.reject(h.toThrow) }));
import { verifyDbReady, delegationService } from '../services/delegationService';

const OUT = process.env.G158_OUT as string;
const rp = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const kinds: Record<string, () => unknown> = {
  ordinary: () => new Error('db boom'),
  revokedProxy: rp,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('boom'); } } }),
  symbolMessage: () => ({ message: Symbol('s') }),
  thrownSymbol: () => Symbol('t'),
  nullThrown: () => null,
  undefinedThrown: () => undefined,
  bigintMessage: () => ({ message: 10n }),
  throwingToJSON: () => ({ message: 'x', toJSON() { throw new Error('tj'); } }),
  throwingToStringObj: () => Object.freeze({ toString() { throw new Error('ts'); } }),
  messageIsThrowingToString: () => ({ message: Object.freeze({ toString() { throw new Error('ts'); } }) }),
  messageNullProto: () => ({ message: Object.create(null) }),
  proxyGetTrapThrows: () => new Proxy({}, { get() { throw new Error('trap'); } }),
  toPrimitiveReturnsObject: () => ({ message: { [Symbol.toPrimitive]: () => ({}) } }),
  numberThrown: () => 42,
  stringThrown: () => 'str',
};
const unh: unknown[] = [];
process.on('unhandledRejection', (r) => { unh.push(r); });
const tname = (v: unknown) => v === null ? 'null' : typeof v;
it('matrix', async () => {
  const realW = console.warn, realE = console.error;
  const rows: string[] = [];
  for (const [name, mk] of Object.entries(kinds)) {
    for (const fn of ['verifyDbReady', 'processExpired']) {
      const rec: unknown[][] = []; let fwdThrew = false;
      const rec2 = (...a: unknown[]) => { rec.push(a); try { (fn === 'verifyDbReady' ? realW : realE)('[g158-fwd]', ...a); } catch { fwdThrew = true; } };
      console.warn = rec2; console.error = rec2;
      h.toThrow = mk(); unh.length = 0;
      let outcome = 'resolve', ret: unknown = undefined;
      try { ret = fn === 'verifyDbReady' ? await verifyDbReady() : await delegationService.processExpiredDelegations(); } catch (e) { outcome = 'reject'; }
      await new Promise((r) => setImmediate(r));
      console.warn = realW; console.error = realE;
      const arg = rec.length === 1 ? rec[0][1] : '<' + rec.length + ' calls>';
      rows.push(JSON.stringify({ mode: process.env.G158_MODE, kind: name, fn, outcome, ret: String(ret), calls: rec.length, loggedType: tname(arg), logged: typeof arg === 'string' ? arg : null, fwdThrew, unhandled: unh.length }));
    }
  }
  fs.appendFileSync(OUT, rows.join('\n') + '\n');
});
