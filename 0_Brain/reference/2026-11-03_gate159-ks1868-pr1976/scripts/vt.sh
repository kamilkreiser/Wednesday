#!/bin/bash
# vt.sh <wt name> <logname> [vitest args...]  -- runs vitest anchored at that worktree's anchoring root
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
n=$1; shift; lg=$1; shift
A=$W/wt_$n/Blockchain/Dev/services/anchoring
V=$W/wt_$n/Blockchain/Dev/node_modules/.bin/vitest
( cd "$A" && "$V" run --root "$A" --reporter=verbose --testTimeout=60000 --hookTimeout=60000 "$@" ) > "$W/logs/$lg.log" 2>&1
rc=$?
echo "rc=$rc" >> "$W/logs/$lg.log"
grep -E '^ *(Test Files|Tests) ' "$W/logs/$lg.log"; echo "rc=$rc"
