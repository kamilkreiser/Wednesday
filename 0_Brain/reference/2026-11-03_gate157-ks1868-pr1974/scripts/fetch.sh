#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974/repo
K="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw"
export GIT_SSH_COMMAND="ssh -i '$K' -o IdentitiesOnly=yes"
git -C $R fetch -q git@github.com:Secuura/Distributed_Secuura.git refs/pull/1974/head:refs/remotes/gate/pr1974 refs/heads/develop:refs/remotes/gate/develop; echo fetch rc=$?
git -C $R rev-parse refs/remotes/gate/pr1974 refs/remotes/gate/pr1974^ refs/remotes/gate/develop
git -C $R log --oneline -1 refs/remotes/gate/pr1974
git -C $R diff --stat refs/remotes/gate/pr1974^ refs/remotes/gate/pr1974
