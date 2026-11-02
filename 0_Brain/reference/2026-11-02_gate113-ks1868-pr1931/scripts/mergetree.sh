#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931/repo
L=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931/logs
date -u > $L/head_mt.log
git -C $R ls-remote origin refs/heads/develop refs/pull/1931/head >> $L/head_mt.log 2>&1
git -C $R fetch -q origin develop > $L/fetch_dev.log 2>&1; echo "fetch rc $?"
DEV=$(git -C $R rev-parse FETCH_HEAD)
{ echo "develop=$DEV"; git -C $R merge-tree --write-tree --name-only $DEV pr1931; echo "rc=$?"; } > $L/mergetree.log 2>&1
T=$(sed -n 2p $L/mergetree.log)
git -C $R diff --numstat $DEV $T > $L/mt_paths.log
git -C $R diff --name-only 968f17070208 $DEV | sort > $L/dev_paths.log
git -C $R diff --name-only 968f17070208 pr1931 | sort > $L/pr_paths.log
git -C $R diff --name-only $DEV $T | sort > $L/mt_names.log
echo "dev_moved_paths=$(wc -l < $L/dev_paths.log) shared_with_pr=$(comm -12 $L/dev_paths.log $L/pr_paths.log | wc -l) dev_auth_paths=$(grep -c 'services/auth/' $L/dev_paths.log)"
cmp -s $L/mt_names.log $L/pr_paths.log && echo SAME_PATHS || echo PATHS_DIFFER
for f in auth internal issuerCerts oauth; do P=Blockchain/Dev/services/auth/src/routes/$f.ts; echo "$f merged=$(git -C $R rev-parse $T:$P | cut -c1-8) pr=$(git -C $R rev-parse pr1931:$P | cut -c1-8) dev=$(git -C $R rev-parse $DEV:$P | cut -c1-8) base=$(git -C $R rev-parse 968f17070208:$P | cut -c1-8)"; done
