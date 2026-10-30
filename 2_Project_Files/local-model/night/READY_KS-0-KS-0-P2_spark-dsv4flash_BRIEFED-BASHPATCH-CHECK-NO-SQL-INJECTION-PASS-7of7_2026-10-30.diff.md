# READY — KS-0-KS-0-P2 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit/out.md.checker/patch.diff`** (from `ls` at 14:00 2026-10-30; sha256[:16] 156f115a9643706e, 4587 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; DIFFERS from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit-control/out.md.checker/patch.diff` (`cmp` rc 1): 4 change line(s) (`+`/`-`, ndiff) differ in check_no_sql_injection_reports_the_hit.test.sh (4; run 80 vs golden 80); APPLIED PRODUCT not compared (the golden has no after.sh) — read the diff before raising.

**Held 14:00 2026-10-30 by Spark operator 24 (Wednesday) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558, Blockchain/Dev/scripts/check-no-sql-injection.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-no-sql-injection.sh', 'Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-no-sql-injection.sh , Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-no-sql-injection.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (1 NON-ASCII chars); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-no-sql-injection.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh` (+80/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL: the hit output has no error headline naming both Unsafe calls', 'FAIL: the offending file and line are not printed']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-no-sql-injection.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-no-sql-injection.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh` (+80/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p2_report_the_hit/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-no-sql-injection.sh
+++ b/Blockchain/Dev/scripts/check-no-sql-injection.sh
@@ -34,5 +34,5 @@
 if [ -n "$hits" ]; then
-  echo "::error::SQL injection risk — $queryRawUnsafe / $executeRawUnsafe used with template-literal interpolation:"
+  echo "::error::SQL injection risk — \$queryRawUnsafe / \$executeRawUnsafe used with template-literal interpolation:"
   echo "$hits" | sed 's/^/  /'
   echo ""
   echo "Fix: pass the SQL as a plain string with positional params:"
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh
@@ -0,0 +1,80 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-sql-injection.sh - a real hit must be
+# REPORTED, not swallowed by `set -u`.
+# =============================================================================
+# The failure branch echoes "::error::SQL injection risk - $queryRawUnsafe / $executeRawUnsafe ..."
+# inside double quotes, so under `set -u` the shell expands two unset variables and
+# aborts with "queryRawUnsafe: unbound variable" BEFORE the hit list is printed. The
+# gate still fails (exit 1) but names nothing.
+# grep is a stub on a private PATH: it answers the scan call with the lines in
+# SHIM_HITS and hands the script's own `grep -v` filter call to the real grep. No tree
+# is ever walked.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${CHECK_NO_SQL_INJECTION_SH:-$HERE/../check-no-sql-injection.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-sql-injection.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/sqlhit.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+mkdir -p "$WORK/bin" "$WORK/root/scripts" "$WORK/root/services" "$WORK/root/packages"
+cp "$SUBJ" "$WORK/root/scripts/check-no-sql-injection.sh"
+cat > "$WORK/bin/grep" <<'STUB'
+#!/bin/sh
+for a in "$@"; do
+  [ "$a" = "-v" ] && exec "$REAL_GREP" "$@"
+done
+[ -n "${SHIM_HITS:-}" ] && printf '%s\n' "$SHIM_HITS"
+exit 0
+STUB
+chmod +x "$WORK/bin/grep"
+
+run_case() {   # $1 = name, $2 = the lines the scan call answers with -> prints rc; output in $WORK/$1.out
+  (
+    export PATH="$WORK/bin:/usr/bin:/bin" REAL_GREP SHIM_HITS="$2"
+    cd "$WORK/root" && bash scripts/check-no-sql-injection.sh
+  ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_CLEAN="$(run_case clean "")"
+RC_HIT="$(run_case hit 'services/x/src/repo.ts:3:  db.$queryRawUnsafe(`SELECT 1 WHERE id = ${id}`);')"
+RC_DEP="$(run_case dep 'services/x/node_modules/y/index.js:9:  db.$queryRawUnsafe(`SELECT ${id}`);')"
+
+# CELL 1 (RED at the tip) - a hit prints the error headline with both API names.
+if "$REAL_GREP" -qF 'SQL injection risk' "$WORK/hit.out" && "$REAL_GREP" -qF '$queryRawUnsafe / $executeRawUnsafe' "$WORK/hit.out"; then
+  echo "PASS: a hit prints the error headline naming both Unsafe calls"; PASS=$((PASS+1))
+else
+  echo "FAIL: the hit output has no error headline naming both Unsafe calls"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - a hit prints the offending line, indented two spaces.
+if "$REAL_GREP" -qF '  services/x/src/repo.ts:3:' "$WORK/hit.out"; then
+  echo "PASS: a hit prints the offending file and line"; PASS=$((PASS+1))
+else
+  echo "FAIL: the offending file and line are not printed"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - exit codes: a hit exits 1, a clean scan exits 0 and says OK.
+if [[ "$RC_HIT" == "1" && "$RC_CLEAN" == "0" ]] && "$REAL_GREP" -qF 'no string-concatenated SQL found' "$WORK/clean.out"; then
+  echo "PASS: CONTROL a hit exits 1 and a clean scan exits 0 with the OK line"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL exit codes: hit=$RC_HIT clean=$RC_CLEAN"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a hit under node_modules is still dropped by the script's own filter.
+if [[ "$RC_DEP" == "0" ]] && "$REAL_GREP" -qF 'no string-concatenated SQL found' "$WORK/dep.out"; then
+  echo "PASS: CONTROL a hit under node_modules is still filtered out"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL node_modules hit: rc=$RC_DEP $(head -2 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "check_no_sql_injection_reports_the_hit: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```
