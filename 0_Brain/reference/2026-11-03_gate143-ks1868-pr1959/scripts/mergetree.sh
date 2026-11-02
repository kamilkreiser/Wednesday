#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959; R=$W/repo
K="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"
git -C $R ls-remote origin refs/heads/develop refs/pull/1959/head
git -C $R fetch origin develop > $W/logs/fetch2.log 2>&1; echo fetch rc=$?
D=$(git -C $R rev-parse origin/develop); echo develop=$D
git -C $R log --oneline 2d3b3bb3..$D
git -C $R merge-tree --write-tree --name-only $D pr1959 > $W/logs/mergetree.out 2>&1; echo "merge-tree rc=$?"
cat $W/logs/mergetree.out
T=$(head -1 $W/logs/mergetree.out)
echo "== paths changed by result vs develop"; git -C $R diff --name-status $D $T
echo "== paths changed by PR (three-dot)"; git -C $R diff --name-status $D...pr1959
echo "== events.ts in result == pr head?"; git -C $R rev-parse $T:Blockchain/Dev/services/auth/src/events.ts pr1959:Blockchain/Dev/services/auth/src/events.ts
echo "== develop-side changes to the auth service since merge-base"; git -C $R diff --stat 2d3b3bb3 $D -- Blockchain/Dev/services/auth | tail -3
