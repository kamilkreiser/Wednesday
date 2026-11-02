#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934
R=$D/repo
SSH="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
test ! -e $R || { echo repo exists; exit 1; }
git -c core.sshCommand="$SSH" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $R > $D/logs/clone.log 2>&1; echo clone rc=$?
git -C $R config core.sshCommand "$SSH"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1934/head:pr1934 develop > $D/logs/fetch.log 2>&1; echo fetch rc=$?
git -C $R ls-remote origin refs/pull/1934/head refs/heads/develop | tee $D/logs/head_start.log
git -C $R merge-base pr1934 origin/develop
git -C $R diff --numstat origin/develop...pr1934 
git -C $R diff --numstat 8f313815f415 pr1934
