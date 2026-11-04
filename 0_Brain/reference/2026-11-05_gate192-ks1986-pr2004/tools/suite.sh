#!/bin/bash
# Gate 192: whole originate suite + tsc + eslint at head, in the gate's own clone. CWD inside the workdir; env -i.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004
D=$W/repo/Blockchain/Dev
S=$D/services/originate
E="env -i PATH=$PATH HOME=$W/home TMPDIR=$W/tmp"
cd $W/cwd || exit 9
echo "verification.ts blob $(git -C $W/repo hash-object $S/src/routes/verification.ts)" > $W/runs/suite.out
$E $D/node_modules/.bin/jest -c $S/jest.config.js --rootDir $S --cacheDirectory $W/tmp/jestcache --json --outputFile=$W/runs/suite.json > $W/runs/suite.log 2>&1
echo "jest rc=$?" >> $W/runs/suite.out
$E $D/node_modules/.bin/tsc --noEmit -p $S/tsconfig.json > $W/runs/tsc.out 2>&1
echo "tsc rc=$? errors=$(grep -c 'error TS' $W/runs/tsc.out)" >> $W/runs/suite.out
