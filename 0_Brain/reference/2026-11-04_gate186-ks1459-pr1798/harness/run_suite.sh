#!/bin/bash
# Gate 186. usage: run_suite.sh <label> [extra vitest args...]  -- whole auth unit suite at the clone's current tree.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate186-ks1459-pr1798
A=$G/repo/Blockchain/Dev/services/auth
L=$1; shift
# run 1 used cwd=$G/cwd: ks1009 and ks1467 read paths relative to process.cwd() and failed there (harness artefact).
# The auth package dir is itself inside the workdir (repo/ is the gate clone), so it satisfies the cwd rule.
cd "${GATE_CWD:-$A}" || exit 9
env -i PATH="$PATH" HOME="$G/home" TMPDIR="$G/tmp" \
  "$G/repo/Blockchain/Dev/node_modules/.bin/vitest" run --root "$A" "$@" > "$G/runs/suite_$L.out" 2>&1
rc=$?
echo "$L rc=$rc"
sed 's/\x1b\[[0-9;]*m//g' "$G/runs/suite_$L.out" | /usr/bin/grep -E "^ *(Test Files|Tests) |FAIL " | head -20
exit $rc
