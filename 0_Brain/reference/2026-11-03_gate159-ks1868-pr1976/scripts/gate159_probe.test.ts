// QA gate 159 probe (KS-1868, PR 1976). Copied verbatim into wt_base and wt_head (src/__tests__/zz_gate159_probe.test.ts)
// and run there with vitest. REAL modules: reconciler.ts, cardano/threadTokenIndex.ts, utils/logger.ts (winston 3.19),
// @secuura/shared (built dist). REPLACED: only ../db (the registry query) and, for the reconciler, the chain/DB/wallet deps.
// The reconciler's production log() is index.ts's own function, extracted from that worktree's index.ts source text
// (index.ts cannot be imported: it starts the HTTP listener on import).
import { it, vi } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const OUT = process.env.GATE_OUT as string;
const SIDE = process.env.GATE_SIDE as string;
const write = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

const h = vi.hoisted(() => ({ dbMode: 'populated' as 'populated' | 'empty' | 'throw', value: undefined as unknown, dbCalls: 0 }));
vi.mock('../db', () => ({
  query: async () => {
    h.dbCalls++;
    if (h.dbMode === 'throw') throw h.value;
    if (h.dbMode === 'empty') return { rows: [] };
    return { rows: [{ document_id: 'doc-1', policy_id: 'pol1', network: 'preprod', status: 'active' }] };
  },
}));

// ---------- thrown values ----------
const revokedProxy = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMessage = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('boom'),
  plainString: () => 'boom',
  revokedProxy,
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  msgSymbol: () => withMessage(Symbol('s')),
  null: () => null,
  undefined: () => undefined,
  msgBigInt: () => withMessage(10n),
  bigIntRaw: () => 10n,
  errThrowingToJSON: () => Object.assign(new Error('boom'), { toJSON() { throw new Error('toJSON boom'); } }),
  msgThrowingToJSON: () => withMessage({ toJSON() { throw new Error('toJSON boom'); } }),
  msgThrowingToString: () => withMessage({ toString() { throw new Error('toString boom'); } }),
  objThrowingToString: () => ({ toString() { throw new Error('toString boom'); } }),
  msgNullProto: () => withMessage(Object.create(null)),
};

