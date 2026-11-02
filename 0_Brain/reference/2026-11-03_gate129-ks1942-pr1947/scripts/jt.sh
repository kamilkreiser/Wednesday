#!/bin/bash
# usage: jt.sh <log> [jest args...]  governance package, anchored with --rootDir; waits for load1 < 16 (logged)
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947
A=$G/repo/Blockchain/Dev/services/governance
LOG="$1"; shift
for i in $(seq 1 15); do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -lt 16 ] && break; sleep 20; done
echo "load1 at start: $(sysctl -n vm.loadavg)" > "$LOG"
export TMPDIR=/private/tmp/g129t; mkdir -p $TMPDIR
nice -n 10 node $G/repo/Blockchain/Dev/node_modules/jest/bin/jest.js --rootDir $A --config $A/jest.config.js --maxWorkers=2 "$@" >> "$LOG" 2>&1; RC=$?
echo "rc=$RC" >> "$LOG"; exit $RC
