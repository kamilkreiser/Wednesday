# READY — KS-1193-F2-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1193-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1193-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1193F2-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 117/117 in the diff; reds matched 2/2; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 117/117 in the diff; reds matched 2/2; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1193-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1193-review-read-query-error-is-not-503.test.ts` (new). `+` lines 117 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 3/3 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F2` → red exactly ['RED KS-1193 F2 - review as SYSTEM_ADMIN: a 40001 serializati', 'RED KS-1193 F2 - review as SYSTEM_ADMIN: a 42P01 missing rel']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1193-ornith35b-night/input.json`. Brief: `night/briefs/KS-1193-F2-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1193-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1193-review-read-query-error-is-not-503.test.ts
@@ -0,0 +1,117 @@
+// KS-1193 F2 (the #1015 gate on KS-1018): the review read has no non-infrastructure cell, so widening its rethrow to every
+// error (the gate's D-TW-GET) reddened 0 of 751 cells. These cells feed query-level pg errors to the review read.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const state = vi.hoisted(() => ({
+  caller: { userId: 'ks1193-admin', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' },
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
+const GET_SQL = 'WHERE id = '; // only the review by-id read carries this
+const MISSING_TABLE = Object.assign(new Error('relation verification_upgrade_requests does not exist'), { code: '42P01' });
+const SERIALIZATION = Object.assign(new Error('could not serialize access due to concurrent update'), { code: '40001' });
+
+let server: Server;
+let baseUrl = '';
+
+/** Every statement answers healthily, except the review by-id read, which rejects with this error. */
+function failReviewRead(err: Error): void {
+  dbQuery.mockImplementation(async (sql: string) => {
+    if (sql.includes(GET_SQL)) throw err;
+    return { rows: [] };
+  });
+}
+
+async function review(requestId: string): Promise<{ status: number; code: unknown }> {
+  const res = await fetch(baseUrl + '/verification/' + requestId + '/review', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action: 'approve' }) });
+  const json = (await res.json()) as { error?: { code?: unknown } };
+  return { status: res.status, code: json.error?.code };
+}
+
+function writes(): number[] {
+  const inserts = dbQuery.mock.calls.filter((c) => String(c[0]).includes('INSERT INTO verification_upgrade_requests')).length;
+  return [vi.mocked(userRepo.updateUserPlatformScope).mock.calls.length, inserts];
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
+  state.caller = { userId: 'ks1193-admin', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' };
+  dbQuery.mockResolvedValue({ rows: [] });
+});
+
+describe('KS-1193 F2 - a query-level pg error on the review read is not an availability failure', () => {
+  it('RED KS-1193 F2 - review as SYSTEM_ADMIN: a 42P01 missing relation on the by-id read is not answered 503', async () => {
+    failReviewRead(MISSING_TABLE);
+    const res = await review('ks1193-unknown-request-a');
+    expect(res.code, 'a query-level error is not an availability failure').not.toBe('SERVICE_UNAVAILABLE');
+    expect([404, 500], 'the fall-through 404, or a KS-253 500').toContain(res.status);
+    expect(writes(), 'no level raised, no row written').toEqual([0, 0]);
+  });
+
+  it('RED KS-1193 F2 - review as SYSTEM_ADMIN: a 40001 serialization failure on the by-id read is not answered 503', async () => {
+    failReviewRead(SERIALIZATION);
+    const res = await review('ks1193-unknown-request-b');
+    expect(res.code, 'a query-level error is not an availability failure').not.toBe('SERVICE_UNAVAILABLE');
+    expect([404, 500], 'the fall-through 404, or a KS-253 500').toContain(res.status);
+    expect(writes(), 'no level raised, no row written').toEqual([0, 0]);
+  });
+
+  it('GREEN KS-1193 control - the 42P01 reaches the review read: its catch logs the line once with that code', async () => {
+    failReviewRead(MISSING_TABLE);
+    await review('ks1193-unknown-request-c');
+    const calls = vi.mocked(logger.error).mock.calls as unknown as Array<[string, Record<string, unknown>]>;
+    expect(calls.filter((c) => c[0] === 'DB getVerificationRequest failed').map((c) => c[1].code), 'the review read').toEqual(['42P01']);
+  });
+});
```
