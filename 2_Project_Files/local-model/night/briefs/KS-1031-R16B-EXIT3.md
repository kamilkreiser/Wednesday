# KS-1031 R16B-EXIT3 - re-brief at develop 8c2f7b3fd of READY_KS-1031_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 10:26:28 AEST by Wednesday's feed9 drafter under the FEED 8 ruling; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip (KS-1081: one hunk corrected to the old brief's intent - see the drafter's note), every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`Blockchain/Dev/scripts/run-migrations.sh` is the one-shot job that `docker-compose.yml:190` runs as the
`migrations` service, and every other service is gated behind it by
`condition: service_completed_successfully`. The script's own header documents four exit codes and line
26 says `3  - at least one migration failed` - but the body never returns 3. Its closing block counts
failures, prints a WARN explaining that it is **deliberately** exiting 0 so dependent services can still
recreate, then falls through to `exit 0` on line 158. So compose's condition is satisfied by a run in
which migrations FAILED. That is what turns KS-754 gate finding F-4 from a warning into a deploy
condition: if the originate image rolls against a DB where `048_ks754_widen_processed_by_to_text.sql`
did not land, every connector erasure anonymises the user, destroys the DEK, then aborts with Postgres
`22P02` - `USER_ERASED=0`, the DSR left `processing` - and because `22P02` is a type error and not a
transient one, the connector's unbounded retry re-runs steps 1-11 and fails the same way forever. The
stated reason for the `exit 0` has itself expired: `BACKLOG.md:131` records "Migrations 002/005 fail
every boot" as **resolved** - both files were made idempotent with column-existence DO blocks - so the
schema-drift failures the block apologises for no longer happen, and a failure reaching that block today
is a real one. This task makes the failure path return the exit code the file has documented all along,
and replaces the WARN prose that justified the lie. NOT in this task: the second, separable half of the
ticket - recording the deploy-ordering condition ("apply 048 BEFORE rolling originate") in the PR body,
`DEPLOYMENT-ARCHITECTURE.md` and the DR runbook - and nothing about the Azure path, where migrations run
at api-gateway boot (`services/api-gateway/src/startup-migrations.ts`) and no compose ordering exists.

## The exact change - 1 hunk(s) in `Blockchain/Dev/scripts/run-migrations.sh` (6 '-' line(s), 11 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
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
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:149` - **must change**: `  echo "schema-drift migrations (e.g. 002 expected verification_policies.scope_id"`
* `:150` - **must change**: `  echo "that doesn't exist on the live schema) are non-blocking — the app's"`
* `:151` - **must change**: `  echo "startup-migrations.ts has its own retry path. Exiting 0 so docker"`
* `:152` - **must change**: `  echo "compose dependent services can recreate; otherwise --force-recreate"`
* `:153` - **must change**: `  echo "would block on migrations service_completed_successfully condition."`
* `:154` - **must change**: `  echo "(BACKLOG #6 — partial-failure exit semantics.)"`
* `:147` - (correct) `if [ "$failed_count" -gt 0 ]; then` - stays
* `:148` - (correct) `  echo "WARN: $failed_count migration(s) failed (see logs above). Pre-existing"` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`

