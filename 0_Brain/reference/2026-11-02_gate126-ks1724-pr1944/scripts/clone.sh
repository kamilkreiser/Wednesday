#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
date -u > $W/logs/head_start.log
git -c core.sshCommand="$K" ls-remote git@github.com:Secuura/Distributed_Secuura.git refs/pull/1944/head refs/heads/develop >> $W/logs/head_start.log 2>&1
git -c core.sshCommand="$K" clone -q --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git $W/repo > $W/logs/clone.log 2>&1; echo "clone rc=$?"
git -C $W/repo config core.sshCommand "$K"
git -C $W/repo remote set-url --push origin no_push_qa_gate
git -C $W/repo fetch -q origin refs/pull/1944/head:refs/gate/pr1944 refs/heads/develop:refs/gate/develop
git -C $W/repo rev-parse refs/gate/pr1944 refs/gate/develop
git -C $W/repo remote -v
