# READY — KS-808-APPLIEDCOUNTSSKIPS-1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/out.md.checker/patch.diff`** (from `ls` at 03:25 2026-10-08; sha256[:16] d47753aa37f9641c, 6445 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden not located — no identity claim is made.

**Held 03:25 2026-10-08 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 46c3e20cfbd21acee0c67d544180c33deaa4c8ef, Blockchain/Dev/scripts/run-migrations.sh and Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/run-migrations.sh', 'Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/run-migrations.sh , Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/run-migrations.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 6 brief `+` line(s) present; script `+` lines 8 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 3; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/run-migrations.sh` (+8/-3 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` (+104/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: one applied + one skipped: rc=0, Summary: applied=2 failed=0, Migration runner finished (applied=2, failed=0).', 'FAIL: a run that only skips: rc=0, Summary: applied=2 failed=0']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive run-migrations.sh: no NEW failure after (2 suite(s))` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/run-migrations.sh` (+8/-3 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` (+104/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/run-migrations.sh
+++ b/Blockchain/Dev/scripts/run-migrations.sh
@@ -118,5 +118,6 @@
   already_applied=$(psql "$TARGET_URL" -tAc "SELECT 1 FROM _secuura_migrations WHERE filename = '$fname' LIMIT 1;" 2>/dev/null)
   if [ "$already_applied" = "1" ]; then
     echo "[$TARGET_NAME] Skipping $fname (already applied)"
+    skipped_count=$((skipped_count + 1))
     return 0
   fi
@@ -143,5 +144,6 @@
 failed_count=0
 applied_count=0
+skipped_count=0
 for f in migrations/*.sql; do
   [ -f "$f" ] || continue
   fname=$(basename "$f")
@@ -165,9 +167,12 @@
     failed_count=$((failed_count + 1))
   fi
 done
-
-echo "Summary: applied=$applied_count failed=$failed_count"
-
+
+# KS-808 (2): apply_one returns 0 for a SKIP as well as for an apply, so the loop counted skips as
+# applications. apply_one counts its skips; take them back out before anything reports applied=.
+applied_count=$((applied_count - skipped_count))
+echo "Summary: applied=$applied_count failed=$failed_count skipped=$skipped_count"
+
 if [ "$failed_count" -gt 0 ]; then
   echo "WARN: $failed_count migration(s) failed (see logs above). Pre-existing"
   echo "ERROR: $failed_count migration(s) failed (see logs above)."
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh
@@ -0,0 +1,104 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/run-migrations.sh - KS-808 (2): the summary's
+# applied=N must not count migrations that were SKIPPED as already applied.
+# =============================================================================
+# apply_one returns 0 on the already-applied path as well as on a real apply, and
+# the caller counted every 0 as an application, so a run that applied nothing and
+# skipped two files printed "applied=2". psql and pg_isready are stubs on a private
+# PATH: no database is ever needed and no migration is ever executed. PSQL_DONE
+# names the migration basenames the tracker query reports as already applied;
+# PSQL_FAIL names the ones the psql stub must fail.
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${RUN_MIGRATIONS_SH:-$HERE/../run-migrations.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: run-migrations.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks808.XXXXXX")"
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
+    *"FROM _secuura_migrations WHERE filename"*)
+      for d in $PSQL_DONE; do
+        case "$a" in *"'$d'"*) echo 1; exit 0 ;; esac
+      done
+      exit 0 ;;
+    *.sql) case " $PSQL_FAIL " in *" ${a##*/} "*) echo "ERROR: 22P02 (stub)" >&2; exit 1 ;; esac ;;
+  esac
+done
+exit 0
+STUB
+chmod +x "$WORK/bin/pg_isready" "$WORK/bin/psql"
+
+run_case() {   # $1 = name, $2 = PSQL_DONE, $3 = PSQL_FAIL -> prints rc; output in $WORK/$1/out.txt
+  mkdir -p "$WORK/$1/scripts" "$WORK/$1/migrations"
+  cp "$SUBJ" "$WORK/$1/scripts/run-migrations.sh"
+  echo "SELECT 1;" > "$WORK/$1/migrations/047_ok.sql"
+  echo "SELECT 1;" > "$WORK/$1/migrations/048_ok.sql"
+  (
+    export PATH="$WORK/bin:/usr/bin:/bin" PSQL_DONE="$2" PSQL_FAIL="$3" DATABASE_URL="$DB_URL"
+    unset PLATFORM_DATABASE_URL
+    cd "$WORK/$1" && sh scripts/run-migrations.sh
+  ) >"$WORK/$1/out.txt" 2>&1
+  echo $?
+}
+
+RC_ONE="$(run_case one_skipped "047_ok.sql" "")"
+RC_ALL="$(run_case all_skipped "047_ok.sql 048_ok.sql" "")"
+RC_CLEAN="$(run_case clean "" "")"
+RC_FAILED="$(run_case one_failed "" "048_ok.sql")"
+summary() { grep -F 'Summary:' "$WORK/$1/out.txt" | head -1; }
+
+# CELL 1 (RED at the tip) - one applied, one skipped: applied=1, and the skip is counted apart.
+if [[ "$RC_ONE" == "0" ]] && grep -qF 'Summary: applied=1 failed=0 skipped=1' "$WORK/one_skipped/out.txt" \
+   && grep -qF 'Migration runner finished (applied=1, failed=0).' "$WORK/one_skipped/out.txt"; then
+  echo "PASS: one applied + one already applied reports applied=1 skipped=1, and the closing line says applied=1"; PASS=$((PASS+1))
+else
+  echo "FAIL: one applied + one skipped: rc=$RC_ONE, $(summary one_skipped), $(grep -F 'Migration runner finished' "$WORK/one_skipped/out.txt")"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - nothing applied, two skipped: applied=0, never applied=2.
+if [[ "$RC_ALL" == "0" ]] && grep -qF 'Summary: applied=0 failed=0 skipped=2' "$WORK/all_skipped/out.txt"; then
+  echo "PASS: a run that only skips reports applied=0 skipped=2"; PASS=$((PASS+1))
+else
+  echo "FAIL: a run that only skips: rc=$RC_ALL, $(summary all_skipped)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the skip is still announced per file.
+if grep -qF '[main] Skipping 047_ok.sql (already applied)' "$WORK/one_skipped/out.txt" \
+   && grep -qF '[main] Applying 048_ok.sql...' "$WORK/one_skipped/out.txt"; then
+  echo "PASS: CONTROL the per-file Skipping / Applying lines are unchanged"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL per-file lines changed: $(grep -F '[main]' "$WORK/one_skipped/out.txt" | tr '\n' ' ')"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - a clean run still applies both and exits 0.
+if [[ "$RC_CLEAN" == "0" ]] && grep -qF 'Summary: applied=2 failed=0' "$WORK/clean/out.txt"; then
+  echo "PASS: CONTROL two clean migrations still print applied=2 failed=0 and exit 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL clean run: rc=$RC_CLEAN, $(summary clean)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 5 (GREEN CONTROL, tip AND after) - a failed migration still exits 3 with failed=1 (KS-1031).
+if [[ "$RC_FAILED" == "3" ]] && grep -qF 'Summary: applied=1 failed=1' "$WORK/one_failed/out.txt"; then
+  echo "PASS: CONTROL one failed migration still exits 3 and reports applied=1 failed=1"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL one failed migration: rc=$RC_FAILED, $(summary one_failed)"; FAIL=$((FAIL+1))
+fi
+
+echo "ks808_run_migrations_counts_skips_apart: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 5 ]]
```

**Appended by Wednesday 03:25 2026-10-08 (not written by hold_ready):** REVIEWED HOLD on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-808-applied-counts-skips/REVIEW.md`) but never held until now; classed UNRAISED by `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md` (forward strict apply at develop eae08a3f441c, reverse refuses, no open PR). Read the REVIEW body for any raise caveat (the census read only its verdict line). Any YAML companion is in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-808-applied-counts-skips/`. Raise is blocked until develop is green on pre-push leg 14 (pickup 03:1x).
