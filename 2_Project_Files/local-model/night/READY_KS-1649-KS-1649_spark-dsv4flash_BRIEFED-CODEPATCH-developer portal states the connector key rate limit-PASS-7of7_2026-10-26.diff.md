# READY — KS-1649-KS-1649 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1649_p1/out.md.checker/patch.diff`** (from `ls` at 09:20 2026-10-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1649_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1649_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1649_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 09:20 2026-10-26 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1649_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html , Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html
32	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1649 - developer-portal.html rate-limit row RED KS-1649 R1 the row says Platform S connector keys are minted at 3,000 req/hour', 'KS-1649 - developer-portal.html rate-limit row RED KS-1649 R2 the row says X-RateLimit-Limit is the actual ceiling for the key']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1175 failed=0 | after: total=1179 failed=0` · `NEW reds: []` [baseline_suite.json total=1175 failed=0; after_suite.json total=1179 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +33/-1 test=src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts` (+32/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1649_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1649): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1649_p1/KS-1649.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1649_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html b/Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html
--- a/Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html
+++ b/Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html
@@ -561,7 +561,7 @@
     <p>Rate limits are enforced per API key / OAuth app. Regular users (JWT) are subject to global limits only.</p>
     <table>
       <tr><th>Scope</th><th>Default Limit</th><th>Headers</th></tr>
-      <tr><td>Per API key / OAuth app</td><td>1,000 req/hour</td><td><code>X-RateLimit-Limit</code>, <code>X-RateLimit-Remaining</code>, <code>X-RateLimit-Reset</code></td></tr>
+      <tr><td>Per API key / OAuth app</td><td>1,000 req/hour by default; Platform S connector keys are minted at 3,000 req/hour</td><td><code>X-RateLimit-Limit</code> (the actual ceiling for the key, on every response), <code>X-RateLimit-Remaining</code>, <code>X-RateLimit-Reset</code></td></tr>
       <tr><td>Login endpoint</td><td>15 req/min</td><td>—</td></tr>
       <tr><td>Registration</td><td>5 req/min</td><td>—</td></tr>
       <tr><td>Verification (public)</td><td>No limit</td><td>Exempt from rate limiting</td></tr>
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1649-developer-portal-states-the-connector-key-rate-limit.test.ts
@@ -0,0 +1,32 @@
+/**
+ * KS-1649 - the developer portal's rate-limit table states the Platform S connector key ceiling.
+ *
+ * services/api-gateway/src/docs/developer-portal.html listed ONE default rate limit for every API key, "1,000 req/hour". That stays true
+ * for a key minted without an explicit rateLimit (the security service's schema default), but keys that
+ * POST /api/platform/organizations/register-connector mints for Platform S are minted at 3,000 req/hour (KS-1195). The row must say both,
+ * and must say that X-RateLimit-Limit reports the actual ceiling on every response.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const html = readFileSync(join(__dirname, '..', 'docs', 'developer-portal.html'), 'utf8');
+const row = html.split('\n').find((l) => l.includes('<td>Per API key / OAuth app</td>')) ?? '';
+
+describe('KS-1649 - developer-portal.html rate-limit row', () => {
+  it('RED KS-1649 R1 the row says Platform S connector keys are minted at 3,000 req/hour', () => {
+    expect(row).toContain('Platform S connector keys are minted at 3,000 req/hour');
+  });
+
+  it('RED KS-1649 R2 the row says X-RateLimit-Limit is the actual ceiling for the key', () => {
+    expect(row).toContain('(the actual ceiling for the key, on every response)');
+  });
+
+  it('CONTROL KS-1649 C1 the per-key default is still stated as 1,000 req/hour', () => {
+    expect(row).toContain('1,000 req/hour');
+  });
+
+  it('CONTROL KS-1649 C2 the row still lists all three rate-limit headers', () => {
+    expect(['X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset'].filter((h) => !row.includes(h))).toEqual([]);
+  });
+});
```
