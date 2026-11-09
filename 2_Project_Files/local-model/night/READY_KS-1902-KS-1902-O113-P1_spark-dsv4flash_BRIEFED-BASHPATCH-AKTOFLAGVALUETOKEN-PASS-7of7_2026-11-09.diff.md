# READY — KS-1902-KS-1902-O113-P1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/out.md.checker/patch.diff`** (from `ls` at 10:25 2026-11-09; sha256[:16] 04fb87d7594f921c, 2412 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes-control/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 10:25 2026-11-09 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4e529633d0a19a3efe626adfe05684fbd964e595`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 4e529633d0a19a3efe626adfe05684fbd964e595, Blockchain/Dev/scripts/check-akto-container-names.sh and Blockchain/Dev/scripts/__tests__/check_akto_container_names.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-akto-container-names.sh', 'Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-akto-container-names.sh , Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-akto-container-names.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_akto_container_names.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 0; must_change sites 0/0 each a `-` line; must_remove 0 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-akto-container-names.sh` (+2/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh` (+19/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=4 pass_lines=8 load_error=0 timeout=0` [red_first.out re-count: 4 FAIL line(s), 8 pass line(s); FAIL lines: ['FAIL: docker exec -u root akto-mongo is flagged (want rc 1, got rc 0)', 'FAIL: docker exec -e FOO=1 akto-mongo is flagged (want rc 1, got rc 0)', 'FAIL: docker logs --tail 5 akto-testing is flagged (want rc 1, got rc 0)', 'FAIL: docker exec -it -u root akto-mongo is flagged (want rc 1, got rc 0)']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 12 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=12 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 12 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-akto-container-names.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-akto-container-names.sh` (+2/-0 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh` (+19/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4e529633d0a19a3efe626adfe05684fbd964e595` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1902_o113_p1_rebrief_insert_line_no_backslashes/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-akto-container-names.sh
+++ b/Blockchain/Dev/scripts/check-akto-container-names.sh
@@ -86,2 +86,4 @@
 
+# KS-1902: a flag that takes a SEPARATE value token (-u root, -e FOO=1, --tail 5) before the name. Each dash-token may be followed by ONE value word; [[:punct:]]? stands for the optional quote.
+PATTERN+="|(docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)([[:space:]]+-[^[:space:]]+([[:space:]]+[^-[:space:]][^[:space:]]*)?)+[[:space:]]+[[:punct:]]?akto-[a-z0-9-]+)"
 hits=$(
--- a/Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh
@@ -56,6 +56,25 @@
 # CELL 6 (GREEN CONTROL, tip AND after) - flags before a non-akto container are clean.
 check "CONTROL docker exec -it other-container is clean" 0 "$(run_case c6 'docker exec -it other-mongo mongosh')"
 
+# KS-1902: a flag that takes a SEPARATE value token (-u root, -e FOO=1, --tail 5) before the name used to break the chain between the verb and the name.
+# CELL 7 (RED at the tip) - a short flag with its value as the next word.
+check "docker exec -u root akto-mongo is flagged" 1 "$(run_case c7 'docker exec -u root akto-mongo mongosh')"
+
+# CELL 8 (RED at the tip) - an environment flag whose value is NAME=value.
+check "docker exec -e FOO=1 akto-mongo is flagged" 1 "$(run_case c8 'docker exec -e FOO=1 akto-mongo mongosh')"
+
+# CELL 9 (RED at the tip) - a long flag with its value as the next word, on logs.
+check "docker logs --tail 5 akto-testing is flagged" 1 "$(run_case c9 'docker logs --tail 5 akto-testing')"
+
+# CELL 10 (RED at the tip) - a no-value flag, then a flag with a separate value.
+check "docker exec -it -u root akto-mongo is flagged" 1 "$(run_case c10 'docker exec -it -u root akto-mongo mongosh')"
+
+# CELL 11 (GREEN CONTROL, tip AND after) - the derived form after a flag and its value is the fix, not the defect.
+check "CONTROL docker exec -u root with the AKTO_PREFIX form is clean" 0 "$(run_case c11 'docker exec -u root "${AKTO_PREFIX:-akto}-mongo" mongosh')"
+
+# CELL 12 (GREEN CONTROL, tip AND after) - a flag and its value before a non-akto container are clean.
+check "CONTROL docker exec -u root other-mongo is clean" 0 "$(run_case c12 'docker exec -u root other-mongo mongosh')"
+
 echo ""
 echo "Results: $PASS passed, $FAIL failed"
 [[ "$FAIL" -eq 0 ]]
```
