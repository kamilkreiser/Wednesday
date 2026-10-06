# READY — KS-1328-DB-RETRY-DESCRIBE-BUDGET-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1328-db-retry-describe-budget/out.md.checker/patch.diff`** (from `ls` at 12:58 2026-10-06; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1328-db-retry-describe-budget/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1328-db-retry-describe-budget-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (db.retry.test.ts, sha256 equal).

**Held 12:58 2026-10-06 by Spark review sub-agent for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1328-db-retry-describe-budget/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts } — one file that is both the product and its test (under Blockchain/Dev/services/kyc/src/__tests__)`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts` (product) and `Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
13	2	Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (11 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 13 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 11 line(s) byte-exact incl. leading whitespace (of 11; 12 line(s) added by the apply)` [a3i_indent.out: `OK 11 line(s) byte-exact incl. leading whitespace (of 11; 12 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/db.retry.test.ts fails at the untouched tip (1 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=1 of total=6; red cell(s): ['db availability retry (KS-377) KS-1328: every cell in this file carries the 60 s budget, not the 5 s default']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/db.retry.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=33 failed=0 | after: total=34 failed=0` · `NEW reds: []` [baseline_suite.json total=33 failed=0; after_suite.json total=34 failed=0]
- A6 [verbatim]: `PASS A6 whole services/kyc suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/kyc: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +13/-2 test=src/__tests__/db.retry.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts` (+13/-2 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1328-db-retry-describe-budget/input.json`. Brief (given by --brief; its `# ` heading names KS-1328): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1328-db-retry-describe-budget/KS-1328.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1328-db-retry-describe-budget/checker.out`.

```diff
--- a/Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts
+++ b/Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts
@@ -36,4 +36,7 @@ async function importDb() {
 const DB_UP = { rows: [{ ok: 1 }] };
-
-describe('db availability retry (KS-377)', () => {
+
+// KS-1328: this file runs on a 60 s budget instead of vitest's 5 s default. Under fleet load the first cell
+// timed out at 11498 ms while passing in 675 ms alone: the overrun is scheduling, not work (the KS-1155 class).
+// The budget sits on this describe only, so every other kyc suite keeps the 5 s default.
+describe('db availability retry (KS-377)', { timeout: 60_000 }, () => {
   // Silence db.ts's structured console.log lines; restored per test below.
@@ -133,2 +136,10 @@ describe('db availability retry (KS-377)', () => {
   });
+
+  it('KS-1328: every cell in this file carries the 60 s budget, not the 5 s default', ({ task }) => {
+    const cells = task.suite?.tasks ?? [];
+    expect(cells.length).toBe(6);
+    for (const cell of cells) {
+      expect((cell as { timeout?: number }).timeout).toBe(60_000);
+    }
+  });
 });
```
