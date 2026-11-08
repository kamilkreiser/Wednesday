# READY - KS-2130-KS-2130-O112-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2130_o112_p1_ks1547_abort_sentence_pinned_whole/out.md.checker/patch.diff` (from `ls` at 09:59 2026-11-09; sha256[:16] 0cb61b2a8b146b47, 1455 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: BYTE-IDENTICAL.

**Held 09:59 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2130_o112_p1_ks1547_abort_sentence_pinned_whole/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `64671e97ce628c0a959515f3c30991f640f59d80`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh']; `+` lines 5 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/scripts/preflight/preflight.sh` blob 3341bab014f1; plant file(s) also unchanged.
- Red cells [input.json]:
  - `RED KS-2130 the abort text states the whole sentence`
- Red evidence under the plant [red_with_plant__*.out, the suite's own FAIL line per red cell, verbatim]:
  - `FAIL RED KS-2130 the abort text states the whole sentence: a glued denominator cannot read as the right total, digits after a separator are not checked`
- Plant file(s) [input.json plant_diff / plant; applied in the checker's clone only]: ['Blockchain/Dev/scripts/preflight/preflight.sh']
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 named cell(s) exist and pass on the unmodified product; declared suites 27 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 26 -> 27 (none lost); 12 sibling suite(s) 334 -> 334 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 named cell(s) print the suite's own FAIL line under the plant (Blockchain/Dev/scripts/preflight/preflight.sh) and pass without it; rc [1]; e.g. ks1547_preflight_step_header_denominator.test.sh: FAIL RED KS-2130 the abort text states the whole sentence: a`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 26 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh': 0}; 12 sibling suite(s) 334 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
@@ -139,6 +139,11 @@
 # F2 (red on develop): the text claimed a doubled or stale denominator cannot read as the right total, which is true only of the shape glued straight after the digits.
 call_step "3/$TOTAL/17  Title"
 expect "RED KS-1613 F2 the abort text states that digits after a separator are not checked" "yes" "$(has 'Digits after a separator')"
+# KS-2130 (gate 247 F69-1): the two cells above pin the phrases "a closing parenthesis" and "Digits after a separator", so an inverted sentence that keeps them
+# (gate 247 planted "are checked.", a wrong example, "can read as the right total") passed 26 of 26. This cell pins the WHOLE sentence, whole line 3 of the abort.
+call_step "3/$TOTAL/17  Title"
+expect "RED KS-2130 the abort text states the whole sentence: a glued denominator cannot read as the right total, digits after a separator are not checked" "yes" \
+  "$(has "so a doubled or stale denominator glued to the digits (3/$TOTAL/17) cannot read as the right total. Digits after a separator (3/$TOTAL:17) are not checked.")"
 call_step "3/$TOTAL:17  Title"
 expect "PIN KS-1613 F2 digits after an allowed separator are accepted: a stated limit of the rule, which the abort text now says" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
```
