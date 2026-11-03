#!/bin/bash
# Gate 168 static: tsc (service + tests) head/base, test-typecheck ratchet head/base, eslint head files + planted control.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/api-gateway; B=$D/node_modules/.bin; L=$W/logs
export HOME=$W/home TMPDIR=$W/tmp
[ "$(git -C $R rev-parse HEAD)" = 1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18 ] || { echo "not at head"; exit 1; }
FILES=$(git -C $R diff --name-only gh/develop pr/1985 -- Blockchain/Dev/services/api-gateway | sed 's#Blockchain/Dev/services/api-gateway/##')
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $L/tsc_service_head.log 2>&1; echo "rc=$?" >> $L/tsc_service_head.log
nice -n 10 $B/tsc -p $A/tsconfig.test.json --noEmit > $L/tsc_tests_head.log 2>&1; echo "rc=$?" >> $L/tsc_tests_head.log
nice -n 10 node $D/scripts/typecheck-tests/check.cjs services/api-gateway > $L/ratchet_head.log 2>&1; echo "rc=$?" >> $L/ratchet_head.log
bash -c "cd $A && $B/eslint $FILES" > $L/eslint_head.log 2>&1; echo "rc=$?" >> $L/eslint_head.log
printf 'export function f(): number { const unused = 1; debugger; return 2; }\n' > $A/src/zz_g168_planted.ts
bash -c "cd $A && $B/eslint src/zz_g168_planted.ts" > $L/eslint_planted.log 2>&1; echo "rc=$?" >> $L/eslint_planted.log
mkdir -p $W/mut/quarantine; mv $A/src/zz_g168_planted.ts $W/mut/quarantine/
git -C $R checkout -q --detach gh/develop
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $L/tsc_service_base.log 2>&1; echo "rc=$?" >> $L/tsc_service_base.log
nice -n 10 $B/tsc -p $A/tsconfig.test.json --noEmit > $L/tsc_tests_base.log 2>&1; echo "rc=$?" >> $L/tsc_tests_base.log
nice -n 10 node $D/scripts/typecheck-tests/check.cjs services/api-gateway > $L/ratchet_base.log 2>&1; echo "rc=$?" >> $L/ratchet_base.log
git -C $R checkout -q gate168
for f in tsc_service_head tsc_tests_head tsc_service_base tsc_tests_base; do echo "$f: $(grep -c 'error TS' $L/$f.log) errors, $(tail -1 $L/$f.log)"; done > $L/static_summary.log
grep 'error TS' $L/tsc_tests_base.log | sed 's/(.*//' | sort | uniq -c > $W/tmp/tb.txt; grep 'error TS' $L/tsc_tests_head.log | sed 's/(.*//' | sort | uniq -c > $W/tmp/th.txt
echo "tests tsc per-file diff base->head:" >> $L/static_summary.log; diff $W/tmp/tb.txt $W/tmp/th.txt >> $L/static_summary.log && echo identical >> $L/static_summary.log
for f in ratchet_head ratchet_base eslint_head eslint_planted; do echo "$f: $(tail -3 $L/$f.log | tr '\n' ' ')"; done >> $L/static_summary.log
git -C $R rev-parse HEAD >> $L/static_summary.log; git -C $R status --short >> $L/static_summary.log
echo done > $L/static.done
