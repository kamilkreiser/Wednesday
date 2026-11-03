#!/bin/bash
# Gate 170 static at head: service tsc, test-typecheck ratchet, eslint on the 9 PR TS files + a planted control.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/api-gateway; B=$D/node_modules/.bin; L=$W/logs
export HOME=$W/home TMPDIR=$W/tmp
[ "$(git -C $R rev-parse HEAD)" = a0a91f65d0006d1adc69325002e6ddf69abffc2b ] || { echo "not at head"; exit 1; }
FILES=$(git -C $R diff --name-only gh/develop...gh/pr1985 -- Blockchain/Dev/services/api-gateway | sed "s#Blockchain/Dev/services/api-gateway/##" | tr "\n" " ")
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $L/tsc_service_head.log 2>&1; echo "rc=$?" >> $L/tsc_service_head.log
bash -c "cd $D && nice -n 10 node scripts/typecheck-tests/check.cjs services/api-gateway" > $L/ratchet_head.log 2>&1; echo "rc=$?" >> $L/ratchet_head.log
bash -c "cd $A && $B/eslint $FILES" > $L/eslint_head.log 2>&1; echo "rc=$?" >> $L/eslint_head.log
printf 'export function f(): number { const unused = 1; debugger; return 2; }\n' > $A/src/zz_g170_planted.ts
bash -c "cd $A && $B/eslint src/zz_g170_planted.ts" > $L/eslint_planted.log 2>&1; echo "rc=$?" >> $L/eslint_planted.log
mkdir -p $W/mut/quarantine; mv $A/src/zz_g170_planted.ts $W/mut/quarantine/
git -C $R status --short > $L/static_status_after.log
echo done > $L/static.done
