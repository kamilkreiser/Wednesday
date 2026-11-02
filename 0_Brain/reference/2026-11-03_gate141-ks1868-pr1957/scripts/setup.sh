#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957
R=$W/repo
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R config core.sshCommand "$K"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1957/head:pr1957 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ date -u; git -C $R ls-remote origin refs/pull/1957/head refs/heads/develop; } | tee $W/logs/head_start.log
git -C $R checkout -q pr1957; git -C $R rev-parse HEAD origin/develop; git -C $R merge-base pr1957 origin/develop
git -C $R diff --numstat origin/develop...pr1957 | tee $W/logs/diffstat.log
