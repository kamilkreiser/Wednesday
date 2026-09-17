/**
 * qa1032r2 DRAFTER PROBE (not a product test; lives OUTSIDE services/auth at <tree>/Blockchain/Dev/qa_probe_1032r2/, the #1018 round-2 gate's F-3).
 * ROUND 2 of #1032: the approve's re-read branches, on the REAL userRoutes + REAL userRepo (updateUser / updateUserPlatformScope / getUserByIdPreAuth /
 * getUserById / getUserByIdPlatformScope) + REAL errorHandler + REAL isInfrastructureDbError, over a stateful `db` stub (the ks1050 pattern).
 * Derived from ../2026-09-17_gate1032/src/qa1032-drafter-probe.template.ts and the round-1 QA probe (pool-timeout shape, warn capture, follow-ups).
 * NEW here:
 *   - every `SELECT … FROM users WHERE id` is CLASSIFIED by what the product passed and the scope it ran under: `readback` = updateUser's trailing read
 *     (an explicit tenantId argument), `reread` = the approve's platform-scope level read (no tenantId argument, platform scope, after the APPROVED save);
 *     each class consumes its own plan queue: ok | pooltimeout | infra | other | empty | stale (answers the row with the PRE-approve level: a copy that
 *     did not see the UPDATE, i.e. another pool / database);
 *   - the pre-auth lookup and the UPDATE take pooltimeout; the UPDATE also takes `landed-throw` (the UPDATE is applied, then the statement throws
 *     `Connection terminated unexpectedly`: committed, acknowledgement lost);
 *   - every statement records the query() tenantId argument and the ALS scope (platform | tenant:<id> | none): the pool-routing INPUTS;
 *   - PII columns are seeded as subject-DEK ciphertext, so NODE_ENV=production (B-10 plaintext cutoff) reads them like a real row.
 * It ASSERTS NOTHING about the product. __AUTH__ = the absolute services/auth path. Rows go to $QA1032R2_ROWS_OUT.
 */
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import { writeFileSync } from 'node:fs';
import express from 'express';

