#!/bin/bash
# usage: probe.sh base|head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941
R=$W/repo; A=$R/Blockchain/Dev/services/originate; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
FILES="src/routes/verification.ts src/routes/verificationV2.ts"
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
mkdir -p $W/logs/head_copy/src/routes $W/logs/_quarantine
for f in $FILES; do cp $A/$f $W/logs/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $W/logs/sha_before_$1.txt
if [ "$1" = base ]; then for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done; fi
for f in $FILES; do sha $A/$f; done > $W/logs/sha_probe_$1.txt
cp $W/scripts/probe.test.ts $A/src/__tests__/zz-gate123-probe.test.ts
: > $W/logs/probe_$1.jsonl
PROBE_OUT=$W/logs/probe_$1.jsonl bash $W/scripts/jest.sh $W/logs/probe_$1_jest.json $W/logs/probe_$1_jest.log zz-gate123-probe
tail -1 $W/logs/probe_$1_jest.log
mv $A/src/__tests__/zz-gate123-probe.test.ts $W/logs/_quarantine/probe_$1.test.ts
for f in $FILES; do cp $W/logs/head_copy/$f $A/$f; done; for f in $FILES; do sha $A/$f; done > $W/logs/sha_after_$1.txt; cmp $W/logs/sha_before_$1.txt $W/logs/sha_after_$1.txt && echo RESTORE_OK
git -C $R status --short
