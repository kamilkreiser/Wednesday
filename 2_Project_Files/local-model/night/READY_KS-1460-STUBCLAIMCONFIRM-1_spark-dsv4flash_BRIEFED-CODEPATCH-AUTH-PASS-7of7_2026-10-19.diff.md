# READY — KS-1460-STUBCLAIMCONFIRM-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/out.md.checker/patch.diff`** (from `ls` at 19:25 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 19:25 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `80868551e67934cb951d28eec44ce3bdf835944c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/auth.ts , Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/auth.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/auth/src/routes/auth.ts
125	0	Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/auth.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/auth.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1460 - claiming an INVITED stub at /register confirms the write that activates it RED KS-1460 R1: when the activating update matches no row the answer is 503, not 201', 'KS-1460 - claiming an INVITED stub at /register confirms the write that activates it RED KS-1460 R2: and nothing is issued over the unconfirmed row (no session, no verification token, no mail)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1084 failed=0 | after: total=1088 failed=0` · `NEW reds: []` [baseline_suite.json total=1084 failed=0; after_suite.json total=1088 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +127/-2 test=src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/auth.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts` (+125/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `80868551e67934cb951d28eec44ce3bdf835944c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1460_p1/KS-1460.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1460_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/auth.ts b/Blockchain/Dev/services/auth/src/routes/auth.ts
index 00023447b..fa7b3386a 100644
--- a/Blockchain/Dev/services/auth/src/routes/auth.ts
+++ b/Blockchain/Dev/services/auth/src/routes/auth.ts
@@ -256,3 +256,3 @@
       // and the row gains the password hash etc. on the same write.
-      await userRepo.updateUser(userId, {
+      await userRepo.updateUserOrThrow(userId, {
         status: 'ACTIVE',
@@ -264,3 +264,3 @@
         role: 'OWNER',
-      });
+      }, 'Claiming the invited account');
       logger.info('KS-74: invited stub claimed on register', { userId });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts
new file mode 100644
index 000000000..833969b2d
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts
@@ -0,0 +1,125 @@
+/**
+ * KS-1460 (the INVITED-stub claim in `routes/auth.ts` only) - registering over an INVITED stub must not answer 201 when the write
+ * that activates the stub did not land.
+ *
+ * `POST /register` claims an INVITED stub with `userRepo.updateUser(...)` and DISCARDS the result. `updateUser` answers
+ * `null` when its UPDATE matched no row (or its read-back found nothing), so the caller was told "registered", given a
+ * session and a verification mail, over a row that is still INVITED. `updateUserOrThrow` is the repository's own
+ * wrapper for exactly this: it throws a 503 (ServiceUnavailableError) when the update cannot be confirmed.
+ * Harness: the real router and error handler; the repository, session, jwt, mail and event bus are mocked.
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const state = vi.hoisted(() => ({
+  existing: null as Record<string, unknown> | null,
+  updateResult: null as Record<string, unknown> | null,
+  updateCalls: 0,
+  sessions: 0,
+  mails: 0,
+  tokens: 0,
+}));
+
+vi.mock('../repositories/userRepo', async () => {
+  const { ServiceUnavailableError } = await import('../middleware/errorHandler');
+  const repoMock = {
+    getUserByEmail: vi.fn(async () => state.existing),
+    createUser: vi.fn(async (user: Record<string, unknown>) => user),
+    updateUser: vi.fn(async () => { state.updateCalls += 1; return state.updateResult; }),
+    updateUserOrThrow: vi.fn(async () => {
+      state.updateCalls += 1;
+      if (!state.updateResult) throw new ServiceUnavailableError('could not be confirmed');
+      return state.updateResult;
+    }),
+    storeEmailToken: vi.fn(async () => { state.tokens += 1; }),
+    seedDemoUsers: vi.fn(async () => undefined),
+  };
+  return { default: repoMock, __esModule: true, ...repoMock };
+});
+vi.mock('../services/password', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  hashPassword: vi.fn(async () => 'hashed'),
+}));
+vi.mock('../services/jwt', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  generateTokenPair: vi.fn(() => ({ accessToken: 'access', refreshToken: 'refresh', expiresIn: 900 })),
+}));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => { state.sessions += 1; return { id: 'session-1460' }; }),
+}));
+vi.mock('../services/email', () => ({
+  sendVerificationEmail: vi.fn(async () => { state.mails += 1; return true; }),
+  sendPasswordResetEmail: vi.fn(async () => true),
+}));
+vi.mock('../events', () => ({
+  publishEvent: vi.fn(async () => undefined),
+  EventTypes: { USER_REGISTERED: 'user.registered' },
+}));
+vi.mock('../db', () => ({ isDbAvailable: () => false, query: vi.fn(async () => ({ rows: [] })) }));
+const silentLogger = vi.hoisted(() => ({ debug: () => undefined, info: () => undefined, warn: () => undefined, error: () => undefined, log: () => undefined }));
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: () => undefined }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+import { authRoutes } from '../routes/auth';
+import { errorHandler } from '../middleware/errorHandler';
+
+let server: Server;
+let baseUrl = '';
+beforeAll(async () => {
+  const app = express();
+  app.use(express.json());
+  app.use('/', authRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => { await new Promise<void>((resolve) => server.close(() => resolve())); });
+
+const STUB = { id: 'stub-1460', status: 'INVITED', tenantId: 'tenant-1460', tenantSlug: 'slug-1460', createdAt: new Date('2026-01-01T00:00:00Z') };
+beforeEach(() => {
+  state.existing = null;
+  state.updateResult = null;
+  state.updateCalls = 0;
+  state.sessions = 0;
+  state.mails = 0;
+  state.tokens = 0;
+});
+
+async function register(): Promise<number> {
+  const res = await fetch(baseUrl + '/register', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ email: 'invitee-1460@example.com', password: 'Tr0ub4dor&3-horse-staple', name: 'Ann Lee' }),
+  });
+  return res.status;
+}
+
+describe('KS-1460 - claiming an INVITED stub at /register confirms the write that activates it', () => {
+  it('RED KS-1460 R1: when the activating update matches no row the answer is 503, not 201', async () => {
+    state.existing = { ...STUB };
+    state.updateResult = null;
+    expect(await register()).toBe(503);
+  });
+
+  it('RED KS-1460 R2: and nothing is issued over the unconfirmed row (no session, no verification token, no mail)', async () => {
+    state.existing = { ...STUB };
+    state.updateResult = null;
+    await register();
+    expect([state.updateCalls, state.sessions, state.tokens, state.mails]).toEqual([1, 0, 0, 0]);
+  });
+
+  it('CONTROL KS-1460 C1: when the activating update lands the claim answers 201 and issues the session once', async () => {
+    state.existing = { ...STUB };
+    state.updateResult = { ...STUB, status: 'ACTIVE' };
+    expect(await register()).toBe(201);
+    expect([state.updateCalls, state.sessions, state.tokens, state.mails]).toEqual([1, 1, 1, 1]);
+  });
+
+  it('CONTROL KS-1460 C2: a fresh registration (no stub) answers 201 and makes no activating update at all', async () => {
+    expect(await register()).toBe(201);
+    expect([state.updateCalls, state.sessions]).toEqual([0, 1]);
+  });
+});
```
