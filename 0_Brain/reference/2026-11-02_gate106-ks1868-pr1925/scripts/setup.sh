#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925; R=$W/repo
SSH="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
if [ -e $R ]; then echo EXISTS; else git -c core.sshCommand="$SSH" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $R > $W/logs/clone.log 2>&1; echo clone rc=$?; fi
git -C $R config core.sshCommand "$SSH"; git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1925/head:pr1925 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
(date -u; git -C $R ls-remote origin refs/pull/1925/head refs/heads/develop) > $W/logs/head_start.log; cat $W/logs/head_start.log
git -C $R merge-base origin/develop pr1925; git -C $R log --format='%H %an <%ae> %s' -2 pr1925
git -C $R checkout -q pr1925; git -C $R status --short | head
