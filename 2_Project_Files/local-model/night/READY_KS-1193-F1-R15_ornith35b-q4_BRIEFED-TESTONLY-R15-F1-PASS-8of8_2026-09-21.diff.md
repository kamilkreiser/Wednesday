# READY — KS-1193-F1-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1193-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 22:00 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,124 @@ declared old=0 new=124 actual old=0 new=153 ); every line byte-exact`; golden not located — no byte-identity claim is made.

**Held 22:00 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1193-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1193-verification-reads-codeless-pool-timeout.test.ts` (new). `+` lines 153 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F1` → red exactly ['RED KS-1193 F1 - GET /me/verification: the codeless pool tim', 'RED KS-1193 F1 - POST /me/verification: the codeless pool ti', 'RED KS-1193 F1 - review as SYSTEM_ADMIN: the codeless pool t']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1193-ornith35b-night/input.json`. Brief: `night/briefs/KS-1193-F1-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1193-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1193-verification-reads-codeless-pool-timeout.test.ts
@@ -0,0 +1,124 @@
+// KS-1193 F1 (the #1015 gate on KS-1018): every KS-1018 cell feeds ECONNREFUSED, which has a code, so the gate's D-NARROW (rethrow only
+// infra errors that ALSO have a code) reddened 0 of 751 cells. These cells feed the KS-217 codeless pool timeout to each read.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const state = vi.hoisted(() => ({
+  caller: { userId: 'ks1193-nobody', role: 'USER', tenantId: 'tenant-default' },
+  users: new Map<string, Record<string, unknown>>(),
+}));
+const dbQuery = vi.hoisted(() => vi.fn());
+
+vi.mock('../repositories/userRepo', () => {
+  const repoMock = {
+    getUserById: vi.fn(async (id: string) => state.users.get(id) ?? null),
+    getUserByIdPlatformScope: vi.fn(async (id: string) => state.users.get(id) ?? null),
+    updateUser: vi.fn(async () => null),
+    updateUserPlatformScope: vi.fn(async () => null),
+    listUsers: vi.fn(async () => []),
+    countUsers: vi.fn(async () => 0),
+    listOrganizations: vi.fn(async () => []),
+    getOrganizationTenant: vi.fn(async () => ({ tenantId: 'tenant-default' })),
+    emailExists: vi.fn(async () => false),
+    createUser: vi.fn(async (user: Record<string, unknown>) => user),
+    createInvitedStub: vi.fn(async () => ({ user: {}, alreadyExisted: false })),
+  };
+  return { default: repoMock, __esModule: true, ...repoMock };
+});
+
+vi.mock('../middleware/authenticate', () => {
+  const injectCaller =
+    () => (req: express.Request & { user?: unknown }, _res: express.Response, next: express.NextFunction) => {
+      (req as { user: unknown }).user = { ...state.caller };
+      next();
+    };
+  return { authenticate: injectCaller, authenticateAccessOrConnector: injectCaller };
+});
+
+vi.mock('../db', () => ({ isDbAvailable: () => true, query: dbQuery }));
+vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
+vi.mock('../services/password', () => ({ hashPassword: vi.fn(async () => 'hashed'), checkPasswordStrength: vi.fn(() => ({ ok: true })), verifyPassword: vi.fn(async () => true) }));
+vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() } }));
+
+import { userRoutes } from '../routes/users';
+import { errorHandler } from '../middleware/errorHandler';
+import { logger } from '../utils/logger';
+import * as userRepo from '../repositories/userRepo';
+
+/** The KS-217 baseline error: the pg pool connection-acquisition timeout. It carries NO code. */
+const POOL_TIMEOUT = 'Connection terminated due to connection timeout';
+const LIST_SQL = 'ORDER BY submitted_at DESC'; // only the list read carries this
+const FIND_SQL = 'AND status'; // only the pending read carries this
+const GET_SQL = 'WHERE id = '; // only the by-id read carries this
+
+let server: Server;
+let baseUrl = '';
+
+/** Every statement answers healthily, except the SELECT carrying the fragment, which rejects with the pool timeout. */
+function timeoutOn(fragment: string): void {
+  dbQuery.mockImplementation(async (sql: string) => {
+    if (sql.includes(fragment)) throw new Error(POOL_TIMEOUT);
+    return { rows: [] };
+  });
+}
+
+function seedUser(id: string): void {
+  state.users.set(id, { id, email: id + '@ks1193.example', role: 'USER', status: 'ACTIVE', verificationLevel: 'BASIC', tenantId: 'tenant-default' });
+  state.caller = { userId: id, role: 'USER', tenantId: 'tenant-default' };
+}
+
+async function call(method: string, path: string, body?: unknown): Promise<{ status: number; code: unknown; data: Record<string, unknown> }> {
+  const res = await fetch(baseUrl + path, { method, headers: { 'Content-Type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
+  const json = (await res.json()) as { error?: { code?: unknown }; data?: Record<string, unknown> };
+  return { status: res.status, code: json.error?.code, data: json.data ?? {} };
+}
+
+function insertCount(): number {
+  return dbQuery.mock.calls.filter((c) => String(c[0]).includes('INSERT INTO verification_upgrade_requests')).length;
+}
+
+function loggedErrors(line: string): unknown[] {
+  const calls = vi.mocked(logger.error).mock.calls as unknown as Array<[string, Record<string, unknown>]>;
+  return calls.filter((c) => c[0] === line).map((c) => c[1].error);
+}
+
+/** A PENDING request for a fresh subject, made through the REAL route with a healthy DB (so memory holds it too); then an admin calls. */
+async function createPending(subject: string): Promise<string> {
+  dbQuery.mockResolvedValue({ rows: [] });
+  seedUser(subject);
+  const created = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+  expect([created.status, created.data.status], 'the request was created').toEqual([200, 'PENDING']);
+  state.caller = { userId: 'ks1193-admin', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' };
+  return String(created.data.requestId);
+}
+
+beforeAll(async () => {
+  const app = express();
+  app.use(express.json());
+  app.use('/', userRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+
+afterAll(async () => { await new Promise<void>((resolve) => server.close(() => resolve())); });
+
+beforeEach(() => {
+  vi.clearAllMocks();
+  state.users.clear();
+  dbQuery.mockResolvedValue({ rows: [] });
+});
+
+describe('KS-1193 F1 - the codeless KS-217 pool timeout on each verification-store read answers 503', () => {
+  it('RED KS-1193 F1 - GET /me/verification: the codeless pool timeout on the list read answers 503, not the in-memory list', async () => {
+    seedUser('ks1193-list-user');
+    timeoutOn(LIST_SQL);
+    const res = await call('GET', '/me/verification');
+    expect([res.status, res.code], 'a codeless pool timeout is an infrastructure failure').toEqual([503, 'SERVICE_UNAVAILABLE']);
+  });
+
+  it('RED KS-1193 F1 - POST /me/verification: the codeless pool timeout on the pending read answers 503 and saves nothing', async () => {
+    seedUser('ks1193-post-user');
+    timeoutOn(FIND_SQL);
+    const res = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([res.status, res.code], 'a codeless pool timeout is an infrastructure failure').toEqual([503, 'SERVICE_UNAVAILABLE']);
+    expect(insertCount(), 'no request row was written').toBe(0);
+  });
+
+  it('RED KS-1193 F1 - review as SYSTEM_ADMIN: the codeless pool timeout on the by-id read answers 503 and approves nothing from memory', async () => {
+    const requestId = await createPending('ks1193-review-subject');
+    const insertsBefore = insertCount();
+    timeoutOn(GET_SQL);
+    const res = await call('POST', '/verification/' + requestId + '/review', { action: 'approve' });
+    expect([res.status, res.code], 'a codeless pool timeout is an infrastructure failure').toEqual([503, 'SERVICE_UNAVAILABLE']);
+    expect([vi.mocked(userRepo.updateUserPlatformScope).mock.calls.length, insertCount() - insertsBefore], 'no level raised, no row written').toEqual([0, 0]);
+  });
+
+  it('GREEN KS-1193 control - the codeless timeout reaches each read: its catch logs the timeout message exactly once', async () => {
+    seedUser('ks1193-reach-user');
+    timeoutOn(LIST_SQL);
+    await call('GET', '/me/verification');
+    timeoutOn(FIND_SQL);
+    await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    const requestId = await createPending('ks1193-reach-subject');
+    timeoutOn(GET_SQL);
+    await call('POST', '/verification/' + requestId + '/review', { action: 'approve' });
+    expect(loggedErrors('DB listUserVerificationRequests failed'), 'the list read').toEqual([POOL_TIMEOUT]);
+    expect(loggedErrors('DB findPendingVerificationRequest failed'), 'the pending read').toEqual([POOL_TIMEOUT]);
+    expect(loggedErrors('DB getVerificationRequest failed'), 'the by-id read').toEqual([POOL_TIMEOUT]);
+  });
+});
```
