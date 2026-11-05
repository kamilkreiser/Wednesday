#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006
K="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw"
export GIT_SSH_COMMAND="ssh -i $K -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
mkdir -p $W/cwd $W/home $W/tmp $W/logs $W/scratch
cd $W/cwd || exit 9
git clone --shared --no-checkout "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" $W/repo > $W/logs/clone.log 2>&1; echo clone_rc=$?
git -C $W/repo remote set-url origin git@github.com:Secuura/Distributed_Secuura.git
git -C $W/repo fetch origin refs/pull/2006/head refs/heads/develop > $W/logs/fetch.log 2>&1; echo fetch_rc=$?
tail -3 $W/logs/fetch.log
git -C $W/repo rev-parse refs/remotes/origin/develop
git -C $W/repo checkout -q --detach 6311c141f99e5ade8d94e60ee15b0c80006a52cd; echo co_rc=$?
git -C $W/repo log --oneline -2
git -C $W/repo ls-remote origin refs/pull/2006/head refs/heads/develop > $W/logs/lsremote_start.txt 2>&1; cat $W/logs/lsremote_start.txt
