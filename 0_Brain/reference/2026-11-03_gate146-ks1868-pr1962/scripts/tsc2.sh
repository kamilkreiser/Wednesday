#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962
R=$W/repo; D=$R/Blockchain/Dev; T=$D/services/transfer; B=$D/node_modules/.bin; REL=Blockchain/Dev/services/transfer
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
P=src/services/approvalWorkflowService.ts; TN=src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts; H=$(sha $T/$P)
TC=$W/scripts/tsconfig.tests.json
tl(){ nice -n 10 $B/tsc -p $TC --listFilesOnly > $W/logs/tsc_files_$1.log 2>&1; nice -n 10 $B/tsc -p $TC > $W/logs/tsc_tests_$1.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$1.log; }
tl head
echo 'export const g146planted: number = "x";' > $T/src/__tests__/zz_g146_planted.test.ts
tl planted
mv $T/src/__tests__/zz_g146_planted.test.ts $W/logs/_quarantine/zz_g146_planted2.test.ts
git -C $R show cc33e702:$REL/$P > $T/$P; mv $T/$TN $W/logs/_quarantine/new.test.ts
tl base
mv $W/logs/_quarantine/new.test.ts $T/$TN; git -C $R show pr1962:$REL/$P > $T/$P
{ for f in head base planted; do echo "$f: $(grep -c 'error TS' $W/logs/tsc_tests_$f.log) errors, $(tail -1 $W/logs/tsc_tests_$f.log), files under transfer/src $(grep -c 'transfer/src/' $W/logs/tsc_files_$f.log) (under __tests__ $(grep -c 'transfer/src/__tests__/' $W/logs/tsc_files_$f.log)), PR test file listed $(grep -c 'ks1868-approval-workflow' $W/logs/tsc_files_$f.log)"; done
  echo "planted errors: $(grep 'error TS' $W/logs/tsc_tests_planted.log | sed 's#.*/src/#src/#')"
  echo "service tsc: $(grep -c 'error TS' $W/logs/tsc_service_head.log) $(tail -1 $W/logs/tsc_service_head.log)"
  [ "$(sha $T/$P)" = "$H" ] && echo "tsc2 restore OK" || echo "tsc2 RESTORE FAIL"; git -C $R status --short; } > $W/logs/tsc_summary.log
