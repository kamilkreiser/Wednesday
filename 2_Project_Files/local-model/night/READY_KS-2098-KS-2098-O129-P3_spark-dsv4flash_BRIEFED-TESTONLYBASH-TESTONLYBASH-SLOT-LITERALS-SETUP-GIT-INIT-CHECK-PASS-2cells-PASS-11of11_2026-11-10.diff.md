# READY - KS-2098-KS-2098-O129-P3 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/expect) - PASS 11/11 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2098_o129_p3_slot_literals_suite_names_a_failed_git_init_in_its_controls/out.md.checker/patch.diff` (from `ls` at 07:53 2026-11-10; sha256[:16] e8290dbb1bdf3fa7, 1694 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 07:53 2026-11-10 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2098_o129_p3_slot_literals_suite_names_a_failed_git_init_in_its_controls/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `0d286210f98b1bd549ff67cec20746648654d501`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['systemTest/__tests__/no_hardcoded_slot_literals.test.sh']; `+` lines 4 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `systemTest/__tests__/support/slot-expect.sh` blob 9bc46a0f07dc.
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
  - `PASS A3 touched set == the brief's declared set (systemTest/__tests__/no_hardcoded_slot_literals.test.sh)`
  - `PASS A4b RED AT BASE: all 2 expectation(s) fail on the untouched tip's suite output`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 0 named cell(s) exist and pass on the unmodified product; declared suites 13 cells, 0 red, rc [0]`
  - `PASS A4e EXPECTATIONS AFTER: all 2 expectation(s) hold on the patched suite's output`
  - `PASS A6 WHOLE SUITE no worse: declared cells 11 -> 13 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A7 REVERSION: with the patch reverse-applied, 2/2 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 11 cell(s), 0 FAIL line(s), rc {'systemTest/__tests__/no_hardcoded_slot_literals.test.sh': 0}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (expect shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the expectation set against the suite output (A4b/A4e/A7). DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/systemTest/__tests__/no_hardcoded_slot_literals.test.sh
+++ b/systemTest/__tests__/no_hardcoded_slot_literals.test.sh
@@ -155,6 +155,8 @@ echo "== POSITIVE CONTROL: a planted literal is found, in every family and shape
 mkdir -p "$TMP/st"
 # The scan lists files through git (KS-1386), so the control tree is a git work tree from the start.
 git -C "$TMP/st" init -q 2>/dev/null
+if [[ "$(git -C "$TMP/st" rev-parse --is-inside-work-tree 2>/dev/null)" == "true" ]]; then ok "SETUP: the planted-control tree is a git work tree"
+else bad "SETUP: git init did not make the planted-control tree a git work tree, so the controls below would read as a scan that found nothing" "     $TMP/st"; fi
 for r in "${CONTROL_ROOTS[@]}"; do [[ -d "$ST/$r" ]] && mkdir -p "$TMP/st/$(dirname "$r")" && cp -R "$ST/$r" "$TMP/st/$r"; done
 rm -rf "$TMP/st/fixtures/generated" "$TMP/st/performance/tests/unit/fixtures/node_modules" 2>/dev/null
 plant="$TMP/st/fixtures/planted.ts"
@@ -226,6 +228,8 @@ else
   # so ONLY the membership check can catch it.
   ctl="$TMP/ctl"; mkdir -p "$ctl/$(dirname "$PROVENANCE_FILE")"
   git -C "$ctl" init -q 2>/dev/null
+  if [[ "$(git -C "$ctl" rev-parse --is-inside-work-tree 2>/dev/null)" == "true" ]]; then ok "SETUP: the provenance-control tree is a git work tree"
+  else bad "SETUP: git init did not make the provenance-control tree a git work tree, so its control would read as a scan that found nothing" "     $ctl"; fi
   # The planted id's slot token is COMPUTED, exactly as the other controls compute theirs, so
   # this file never itself holds a slot 2..MAX literal (the guard scans __tests__).
   ctl_id="pre-merge-ks-0000-2026-01-01T00-00-00Z-$(se_tag 2)"
```
