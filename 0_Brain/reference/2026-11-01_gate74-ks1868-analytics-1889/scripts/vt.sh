#!/bin/bash
# usage: vt.sh <log> [vitest args...]   (run from analytics dir via --root)
set -u
LOG="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate74-ks1868-analytics-1889
A=$G/repo/Blockchain/Dev/services/analytics
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad
nice -n 10 $G/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" > "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
