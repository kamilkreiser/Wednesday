# READY — KS-1873-KS-1873-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/out.md.checker/patch.diff`** (from `ls` at 06:57 2026-11-12; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id-control/out.md.checker/patch.diff` rc 0, Wednesday (o158 operator)).

**Held 06:57 2026-11-12 by Wednesday (o158 operator) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c78c80bd537015674fa5e22701d745946f94d4fb`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/users.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/users.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/auth/src/routes/users.ts
133	0	Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (1 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: users.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/users.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/users.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts 133 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/users.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1873 admin create-user logs the new user id, never the email RED ks1873 R1 nothing logged while creating a user contains the email', 'KS-1873 admin create-user logs the new user id, never the email RED ks1873 R2 the create line carries the new user id']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1839 failed=0 | after: total=1843 failed=0` · `NEW reds: []` [baseline_suite.json total=1839 failed=0; after_suite.json total=1843 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/users.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts` (+133/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/users.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `c78c80bd537015674fa5e22701d745946f94d4fb` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/users.ts b/Blockchain/Dev/services/auth/src/routes/users.ts
--- a/Blockchain/Dev/services/auth/src/routes/users.ts
+++ b/Blockchain/Dev/services/auth/src/routes/users.ts
@@ -675,7 +675,7 @@
 
     await userRepo.createUser(user);
 
-    logger.info('Admin created user', { email, role: user.role, createdBy: req.user!.userId });
+    logger.info('Admin created user', { userId: user.id, role: user.role, createdBy: req.user!.userId });
 
     res.status(201).json({
       success: true,
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts
@@ -0,0 +1,133 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1873: POST /admin/create logged the new user's plaintext email at info level. Wednesday's ruling: the log line carries the
+// new user's id and never the email (no hash, no mask). This drives the real router with the logger replaced by a recorder, so the
+// assertions read exactly what the route passed to the logger.
+
+const state = vi.hoisted(() => ({
+  caller: { userId: 'dddddddd-4444-4444-8444-dddddddddddd', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' } as {
+    userId: string;
+    role: string;
+    tenantId?: string;
+  },
+}));
+
+const logged = vi.hoisted(() => ({ calls: [] as Array<{ level: string; message: string; meta: Record<string, unknown> }> }));
+
+const repoMock = vi.hoisted(() => ({
+  emailExists: vi.fn(async () => false),
+  createUser: vi.fn(async (user: unknown) => user),
+}));
+vi.mock('../repositories/userRepo', () => repoMock);
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => false,
+  query: vi.fn(async () => ({ rows: [] })),
+}));
+
+vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
+
+vi.mock('../services/password', () => ({
+  hashPassword: vi.fn(async () => 'hashed'),
+  checkPasswordStrength: vi.fn(() => ({ ok: true })),
+  verifyPassword: vi.fn(async () => true),
+}));
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
+vi.mock('../utils/logger', () => {
+  const record = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    logged.calls.push({ level, message, meta: meta ?? {} });
+  };
+  return { logger: { info: record('info'), warn: record('warn'), error: record('error'), debug: record('debug') } };
+});
+
+import { userRoutes } from '../routes/users';
+import { errorHandler } from '../middleware/errorHandler';
+import { logger } from '../utils/logger';
+
+const PROBE_EMAIL = 'ks1873.probe@example.test';
+let server: Server;
+let baseUrl: string;
+
+const SAVED_DATABASE_URL = process.env.DATABASE_URL;
+beforeAll(async () => {
+  delete process.env.DATABASE_URL;
+  const app = express();
+  app.use(express.json());
+  app.use('/', userRoutes);
+  app.use(errorHandler);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => {
+      const { port } = server.address() as AddressInfo;
+      baseUrl = `http://127.0.0.1:${port}`;
+      resolve();
+    });
+  });
+});
+
+afterAll(async () => {
+  if (SAVED_DATABASE_URL === undefined) delete process.env.DATABASE_URL; else process.env.DATABASE_URL = SAVED_DATABASE_URL;
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+beforeEach(() => {
+  logged.calls.length = 0;
+  repoMock.emailExists.mockClear();
+  repoMock.createUser.mockClear();
+});
+
+async function createProbeUser(): Promise<{ status: number; id: string }> {
+  const res = await fetch(`${baseUrl}/admin/create`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ email: PROBE_EMAIL, password: 'a-long-enough-password-1', firstName: 'Pat', lastName: 'Probe' }),
+  });
+  const body = (await res.json()) as { data?: { id?: string } };
+  return { status: res.status, id: body.data?.id ?? '' };
+}
+
+function createLine() {
+  return logged.calls.find((c) => c.message === 'Admin created user');
+}
+
+describe('KS-1873 admin create-user logs the new user id, never the email', () => {
+  it('control ks1873 C0 the recorder sees the create line with its role and the caller id', async () => {
+    const made = await createProbeUser();
+    expect(made.status).toBe(201);
+    const line = createLine();
+    expect(line).toBeDefined();
+    expect(line?.level).toBe('info');
+    expect(line?.meta.role).toBe('OWNER');
+    expect(line?.meta.createdBy).toBe('dddddddd-4444-4444-8444-dddddddddddd');
+  });
+
+  it('control ks1873 C1 the recorder would show an email if one were logged', () => {
+    logger.info('planted', { email: PROBE_EMAIL });
+    expect(JSON.stringify(logged.calls)).toContain(PROBE_EMAIL);
+  });
+
+  it('RED ks1873 R1 nothing logged while creating a user contains the email', async () => {
+    const made = await createProbeUser();
+    expect(made.status).toBe(201);
+    expect(logged.calls.length).toBeGreaterThan(0);
+    expect(JSON.stringify(logged.calls)).not.toContain(PROBE_EMAIL);
+  });
+
+  it('RED ks1873 R2 the create line carries the new user id', async () => {
+    const made = await createProbeUser();
+    expect(made.status).toBe(201);
+    expect(made.id).not.toBe('');
+    expect(createLine()?.meta.userId).toBe(made.id);
+  });
+});
```
