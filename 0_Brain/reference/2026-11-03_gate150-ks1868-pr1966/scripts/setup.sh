#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate150-ks1868-pr1966
R=$W/repo
mkdir -p $W/logs $W/logs/_quarantine
[ -e $R ] && { echo REPO EXISTS; exit 1; }
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -c core.sshCommand="$K" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $R > $W/logs/clone.log 2>&1; echo clone rc=$?
git -C $R config core.sshCommand "$K"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1966/head:pr1966 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ date -u; git -C $R ls-remote origin refs/pull/1966/head refs/heads/develop; } | tee $W/logs/head_start.log
git -C $R checkout -q pr1966; git -C $R rev-parse HEAD origin/develop; git -C $R merge-base pr1966 origin/develop
git -C $R diff --numstat origin/develop...pr1966 | tee $W/logs/diffstat.log; git -C $R log --oneline -3 pr1966
