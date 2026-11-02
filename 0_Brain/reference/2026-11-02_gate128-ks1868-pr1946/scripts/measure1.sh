#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
O=$W/repo/Blockchain/Dev/services/originate
PF=$O/src/services/retentionScheduler.ts
T=$O/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts
J="$O/node_modules/.bin/jest --config $O/jest.config.js --rootDir $O --runInBand --runTestsByPath"
SAVE=$(shasum -a 256 $PF|cut -d' ' -f1)
git -C $W/repo show e2a2426d221d:Blockchain/Dev/services/originate/src/services/retentionScheduler.ts > $PF
$J $T --json --outputFile=$W/logs/red_base.json > $W/logs/red_base.log 2>&1; echo red_rc=$?
git -C $W/repo checkout -q -- Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
echo restore=$([ "$(shasum -a 256 $PF|cut -d' ' -f1)" = "$SAVE" ] && echo OK || echo BAD)
for i in 1 2 3 4 5 6 7 8; do
  L=$(uptime | sed 's/.*load averages: //')
  $J $T --json --outputFile=$W/logs/green_$i.json > $W/logs/green_$i.log 2>&1; rc=$?
  echo "run$i rc=$rc load=[$L]"
done
