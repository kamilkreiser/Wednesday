#!/bin/bash
# usage: vt.sh <log> [vitest args...]  (security package)
set -u
LOG="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930
A=$G/repo/Blockchain/Dev/services/security
for i in 1 2; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 10 ] && break; echo "load1=$L > 10, waiting ($i)" >&2; sleep 20; done
echo "load1 at start: $L" > "$LOG"
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a974be12-1abe-4d9a-9532-9c46296d28fc/scratchpad
nice -n 10 $G/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
