# READY — KS-1903-KS-1903-O46-P1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case/out.md.checker/patch.diff`** (from `ls` at 21:55 2026-11-01; sha256[:16] e20e6db898172f0d, 2828 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 2828 B vs golden 3122 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-dockerfile-non-root.sh 4, check_dockerfile_non_root_reports_root.test.sh 43); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 21:55 2026-11-01 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d7691f35312ea158f043e87a3227e477cccb183d`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d7691f35312ea158f043e87a3227e477cccb183d, Blockchain/Dev/scripts/check-dockerfile-non-root.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-dockerfile-non-root.sh', 'Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-dockerfile-non-root.sh , Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 3 brief `+` line(s) present; script `+` lines 4 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 0; must_change sites 0/0 each a `-` line; must_remove 0 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (+4/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` (+42/-1 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh fails at the untouched tip (rc=1, 3 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=3 pass_lines=6 load_error=0 timeout=0` [red_first.out re-count: 3 FAIL line(s), 6 pass line(s); FAIL lines: ['FAIL: USER root:root case: rc=0 out=OK — all 1 Dockerfile(s) drop root for runtime.', 'FAIL: USER 0:0 case: rc=0 out=OK — all 1 Dockerfile(s) drop root for runtime.', 'FAIL: USER ROOT case: rc=0 out=OK — all 1 Dockerfile(s) drop root for runtime.']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 9 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=9 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 9 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-dockerfile-non-root.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (+4/-0 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh` (+42/-1); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d7691f35312ea158f043e87a3227e477cccb183d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-01_o46_p1_ks1903_dockerfile_non_root_user_group_case/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-dockerfile-non-root.sh
+++ b/Blockchain/Dev/scripts/check-dockerfile-non-root.sh
@@ -29,3 +29,7 @@
+  # KS-1903: `USER root:root`, `USER 0:0` and `USER ROOT` run as root too: drop any :group, ignore case.
+  last_user=${last_user%%:*}
+  last_user=$(printf '%s' "$last_user" | tr 'A-Z' 'a-z')
+
   if [ -z "$last_user" ]; then
     echo "::error::$f has NO USER directive — runs as root (pen-test F-15)"
     EXIT=1
--- a/Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh
@@ -69,2 +69,43 @@
+# KS-1903: a final USER written as user:group, or in another case, is still root.
+# CELL 5 (RED at the tip) - `USER root:root` exits 1 and is named.
+RC_RR="$(run_case rootroot $'FROM node:20\nUSER root:root\n')"
+if [[ "$RC_RR" == "1" ]] && "$REAL_GREP" -qF "final USER is" "$WORK/rootroot.out"; then
+  echo "PASS: a final USER root:root exits 1 and is named"; PASS=$((PASS+1))
+else
+  echo "FAIL: USER root:root case: rc=$RC_RR out=$(head -2 "$WORK/rootroot.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 6 (RED at the tip) - `USER 0:0` exits 1 and is named.
+RC_ZZ="$(run_case zerozero $'FROM node:20\nUSER 0:0\n')"
+if [[ "$RC_ZZ" == "1" ]] && "$REAL_GREP" -qF "final USER is" "$WORK/zerozero.out"; then
+  echo "PASS: a final USER 0:0 exits 1 and is named"; PASS=$((PASS+1))
+else
+  echo "FAIL: USER 0:0 case: rc=$RC_ZZ out=$(head -2 "$WORK/zerozero.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 7 (RED at the tip) - `USER ROOT` exits 1 and is named.
+RC_UP="$(run_case upper $'FROM node:20\nUSER ROOT\n')"
+if [[ "$RC_UP" == "1" ]] && "$REAL_GREP" -qF "final USER is" "$WORK/upper.out"; then
+  echo "PASS: a final USER ROOT exits 1 and is named"; PASS=$((PASS+1))
+else
+  echo "FAIL: USER ROOT case: rc=$RC_UP out=$(head -2 "$WORK/upper.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 8 (GREEN CONTROL, tip AND after) - a non-root user:group passes.
+RC_AG="$(run_case appgroup $'FROM node:20\nUSER app:app\n')"
+if [[ "$RC_AG" == "0" ]]; then
+  echo "PASS: CONTROL USER app:app exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL USER app:app: rc=$RC_AG out=$(head -2 "$WORK/appgroup.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 9 (GREEN CONTROL, tip AND after) - a numeric non-root uid:gid passes.
+RC_NU="$(run_case numeric $'FROM node:20\nUSER 1000:1000\n')"
+if [[ "$RC_NU" == "0" ]]; then
+  echo "PASS: CONTROL USER 1000:1000 exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL USER 1000:1000: rc=$RC_NU out=$(head -2 "$WORK/numeric.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
 echo "check_dockerfile_non_root_reports_root: $PASS passed, $FAIL failed"
-[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
+[[ "$FAIL" -eq 0 && "$PASS" -eq 9 ]]
```