// ---------- output capture (real logger writes go through these) ----------
type Cap = { lines: string[]; unhandled: string[]; uncaught: string[] };
function describeErr(e: unknown): string {
  try {
    if (e instanceof Error) return `${e.constructor.name}: ${e.message}`;
    return `${typeof e}:${String(e)}`;
  } catch { return `<unprintable ${typeof e}>`; }
}
async function capture<T>(fn: () => Promise<T>): Promise<{ cap: Cap; res: T }> {
  const cap: Cap = { lines: [], unhandled: [], uncaught: [] };
  const c: any = console;
  const saved: Array<[any, string, any]> = [];
  const hook = (obj: any, key: string) => {
    if (!obj || typeof obj[key] !== 'function') return;
    const orig = obj[key];
    saved.push([obj, key, orig]);
    obj[key] = (...a: unknown[]) => { cap.lines.push(a.map((x) => (typeof x === 'string' ? x : String(x))).join(' ').replace(/\u001b\[[0-9;]*m/g, '').trimEnd()); return true; };
  };
  hook(process.stdout, 'write'); hook(process.stderr, 'write');
  if (c._stdout && c._stdout !== process.stdout) hook(c._stdout, 'write');
  if (c._stderr && c._stderr !== process.stderr) hook(c._stderr, 'write');
  hook(c, 'log'); hook(c, 'error'); hook(c, 'warn'); hook(c, 'info'); hook(c, 'debug');
  const onUR = (r: unknown) => cap.unhandled.push(describeErr(r));
  const onUE = (e: unknown) => cap.uncaught.push(describeErr(e));
  process.on('unhandledRejection', onUR);
  process.on('uncaughtException', onUE);
  let res: T;
  try {
    res = await fn();
    for (let i = 0; i < 5; i++) await new Promise((r) => setImmediate(r));
    await new Promise((r) => setTimeout(r, 30));
  } finally {
    for (const [o, k, f] of saved.reverse()) o[k] = f;
    process.off('unhandledRejection', onUR);
    process.off('uncaughtException', onUE);
  }
  return { cap, res: res! };
}

// ---------- registry ----------
type Idx = typeof import('../cardano/threadTokenIndex');
async function loadIdx(strict: boolean, nodeEnv: string): Promise<Idx> {
  process.env.STRICT_THREAD_TOKEN_INDEX = strict ? 'true' : 'false';
  process.env.NODE_ENV = nodeEnv;
  delete process.env.LOG_LEVEL;
  vi.resetModules();
  return import('../cardano/threadTokenIndex');
}
const UTXO_FOREIGN = { amount: [{ unit: 'lovelace', quantity: '2000000' }, { unit: 'attackerpol', quantity: '1' }] };
const UTXO_GOOD = { amount: [{ unit: 'lovelace', quantity: '2000000' }, { unit: 'pol1', quantity: '1' }] };

function summarise(v: unknown): unknown {
  if (Array.isArray(v)) return v.map((x: any) => (x && typeof x === 'object' && 'utxo' in x ? { utxo: x.utxo === UTXO_FOREIGN ? 'FOREIGN' : x.utxo === UTXO_GOOD ? 'GOOD' : '?', documentId: x.documentId, policyId: x.policyId } : x));
  return v;
}

async function registryCell(fnName: 'loadActiveRegistry' | 'filterUtxosByRegistry' | 'utxoIsTrusted', strict: boolean, nodeEnv: string, dbMode: 'populated' | 'empty' | 'throw', valueName: string | null) {
  const idx = await loadIdx(strict, nodeEnv);
  h.dbMode = dbMode; h.dbCalls = 0;
  const original = valueName ? VALUES[valueName]() : undefined;
  h.value = original;
  const { cap, res } = await capture(async () => {
    try {
      let v: unknown;
      if (fnName === 'loadActiveRegistry') v = await idx.loadActiveRegistry('preprod' as never);
      else if (fnName === 'filterUtxosByRegistry') v = await idx.filterUtxosByRegistry([UTXO_FOREIGN, UTXO_GOOD] as never, 'preprod' as never);
      else v = await idx.utxoIsTrusted(UTXO_FOREIGN as never, 'preprod' as never);
      return { settled: 'resolved', value: summarise(v) };
    } catch (e) {
      return { settled: 'rejected', sameAsThrown: e === original, error: describeErr(e) };
    }
  });
  write({ kind: 'registry', side: SIDE, fn: fnName, strict, nodeEnv, db: dbMode, thrown: valueName, ...res, dbCalls: h.dbCalls, lines: cap.lines, unhandled: cap.unhandled, uncaught: cap.uncaught });
}

// ---------- reconciler ----------
const TXS = ['a', 'b', 'c'].map((ch) => ch.repeat(64));
function extractRealLog(): (level: string, message: string, meta?: object) => void {
  const src = fs.readFileSync(path.resolve(__dirname, '../index.ts'), 'utf8');
  const m = /\nfunction log\(level: 'info' \| 'warn' \| 'error', message: string, meta\?: object\) \{\n([\s\S]*?)\n\}\n/.exec(src);
  if (!m) throw new Error('could not extract index.ts log()');
  // eslint-disable-next-line no-new-func
  return new Function('level', 'message', 'meta', m[1]) as never;
}

type RecSetup = { where: 'none' | 'checkTx' | 'select' | 'updateStatus' | 'sweepScan' | 'giveupNone' | 'giveupCheckTx'; value: string | null };
async function reconcilerCell(s: RecSetup) {
  const { createStuckAnchorReconciler } = await import('../reconciler');
  const realLog = extractRealLog();
  const original = s.value ? VALUES[s.value]() : undefined;
  const updates: Array<{ id: string; status: unknown; tx?: unknown }> = [];
  let clock = new Date('2026-08-11T12:00:00Z').getTime();
  const GU = s.where.startsWith('giveup');
  // giveup*: rows last written 2 days ago (past the 24 h window); rows 2,3 answered 'not found'; the wallet search finds nothing.
  const rowsWithHash = TXS.map((tx, i) => ({ id: `r${i + 1}`, transaction_hash: tx, metadata_payload: { doc: `r${i + 1}` }, created_at: GU ? '2026-08-09T09:00:00Z' : '2026-08-11T09:00:00Z', updated_at: GU ? '2026-08-09T09:00:00Z' : '2026-08-11T09:00:00Z' }));
  const nullRows = [1, 2].map((i) => ({ id: `n${i}`, status: 'pending', transaction_hash: null, metadata_label: 674, metadata_payload: { doc: `n${i}` }, error_message: null, created_at: '2026-08-11T09:00:00Z', updated_at: '2026-08-11T09:00:00Z', updated_at_token: '2026-08-11 09:00:00+00' }));
  let pass = 0;
  const deps: any = {
    isDbAvailable: () => true,
    isCardanoReady: () => true,
    query: async (sql: string) => {
      if (s.where === 'select' && /transaction_hash IS NOT NULL/.test(sql)) return Promise.reject(original);
      if (/transaction_hash IS NOT NULL/.test(sql)) return { rows: GU ? rowsWithHash : pass === 1 ? rowsWithHash : [] };
      if (GU) return { rows: [] };
      return { rows: pass === 2 ? nullRows : [] };
    },
    checkTx: async (tx: string) => {
      if ((s.where === 'checkTx' || s.where === 'giveupCheckTx') && tx === TXS[0]) return Promise.reject(original);
      if (GU) return { confirmed: false, polled: 1, errored: 0 };
      if (tx.startsWith('f')) return { confirmed: true, blockNumber: 9, blockHash: 'bh', slot: 9, confirmations: 1, polled: 1 };
      return { confirmed: true, blockNumber: 7, blockHash: 'bh', slot: 7, confirmations: 1, polled: 1 };
    },
    updateStatus: async (id: string, u: Record<string, unknown>) => {
      if (s.where === 'updateStatus' && id === 'r1') return Promise.reject(original);
      updates.push({ id, status: u.status, tx: u.transactionHash });
      return 1;
    },
    log: (level: string, message: string, meta?: Record<string, unknown>) => realLog(level, message, meta),
    now: () => clock,
    isDriven: () => false,
    scanWallet: async () => {
      if (s.where === 'sweepScan') return Promise.reject(original);
      if (GU) return { outcome: 'complete', scanned: 0, matches: [] };
      return { outcome: 'complete', scanned: 1, matches: [{ txHash: 'f'.repeat(64), json: {} }] };
    },
  };
  const reconcile = createStuckAnchorReconciler(deps, { minAgeMs: 600_000, giveUpMs: 24 * 3_600_000, batch: 25 });
  const passes: unknown[] = [];
  const { cap } = await capture(async () => {
    // pass 1: the hash rows (sweep not yet armed: boot grace). pass 2: past the boot grace, the sweep's no-hash rows.
    // pass 3: proves `running` was released (a fresh, empty pass resolves).
    for (pass = 1; pass <= 3; pass++) {
      if (pass === 2) clock += 3 * 3_600_000;
      try { passes.push({ settled: 'resolved', value: await reconcile() }); }
      catch (e) { passes.push({ settled: 'rejected', error: describeErr(e) }); }
    }
    return null;
  });
  write({ kind: 'reconciler', side: SIDE, where: s.where, thrown: s.value, passes, updates, lines: cap.lines, unhandled: cap.unhandled, uncaught: cap.uncaught });
}

it('gate159 probe', async () => {
  const names = Object.keys(VALUES);
  const fns = ['loadActiveRegistry', 'filterUtxosByRegistry', 'utxoIsTrusted'] as const;
  for (const nodeEnv of ['test', 'production']) {
    for (const strict of [false, true]) {
      for (const fn of fns) {
        await registryCell(fn, strict, nodeEnv, 'populated', null);
        await registryCell(fn, strict, nodeEnv, 'empty', null);
        for (const v of names) await registryCell(fn, strict, nodeEnv, 'throw', v);
      }
    }
  }
  await reconcilerCell({ where: 'none', value: null });
  await reconcilerCell({ where: 'giveupNone', value: null });
  for (const v of names) await reconcilerCell({ where: 'giveupCheckTx', value: v });
  for (const where of ['checkTx', 'select', 'updateStatus', 'sweepScan'] as const) {
    for (const v of names) await reconcilerCell({ where, value: v });
  }
}, 600_000);
