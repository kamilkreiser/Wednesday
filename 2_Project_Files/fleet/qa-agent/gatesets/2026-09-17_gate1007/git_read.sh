#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1007 (KS-864) tier-2 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007'
H=b28ed490ada70df2056763f4512c98443285a694
D=40fe4db6963cd11dba06bd46e0b00af39e68ef3a
SS='Blockchain/Dev/services/api-gateway/src/routes/system-status.ts'
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-864-ornith-dead-estate-pointers refs/pull/1007/head refs/heads/develop refs/pull/1005/head refs/pull/1006/head
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1)"
git -C "$R" log -3 --format='%H %P %T %an %ad %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $D 2>&1)"
echo "rev-list count develop..head: $(git -C "$R" rev-list --count $D..$H)  head..develop: $(git -C "$R" rev-list --count $H..$D)"
echo "--- head diff (numstat, raw, no-renames)"
git -C "$R" diff --numstat --no-renames $D $H
git -C "$R" diff --raw --no-renames $D $H
git -C "$R" diff --no-renames $D $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
echo "--- blobs"
git -C "$R" show "$D:$SS" > "$GS/src/system-status.base.ts"
git -C "$R" show "$H:$SS" > "$GS/src/system-status.head.ts"
for f in ks864a-dead-estate-helper.test.ts ks864b-dead-estate-portals.test.ts; do git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/__tests__/$f" > "$GS/src/$f"; done
echo "--- test-file counts (ls-tree *.test.ts under api-gateway src/__tests__)"
for s in $D $H; do echo "$s $(git -C "$R" ls-tree -r --name-only $s Blockchain/Dev/services/api-gateway/src | /usr/bin/grep -c '\.test\.ts$')"; done
echo "--- dead-estate grep -c -E 'ashypond|westeurope|secuura-staging-' system-status.ts"
echo "base $(/usr/bin/grep -c -E 'ashypond|westeurope|secuura-staging-' "$GS/src/system-status.base.ts")  head $(/usr/bin/grep -c -E 'ashypond|westeurope|secuura-staging-' "$GS/src/system-status.head.ts")"
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
