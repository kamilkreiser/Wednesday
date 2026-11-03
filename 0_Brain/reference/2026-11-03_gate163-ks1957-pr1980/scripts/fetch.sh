#!/bin/bash
# Gate 163: fetch develop + both PR heads from GitHub INTO MY CLONE (read-only use of the project's deploy key).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980
GIT_SSH_COMMAND='ssh -i "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw" -o IdentitiesOnly=yes -o BatchMode=yes' \
  git -C $W/repo fetch -q git@github.com:Secuura/Distributed_Secuura.git +refs/pull/1980/head:refs/remotes/pr/1980 +refs/pull/1979/head:refs/remotes/pr/1979 +refs/heads/develop:refs/remotes/gh/develop
echo "fetch rc=$?"; git -C $W/repo for-each-ref refs/remotes/pr refs/remotes/gh
