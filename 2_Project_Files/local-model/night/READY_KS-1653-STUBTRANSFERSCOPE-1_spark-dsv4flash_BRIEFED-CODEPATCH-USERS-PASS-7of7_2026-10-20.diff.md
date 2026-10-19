# READY — KS-1653-STUBTRANSFERSCOPE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/out.md.checker/patch.diff`** (from `ls` at 00:18 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1-control/out.md.checker/patch.diff` rc 0, Wednesday (overnight 10-20)).

**Held 00:18 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4a065fb7535080190c407237f948d0af3538f2dd`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/users.ts , Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/users.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/auth/src/routes/users.ts
108	0	Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/users.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/users.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts fails at the untouched tip (2 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=2 of total=6; red cell(s): ['KS-1653 - /api/users/stub admits a transfer-custody caller on its own scope RED KS-1653 S1: a connector holding only documents:transfer-custody is admitted (201) and the stub is minted once', "KS-1653 - /api/users/stub admits a transfer-custody caller on its own scope RED KS-1653 S2: Platform S's minted set WITHOUT certifications:write is still admitted for transfer-custody"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1089 failed=0 | after: total=1095 failed=0` · `NEW reds: []` [baseline_suite.json total=1089 failed=0; after_suite.json total=1095 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +110/-0 test=src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/users.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts` (+108/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4a065fb7535080190c407237f948d0af3538f2dd` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1653_p1/KS-1653.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1653_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/users.ts b/Blockchain/Dev/services/auth/src/routes/users.ts
index c360ce040..10fab906c 100644
--- a/Blockchain/Dev/services/auth/src/routes/users.ts
+++ b/Blockchain/Dev/services/auth/src/routes/users.ts
@@ -256,2 +256,4 @@
   // users surface it has no need for.
+  // KS-1653: Platform S's transfer-custody calls are admitted on their own scope, not only because S's key also holds certifications:write.
+  if (scopes.includes('documents:transfer-custody')) return true;
   return scopes.includes('certifications:write');
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts
new file mode 100644
index 000000000..0a1f5e5a1
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1653-stub-admits-transfer-custody-on-its-own-scope.test.ts
@@ -0,0 +1,108 @@
+/**
+ * KS-1653 - `POST /api/users/stub` admits Platform S's transfer-custody calls only because S's minted connector set also
+ * carries `certifications:write` (KS-564 Option A). The scope that does the admitting has nothing to do with the operation
+ * being performed. After the fix `documents:transfer-custody` admits the call in its own right, and `certifications:write`
+ * stays admitted (KS-564 depends on it). The control cells pin what must not widen: other scopes, and no scopes at all,
+ * are still refused with a 403 and no stub is minted.
+ * Harness: the real users router and error handler; the authentication middleware and the repository are mocked.
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const state = vi.hoisted(() => ({
+  scopes: undefined as string[] | undefined,
+  role: 'connector',
+  stubCalls: 0,
+}));
+
+vi.mock('../middleware/authenticate', () => {
+  const asCaller = (req: { user?: unknown }, _res: unknown, next: () => void) => {
+    req.user = { userId: 'connector:platform-s:1653', role: state.role, tenantId: 'tenant-1653', scopes: state.scopes };
+    next();
+  };
+  return { authenticate: () => asCaller, authenticateAccessOrConnector: () => asCaller };
+});
+vi.mock('../repositories/userRepo', () => {
+  const repoMock = {
+    createInvitedStub: vi.fn(async () => {
+      state.stubCalls += 1;
+      return { alreadyExisted: false, user: { id: 'stub-1653', status: 'INVITED', email: 'holder-1653@example.com', tenantId: 'tenant-1653' } };
+    }),
+  };
+  return { default: repoMock, __esModule: true, ...repoMock };
+});
+vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => undefined) }));
+vi.mock('../db', () => ({ isDbAvailable: () => false, query: vi.fn(async () => ({ rows: [] })) }));
+const silentLogger = vi.hoisted(() => ({ debug: () => undefined, info: () => undefined, warn: () => undefined, error: () => undefined, log: () => undefined }));
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: () => undefined }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+import { userRoutes } from '../routes/users';
+import { errorHandler } from '../middleware/errorHandler';
+
+let server: Server;
+let baseUrl = '';
+beforeAll(async () => {
+  const app = express();
+  app.use(express.json());
+  app.use('/', userRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => { await new Promise<void>((resolve) => server.close(() => resolve())); });
+beforeEach(() => {
+  state.scopes = undefined;
+  state.role = 'connector';
+  state.stubCalls = 0;
+});
+
+async function stub(): Promise<number> {
+  const res = await fetch(baseUrl + '/stub', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ email: 'holder-1653@example.com' }),
+  });
+  return res.status;
+}
+
+describe('KS-1653 - /api/users/stub admits a transfer-custody caller on its own scope', () => {
+  it('RED KS-1653 S1: a connector holding only documents:transfer-custody is admitted (201) and the stub is minted once', async () => {
+    state.scopes = ['documents:transfer-custody'];
+    expect(await stub()).toBe(201);
+    expect(state.stubCalls).toBe(1);
+  });
+
+  it('RED KS-1653 S2: Platform S\'s minted set WITHOUT certifications:write is still admitted for transfer-custody', async () => {
+    state.scopes = ['documents:write', 'documents:read', 'documents:share', 'documents:revoke', 'documents:transfer-custody', 'anchors:read', 'anchors:write'];
+    expect(await stub()).toBe(201);
+    expect(state.stubCalls).toBe(1);
+  });
+
+  it('CONTROL KS-1653 C1: certifications:write is still admitted (KS-564 Option A depends on it)', async () => {
+    state.scopes = ['certifications:write'];
+    expect(await stub()).toBe(201);
+    expect(state.stubCalls).toBe(1);
+  });
+
+  it('CONTROL KS-1653 C2: users:read is still admitted', async () => {
+    state.scopes = ['users:read'];
+    expect(await stub()).toBe(201);
+    expect(state.stubCalls).toBe(1);
+  });
+
+  it('CONTROL KS-1653 C3: an unrelated scope set (documents:read, documents:write) is refused with a 403 and mints no stub', async () => {
+    state.scopes = ['documents:read', 'documents:write'];
+    expect(await stub()).toBe(403);
+    expect(state.stubCalls).toBe(0);
+  });
+
+  it('CONTROL KS-1653 C4: no scopes at all is refused with a 403 and mints no stub', async () => {
+    state.scopes = [];
+    expect(await stub()).toBe(403);
+    expect(state.stubCalls).toBe(0);
+  });
+});
```
