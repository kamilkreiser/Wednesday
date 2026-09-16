#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1011 ROUND 2 drafter. Read verbs only.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1011r2'
H=6dc8256448b50de6a15519001a4f7032ace1ae19
H1=0a1f8900c7094fbdaed1099799c029e351296b39
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-871-ornith-audit-path-captured-at-entry refs/pull/1011/head refs/heads/develop
for c in $H 22c0a51a8 1125607e9 79432c797; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
echo "--- log head (first-parent + parents)"
git -C "$R" log -4 --format='%H | parents %P | %an | %ad | %s' $H
echo "--- rev-parse"
git -C "$R" rev-parse 22c0a51a8 1125607e9 79432c797 2>&1
echo "merge-base head 79432c797: $(git -C "$R" merge-base $H 79432c797 2>&1)"
echo "merge-base head 1125607e9: $(git -C "$R" merge-base $H 1125607e9 2>&1)"
echo "is 1125607e9 ancestor of 79432c797: $(git -C "$R" merge-base --is-ancestor 1125607e9 79432c797; echo rc=$?)"
echo "log 1125607e9..79432c797:"; git -C "$R" log --format='%H %P %s' 1125607e9..79432c797
echo "--- diff 79432c797..$H (numstat, raw)"
git -C "$R" diff --numstat --no-renames 79432c797 $H
git -C "$R" diff --raw --no-renames 79432c797 $H
echo "--- diff 1125607e9..$H (numstat) = the PR delta over the develop it merged"
git -C "$R" diff --numstat --no-renames 1125607e9 $H
git -C "$R" diff --raw --no-renames 1125607e9 $H
echo "--- diff 1125607e9..79432c797 (develop move, numstat)"
git -C "$R" diff --numstat --no-renames 1125607e9 79432c797
echo "--- diff round1 head $H1..$H (numstat, raw)"
git -C "$R" diff --numstat --no-renames $H1 $H
git -C "$R" diff --raw --no-renames $H1 $H
git -C "$R" diff --no-renames 1125607e9 $H > "$GS/diff_dev1125607e9_to_head.patch"
git -C "$R" diff --no-renames $H1 $H -- Blockchain/Dev/services/api-gateway/src/middleware/audit.ts > "$GS/diff_r1head_to_r2head_audit.patch"
echo "patch lines $(wc -l < "$GS/diff_dev1125607e9_to_head.patch") / $(wc -l < "$GS/diff_r1head_to_r2head_audit.patch")"
for f in middleware/audit.ts index.ts routes/versioning.ts routes/proxy.ts; do n=$(echo $f | tr / _); git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/head.$n"; git -C "$R" show "1125607e9:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/dev1125607e9.$n"; done
git -C "$R" ls-tree -r --name-only $H Blockchain/Dev/services/api-gateway/src/__tests__ | /usr/bin/grep -i ks871
echo "api-gateway tree 1125607e9 $(git -C "$R" rev-parse 1125607e9:Blockchain/Dev/services/api-gateway) 79432c797 $(git -C "$R" rev-parse 79432c797:Blockchain/Dev/services/api-gateway) head $(git -C "$R" rev-parse $H:Blockchain/Dev/services/api-gateway) r1head $(git -C "$R" rev-parse $H1:Blockchain/Dev/services/api-gateway)"
echo "test-file counts 79432c797 $(git -C "$R" ls-tree -r --name-only 79432c797 Blockchain/Dev/services/api-gateway/src | /usr/bin/grep -i -c '\.test\.ts$') head $(git -C "$R" ls-tree -r --name-only $H Blockchain/Dev/services/api-gateway/src | /usr/bin/grep -i -c '\.test\.ts$')"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
