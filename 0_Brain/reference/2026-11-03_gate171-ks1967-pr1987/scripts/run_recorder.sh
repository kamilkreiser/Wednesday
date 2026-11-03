#!/bin/bash
# usage: run_recorder.sh <label> <path-to-accountLockout.ts-to-use>
set -u
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate171-ks1967-pr1987
A=$W/repo/Blockchain/Dev/services/auth
cp "$2" $A/src/services/accountLockout.ts
cp $W/scripts/gate171-recorder.test.ts $A/src/__tests__/gate171-recorder.test.ts
mkdir -p $W/runs
env -i PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp G171_OUT=$W/runs/$1.json \
  bash -c "cd $A && npx vitest run --root $A --hookTimeout=120000 src/__tests__/gate171-recorder.test.ts" > $W/logs/rec_$1.log 2>&1
rc=$?
mv -f $A/src/__tests__/gate171-recorder.test.ts $W/scratch/last-recorder-copy.test.ts
git -C $W/repo show pr1987:Blockchain/Dev/services/auth/src/services/accountLockout.ts > $A/src/services/accountLockout.ts
echo "rec $1 rc=$rc"
