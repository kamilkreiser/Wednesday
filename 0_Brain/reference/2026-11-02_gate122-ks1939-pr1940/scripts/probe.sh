#!/bin/bash
# usage: probe.sh base|head  (base = e2a2426d product, head = PR product; tests untouched)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
F=src/routes/verification.ts; MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
mkdir -p $L/head_copy $L/_quarantine
cp $A/$F $L/head_copy/verification.ts; h0=$(sha $A/$F)
[ "$1" = base ] && git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F
echo "product sha $1: $(sha $A/$F)"
cp $W/scripts/probe.test.ts $A/src/__tests__/zz-gate122-probe.test.ts
: > $L/probe_$1.jsonl
PROBE_OUT=$L/probe_$1.jsonl nice -n 10 $D/node_modules/.bin/jest --config $A/jest.config.js --rootDir $A --forceExit zz-gate122-probe > $L/probe_$1_jest.log 2>&1; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate122-probe.test.ts $L/_quarantine/probe_$1.test.ts
cp $L/head_copy/verification.ts $A/$F; [ "$(sha $A/$F)" = "$h0" ] && echo RESTORE_OK
git -C $R status --short
