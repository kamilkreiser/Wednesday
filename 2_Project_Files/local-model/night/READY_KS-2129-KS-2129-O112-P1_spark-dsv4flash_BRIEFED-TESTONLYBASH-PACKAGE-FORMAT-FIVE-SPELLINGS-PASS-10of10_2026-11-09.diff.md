# READY - KS-2129-KS-2129-O112-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2129_o112_p1_ks1728_scanner_misses_five_spellings_of_the_closed_pipe_fault/out.md.checker/patch.diff` (from `ls` at 09:59 2026-11-09; sha256[:16] f4b11306382512da, 2397 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: BYTE-IDENTICAL.

**Held 09:59 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2129_o112_p1_ks1728_scanner_misses_five_spellings_of_the_closed_pipe_fault/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `64671e97ce628c0a959515f3c30991f640f59d80`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh']; `+` lines 19 (ASCII), `-` lines 2.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `systemTest/scripts/check-package-format.sh` blob 2b4d5d0fd35e; plant file(s) also unchanged.
- Red cells [input.json]:
  - `Blockchain/Dev/scripts/rls/verify-fail-closed.sh has no line with a printf piped into grep -q`
  - `systemTest/akto/scripts/update-akto-images.sh has no line with a printf piped into grep -q`
  - `Blockchain/Dev/scripts/preflight/action-pins-labelled.sh has no line with a printf piped into grep -q`
  - `Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh has no line with a printf piped into grep -q`
  - `systemTest/scripts/check-package-format.sh has no line with a printf piped into grep -q`
- Red evidence under the plant [red_with_plant__*.out, the suite's own FAIL line per red cell, verbatim]:
  - `FAIL Blockchain/Dev/scripts/rls/verify-fail-closed.sh has no line with a printf piped into grep -q`
  - `FAIL systemTest/akto/scripts/update-akto-images.sh has no line with a printf piped into grep -q`
  - `FAIL Blockchain/Dev/scripts/preflight/action-pins-labelled.sh has no line with a printf piped into grep -q`
  - `FAIL Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh has no line with a printf piped into grep -q`
  - `FAIL systemTest/scripts/check-package-format.sh has no line with a printf piped into grep -q`
- Plant file(s) [input.json plant_diff / plant; applied in the checker's clone only]: ['Blockchain/Dev/scripts/preflight/action-pins-labelled.sh', 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh', 'Blockchain/Dev/scripts/rls/verify-fail-closed.sh', 'systemTest/akto/scripts/update-akto-images.sh', 'systemTest/scripts/check-package-format.sh']
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 5 named cell(s) exist and pass on the unmodified product; declared suites 31 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 29 -> 31 (none lost); 5 sibling suite(s) 147 -> 147 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 5 named cell(s) print the suite's own FAIL line under the plant (Blockchain/Dev/scripts/rls/verify-fail-closed.sh, systemTest/akto/scripts/update-akto-images.sh, Blockchain/Dev/scripts/preflight/action-pins-labelled.sh, systemTest/scripts/check-package-format.sh, Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh) and pass without it; rc [1]; e.g. ks1728_product_scripts_grade_without_a_closing_pipe.test.sh: FAIL Blockchain/Dev/scripts/rls/verify-fail-close`
  - `PASS A8 RESTORE: 6 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 29 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh': 0}; 5 sibling suite(s) 147 cell(s), 0 FAIL line(s)`
  - `INFO named cell(s) already present at the tip (changed in place, or the gap is already pinned): ['ks1728_product_scripts_grade_without_a_closing_pipe.test.sh :: Blockchain/Dev/scripts/preflight/action-pins-labelled.sh has no line with a printf piped into grep -q', 'ks1728_product_scripts_grade_without_a_closing_pipe.test.sh :: Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh has no line with a printf piped into grep -q', 'ks1728_product_scripts_grade_without_a_closing_pipe.test.sh :: Blockchain/Dev/scripts/rls/verify-fail-closed.sh has no line with a printf piped into grep -q']`
  - `INFO other cell(s) in the declared suites also red under the plant: ['ks1728_product_scripts_grade_without_a_closing_pipe.test.sh :: systemTest/scripts/check-package-format.sh holds exactly one: grep -xF "$full" >/dev/null']`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1728_product_scripts_grade_without_a_closing_pipe.test.sh
@@ -38,8 +38,8 @@
     else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
 }
 
-# The class: a printf piped into a grep whose option cluster contains q. The same regex the ticket's census uses, widened to any flag order.
-CLASS='printf [^|]*\| *grep -[A-Za-z]*q'
+# The class: a pipe into a grep whose option cluster contains q (or --quiet), wherever the flag sits among the grep's words and whatever feeds the pipe (printf, echo).
+CLASS='\|[[:space:]]*grep[[:space:]]([^|]*[[:space:]])?(-[A-Za-z]*q[A-Za-z]*|--quiet)([[:space:]]|$)'
 # class_lines <file>: how many lines of the file are in the class (0 when the file is missing, which the existence cell reports separately).
 class_lines() { [[ -f "$1" ]] && { grep -c -E -e "$CLASS" "$1" || true; } || echo missing; }
 
@@ -64,6 +64,23 @@
 printf '%s\n' "  if printf '%s' \"\$x\" | $G -qE 'a|b'; then" > "$T/flags.sh"
 check "CONTROL a flag cluster in another order (grep -qE) is still in the class" "1" "$(class_lines "$T/flags.sh")"
 
+# KS-2129 (gate 247 F74-4): spellings of the fault the first regex missed. Each fixture line is written with GREP in place of the
+# command word (split like G above, so this fixture is not itself a hit) and must be counted as 1 line.
+seen=0; total=0
+while IFS= read -r line; do
+    total=$((total + 1)); printf '%s\n' "${line//GREP/$G}" > "$T/spelling.sh"
+    [[ "$(class_lines "$T/spelling.sh")" == "1" ]] && seen=$((seen + 1))
+done <<'MISSED_SPELLINGS'
+printf '%s\n' "$x" | GREP -xF "$x" >/dev/null -q
+echo "$x" | GREP -E -q 'a|b'
+echo "$x" | GREP -q 'a'
+printf '%s|' "$x" | GREP -q 'a'
+printf '%s' "$x" | GREP --quiet 'a'
+MISSED_SPELLINGS
+check "CONTROL the scanner counts every spelling the first regex missed as 1 line ($total spellings)" "$total" "$seen"
+printf '%s\n' "$G"' -Fqx "$1" "$TRUNCATED" || return 0' > "$T/nopipe.sh"
+check "CONTROL a quiet grep with no pipe in front of it is not in the class" "0" "$(class_lines "$T/nopipe.sh")"
+
 for f in "${FILES[@]}"; do
     check "$f exists" "yes" "$([[ -f "$ROOT/$f" ]] && echo yes || echo no)"
     check "$f has no line with a printf piped into grep -q" "0" "$(class_lines "$ROOT/$f")"
```
