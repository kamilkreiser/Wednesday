#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; R=$W/repo
SSH="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
if [ -e $R ]; then echo EXISTS; exit 1; fi
git -c core.sshCommand="$SSH" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $R > $W/logs/clone.log 2>&1; echo clone rc=$?
git -C $R config core.sshCommand "$SSH"; git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1942/head:pr1942 refs/pull/1941/head:pr1941 refs/pull/1940/head:pr1940 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
(date -u; git -C $R ls-remote origin refs/pull/1942/head refs/pull/1941/head refs/pull/1940/head refs/heads/develop) > $W/logs/head_start.log; cat $W/logs/head_start.log
git -C $R merge-base origin/develop pr1942; git -C $R log --format='%H %P %an <%ae> %s' -2 pr1942
git -C $R checkout -q pr1942; git -C $R status --short | head
