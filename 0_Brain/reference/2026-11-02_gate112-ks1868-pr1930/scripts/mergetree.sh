#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930
R=$W/repo; L=$W/logs; DEV=${1:-develop_now}
echo "develop ref $DEV = $(git -C $R rev-parse $DEV)"
git -C $R diff --name-only cd9c4a7dd3b8 $DEV > $L/dev_paths.log; echo "develop paths past base: $(wc -l < $L/dev_paths.log)"; cat $L/dev_paths.log
git -C $R diff --name-only cd9c4a7dd3b8 pr1930 > $L/pr_paths.log
echo "shared: $(comm -12 <(sort $L/dev_paths.log) <(sort $L/pr_paths.log) | wc -l) control(dev vs dev): $(comm -12 <(sort $L/dev_paths.log) <(sort $L/dev_paths.log) | wc -l)"
git -C $R diff --quiet cd9c4a7dd3b8 $DEV -- Blockchain/Dev/services/security Blockchain/Dev/packages/shared && echo "services/security + packages/shared unchanged base->develop"
git -C $R merge-tree --write-tree $DEV pr1930 > $L/mergetree_out.log 2>&1; echo "merge-tree rc=$?"; cat $L/mergetree_out.log
MT=$(head -1 $L/mergetree_out.log)
git -C $R diff --name-only $DEV $MT > $L/mt_paths.log
cmp -s <(sort $L/mt_paths.log) <(sort $L/pr_paths.log) && echo SAME_PATHS || echo PATHS_DIFFER
git -C $R diff --shortstat $DEV $MT
echo "merged index/db blobs: $(git -C $R rev-parse $MT:Blockchain/Dev/services/security/src/index.ts $MT:Blockchain/Dev/services/security/src/db.ts | tr '\n' ' ')"
