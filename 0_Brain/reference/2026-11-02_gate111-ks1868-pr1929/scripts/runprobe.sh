#!/bin/bash
# Gate 111: run the probe at base and head product, under NODE_ENV test and production. Restores head after.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate111-ks1868-pr1929
G=$W/repo/Blockchain/Dev/services/governance
SVC=$G/src/services/governanceService.ts
PROBE=$G/src/__tests__/g111_probe.test.ts
cp $W/scripts/g111_probe.test.ts $PROBE
for ver in base head; do
  for ne in test production; do
    cp $W/scripts/svc_$ver.ts $SVC
    out=$W/logs/probe_${ver}_${ne}.jsonl; : > $out
    PROBE_OUT=$out PROBE_VER=$ver PROBE_NODE_ENV=$ne $G/node_modules/.bin/jest --config $G/jest.config.js --rootDir $G --testPathPattern g111_probe > $W/logs/probe_${ver}_${ne}.log 2>&1
    echo "$ver $ne rc $? lines $(wc -l < $out)"
  done
done
cp $W/scripts/svc_head.ts $SVC
mv $PROBE $W/scripts/_probe_copy_moved_out.ts
shasum -a 256 $SVC
git -C $W/repo status --short
