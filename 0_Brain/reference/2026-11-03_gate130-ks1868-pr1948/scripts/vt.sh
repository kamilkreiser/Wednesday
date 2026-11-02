#!/bin/bash
# usage: vt.sh <log> [vitest args...]  (security package). Load gate: wait up to 6 x 20s for load1<=14, then proceed anyway (logged).
set -u
LOG="$1"; shift
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948
A=$W/repo/Blockchain/Dev/services/security
for i in 1 2 3 4 5 6; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 14 ] && break; echo "load1=$L > 14, waiting ($i)" >&2; sleep 20; done
echo "load1 at start: $L" > "$LOG"
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/63368015-16aa-4db8-b8cd-a340b48c55c0/scratchpad
mkdir -p $TMPDIR
nice -n 10 $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
