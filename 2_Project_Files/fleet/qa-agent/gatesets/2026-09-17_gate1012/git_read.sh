#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1012 (KS-745) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1012'
H=e225a49480e16bb77251a5d7cbd16afdf2929550
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/pull/1012/head refs/heads/develop 'refs/heads/feature/ks-745*'
D=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
echo "current develop (ls-remote) $D"
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1) develop: $(git -C "$R" cat-file -t $D 2>&1)"
git -C "$R" log -3 --format='%H %P %an %ad %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $D 2>&1)"
B=$(git -C "$R" merge-base $H $D)
echo "rev-list develop..head: $(git -C "$R" rev-list --count $D..$H)  head..develop: $(git -C "$R" rev-list --count $H..$D)"
echo "--- base->head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
echo "--- commit message head"
git -C "$R" log -1 --format='%B' $H
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
echo "end $(date '+%H:%M:%S %Z')"
