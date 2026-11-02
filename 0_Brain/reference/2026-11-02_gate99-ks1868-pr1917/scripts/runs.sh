#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917
A=$W/repo/Blockchain/Dev/services/tenant-provisioning; M=$A/src/index.ts; T=$A/src/__tests__
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW="ks1868-tenant-provisioning-delete-catches-p2 ks1868-tenant-provisioning-route-catches-p1 ks1868-tenant-provisioning-zod-precheck"
echo "diff ks1410 base..head (empty = unchanged):"; git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo diff --stat 03977e89a343 pr/1917 -- Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts
bash $W/scripts/vt.sh $W/logs/head_whole.log; echo "head whole rc=$?"
bash $W/scripts/vt.sh $W/logs/head_ks1410_ks1861.log ks1410 ks1861; echo "head 1410/1861 rc=$?"
cp $W/logs/base_index.ts $M; echo "base product $(sha $M)"
bash $W/scripts/vt.sh $W/logs/base_new_tests.log $NEW; echo "base+new rc=$?"
mkdir -p $W/logs/_stash; for f in $T/ks1868-tenant-provisioning-*.test.ts; do mv "$f" $W/logs/_stash/; done
bash $W/scripts/vt.sh $W/logs/base_whole_excl_new.log; echo "base whole excl new rc=$?"
mv $W/logs/_stash/*.test.ts $T/
cp $W/logs/head_index.ts $M
[ "$(sha $M)" = "$(sha $W/logs/head_index.ts)" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo status --short
