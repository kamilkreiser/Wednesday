#!/bin/bash
# usage: probe.sh base|head [probe file]
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942
R=$W/repo; A=$R/Blockchain/Dev/services/originate; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
F=src/routes/certifications.ts; MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
P=${2:-probe}
mkdir -p $W/logs/head_copy/src/routes $W/logs/_quarantine
cp $A/$F $W/logs/head_copy/$F; sha $A/$F > $W/logs/sha_before_$P_$1.txt
if [ "$1" = base ]; then git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F; fi
sha $A/$F > $W/logs/sha_${P}_$1.txt
cp $W/scripts/$P.test.ts $A/src/__tests__/zz-gate124-$P.test.ts
: > $W/logs/${P}_$1.jsonl
PROBE_OUT=$W/logs/${P}_$1.jsonl bash $W/scripts/jest.sh $W/logs/${P}_$1_jest.json $W/logs/${P}_$1_jest.log zz-gate124-$P
tail -3 $W/logs/${P}_$1_jest.log
mv $A/src/__tests__/zz-gate124-$P.test.ts $W/logs/_quarantine/${P}_$1.test.ts
cp $W/logs/head_copy/$F $A/$F; sha $A/$F > $W/logs/sha_after_${P}_$1.txt; cmp $W/logs/sha_before_$P_$1.txt $W/logs/sha_after_${P}_$1.txt && echo RESTORE_OK
git -C $R status --short
