# READY — KS-1031 (KS-754 gate F-4 — `run-migrations.sh` exits 0 when a migration FAILS, contradicting its own header line 26 which documents `3 — at least one migration failed`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r2, BASH_PATCH, NEW test file, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1031-ornith35b-night2
# Source read by me (Wednesday): the applied test section is 4708 B / 106 `+` lines (r1's was 337 B — see below), it carries the completeness guard, and B5's FIVE pass lines are the four graded cells plus that guard, so the suite genuinely ran rather than skipping. B4 red-first genuine, B5 green-after, B6 the one sibling suite unchanged. Product hunk 7 `-` / 11 `+`, one hunk, unchanged between rounds — it passed B2/B3/B3b in BOTH.
# ⚠ WHY R1 FAILED, because it is a MODEL DIALECT worth carrying: r1 stopped at B4 with `rc=0 fail_lines=0 pass_lines=0` — a suite that ran and asserted NOTHING. The cause was in the diff: the model's whole test section was one line — *"This file contains the full test suite content as specified in the brief. Due to length constraints, only the first line is shown here."* **The brief's test body was 179 lines. KS-1081, which passed on its first sample, was ~90.** There is a TRANSCRIPTION CEILING, and above it the failure is a silent substitution that every other gate passes. Body cut to 105 lines; a do-not-summarise block added; and CELL 5 asserts `PASS+FAIL == EXPECTED_CELLS`, proven to fire (with the graded cells deleted it prints `only 0 of 4 cells ran` and exits 1). **Every brief in this tier should carry that cell.**
# PR NOTES for the Sunday raising seat: (1) TWO files: `Blockchain/Dev/scripts/run-migrations.sh` (one hunk, the WARN block at :148-154) + the NEW suite `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`. The suite stubs `psql` and `pg_isready` on a private PATH — **no Postgres required**. (2) **Scope: the ticket names TWO fixes and this is fix 2 only.** Fix 1 (apply 048 before rolling the originate image) is a deploy-ordering CONDITION for the PR body / DEPLOYMENT-ARCHITECTURE.md / the DR runbook — documentation, not code, and not in this diff. (3) **What makes a hard `exit 3` safe rather than a Kam decision:** the closing block apologises for "pre-existing schema-drift migrations (e.g. 002…) are non-blocking", and `BACKLOG.md:131` marks exactly that ✅ resolved — 002 and 005 were made idempotent in the same change that introduced the `exit 0`. **The workaround outlived its problem.** Put that in the PR body. (4) Incidental second defect found in the same file and NOT briefed: `/tmp/migrate-err.log` at :101 is a fixed shared path — two concurrent runners on one host interleave it. File it separately.

```diff
--- a/Blockchain/Dev/scripts/run-migrations.sh
+++ b/Blockchain/Dev/scripts/run-migrations.sh
@@ -145,13 +145,17 @@ echo "Summary: applied=$applied_count failed=$failed_count"
 
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
