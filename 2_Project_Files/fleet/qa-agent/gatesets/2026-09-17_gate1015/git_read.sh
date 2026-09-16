#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1015 (KS-1018) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1015'
H=77145ce84353534ba381688d5bbd16ff9ff27aef
AU='Blockchain/Dev/services/auth'
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/pull/1015/head refs/heads/develop
echo "branch for head:"; git -C "$R" ls-remote origin | /usr/bin/grep "^$H"
D=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
echo "develop now $D"
echo "cat-file head: $(git -C "$R" cat-file -t $H)"
echo "log head (parents):"; git -C "$R" log --format='%H %P %s' -3 $H
B=$(git -C "$R" merge-base $H $D)
echo "merge-base head develop: $B"
echo "rev-list develop..head: $(git -C "$R" rev-list --count $D..$H)  head..develop: $(git -C "$R" rev-list --count $H..$D)"
echo "--- base->head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames --abbrev=40 $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
P1=$(git -C "$R" log --format='%H' -2 $H | tail -1)
echo "--- commit 1 $P1 numstat"; git -C "$R" diff --numstat $B $P1
echo "--- commit 2 $H vs $P1 numstat"; git -C "$R" diff --numstat $P1 $H
git -C "$R" diff $P1 $H > "$GS/diff_commit2_typing.patch"
echo "commit2 patch lines $(wc -l < "$GS/diff_commit2_typing.patch")"
echo "--- commit messages"; git -C "$R" log --format='=== %H%n%B' $B..$H
git -C "$R" show "$B:$AU/src/routes/users.ts" > "$GS/src/users_base.ts"
git -C "$R" show "$H:$AU/src/routes/users.ts" > "$GS/src/users_head.ts"
git -C "$R" show "$P1:$AU/src/routes/users.ts" > "$GS/src/users_c1.ts"
echo "--- touched test files at head"
git -C "$R" diff --name-only $B $H
echo "--- callers of the three reads at head (auth src, non-test)"
git -C "$R" grep -n -E 'getVerificationRequest|findPendingVerificationRequest|listUserVerificationRequests|saveVerificationRequest' $H -- "$AU/src" | /usr/bin/grep -v __tests__
echo "--- positive control: grep for isInfrastructureDbError in auth src at head"
git -C "$R" grep -c 'isInfrastructureDbError' $H -- "$AU/src"
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
ls -la "$R/Blockchain/Dev/services/auth/node_modules/.vite/vitest/"*/results.json "$R/Blockchain/Dev/services/api-gateway/node_modules/.vite/vitest/"*/results.json
echo "end $(date '+%H:%M:%S %Z')"
