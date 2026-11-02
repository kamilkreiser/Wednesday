#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947
D=$G/repo/Blockchain/Dev; A=$D/services/governance; T=$A/src/__tests__; B=$D/node_modules/.bin
MB=1584c0f0ff808fddf35245bee41b6b5f9231054c; Q=$G/logs/_quarantine
NEW=ks1942-register-binds-the-linked-wallet-and-stake-is-admin-set.test.ts
tscrun(){ nice -n 10 $B/tsc -p $G/scripts/tsconfig.gate129-tests.json > $G/logs/$1 2>&1; echo "rc=$?" >> $G/logs/$1; echo "$1: $(/usr/bin/grep -c 'error TS' $G/logs/$1) errors, $(tail -1 $G/logs/$1)"; }
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $G/logs/tsc_plain_head.log 2>&1; echo "tsc plain head rc=$?"
tscrun tsc_tests_head.log
# planted: unused local in the new test file
cp $T/$NEW $G/logs/_new_test_orig.ts; H=$(shasum -a 256 $T/$NEW | cut -c1-16)
printf '\nconst GATE129_UNUSED = 1;\n' >> $T/$NEW; tscrun tsc_tests_planted.log
cp $G/logs/_new_test_orig.ts $T/$NEW; echo "restore $( [ "$(shasum -a 256 $T/$NEW | cut -c1-16)" = "$H" ] && echo OK || echo FAIL)"
# base: base product + base tests
bash $G/scripts/swap.sh base > /dev/null
mkdir -p $G/logs/tests_head; cp $T/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts $T/governance.test.ts $G/logs/tests_head/
mv $T/$NEW $Q/$NEW.during_base_tsc
for f in ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts governance.test.ts; do git -C $G/repo show $MB:Blockchain/Dev/services/governance/src/__tests__/$f > $T/$f; done
tscrun tsc_tests_base.log
cp $Q/$NEW.during_base_tsc $T/$NEW; cp $G/logs/tests_head/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts $G/logs/tests_head/governance.test.ts $T/
bash $G/scripts/swap.sh head > /dev/null
git -C $G/repo status --short; echo "status above (empty = clean)"
# eslint on the changed files, cwd-free via --config
CH="src/db.ts src/routes/governance.ts src/services/governanceService.ts src/__tests__/$NEW src/__tests__/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts src/__tests__/governance.test.ts"
nice -n 10 $B/eslint --config $D/eslint.config.mjs $(for f in $CH; do printf '%s/%s ' $A $f; done) > $G/logs/eslint_changed.log 2>&1; echo "rc=$?" >> $G/logs/eslint_changed.log; echo "eslint changed: $(tail -1 $G/logs/eslint_changed.log) $(/usr/bin/grep -c -i 'problem' $G/logs/eslint_changed.log) problem lines"
printf 'export function f(): number { const unused = 1; debugger; return 2; }\n' > $A/src/zz_gate129_planted.ts
nice -n 10 $B/eslint --config $D/eslint.config.mjs $A/src/zz_gate129_planted.ts > $G/logs/eslint_planted.log 2>&1; echo "rc=$?" >> $G/logs/eslint_planted.log; echo "eslint planted: $(tail -1 $G/logs/eslint_planted.log)"
mv $A/src/zz_gate129_planted.ts $Q/zz_gate129_planted.ts
git -C $G/repo status --short; echo "final status above (empty = clean)"
