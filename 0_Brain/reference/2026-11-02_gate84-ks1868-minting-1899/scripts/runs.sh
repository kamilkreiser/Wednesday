#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899
R=$G/repo; P=Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts; M=$R/$P
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW='ks1868-nft-'
H1=$(sha $M); echo "head sha $H1" | tee $G/logs/product_sha.log
cp $M $G/logs/head_minting.service.ts
git -C $R show refs/gate/develop:$P > $G/logs/base_minting.service.ts
git -C $R show refs/gate/pr1899^:$P > $G/logs/mergebase_minting.service.ts
echo "develop(ca36945e) product == mergebase(d7691f35) product: $(cmp -s $G/logs/base_minting.service.ts $G/logs/mergebase_minting.service.ts && echo identical || echo DIFFERENT)"
# (1) head, new tests
bash $G/scripts/vt.sh $G/logs/head_new_tests.log ks1868-nft-db-save ks1868-nft-get-nft ks1868-nft-get-user ks1868-nft-load-from; echo "head new tests rc=$?"
# (2) red at base product (parent d7691f35 product == mergebase)
cp $G/logs/mergebase_minting.service.ts $M; echo "base product sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log ks1868-nft-db-save ks1868-nft-get-nft ks1868-nft-get-user ks1868-nft-load-from; echo "red rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-nft-db-save*' --exclude '**/ks1868-nft-get-nft*' --exclude '**/ks1868-nft-get-user*' --exclude '**/ks1868-nft-load-from*'; echo "base whole rc=$?"
cp $G/logs/head_minting.service.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C $R status --short
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
