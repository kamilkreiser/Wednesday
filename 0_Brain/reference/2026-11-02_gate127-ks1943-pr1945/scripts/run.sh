#!/bin/bash
# usage: run.sh <logprefix> [jest args]
set -u
P="$1"; shift
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945
D=$W/repo/Blockchain/Dev; A=$D/services/originate
export TMPDIR=/tmp/g127
echo "node $(node -v) load $(sysctl -n vm.loadavg) $(date -u +%T)" > "$P.log"
nice -n 10 $D/node_modules/.bin/jest --rootDir $A --config $A/jest.config.js --maxWorkers=3 --forceExit --json --outputFile="$P.json" "$@" >> "$P.log" 2>&1; RC=$?
echo "rc=$RC $(date -u +%T)" >> "$P.log"; exit $RC
