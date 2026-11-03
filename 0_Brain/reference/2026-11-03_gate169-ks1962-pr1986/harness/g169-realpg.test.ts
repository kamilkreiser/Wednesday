// Gate 169: the REAL threadTokenIndex + REAL db.ts + REAL pg driver + REAL Postgres 15 (migration 010) + REAL winston logger
// (a capture transport is added to it). Nothing is mocked. STRICT_MODE is read at module load: each cell loads a fresh copy.
import { describe, it, vi, beforeAll, afterAll } from 'vitest';
import net from 'node:net';
import { Client } from 'pg';
import { NET, GENUINE, FOREIGN, lines, Cap, typeName, race, record, reset } from './g169-common';
const OUT = process.env.G169_OUT as string;
const PORT = process.env.G169_PG_PORT as string;
const PW = process.env.G169_PG_PW as string;
const url = (db: string, extra = '') => `postgres://postgres:${PW}@127.0.0.1:${PORT}/${db}${extra}`;
let silent: net.Server; let silentPort = 0; const socks: net.Socket[] = [];
beforeAll(async () => {
  reset(OUT);
  silent = net.createServer((s) => { socks.push(s); /* accept, never answer */ });
  await new Promise<void>((r) => silent.listen(0, '127.0.0.1', () => r()));
  silentPort = (silent.address() as net.AddressInfo).port;
});
afterAll(async () => { socks.forEach((s) => s.destroy()); await new Promise((r) => silent.close(r)); });

async function load(strict: boolean, dbUrl: string | undefined) {
  process.env.STRICT_THREAD_TOKEN_INDEX = strict ? 'true' : 'false';
  if (dbUrl === undefined) delete process.env.DATABASE_URL; else process.env.DATABASE_URL = dbUrl;
  vi.resetModules();
  const idx = await import('../cardano/threadTokenIndex');
  const db = await import('../db');
  const lg = await import('../utils/logger');
  lg.logger.add(new Cap());
  return { idx, db };
}
const summ = (r: { s: string; v?: unknown; ms: number }) =>
  r.s === 'resolved' ? { s: r.s, v: Array.isArray(r.v) ? { len: r.v.length, attributed: r.v.map((x: any) => x?.documentId ?? x?.policyId ?? null) } : r.v, ms: r.ms }
  : r.s === 'rejected' ? { s: r.s, type: typeName(r.v), code: (r.v as any)?.code ?? null, ms: r.ms } : { s: r.s, ms: r.ms };

async function cell(kind: string, strict: boolean, dbUrl: string | undefined, waitMs: number, before?: () => Promise<() => Promise<void>>) {
  lines.length = 0;
  const { idx, db } = await load(strict, dbUrl);
  const release = before ? await before() : undefined;
  const tF = summ(await race(idx.utxoIsTrusted(FOREIGN, NET), waitMs));
  const tG = summ(await race(idx.utxoIsTrusted(GENUINE, NET), waitMs));
  const f = summ(await race(idx.filterUtxosByRegistry([GENUINE, FOREIGN], NET), waitMs));
  const l = summ(await race(idx.loadActiveRegistry(NET), waitMs));
  let afterRelease: unknown = null;
  if (release) {
    const p = race(idx.utxoIsTrusted(FOREIGN, NET), 30_000);
    await release();
    afterRelease = summ(await p);
  }
  record(OUT, { kind, strict, trustedForeign: tF, trustedGenuine: tG, filter: f, load: l, afterRelease, logs: lines.filter((x) => x.includes('state_thread_registry')) , allLogs: lines.length });
  try { await Promise.race([db.closeDb(), new Promise((r) => setTimeout(r, 2000))]); } catch { /* ignore */ }
}

const kinds: [string, () => string | undefined, number, (() => Promise<() => Promise<void>>)?][] = [
  ['populated', () => url('reg'), 8000],
  ['empty-readable', () => url('empty'), 8000],
  ['missing-table-42P01', () => url('missing'), 8000],
  ['unknown-db-planted-3D000', () => url('plant_g169_secretmark'), 8000],
  ['bad-password-28P01', () => `postgres://postgres:plant_g169_pwmark@127.0.0.1:${PORT}/reg`, 8000],
  ['refused-ECONNREFUSED', () => 'postgres://postgres:x@127.0.0.1:1/reg', 8000],
  ['database-url-unset', () => undefined, 8000],
  ['connect-timeout-silent-server', () => `postgres://postgres:x@127.0.0.1:${silentPort}/reg`, 12_000],
  ['statement-timeout-57014-under-lock', () => url('reg', '?options=-c%20statement_timeout%3D300'), 8000, lockTable],
  ['hang-under-lock', () => url('reg'), 4000, lockTable],
];
async function lockTable(): Promise<() => Promise<void>> {
  const c = new Client({ connectionString: url('reg') });
  await c.connect();
  await c.query('BEGIN');
  await c.query('LOCK TABLE state_thread_registry IN ACCESS EXCLUSIVE MODE');
  return async () => { await c.query('ROLLBACK'); await c.end(); };
}
describe('gate169 real pg matrix', () => {
  for (const strict of [false, true]) {
    for (const [kind, u, ms, before] of kinds) {
      it(`${strict ? 'strict' : 'non-strict'} ${kind}`, async () => { await cell(kind, strict, u(), ms, before); }, 120_000);
    }
  }
});
