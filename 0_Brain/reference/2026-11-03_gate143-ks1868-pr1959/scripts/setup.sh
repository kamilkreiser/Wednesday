#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959
R=$W/repo
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
[ -e $R ] && { echo repo exists; exit 1; }
git -c core.sshCommand="$K" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $R > $W/logs/clone.log 2>&1; echo clone rc=$?
git -C $R config core.sshCommand "$K"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1959/head:pr1959 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ date -u; git -C $R ls-remote origin refs/pull/1959/head refs/heads/develop; } | tee $W/logs/head_start.log
git -C $R checkout -q pr1959
git -C $R log --oneline -3 origin/develop
git -C $R merge-base pr1959 origin/develop
git -C $R diff --numstat origin/develop...pr1959 | tee $W/logs/diffstat.log