type Plan = { insert: string[]; preauth: string; update: string; readback: string[]; reread: string[]; list: string; startLevel: string };
const TENANT = 'b1000000-0000-4000-8000-000000001032';
const state = vi.hoisted(() => ({
  caller: {} as Record<string, string>,
  userRow: {} as Record<string, unknown>,
  preLevel: 'basic' as string,
  vrows: new Map<string, Record<string, unknown>>(),
  plan: {} as { insert: string[]; preauth: string; update: string; readback: string[]; reread: string[]; list: string; startLevel: string },
  seq: [] as string[],
  approvedSaved: false,
}));
const log = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() }));
const ERR = vi.hoisted(() => ({
  infra: () => Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' }),
  pooltimeout: () => new Error('timeout exceeded when trying to connect'),
  other: () => Object.assign(new Error('value too long for type character varying(32)'), { code: '22001' }),
  terminated: () => new Error('Connection terminated unexpectedly'),
}));
function fault(mode: string): Error | null {
  if (mode === 'infra') return ERR.infra();
  if (mode === 'pooltimeout') return ERR.pooltimeout();
  if (mode === 'other') return ERR.other();
  return null;
}
vi.mock('__AUTH__/src/utils/logger', () => ({ logger: log, createLogger: () => log, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: log, createLogger: () => log }));
const TEST_DEK = vi.hoisted(() => Buffer.alloc(32, 7));
vi.mock('__AUTH__/src/services/subjectDeks', () => ({ subjectDeks: { getDek: vi.fn(async () => TEST_DEK), getOrCreateDek: vi.fn(async () => TEST_DEK) } }));
vi.mock('__AUTH__/src/db', async () => {
  const shared = await import('@secuura/shared');
  const scope = () => (shared.isPlatformScope() ? 'platform' : shared.currentTenantId() ? 'tenant:' + String(shared.currentTenantId()).slice(-4) : 'none');
  const tag = (name: string, tenantArg: unknown, mode: string) => state.seq.push(name + ':' + mode + '[arg=' + (tenantArg ? String(tenantArg).slice(-4) : '-') + ',als=' + scope() + ']');
  return {
    isDbAvailable: () => true,
    getPool: () => ({}),
    query: vi.fn(async (sql: string, params: unknown[] = [], tenantArg?: string) => {
      if (/INSERT INTO verification_upgrade_requests/.test(sql)) {
        const mode = state.plan.insert.length ? String(state.plan.insert.shift()) : 'ok';
        tag('INSERT:' + String(params[5]), tenantArg, mode);
        const f = fault(mode); if (f) throw f;
        state.vrows.set(String(params[0]), { id: params[0], user_id: params[1], current_level: params[2], target_level: params[3], documents: params[4], status: params[5], submitted_at: params[6], reviewed_at: params[7], reviewed_by: params[8], rejection_reason: params[9] });
        if (params[5] === 'APPROVED') state.approvedSaved = true;
        return { rows: [], rowCount: 1 };
      }
      if (/FROM verification_upgrade_requests WHERE user_id = \$1 AND status = 'PENDING'/.test(sql)) {
        return { rows: [...state.vrows.values()].filter((r) => r.user_id === params[0] && r.status === 'PENDING').slice(0, 1) };
      }
      if (/FROM verification_upgrade_requests WHERE id = \$1/.test(sql)) return { rows: state.vrows.has(String(params[0])) ? [{ ...state.vrows.get(String(params[0])) }] : [] };
      if (/FROM verification_upgrade_requests WHERE user_id = \$1 ORDER BY/.test(sql)) {
        if (state.plan.list === 'other') throw ERR.other();
        return { rows: [...state.vrows.values()].filter((r) => r.user_id === params[0]).map((r) => ({ ...r })) };
      }
      if (/auth_find_user_by_id/.test(sql)) {
        tag('PREAUTH', tenantArg, state.plan.preauth);
        const f = fault(state.plan.preauth); if (f) throw f;
        return { rows: [{ ...state.userRow }], rowCount: 1 };
      }
      const upd = /^\s*UPDATE\s+users\s+SET\s+(.*)\s+WHERE\s+id\s*=\s*\$\d+\s*$/is.exec(sql);
      if (upd) {
        tag('UPDATE_USERS', tenantArg, state.plan.update);
        const f = fault(state.plan.update); if (f) throw f;
        if (state.plan.update === 'zero') return { rows: [], rowCount: 0 };
        for (const clause of upd[1].split(/,\s*/)) {
          const m = /^(\w+)\s*=\s*(?:\$(\d+)|NOW\(\))$/.exec(clause.trim());
          if (m) state.userRow[m[1]] = m[2] ? params[Number(m[2]) - 1] : new Date();
        }
        if (state.plan.update === 'landed-throw') throw ERR.terminated();
        return { rows: [], rowCount: 1 };
      }
      if (/FROM\s+users\s+WHERE\s+id/i.test(sql)) {
        const platform = shared.isPlatformScope();
        const cls = tenantArg ? 'readback' : (platform && state.approvedSaved ? 'reread' : 'other');
        const queue = cls === 'readback' ? state.plan.readback : cls === 'reread' ? state.plan.reread : [];
        const mode = queue.length ? String(queue.shift()) : 'ok';
        tag('READ_USERS:' + cls, tenantArg, mode);
        const f = fault(mode); if (f) throw f;
        if (mode === 'empty') return { rows: [], rowCount: 0 };
        if (mode === 'stale') return { rows: [{ ...state.userRow, verification_level: state.preLevel }], rowCount: 1 };
        return { rows: [{ ...state.userRow }], rowCount: 1 };
      }
      tag('UNMATCHED:' + sql.replace(/\s+/g, ' ').slice(0, 50), tenantArg, '-');
      return { rows: [], rowCount: 0 };
    }),
  };
});
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

import { encryptFieldWithDek } from '@secuura/shared';
import { userRoutes } from '__AUTH__/src/routes/users';
import { errorHandler } from '__AUTH__/src/middleware/errorHandler';

let server: ReturnType<ReturnType<typeof express>['listen']>;
let base = '';
const ROWS: Array<Record<string, unknown>> = [];
beforeAll(async () => {
  const app = express(); app.use(express.json()); app.use('/', userRoutes); app.use(errorHandler);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port); r(); }); });
  writeFileSync(String(process.env.QA1032R2_ROWS_OUT) + '.listen', JSON.stringify({ pid: process.pid, base, cwd: process.cwd(), nodeEnv: process.env.NODE_ENV }));
});
afterAll(async () => {
  await new Promise<void>((r) => server.close(() => r()));
  writeFileSync(String(process.env.QA1032R2_ROWS_OUT), JSON.stringify({ nodeEnv: process.env.NODE_ENV, rows: ROWS }, null, 1));
});

