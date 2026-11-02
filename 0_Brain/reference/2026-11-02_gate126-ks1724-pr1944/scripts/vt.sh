#!/bin/bash
# usage: vt.sh <repo|base> <unit rel to Dev, e.g. packages/shared> <log> [vitest args...]
# Runs the unit's own `npm run test` (cwd = the unit, anchored by --prefix), maxWorkers=2, nice 10. Logs load1 at start.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
T="$1"; U="$2"; LOG="$3"; shift 3
A=$G/$T/Blockchain/Dev/$U
echo "tree=$T unit=$U load=$(sysctl -n vm.loadavg) start=$(date -u +%H:%M:%SZ)" > "$LOG"
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/63368015-16aa-4db8-b8cd-a340b48c55c0/scratchpad/tmp
mkdir -p $TMPDIR
nice -n 10 npm --prefix "$A" run test -- --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC end=$(date -u +%H:%M:%SZ)" >> "$LOG"; exit $RC
