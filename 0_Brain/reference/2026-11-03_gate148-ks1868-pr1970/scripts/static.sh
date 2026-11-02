#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/api-gateway; B=$D/node_modules/.bin
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g148; mkdir -p $SC/heldtsc
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW="ks1868-audit-write-failed-catch-unreadable-throw.test.ts ks1868-brute-force-redis-catch-unreadable-throw.test.ts ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts"
PROD="security rateLimitEnforce audit"
nice -n 10 $B/tsc -p $A/tsconfig.test.json > $W/logs/tsc_tests_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_head.log
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $W/logs/tsc_service_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_head.log
nice -n 10 node $D/scripts/typecheck-tests/check.cjs services/api-gateway > $W/logs/ratchet_head.log 2>&1; echo "rc=$?" >> $W/logs/ratchet_head.log
for f in $PROD; do git -C $R show 4d1ab2cb:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $A/src/middleware/$f.ts; done
for t in $NEW; do mv $A/src/__tests__/$t $SC/heldtsc/$t; done
nice -n 10 $B/tsc -p $A/tsconfig.test.json > $W/logs/tsc_tests_base.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_base.log
nice -n 10 node $D/scripts/typecheck-tests/check.cjs services/api-gateway > $W/logs/ratchet_base.log 2>&1; echo "rc=$?" >> $W/logs/ratchet_base.log
for t in $NEW; do mv $SC/heldtsc/$t $A/src/__tests__/$t; done
for f in $PROD; do git -C $R show pr1970:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $A/src/middleware/$f.ts; done
git -C $R status --short > $W/logs/static_restore.log; echo "status lines: $(wc -l < $W/logs/static_restore.log)" >> $W/logs/static_restore.log
for f in head base; do echo "$f: $(grep -c 'error TS' $W/logs/tsc_tests_$f.log) errors $(tail -1 $W/logs/tsc_tests_$f.log)"; done > $W/logs/tsc_summary.log
grep 'error TS' $W/logs/tsc_tests_head.log | sed 's/(.*//' | sort > $SC/tsc_h.txt; grep 'error TS' $W/logs/tsc_tests_base.log | sed 's/(.*//' | sort > $SC/tsc_b.txt
echo "file-set diff head vs base:" >> $W/logs/tsc_summary.log; diff $SC/tsc_b.txt $SC/tsc_h.txt >> $W/logs/tsc_summary.log && echo identical >> $W/logs/tsc_summary.log
echo "service tsc: $(grep -c 'error TS' $W/logs/tsc_service_head.log) $(tail -1 $W/logs/tsc_service_head.log)" >> $W/logs/tsc_summary.log
node $W/scripts/lint.js > $W/logs/eslint_summary.log 2>&1
bash $W/scripts/frag.sh > $W/logs/frag_summary.log 2>&1
git -C $R status --short > $W/logs/static_status_after.log
echo done > $W/logs/static.done
