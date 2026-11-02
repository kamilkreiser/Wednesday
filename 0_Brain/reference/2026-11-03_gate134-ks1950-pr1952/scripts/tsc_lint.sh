#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952
D=$G/repo/Blockchain/Dev; A=$D/services/governance; T=$A/src/__tests__; B=$D/node_modules/.bin
MB=8150eeb3802bd9cfe5242ffbc49278c1a3739a84; Q=$G/logs/_quarantine; mkdir -p $Q
NEW=ks1950-an-admin-change-made-mid-request-is-not-reverted-by-a-stale-row-write.test.ts
K40=ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts
K42=ks1942-register-binds-the-linked-wallet-and-stake-is-admin-set.test.ts
tscrun(){ nice -n 10 $B/tsc -p $G/scripts/tsconfig.gate134-tests.json > $G/logs/$1 2>&1; echo "rc=$?" >> $G/logs/$1; echo "$1: $(/usr/bin/grep -c 'error TS' $G/logs/$1) errors, $(tail -1 $G/logs/$1)"; }
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $G/logs/tsc_plain_head.log 2>&1; echo "tsc plain head rc=$?"
tscrun tsc_tests_head.log
cp $T/$NEW $G/logs/_new_test_orig.ts; H=$(shasum -a 256 $T/$NEW | cut -c1-16)
printf '\nconst GATE134_UNUSED = 1;\n' >> $T/$NEW; tscrun tsc_tests_planted.log
cp $G/logs/_new_test_orig.ts $T/$NEW; echo "restore $( [ "$(shasum -a 256 $T/$NEW | cut -c1-16)" = "$H" ] && echo OK || echo FAIL)"
bash $G/scripts/swap.sh base > /dev/null
mv $T/$NEW $Q/$NEW.during_base_tsc
for f in $K40 $K42; do git -C $G/repo show $MB:Blockchain/Dev/services/governance/src/__tests__/$f > $T/$f; done
tscrun tsc_tests_base.log
cp $Q/$NEW.during_base_tsc $T/$NEW; cp $G/logs/tests_head/$K40 $G/logs/tests_head/$K42 $T/
bash $G/scripts/swap.sh head > /dev/null
git -C $G/repo status --short; echo "status above (empty = clean)"
