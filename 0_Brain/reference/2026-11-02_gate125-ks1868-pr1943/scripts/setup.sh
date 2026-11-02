#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -c core.sshCommand="$K" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $W/repo > $W/logs/clone.log 2>&1; echo clone RC=$?
git -C $W/repo config core.sshCommand "$K"; git -C $W/repo remote set-url --push origin no_push_qa_gate
date -u > $W/logs/head_start.log
git -C $W/repo ls-remote origin refs/pull/1943/head refs/heads/develop >> $W/logs/head_start.log 2>&1
git -C $W/repo fetch origin refs/pull/1943/head:pr1943 develop > $W/logs/fetch.log 2>&1; echo fetch RC=$?
cat $W/logs/head_start.log
