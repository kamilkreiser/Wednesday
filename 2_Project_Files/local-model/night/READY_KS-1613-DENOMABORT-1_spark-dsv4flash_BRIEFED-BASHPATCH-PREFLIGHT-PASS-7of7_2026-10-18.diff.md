# READY — KS-1613-DENOMABORT-1 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1/out.md.checker/patch.diff`** (from `ls` at 20:38 2026-10-18; sha256[:16] 1f1118aca669c828, 2702 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 2702 B vs golden 3056 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (preflight.sh 4, ks1547_preflight_step_header_denominator.test.sh 28); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 20:38 2026-10-18 by Wednesday 2026-10-18 20:3x (read at source) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d2ec786e6130c7ce13384185c84cc1e7566d77cb`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d2ec786e6130c7ce13384185c84cc1e7566d77cb, Blockchain/Dev/scripts/preflight/preflight.sh and Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/preflight/preflight.sh', 'Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/preflight/preflight.sh , Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/preflight/preflight.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/preflight/preflight.sh` (+2/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh` (+28/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=10 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 10 pass line(s); FAIL lines: ['FAIL RED KS-1613 the abort for an empty denominator quotes the empty text after the slash', 'FAIL RED KS-1613 the abort for a non-digit denominator quotes the text after the slash']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 12 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=12 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 12 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive preflight.sh: no NEW failure after (15 suite(s))` [15 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/preflight/preflight.sh` (+2/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh` (+28/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d2ec786e6130c7ce13384185c84cc1e7566d77cb` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1613_p1/KS-1613.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1613_p1/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -224,3 +224,3 @@ step() {
     CURRENT_LEG="${1%%/*}"
-    _hdr_total="${1#*/}"; _hdr_total="${_hdr_total%%[!0-9]*}"
+    _hdr_tail="${1#*/}"; _hdr_total="${_hdr_tail%%[!0-9]*}"
     if [ "$_hdr_total" != "$TOTAL_LEGS" ]; then
@@ -230,3 +230,3 @@ step() {
         echo "  Fix the header or TOTAL_LEGS in scripts/preflight/preflight.sh, then push again."
-        echo "  (step header $CURRENT_LEG/$_hdr_total disagrees with TOTAL_LEGS $TOTAL_LEGS)"
+        echo "  (step header $CURRENT_LEG/$_hdr_total disagrees with TOTAL_LEGS $TOTAL_LEGS; the header's text after the slash is \"$_hdr_tail\")"
         exit 1
--- a/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
@@ -70,2 +70,30 @@ expect "CONTROL a wrong denominator followed by a TAB still aborts" "1 no yes" "
 
+# KS-1613 (the PR #1552 gate): the empty / non-digit denominator abort was pinned by no cell (mutant N7, a numeric -ne
+# compare, let 3/ and 3/x through), the digit class was never tested with a 0 in the total (mutant N4), and the abort
+# text dropped a non-digit tail, so step "3/x" said "/". The abort now also quotes the header's text after the slash.
+# call_step_total <total> <header>: as call_step, with TOTAL_LEGS overridden after the helpers (a total containing 0).
+call_step_total() {
+  {
+    printf 'set -uo pipefail\nGATEWAY=http://127.0.0.1:9\n'
+    cat "$tmp/helpers.sh"
+    printf 'TOTAL_LEGS=%s\nstep %q\necho STEP-RETURNED\n' "$1" "$2"
+  } > "$tmp/run.sh"
+  bash "$tmp/run.sh" > "$tmp/out.txt" 2>&1
+  RC=$?
+}
+
+call_step "3/"
+expect "CONTROL KS-1613 an empty denominator aborts" "1 no yes" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+expect "RED KS-1613 the abort for an empty denominator quotes the empty text after the slash" "yes" "$(has "the header's text after the slash is \"\"")"
+
+call_step "3/x  Title"
+expect "CONTROL KS-1613 a non-digit denominator aborts" "1 no yes" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+expect "RED KS-1613 the abort for a non-digit denominator quotes the text after the slash" "yes" "$(has "the header's text after the slash is \"x  Title\"")"
+
+call_step "3/$TOTAL)  Title"
+expect "CONTROL KS-1613 a closing bracket after the right denominator is accepted" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
+call_step_total 20 "3/20  Title"
+expect "CONTROL KS-1613 a total containing 0 is read whole and accepted" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
 echo ""
```