let n = 0;
function uid(): string { n += 1; return 'c1000000-0000-4000-8000-' + String(1032200000 + n).padStart(12, '0'); }
const enc = (v: string, col: string, id: string) => encryptFieldWithDek(v, 'users.' + col + '.' + id, TEST_DEK) as string;
function seedUser(id: string, level: string): void {
  state.preLevel = level;
  state.userRow = {
    id, email: enc('qa1032r2-' + String(n) + '@example.test', 'email', id), first_name: enc('Q', 'first_name', id), last_name: enc('A', 'last_name', id), display_name: null,
    role: 'user', status: 'active', email_verified: true, phone_number: null, phone_verified: false, mfa_enabled: false, mfa_secret: null, mfa_backup_codes: null,
    verification_level: level, organization_id: null, tenant_id: TENANT, tenant_slug: null, wallet_address: null, auth_method: 'password', external_provider: null,
    external_id: null, google_id: null, linkedin_id: null, facebook_id: null, apple_id: null, github_id: null, microsoft_personal_id: null, metadata: null,
    created_at: new Date(), updated_at: new Date(), last_login_at: null,
  };
}
function reset(p: Partial<Plan>): void {
  state.vrows.clear(); state.seq = []; state.approvedSaved = false; log.error.mockClear(); log.warn.mockClear();
  state.plan = { insert: [...(p.insert || [])], preauth: p.preauth || 'ok', update: p.update || 'ok', readback: [...(p.readback || [])], reread: [...(p.reread || [])], list: p.list || 'ok', startLevel: p.startLevel || 'basic' };
}
/** keep the stored rows + level; clear faults, sequence and logs for the next step */
function heal(): void {
  state.seq = []; state.approvedSaved = false; log.error.mockClear(); log.warn.mockClear();
  state.plan = { insert: [], preauth: 'ok', update: 'ok', readback: [], reread: [], list: 'ok', startLevel: state.plan.startLevel };
  state.preLevel = String(state.userRow.verification_level);
}
async function call(method: string, path: string, body?: unknown): Promise<{ status: number; json: Record<string, any> }> {
  const res = await fetch(base + path, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  const t = await res.text(); let j: Record<string, any> = {}; try { j = JSON.parse(t); } catch { j = { raw: t.slice(0, 120) }; }
  return { status: res.status, json: j };
}
const USER = (id: string) => { state.caller = { userId: id, role: 'USER', tenantId: TENANT }; };
const ADMIN = (role = 'SYSTEM_ADMIN') => { state.caller = { userId: 'a1000000-0000-4000-8000-000000001032', role, tenantId: TENANT }; };
const isProductLine = (m: string) => !/^DB |^Error occurred/.test(m);
function snapshot(r: { status: number; json: Record<string, any> }, rid: string): Record<string, unknown> {
  const row = state.vrows.get(rid) || null;
  const lines = (fn: any) => (fn.mock.calls as unknown as Array<[string, Record<string, unknown>]>).map(([m, p]) => ({ msg: String(m).slice(0, 170), keys: Object.keys(p || {}).sort(), requestId: p?.requestId ?? null, userId: p?.userId ?? null, targetLevel: p?.targetLevel ?? null, levelNow: p?.levelNow ?? null }));
  return {
    status: r.status, code: r.json.error?.code ?? null, message: String(r.json.message ?? r.json.error?.message ?? '').slice(0, 120), dataStatus: r.json.data?.status ?? null,
    requestRow: row ? { status: row.status, reviewed_by: row.reviewed_by ? 'set' : null, reviewed_at: row.reviewed_at ? 'set' : null } : null,
    level: state.userRow.verification_level, seq: [...state.seq],
    errorLines: lines(log.error).filter((l) => isProductLine(l.msg)), warnLines: lines(log.warn).filter((l) => isProductLine(l.msg) && !/plaintext/.test(l.msg)),
    classifierLines: lines(log.error).filter((l) => !isProductLine(l.msg)).map((l) => l.msg.slice(0, 40)),
  };
}
function pending(rid: string, userId: string): void {
  state.vrows.set(rid, { id: rid, user_id: userId, current_level: 'BASIC', target_level: 'ENHANCED', documents: [], status: 'PENDING', submitted_at: '2026-09-18T00:00:00.000Z', reviewed_at: null, reviewed_by: null, rejection_reason: null });
}

// [id, plan, expected branch at head (drafter's READ of the head approve block), role?]
const APPROVE: Array<[string, Partial<Plan>, string, string?]> = [
  ['B-OK', {}, 'ok'],
  ['B-OK-ORGADMIN', {}, 'ok', 'ORG_ADMIN'],
  // the level reads the TARGET: the raise landed, acknowledgement lost
  ['T-READBACK-POOLTIMEOUT', { readback: ['pooltimeout'] }, 'target'],
  ['T-READBACK-POOLTIMEOUT-ORGADMIN', { readback: ['pooltimeout'] }, 'target', 'ORG_ADMIN'],
  ['T-READBACK-INFRA', { readback: ['infra'] }, 'target'],
  ['T-READBACK-OTHER', { readback: ['other'] }, 'target'],
  ['T-READBACK-EMPTY', { readback: ['empty'] }, 'target'],
  ['T-UPD-LANDED-THROW', { update: 'landed-throw' }, 'target'],
  ['T-ALREADY-TARGET-UPD-ZERO', { startLevel: 'enhanced', update: 'zero' }, 'target (level was already the target before this approve)'],
  // the level reads ANOTHER level: this approve did not raise it
  ['O-UPD-ZERO', { update: 'zero' }, 'other'],
  ['O-UPD-POOLTIMEOUT', { update: 'pooltimeout' }, 'other'],
  ['O-UPD-OTHER', { update: 'other' }, 'other'],
  ['O-PREAUTH-POOLTIMEOUT', { preauth: 'pooltimeout' }, 'other'],
  ['O-HIGHER-LEVEL-UPD-ZERO', { startLevel: 'high', update: 'zero' }, 'other (the level reads ABOVE the target)'],
  ['O-READBACK-POOLTIMEOUT-REREAD-STALE', { readback: ['pooltimeout'], reread: ['stale'] }, 'other: the re-read sees a copy WITHOUT the landed UPDATE (another pool / DB)'],
  // STATED RESIDUAL (i): another-level read AND a failed PENDING restore
  ['RI-UPD-ZERO-RESTORE-POOLTIMEOUT', { update: 'zero', insert: ['ok', 'pooltimeout'] }, 'residual (i)'],
  ['RI-PREAUTH-POOLTIMEOUT-RESTORE-POOLTIMEOUT', { preauth: 'pooltimeout', insert: ['ok', 'pooltimeout'] }, 'residual (i) by pool starvation: preauth fails, re-read succeeds, restore fails'],
  ['RI-STALE-RESTORE-POOLTIMEOUT', { readback: ['pooltimeout'], reread: ['stale'], insert: ['ok', 'pooltimeout'] }, 'residual (i) with the level actually RAISED'],
  // UNREADABLE (stated residual (ii))
  ['U-LANDED-READBACK-POOLTIMEOUT-REREAD-POOLTIMEOUT', { readback: ['pooltimeout'], reread: ['pooltimeout'] }, 'unreadable, raise LANDED'],
  ['U-LANDED-READBACK-EMPTY-REREAD-EMPTY', { readback: ['empty'], reread: ['empty'] }, 'unreadable (no row), raise LANDED'],
  ['U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT', { preauth: 'pooltimeout', reread: ['pooltimeout'] }, 'residual (ii): unreadable, raise did NOT land'],
  ['U-NOTLANDED-UPD-POOLTIMEOUT-REREAD-POOLTIMEOUT', { update: 'pooltimeout', reread: ['pooltimeout'] }, 'residual (ii): unreadable, raise did NOT land'],
  ['U-NOTLANDED-UPD-ZERO-REREAD-INFRA', { update: 'zero', reread: ['infra'] }, 'residual (ii): unreadable, 0-row UPDATE'],
  ['U-NOTLANDED-UPD-OTHER-REREAD-OTHER', { update: 'other', reread: ['other'] }, 'residual (ii): unreadable, non-infra both'],
  // save refused before any level write (round-1 CLOSED instances, kept as controls)
  ['C-SAVE-POOLTIMEOUT', { insert: ['pooltimeout'] }, 'save refused 503, level untouched'],
  ['C-SAVE-OTHER', { insert: ['other'] }, 'save refused 500, level untouched'],
];
const FOLLOW: Array<[string, string]> = [
  ['T-READBACK-POOLTIMEOUT', 'ADMIN-REJECT'],
  ['T-READBACK-POOLTIMEOUT', 'ADMIN-RETRY-APPROVE'],
  ['O-READBACK-POOLTIMEOUT-REREAD-STALE', 'ADMIN-REJECT'],
  ['O-READBACK-POOLTIMEOUT-REREAD-STALE', 'SUBJECT-GET'],
  ['RI-UPD-ZERO-RESTORE-POOLTIMEOUT', 'ADMIN-RETRY-APPROVE'],
  ['RI-UPD-ZERO-RESTORE-POOLTIMEOUT', 'SUBJECT-GET'],
  ['RI-UPD-ZERO-RESTORE-POOLTIMEOUT', 'SUBJECT-RESUBMIT-THEN-ADMIN-APPROVE'],
  ['U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'ADMIN-RETRY-APPROVE'],
  ['U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'ADMIN-REJECT'],
  ['U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'SUBJECT-GET'],
  ['U-NOTLANDED-PREAUTH-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'SUBJECT-RESUBMIT-THEN-ADMIN-APPROVE'],
  ['U-LANDED-READBACK-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'ADMIN-RETRY-APPROVE'],
  ['U-LANDED-READBACK-POOLTIMEOUT-REREAD-POOLTIMEOUT', 'SUBJECT-GET'],
];

describe('qa1032r2 drafter probe', () => {
  for (const [id, plan, expect, role] of APPROVE) it(id, async () => {
    const u = uid(); seedUser(u, plan.startLevel || 'basic'); reset(plan); ADMIN(role); const rid = 'vr-qa1032r2-' + id; pending(rid, u);
    const r = await call('POST', '/verification/' + rid + '/review', { action: 'approve' });
    ROWS.push({ id, kind: 'approve', role: role || 'SYSTEM_ADMIN', plan, expect, ...snapshot(r, rid) });
  });
  for (const [start, move] of FOLLOW) it('FU ' + start + ' -> ' + move, async () => {
    const [, plan] = APPROVE.find((a) => a[0] === start)!;
    const u = uid(); seedUser(u, plan.startLevel || 'basic'); reset(plan); ADMIN(); const rid = 'vr-qa1032r2-fu-' + start + move; pending(rid, u);
    const r0 = await call('POST', '/verification/' + rid + '/review', { action: 'approve' });
    const s0 = snapshot(r0, rid);
    heal();
    const steps: Array<Record<string, unknown>> = [];
    if (move === 'ADMIN-REJECT') { ADMIN(); const r = await call('POST', '/verification/' + rid + '/review', { action: 'reject', reason: 'qa' }); steps.push({ step: 'reject', ...snapshot(r, rid) }); }
    if (move === 'ADMIN-RETRY-APPROVE') { ADMIN(); const r = await call('POST', '/verification/' + rid + '/review', { action: 'approve' }); steps.push({ step: 'retry approve', ...snapshot(r, rid) }); }
    if (move === 'SUBJECT-GET') { USER(u); const r = await call('GET', '/me/verification'); steps.push({ step: 'subject GET', status: r.status, currentLevel: r.json.data?.currentLevel ?? null, requests: (r.json.data?.requests || []).map((x: any) => x.status) }); }
    if (move === 'SUBJECT-RESUBMIT-THEN-ADMIN-APPROVE') {
      USER(u); const s = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
      const newId = s.json.data?.requestId ?? s.json.data?.id ?? null;
      steps.push({ step: 'subject resubmit ENHANCED', status: s.status, code: s.json.error?.code ?? null, message: String(s.json.message ?? s.json.error?.message ?? '').slice(0, 100), dataStatus: s.json.data?.status ?? null, newRequestId: newId ? 'set' : null, rows: state.vrows.size });
      if (newId) { heal(); ADMIN(); const a = await call('POST', '/verification/' + String(newId) + '/review', { action: 'approve' }); steps.push({ step: 'admin approves the new request', ...snapshot(a, String(newId)) }); }
    }
    ROWS.push({ id: 'FU ' + start + ' -> ' + move, kind: 'follow-up', first: { status: s0.status, message: s0.message, requestRow: s0.requestRow, level: s0.level }, steps });
  });
});
