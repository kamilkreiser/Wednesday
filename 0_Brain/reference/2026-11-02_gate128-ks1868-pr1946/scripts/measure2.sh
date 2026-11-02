#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
O=$W/repo/Blockchain/Dev/services/originate
T=$O/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts
J="$O/node_modules/.bin/jest --config $O/jest.config.js --rootDir $O --runInBand --runTestsByPath"
for i in 1 2 3; do
  L=$(uptime | sed 's/.*load averages: //')
  $J $T --no-cache --json --outputFile=$W/logs/nocache_$i.json > $W/logs/nocache_$i.log 2>&1; echo "nocache$i rc=$? load=[$L]"
done
# 3 concurrent runs x2 rounds
for r in 1 2; do
  L=$(uptime | sed 's/.*load averages: //'); echo "round$r load=[$L]"
  for k in 1 2 3; do $J $T --json --outputFile=$W/logs/par_${r}_$k.json > $W/logs/par_${r}_$k.log 2>&1 & done; wait
done
