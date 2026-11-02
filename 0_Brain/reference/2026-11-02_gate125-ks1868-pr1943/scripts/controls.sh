#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
D=$W/repo/Blockchain/Dev; S=$D/services/originate
PL=$S/src/__tests__/zz_planted_g125.test.ts
printf "const unusedPlanted: number = 'x';\ndebugger;\n" > $PL
$S/node_modules/.bin/tsc -p $W/tsconfig.g125.json > $W/logs/tsc_planted.log 2>&1; echo tsc planted rc=$? ; /usr/bin/grep -c 'error TS' $W/logs/tsc_planted.log
(cd $D && $D/node_modules/.bin/eslint services/originate/src/__tests__/zz_planted_g125.test.ts > $W/logs/eslint_planted.log 2>&1; echo eslint planted rc=$?); tail -6 $W/logs/eslint_planted.log
mv $PL $W/logs/_quarantine/zz_planted_g125.test.ts
# base product tsc
PF=$S/src/repositories/certificationRepo.ts; H=$(shasum -a 256 < $PF)
cp $W/scratch_base_product.ts $PF
$S/node_modules/.bin/tsc -p $W/tsconfig.g125.json > $W/logs/tsc_tests_base.log 2>&1; echo tsc tests base-product rc=$? errors=$(/usr/bin/grep -c 'error TS' $W/logs/tsc_tests_base.log)
cp $W/scratch_head_product.ts $PF; [ "$(shasum -a 256 < $PF)" = "$H" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C $W/repo status --short | head