File: `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (105 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`, ONE hunk header `@@ -0,0 +1,105 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/run-migrations.sh - a FAILED migration must
# NOT exit 0 (KS-1031, KS-754 gate F-4)
# =============================================================================
# psql and pg_isready are stubs on a private PATH: no database is ever needed
# and no migration is ever executed. PSQL_FAIL names the migration basenames
# the psql stub must fail.
# Usage: bash Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${RUN_MIGRATIONS_SH:-$HERE/../run-migrations.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: run-migrations.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1031.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
EXPECTED_CELLS=4
DB_URL="postgresql://secuura:pw@localhost:5432/secuura"

mkdir -p "$WORK/bin"
cat > "$WORK/bin/pg_isready" <<'STUB'
#!/bin/sh
exit 0
STUB
cat > "$WORK/bin/psql" <<'STUB'
#!/bin/sh
for a in "$@"; do
  case "$a" in
    *.sql) case " $PSQL_FAIL " in *" ${a##*/} "*) echo "ERROR: 22P02 (stub)" >&2; exit 1 ;; esac ;;
  esac
done
exit 0
STUB
chmod +x "$WORK/bin/pg_isready" "$WORK/bin/psql"

fixture() {
  mkdir -p "$1/scripts" "$1/migrations"
  cp "$SUBJ" "$1/scripts/run-migrations.sh"
  echo "SELECT 1;" > "$1/migrations/047_ok.sql"
  echo "SELECT 1;" > "$1/migrations/048_ks754_widen_processed_by_to_text.sql"
}

run_at() {
  (
    export PATH="$WORK/bin:/usr/bin:/bin" PSQL_FAIL="$2"
    if [ -n "$3" ]; then export DATABASE_URL="$3"; else unset DATABASE_URL; fi
    unset PLATFORM_DATABASE_URL
    cd "$1" && sh scripts/run-migrations.sh
  ) >"$1/out.txt" 2>&1
  echo $?
}

fixture "$WORK/partial"
RC_PARTIAL="$(run_at "$WORK/partial" "048_ks754_widen_processed_by_to_text.sql" "$DB_URL")"
OUT_PARTIAL="$WORK/partial/out.txt"
fixture "$WORK/clean"
RC_CLEAN="$(run_at "$WORK/clean" "" "$DB_URL")"
OUT_CLEAN="$WORK/clean/out.txt"
fixture "$WORK/nourl"
RC_NOURL="$(run_at "$WORK/nourl" "" "")"
OUT_NOURL="$WORK/nourl/out.txt"

# CELL 1 (RED at the tip) - one migration of two fails: the runner must exit 3.
if [[ "$RC_PARTIAL" == "3" ]]; then
  echo "PASS: a run in which 048 failed exits 3, so compose service_completed_successfully cannot be satisfied by it"; PASS=$((PASS+1))
else
  echo "FAIL: a run in which 048 failed exited $RC_PARTIAL, not 3 ($(grep -F 'Summary:' "$OUT_PARTIAL" | head -1))"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - the message must stop calling the exit 0 deliberate.
if grep -qF 'ERROR: 1 migration(s) failed' "$OUT_PARTIAL" && ! grep -qF 'Exiting 0 so docker' "$OUT_PARTIAL"; then
  echo "PASS: the failure output reports an ERROR and no longer says it is exiting 0 on purpose"; PASS=$((PASS+1))
else
  echo "FAIL: ERROR line present=$(grep -qF 'ERROR: 1 migration(s) failed' "$OUT_PARTIAL" && echo yes || echo NO), stale 'Exiting 0 so docker' present=$(grep -qF 'Exiting 0 so docker' "$OUT_PARTIAL" && echo YES || echo no)"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - the happy path is untouched.
if [[ "$RC_CLEAN" == "0" ]] && grep -qF 'Summary: applied=2 failed=0' "$OUT_CLEAN" && grep -qF 'Migration runner finished' "$OUT_CLEAN"; then
  echo "PASS: CONTROL two clean migrations still apply, print applied=2 failed=0, and exit 0"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL clean run exited $RC_CLEAN (want 0), $(grep -F 'Summary:' "$OUT_CLEAN" | head -1)"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - the other documented code is unchanged.
if [[ "$RC_NOURL" == "1" ]] && grep -qF 'DATABASE_URL is not set' "$OUT_NOURL"; then
  echo "PASS: CONTROL a missing DATABASE_URL still exits 1 and says so"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL missing DATABASE_URL exited $RC_NOURL (want 1): $(head -1 "$OUT_NOURL")"; FAIL=$((FAIL+1))
fi

# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing
# is a check that cannot fail, so a short count is itself a FAIL.
if [[ $((PASS + FAIL)) -eq "$EXPECTED_CELLS" ]]; then
  echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))
else
  echo "FAIL: only $((PASS + FAIL)) of $EXPECTED_CELLS cells ran - a suite that asserts nothing is not a pass"; FAIL=$((FAIL+1))
fi

echo ""
echo "run_migrations_failure_exit_code: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 (RED at the tip) - one migration of two fails: the runner must exit 3.`
- `echo "PASS: a run in which 048 failed exits 3, so compose service_completed_successfully cannot be satisfied by it"; PASS=$((PASS+1))`
- `# CELL 2 (RED at the tip) - the message must stop calling the exit 0 deliberate.`
- `echo "PASS: the failure output reports an ERROR and no longer says it is exiting 0 on purpose"; PASS=$((PASS+1))`
- `# CELL 3 (GREEN CONTROL, tip AND after) - the happy path is untouched.`
- `echo "PASS: CONTROL two clean migrations still apply, print applied=2 failed=0, and exit 0"; PASS=$((PASS+1))`
- `# CELL 4 (GREEN CONTROL, tip AND after) - the other documented code is unchanged.`
- `echo "PASS: CONTROL a missing DATABASE_URL still exits 1 and says so"; PASS=$((PASS+1))`
- `# CELL 5 - the completeness guard. A suite that exits 0 having asserted nothing`
- `echo "PASS: all $EXPECTED_CELLS cells ran"; PASS=$((PASS+1))`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/run-migrations.sh` / `+++ b/Blockchain/Dev/scripts/run-migrations.sh` (1 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` (one hunk, `@@ -0,0 +1,105 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed9 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 10:26:28 AEST)
- `Blockchain/Dev/scripts/run-migrations.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Blockchain/Dev/scripts/run-migrations.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x; FEED 9 inherits it) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed9-drafter-precheck/EXIT3/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1031 on the Secuura board at 2026-09-22 10:26:28 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
