#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta
D=$G/repo/Blockchain/Dev; A=$D/services/governance; T=$A/src/__tests__; B=$D/node_modules/.bin
NEW=ks1950-an-admin-change-made-mid-request-is-not-reverted-by-a-stale-row-write.test.ts
tscrun(){ nice -n 10 $B/tsc -p $G/scripts/tsconfig.gate136-tests.json > $G/logs/$1 2>&1; echo "rc=$?" >> $G/logs/$1; echo "$1: $(/usr/bin/grep -c 'error TS' $G/logs/$1) errors, $(tail -1 $G/logs/$1)"; }
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $G/logs/tsc_plain_head.log 2>&1; echo "tsc plain head rc=$?"
tscrun tsc_tests_head.log
cp $T/$NEW $G/logs/_new_test_orig.ts; H=$(shasum -a 256 $T/$NEW | cut -c1-16)
printf '\nconst GATE136_UNUSED = 1;\n' >> $T/$NEW; tscrun tsc_tests_planted.log
cp $G/logs/_new_test_orig.ts $T/$NEW; echo "restore $( [ "$(shasum -a 256 $T/$NEW | cut -c1-16)" = "$H" ] && echo OK || echo FAIL)"
bash $G/scripts/swap.sh r1 > /dev/null; tscrun tsc_tests_r1prod.log; bash $G/scripts/swap.sh head
git -C $G/repo status --short; echo "status above (empty = clean)"
