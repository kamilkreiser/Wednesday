#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta
R=$G/repo
KEY='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw'
SC="ssh -i '$KEY' -o IdentitiesOnly=yes -o BatchMode=yes"
[ -e "$R" ] && { echo "repo EXISTS, stop"; exit 1; }
git -c core.sshCommand="$SC" clone --filter=blob:none --no-checkout -q git@github.com:Secuura/Distributed_Secuura.git "$R"; echo "clone rc=$?"
git -C "$R" config core.sshCommand "$SC"
git -C "$R" remote set-url --push origin no_push_qa_gate
git -C "$R" fetch -q origin +refs/pull/1952/head:refs/gate/pr1952 +refs/heads/develop:refs/gate/develop; echo "fetch rc=$?"
git -C "$R" fetch -q origin 7fe1d809936440ac8049a994a11edd8d4d90dee9 ; echo "fetch r1 rc=$?"
git -C "$R" checkout -q -B gate136 refs/gate/pr1952; echo "checkout rc=$?"
