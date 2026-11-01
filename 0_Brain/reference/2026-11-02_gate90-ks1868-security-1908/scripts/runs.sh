#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908
R=$G/repo; P=Blockchain/Dev/services/security/src/index.ts; M=$R/$P
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW="ks1868-security-"
H1=$(sha $M); echo "head sha $H1" | tee $G/logs/product_sha.log
cp $M $G/logs/head_index.ts
git -C $R show refs/gate/develop:$P > $G/logs/develop_index.ts
git -C $R show refs/gate/pr1908^:$P > $G/logs/mergebase_index.ts
echo "develop(3281db32) product == mergebase(8afcf256) product: $(cmp -s $G/logs/develop_index.ts $G/logs/mergebase_index.ts && echo identical || echo DIFFERENT)"
bash $G/scripts/vt.sh $G/logs/head_new_tests.log $NEW; echo "head new tests rc=$?"
cp $G/logs/mergebase_index.ts $M; echo "base product sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log $NEW; echo "red rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-security-*' --exclude '**/*.integration.test.ts' --exclude '**/node_modules/**'; echo "base whole excl new rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_incl_new.log; echo "base whole incl new rc=$?"
cp $G/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908/repo status --short
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
