/**
 * qa1032r2 DRAFTER POOL-ROUTING PROBE (not a product test; lives OUTSIDE services/auth at <tree>/Blockchain/Dev/qa_probe_1032r2/).
 * QUESTION (brief lead 3): under multi-tenancy, does the approve's platform-scope level re-read (`getUserByIdPlatformScope`) read the SAME row the
 * level UPDATE wrote (`updateUser` -> `query(…, tenantForRls)` -> `tenantManager.getPool(tenantId)`)?
 * HARNESS: the REAL services/auth `db.ts` (query / initDb / initTenantManager / getTenantManager), the REAL shared `TenantPoolManager.getPool`, the REAL
 * `queryWithTenantGuc` + `runWithTenantId` + `runWithPlatformScope`, the REAL userRoutes + userRepo + errorHandler. Only `pg` is faked:
 *   - `vi.mock('pg')` supplies db.ts's own pool (a FakePool on database `secuura`);
 *   - the TenantPoolManager is constructed by the product (native require of @secuura/shared; its platform URL points at 127.0.0.1:1, so its first config
 *     refresh fails and is swallowed), then its `defaultPool` / `platformPool` fields are swapped for FakePools and its tenant config set per ARM;
 *   - every FakePool statement records: pool label, database, the GUC in force on that connection (none | tenant | platform), rows affected;
 *   - databases are Maps (`secuura`, `secuura_t1032`); `users` optionally enforces the fail-closed RLS model (rows visible only with a matching tenant GUC
 *     or the platform GUC; `auth_find_user_by_id` is SECURITY DEFINER and always sees the row); `verification_upgrade_requests` has no RLS (migration READ).
 * ARMS: S = MULTI_TENANCY off (no tenant manager) · M1 = on, PROVISION_PER_TENANT_DB off (every tenant -> the manager's default pool) · M2 = on, per-tenant
 * DB on and the subject's tenant configured with a DISTINCT database. Each arm x RLS model {on, off} x fault {none, readback pooltimeout on the UPDATE's pool}.
 * It ASSERTS NOTHING about the product. __AUTH__ = the absolute services/auth path. Rows go to $QA1032R2_ROWS_OUT.
 */
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import { writeFileSync } from 'node:fs';
import express from 'express';

