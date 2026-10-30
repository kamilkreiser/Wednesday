# READY — KS-0-KS-0-P1 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules/out.md.checker/patch.diff`** (from `ls` at 13:59 2026-10-30; sha256[:16] 637cf3c46afdc0f6, 4877 B — a BYTE count; NOTE — `cat section_*.diff | cmp patch.diff` rc 1, differing by 5 line(s); the checker REWROTE section_1.diff; patch.diff is the model's AS-WRITTEN block, the SECTION FILES are the applied units and the canonical for the raise: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip — with an accommodation: section_1.diff: REANCHORED (hunk 1: reanchored at 28 (1 '-' / 1 '+' lines; model header -26,6 +26,6);reanchored 1/1 hunk(s););` — STRICT APPLY NOT CLAIMED for the whole patch: apply PER SECTION with the options recorded in section_<k>.diff.opts (the raise seat states which); CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4877 B vs golden 5193 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-no-sql-injection.sh 2, check_no_sql_injection_skips_node_modules.test.sh 84); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 13:59 2026-10-30 by Spark operator 24 (Wednesday) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558, Blockchain/Dev/scripts/check-no-sql-injection.sh and Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-no-sql-injection.sh', 'Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-no-sql-injection.sh , Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-no-sql-injection.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-no-sql-injection.sh` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): NON-EMPTY: `error: patch failed: Blockchain/Dev/scripts/check-no-sql-injection.sh:26`; checker-REWRITTEN: REANCHORED (applied file = the reanchored hunks; as-written kept at section_1.diff.as-written))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh` (+84/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: the scan call does not exclude node_modules: -rEn --include=*.ts --include=*.tsx --include=*.js \\$(query|execute)RawUnsafe\\(\\s*`[^`]*\\$\\{ services/ packages/']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names check-no-sql-injection.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-no-sql-injection.sh` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh` (+84/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — the CHECKER-REWRITTEN file, not the fence; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_filing_sqlinj_p1_exclude_node_modules/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-no-sql-injection.sh
+++ b/Blockchain/Dev/scripts/check-no-sql-injection.sh
@@ -26,6 +26,6 @@
 # Match: $queryRawUnsafe( ` … ${ ANY } …
 # (template literal with interpolation passed straight to *Unsafe)
-hits=$(grep -rEn --include='*.ts' --include='*.tsx' --include='*.js' \
+hits=$(grep -rEn --exclude-dir=node_modules --include='*.ts' --include='*.tsx' --include='*.js' \
        '\$(query|execute)RawUnsafe\(\s*`[^`]*\$\{' \
        services/ packages/ 2>/dev/null \
        | grep -v 'node_modules\|/dist/\|src/db.ts:.*\\$queryRaw\|originate/src/db.ts' \
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh
@@ -0,0 +1,84 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-no-sql-injection.sh - its scan must not
+# descend into node_modules.
+# =============================================================================
+# The scan is `grep -rEn ... services/ packages/` and only AFTERWARDS drops every hit
+# whose path names node_modules, so it reads every installed package first. Its sibling
+# check-no-*.sh scripts pass --exclude-dir=node_modules to grep itself.
+# grep is a stub on a private PATH: it logs every call's arguments, answers the scan
+# call with the lines in SHIM_HITS, and hands the script's own `grep -v` filter call to
+# the real grep. No tree is ever walked.
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_sql_injection_skips_node_modules.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${CHECK_NO_SQL_INJECTION_SH:-$HERE/../check-no-sql-injection.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-sql-injection.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/sqlinj.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+REAL_GREP="$(command -v grep)"
+
+mkdir -p "$WORK/bin" "$WORK/root/scripts" "$WORK/root/services" "$WORK/root/packages"
+cp "$SUBJ" "$WORK/root/scripts/check-no-sql-injection.sh"
+cat > "$WORK/bin/grep" <<'STUB'
+#!/bin/sh
+echo "$*" >> "$SHIM_LOG"
+for a in "$@"; do
+  [ "$a" = "-v" ] && exec "$REAL_GREP" "$@"
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
+    cd "$WORK/root" && bash scripts/check-no-sql-injection.sh
+  ) >"$WORK/$1.out" 2>&1
+  echo $?
+}
+
+RC_CLEAN="$(run_case clean "")"
+RC_HIT="$(run_case hit 'services/x/src/repo.ts:3:  db.$queryRawUnsafe(`SELECT 1 WHERE id = ${id}`);')"
+RC_DEP="$(run_case dep 'services/x/node_modules/y/index.js:9:  db.$queryRawUnsafe(`SELECT ${id}`);')"
+SCAN_CALL="$("$REAL_GREP" -m1 -e '-rEn' "$WORK/clean.log")"
+
+# CELL 1 (RED at the tip) - the scan call itself excludes node_modules.
+if [[ -n "$SCAN_CALL" && "$SCAN_CALL" == *"--exclude-dir=node_modules"* ]]; then
+  echo "PASS: the scan call carries --exclude-dir=node_modules"; PASS=$((PASS+1))
+else
+  echo "FAIL: the scan call does not exclude node_modules: $SCAN_CALL"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (GREEN CONTROL, tip AND after) - the stub saw the scan: the three file types, both roots.
+if [[ "$SCAN_CALL" == *"--include=*.ts"* && "$SCAN_CALL" == *"--include=*.tsx"* && "$SCAN_CALL" == *"--include=*.js"* \
+   && "$SCAN_CALL" == *"services/ packages/"* ]]; then
+  echo "PASS: CONTROL the scan still reads .ts, .tsx and .js under services/ and packages/"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL scan call: $SCAN_CALL"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - a clean scan exits 0; a hit in service source exits 1.
+if [[ "$RC_CLEAN" == "0" ]] && "$REAL_GREP" -qF 'no string-concatenated SQL found' "$WORK/clean.out" \
+   && [[ "$RC_HIT" == "1" ]]; then
+  echo "PASS: CONTROL a clean scan exits 0 and a hit in service source exits 1"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL exit codes: clean=$RC_CLEAN hit=$RC_HIT"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a hit whose path names node_modules is still dropped by the script's own filter.
+if [[ "$RC_DEP" == "0" ]] && "$REAL_GREP" -qF 'no string-concatenated SQL found' "$WORK/dep.out"; then
+  echo "PASS: CONTROL a hit under node_modules is still filtered out"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL node_modules hit: rc=$RC_DEP $(head -2 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+echo "check_no_sql_injection_skips_node_modules: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```

**APPLIED `section_1.diff` (REANCHORED (applied file = the reanchored hunks; as-written kept at section_1.diff.as-written)) — byte for byte:**
```diff
--- a/Blockchain/Dev/scripts/check-no-sql-injection.sh
+++ b/Blockchain/Dev/scripts/check-no-sql-injection.sh
@@ -25,7 +25,7 @@
 
 # Match: $queryRawUnsafe( ` … ${ ANY } …
 # (template literal with interpolation passed straight to *Unsafe)
-hits=$(grep -rEn --include='*.ts' --include='*.tsx' --include='*.js' \
+hits=$(grep -rEn --exclude-dir=node_modules --include='*.ts' --include='*.tsx' --include='*.js' \
        '\$(query|execute)RawUnsafe\(\s*`[^`]*\$\{' \
        services/ packages/ 2>/dev/null \
        | grep -v 'node_modules\|/dist/\|src/db.ts:.*\\\$queryRaw\|originate/src/db.ts' \
```
