#!/bin/bash
# usage: vt.sh <log> [vitest args...]  (billing). The child shell's cwd is set INSIDE the clone (never the WEDNESDAY root).
set -u
LOG="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate95-ks1868-pr1913
A=$G/repo/Blockchain/Dev/services/billing
for i in 1 2 3 4 5 6 7 8 9 10; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 10 ] && break; echo "load1=$L > 10, waiting ($i)" >&2; sleep 20; done
echo "load1 at start: $L" > "$LOG"
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/67d2d8aa-3620-4c8c-99c3-e332209d1f85/scratchpad
mkdir -p $TMPDIR
builtin cd "$A" || exit 9
echo "cwd: $(pwd)" >> "$LOG"
nice -n 10 $G/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
