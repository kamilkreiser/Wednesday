# READY - KS-2132-KS-2132-O110-P1 (spark-dsv4flash, briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2132_o110_p1_connector_allow_list_non_string_at_the_last_index/out.md.checker/patch.diff` (from `ls` at 06:51 2026-11-09; sha256[:16] 2fa99a7f1c62ac8e, 1007 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 06:51 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2132_o110_p1_connector_allow_list_non_string_at_the_last_index/out.md.checker`; product bytes were RE-MEASURED here.** Tip `5d6a95c552fd131a166776076d951666b6de7329`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-an-allow-list-of-non-strings-is-refused-by-both-reads.test.ts']; `+` lines 3 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/services/connectorAllowList.ts` blob 28327cb4e31e; plant file(s) also unchanged.
- Red cells [input.json]:
  - `KS-1534 R1 the info reader refuses every non-string list`
  - `KS-1534 R2 the create path refuses every non-string list naming SSD_DOCUMENT`
  - `KS-1534 R5 the shared text is ONE exported constant`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-an-allow-list-of-non-strings-is-refused-by-both-reads.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 3 red cell(s) exist and pass on the unmodified product; declared files 11 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1880 -> 1880, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 3 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/services/connectorAllowList.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-an-allow-list-of-non-strings-is-refused-by-both-reads.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-an-allow-list-of-non-strings-is-refused-by-both-reads.test.ts
@@ -64,6 +64,9 @@
   // non-string where an ends-only (or first-few-only) check cannot see it. Both flow into R1 to R5. They are GREEN on develop by design.
   ['a number in the MIDDLE of three strings', ['SSD_DOCUMENT', 1, 'X']],
   ['a null at index 3 of five strings', ['SSD_DOCUMENT', 'X', 'Y', null, 'Z']],
+  // KS-2132 (gate 249 F-1): the non-string at the LAST index of a list of three or more. A loop that skipped the last element of such a list survived 11 of 11.
+  ['a number LAST of four strings', ['SSD_DOCUMENT', 'X', 'Y', 1]],
+  ['a null at index 4, the last, of five', ['SSD_DOCUMENT', 'X', 'Y', 'Z', null]],
 ];
 /** Present values that are not arrays: they keep the older refusal text. */
 const NON_ARRAYS: Array<[string, unknown]> = [
```
