#!/bin/bash
# usage: probe.sh base|head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate101-ks1868-pr1919
R=$W/repo; A=$R/Blockchain/Dev/services/originate; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
FILES="src/routes/systemErrors.ts src/services/errorTrackingService.ts src/repositories/certificationRepo.ts src/repositories/documentRepo.ts src/utils/notificationClient.ts src/routes/metering.ts"
mkdir -p $W/logs/head_copy; 
for f in $FILES; do mkdir -p $W/logs/head_copy/$(dirname $f); cp $A/$f $W/logs/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $W/logs/sha_before_$1.txt
if [ "$1" = base ]; then for f in $FILES; do git -C $R show $(git -C $R merge-base origin/develop pr1919):Blockchain/Dev/services/originate/$f > $A/$f; done; fi
for p in probe probe2; do
  cp $W/scripts/$p.test.ts $A/src/__tests__/zz-gate101-$p.test.ts
  : > $W/logs/${p}_$1.jsonl
  (cd $A && PROBE_OUT=$W/logs/${p}_$1.jsonl nice -n 10 npx jest zz-gate101-$p > $W/logs/${p}_$1_jest.log 2>&1); echo "$p $1 rc=$?"
  mkdir -p $W/logs/_quarantine; mv $A/src/__tests__/zz-gate101-$p.test.ts $W/logs/_quarantine/${p}_$1.test.ts
done
for f in $FILES; do cp $W/logs/head_copy/$f $A/$f; done; for f in $FILES; do sha $A/$f; done > $W/logs/sha_after_$1.txt; cmp $W/logs/sha_before_$1.txt $W/logs/sha_after_$1.txt && echo RESTORE_OK
git -C $R status --short
