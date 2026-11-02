#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964
O=$W/repo/Blockchain/Dev/services/originate
bash $W/scripts/suites.sh
bash $W/scripts/static.sh
cp $W/scripts/zz_g149_pc.test.ts $O/src/__tests__/zz_g149_pc.test.ts
nice -n 10 node $W/scripts/jest.js --runTestsByPath $O/src/__tests__/zz_g149_pc.test.ts > $W/logs/pc_unhandled.log 2>&1; echo "rc=$?" >> $W/logs/pc_unhandled.log
mv $O/src/__tests__/zz_g149_pc.test.ts $W/logs/_quarantine/zz_g149_pc.test.ts
python3 $W/scripts/mutants.py > $W/logs/mutants_run.log 2>&1
git -C $W/repo status --short > $W/logs/chain_status_after.log
date > $W/logs/chain.done
