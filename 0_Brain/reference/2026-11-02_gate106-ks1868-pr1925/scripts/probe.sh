#!/bin/bash
# usage: probe.sh base|head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925
R=$W/repo; A=$R/Blockchain/Dev/services/originate; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
FILES="src/routes/verification.ts src/routes/verificationV2.ts"
MB=fcfa5dfdba9b5fe1b4a7c4619403ff3d0e2fe54c
mkdir -p $W/logs/head_copy/src/routes $W/logs/_quarantine
for f in $FILES; do cp $A/$f $W/logs/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $W/logs/sha_before_$1.txt
if [ "$1" = base ]; then for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done; fi
cp $W/scripts/probe.test.ts $A/src/__tests__/zz-gate106-probe.test.ts
: > $W/logs/probe_$1.jsonl
(cd $A && PROBE_OUT=$W/logs/probe_$1.jsonl nice -n 10 npx jest --forceExit zz-gate106-probe > $W/logs/probe_$1_jest.log 2>&1); echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate106-probe.test.ts $W/logs/_quarantine/probe_$1.test.ts
for f in $FILES; do cp $W/logs/head_copy/$f $A/$f; done; for f in $FILES; do sha $A/$f; done > $W/logs/sha_after_$1.txt; cmp $W/logs/sha_before_$1.txt $W/logs/sha_after_$1.txt && echo RESTORE_OK
git -C $R status --short
