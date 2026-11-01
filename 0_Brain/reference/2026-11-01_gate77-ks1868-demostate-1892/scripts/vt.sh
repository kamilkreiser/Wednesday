#!/bin/bash
# usage: vt.sh <log> [vitest args...]
set -u
LOG="$1"; shift
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892
D=$W/repo/Blockchain/Dev
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2dc9c5a2-efc6-4975-a82f-157a5a9bc219/scratchpad
nice -n 10 $D/node_modules/.bin/vitest run --root $D/services/demo-service --maxWorkers=2 --silent=false "$@" > "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
