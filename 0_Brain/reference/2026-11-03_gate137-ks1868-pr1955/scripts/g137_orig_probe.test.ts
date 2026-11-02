// GATE 137 probe (adapted from gate 114) (originate). Real anchorsRouter, real errorHandler, REAL winston logger (call-through capture),
// prisma replaced by a stateful stand-in (anchor_store table; writes counted), auth stubbed as in ks1657.
// Env: G137_OUT (jsonl path), G137_LOGENV (test|production), G137_STAGE (base|head).
/* eslint-disable */
import fs from 'fs';
import net from 'net';

const S: any = {
  rows: [] as any[],
  reject: null as null | RegExp,
  value: undefined as unknown,
  writes: 0,
  readCalls: 0,
  getterReads: 0,
};
jest.mock('../db', () => ({
  prisma: {
    $queryRaw: (strings: TemplateStringsArray, ...vals: unknown[]) => {
      const sql = Array.isArray(strings) ? strings.join('?') : String(strings);
      S.readCalls += 1;
      if (S.reject && S.reject.test(sql)) return Promise.reject(S.value);
      if (/SELECT 1/.test(sql)) return Promise.resolve([{ '?column?': 1 }]);
      if (/FROM anchor_store WHERE document_id/.test(sql)) return Promise.resolve(S.rows.filter((r: any) => r.document_id === vals[0]));
      return Promise.resolve([]);
    },
    $executeRaw: () => { S.writes += 1; return Promise.resolve(1); },
    $transaction: () => { S.writes += 1; return Promise.resolve([]); },
  },
  getTenantManager: () => null,
}));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
    next();
  },
}));
jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));

const OUT = process.env.G137_OUT as string;
const LOGENV = process.env.G137_LOGENV || 'test';
const STAGE = process.env.G137_STAGE || '?';
const outbound: string[] = [];
const connects: string[] = [];
const origConnect = net.Socket.prototype.connect;
(net.Socket.prototype as any).connect = function (...args: any[]) {
  const o = args[0];
  const host = typeof o === 'object' && o ? (o.host ?? o.path ?? 'localhost') : (typeof args[1] === 'string' ? args[1] : 'localhost');
  const port = typeof o === 'object' && o ? o.port : o;
  connects.push(`${host}:${port}`);
  if (!/^(127\.0\.0\.1|localhost|::1|\/)/.test(String(host))) outbound.push(`${host}:${port}`);
  return (origConnect as any).apply(this, args);
};

let logger: any; let anchorsRouter: any; let verifyAnchorsDbReady: any; let errorHandler: any;
const captured: any[] = [];
let server: any; let base = '';
let unhandled = 0;
const onUnh = () => { unhandled += 1; };

const revokedProxy = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const errWithMsg = (get: () => unknown) => Object.create(Error.prototype, { message: { get } });
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('lookup down at 10.0.0.7 password=hunter2'),
  revokedProxy,
  getterThrows: () => errWithMsg(() => { throw new Error('getter boom'); }),
  nullProto: () => Object.create(null),
  symbol: () => Symbol('sym-thrown'),
  plainString: () => 'plain string thrown',
  msgRevokedProxy: () => errWithMsg(() => revokedProxy()),
  msgBigInt: () => errWithMsg(() => BigInt(7)),
  msgSymbol: () => errWithMsg(() => Symbol('m')),
  msgToStringThrows: () => errWithMsg(() => ({ secretField: 's3cr3t', toString() { throw new Error('ts boom'); } })),
  msgNullProto: () => errWithMsg(() => Object.create(null)),
  // gate 137 additions
  msgUndefined: () => { const e: any = new Error('x'); e.message = undefined; return e; },
  msgNull: () => { const e: any = new Error('x'); e.message = null; return e; },
  msgNumber: () => errWithMsg(() => 42),
  msgPlainObject: () => errWithMsg(() => ({ secretField: 's3cr3t' })),
  msgCustomToString: () => errWithMsg(() => ({ secretField: 's3cr3t', toString() { return 'custom text'; } })),
  msgNonIdempotent: () => { let n = 0; return errWithMsg(() => { n += 1; S.getterReads += 1; return n === 1 ? 'first read text' : revokedProxy(); }); },
  plainObjectNoMsg: () => ({ code: 'E1' }),
  emptyMsgError: () => new Error(),
};
const DOC = 'doc-g137-seeded';
const HASH = 'ab'.repeat(32);

