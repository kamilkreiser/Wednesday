#!/bin/bash
# usage: vt.sh <log> [vitest args...]   gate 79: waits while load1 > 20, nice 10, maxWorkers=2
set -u
LOG="$1"; shift
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate79-ks1868-persona-1894
D=$W/repo/Blockchain/Dev
: > "$LOG"
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 20 ] && break; echo "WAIT: load1=$L > 20 at $(date +%T)" >> "$LOG"; sleep 20; done
echo "start $(date +%T) loadavg: $(sysctl -n vm.loadavg)" >> "$LOG"
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2dc9c5a2-efc6-4975-a82f-157a5a9bc219/scratchpad
nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/demo-service --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
