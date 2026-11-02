#!/bin/bash
# tsc incl. tests (head, base products + no new tests, planted); service tsc; eslint changed + planted; docs-fragments with planted defects.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate145-ks1868-pr1961
R=$W/repo; D=$R/Blockchain/Dev; O=$D/services/originate; B=$D/node_modules/.bin; REL=Blockchain/Dev/services/originate
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
P1=src/services/errorTrackingService.ts; P2=src/utils/lifecyclePayloadCodec.ts; H1=$(sha $O/$P1); H2=$(sha $O/$P2)
T1=src/__tests__/ks1868-error-tracking-get-recent-errors-catch-unreadable-throw.test.ts; T2=src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts
TC=$W/scripts/tsconfig.tests.json
tl(){ nice -n 10 $B/tsc -p $TC --listFilesOnly > $W/logs/tsc_files_$1.log 2>&1; nice -n 10 $B/tsc -p $TC > $W/logs/tsc_tests_$1.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$1.log; }
tl head
nice -n 10 $B/tsc -p $O/tsconfig.json --noEmit > $W/logs/tsc_service_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_head.log
echo 'export const g145planted: number = "x";' > $O/src/__tests__/zz_g145_planted.test.ts
tl planted
mv $O/src/__tests__/zz_g145_planted.test.ts $W/logs/_quarantine/zz_g145_planted.test.ts
for p in $P1 $P2; do git -C $R show 2d3b3bb3:$REL/$p > $O/$p; done
mv $O/$T1 $W/logs/_quarantine/t1.ts; mv $O/$T2 $W/logs/_quarantine/t2.ts
tl base
mv $W/logs/_quarantine/t1.ts $O/$T1; mv $W/logs/_quarantine/t2.ts $O/$T2
for p in $P1 $P2; do git -C $R show pr1961:$REL/$p > $O/$p; done
{ for f in head base planted; do echo "$f: $(grep -c 'error TS' $W/logs/tsc_tests_$f.log) errors, $(tail -1 $W/logs/tsc_tests_$f.log), files $(grep -c '/src/' $W/logs/tsc_files_$f.log) (under __tests__ $(grep -c '/src/__tests__/' $W/logs/tsc_files_$f.log)), PR test files listed $(grep -c 'ks1868-error-tracking-get-recent\|ks1868-lifecycle-payload-codec-decrypt' $W/logs/tsc_files_$f.log)"; done
  echo "planted errors: $(grep 'error TS' $W/logs/tsc_tests_planted.log | sed 's#.*/src/#src/#')"
  echo "service tsc: $(grep -c 'error TS' $W/logs/tsc_service_head.log) $(tail -1 $W/logs/tsc_service_head.log)"
  [ "$(sha $O/$P1)" = "$H1" ] && [ "$(sha $O/$P2)" = "$H2" ] && echo "tsc restore OK" || echo "tsc RESTORE FAIL"; git -C $R status --short; } > $W/logs/tsc_summary.log
