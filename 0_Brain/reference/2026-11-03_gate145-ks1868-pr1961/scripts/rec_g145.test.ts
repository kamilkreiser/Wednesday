// Gate 145 recorder (never committed). REAL getRecentErrors + REAL decodeLifecyclePayload + REAL originate winston logger
// (NODE_ENV decides dev Console vs production json + File transports; cwd anchored in the gate workdir). Replaced: ../db, decryptField.
import * as fs from 'node:fs';
const mockH: { toThrow: unknown } = { toThrow: undefined };
jest.mock('../db', () => ({ prisma: { $queryRaw: async () => { throw mockH.toThrow; }, $executeRaw: async () => 0 } }));
jest.mock('@secuura/shared', () => ({ ...jest.requireActual('@secuura/shared'), isEncryptedPii: () => true, decryptField: () => { throw mockH.toThrow; } }));
import { getRecentErrors } from '../services/errorTrackingService';
import { decodeLifecyclePayload } from '../utils/lifecyclePayloadCodec';
import { logger } from '../utils/logger';
const nameOf = (e: unknown): string => { try { if (e instanceof Error) return `${e.constructor.name}: ${String(e.message).slice(0, 70)}`; return typeof e; } catch { return 'hostile'; } };
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const em = (m: unknown) => Object.defineProperty(new Error('x'), 'message', { value: m, enumerable: false });
const V: [string, () => unknown][] = [
  ['ordinary Error', () => new Error('boom')],
  ['plain string', () => 'just a string'],
  ['number 42', () => 42],
  ['undefined', () => undefined],
  ['null', () => null],
  ['Symbol thrown', () => Symbol('sym')],
  ['BigInt thrown', () => 10n],
  ['Error msg Symbol', () => em(Symbol('m'))],
  ['Error msg BigInt', () => em(10n)],
  ['Error msg 42', () => em(42)],
  ['Error msg undefined', () => em(undefined)],
  ['Error msg null-proto obj', () => em(Object.create(null))],
  ['Error msg getter throws', () => Object.defineProperty(new Error('x'), 'message', { get() { throw new Error('inner'); } })],
  ['revoked Proxy', revoked],
  ['getPrototypeOf trap throws', () => new Proxy({}, { getPrototypeOf() { throw new Error('trap'); } })],
  ['null-prototype object', () => Object.create(null)],
  ['throwing toString', () => ({ toString() { throw new Error('ts'); } })],
];
it('rec', async () => {
  const out: any[] = [];
  const lines: string[] = []; const lerr: string[] = [];
  const tr: any = (logger as any).transports[0];
  const on = (info: any) => lines.push(String(info[Symbol.for('message')]).replace(/\u001b\[[0-9;]*m/g, '').replace(/^\d{4}-\d{2}-\d{2} [0-9:.]+ /, '').replace(/"timestamp":"[^"]*",?/, ''));
  tr.on('logged', on); (logger as any).on('error', (e: unknown) => lerr.push(nameOf(e)));
  const flush = () => new Promise<void>((r) => setImmediate(r));
  for (const site of ['query', 'decode']) for (const [name, mk] of V) {
    lines.length = 0; lerr.length = 0; mockH.toThrow = mk(); let outcome: string;
    try {
      if (site === 'query') { const v: any = await getRecentErrors(); outcome = `RESOLVED errors=${v.errors.length} total=${v.total}`; }
      else { const v = decodeLifecyclePayload('v1:aa:bb:cc', 'event-1'); outcome = 'RETURNED ' + JSON.stringify(v); }
    } catch (e) { outcome = 'THREW ' + nameOf(e); }
    await flush();
    out.push({ site, name, outcome, logs: [...lines, ...lerr.map((x) => 'LOGGER-ERROR ' + x)] });
  }
  tr.off('logged', on);
  fs.writeFileSync(process.env.G145_OUT as string, JSON.stringify(out, null, 1));
}, 120000);
