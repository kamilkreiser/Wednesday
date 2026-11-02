// Gate 117 probe (NOT part of PR 1935). Runs the REAL enforceRetention (gdprService.ts) and the REAL
// POST /api/gdpr/retention/enforce handler + real fail500, with only prisma replaced by a recorder and
// auth/logger stubbed. Every tagged-template statement is recorded with its full SQL text and values.
import * as fs from 'fs';

type Stmt = { fn: string; sql: string; values: string; label: string; failed: boolean };
const st: { failAt: string | null; thrown: unknown; stmts: Stmt[]; errs: string[] } = { failAt: null, thrown: undefined, stmts: [], errs: [] };

const POLICIES = [
  { id: 'p1-0000', data_type: 'user_sessions', retention_period_days: 30, deletion_method: 'delete', auto_delete: true },
  { id: 'p2-0000', data_type: 'audit_logs', retention_period_days: 365, deletion_method: 'anonymize', auto_delete: true },
  { id: 'p3-0000', data_type: 'share_records', retention_period_days: 90, deletion_method: 'delete', auto_delete: true },
  { id: 'p4-0000', data_type: 'no_such_type', retention_period_days: 10, deletion_method: 'delete', auto_delete: true },
];

function label(sql: string, values: unknown[]): string {
  if (/FROM data_retention_policies/.test(sql)) return 'SELECT policies';
  let m = /DELETE FROM (\w+)/.exec(sql); if (m) return 'DELETE ' + m[1];
  m = /UPDATE (audit_logs|system_errors) SET/.exec(sql); if (m) return 'ANON ' + m[1];
  if (/INSERT INTO data_deletion_log/.test(sql)) return 'INSERT log ' + String(values[0]);
  if (/UPDATE data_retention_policies/.test(sql)) return 'STAMP ' + String(values[0]);
  return 'OTHER';
}
async function rec(fn: string, strings: TemplateStringsArray, values: unknown[]): Promise<unknown> {
  const sql = strings.join('$?').replace(/\s+/g, ' ').trim();
  const l = label(sql, values);
  const failed = st.failAt === l;
  st.stmts.push({ fn, sql, values: JSON.stringify(values), label: l, failed });
  if (failed) throw st.thrown;
  if (l === 'SELECT policies') return POLICIES.map((p) => ({ ...p }));
  if (l.startsWith('DELETE') || l.startsWith('ANON')) return 3;
  if (l.startsWith('INSERT')) return [{ id: 'log-' + String(values[0]), data_type: values[0], records_affected: values[1], deletion_method: values[2], reason: values[3], performed_by: values[4], created_at: 'T' }];
  return 1;
}
jest.mock('../db', () => ({
  prisma: {
    $queryRaw: (s: TemplateStringsArray, ...v: unknown[]) => rec('queryRaw', s, v),
    $executeRaw: (s: TemplateStringsArray, ...v: unknown[]) => rec('executeRaw', s, v),
  },
}));
function safe(x: unknown): string { try { return JSON.stringify(x); } catch { return '<unserialisable>'; } }
jest.mock('../utils/logger', () => ({
  logger: { info: () => undefined, warn: () => undefined, debug: () => undefined, error: (...a: unknown[]) => { st.errs.push(safe(a)); } },
}));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (_q: unknown, _r: unknown, n: () => void) => n(),
  requireRole: () => (_q: unknown, _r: unknown, n: () => void) => n(),
  requireSelfOrRole: () => (_q: unknown, _r: unknown, n: () => void) => n(),
  hasAnyRole: () => true,
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { enforceRetention } from '../services/gdprService';
import { gdprRouter } from '../routes/gdpr';

const FIXED = Date.UTC(2026, 10, 2, 0, 0, 0);
const realNow = Date.now;
const THROWN: Record<string, () => unknown> = {
  error: () => new Error('db down'),
  string: () => 'db down string',
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  getterThrowsError: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  getterThrowsRevoked: () => Object.create(Error.prototype, { message: { get() { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); throw proxy; } } }),
  protoTrapThrows: () => new Proxy({}, { getPrototypeOf() { throw new Error('trap boom'); } }),
  toStringThrows: () => ({ toString() { throw new Error('toString boom'); } }),
};
const POINTS = ['none', 'SELECT policies', 'DELETE user_sessions', 'INSERT log user_sessions', 'STAMP p1-0000', 'ANON audit_logs', 'INSERT log audit_logs', 'STAMP p2-0000', 'DELETE share_records', 'INSERT log share_records', 'STAMP p3-0000', 'STAMP p4-0000'];

const out: unknown[] = [];
let unhandled = 0;
const onUnh = () => { unhandled += 1; };
const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';
beforeAll(async () => {
  process.on('unhandledRejection', onUnh);
  Date.now = () => FIXED;
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  Date.now = realNow;
  process.off('unhandledRejection', onUnh);
  server?.close();
  fs.writeFileSync(process.env.G117_OUT as string, JSON.stringify({ unhandled, cells: out }, null, 1));
});

function reset(point: string, kind: string) {
  st.failAt = point === 'none' ? null : point; st.thrown = THROWN[kind](); st.stmts = []; st.errs = [];
}
test('g117 grid', async () => {
  for (const kind of Object.keys(THROWN)) {
    for (const point of POINTS) {
      if (point === 'none' && kind !== 'error') continue;
      // 1. the function
      reset(point, kind);
      let settled = 'resolved'; let ret = '';
      try { ret = safe(await enforceRetention()); } catch (e) { settled = 'rejected'; let d = ''; try { d = e instanceof Error ? e.constructor.name + ':' + e.message : typeof e; } catch { d = 'unreadable'; } ret = d; }
      out.push({ via: 'function', kind, point, settled, ret, stmts: st.stmts, errs: st.errs });
      // 2. the manual route
      reset(point, kind);
      const res = await fetch(baseUrl + '/api/gdpr/retention/enforce', { method: 'POST' });
      const body = await res.text();
      out.push({ via: 'route', kind, point, status: res.status, body, stmts: st.stmts, errs: st.errs });
    }
  }
  await new Promise((r) => setTimeout(r, 50));
  expect(out.length).toBeGreaterThan(0);
}, 120000);