const TENANT = 'b1000000-0000-4000-8000-000000001032';
const W = vi.hoisted(() => {
  type Row = Record<string, unknown>;
  const dbs: Record<string, { users: Map<string, Row>; vrows: Map<string, Row> }> = {};
  const db = (name: string) => (dbs[name] ||= { users: new Map(), vrows: new Map() });
  const st = { rls: true, seq: [] as string[], faults: [] as Array<{ pool: string; match: RegExp; err: string; used?: boolean }>, tenantRows: [] as Row[] };
  const guc = (text: string, values: unknown[]) => (/app\.tenant_scope_bypass/.test(text) ? 'platform' : /app\.current_tenant_id/.test(text) ? 'tenant:' + String(values[0]).slice(-4) : null);
  function exec(label: string, dbName: string, gucNow: string, text: string, params: unknown[] = []): { rows: Row[]; rowCount: number } {
    const d = db(dbName); const sql = text.replace(/\s+/g, ' ').trim();
    const f = st.faults.find((x) => !x.used && (x.pool === label || x.pool === '*') && x.match.test(sql));
    const visible = (u: Row) => !st.rls || gucNow === 'platform' || gucNow === 'tenant:' + String(u.tenant_id).slice(-4);
    const rec = (what: string, rows: number) => st.seq.push(`${what}@${label}/${dbName}[guc=${gucNow}] rows=${rows}`);
    if (f) { f.used = true; rec('FAULT(' + f.err + ') ' + sql.slice(0, 40), 0); throw new Error(f.err); }
    if (/^SELECT 1 AS ok/.test(sql)) return { rows: [{ ok: 1 }], rowCount: 1 };
    if (/has_schema_privilege/.test(sql)) return { rows: [{ ok: false }], rowCount: 1 };
    if (/FROM tenants t/.test(sql)) return { rows: st.tenantRows, rowCount: st.tenantRows.length };
    if (/^(BEGIN|COMMIT|ROLLBACK)$/.test(sql) || /set_config/.test(sql)) return { rows: [], rowCount: 0 };
    if (/INSERT INTO verification_upgrade_requests/.test(sql)) {
      d.vrows.set(String(params[0]), { id: params[0], user_id: params[1], current_level: params[2], target_level: params[3], documents: params[4], status: params[5], submitted_at: params[6], reviewed_at: params[7], reviewed_by: params[8], rejection_reason: params[9] });
      rec('INSERT:' + String(params[5]), 1); return { rows: [], rowCount: 1 };
    }
    if (/FROM verification_upgrade_requests WHERE id = \$1/.test(sql)) { const r = d.vrows.get(String(params[0])); return { rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 }; }
    if (/FROM verification_upgrade_requests WHERE user_id = \$1/.test(sql)) { const rs = [...d.vrows.values()].filter((r) => r.user_id === params[0] && (!/PENDING/.test(sql) || r.status === 'PENDING')); return { rows: rs.map((r) => ({ ...r })), rowCount: rs.length }; }
    if (/auth_find_user_by_id/.test(sql)) { const u = d.users.get(String(params[0])); rec('PREAUTH', u ? 1 : 0); return { rows: u ? [{ ...u }] : [], rowCount: u ? 1 : 0 }; }
    const upd = /^UPDATE users SET (.*) WHERE id = \$(\d+)$/.exec(sql);
    if (upd) {
      const u = d.users.get(String(params[Number(upd[2]) - 1]));
      if (!u || !visible(u)) { rec('UPDATE_USERS', 0); return { rows: [], rowCount: 0 }; }
      for (const clause of upd[1].split(/,\s*/)) { const m = /^(\w+)\s*=\s*(?:\$(\d+)|NOW\(\))$/.exec(clause.trim()); if (m) u[m[1]] = m[2] ? params[Number(m[2]) - 1] : new Date(); }
      rec('UPDATE_USERS level=' + String(u.verification_level), 1); return { rows: [], rowCount: 1 };
    }
    if (/FROM users WHERE id/.test(sql)) {
      const u = d.users.get(String(params[0]));
      const ok = !!u && visible(u); rec('READ_USERS level=' + (ok ? String(u!.verification_level) : '-'), ok ? 1 : 0);
      return { rows: ok ? [{ ...u! }] : [], rowCount: ok ? 1 : 0 };
    }
    rec('UNMATCHED ' + sql.slice(0, 50), 0); return { rows: [], rowCount: 0 };
  }
  class FakePool {
    label: string; dbName: string;
    constructor(opts: Record<string, unknown> = {}, label?: string) {
      this.dbName = String(opts.database || (opts.connectionString ? new URL(String(opts.connectionString)).pathname.slice(1) : 'secuura'));
      this.label = label || 'db.ts-pool';
    }
    on() { return this; }
    async end() { /* nothing */ }
    async query(text: string, params?: unknown[]) { return exec(this.label, this.dbName, 'none', text, params); }
    async connect() {
      const f = st.faults.find((x) => !x.used && (x.pool === this.label || x.pool === '*') && x.match.source === 'CONNECT');
      if (f) { f.used = true; st.seq.push(`FAULT(${f.err}) CONNECT@${this.label}/${this.dbName}`); throw new Error(f.err); }
      let g = 'none'; const self = this;
      return { async query(text: string, values?: unknown[]) { const n = guc(text, values || []); if (n) g = n; if (/^\s*(COMMIT|ROLLBACK)\s*$/.test(text)) g = 'none'; return exec(self.label, self.dbName, g, text, values); }, release() { /* nothing */ } };
    }
  }
  return { dbs, db, st, FakePool };
});
vi.mock('pg', () => ({ Pool: W.FakePool, default: { Pool: W.FakePool } }));
const log = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() }));
vi.mock('__AUTH__/src/utils/logger', () => ({ logger: log, createLogger: () => log, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: log, createLogger: () => log }));
const TEST_DEK = vi.hoisted(() => Buffer.alloc(32, 7));
vi.mock('__AUTH__/src/services/subjectDeks', () => ({ subjectDeks: { getDek: vi.fn(async () => TEST_DEK), getOrCreateDek: vi.fn(async () => TEST_DEK) } }));
const caller = vi.hoisted(() => ({ v: {} as Record<string, string> }));
vi.mock('__AUTH__/src/middleware/authenticate', async () => {
  const { runWithTenantId } = await import('@secuura/shared');
  const inject = () => (req: express.Request & { user?: unknown }, _res: express.Response, next: express.NextFunction) => {
    (req as { user: unknown }).user = { ...caller.v };
    runWithTenantId(caller.v.tenantId, () => next());
  };
  return { authenticate: inject, authenticateAccessOrConnector: inject };
});
vi.mock('__AUTH__/src/services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
vi.mock('__AUTH__/src/services/password', () => ({ hashPassword: vi.fn(async () => 'hashed'), checkPasswordStrength: vi.fn(() => ({ ok: true })), verifyPassword: vi.fn(async () => true) }));

import { encryptFieldWithDek } from '@secuura/shared';
import * as dbmod from '__AUTH__/src/db';
import { userRoutes } from '__AUTH__/src/routes/users';
import { errorHandler } from '__AUTH__/src/middleware/errorHandler';

let server: ReturnType<ReturnType<typeof express>['listen']>;
let base = '';
const ROWS: Array<Record<string, unknown>> = [];
const SETUP: Record<string, unknown> = {};
beforeAll(async () => {
  process.env.DATABASE_URL = 'postgresql://qa:qa@127.0.0.1:1/secuura';
  process.env.PLATFORM_DATABASE_URL = 'postgresql://qa:qa@127.0.0.1:1/secuura_platform';
  // DRAFTER v2: QA1032R2_MT=off runs the REAL single-pool arm S (MULTI_TENANCY_ENABLED unset: initTenantManager returns before building a manager)
  if (process.env.QA1032R2_MT !== 'off') process.env.MULTI_TENANCY_ENABLED = 'true'; else delete process.env.MULTI_TENANCY_ENABLED;
  SETUP.mt = process.env.QA1032R2_MT;
  SETUP.initDb = await dbmod.initDb();
  SETUP.isDbAvailable = dbmod.isDbAvailable();
  try { await dbmod.initTenantManager(); SETUP.initTenantManager = 'returned'; } catch (e: any) { SETUP.initTenantManager = 'threw ' + String(e?.message).slice(0, 120); }
  const tm: any = dbmod.getTenantManager();
  SETUP.tenantManager = tm ? tm.constructor?.name : null;
  if (tm) {
    SETUP.realDefaultPoolClass = tm.defaultPool?.constructor?.name;
    tm.defaultPool = new W.FakePool({ connectionString: process.env.DATABASE_URL }, 'tm-default');
    tm.platformPool = new W.FakePool({ connectionString: process.env.PLATFORM_DATABASE_URL }, 'tm-platform');
    if (tm.refreshTimer) { clearInterval(tm.refreshTimer); tm.refreshTimer = null; SETUP.refreshTimerCleared = true; }
  }
  const app = express(); app.use(express.json()); app.use('/', userRoutes); app.use(errorHandler);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port); r(); }); });
  writeFileSync(String(process.env.QA1032R2_ROWS_OUT) + '.listen', JSON.stringify({ pid: process.pid, base, cwd: process.cwd(), nodeEnv: process.env.NODE_ENV }));
});
afterAll(async () => {
  await new Promise<void>((r) => server.close(() => r()));
  writeFileSync(String(process.env.QA1032R2_ROWS_OUT), JSON.stringify({ nodeEnv: process.env.NODE_ENV, setup: SETUP, rows: ROWS }, null, 1));
});

