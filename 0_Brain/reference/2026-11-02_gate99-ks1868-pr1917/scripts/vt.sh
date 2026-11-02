#!/bin/bash
# usage: vt.sh <log> [vitest args...] (tenant-provisioning). Load gate: wait up to 10 x 20s for load1<=8.
set -u
LOG="$1"; shift
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917
A=$W/repo/Blockchain/Dev/services/tenant-provisioning
for i in 1 2 3 4 5 6 7 8 9 10; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting ($i)" >&2; sleep 20; done
echo "load1 at start: $L" > "$LOG"
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6737ee07-39e0-4a0c-b588-61b97461401d/scratchpad
mkdir -p $TMPDIR
nice -n 10 $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
