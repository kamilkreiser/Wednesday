#!/bin/bash
# Gate 73 probe runner. usage: vp.sh <log>   nice 10; waits while load1 > 8; stderr kept.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888
LOG="$1"; shift
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" | tee -a "$LOG.wait" >&2; sleep 20; done
echo "# load at start: $(sysctl -n vm.loadavg)" > "$LOG"
nice -n 10 "$G/repo/Blockchain/Dev/node_modules/.bin/vitest" run --config "$G/scripts/vitest.probe.config.ts" "$@" >> "$LOG" 2>&1
RC=$?; echo "rc=$RC" >> "$LOG"; exit $RC