let n = 0;
function seed(dbNames: string[]): string {
  n += 1; const id = 'c1000000-0000-4000-8000-' + String(1032300000 + n).padStart(12, '0');
  const enc = (v: string, col: string) => encryptFieldWithDek(v, 'users.' + col + '.' + id, TEST_DEK) as string;
  for (const name of dbNames) {
    W.db(name).users.set(id, {
      id, email: enc('qa1032r2-pool-' + String(n) + '@example.test', 'email'), first_name: enc('Q', 'first_name'), last_name: enc('A', 'last_name'), display_name: null,
      role: 'user', status: 'active', email_verified: true, phone_number: null, phone_verified: false, mfa_enabled: false, mfa_secret: null, mfa_backup_codes: null,
      verification_level: 'basic', organization_id: null, tenant_id: TENANT, tenant_slug: null, wallet_address: null, auth_method: 'password', external_provider: null,
      external_id: null, google_id: null, linkedin_id: null, facebook_id: null, apple_id: null, github_id: null, microsoft_personal_id: null, metadata: null,
      created_at: new Date(), updated_at: new Date(), last_login_at: null,
    });
  }
  return id;
}
function arm(name: 'S' | 'M0' | 'M1' | 'M2'): Record<string, unknown> {
  const tm: any = dbmod.getTenantManager();
  const internals: any = dbmod;
  if (!tm) return { arm: name, tenantManager: 'NONE (db.ts query() takes the queryWithTenantGuc branch)' };
  if (name === 'M0') { tm.enabled = false; }
  else { tm.enabled = true; tm.perTenantDbEnabled = name === 'M2'; tm.tenantPools = new Map(); }
  tm.tenantConfigs = new Map([[TENANT, { tenantId: TENANT, dbName: name === 'M2' ? 'secuura_t1032' : 'secuura', dbHost: '', dbPort: 1, status: 'active', slug: 'qa1032' }]]);
  if (name === 'M2') {
    // the product would construct a real pg Pool for the tenant DB here; pre-seat a FakePool under the same key so the product's own map lookup returns it
    tm.tenantPools.set(TENANT, { pool: new W.FakePool({ database: 'secuura_t1032' }, 'tm-tenant'), lastUsed: Date.now() });
  }
  void internals;
  const p = tm.getPool(TENANT);
  return { arm: name, enabled: tm.enabled, perTenantDb: tm.perTenantDbEnabled, getPoolTENANT: p?.label + '/' + p?.dbName, getPoolUndefined: tm.getPool(undefined)?.label };
}
async function call(method: string, path: string, body?: unknown): Promise<{ status: number; json: Record<string, any> }> {
  const res = await fetch(base + path, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
  const t = await res.text(); let j: Record<string, any> = {}; try { j = JSON.parse(t); } catch { j = { raw: t.slice(0, 120) }; }
  return { status: res.status, json: j };
}
const levels = (id: string) => Object.fromEntries(Object.entries(W.dbs).map(([k, v]) => [k, v.users.get(id)?.verification_level ?? '-']));
const requestIn = (rid: string) => Object.fromEntries(Object.entries(W.dbs).map(([k, v]) => [k, v.vrows.get(rid)?.status ?? '-']));

const CASES: Array<['S' | 'M0' | 'M1' | 'M2', boolean, string]> = [];
const ARMS = process.env.QA1032R2_MT === 'off' ? (['S'] as const) : (['M0', 'M1', 'M2'] as const);
for (const a of ARMS) for (const rls of [true, false]) for (const f of ['none', 'readback-pooltimeout']) CASES.push([a, rls, f]);

describe('qa1032r2 drafter pool routing', () => {
  for (const [a, rls, f] of CASES) it(`${a} rls=${rls} fault=${f}`, async () => {
    const armInfo = arm(a);
    W.st.rls = rls; W.st.seq = []; log.error.mockClear(); log.warn.mockClear();
    const id = seed(a === 'M2' ? ['secuura', 'secuura_t1032'] : ['secuura']);
    const rid = 'vr-qa1032r2-pool-' + String(n);
    W.db('secuura').vrows.set(rid, { id: rid, user_id: id, current_level: 'BASIC', target_level: 'ENHANCED', documents: [], status: 'PENDING', submitted_at: '2026-09-18T00:00:00.000Z', reviewed_at: null, reviewed_by: null, rejection_reason: null });
    // the fault: the SELECT FROM users read-back on the pool the UPDATE used (the tenant route when a manager routes it, else db.ts's pool)
    const updPool = a === 'S' ? 'db.ts-pool' : a === 'M2' ? 'tm-tenant' : 'tm-default';
    W.st.faults = f === 'none' ? [] : [{ pool: updPool, match: /FROM users WHERE id/, err: 'timeout exceeded when trying to connect' }];
    caller.v = { userId: 'a1000000-0000-4000-8000-000000001032', role: 'SYSTEM_ADMIN', tenantId: TENANT };
    const r = await call('POST', '/verification/' + rid + '/review', { action: 'approve' });
    const approveSeq = [...W.st.seq];
    const afterApprove = { request: requestIn(rid), level: levels(id) }; // DRAFTER v2: snapshot BEFORE the reject
    W.st.seq = []; W.st.faults = [];
    const rej = await call('POST', '/verification/' + rid + '/review', { action: 'reject', reason: 'qa' });
    ROWS.push({
      id: `${a} rls=${rls} fault=${f}`, armInfo, status: r.status, message: String(r.json.message ?? r.json.error?.message ?? '').slice(0, 90),
      afterApprove, seq: approveSeq,
      errorLines: (log.error.mock.calls as any[]).map(([m, p]) => String(m).slice(0, 110) + ' ' + JSON.stringify({ levelNow: p?.levelNow, readError: p?.readError })).filter((m) => !/^DB |^Error occurred/.test(m)),
      warnLines: (log.warn.mock.calls as any[]).map(([m]) => String(m).slice(0, 110)).filter((m) => /Verification approve|matched 0 rows/.test(m)),
      thenReject: { status: rej.status, message: String(rej.json.message ?? rej.json.error?.message ?? '').slice(0, 60), request: requestIn(rid), level: levels(id) },
    });
  });
});
