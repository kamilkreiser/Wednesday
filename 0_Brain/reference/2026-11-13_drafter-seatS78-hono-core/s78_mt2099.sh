#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2
git -C $C fetch origin refs/pull/2099/head:refs/remotes/pr/2099 > $F/s78_fetch2099.out 2>&1; echo fetch rc=$?
git -C $C rev-parse pr/2099
for X in s78fix s78plant; do git -C $C merge-tree --write-tree refs/scratch/$X pr/2099 > $F/s78_mt2099_$X.out 2>&1; echo "merge-tree $X vs 2099 rc=$?"; done
git -C $C merge-tree --write-tree refs/scratch/s78merged pr/2099 > $F/s78_mt2099_merged.out 2>&1; echo "merge-tree s78merged vs 2099 rc=$?"
