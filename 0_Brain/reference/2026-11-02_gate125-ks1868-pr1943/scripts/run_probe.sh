#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
S=$W/repo/Blockchain/Dev/services/originate
P=$S/src/__tests__/zz_gate125_probe.test.ts
cp $W/scripts/probe_routes.test.ts $P
export PROBE_OUT=$W/logs/probe_$1.jsonl; : > $PROBE_OUT
$S/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js --runTestsByPath $P > $W/logs/probe_$1.out 2>&1; echo jest rc=$?
mv $P $W/logs/_quarantine/zz_probe_$1.test.ts
wc -l $PROBE_OUT
