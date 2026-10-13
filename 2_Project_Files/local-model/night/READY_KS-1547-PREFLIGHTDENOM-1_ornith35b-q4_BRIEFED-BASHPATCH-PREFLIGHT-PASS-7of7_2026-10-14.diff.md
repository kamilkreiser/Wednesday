# READY — KS-1547-PREFLIGHTDENOM-1 (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ✏️ **CORRECTION by Wednesday 07:16 2026-10-14 (the tool's text below is left as written):** the MODEL was **the Spark (DeepSeek V4 Flash, endpoint 127.0.0.1:47788 via spark/round.sh)**, NOT Ornith: `hold_ready.py` labels every run Ornith in the title and filename. The brief WAS located: `local-model/night/briefs/ks_1547_p1/KS-1547.md` (hold_ready looks only for `night/briefs/<id>.md`, not a brief DIRECTORY). Rounds: 3 runs of the SAME brief, 0 rebriefs; runs 1-2 failed only at B6 on the pre-existing ks884 flake (IMPROVEMENTS 2026-10-14). Opus QA gate required before merge (preflight is every developer's push gate).

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-r3/out.md.checker/patch.diff`** (from `ls` at 07:15 2026-10-14; sha256[:16] 36f615a5b342ddc4, 4108 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-r3/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-r3/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4108 B vs golden 4468 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (preflight.sh 2, ks1547_preflight_step_header_denominator.test.sh 73); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 07:15 2026-10-14 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-r3/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3c0a522216258040f32d400ede433e48e683f734`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 3c0a522216258040f32d400ede433e48e683f734, Blockchain/Dev/scripts/preflight/preflight.sh and Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/preflight/preflight.sh', 'Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/preflight/preflight.sh , Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/preflight/preflight.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/preflight/preflight.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh` (+73/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=4 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 4 pass line(s); FAIL lines: ['FAIL RED a TAB after the right denominator does not abort', 'FAIL RED a colon after the right denominator does not abort']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 6 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=6 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 6 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive preflight.sh: no NEW failure after (15 suite(s))` [15 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/preflight/preflight.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh` (+73/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3c0a522216258040f32d400ede433e48e683f734` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-r3/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1547_p1-r3/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/preflight/preflight.sh
+++ b/Blockchain/Dev/scripts/preflight/preflight.sh
@@ -222,7 +222,7 @@ step() {
     # KS-1209: fail is per-leg from here on; fail_total keeps the run's result.
     fail_total=$(( ${fail_total:-0} | fail )); fail=0
     CURRENT_LEG="${1%%/*}"
-    _hdr_total="${1#*/}"; _hdr_total="${_hdr_total%% *}"
+    _hdr_total="${1#*/}"; _hdr_total="${_hdr_total%%[!0-9]*}"
     if [ "$_hdr_total" != "$TOTAL_LEGS" ]; then
         echo ""
         echo "PREFLIGHT ABORTED — step header \"$1\" says /$_hdr_total but TOTAL_LEGS=$TOTAL_LEGS."
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
@@ -0,0 +1,73 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS that preflight's step() reads the header's denominator as digits (KS-1547)
+# =============================================================================
+# step() compares the "N/TOTAL" header's denominator with TOTAL_LEGS and ABORTS
+# on a mismatch (KS-1046). It cut the denominator at the first SPACE, so a header
+# whose total is followed by a TAB or a colon kept that tail and aborted although
+# the count was right. These cases build the harness from preflight.sh's OWN
+# lines - its state and its step() helper - call step() once with a chosen
+# header, and read the exit code and the output. No leg body runs: no npm, no
+# node, no network.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+PREFLIGHT="$HERE/../preflight/preflight.sh"
+PASS=0
+FAIL=0
+
+expect() {
+  local desc="$1" want="$2" got="$3"
+  if [[ "$got" == "$want" ]]; then
+    PASS=$((PASS + 1)); printf 'ok   %s\n' "$desc"
+  else
+    FAIL=$((FAIL + 1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"
+  fi
+}
+
+tmp="$(mktemp -d "${TMPDIR:-/tmp}/ks1547-step.XXXXXX")"
+trap 'rm -rf "$tmp"' EXIT INT TERM
+
+# The product's own lines: from `fail=0` up to the first leg (state and helpers).
+awk '/^fail=0$/{on=1} /^step "1\//{on=0} on' "$PREFLIGHT" > "$tmp/helpers.sh"
+TOTAL="$(awk -F= '$1 == "TOTAL_LEGS" {print $2}' "$tmp/helpers.sh")"
+
+# call_step <header>: one call to the script's own step(), then a marker line.
+# Sets RC and writes $tmp/out.txt.
+call_step() {
+  {
+    printf 'set -uo pipefail\nGATEWAY=http://127.0.0.1:9\n'
+    cat "$tmp/helpers.sh"
+    printf 'step %q\necho STEP-RETURNED\n' "$1"
+  } > "$tmp/run.sh"
+  bash "$tmp/run.sh" > "$tmp/out.txt" 2>&1
+  RC=$?
+}
+
+has() { if grep -q -F -- "$1" "$tmp/out.txt"; then echo yes; else echo no; fi; }
+
+expect "CONTROL the harness holds preflight's own state, step() and its abort, and a leg total" "yes yes yes yes" \
+  "$(grep -q '^fail=0$' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q '^step() {' "$tmp/helpers.sh" && echo yes || echo no) $(grep -q 'PREFLIGHT ABORTED' "$tmp/helpers.sh" && echo yes || echo no) $([ "${TOTAL:-0}" -gt 1 ] && echo yes || echo no)"
+
+call_step "3/$TOTAL  Title"
+expect "CONTROL a space after the right denominator is accepted" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
+call_step "3/$((TOTAL + 1))  Title"
+expect "CONTROL a wrong denominator still aborts" "1 no yes" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
+call_step "3/$TOTAL"$'\t'"Title"
+expect "RED a TAB after the right denominator does not abort" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
+call_step "3/$TOTAL:Title"
+expect "RED a colon after the right denominator does not abort" "0 yes no" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
+call_step "3/$((TOTAL + 1))"$'\t'"Title"
+expect "CONTROL a wrong denominator followed by a TAB still aborts" "1 no yes" "$RC $(has STEP-RETURNED) $(has 'PREFLIGHT ABORTED')"
+
+echo ""
+echo "ks1547_preflight_step_header_denominator: $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ]
```
