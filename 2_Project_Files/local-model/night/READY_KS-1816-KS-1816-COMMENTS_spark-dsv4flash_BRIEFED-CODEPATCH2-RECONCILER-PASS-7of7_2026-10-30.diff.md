# READY — KS-1816-KS-1816-COMMENTS (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1816_p2_reconciler_comments/out.md.checker/patch.diff`** (from `ls` at 07:03 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1816_p2_reconciler_comments/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1816_p2_reconciler_comments/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 07:03 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1816_p2_reconciler_comments/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7152ac669d2d6af08be5b9dcd35132818377155d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/reconciler.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/reconciler.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	3	Blockchain/Dev/services/anchoring/src/reconciler.ts
33	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: reconciler.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/reconciler.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/reconciler.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts 33 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/reconciler.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1816: the two reconciler.ts comments match the code RED KS-1816 R1 the header property no longer claims a provider error always leaves the row untouched', 'KS-1816: the two reconciler.ts comments match the code RED KS-1816 R2 the MIN_AGE comment no longer says the live loop touches updated_at as it goes']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=545 failed=1 | after: total=550 failed=1` · `NEW reds: []` [baseline_suite.json total=545 failed=1; after_suite.json total=550 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/reconciler.ts` (+7/-3 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts` (+33/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/reconciler.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7152ac669d2d6af08be5b9dcd35132818377155d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1816_p2_reconciler_comments/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1816_p2_reconciler_comments/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/reconciler.ts b/Blockchain/Dev/services/anchoring/src/reconciler.ts
--- a/Blockchain/Dev/services/anchoring/src/reconciler.ts
+++ b/Blockchain/Dev/services/anchoring/src/reconciler.ts
@@ -19,7 +19,9 @@
  *     something else — the KS-535 `All inputs are spent` class);
  *   - fabricated refs (`tx_sim_`/`mock_tx_`) are never chain-checked — KS-587
  *     owns those rows;
- *   - a chain-provider error leaves the row untouched for the next pass.
+ *   - a chain-provider error leaves the row untouched for the next pass only below
+ *     the give-up age; at or past it the same error is read as absence and the row
+ *     is marked failed (KS-1810).
  *
  * Dependency-injected so it is unit-testable without booting the service
  * (index.ts starts the HTTP listener on import).
@@ -60,8 +62,10 @@
     running = true;
     const now = deps.now ?? Date.now;
     try {
-      // MIN_AGE keeps the reconciler off rows the live submit/confirm loop is
-      // still actively working (it touches updated_at as it goes).
+      // MIN_AGE keeps the reconciler off rows that were written recently. The age is
+      // read from updated_at, which each status write moves, but the confirmation poll
+      // writes nothing between submitted and confirmed, so a row the live loop is still
+      // polling can pass MIN_AGE (KS-1816).
       const rows = await deps.query(
         `SELECT id, transaction_hash, created_at, updated_at FROM anchor_store
           -- KS-726: 'submitting' is the write-ahead state — the row NAMES a
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts
@@ -0,0 +1,33 @@
+// KS-1816 (anchoring reconciler.ts): two comments said what the code does not do. The header property claimed a chain-provider error always leaves the row untouched for the next pass
+// (past the give-up age the same error is read as absence and the row is failed). The MIN_AGE comment claimed the live loop touches updated_at as it goes (the confirmation poll writes nothing).
+// These cells read reconciler.ts as text. R1 and R2 are red until the two comments are corrected; C1 to C3 pin the code lines the comments describe, which must not move.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+
+const SRC = readFileSync(resolve(__dirname, '..', 'reconciler.ts'), 'utf8');
+
+describe('KS-1816: the two reconciler.ts comments match the code', () => {
+  it('RED KS-1816 R1 the header property no longer claims a provider error always leaves the row untouched', () => {
+    expect(SRC).not.toContain('error leaves the row untouched for the next pass.');
+    expect(SRC).toContain('only below');
+    expect(SRC).toContain('marked failed (KS-1810)');
+  });
+
+  it('RED KS-1816 R2 the MIN_AGE comment no longer says the live loop touches updated_at as it goes', () => {
+    expect(SRC).not.toContain('it touches updated_at as it goes');
+    expect(SRC).toContain('writes nothing between submitted and confirmed');
+  });
+
+  it('control KS-1816 C1 the select still ages rows by updated_at', () => {
+    expect(SRC).toContain("AND updated_at < NOW() - ($1 || ' milliseconds')::interval");
+  });
+
+  it('control KS-1816 C2 the give-up test still reads created_at', () => {
+    expect(SRC).toContain('else if (now() - new Date(row.created_at).getTime() > config.giveUpMs) {');
+  });
+
+  it('control KS-1816 C3 the file was read (the instrument is not reading an empty string)', () => {
+    expect(SRC.length).toBeGreaterThan(3000);
+  });
+});
```
