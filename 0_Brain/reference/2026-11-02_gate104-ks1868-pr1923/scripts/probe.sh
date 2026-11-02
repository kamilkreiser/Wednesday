#!/bin/bash
# usage: probe.sh base|head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923
R=$W/repo; A=$R/Blockchain/Dev/services/originate; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
FILES="src/routes/signatories.ts src/routes/thirdPartyVerifiers.ts src/services/retentionScheduler.ts"
MB=04ff5262ad526a13c1a0df99480b76860a8d11d1
mkdir -p $W/logs/head_copy/src/routes $W/logs/head_copy/src/services $W/logs/_quarantine
for f in $FILES; do cp $A/$f $W/logs/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $W/logs/sha_before_$1.txt
if [ "$1" = base ]; then for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done; fi
for p in ${PROBES:-probe probe2}; do
  cp $W/scripts/$p.test.ts $A/src/__tests__/zz-gate104-$p.test.ts
  : > $W/logs/${p}_$1.jsonl
  (cd $A && PROBE_OUT=$W/logs/${p}_$1.jsonl nice -n 10 npx jest zz-gate104-$p > $W/logs/${p}_$1_jest.log 2>&1); echo "$p $1 rc=$?"
  mv $A/src/__tests__/zz-gate104-$p.test.ts $W/logs/_quarantine/${p}_$1.test.ts
done
for f in $FILES; do cp $W/logs/head_copy/$f $A/$f; done; for f in $FILES; do sha $A/$f; done > $W/logs/sha_after_$1.txt; cmp $W/logs/sha_before_$1.txt $W/logs/sha_after_$1.txt && echo RESTORE_OK
git -C $R status --short
