#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900
D=$G/repo/Blockchain/Dev; A=$D/services/kyc; B=$D/node_modules/.bin
nice -n 10 $B/tsc -p $A/tsconfig.json --noEmit > $G/logs/tsc_plain_head.log 2>&1; echo "rc=$?" >> $G/logs/tsc_plain_head.log
nice -n 10 $B/tsc -p $G/scripts/tsconfig.tests.json > $G/logs/tsc_tests_head.log 2>&1; echo "rc=$?" >> $G/logs/tsc_tests_head.log
nice -n 10 $B/tsc -p $G/scripts/tsconfig.tests_excl_new.json > $G/logs/tsc_tests_excl_new_head.log 2>&1; echo "rc=$?" >> $G/logs/tsc_tests_excl_new_head.log
echo "--- tsc tests: errors naming new files:"; grep -c "ks1868-kyc-" $G/logs/tsc_tests_head.log
tail -4 $G/logs/tsc_plain_head.log $G/logs/tsc_tests_head.log $G/logs/tsc_tests_excl_new_head.log
# eslint with the workspace flat config, on the PR's six .ts files plus a positive control (an untouched kyc file)
nice -n 10 $B/eslint --config $D/eslint.config.mjs $A/src/index.ts $A/src/__tests__/ks1868-kyc-*.test.ts $A/src/userErasedSubscriber.ts > $G/logs/eslint_pr_files.log 2>&1; echo "rc=$?" >> $G/logs/eslint_pr_files.log
tail -8 $G/logs/eslint_pr_files.log
