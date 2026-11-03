#!/bin/bash
# Gate 162 setup: shared clone of the read-only Blockchain checkout, fetch PR 1979 head + develop INTO THE CLONE.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979
S="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
R=$W/repo
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
mkdir -p $W/logs
test -e $R && { echo "repo exists, abort"; exit 1; }
git clone -q --shared --no-checkout "$S" $R; echo clone rc=$?
git -C $R remote set-url origin git@github.com:Secuura/Distributed_Secuura.git
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R config core.sshCommand "$K"
{ date -u; git -C $R ls-remote origin refs/pull/1979/head refs/heads/develop refs/heads/fix/ks-1956-milestone-award-once; } | tee $W/logs/head_start.log
git -C $R fetch -q origin refs/pull/1979/head:pr1979 +refs/heads/develop:refs/remotes/origin/develop; echo fetch rc=$?
echo "pr1979 / develop / merge-base:"
git -C $R rev-parse pr1979 origin/develop
git -C $R merge-base pr1979 origin/develop
git -C $R log --oneline -3 pr1979
git -C $R checkout -q pr1979; echo checkout rc=$?
git -C $R remote -v
