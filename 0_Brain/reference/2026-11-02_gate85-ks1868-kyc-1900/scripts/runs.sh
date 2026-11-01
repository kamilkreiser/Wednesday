#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900
R=$G/repo; P=Blockchain/Dev/services/kyc/src/index.ts; M=$R/$P
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW="ks1868-kyc-"
H1=$(sha $M); echo "head sha $H1" | tee $G/logs/product_sha.log
cp $M $G/logs/head_index.ts
git -C $R show refs/gate/develop:$P > $G/logs/develop_index.ts
git -C $R show refs/gate/pr1900^:$P > $G/logs/mergebase_index.ts
echo "develop(a1350ccb) product == mergebase(8126b22b) product: $(cmp -s $G/logs/develop_index.ts $G/logs/mergebase_index.ts && echo identical || echo DIFFERENT)"
bash $G/scripts/vt.sh $G/logs/head_new_tests.log $NEW; echo "head new tests rc=$?"
cp $G/logs/mergebase_index.ts $M; echo "base product sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log $NEW; echo "red rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-kyc-*'; echo "base whole excl new rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_incl_new.log; echo "base whole incl new rc=$?"
cp $G/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C $R status --short
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
