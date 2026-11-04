import { describe, it, expect, vi, beforeEach, afterAll } from 'vitest';
import { writeFileSync } from 'node:fs';
import { inspect } from 'node:util';

// Gate 187 harness (credentialRepo three changed catches). Drives the REAL module with ../db and the
// logger replaced. Writes a raw cell table; asserts nothing about base/head (the table is compared offline).
const TOKEN = 'G187PLANTEDzq81';
const OUT = process.env.G187_OUT || '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate187-ks1868-pr1968/runs/cells_repo_' + (/\/(?:scratch|mut)\/([^/]+)\//.exec(__filename)?.[1] ?? 'x') + '.json';

const h = vi.hoisted(() => ({
  mode: 'reject' as 'reject' | 'row',
  toThrow: undefined as unknown,
  row: undefined as unknown,
  logs: [] as { level: string; message: string; meta: unknown }[],
}));
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: (sql: string) => {
    if (/LIMIT 0/i.test(sql)) return Promise.resolve({ rows: [] });
    if (h.mode === 'row') return Promise.resolve({ rows: [h.row] });
    return Promise.reject(h.toThrow);
  },
}));
vi.mock('../utils/logger', () => {
  const rec = (level: string) => (message: string, meta?: unknown) => {
    h.logs.push({ level, message, meta });
  };
  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
});

import * as repo from '../repositories/credentialRepo';

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
const SITES: Record<string, { fn: () => Promise<unknown>; prefix: string }> = {
  getById: { fn: () => repo.getById('cred-g187'), prefix: 'DB read failed' },
  getRecordById: { fn: () => repo.getRecordById('cred-g187'), prefix: 'DB read failed' },
  getByHash: { fn: () => repo.getByHash('hash-g187'), prefix: 'DB hash lookup failed' },
};

const table: any[] = [];
beforeEach(() => { h.logs.length = 0; h.mode = 'reject'; h.toThrow = undefined; h.row = undefined; });
afterAll(() => { writeFileSync(OUT, JSON.stringify(table, null, 1)); });

describe('gate187 repo cells', () => {
  for (const [site, s] of Object.entries(SITES)) {
    for (const [vname, mk] of Object.entries(VALUES)) {
      it(`${site} x ${vname}`, async () => {
        h.toThrow = mk();
        let outcome: any;
        try { outcome = { threw: false, value: await s.fn() }; } catch { outcome = { threw: true }; }
        const lines = h.logs.filter((l) => l.message.startsWith(s.prefix));
        const all = h.logs.map((l) => l.message + ' ' + inspect(l.meta, { depth: 5, showHidden: true })).join('\n');
        const err = (lines[0]?.meta as any)?.error;
        table.push({ site, value: vname, threw: outcome.threw, value_out: outcome.threw ? null : String(outcome.value),
          lines: lines.length, allLogs: h.logs.length, reasonType: typeof err, reason: typeof err === 'symbol' ? String(err) : err,
          metaKeys: lines[0] ? Object.keys(lines[0].meta as object) : null, tokenInLogs: all.includes(TOKEN) });
        expect(true).toBe(true);
      });
    }
    it(`${site} x rowWithToken`, async () => {
      h.mode = 'row';
      const cred = { id: 'cred-g187', proof: TOKEN, credentialSubject: { documentHash: 'hash-g187', secret: TOKEN } };
      h.row = { credential: cred, created_by_user_id: 'u-' + TOKEN, created_by_tenant_id: null };
      let outcome: any;
      try { outcome = { threw: false, value: await s.fn() }; } catch { outcome = { threw: true }; }
      const all = h.logs.map((l) => l.message + ' ' + inspect(l.meta, { depth: 5, showHidden: true })).join('\n');
      table.push({ site, value: 'rowWithToken', threw: outcome.threw, value_out: outcome.threw ? null : (outcome.value ? 'credential' : String(outcome.value)),
        lines: 0, allLogs: h.logs.length, reasonType: null, reason: null, metaKeys: null, tokenInLogs: all.includes(TOKEN) });
    });
  }
});
