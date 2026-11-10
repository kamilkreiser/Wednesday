# READY - KS-2156-KS-2156-O132-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/expect) - PASS 11/11 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2156_o132_p1_ks1728_closed_pipe_scanner_reads_path_wrapped_egrep_and_silent_spellings/out.md.checker/patch.diff` (from `ls` at 15:35 2026-11-10; sha256[:16] 85311716f3c80782, 1873 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 15:35 2026-11-10 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2156_o132_p1_ks1728_closed_pipe_scanner_reads_path_wrapped_egrep_and_silent_spellings/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `0e6479d7b6c06b6f8a77aae1cbad167afbdaa089`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh']; `+` lines 8 (ASCII), `-` lines 2.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `systemTest/scripts/setup-env.sh` blob 36c92165072c.
- Red cells [input.json]:
  - (expect shape: see the expectations below)
- Red evidence (expect shape) [checker.out, verbatim]: A4b (expectations FAIL at the untouched tip), A4e (hold after the patch), A7 (patch reverse-applied, every expectation fails again):
  - `PASS A4b RED AT BASE: all 2 expectation(s) fail on the untouched tip's suite output`
  - `PASS A4e EXPECTATIONS AFTER: all 2 expectation(s) hold on the patched suite's output`
  - `PASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)`
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh)`
  - `PASS A4b RED AT BASE: all 2 expectation(s) fail on the untouched tip's suite output`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 0 named cell(s) exist and pass on the unmodified product; declared suites 31 cells, 0 red, rc [0]`
  - `PASS A4e EXPECTATIONS AFTER: all 2 expectation(s) hold on the patched suite's output`
  - `PASS A6 WHOLE SUITE no worse: declared cells 31 -> 31 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 31 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh': 0}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (expect shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the expectation set against the suite output (A4b/A4e/A7). DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh
@@ -38,8 +38,9 @@ check() {
     else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
 }
 
-# The class: a pipe into a grep whose option cluster contains q (or --quiet), wherever the flag sits among the grep's words and whatever feeds the pipe (printf, echo).
-CLASS='\|[[:space:]]*grep[[:space:]]([^|]*[[:space:]])?(-[A-Za-z]*q[A-Za-z]*|--quiet)([[:space:]]|$)'
+# The class: a pipe into a quiet grep (an option cluster containing q, --quiet or --silent), wherever the flag sits among the grep's words and whatever feeds the pipe (printf, echo).
+# The grep may be plain, path-qualified (/usr/bin/grep), wrapped (command grep) or egrep or fgrep. A grep held in a variable ($G -q) is NOT read: out of scope (KS-2156).
+CLASS='\|[[:space:]]*((command|builtin)[[:space:]]+)?([^[:space:]|]*/)?(e|f)?grep[[:space:]]([^|]*[[:space:]])?(-[A-Za-z]*q[A-Za-z]*|--quiet|--silent)([[:space:]]|$)'
 # class_lines <file>: how many lines of the file are in the class (0 when the file is missing, which the existence cell reports separately).
 class_lines() { [[ -f "$1" ]] && { grep -c -E -e "$CLASS" "$1" || true; } || echo missing; }
 
@@ -76,6 +77,11 @@ echo "$x" | GREP -E -q 'a|b'
 echo "$x" | GREP -q 'a'
 printf '%s|' "$x" | GREP -q 'a'
 printf '%s' "$x" | GREP --quiet 'a'
+echo "$x" | /usr/bin/GREP -q 'a'
+echo "$x" | command GREP -q 'a'
+echo "$x" | eGREP -q 'a|b'
+echo "$x" | fGREP -q 'a'
+echo "$x" | GREP --silent 'a'
 MISSED_SPELLINGS
 check "CONTROL the scanner counts every spelling the first regex missed as 1 line ($total spellings)" "$total" "$seen"
 printf '%s\n' "$G"' -Fqx "$1" "$TRUNCATED" || return 0' > "$T/nopipe.sh"
```
