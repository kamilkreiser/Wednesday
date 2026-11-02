#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931
D=$W/repo/Blockchain/Dev; A=$D/services/auth
bash $W/scripts/swap.sh head > $W/logs/swap_suite_head.log
$D/node_modules/.bin/vitest run --root $A --reporter=json --outputFile=$W/logs/suite_head.json > $W/logs/suite_head.out 2>&1; echo "suite head rc=$?"
$D/node_modules/.bin/tsc -p $A/tsconfig.test.json > $W/logs/tsc_head.log 2>&1; echo "tsc head rc=$? errors=$(grep -c 'error TS' $W/logs/tsc_head.log)"
bash $W/scripts/swap.sh base > $W/logs/swap_suite_base.log
mkdir -p $W/scripts/_held_new_tests
for t in ks1868-auth-rehash-and-logout-denylist-unreadable-throw ks1868-internal-connector-token-unreadable-throw ks1868-issuer-certs-list-revoke-unreadable-throw ks1868-oauth-authorize-token-unreadable-throw; do mv $A/src/__tests__/$t.test.ts $W/scripts/_held_new_tests/; done
$D/node_modules/.bin/vitest run --root $A --reporter=json --outputFile=$W/logs/suite_base.json > $W/logs/suite_base.out 2>&1; echo "suite base rc=$?"
$D/node_modules/.bin/tsc -p $A/tsconfig.test.json > $W/logs/tsc_base.log 2>&1; echo "tsc base rc=$? errors=$(grep -c 'error TS' $W/logs/tsc_base.log)"
for t in $W/scripts/_held_new_tests/*.ts; do mv "$t" $A/src/__tests__/; done
bash $W/scripts/swap.sh head > /dev/null
git -C $W/repo status --porcelain
