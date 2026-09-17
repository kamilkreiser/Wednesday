/**
 * qa1032 DRAFTER PROBE (not a product test; lives OUTSIDE services/auth — the #1018 round-2 gate's F-3).
 * The fail-closed census of every verification-request save path in services/auth routes/users.ts, run on the REAL userRoutes + the REAL
 * userRepo (updateUser / updateUserPlatformScope / getUserByIdPreAuth / getUserById) + the real errorHandler + the real isInfrastructureDbError,
 * over a stateful `db` stub (the ks1050 pattern) that keeps the users row and the verification_upgrade_requests rows, with a per-row FAULT PLAN:
 *   INSERT verification_upgrade_requests: ok | infra (ECONNREFUSED) | other (22001) | zero (rowCount 0, nothing stored)
 *   UPDATE users: ok | zero | infra | other      auth_find_user_by_id (pre-auth lookup): ok | infra
 *   the SELECT FROM users read-back AFTER an UPDATE landed: ok | infra | empty
 *   the list SELECT (GET /me/verification): ok | other (the memory fallback exposed)
 * Every row records status, body, the statement sequence, the stored request row, the stored level, and every logger.error (message + payload).
 * It ASSERTS NOTHING about the product; the runner compares develop vs head. __AUTH__ is substituted with the absolute services/auth path.
 */
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import { writeFileSync } from 'node:fs';
import express from 'express';

type Plan = { insert: string[]; update: string; preauth: string; readback: string; list: string; dbAvailable: boolean };
const TENANT = 'b1000000-0000-4000-8000-000000001032';
const state = vi.hoisted(() => ({
  caller: {} as Record<string, string>,
  userRow: {} as Record<string, unknown>,
  vrows: new Map<string, Record<string, unknown>>(),
  plan: { insert: [], update: 'ok', preauth: 'ok', readback: 'ok', list: 'ok', dbAvailable: true } as { insert: string[]; update: string; preauth: string; readback: string; list: string; dbAvailable: boolean },
  seq: [] as string[],
  updated: false,
}));
const log = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() }));
const ERR = vi.hoisted(() => ({
  infra: () => Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' }),
  other: () => Object.assign(new Error('value too long for type character varying(32)'), { code: '22001' }),
}));
vi.mock('__AUTH__/src/utils/logger', () => ({ logger: log, createLogger: () => log, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: log, createLogger: () => log }));
const TEST_DEK = vi.hoisted(() => Buffer.alloc(32, 7));
vi.mock('__AUTH__/src/services/subjectDeks', () => ({ subjectDeks: { getDek: vi.fn(async () => TEST_DEK), getOrCreateDek: vi.fn(async () => TEST_DEK) } }));
vi.mock('__AUTH__/src/db', () => ({
  isDbAvailable: () => state.plan.dbAvailable,
  getPool: () => ({}),
  query: vi.fn(async (sql: string, params: unknown[] = []) => {
    if (/INSERT INTO verification_upgrade_requests/.test(sql)) {
      const mode = state.plan.insert.length ? String(state.plan.insert.shift()) : 'ok';
      state.seq.push('INSERT:' + String(params[5]) + ':' + mode);
      if (mode === 'infra') throw ERR.infra();
      if (mode === 'other') throw ERR.other();
      if (mode === 'zero') return { rows: [], rowCount: 0 };
      state.vrows.set(String(params[0]), { id: params[0], user_id: params[1], current_level: params[2], target_level: params[3], documents: params[4], status: params[5], submitted_at: params[6], reviewed_at: params[7], reviewed_by: params[8], rejection_reason: params[9] });
      return { rows: [], rowCount: 1 };
    }
    if (/FROM verification_upgrade_requests WHERE user_id = \$1 AND status = 'PENDING'/.test(sql)) {
      return { rows: [...state.vrows.values()].filter((r) => r.user_id === params[0] && r.status === 'PENDING').slice(0, 1) };
    }
    if (/FROM verification_upgrade_requests WHERE id = \$1/.test(sql)) return { rows: state.vrows.has(String(params[0])) ? [state.vrows.get(String(params[0]))] : [] };
    if (/FROM verification_upgrade_requests WHERE user_id = \$1 ORDER BY/.test(sql)) {
      if (state.plan.list === 'other') throw ERR.other();
      return { rows: [...state.vrows.values()].filter((r) => r.user_id === params[0]) };
    }
    if (/auth_find_user_by_id/.test(sql)) {
      state.seq.push('PREAUTH:' + state.plan.preauth);
      if (state.plan.preauth === 'infra') throw ERR.infra();
      return { rows: [{ ...state.userRow }], rowCount: 1 };
    }
    const upd = /^\s*UPDATE\s+users\s+SET\s+(.*)\s+WHERE\s+id\s*=\s*\$\d+\s*$/is.exec(sql);
    if (upd) {
      state.seq.push('UPDATE_USERS:' + state.plan.update);
      if (state.plan.update === 'infra') throw ERR.infra();
      if (state.plan.update === 'other') throw ERR.other();
      if (state.plan.update === 'zero') return { rows: [], rowCount: 0 };
      for (const clause of upd[1].split(/,\s*/)) {
        const m = /^(\w+)\s*=\s*(?:\$(\d+)|NOW\(\))$/.exec(clause.trim());
        if (m) state.userRow[m[1]] = m[2] ? params[Number(m[2]) - 1] : new Date();
      }
      state.updated = true;
      return { rows: [], rowCount: 1 };
    }
    if (/FROM\s+users\s+WHERE\s+id/i.test(sql)) {
      if (state.updated) {
        state.seq.push('READBACK:' + state.plan.readback);
        if (state.plan.readback === 'infra') throw ERR.infra();
        if (state.plan.readback === 'empty') return { rows: [], rowCount: 0 };
      }
      return { rows: [{ ...state.userRow }], rowCount: 1 };
    }
    state.seq.push('UNMATCHED:' + sql.replace(/\s+/g, ' ').slice(0, 60));
    return { rows: [], rowCount: 0 };
  }),
}));
vi.mock('__AUTH__/src/middleware/authenticate', async () => {
  const { runWithTenantId } = await import('@secuura/shared');
  const inject = () => (req: express.Request & { user?: unknown }, _res: express.Response, next: express.NextFunction) => {
    (req as { user: unknown }).user = { ...state.caller };
    runWithTenantId(state.caller.tenantId, () => next());
  };
  return { authenticate: inject, authenticateAccessOrConnector: inject };
});
vi.mock('__AUTH__/src/services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
vi.mock('__AUTH__/src/services/password', () => ({ hashPassword: vi.fn(async () => 'hashed'), checkPasswordStrength: vi.fn(() => ({ ok: true })), verifyPassword: vi.fn(async () => true) }));

import { userRoutes } from '__AUTH__/src/routes/users';
import { errorHandler } from '__AUTH__/src/middleware/errorHandler';

let server: ReturnType<ReturnType<typeof express>['listen']>;
let base = '';
const ROWS: Array<Record<string, unknown>> = [];
beforeAll(async () => {
  const app = express(); app.use(express.json()); app.use('/', userRoutes); app.use(errorHandler);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port); r(); }); });
});
afterAll(async () => {
  await new Promise<void>((r) => server.close(() => r()));
  writeFileSync(String(process.env.QA1032_ROWS_OUT), JSON.stringify(ROWS, null, 1));
});

