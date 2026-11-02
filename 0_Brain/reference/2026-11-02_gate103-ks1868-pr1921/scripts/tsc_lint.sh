#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921
A=$G/repo/Blockchain/Dev/services/kyc; B=$G/repo/Blockchain/Dev/node_modules/.bin; M=$A/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }; H1=$(sha $G/logs/head_index.ts)
T(){ $B/tsc -p $G/scripts/tsconfig.gate.json --listFilesOnly 2>/dev/null | grep -c "/services/kyc/src/" > $G/logs/$1_files.log; $B/tsc -p $G/scripts/tsconfig.gate.json > $G/logs/$1.log 2>&1; echo "rc=$?" >> $G/logs/$1.log; echo "$1 rc=$(tail -1 $G/logs/$1.log) errors=$(grep -c 'error TS' $G/logs/$1.log) kyc-src-files=$(cat $G/logs/$1_files.log)"; }
T tsc_tests_head
cp $G/logs/mergebase_index.ts $M; T tsc_tests_base_product   # base product + new tests (tests compile vs base)
mkdir -p $G/logs/_quarantine/tsc_base_tests
mv $A/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts $A/src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts $G/logs/_quarantine/tsc_base_tests/
T tsc_tests_base_pure
mv $G/logs/_quarantine/tsc_base_tests/*.ts $A/src/__tests__/
cp $G/logs/head_index.ts $M; [ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
# planted TS error control
f=$A/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts; h=$(sha $f); cp $f $G/logs/_quarantine/orig_saveimage_test.ts
printf '\nconst gate103Planted: number = "x";\nvoid gate103Planted;\n' >> $f; T tsc_tests_planted; cp $G/logs/_quarantine/orig_saveimage_test.ts $f; [ "$(sha $f)" = "$h" ] && echo TEST_RESTORE_OK || echo TEST_RESTORE_FAIL
cd_eslint(){ (cd $A && $B/eslint "$@"); }
(cd $A && $B/eslint src/index.ts src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts src/__tests__/ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts) > $G/logs/eslint_pr_files.log 2>&1; echo "eslint rc=$?" | tee -a $G/logs/eslint_pr_files.log
printf 'export function f(): number { const unused = 1; debugger; return 2; }\n' > $A/src/zz_gate103_planted.ts
(cd $A && $B/eslint src/zz_gate103_planted.ts) > $G/logs/eslint_planted.log 2>&1; echo "eslint planted rc=$?" | tee -a $G/logs/eslint_planted.log
mv $A/src/zz_gate103_planted.ts $G/logs/_quarantine/
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921/repo status --short
