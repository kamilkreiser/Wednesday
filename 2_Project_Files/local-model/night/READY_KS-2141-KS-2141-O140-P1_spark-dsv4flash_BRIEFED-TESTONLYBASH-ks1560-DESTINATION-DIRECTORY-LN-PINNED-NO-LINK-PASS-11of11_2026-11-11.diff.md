# READY - KS-2141-KS-2141-O140-P1 (spark-dsv4flash, briefed, test_only_bash/expect) - PASS 11/11 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2141_o140_p1_ks1560_destination_directory_link_spelling_pinned_as_no_link/out.md.checker/patch.diff` (from `ls` at 16:48 2026-11-11; sha256[:16] 3b284b96353d39d7, 1162 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 16:48 2026-11-11 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2141_o140_p1_ks1560_destination_directory_link_spelling_pinned_as_no_link/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `6911aa643db13ad1d09b37dd69c38df01cb029a4`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2141_o140_p1_ks1560_destination_directory_link_spelling_pinned_as_no_link/KS-2141.md`
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh']; `+` lines 5 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` blob 4112941ddbe5.
- Red cells [input.json]:
  - (expect shape: see the expectations below)
- Red evidence (expect shape) [checker.out, verbatim]: A4b (expectations FAIL at the untouched tip), A4e (hold after the patch), A7 (patch reverse-applied, every expectation fails again):
  - `PASS A4b RED AT BASE: all 1 expectation(s) fail on the untouched tip's suite output`
  - `PASS A4e EXPECTATIONS AFTER: all 1 expectation(s) hold on the patched suite's output`
  - `PASS A7 REVERSION: with the patch reverse-applied, 1/1 expectation(s) fail again (the check discriminates)`
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh)`
  - `PASS A4b RED AT BASE: all 1 expectation(s) fail on the untouched tip's suite output`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 0 named cell(s) exist and pass on the unmodified product; declared suites 15 cells, 0 red, rc [0]`
  - `PASS A4e EXPECTATIONS AFTER: all 1 expectation(s) hold on the patched suite's output`
  - `PASS A6 WHOLE SUITE no worse: declared cells 14 -> 15 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A7 REVERSION: with the patch reverse-applied, 1/1 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 14 cell(s), 0 FAIL line(s), rc {'Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh': 0}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (expect shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the expectation set against the suite output (A4b/A4e/A7). DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh
@@ -116,6 +116,11 @@
 check "F-2078-1 every legitimate respelling of the link statement is judged a link ($total spellings)" "$total" "$accepted"
 printf '%s\n' 'ln -sf \' '    "$JQ_BIN" "$root/bin/jq"' > "$FX/continued.sh"
 check "F-2078-1 a backslash-continued ln -sf is judged a link" "yes" "$(verdict "$FX/continued.sh")"
+
+# KS-2141 (pin, not a fix): a link into the stub DIRECTORY (`ln -sf "$JQ_BIN" "$root/bin/"`, the destination names no jq) is judged NO link by
+# the predicate today. Whether links_jq should widen to read it is a design choice; this cell pins the current answer so a change is deliberate.
+printf '%s\n' 'ln -sf "$JQ_BIN" "$root/bin/"' > "$FX/dest_dir.sh"
+check "KS-2141 PIN the destination-directory spelling (the stub dir named, no jq in the destination) is judged no link, the current answer" "no" "$(verdict "$FX/dest_dir.sh")"
 
 # KS-2141 F-2078-2: a trailing comment or a trailing word that names bin/jq on another statement is NOT a link.
 rejected=0; total=0
```

> NOTE (operator o140, 2026-11-11): Pure pin, GREEN at the tip; the model output omitted only the diff --git header line (golden TREE-IDENTICAL, not byte). links_jq NOT widened (design choice). Same suite is touched by an unheld KS-2154 brief (o129 p1): hunks do not overlap, second to merge rebases offsets.
