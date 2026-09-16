#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1013 (KS-999) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013'
H=5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2
B=1125607e978d6ad637720c985e43e3d79fecdf88
AU='Blockchain/Dev/services/auth'
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/pull/1013/head refs/heads/develop
echo "branch for head:"; git -C "$R" ls-remote origin | /usr/bin/grep "^$H" 
D=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
echo "merge-base head develop: $(git -C "$R" merge-base $H $D)"
echo "rev-list develop..head: $(git -C "$R" rev-list --count $D..$H)  head..develop: $(git -C "$R" rev-list --count $H..$D)"
echo "--- base->head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
git -C "$R" show "$B:$AU/src/repositories/userRepo.ts" > "$GS/src/userRepo_base.ts"
git -C "$R" show "$H:$AU/src/repositories/userRepo.ts" > "$GS/src/userRepo_head.ts"
echo "--- commit message head"
git -C "$R" log -1 --format='%B' $H
echo "--- auth tree listing (src top)"
git -C "$R" ls-tree --name-only $H $AU/src/ $AU/src/routes/ $AU/ 
echo "--- getUserById callers at head (auth src)"
git -C "$R" grep -n 'getUserById' $H -- "$AU/src" | /usr/bin/grep -v __tests__
echo "--- openapi specs"
git -C "$R" ls-tree -r --name-only $H | /usr/bin/grep -iE 'openapi.*\.ya?ml$|swagger'
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
ls -laR "$R/Blockchain/Dev/services/auth/node_modules/.vite" 
ls -laR "$R/Blockchain/Dev/services/api-gateway/node_modules/.vite"
echo "end $(date '+%H:%M:%S %Z')"
