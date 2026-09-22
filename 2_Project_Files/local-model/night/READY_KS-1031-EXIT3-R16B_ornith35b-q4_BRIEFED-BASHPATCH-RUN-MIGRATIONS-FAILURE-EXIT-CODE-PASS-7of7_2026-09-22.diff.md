# READY — KS-1031-EXIT3-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 11:13 2026-09-22; sha256[:16] 25602a8a7cb0ef9c, 6330 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/EXIT3/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 11:13 2026-09-22 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1031EXIT3-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/scripts/run-migrations.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/run-migrations.sh', 'Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/run-migrations.sh , Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/run-migrations.sh` (script) and `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 11 brief `+` line(s) present; script `+` lines 11 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 6; must_change sites 6/6 each a `-` line; must_remove 6 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/run-migrations.sh` (+11/-6 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` (+105/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL: a run in which 048 failed exited 0, not 3 (Summary: applied=1 failed=1)', "FAIL: ERROR line present=NO, stale 'Exiting 0 so docker' present=YES"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive run-migrations.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/run-migrations.sh` (+11/-6 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` (+105/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['EXIT3', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1031-R16B-EXIT3.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1031-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/run-migrations.sh
+++ b/Blockchain/Dev/scripts/run-migrations.sh
@@ -147,11 +147,16 @@ echo "Summary: applied=$applied_count failed=$failed_count"
 if [ "$failed_count" -gt 0 ]; then
   echo "WARN: $failed_count migration(s) failed (see logs above). Pre-existing"
-  echo "schema-drift migrations (e.g. 002 expected verification_policies.scope_id"
-  echo "that doesn't exist on the live schema) are non-blocking — the app's"
-  echo "startup-migrations.ts has its own retry path. Exiting 0 so docker"
-  echo "compose dependent services can recreate; otherwise --force-recreate"
-  echo "would block on migrations service_completed_successfully condition."
-  echo "(BACKLOG #6 — partial-failure exit semantics.)"
+  echo "ERROR: $failed_count migration(s) failed (see logs above)."
+  echo "KS-1031 (KS-754 gate F-4): this runner used to exit 0 here, so the"
+  echo "docker-compose condition service_completed_successfully was satisfied"
+  echo "by a run in which migrations FAILED, and originate could roll against a"
+  echo "DB that never took 048. Every connector erasure then anonymises the"
+  echo "user, shreds the DEK and aborts on 22P02 - forever, because that cause"
+  echo "is not transient. The BACKLOG #6 reason for exiting 0 (migrations"
+  echo "002/005 failing every boot) was itself fixed and BACKLOG.md marks it"
+  echo "resolved, so a failure here is a real failure. Exit 3 - the code this"
+  echo "script header has documented all along - and let the gate fail."
+  exit 3
 fi
 
 echo "Migration runner finished (applied=$applied_count, failed=$failed_count)."
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh
@@ -0,0 +1,105 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/run-migrations.sh - a FAILED migration must
+# NOT exit 0 (KS-1031, KS-754 gate F-4)
+# =============================================================================
+# psql and pg_isready are stubs on a private PATH: no database is ever needed
+# and no migration is ever executed. PSQL_FAIL names the migration basenames
+# the psql stub must fail.
+# Usage: bash Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${RUN_MIGRATIONS_SH:-$HERE/../run-migrations.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: run-migrations.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1031.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+EXPECTED_CELLS=4
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
+fixture() {
+  mkdir -p "$1/scripts" "$1/migrations"
+  cp "$SUBJ" "$1/scripts/run-migrations.sh"
+  echo "SELECT 1;" > "$1/migrations/047_ok.sql"
+  echo "SELECT 1;" > "$1/migrations/048_ks754_widen_processed_by_to_text.sql"
+}
+
+run_at() {
+  (
+    export PATH="$WORK/bin:/usr/bin:/bin" PSQL_FAIL="$2"
+    if [ -n "$3" ]; then export DATABASE_URL="$3"; else unset DATABASE_URL; fi
+    unset PLATFORM_DATABASE_URL
+    cd "$1" && sh scripts/run-migrations.sh
+  ) >"$1/out.txt" 2>&1
+  echo $?
+}
+
+fixture "$WORK/partial"
+RC_PARTIAL="$(run_at "$WORK/partial" "048_ks754_widen_processed_by_to_text.sql" "$DB_URL")"
+OUT_PARTIAL="$WORK/partial/out.txt"
+fixture "$WORK/clean"
+RC_CLEAN="$(run_at "$WORK/clean" "" "$DB_URL")"
+OUT_CLEAN="$WORK/clean/out.txt"
+fixture "$WORK/nourl"
+RC_NOURL="$(run_at "$WORK/nourl" "" "")"
+OUT_NOURL="$WORK/nourl/out.txt"
+
+# CELL 1 (RED at the tip) - one migration of two fails: the runner must exit 3.
+if [[ "$RC_PARTIAL" == "3" ]]; then
+  echo "PASS: a run in which 048 failed exits 3, so compose service_completed_successfully cannot be satisfied by it"; PASS=$((PASS+1))
+else
+  echo "FAIL: a run in which 048 failed exited $RC_PARTIAL, not 3 ($(grep -F 'Summary:' "$OUT_PARTIAL" | head -1))"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - the message must stop calling the exit 0 deliberate.
+if grep -qF 'ERROR: 1 migration(s) failed' "$OUT_PARTIAL" && ! grep -qF 'Exiting 0 so docker' "$OUT_PARTIAL"; then
+  echo "PASS: the failure output reports an ERROR and no longer says it is exiting 0 on purpose"; PASS=$((PASS+1))
+else
+  echo "FAIL: ERROR line present=$(grep -qF 'ERROR: 1 migration(s) failed' "$OUT_PARTIAL" && echo yes || echo NO), stale 'Exiting 0 so docker' present=$(grep -qF 'Exiting 0 so docker' "$OUT_PARTIAL" && echo YES || echo no)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the happy path is untouched.
+if [[ "$RC_CLEAN" == "0" ]] && grep -qF 'Summary: applied=2 failed=0' "$OUT_CLEAN" && grep -qF 'Migration runner finished' "$OUT_CLEAN"; then
+  echo "PASS: CONTROL two clean migrations still apply, print applied=2 failed=0, and exit 0"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL clean run exited $RC_CLEAN (want 0), $(grep -F 'Summary:' "$OUT_CLEAN" | head -1)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - the other documented code is unchanged.
+if [[ "$RC_NOURL" == "1" ]] && grep -qF 'DATABASE_URL is not set' "$OUT_NOURL"; then
+  echo "PASS: CONTROL a missing DATABASE_URL still exits 1 and says so"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL missing DATABASE_URL exited $RC_NOURL (want 1): $(head -1 "$OUT_NOURL")"; FAIL=$((FAIL+1))
+fi
+
+# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing
+# is a check that cannot fail, so a short count is itself a FAIL.
+if [[ $((PASS + FAIL)) -eq "$EXPECTED_CELLS" ]]; then
+  echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))
+else
+  echo "FAIL: only $((PASS + FAIL)) of $EXPECTED_CELLS cells ran - a suite that asserts nothing is not a pass"; FAIL=$((FAIL+1))
+fi
+
+echo ""
+echo "run_migrations_failure_exit_code: $PASS passed, $FAIL failed"
+[[ $FAIL -eq 0 ]]
```
