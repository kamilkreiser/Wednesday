#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1014 (KS-1176) tier-1 drafter. Read verbs only (ls-remote, cat-file, log, diff, show, ls-tree, rev-parse, merge-base, merge-tree --write-tree writes loose objects only into the object store it reads — NOT used here).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'
H=616c766a57a51238450c99bbf1d59bb109e3841c
B=e0f41a8fafd64fa31524390cfeab320e822f3d15
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-1176-connector-key-level-ranks-as-none refs/pull/1014/head refs/heads/develop refs/pull/1011/head
for c in $H $B; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
git -C "$R" log -3 --format='%H | parents %P | %an <%ae> | %ad | %s' $H
echo "merge-base head $B: $(git -C "$R" merge-base $H $B 2>&1)"
echo "--- diff base..head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
for f in services/enforcement.ts middleware/auth.ts routes/verification.ts index.ts services/redis.ts routes/platform.ts middleware/rateLimitEnforce.ts; do n=$(echo $f | tr / _); git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/head.$n" 2>> "$GS/src/show.err"; git -C "$R" show "$B:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/base.$n" 2>> "$GS/src/show.err"; done
echo "show.err bytes $(wc -c < "$GS/src/show.err")"
git -C "$R" ls-tree -r --name-only $H Blockchain/Dev/services/api-gateway/src/__tests__ | /usr/bin/grep -i 1176
echo "api-gateway tree base $(git -C "$R" rev-parse $B:Blockchain/Dev/services/api-gateway) head $(git -C "$R" rev-parse $H:Blockchain/Dev/services/api-gateway); shared base $(git -C "$R" rev-parse $B:Blockchain/Dev/packages/shared) head $(git -C "$R" rev-parse $H:Blockchain/Dev/packages/shared)"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
