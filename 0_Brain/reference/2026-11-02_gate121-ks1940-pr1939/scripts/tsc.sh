#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate121-ks1940-pr1939
G=$W/repo/Blockchain/Dev/services/governance; TSC=$G/node_modules/.bin/tsc
SVC=$G/src/services/governanceService.ts; RT=$G/src/routes/governance.ts
NEW=$G/src/__tests__/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts
run(){ $TSC -p $1 --noEmit --listFilesOnly > $W/logs/tsc_$2_files.log 2>&1; $TSC -p $1 --noEmit > $W/logs/tsc_$2.log 2>&1; rc=$?; echo "$2 rc $rc errors $(/usr/bin/grep -c 'error TS' $W/logs/tsc_$2.log) srcfiles $(/usr/bin/grep -c "$G/src" $W/logs/tsc_$2_files.log) tests $(/usr/bin/grep -c "__tests__" $W/logs/tsc_$2_files.log)"; }
run $G/tsconfig.json plain_head
run $W/scripts/tsconfig.tests.json tests_head
cp $W/scripts/svc_base.ts $SVC; cp $W/scripts/routes_base.ts $RT; mv $NEW $W/tmp/parked.ts
run $G/tsconfig.json plain_base
run $W/scripts/tsconfig.tests.json tests_base
mv $W/tmp/parked.ts $NEW; cp $W/scripts/svc_head.ts $SVC; cp $W/scripts/routes_head.ts $RT
h=$(shasum -a 256 $NEW | cut -c1-64); cp $NEW $W/tmp/new_orig.ts
printf '\nconst g121Planted: number = "x";\n' >> $NEW
run $W/scripts/tsconfig.tests.json tests_planted
cp $W/tmp/new_orig.ts $NEW; [ "$(shasum -a 256 $NEW | cut -c1-64)" = "$h" ] && echo RESTORE_OK || echo RESTORE_FAIL
/usr/bin/grep "error TS" $W/logs/tsc_tests_planted.log | head -3
git -C $W/repo status --short
