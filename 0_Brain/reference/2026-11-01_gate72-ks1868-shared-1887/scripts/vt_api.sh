#!/bin/bash
# usage: vt_api.sh <log> [vitest args...]   (runs in services/api-gateway; nice 10; waits while load1 > 8)
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate72-ks1868-shared-1887
LOG="$1"; shift
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" >&2; sleep 20; done
cd "$G/repo/Blockchain/Dev/services/api-gateway" || exit 99
nice -n 10 "$G/repo/Blockchain/Dev/node_modules/.bin/vitest" run --maxWorkers=2 "$@" > "$LOG" 2>&1
RC=$?; echo "rc=$RC" >> "$LOG"; exit $RC
