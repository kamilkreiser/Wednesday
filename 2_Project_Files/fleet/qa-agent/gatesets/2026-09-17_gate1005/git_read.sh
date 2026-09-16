#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1005 (KS-1073) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9
B=dd66863dd
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-1073-ornith-tier2-statusless-carveout refs/pull/1005/head refs/heads/develop
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1)"
git -C "$R" log -2 --format='%H %P %T %an %ad %s' $H
BF=$(git -C "$R" rev-parse $B); echo "base full: $BF"
echo "merge-base head develop@40fe4db69: $(git -C "$R" merge-base $H 40fe4db69 2>&1)"
echo "rev-list count base..head: $(git -C "$R" rev-list --count $B..$H)"
git -C "$R" log -4 --format='%H %P %ad %s' 40fe4db69 2>&1
echo "--- head diff"
git -C "$R" diff --numstat $B $H
git -C "$R" diff --raw $B $H
echo "--- develop delta base..40fe4db69"
git -C "$R" diff --numstat $B 40fe4db69
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -c1-16) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
