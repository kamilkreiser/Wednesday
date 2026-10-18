# READY — KS-1504-AUTHMETHODLOGFIELD-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1/out.md.checker/patch.diff`** (from `ls` at 03:01 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in rateLimitEnforce.ts (run 4 vs golden 7 body lines — context, since the change lines are equal) (identical in ks1504-no-allowance-warning-escapes-the-auth-method.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 03:01 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `385fc288fae831f2ca15b9d091c844f33285b784`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
93	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1504 - the no-allowance warning escapes authMethod RED KS-1504 an authMethod holding a newline and a forged line is ONE log line with no raw line break', 'KS-1504 - the no-allowance warning escapes authMethod RED KS-1504 the newline is written as the two characters backslash and n', 'KS-1504 - the no-allowance warning escapes authMethod RED KS-1504 the Unicode line and paragraph separators in an authMethod are escaped too']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1175 failed=0 | after: total=1181 failed=0` · `NEW reds: []` [baseline_suite.json total=1175 failed=0; after_suite.json total=1181 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +94/-1 test=src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts` (+93/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `385fc288fae831f2ca15b9d091c844f33285b784` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1504_p1/KS-1504.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1504_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts
@@ -180,3 +180,3 @@ export function enforceClientRateLimit(injectedClient?: any) {
       // KS-1464: throttled on the bucket (clientId), decided above, which carries the tenant.
-      warnNoAllowance(clientId, String(user.connectorId || user.userId), String(user.tenantId || 'none'), String(user.authMethod));
+      warnNoAllowance(clientId, String(user.connectorId || user.userId), String(user.tenantId || 'none'), logField(user.authMethod));
     }
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1504-no-allowance-warning-escapes-the-auth-method.test.ts
@@ -0,0 +1,93 @@
+/**
+ * =============================================================================
+ * KS-1504 - the "no rateLimit" warning writes its authMethod through logField
+ * =============================================================================
+ * The warning in middleware/rateLimitEnforce.ts escapes its principal and its tenant (KS-1480) but wrote `authMethod`
+ * raw. That was safe only because the gate in front of it admits the two fixed tokens of MACHINE_AUTH_METHODS
+ * (`api_key`, `oauth_app`). Escaping the field removes the dependency on that set: a value that is not a clean token
+ * can no longer split or forge a log line, and the two real members are written byte for byte as before.
+ *
+ * The gate cannot be made to admit a hostile value from outside the module, so the user object below answers the gate's
+ * first read of `authMethod` with a real member and every later read (the warning's own) with the value under test.
+ * =============================================================================
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+
+const fakeRedis = vi.hoisted(() => ({ counts: new Map<string, number>() }));
+vi.mock('../services/redis', async (importOriginal) => {
+  const real = (await importOriginal()) as Record<string, unknown>;
+  const client = {
+    status: 'ready',
+    incr: async (k: string) => { const n = (fakeRedis.counts.get(k) ?? 0) + 1; fakeRedis.counts.set(k, n); return n; },
+    pexpire: async () => 1,
+    pttl: async () => 60000,
+  };
+  return { ...real, getRedisClient: () => client };
+});
+
+import { enforceClientRateLimit } from '../middleware/rateLimitEnforce';
+
+function makeRes() {
+  const res: any = { headers: {} as Record<string, string>, code: undefined as number | undefined };
+  res.setHeader = (k: string, v: string) => { res.headers[k] = v; };
+  res.status = (c: number) => { res.code = c; return res; };
+  res.json = () => res;
+  return res;
+}
+
+let warn: ReturnType<typeof vi.spyOn>;
+const lines = (): string[] => warn.mock.calls.map((c: unknown[]) => String(c[0])).filter((l: string) => l.includes('has no rateLimit'));
+
+/** One request of a machine principal with NO allowance; returns the new warning lines it logged. */
+async function warnFor(user: Record<string, unknown>): Promise<string[]> {
+  const before = lines().length;
+  await enforceClientRateLimit()({ user } as any, makeRes(), vi.fn());
+  return lines().slice(before);
+}
+
+/** A principal the gate admits as `api_key` on its first read of authMethod; every later read answers `later`. */
+function userWhoseMethodReadsBackAs(later: string, over: Record<string, unknown>): Record<string, unknown> {
+  let reads = 0;
+  return { ...over, get authMethod() { reads += 1; return reads === 1 ? 'api_key' : later; } };
+}
+
+beforeAll(() => { warn = vi.spyOn(console, 'warn').mockImplementation(() => undefined); });
+afterAll(() => { warn.mockRestore(); vi.restoreAllMocks(); });
+
+describe('KS-1504 - the no-allowance warning escapes authMethod', () => {
+  it('CONTROL KS-1504 api_key is written byte for byte', async () => {
+    const out = await warnFor({ authMethod: 'api_key', tenantId: 'ks1504-t1', connectorId: 'ks1504-c1' });
+    expect(out).toHaveLength(1);
+    expect(out[0]).toContain('machine caller ks1504-c1 (api_key, tenant ks1504-t1) has no rateLimit');
+  });
+
+  it('CONTROL KS-1504 oauth_app is written byte for byte', async () => {
+    const out = await warnFor({ authMethod: 'oauth_app', tenantId: 'ks1504-t2', connectorId: 'ks1504-c2' });
+    expect(out).toHaveLength(1);
+    expect(out[0]).toContain('machine caller ks1504-c2 (oauth_app, tenant ks1504-t2) has no rateLimit');
+  });
+
+  it('CONTROL KS-1504 the getter user is a real machine principal: a clean later value gives the ordinary line', async () => {
+    const out = await warnFor(userWhoseMethodReadsBackAs('api_key', { tenantId: 'ks1504-t3', connectorId: 'ks1504-c3' }));
+    expect(out).toHaveLength(1);
+    expect(out[0]).toContain('machine caller ks1504-c3 (api_key, tenant ks1504-t3) has no rateLimit');
+  });
+
+  it('RED KS-1504 an authMethod holding a newline and a forged line is ONE log line with no raw line break', async () => {
+    const out = await warnFor(userWhoseMethodReadsBackAs('api_key\n[rateLimit] forged', { tenantId: 'ks1504-t4', connectorId: 'ks1504-c4' }));
+    expect(out, 'one request, one warning').toHaveLength(1);
+    expect(out[0].split(/\r\n|\r|\n/), 'no raw LF or CR survives into the line').toHaveLength(1);
+  });
+
+  it('RED KS-1504 the newline is written as the two characters backslash and n', async () => {
+    const out = await warnFor(userWhoseMethodReadsBackAs('api_key\n[rateLimit] forged', { tenantId: 'ks1504-t5', connectorId: 'ks1504-c5' }));
+    expect(out).toHaveLength(1);
+    expect(out[0]).toContain('(api_key\\n[rateLimit] forged, tenant ks1504-t5)');
+  });
+
+  it('RED KS-1504 the Unicode line and paragraph separators in an authMethod are escaped too', async () => {
+    const out = await warnFor(userWhoseMethodReadsBackAs('api_key' + String.fromCharCode(0x2028) + 'a' + String.fromCharCode(0x2029) + 'b', { tenantId: 'ks1504-t6', connectorId: 'ks1504-c6' }));
+    expect(out).toHaveLength(1);
+    expect(/[\u2028\u2029]/.test(out[0]), 'neither U+2028 nor U+2029 is raw in the line').toBe(false);
+  });
+});
```
