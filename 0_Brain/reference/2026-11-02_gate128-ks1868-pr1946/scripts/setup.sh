#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
R=$W/repo
git -C $R config core.sshCommand "ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1946/head:pr1946 develop 2>&1 | tail -2
{ git -C $R ls-remote origin refs/pull/1946/head refs/heads/develop; date -u; } | tee $W/logs/head_start.log
MB=$(git -C $R merge-base origin/develop pr1946); echo MB=$MB
git -C $R log --oneline $MB..pr1946
git -C $R diff --numstat $MB pr1946
git -C $R diff --numstat $MB...pr1946 >/dev/null
git -C $R diff --name-only $MB origin/develop | wc -l
