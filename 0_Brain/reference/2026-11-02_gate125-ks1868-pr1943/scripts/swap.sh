#!/bin/bash
# usage: swap.sh <variantfile> <label> -- runs the route probe AND the new test file against the product replaced by variantfile; restores by sha.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
S=$W/repo/Blockchain/Dev/services/originate
PF=$S/src/repositories/certificationRepo.ts
H=$(shasum -a 256 < $PF)
cp $PF $W/scratch_head_product.ts
cp "$1" $PF
echo "variant sha $(shasum -a 256 < $PF)"
if [ "$3" != "noprobe" ]; then bash $W/scripts/run_probe.sh $2; fi
$S/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js --runTestsByPath $S/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts > $W/logs/newtest_$2.log 2>&1; echo newtest rc=$?
cp $W/scratch_head_product.ts $PF
[ "$(shasum -a 256 < $PF)" = "$H" ] && echo RESTORE_OK || echo RESTORE_FAIL
