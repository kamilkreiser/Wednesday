import { describe, it, expect, vi, beforeEach, afterAll } from 'vitest';
import { writeFileSync } from 'node:fs';
import { inspect } from 'node:util';

// Gate 187 harness (db.ts two changed catches: pool 'error' listener, runDbReadyHook). Real module, pg + logger replaced.
const TOKEN = 'G187PLANTEDzq81';
const OUT = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate187-ks1868-pr1968/runs/cells_db_' + (/\/(?:scratch|mut)\/([^/]+)\//.exec(__filename)?.[1] ?? 'x') + '.json';

const h = vi.hoisted(() => ({
  listener: undefined as undefined | ((e: unknown) => void),
  calls: [] as { level: string; message: string; meta: unknown }[],
}));
vi.mock('../utils/logger', () => {
  const rec = (level: string) => (message: string, meta?: unknown) => { h.calls.push({ level, message, meta }); };
  return { logger: { error: rec('error'), warn: rec('warn'), info: rec('info'), debug: rec('debug') } };
});
vi.mock('pg', () => ({
  Pool: function PoolMock() {
    return {
      query: async () => ({ rows: [{ ok: 1 }] }),
      on: (event: string, fn: (e: unknown) => void) => { if (event === 'error') h.listener = fn; },
      end: async () => undefined,
      connect: async () => undefined,
    };
  },
}));

const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
const revoked = (): unknown => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const VALUES: Record<string, () => unknown> = {
  ordinaryError: () => new Error('ord-msg'),
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => withMessage(Symbol('g187')),
  objectMessage: () => withMessage({ toString() { return 'objstr'; } }),
  objectMessageToStringThrows: () => withMessage({ toString() { throw new Error('ts boom'); } }),
  numberMessage: () => withMessage(7),
  thrownNull: () => null,
  thrownUndefined: () => undefined,
  thrownString: () => 'plain',
  thrownNumber: () => 42,
  secretInOtherFields: () => {
    const e: any = new Error('ord-msg');
    e.detail = 'detail ' + TOKEN; e.hint = TOKEN; e.where = TOKEN; e.query = 'SELECT ' + TOKEN;
    e.cause = new Error('cause ' + TOKEN); e.stack = 'Error: ord-msg\n at ' + TOKEN; e.parameters = [TOKEN];
    return e;
  },
  secretInMessage: () => new Error('msg ' + TOKEN),
};

const realUrl = process.env.DATABASE_URL;
const table: any[] = [];
beforeEach(() => { h.listener = undefined; h.calls.length = 0; process.env.DATABASE_URL = 'postgresql://t:t@localhost:5432/t'; });
afterAll(() => {
  if (realUrl === undefined) delete process.env.DATABASE_URL; else process.env.DATABASE_URL = realUrl;
  writeFileSync(OUT, JSON.stringify(table, null, 1));
});
const fresh = async () => { vi.resetModules(); return import('../db'); };
const dump = () => h.calls.map((c) => c.message + ' ' + inspect(c.meta, { depth: 5, showHidden: true })).join('\n');
const row = (site: string, vname: string, outcome: any, msg: string) => {
  const lines = h.calls.filter((c) => c.message === msg);
  const err = (lines[0]?.meta as any)?.error;
  table.push({ site, value: vname, ...outcome, lines: lines.length, reasonType: typeof err,
    reason: typeof err === 'symbol' ? String(err) : err, metaKeys: lines[0] ? Object.keys(lines[0].meta as object) : null,
    tokenInLogs: dump().includes(TOKEN) });
};

describe('gate187 db cells', () => {
  for (const [vname, mk] of Object.entries(VALUES)) {
    it(`poolListener x ${vname}`, async () => {
      const db = await fresh();
      db.getPool();
      let threw = false;
      try { (h.listener as (e: unknown) => void)(mk()); } catch { threw = true; }
      row('poolListener', vname, { threw }, 'DB pool unexpected error');
      expect(true).toBe(true);
    }, 30000);
    it(`readyHook x ${vname}`, async () => {
      const db = await fresh();
      const v = mk();
      let out: any;
      try { out = { threw: false, initDb: await db.initDb(async () => { throw v; }) }; } catch { out = { threw: true, initDb: null }; }
      row('readyHook', vname, out, 'DB ready boot work failed');
      expect(true).toBe(true);
    }, 30000);
  }
});
