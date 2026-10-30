# READY — KS-0-KS-0-O25-P3 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules/out.md.checker/patch.diff`** (from `ls` at 14:14 2026-10-30; sha256[:16] 5cd3d94e841a4e8f, 4748 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4748 B vs golden 5051 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-connector-xss.sh 2, check_connector_xss_skips_node_modules.test.sh 85); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 14:14 2026-10-30 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558, Blockchain/Dev/scripts/check-connector-xss.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-connector-xss.sh', 'Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-connector-xss.sh , Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-connector-xss.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-connector-xss.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh` (+85/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: the scan call does not exclude node_modules: -rEn (^|[[:space:]<])on[a-z]+=[\'"] connectors/ --include=*.js --include=*.ts --include=*.jsx --include=*.tsx']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-connector-xss.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-connector-xss.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh` (+85/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_scripts_connector_xss_skips_node_modules/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-connector-xss.sh
+++ b/Blockchain/Dev/scripts/check-connector-xss.sh
@@ -23,4 +23,4 @@
-HITS=$(grep -rEn "(^|[[:space:]<])on[a-z]+=['\"]" connectors/ \
+HITS=$(grep -rEn --exclude-dir=node_modules "(^|[[:space:]<])on[a-z]+=['\"]" connectors/ \
        --include='*.js' --include='*.ts' --include='*.jsx' --include='*.tsx' \
        2>/dev/null \
        | grep -vE 'node_modules|/dist/|\.min\.' \
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh
@@ -0,0 +1,85 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-connector-xss.sh - its scan must not descend
+# into node_modules.
+# =============================================================================
+# The scan is `grep -rEn ... connectors/ --include=...` and only AFTERWARDS drops every hit
+# whose path names node_modules, so it reads every installed package under connectors/ first.
+# Its siblings (check-no-default-passwords.sh, check-no-math-random.sh) pass
+# --exclude-dir=node_modules to grep itself.
+# grep is a stub on a private PATH: it logs every call's arguments, answers the scan call with
+# the lines in SHIM_HITS, and hands the script's own `grep -vE` filter call to the real grep.
+# No tree is ever walked.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_connector_xss_skips_node_modules.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${CHECK_CONNECTOR_XSS_SH:-$HERE/../check-connector-xss.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: check-connector-xss.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/xss.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+mkdir -p "$WORK/bin" "$WORK/root/scripts" "$WORK/root/connectors"
+cp "$SUBJ" "$WORK/root/scripts/check-connector-xss.sh"
+cat > "$WORK/bin/grep" <<'STUB'
+#!/bin/sh
+echo "$*" >> "$SHIM_LOG"
+for a in "$@"; do
+  case "$a" in -v*) exec "$REAL_GREP" "$@" ;; esac
+done
+[ -n "${SHIM_HITS:-}" ] && printf '%s\n' "$SHIM_HITS"
+exit 0
+STUB
+chmod +x "$WORK/bin/grep"
+
+run_case() {   # $1 = name, $2 = the lines the scan call answers with -> prints rc; output in $WORK/$1.out, grep calls in $WORK/$1.log
+  : > "$WORK/$1.log"
+  (
+    export PATH="$WORK/bin:/usr/bin:/bin" REAL_GREP SHIM_LOG="$WORK/$1.log" SHIM_HITS="$2"
+    cd "$WORK/root" && bash scripts/check-connector-xss.sh
+  ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_CLEAN="$(run_case clean "")"
+RC_HIT="$(run_case hit $'connectors/a/src/a.js:1:const h = \'<a onclick="x()">\';')"
+RC_DEP="$(run_case dep $'connectors/a/node_modules/y/index.js:9:h = \'<a onclick="x()">\';')"
+SCAN_CALL="$("$REAL_GREP" -m1 -e '-rEn' "$WORK/clean.log")"
+
+# CELL 1 (RED at the tip) - the scan call itself excludes node_modules.
+if [[ -n "$SCAN_CALL" && "$SCAN_CALL" == *"--exclude-dir=node_modules"* ]]; then
+  echo "PASS: the scan call carries --exclude-dir=node_modules"; PASS=$((PASS+1))
+else
+  echo "FAIL: the scan call does not exclude node_modules: $SCAN_CALL"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (GREEN CONTROL, tip AND after) - the scan still reads the four file types under connectors/.
+if [[ "$SCAN_CALL" == *"--include=*.js"* && "$SCAN_CALL" == *"--include=*.ts"* && "$SCAN_CALL" == *"--include=*.jsx"* \
+   && "$SCAN_CALL" == *"--include=*.tsx"* && "$SCAN_CALL" == *"connectors/"* ]]; then
+  echo "PASS: CONTROL the scan still reads .js, .ts, .jsx and .tsx under connectors/"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL scan call: $SCAN_CALL"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - a hit exits 1 and prints the line and the headline; clean exits 0.
+if [[ "$RC_CLEAN" == "0" && "$RC_HIT" == "1" ]] && "$REAL_GREP" -qF 'use addEventListener' "$WORK/hit.out" \
+   && "$REAL_GREP" -qF '  connectors/a/src/a.js:1:' "$WORK/hit.out"; then
+  echo "PASS: CONTROL a hit exits 1 and is printed; a clean scan exits 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL exit codes: clean=$RC_CLEAN hit=$RC_HIT out=$(head -2 "$WORK/hit.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a hit under node_modules is still dropped by the script's own filter.
+if [[ "$RC_DEP" == "0" ]]; then
+  echo "PASS: CONTROL a hit under node_modules is still filtered out"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL node_modules hit: rc=$RC_DEP $(head -2 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "check_connector_xss_skips_node_modules: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```
