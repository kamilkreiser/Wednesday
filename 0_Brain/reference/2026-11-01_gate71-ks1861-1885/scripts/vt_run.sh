#!/bin/bash
# Gate 71 (pattern of gate 68's jest_run.sh): run tenant-provisioning vitest. nice -n 10; waits while load1 > 8.
# usage: vt_run.sh <log> [vitest args...]
set -u
LOG="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate71-ks1861-1885
D=$G/repo/Blockchain/Dev
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/tmp; mkdir -p $TMPDIR
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
echo "load1 at start: $(sysctl -n vm.loadavg)" > "$LOG"
nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/tenant-provisioning --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "load1 at end: $(sysctl -n vm.loadavg)" >> "$LOG"
echo "rc=$RC" >> "$LOG"
exit $RC
