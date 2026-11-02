#!/bin/bash
# usage: run.sh <logprefix> [jest args]
set -u
P="$1"; shift
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate117-ks1938-pr1935
D=$G/repo/Blockchain/Dev; A=$D/services/originate
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0b6f2563-591e-4408-ab3d-78a74ca3c4e8/scratchpad
echo "node $(node -v) load $(sysctl -n vm.loadavg) $(date -u +%T)" > "$P.log"
nice -n 10 $D/node_modules/.bin/jest --rootDir $A --config $A/jest.config.js --maxWorkers=3 --forceExit --json --outputFile="$P.json" "$@" >> "$P.log" 2>&1; RC=$?
echo "rc=$RC $(date -u +%T)" >> "$P.log"; exit $RC
