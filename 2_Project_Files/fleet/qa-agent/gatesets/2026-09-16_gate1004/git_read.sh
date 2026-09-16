#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1004 (KS-932) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=6d077d3fe35cd5f3c09d394553d320e97b1abe32
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-932-ornith-timeout-bounds-dns refs/pull/1004/head refs/heads/develop
git -C "$R" log -3 --format='%H %P %T %an %ad %s' $H
echo "merge-base: $(git -C "$R" merge-base $H 5b4f38a48aeb40c2295895aaa5cd08e273aa7a08)"
echo "rev-list count develop..head: $(git -C "$R" rev-list --count 5b4f38a48aeb40c2295895aaa5cd08e273aa7a08..$H)"
echo "rev-list count head..develop: $(git -C "$R" rev-list --count $H..5b4f38a48aeb40c2295895aaa5cd08e273aa7a08)"
git -C "$R" log -8 --format='%h %P %ad %s' 5b4f38a48aeb40c2295895aaa5cd08e273aa7a08
git -C "$R" diff --numstat 5b4f38a48aeb40c2295895aaa5cd08e273aa7a08 $H
git -C "$R" diff --raw 5b4f38a48aeb40c2295895aaa5cd08e273aa7a08 $H
git -C "$R" diff --stat 5b4f38a48aeb40c2295895aaa5cd08e273aa7a08 $H | tail -1
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -c1-16) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
