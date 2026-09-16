/**
 * qa1015-drafter-probe — DRAFTER probe (not a product test; lives only in the drafter's scratch trees, quarantined after).
 * REAL userRoutes + REAL errorHandler over 127.0.0.1:0. db.query is a STATEFUL stub over one in-probe verification_upgrade_requests
 * "table" with an SQL-scoped fault switch; userRepo is a recording stub (as the seat's cells), so a fault here is confined to the
 * verification table (F-ver). Records status, body, headers, INSERTs, user-level writes, error log lines per scenario.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';
import fs from 'node:fs';

const st = vi.hoisted(() => ({
  caller: { userId: '', role: 'USER', tenantId: 'tenant-default' } as Record<string, string>,
  users: new Map<string, Record<string, unknown>>(),
  table: new Map<string, Record<string, unknown>>(),
  fault: null as null | { re: RegExp; err: unknown },
  inserts: [] as unknown[][],
  userWrites: [] as unknown[],
}));
const q = vi.hoisted(() => vi.fn());
vi.mock('../repositories/userRepo', () => {
  const m = {
    getUserById: vi.fn(async (id: string) => st.users.get(id) ?? null),
    getUserByIdPlatformScope: vi.fn(async (id: string) => st.users.get(id) ?? null),
    updateUser: vi.fn(async (id: string, u: Record<string, unknown>) => { st.userWrites.push(['updateUser', id, u]); return { ...(st.users.get(id) || {}), ...u }; }),
    updateUserPlatformScope: vi.fn(async (id: string, u: Record<string, unknown>) => { st.userWrites.push(['updateUserPlatformScope', id, u]); return { ...(st.users.get(id) || {}), ...u }; }),
  };
  return { default: m, __esModule: true, ...m };
});
vi.mock('../middleware/authenticate', () => {
  const inject = () => (req: any, _res: any, next: any) => { req.user = { ...st.caller }; next(); };
  return { authenticate: inject, authenticateAccessOrConnector: inject };
});
vi.mock('../db', () => ({ isDbAvailable: () => true, query: q }));
vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
vi.mock('../services/password', () => ({ hashPassword: vi.fn(async () => 'h'), checkPasswordStrength: vi.fn(() => ({ ok: true })), verifyPassword: vi.fn(async () => true) }));
vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() } }));

import { userRoutes } from '../routes/users';
import { errorHandler } from '../middleware/errorHandler';
import { logger } from '../utils/logger';

q.mockImplementation(async (sql: string, p: unknown[] = []) => {
  if (st.fault && st.fault.re.test(sql)) throw st.fault.err;
  if (/INSERT INTO verification_upgrade_requests/.test(sql)) {
    st.inserts.push(p);
    const [id, user_id, current_level, target_level, documents, status, submitted_at, reviewed_at, reviewed_by, rejection_reason] = p as any[];
    const prev = st.table.get(id);
    st.table.set(id, prev ? { ...prev, status, reviewed_at, reviewed_by, rejection_reason } : { id, user_id, current_level, target_level, documents, status, submitted_at, reviewed_at, reviewed_by, rejection_reason });
    return { rows: [] };
  }
  const all = Array.from(st.table.values());
  if (/WHERE id = \$1/.test(sql)) return { rows: all.filter(r => r.id === p[0]) };
  if (/status = 'PENDING'/.test(sql)) return { rows: all.filter(r => r.user_id === p[0] && r.status === 'PENDING').slice(0, 1) };
  if (/ORDER BY submitted_at DESC/.test(sql)) return { rows: all.filter(r => r.user_id === p[0]) };
  return { rows: [] };
});

const ECONN = () => Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' });
const MSG = () => new Error('Connection terminated due to connection timeout');
const P53300 = () => Object.assign(new Error('sorry, too many clients already'), { code: '53300' });
const NONINFRA = () => Object.assign(new Error('relation "verification_upgrade_requests" does not exist'), { code: '42P01' });
const SEL_PENDING = /SELECT[\s\S]*status = 'PENDING'/;
const SEL_ID = /SELECT[\s\S]*WHERE id = \$1/;
const SEL_LIST = /SELECT[\s\S]*ORDER BY submitted_at DESC/;
const INSERT = /INSERT INTO verification_upgrade_requests/;

let server: Server; let base = '';
const rows: Record<string, unknown>[] = [];
beforeAll(async () => {
  const app = express(); app.use(express.json()); app.use('/', userRoutes); app.use(errorHandler);
  await new Promise<void>(r => { server = app.listen(0, '127.0.0.1', () => { base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`; r(); }); });
});
afterAll(async () => {
  await new Promise<void>(r => server.close(() => r()));
  fs.writeFileSync(process.env.QA_PROBE_OUT as string, JSON.stringify(rows, null, 1));
});
function user(id: string, extra: Record<string, unknown> = {}) { st.users.set(id, { id, email: `${id.slice(0, 4)}@t.example`, role: 'USER', status: 'ACTIVE', verificationLevel: 'BASIC', tenantId: 'tenant-default', ...extra }); }
function pendingRow(id: string, uid: string, status = 'PENDING') { st.table.set(id, { id, user_id: uid, current_level: 'BASIC', target_level: 'ENHANCED', documents: [], status, submitted_at: new Date().toISOString() }); }
async function call(scn: string, method: string, path: string, body?: unknown) {
  st.inserts.length = 0; st.userWrites.length = 0; vi.mocked(logger.error).mockClear(); vi.mocked(logger.warn).mockClear();
  const res = await fetch(base + path, { method, headers: body ? { 'Content-Type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined });
  const text = await res.text();
  const hdrs: Record<string, string> = {}; res.headers.forEach((v, k) => { if (!['date', 'etag', 'content-length', 'connection', 'keep-alive'].includes(k)) hdrs[k] = v; });
  const row = { scn, method, path, status: res.status, body: text.slice(0, 400), headers: hdrs, retryAfter: res.headers.get('retry-after'),
    inserts: st.inserts.map(p => [p[0], p[1], p[5]]), userWrites: JSON.parse(JSON.stringify(st.userWrites)),
    errorLogs: vi.mocked(logger.error).mock.calls.map(c => [c[0], Object.keys((c as any)[1] || {}).sort()]),
    warnLogs: vi.mocked(logger.warn).mock.calls.map(c => c[0]),
    pendingRowsForCaller: Array.from(st.table.values()).filter(r => r.user_id === st.caller.userId && r.status === 'PENDING').length };
  rows.push(row); return row;
}

describe('qa1015 drafter probe', () => {
  it('records', async () => {
    // S1 duplicate PENDING under an F-ver fault on the pending read, three infra forms + a non-infra control
    for (const [tag, mk] of [['ECONNREFUSED', ECONN], ['message-form', MSG], ['pg-53300', P53300], ['non-infra-42P01', NONINFRA]] as const) {
      const u = `s1${tag.length}${tag.charCodeAt(0)}-aaaa-4aaa-8aaa-aaaaaaaaaaaa`; user(u); pendingRow(`vr-s1-${tag}`, u);
      st.caller = { userId: u, role: 'USER', tenantId: 'tenant-default' };
      st.fault = { re: SEL_PENDING, err: mk() };
      await call(`S1 POST dup while PENDING exists, fault pending-read ${tag}`, 'POST', '/me/verification', { targetLevel: 'ENHANCED' });
      st.fault = null;
    }
    // S1-healthy control: the same shape without a fault refuses 400
    { const u = 's1hh-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; user(u); pendingRow('vr-s1-healthy', u); st.caller = { userId: u, role: 'USER', tenantId: 'tenant-default' };
      await call('S1 control healthy POST while PENDING exists', 'POST', '/me/verification', { targetLevel: 'ENHANCED' }); }
    // S2 STANDARD auto-approve (mfaEnabled) while a PENDING request exists, fault on the pending read
    { const u = 's2aa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; user(u, { mfaEnabled: true }); pendingRow('vr-s2', u);
      st.caller = { userId: u, role: 'USER', tenantId: 'tenant-default' }; st.fault = { re: SEL_PENDING, err: ECONN() };
      await call('S2 POST STANDARD auto-approve while PENDING exists, fault pending-read ECONNREFUSED', 'POST', '/me/verification', { targetLevel: 'STANDARD' }); st.fault = null; }
    // S3 review from a STALE in-memory copy: created healthy here, REJECTED by "another replica" in the table, then the by-id read faults
    { const u = 's3aa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; user(u); st.caller = { userId: u, role: 'USER', tenantId: 'tenant-default' };
      const created = await call('S3 setup healthy POST', 'POST', '/me/verification', { targetLevel: 'ENHANCED' });
      const rid = JSON.parse(created.body as string).data.requestId as string;
      const r = st.table.get(rid)!; st.table.set(rid, { ...r, status: 'REJECTED' });
      st.caller = { userId: 'adm0-aaaa-4aaa-8aaa-aaaaaaaaaaaa', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' };
      await call('S3 control healthy review of the REJECTED request', 'POST', `/verification/${rid}/review`, { action: 'approve' });
      st.fault = { re: SEL_ID, err: ECONN() };
      await call('S3 review approve, by-id read faults ECONNREFUSED, memory holds a stale PENDING copy', 'POST', `/verification/${rid}/review`, { action: 'approve' });
      st.fault = null; (rows[rows.length - 1] as any).tableStatusAfter = st.table.get(rid)!.status; }
    // S4 list under the fault vs healthy
    { const u = 's4aa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; user(u); pendingRow('vr-s4', u); st.caller = { userId: u, role: 'USER', tenantId: 'tenant-default' };
      await call('S4 GET list healthy', 'GET', '/me/verification');
      st.fault = { re: SEL_LIST, err: ECONN() }; await call('S4 GET list, fault ECONNREFUSED', 'GET', '/me/verification');
      st.fault = { re: SEL_LIST, err: NONINFRA() }; await call('S4 GET list, fault non-infra 42P01', 'GET', '/me/verification'); st.fault = null; }
    // S5 review not found, healthy and non-infra
    { st.caller = { userId: 'adm0-aaaa-4aaa-8aaa-aaaaaaaaaaaa', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' };
      await call('S5 review unknown id healthy', 'POST', '/verification/vr-none/review', { action: 'approve' });
      st.fault = { re: SEL_ID, err: NONINFRA() }; await call('S5 review unknown id, non-infra 42P01', 'POST', '/verification/vr-none/review', { action: 'approve' });
      st.fault = { re: SEL_ID, err: MSG() }; await call('S5 review unknown id, message-form infra', 'POST', '/verification/vr-none/review', { action: 'approve' }); st.fault = null; }
    // S6 the unchanged save: INSERT faults, then a healthy list
    { const u = 's6aa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; user(u); st.caller = { userId: u, role: 'USER', tenantId: 'tenant-default' };
      st.fault = { re: INSERT, err: ECONN() }; await call('S6 POST, INSERT faults ECONNREFUSED (saveVerificationRequest unchanged)', 'POST', '/me/verification', { targetLevel: 'ENHANCED' }); st.fault = null;
      await call('S6 then healthy GET list', 'GET', '/me/verification'); }
    expect(rows.length).toBeGreaterThan(10);
  });
});
