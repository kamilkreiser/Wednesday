#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate121-ks1940-pr1939
G=$W/repo/Blockchain/Dev/services/governance
SVC=$G/src/services/governanceService.ts; RT=$G/src/routes/governance.ts
NEW=$G/src/__tests__/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts
J="$G/node_modules/.bin/jest --config $G/jest.config.js --rootDir $G"
export TMPDIR=$W/tmp
# head new file x3
for i in 1 2 3; do $J --testPathPattern ks1940 --json --outputFile $W/logs/green_head_$i.json > $W/logs/green_head_$i.log 2>&1; echo "green $i rc $?"; done
# whole head suite
$J --json --outputFile $W/logs/suite_head.json > $W/logs/suite_head.log 2>&1; echo "suite head rc $?"
# base product
cp $W/scripts/svc_base.ts $SVC; cp $W/scripts/routes_base.ts $RT
$J --testPathPattern ks1940 --json --outputFile $W/logs/red_base.json > $W/logs/red_base.log 2>&1; echo "red base rc $?"
mv $NEW $W/tmp/new_test_parked.ts
$J --json --outputFile $W/logs/suite_base.json > $W/logs/suite_base.log 2>&1; echo "suite base rc $?"
mv $W/tmp/new_test_parked.ts $NEW
cp $W/scripts/svc_head.ts $SVC; cp $W/scripts/routes_head.ts $RT
git -C $W/repo status --short; echo status_rc $?
