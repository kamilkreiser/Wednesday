#!/bin/bash
# usage: runprobe.sh base|head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
O=$W/repo/Blockchain/Dev/services/originate
PF=$O/src/services/retentionScheduler.ts
T=$O/src/__tests__/zz_g128_probe.test.ts
SAVE=$(shasum -a 256 $PF|cut -d' ' -f1)
cp $W/scripts/probe.test.ts $T
if [ "$1" = base ]; then git -C $W/repo show e2a2426d221d:Blockchain/Dev/services/originate/src/services/retentionScheduler.ts > $PF; fi
PROBE_OUT=$W/logs/probe_$1.jsonl $O/node_modules/.bin/jest --config $O/jest.config.js --rootDir $O --runInBand $T > $W/logs/probe_$1.out 2>&1; echo jest_rc=$?
git -C $W/repo checkout -q -- Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
mkdir -p $W/logs/_quarantine; mv $T $W/logs/_quarantine/zz_g128_probe_$1.test.ts
echo restored=$([ "$(shasum -a 256 $PF|cut -d' ' -f1)" = "$SAVE" ] && echo OK || echo BAD)
git -C $W/repo status --short | head
