#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1006 (KS-844) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=86fe59e6bf07108142fb3dbd06bef8747d2a4687
P=e28c91f9b990273ea34036cb88ad6abf0f39e73b
DEV=40fe4db6963cd11dba06bd46e0b00af39e68ef3a
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-844-demo-service-error-handler refs/pull/1006/head refs/heads/develop
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1) | prev: $(git -C "$R" cat-file -t $P 2>&1) | develop: $(git -C "$R" cat-file -t $DEV 2>&1)"
echo "--- log head -4 (H P T an ad s)"
git -C "$R" log -4 --format='%H | parents %P | tree %T | %an | %ad | %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $DEV 2>&1)"
echo "rev-list count develop..head: $(git -C "$R" rev-list --count $DEV..$H)"
echo "rev-list count head..develop: $(git -C "$R" rev-list --count $H..$DEV)"
echo "rev-list develop..head:"; git -C "$R" rev-list --parents $DEV..$H
echo "--- numstat develop..prev (e28c91f9b)"
git -C "$R" diff --numstat $DEV $P
echo "--- raw develop..prev"
git -C "$R" diff --raw --abbrev=40 $DEV $P
echo "--- numstat prev..head (header commit)"
git -C "$R" diff --numstat $P $H
git -C "$R" diff --raw --abbrev=40 $P $H
echo "--- numstat develop..head"
git -C "$R" diff --numstat $DEV $H
git -C "$R" diff --raw --abbrev=40 $DEV $H
echo "--- commit messages"
git -C "$R" log --format='=== %H%n%B' $DEV..$H
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -c1-16) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
