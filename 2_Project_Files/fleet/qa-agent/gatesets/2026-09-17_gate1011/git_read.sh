#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1011 (KS-871) tier-1 gate set. Read verbs only on the Secuura checkout (worktree LIST is a read).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011'
H=0a1f8900c7094fbdaed1099799c029e351296b39
B=d067725ff1c7f036dbf0f726b9bf12f4daefebe7
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-871-ornith-audit-path-captured-at-entry refs/pull/1011/head refs/heads/develop refs/pull/1010/head
git -C "$R" log -2 --format='%H %P %an %ad %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $B)"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
git -C "$R" show "$B:Blockchain/Dev/services/api-gateway/src/middleware/audit.ts" > "$GS/src/base.audit.ts"
git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/middleware/audit.ts" > "$GS/src/head.audit.ts"
echo "api-gateway tree base $(git -C "$R" rev-parse $B:Blockchain/Dev/services/api-gateway) head $(git -C "$R" rev-parse $H:Blockchain/Dev/services/api-gateway)"
echo "test-file counts base $(git -C "$R" ls-tree -r --name-only $B Blockchain/Dev/services/api-gateway/src | /usr/bin/grep -i -c '\.test\.ts$') head $(git -C "$R" ls-tree -r --name-only $H Blockchain/Dev/services/api-gateway/src | /usr/bin/grep -i -c '\.test\.ts$')"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(git -C "$R" worktree list | wc -l | tr -d ' ')"
