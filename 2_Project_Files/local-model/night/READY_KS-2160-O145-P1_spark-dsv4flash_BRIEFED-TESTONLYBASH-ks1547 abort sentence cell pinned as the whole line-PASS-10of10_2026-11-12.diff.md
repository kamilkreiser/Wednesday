# READY - KS-2160-O145-P1 (spark-dsv4flash, briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2160_o145_p1_ks1547_abort_sentence_pinned_as_the_whole_line/out.md.checker/patch.diff` (from `ls` at 00:45 2026-11-12; sha256[:16] 47458dd3994d1abf, 1193 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: BYTE-IDENTICAL.

**Held 00:45 2026-11-12 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2160_o145_p1_ks1547_abort_sentence_pinned_as_the_whole_line/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `cb46c28eef6f6aa761111f4737e53f3de1e43d74`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2160_o145_p1_ks1547_abort_sentence_pinned_as_the_whole_line/KS-2160.md`
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh']; `+` lines 1 (ASCII), `-` lines 1.
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
  - `PASS A3p the plant applies at the tip (1 pinned line(s))`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 named cell(s) exist and pass on the unmodified product; declared suites 27 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 27 -> 27 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 named cell(s) print the suite's own FAIL line under the plant (Blockchain/Dev/scripts/preflight/preflight.sh) and pass without it; rc [1]; e.g. ks1547_preflight_step_header_denominator.test.sh: FAIL RED KS-2130 the abort text states the whole sentence: a`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 27 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh': 0}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
  - `INFO named cell(s) already present at the tip (changed in place, or the gap is already pinned): ['ks1547_preflight_step_header_denominator.test.sh :: RED KS-2130 the abort text states the whole sentence: a glued denominator cannot read as the right total, digits after a separator are not checked']`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
@@ -143,7 +143,7 @@
 # (gate 247 planted "are checked.", a wrong example, "can read as the right total") passed 26 of 26. This cell pins the WHOLE sentence, whole line 3 of the abort.
 call_step "3/$TOTAL/17  Title"
 expect "RED KS-2130 the abort text states the whole sentence: a glued denominator cannot read as the right total, digits after a separator are not checked" "yes" \
-  "$(has "so a doubled or stale denominator glued to the digits (3/$TOTAL/17) cannot read as the right total. Digits after a separator (3/$TOTAL:17) are not checked.")"
+  "$(if grep -q -x -F -- "  so a doubled or stale denominator glued to the digits (3/$TOTAL/17) cannot read as the right total. Digits after a separator (3/$TOTAL:17) are not checked." "$tmp/out.txt"; then echo yes; else echo no; fi)"
 call_step "3/$TOTAL:17  Title"
 expect "PIN KS-1613 F2 digits after an allowed separator are accepted: a stated limit of the rule, which the abort text now says" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
```

> NOTE (operator o145, 2026-11-12): TEST-ONLY bash tier, PLANT shape (append ' BUT ACTUALLY THEY ARE.' to preflight.sh:246); read the + line of golden at source. Label unchanged, one hunk.
