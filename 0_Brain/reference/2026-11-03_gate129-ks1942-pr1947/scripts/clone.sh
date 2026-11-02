#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947
R=$G/repo
KEY='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw'
SC="ssh -i '$KEY' -o IdentitiesOnly=yes -o BatchMode=yes"
[ -e "$R" ] && { echo "repo EXISTS, stop"; exit 1; }
git -c core.sshCommand="$SC" clone --filter=blob:none --no-checkout -q git@github.com:Secuura/Distributed_Secuura.git "$R"; echo "clone rc=$?"
git -C "$R" config core.sshCommand "$SC"
git -C "$R" remote set-url --push origin no_push_qa_gate
git -C "$R" fetch -q origin +refs/pull/1947/head:refs/gate/pr1947 +refs/heads/develop:refs/gate/develop; echo "fetch rc=$?"
git -C "$R" checkout -q -B gate129 refs/gate/pr1947; echo "checkout rc=$?"
