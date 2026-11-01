#!/bin/bash
# usage: vt.sh <log> [vitest args...]
set -u
LOG="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893
A=$G/repo/Blockchain/Dev/services/analytics
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2dc9c5a2-efc6-4975-a82f-157a5a9bc219/scratchpad
mkdir -p $TMPDIR
nice -n 10 $G/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" > "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
