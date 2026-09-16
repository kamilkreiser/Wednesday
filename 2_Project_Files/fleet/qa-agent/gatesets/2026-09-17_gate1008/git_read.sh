#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1008 (KS-1087) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=dd7086d5aa574285beffc515f9371a438621f25d
DEV=93629700c3d219c1d8ca61d69150bb9b623fc1be
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending refs/pull/1008/head refs/heads/develop refs/pull/1006/head refs/pull/1007/head
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1) | develop: $(git -C "$R" cat-file -t $DEV 2>&1)"
echo "--- log head -3"
git -C "$R" log -3 --format='%H | parents %P | tree %T | %an | %ad | %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $DEV 2>&1)"
echo "rev-list count develop..head: $(git -C "$R" rev-list --count $DEV..$H)"
echo "rev-list count head..develop: $(git -C "$R" rev-list --count $H..$DEV)"
echo "--- numstat develop..head"
git -C "$R" diff --numstat $DEV $H
git -C "$R" diff --raw --abbrev=40 $DEV $H
echo "--- commit message"
git -C "$R" log --format='=== %H%n%B' $DEV..$H
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -c1-16) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
