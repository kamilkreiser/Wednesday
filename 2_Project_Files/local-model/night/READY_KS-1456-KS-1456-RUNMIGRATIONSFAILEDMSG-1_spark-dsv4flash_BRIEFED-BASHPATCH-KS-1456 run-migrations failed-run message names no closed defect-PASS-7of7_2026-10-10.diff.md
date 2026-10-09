# READY — KS-1456-KS-1456-RUNMIGRATIONSFAILEDMSG-1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message/out.md.checker/patch.diff`** (from `ls` at 08:08 2026-10-10; sha256[:16] 48c0701df4f71ec8, 5322 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 5322 B vs golden 5702 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (run-migrations.sh 3, ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh 92); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT not compared (the golden has no after.sh); the new test's content IS its `+` lines, so the created file is identical.

**Held 08:08 2026-10-10 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `613070f29112a40a0d8d9684cd50c7c2ae54592c`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 613070f29112a40a0d8d9684cd50c7c2ae54592c, Blockchain/Dev/scripts/run-migrations.sh and Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/run-migrations.sh', 'Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/run-migrations.sh , Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/run-migrations.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/run-migrations.sh` (+1/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh` (+92/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: the failed-run output still names the closed defect: applied=N-counts-skips defect is KS-808. Exit 3 - the code this']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive run-migrations.sh: no NEW failure after (3 suite(s))` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/run-migrations.sh` (+1/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh` (+92/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `613070f29112a40a0d8d9684cd50c7c2ae54592c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/run-migrations.sh
+++ b/Blockchain/Dev/scripts/run-migrations.sh
@@ -184,8 +184,7 @@ if [ "$failed_count" -gt 0 ]; then
   echo "DB that never took 048. Every connector erasure then anonymises the"
   echo "user, shreds the DEK and aborts on 22P02 - forever, because that cause"
   echo "is not transient. The exit-0 behaviour and its reason (migrations"
-  echo "002/005 failing every boot) were changed under KS-1031; the remaining"
-  echo "applied=N-counts-skips defect is KS-808. Exit 3 - the code this"
+  echo "002/005 failing every boot) were changed under KS-1031. Exit 3 - the code this"
   echo "script header has documented all along - and let the gate fail."
   # KS-808 (3): these lines used to cite "BACKLOG #6" and then assert that "BACKLOG.md marks it
   # resolved". Measured at develop 6ab9d5021e96, BACKLOG.md (1,234 lines) matches NEITHER phrase, nor
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh
@@ -0,0 +1,92 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/run-migrations.sh - KS-1456: the failed-run
+# message must not name a defect the runner no longer has.
+# =============================================================================
+# The failure branch printed "the remaining applied=N-counts-skips defect is
+# KS-808" on every failed run, after KS-808 (2) made the runner count skips apart.
+# psql and pg_isready are stubs on a private PATH: no database is ever needed and
+# no migration is ever executed. PSQL_FAIL names the migration basenames the psql
+# stub must fail.
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${RUN_MIGRATIONS_SH:-$HERE/../run-migrations.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: run-migrations.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1456.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+DB_URL="postgresql://secuura:pw@localhost:5432/secuura"
+
+mkdir -p "$WORK/bin"
+cat > "$WORK/bin/pg_isready" <<'STUB'
+#!/bin/sh
+exit 0
+STUB
+cat > "$WORK/bin/psql" <<'STUB'
+#!/bin/sh
+for a in "$@"; do
+  case "$a" in
+    *.sql) case " $PSQL_FAIL " in *" ${a##*/} "*) echo "ERROR: 22P02 (stub)" >&2; exit 1 ;; esac ;;
+  esac
+done
+exit 0
+STUB
+chmod +x "$WORK/bin/pg_isready" "$WORK/bin/psql"
+
+run_case() {   # $1 = name, $2 = PSQL_FAIL -> prints rc; output in $WORK/$1/out.txt
+  mkdir -p "$WORK/$1/scripts" "$WORK/$1/migrations"
+  cp "$SUBJ" "$WORK/$1/scripts/run-migrations.sh"
+  echo "SELECT 1;" > "$WORK/$1/migrations/047_ok.sql"
+  echo "SELECT 1;" > "$WORK/$1/migrations/048_ok.sql"
+  (
+    export PATH="$WORK/bin:/usr/bin:/bin" PSQL_FAIL="$2" DATABASE_URL="$DB_URL"
+    unset PLATFORM_DATABASE_URL
+    cd "$WORK/$1" && sh scripts/run-migrations.sh
+  ) >"$WORK/$1/out.txt" 2>&1
+  echo $?
+}
+
+RC_FAILED="$(run_case one_failed "048_ok.sql")"
+RC_CLEAN="$(run_case clean "")"
+OUT_FAILED="$WORK/one_failed/out.txt"
+
+# CELL 1 (RED at the tip) - the failed-run output must not name the counting defect as open.
+if ! grep -qF 'counts-skips' "$OUT_FAILED" && ! grep -qF 'the remaining' "$OUT_FAILED"; then
+  echo "PASS: the failed-run output no longer names the applied=N counts-skips defect"; PASS=$((PASS+1))
+else
+  echo "FAIL: the failed-run output still names the closed defect: $(grep -F 'counts-skips' "$OUT_FAILED" | head -1)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (GREEN CONTROL, tip AND after) - the exit-3 explanation and the KS-1031 reasoning are kept.
+if [[ "$RC_FAILED" == "3" ]] \
+   && grep -qF 'ERROR: 1 migration(s) failed' "$OUT_FAILED" \
+   && grep -qF 'KS-1031 (KS-754 gate F-4)' "$OUT_FAILED" \
+   && grep -qF 'Exit 3 - the code this' "$OUT_FAILED" \
+   && grep -qF 'script header has documented all along - and let the gate fail.' "$OUT_FAILED"; then
+  echo "PASS: CONTROL a failed run still exits 3 and still explains the exit code and KS-1031"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL failed run: rc=$RC_FAILED, $(head -3 "$OUT_FAILED" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the counting is untouched.
+if grep -qF 'Summary: applied=1 failed=1 skipped=0' "$OUT_FAILED"; then
+  echo "PASS: CONTROL a failed run still reports applied=1 failed=1 skipped=0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL summary: $(grep -F 'Summary:' "$OUT_FAILED" | head -1)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a clean run prints no failure text and exits 0.
+if [[ "$RC_CLEAN" == "0" ]] && ! grep -qF 'migration(s) failed' "$WORK/clean/out.txt" \
+   && grep -qF 'Summary: applied=2 failed=0 skipped=0' "$WORK/clean/out.txt"; then
+  echo "PASS: CONTROL a clean run exits 0 and prints no failure text"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL clean run: rc=$RC_CLEAN, $(grep -F 'Summary:' "$WORK/clean/out.txt" | head -1)"; FAIL=$((FAIL+1))
+fi
+
+echo "ks1456_run_migrations_failed_run_names_no_closed_defect: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```
