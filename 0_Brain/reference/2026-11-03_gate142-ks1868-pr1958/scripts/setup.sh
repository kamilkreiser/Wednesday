#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
[ -e $W/repo ] && { echo repo exists; exit 1; }
git -c core.sshCommand="$K" clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $W/repo > $W/logs/clone.log 2>&1; echo clone RC=$?
git -C $W/repo config core.sshCommand "$K"
git -C $W/repo remote set-url --push origin no_push_qa_gate
git -C $W/repo fetch origin refs/pull/1958/head:pr1958 >> $W/logs/clone.log 2>&1; echo fetch RC=$?
git -C $W/repo fetch origin develop >> $W/logs/clone.log 2>&1
(git -C $W/repo ls-remote origin refs/pull/1958/head refs/heads/develop; date -u) | tee $W/logs/head_start.log
