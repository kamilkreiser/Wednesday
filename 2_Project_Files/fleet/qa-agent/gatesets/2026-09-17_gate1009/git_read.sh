#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1009 (KS-864 F-1007-1 follow-up) tier-2 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1009'
H=6ec0cb19834407887daa7bf5994f2da169abd30e
B=0308b7a0447a2c01c12aad358c9b4d04a5178210
D=73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5
T='Blockchain/Dev/services/api-gateway/src/__tests__'
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin 'refs/heads/feature/ks-864-f1-portal-env-var-cells' refs/pull/1009/head refs/heads/develop refs/pull/1008/head
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1) develop: $(git -C "$R" cat-file -t $D 2>&1)"
git -C "$R" log -3 --format='%H %P %an %ad %s' $H
git -C "$R" log -3 --format='%H %P %an %ad %s' $D
echo "merge-base head develop: $(git -C "$R" merge-base $H $D 2>&1)"
echo "rev-list develop..head: $(git -C "$R" rev-list --count $D..$H)  head..develop: $(git -C "$R" rev-list --count $H..$D)"
echo "--- head diff base->head (numstat, raw, no-renames)"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
echo "--- develop delta base->develop (numstat)"
git -C "$R" diff --numstat --no-renames $B $D
echo "--- commit message head"
git -C "$R" log -1 --format='%B' $H
echo "--- blobs"
for f in ks864a-dead-estate-helper.test.ts ks864b-dead-estate-portals.test.ts; do
  git -C "$R" show "$B:$T/$f" > "$GS/src/base.$f"
  git -C "$R" show "$H:$T/$f" > "$GS/src/head.$f"
done
git -C "$R" show "$H:$T/ks864c-portal-env-vars.test.ts" > "$GS/src/head.ks864c-portal-env-vars.test.ts" 2>&1
echo "ks864c show rc $?"
git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/routes/system-status.ts" > "$GS/src/head.system-status.ts"
git -C "$R" ls-tree -r $H "$T" | /usr/bin/grep -i ks864
echo "system-status blob base $(git -C "$R" rev-parse $B:Blockchain/Dev/services/api-gateway/src/routes/system-status.ts) head $(git -C "$R" rev-parse $H:Blockchain/Dev/services/api-gateway/src/routes/system-status.ts) develop $(git -C "$R" rev-parse $D:Blockchain/Dev/services/api-gateway/src/routes/system-status.ts)"
echo "api-gateway tree base $(git -C "$R" rev-parse $B:Blockchain/Dev/services/api-gateway) develop $(git -C "$R" rev-parse $D:Blockchain/Dev/services/api-gateway)"
echo "shared tree base $(git -C "$R" rev-parse $B:Blockchain/Dev/packages/shared) develop $(git -C "$R" rev-parse $D:Blockchain/Dev/packages/shared)"
echo "--- test-file counts"
for s in $B $H $D; do echo "$s $(git -C "$R" ls-tree -r --name-only $s Blockchain/Dev/services/api-gateway/src | /usr/bin/grep -c '\.test\.ts$')"; done
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees $(git -C "$R" worktree list | wc -l | tr -d ' ')"