function errText(e: unknown): string {
  try { return e instanceof Error ? `${e.constructor.name}: ${e.message}` : `non-Error ${typeof e}`; } catch { return '<<unreadable>>'; }
}
async function send(path: string): Promise<any> {
  try {
    const res = await fetch(`${base}${path}`, { signal: AbortSignal.timeout(1500) });
    return { status: res.status, body: await res.text() };
  } catch (e: any) { return { status: 'NO_RESPONSE', err: String(e?.name) }; }
}
function rec(o: any) { fs.appendFileSync(OUT, JSON.stringify({ stage: STAGE, logenv: LOGENV, ...o }) + '\n'); }

beforeAll(async () => {
  process.env.NODE_ENV = LOGENV;
  process.chdir(process.env.G137_CWD as string); // production File transports write logs/ here (scratch)
  logger = require('../utils/logger').logger;
  for (const t of logger.transports) {
    const orig = t.log.bind(t);
    t.log = (info: any, cb: any) => {
      const sym = Object.getOwnPropertySymbols(info).find((s) => String(s) === 'Symbol(message)');
      captured.push({ transport: t.name || t.constructor?.name, level: String(info.level).replace(/\u001b\[[0-9;]*m/g, ''), message: info.message, line: sym ? String(info[sym]).replace(/\u001b\[[0-9;]*m/g, '') : null });
      return orig(info, cb);
    };
  }
  ({ anchorsRouter, verifyAnchorsDbReady } = require('../routes/anchors'));
  ({ errorHandler } = require('../middleware/errorHandler'));
  const express = require('express');
  const app = express();
  app.use('/api/anchors', express.json(), anchorsRouter);
  app.use(errorHandler);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  base = `http://127.0.0.1:${server.address().port}`;
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnh);
});
afterAll(() => { server?.closeAllConnections?.(); server?.close(); });

function reset() {
  S.rows = [{ id: 'row-1', document_id: DOC, transaction_hash: 'ef'.repeat(32), block_number: 12, network: 'preview', content_hash: HASH, anchored_at: new Date(0), simulated: false }];
  S.reject = null; S.value = undefined; S.writes = 0; S.readCalls = 0; S.getterReads = 0; captured.length = 0; unhandled = 0;
}
const settle = () => new Promise((r) => setTimeout(r, 60));

test('g137 originate probe', async () => {
  // positive control: the store answers the seeded row
  reset();
  let w = await send(`/api/anchors/${DOC}`); await settle();
  rec({ cell: 'get_control_found', kind: 'none', res: w, writes: S.writes, unhandled, logs: captured.slice() });
  reset();
  w = await send(`/api/anchors/doc-g137-absent`); await settle();
  rec({ cell: 'get_control_absent', kind: 'none', res: w, writes: S.writes, unhandled, logs: captured.slice() });
  for (const [kind, mk] of Object.entries(KINDS)) {
    reset(); S.reject = /FROM anchor_store WHERE document_id/; S.value = mk();
    w = await send(`/api/anchors/${DOC}`); await settle();
    rec({ cell: 'get_lookup_throws', kind, res: w, getterReads: S.getterReads, writes: S.writes, unhandled, logs: captured.slice() });

    reset(); S.reject = /SELECT 1/; S.value = mk();
    let out: any;
    try { await verifyAnchorsDbReady(); out = { resolved: true }; } catch (e) { out = { rejected: errText(e) }; }
    await settle();
    rec({ cell: 'dbready_direct', kind, out, getterReads: S.getterReads, writes: S.writes, unhandled, logs: captured.slice() });

    reset(); S.reject = /SELECT 1/; S.value = mk();
    // index.ts:410-516 shape: Promise.all([...verifyAnchorsDbReady()]).then(...).catch(err => logger.warn(..., { error: err?.message }))
    let boot: any = 'pending';
    await Promise.all([verifyAnchorsDbReady()]).then(() => { boot = 'then'; }).catch((err: any) => {
      try { logger.warn('Some database connections failed — service may have degraded functionality', { error: err?.message }); boot = 'caught'; } catch (e) { boot = `catch threw: ${errText(e)}`; }
    });
    await settle();
    rec({ cell: 'dbready_boot', kind, out: boot, writes: S.writes, unhandled, logs: captured.slice() });
  }
  rec({ cell: 'network', connects: Array.from(new Set(connects)), outbound });
}, 120000);