let n = 0;
function uid(): string { n += 1; return 'c1000000-0000-4000-8000-' + String(1032000000 + n).padStart(12, '0'); }
function seedUser(id: string, mfa: boolean): void {
  state.userRow = {
    id, email: 'qa1032-' + String(n) + '@example.test', first_name: 'Q', last_name: 'A', display_name: null, role: 'user', status: 'active', email_verified: true,
    phone_number: null, phone_verified: false, mfa_enabled: mfa, mfa_secret: null, mfa_backup_codes: null, verification_level: 'basic', organization_id: null,
    tenant_id: TENANT, tenant_slug: null, wallet_address: null, auth_method: 'password', external_provider: null, external_id: null, google_id: null, linkedin_id: null,
    facebook_id: null, apple_id: null, github_id: null, microsoft_personal_id: null, metadata: null, created_at: new Date(), updated_at: new Date(), last_login_at: null,
  };
}
function reset(p: Partial<Plan>): void {
  state.vrows.clear(); state.seq = []; state.updated = false; log.error.mockClear();
  state.plan = { insert: [], update: 'ok', preauth: 'ok', readback: 'ok', list: 'ok', dbAvailable: true, ...p };
}
async function call(method: string, path: string, body?: unknown): Promise<{ status: number; json: Record<string, any> }> {
  const res = await fetch(base + path, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  const t = await res.text(); let j: Record<string, any> = {}; try { j = JSON.parse(t); } catch { j = { raw: t.slice(0, 120) }; }
  return { status: res.status, json: j };
}
function record(id: string, route: string, plan: Partial<Plan>, r: { status: number; json: Record<string, any> }, extra: Record<string, unknown> = {}): void {
  const reqRow = [...state.vrows.values()][0] || null;
  ROWS.push({
    id, route, plan, status: r.status, success: r.json.success, code: r.json.error?.code ?? null, message: String(r.json.message ?? r.json.error?.message ?? '').slice(0, 140),
    dataStatus: r.json.data?.status ?? null, seq: [...state.seq], requestRow: reqRow ? { status: reqRow.status, reviewed_by: reqRow.reviewed_by ?? null, reviewed_at: reqRow.reviewed_at ? 'set' : null } : null,
    requestRows: state.vrows.size, level: state.userRow.verification_level,
    errorLogs: (log.error.mock.calls as unknown as Array<[string, Record<string, unknown>]>).map(([m, p]) => ({ msg: String(m).slice(0, 170), keys: Object.keys(p || {}).sort(), requestId: p?.requestId ?? null })),
    ...extra,
  });
}
const USER = (id: string) => { state.caller = { userId: id, role: 'USER', tenantId: TENANT }; };
const ADMIN = (role = 'SYSTEM_ADMIN') => { state.caller = { userId: 'a1000000-0000-4000-8000-000000001032', role, tenantId: TENANT }; };
function pending(rid: string, userId: string): void {
  state.vrows.set(rid, { id: rid, user_id: userId, current_level: 'BASIC', target_level: 'ENHANCED', documents: [], status: 'PENDING', submitted_at: '2026-09-17T00:00:00.000Z', reviewed_at: null, reviewed_by: null, rejection_reason: null });
}

const SUBMIT: Array<[string, Partial<Plan>]> = [
  ['S-OK', {}], ['S-INFRA', { insert: ['infra'] }], ['S-OTHER', { insert: ['other'] }], ['S-ZERO', { insert: ['zero'] }], ['S-NODB', { dbAvailable: false }],
];
const MFA: Array<[string, Partial<Plan>]> = [
  ['M-OK', {}], ['M-UPD-ZERO', { update: 'zero' }], ['M-UPD-INFRA', { update: 'infra' }], ['M-UPD-OTHER', { update: 'other' }], ['M-READBACK-INFRA', { readback: 'infra' }], ['M-READBACK-EMPTY', { readback: 'empty' }],
];
const APPROVE: Array<[string, Partial<Plan>, string?]> = [
  ['A-OK', {}], ['A-OK-ORGADMIN', {}, 'ORG_ADMIN'], ['A-SAVE-INFRA', { insert: ['infra'] }], ['A-SAVE-OTHER', { insert: ['other'] }], ['A-SAVE-ZERO', { insert: ['zero'] }],
  ['A-UPD-ZERO', { update: 'zero' }], ['A-UPD-INFRA', { update: 'infra' }], ['A-UPD-OTHER', { update: 'other' }], ['A-PREAUTH-INFRA', { preauth: 'infra' }],
  ['A-READBACK-INFRA', { readback: 'infra' }], ['A-READBACK-EMPTY', { readback: 'empty' }],
  ['A-DOUBLE', { update: 'zero', insert: ['ok', 'infra'] }], ['A-DOUBLE-OTHER', { update: 'zero', insert: ['ok', 'other'] }], ['A-RESTORE-ZERO', { update: 'zero', insert: ['ok', 'zero'] }],
  ['A-DOUBLE-READBACK', { readback: 'infra', insert: ['ok', 'infra'] }],
];
const REJECT: Array<[string, Partial<Plan>]> = [['R-OK', {}], ['R-SAVE-INFRA', { insert: ['infra'] }], ['R-SAVE-OTHER', { insert: ['other'] }], ['R-SAVE-ZERO', { insert: ['zero'] }]];

describe('qa1032 drafter probe', () => {
  for (const [id, plan] of SUBMIT) it(id, async () => {
    const u = uid(); seedUser(u, false); reset(plan); USER(u);
    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
    record(id, 'POST /me/verification', plan, r);
  });
  it('S-INFRA-THEN-LIST-MEMORY', async () => {
    const u = uid(); seedUser(u, false); reset({ insert: ['infra'] }); USER(u);
    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
    state.plan.list = 'other';
    const g = await call('GET', '/me/verification');
    record('S-INFRA-THEN-LIST-MEMORY', 'POST then GET /me/verification (list falls back to memory)', { insert: ['infra'], list: 'other' }, r, { listStatus: g.status, listedFromMemory: (g.json.data?.requests || []).length });
  });
  for (const [id, plan] of MFA) it(id, async () => {
    const u = uid(); seedUser(u, true); reset(plan); USER(u);
    const r = await call('POST', '/me/verification', { targetLevel: 'STANDARD' });
    record(id, 'POST /me/verification MFA auto-approve (STANDARD, mfa_enabled)', plan, r);
  });
  for (const [id, plan, role] of APPROVE) it(id, async () => {
    const u = uid(); seedUser(u, false); reset(plan); ADMIN(role); const rid = 'vr-qa1032-' + id; pending(rid, u);
    const r = await call('POST', '/verification/' + rid + '/review', { action: 'approve' });
    record(id, 'POST /verification/:id/review approve (' + (role || 'SYSTEM_ADMIN') + ')', plan, r);
  });
  for (const [id, plan] of REJECT) it(id, async () => {
    const u = uid(); seedUser(u, false); reset(plan); ADMIN(); const rid = 'vr-qa1032-' + id; pending(rid, u);
    const r = await call('POST', '/verification/' + rid + '/review', { action: 'reject', reason: 'qa' });
    record(id, 'POST /verification/:id/review reject', plan, r);
  });
});
