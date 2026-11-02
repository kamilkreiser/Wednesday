#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962
R=$W/repo
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
test -e $R && { echo "repo exists, abort"; exit 1; }
git -c core.sshCommand="$K" clone -q --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $R > $W/logs/clone.log 2>&1; echo clone rc=$?
git -C $R config core.sshCommand "$K"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1962/head:pr1962 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ date -u; git -C $R ls-remote origin refs/pull/1962/head refs/heads/develop; } | tee $W/logs/head_start.log
git -C $R checkout -q pr1962; git -C $R rev-parse HEAD origin/develop; git -C $R merge-base pr1962 origin/develop
git -C $R diff --numstat origin/develop...pr1962 | tee $W/logs/diffstat.log
git -C $R log --oneline cc33e702..pr1962
git -C $R remote -v
