#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
S=$W/repo/Blockchain/Dev/services/originate
PF=$S/src/repositories/certificationRepo.ts
H=$(shasum -a 256 < $PF)
cp $W/scratch_base_product.ts $PF
echo "load $(uptime)" > $W/logs/suite_base_excl_new.log
$S/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js --silent --testPathIgnorePatterns 'ks1868-certification-repo-list-and-shares-catches' '/node_modules/' '\.integration\.test\.ts$' >> $W/logs/suite_base_excl_new.log 2>&1; echo "jest rc=$?" >> $W/logs/suite_base_excl_new.log
cp $W/scratch_head_product.ts $PF
[ "$(shasum -a 256 < $PF)" = "$H" ] && echo RESTORE_OK || echo RESTORE_FAIL
python3 $W/scripts/mutants.py > $W/logs/mutants_run.out 2>&1
shasum -a 256 < $PF
echo ALLDONE
