#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
S=$W/repo/Blockchain/Dev/services/originate
T=$S/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts
for i in 1 2 3; do
 echo "run $i $(uptime | sed 's/.*load/load/')"
 $S/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js --runTestsByPath $T > $W/logs/timing_head_$i.log 2>&1; echo rc=$?
 /usr/bin/grep -E 'R3|Tests:' $W/logs/timing_head_$i.log | cut -c1-60,150-260
done
