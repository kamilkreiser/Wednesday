#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate139-ks1868-pr1956
R=$W/repo
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R config core.sshCommand "$K"
git -C $R remote set-url --push origin no_push_qa_gate
git -C $R fetch origin refs/pull/1956/head:pr1956 develop > $W/logs/fetch.log 2>&1; echo fetch rc=$?
{ date -u; git -C $R ls-remote origin refs/pull/1956/head refs/heads/develop; } | tee $W/logs/head_start.log
git -C $R checkout -q pr1956; git -C $R rev-parse HEAD origin/develop; git -C $R log --oneline -2; git -C $R merge-base pr1956 origin/develop
