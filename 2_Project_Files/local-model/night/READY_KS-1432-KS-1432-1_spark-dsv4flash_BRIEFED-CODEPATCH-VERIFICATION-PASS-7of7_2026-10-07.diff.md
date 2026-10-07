# READY — KS-1432-KS-1432-1 (Spark DeepSeek V4 Flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/out.md.checker/patch.diff`** (from `ls` at 11:57 2026-10-07; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate-control/out.md.checker/patch.diff` rc 0, Wednesday late-morning seat).

**Held 11:57 2026-10-07 by Wednesday late-morning seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/verification.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
11	2	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
20	4	Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 11 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 9 line(s) byte-exact incl. leading whitespace (of 9; 10 line(s) added by the apply)` [a3i_indent.out: `OK 9 line(s) byte-exact incl. leading whitespace (of 9; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks529-non-object-body-guard.test.ts fails at the untouched tip (9 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=9 of total=10; red cell(s): ['KS-1432 - the guard under test is the one the route uses RED KS-1432 R1: routes/verification.ts exports the guard as isAcceptableDocumentBody', 'KS-529 — non-object request bodies are refused, not crashed on refuses a literal null body (the exact DoS payload)', 'KS-529 — non-object request bodies are refused, not crashed on refuses a array body', 'KS-529 — non-object request bodies are refused, not crashed on refuses a number body', 'KS-529 — non-object request bodies are refused, not crashed on refuses a string body', 'KS-529 — non-object request bodies are refused, not crashed on refuses a boolean body', 'KS-529 — non-object request bodies are refused, not crashed on accepts a empty object body', 'KS-529 — non-object request bodies are refused, not crashed on accepts a populated object body', 'KS-529 — non-object request bodies are refused, not crashed on the guard is what stops the null-deref that killed the process']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks529-non-object-body-guard.test.ts passes with the product hunk (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=818 failed=0 | after: total=820 failed=0` · `NEW reds: []` [baseline_suite.json total=818 failed=0; after_suite.json total=820 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +31/-6 test=src/__tests__/ks529-non-object-body-guard.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+11/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts` (+20/-4); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -259,3 +259,12 @@
 }
-
+
+/**
+ * KS-529 / KS-1432: the POST /api/documents body guard. `JSON.parse` returns whatever the document was (a
+ * literal null, a number, a string, an array); only a non-null, non-array object is an acceptable body.
+ * Exported so the unit test exercises THIS predicate rather than a copy of it.
+ */
+export function isAcceptableDocumentBody(parsed: unknown): boolean {
+  return !(parsed === null || typeof parsed !== 'object' || Array.isArray(parsed));
+}
+
 /**
@@ -1151,3 +1160,3 @@
         // KS-501, which fixed the non-string case but not the non-object one.
-        if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
+        if (!isAcceptableDocumentBody(parsed)) {
           res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Request body must be a JSON object' } });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts
@@ -22,6 +22,22 @@
 import { describe, it, expect } from 'vitest';
-
-/** Mirrors the guard in routes/verification.ts POST /api/documents. */
-function isAcceptableBody(parsed: unknown): boolean {
-  return !(parsed === null || typeof parsed !== 'object' || Array.isArray(parsed));
+import * as verification from '../routes/verification';
+
+// KS-1432: this file used to define its own COPY of the guard, so deleting the real check left it green.
+// It now calls the predicate routes/verification.ts exports and uses at the POST /api/documents call site.
+const realGuard = (verification as Record<string, unknown>).isAcceptableDocumentBody as
+  | ((parsed: unknown) => boolean)
+  | undefined;
+
+describe('KS-1432 - the guard under test is the one the route uses', () => {
+  it('RED KS-1432 R1: routes/verification.ts exports the guard as isAcceptableDocumentBody', () => {
+    expect(typeof realGuard).toBe('function');
+  });
+
+  it('control KS-1432 C1: the route module still exports createVerificationRoutes', () => {
+    expect(typeof verification.createVerificationRoutes).toBe('function');
+  });
+});
+
+function isAcceptableBody(parsed: unknown): boolean | undefined {
+  return realGuard?.(parsed);
 }
```
