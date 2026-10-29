# READY — KS-1733-KS-1733-R8-STATUSCASE (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1733_p1_status_case/out.md.checker/patch.diff`** (from `ls` at 07:03 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1733_p1_status_case/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 07:03 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1733_p1_status_case/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7152ac669d2d6af08be5b9dcd35132818377155d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/governance/src/types/governance.types.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	0	Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (14 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 16 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 14 line(s) byte-exact incl. leading whitespace (of 14; 16 line(s) added by the apply)` [a3i_indent.out: `OK 14 line(s) byte-exact incl. leading whitespace (of 14; 16 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/governance/src/types/governance.types.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `34d8fe7c8a8018c6` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/governance/src/types/governance.types.ts:353)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1733_p1_status_case_062939/clone/Blockchain/Dev/services/governance/src/types/governance.types.ts:353: 'export const PROPOSAL_STATUS_LIST_PATTERN = new RegExp(`^(?:${STATUS_ALTERNATION})(?:,(?:${STATUS_ALTERNATION}))*$`);' -> "export const PROPOSAL_STATUS_LIST_PATTERN = new RegExp(`^(?:${STATUS_ALTERNATION})(?:,(?:${STATUS_ALTERNATION}))*$`, 'i');"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/governance/src/types/governance.types.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 353. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts fails at the untouched tip (3 failed / 48 run; controls green; assertion reds)` [red_first.json: failed=3 of total=48; red cell(s): ['KS-1722 category and status: present but unusable is refused RED KS-1733 R8 an upper-case status -> 400, never reaches SQL', 'KS-1722 category and status: present but unusable is refused RED KS-1733 R8 a capitalised status -> 400, never reaches SQL', 'KS-1722 category and status: present but unusable is refused RED KS-1733 R8 one capitalised part in a list -> 400, never reaches SQL']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts passes with the product hunk (48 passed / 48 run)` [green_after.json: failed=0 of total=48, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=162 failed=0 | after: total=167 failed=0` · `NEW reds: []` [baseline_suite.json total=162 failed=0; after_suite.json total=167 failed=0]
- A6 [verbatim]: `PASS A6 whole services/governance suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/governance: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +16/-0 test=src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts` (+16/-0 per numstat.out); the product `Blockchain/Dev/services/governance/src/types/governance.types.ts` is the tamper target and is byte-unchanged (sha256 34d8fe7c8a8018c6, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `7152ac669d2d6af08be5b9dcd35132818377155d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1733_p1_status_case/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1733_p1_status_case/checker.out`.

```diff
--- a/Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts
+++ b/Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts
@@ -254,4 +254,20 @@
   it('R7 one bad filter refuses the request even beside good ones -> 400', async () => {
     expectRefused(await list('?status=active&proposerId='));
   });
+
+  // KS-1733 item 2 (gate on #1696, Minor 2): no cell pinned upper case, so a case-insensitive status check stayed green on all 43 cells above. The policy pinned here is the one at the tip: lower case only.
+  it.each([
+    ['an upper-case status', '?status=ACTIVE'],
+    ['a capitalised status', '?status=Active'],
+    ['one capitalised part in a list', '?status=active%2CQueued'],
+  ])('RED KS-1733 R8 %s -> 400, never reaches SQL', async (_label, q) => {
+    expectRefused(await list(q));
+  });
+
+  it.each([
+    ['an upper-case category', '?category=GENERAL'],
+    ['a capitalised category', '?category=General'],
+  ])('control KS-1733 R9 %s -> 400 (the category enum is exact-case)', async (_label, q) => {
+    expectRefused(await list(q));
+  });
 });
```
