# READY — KS-623-TESTTOKENENVALLOW-2 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_623_r2/out.md.checker/patch.diff`** (from `ls` at 14:12 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_623_r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_623_r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 14:12 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_623_r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `9b90f8ac77532141624a2c5892a0b47074e01427`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/middleware/authenticate.ts , Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/middleware/authenticate.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/auth/src/middleware/authenticate.ts
77	0	Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/middleware/authenticate.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/middleware/authenticate.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts fails at the untouched tip (2 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=2 of total=6; red cell(s): ['KS-623 - the auth service accepts a test token only in an explicit development or test environment RED KS-623 T1: an UNSET NODE_ENV with ENABLE_TEST_TOKENS=true refuses the test token', 'KS-623 - the auth service accepts a test token only in an explicit development or test environment RED KS-623 T2: NODE_ENV=staging with ENABLE_TEST_TOKENS=true refuses the test token']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1073 failed=2 | after: total=1079 failed=0` · `NEW reds: []` [baseline_suite.json total=1073 failed=2; after_suite.json total=1079 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +79/-2 test=src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/middleware/authenticate.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts` (+77/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `9b90f8ac77532141624a2c5892a0b47074e01427` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_623_r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_623_r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/middleware/authenticate.ts b/Blockchain/Dev/services/auth/src/middleware/authenticate.ts
index 9430831cd..56a50f144 100644
--- a/Blockchain/Dev/services/auth/src/middleware/authenticate.ts
+++ b/Blockchain/Dev/services/auth/src/middleware/authenticate.ts
@@ -19,4 +19,4 @@ const TEST_TOKEN_PREFIX = 'test_token_';
 function parseTestToken(token: string): JwtPayload | null {
-  // SECURITY: Never accept test tokens in production
-  if (process.env.NODE_ENV === 'production') {
+  // SECURITY: test tokens only in an explicit development or test environment; an unset or any other NODE_ENV fails closed (KS-623), as the gateway's parseTestToken does
+  if (!['development', 'test'].includes(process.env.NODE_ENV || '')) {
     return null;
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts
new file mode 100644
index 000000000..8d4deeaf3
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks623-test-tokens-need-an-explicit-development-or-test-env.test.ts
@@ -0,0 +1,77 @@
+/**
+ * KS-623 - the auth service accepted an unsigned `test_token_<base64>` (a self-asserted role and tenant) in EVERY
+ * environment except NODE_ENV === 'production' (a denylist), so an unset or unexpected NODE_ENV (staging, a typo)
+ * together with ENABLE_TEST_TOKENS=true let a stranger assert any role. The gateway's twin
+ * (api-gateway/src/middleware/auth.ts parseTestToken) is an allowlist: only 'development' and 'test'. The auth
+ * service now matches it, so the unset case fails closed on both sides. `authenticate()` is driven directly: a test
+ * token that is refused falls through to the standard JWT path, where the mocked verifier throws, and next() gets
+ * that error; a test token that is accepted sets req.user and calls next() with no error.
+ */
+import { describe, it, expect, afterEach, vi } from 'vitest';
+
+vi.mock('../services/jwt', () => ({
+  verifyAccessToken: vi.fn(() => { throw new Error('ks623 not a signed token'); }),
+  verifyConnectorToken: vi.fn(() => { throw new Error('ks623 not a connector token'); }),
+}));
+vi.mock('../services/session', () => ({
+  validateSession: vi.fn(async () => true),
+  updateSessionActivity: vi.fn(async () => undefined),
+}));
+
+import { authenticate } from '../middleware/authenticate';
+
+const SAVED = { NODE_ENV: process.env.NODE_ENV, ENABLE_TEST_TOKENS: process.env.ENABLE_TEST_TOKENS };
+afterEach(() => {
+  for (const [k, v] of Object.entries(SAVED)) {
+    if (v === undefined) delete process.env[k]; else process.env[k] = v;
+  }
+});
+
+function setEnv(nodeEnv: string | undefined, enable: string | undefined): void {
+  if (nodeEnv === undefined) delete process.env.NODE_ENV; else process.env.NODE_ENV = nodeEnv;
+  if (enable === undefined) delete process.env.ENABLE_TEST_TOKENS; else process.env.ENABLE_TEST_TOKENS = enable;
+}
+
+const TEST_TOKEN = 'test_token_' + Buffer.from(JSON.stringify({ sub: 'u-ks623', role: 'SUPER_ADMIN', organizationId: 'org-ks623' })).toString('base64');
+
+/** Run authenticate() once with the test token; report what the middleware did with it. */
+async function present(): Promise<{ userId: string | undefined; role: string | undefined; error: string | undefined }> {
+  const req: any = { headers: { authorization: 'Bearer ' + TEST_TOKEN } };
+  let error: string | undefined;
+  await authenticate()(req, {} as any, (err?: unknown) => { if (err) error = err instanceof Error ? err.message : String(err); });
+  return { userId: req.user?.userId, role: req.user?.role, error };
+}
+
+const REFUSED = { userId: undefined, role: undefined, error: 'ks623 not a signed token' };
+
+describe('KS-623 - the auth service accepts a test token only in an explicit development or test environment', () => {
+  it('RED KS-623 T1: an UNSET NODE_ENV with ENABLE_TEST_TOKENS=true refuses the test token', async () => {
+    setEnv(undefined, 'true');
+    expect(await present()).toEqual(REFUSED);
+  });
+
+  it('RED KS-623 T2: NODE_ENV=staging with ENABLE_TEST_TOKENS=true refuses the test token', async () => {
+    setEnv('staging', 'true');
+    expect(await present()).toEqual(REFUSED);
+  });
+
+  it('CONTROL KS-623 T3: NODE_ENV=test with ENABLE_TEST_TOKENS=true still accepts it, as SUPER_ADMIN', async () => {
+    setEnv('test', 'true');
+    expect(await present()).toEqual({ userId: 'u-ks623', role: 'SUPER_ADMIN', error: undefined });
+  });
+
+  it('CONTROL KS-623 T4: NODE_ENV=development with ENABLE_TEST_TOKENS=true still accepts it', async () => {
+    setEnv('development', 'true');
+    expect(await present()).toEqual({ userId: 'u-ks623', role: 'SUPER_ADMIN', error: undefined });
+  });
+
+  it('CONTROL KS-623 T5: NODE_ENV=production refuses it even with ENABLE_TEST_TOKENS=true', async () => {
+    setEnv('production', 'true');
+    expect(await present()).toEqual(REFUSED);
+  });
+
+  it('CONTROL KS-623 T6: NODE_ENV=test without the ENABLE_TEST_TOKENS opt-in refuses it', async () => {
+    setEnv('test', undefined);
+    expect(await present()).toEqual(REFUSED);
+  });
+});
```
