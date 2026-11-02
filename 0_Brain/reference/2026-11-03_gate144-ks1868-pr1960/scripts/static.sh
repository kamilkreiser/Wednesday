#!/bin/bash
# tsc with tests (tsconfig.test.json) head and base; ratchet check.cjs; service tsc; eslint changed files + planted; docs-fragments with planted defects
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/api-gateway; B=$D/node_modules/.bin
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
P=$A/src/services/redis.ts; REL=Blockchain/Dev/services/api-gateway/src/services/redis.ts; H=$(sha $P)
TB=src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts
nice -n 10 $B/tsc -p $A/tsconfig.test.json > $W/logs/tsc_tests_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_head.log
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $W/logs/tsc_service_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_head.log
nice -n 10 node $D/scripts/typecheck-tests/check.cjs services/api-gateway > $W/logs/ratchet_head.log 2>&1; echo "rc=$?" >> $W/logs/ratchet_head.log
git -C $R show 2d3b3bb3:$REL > $P
mkdir -p $W/logs/_quarantine; mv $A/$TB $W/logs/_quarantine/new_test_during_base_tsc.ts
nice -n 10 $B/tsc -p $A/tsconfig.test.json > $W/logs/tsc_tests_base.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_base.log
mv $W/logs/_quarantine/new_test_during_base_tsc.ts $A/$TB
git -C $R show pr1960:$REL > $P; [ "$(sha $P)" = "$H" ] && echo "tsc restore OK" > $W/logs/static_restore.log || echo "tsc RESTORE FAIL" > $W/logs/static_restore.log
for f in head base; do echo "$f: $(grep -c 'error TS' $W/logs/tsc_tests_$f.log) errors $(tail -1 $W/logs/tsc_tests_$f.log)"; done > $W/logs/tsc_summary.log
echo "service tsc: $(grep -c 'error TS' $W/logs/tsc_service_head.log) $(tail -1 $W/logs/tsc_service_head.log)" >> $W/logs/tsc_summary.log
node $W/scripts/lint.js > $W/logs/eslint_summary.log 2>&1
bash $W/scripts/frag.sh > $W/logs/frag_summary.log 2>&1
git -C $R status --short > $W/logs/static_status_after.log
echo done > $W/logs/static.done
