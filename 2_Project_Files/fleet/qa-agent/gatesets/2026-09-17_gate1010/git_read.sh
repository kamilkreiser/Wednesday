#!/bin/zsh
# git_read.sh — READ-ONLY git reads for the #1010 (KS-1183) tier-1 gate set. Read verbs only on the Secuura checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1010'
H=c3213b04e3ad96068c367f7e0ba426822d32cda9
B=f7c2f4acb28875e3665a61c8eaaad5c54bd3aa55
BR='refs/heads/feature/ks-1183-workflow-approve-the-forward-to-originate-has-no-timeout-so'
GW='Blockchain/Dev/services/api-gateway'
V="$GW/src/routes/verification.ts"
K="$GW/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts"
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin "$BR" refs/pull/1010/head refs/heads/develop
D=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
echo "current develop (ls-remote) $D"
echo "cat-file head: $(git -C "$R" cat-file -t $H 2>&1) base: $(git -C "$R" cat-file -t $B 2>&1) develop: $(git -C "$R" cat-file -t $D 2>&1)"
git -C "$R" log -2 --format='%H %P %an %ad %s' $H
git -C "$R" log -3 --format='%H %P %an %ad %s' $D
echo "merge-base head develop: $(git -C "$R" merge-base $H $D 2>&1)"
echo "rev-list develop..head: $(git -C "$R" rev-list --count $D..$H)  head..develop: $(git -C "$R" rev-list --count $H..$D)"
echo "--- base->head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
echo "--- base->develop numstat"
git -C "$R" diff --numstat --no-renames $B $D
echo "--- blobs verification.ts base/head/develop"
for s in $B $H $D; do echo "$s V $(git -C "$R" rev-parse $s:$V 2>&1) K $(git -C "$R" rev-parse $s:$K 2>&1)"; done
git -C "$R" show "$B:$V" > "$GS/src/verification_base.ts"
git -C "$R" show "$H:$V" > "$GS/src/verification_head.ts"
git -C "$R" show "$B:$K" > "$GS/src/ks1087_base.test.ts"
git -C "$R" show "$H:$K" > "$GS/src/ks1087_head.test.ts"
git -C "$R" show "$H:$GW/src/index.ts" > "$GS/src/gateway_index_head.ts"
echo "--- pinned files blob at base/head/develop"
for f in $GW/src/index.ts $GW/src/middleware/auth.ts $GW/src/services/redis.ts $GW/src/services/enforcement.ts $GW/package.json $GW/vitest.config.ts $GW/vitest.setup.ts $GW/tsconfig.json Blockchain/Dev/services/originate/src/routes/documents.ts Blockchain/Dev/eslint.config.mjs docs/openapi/secuura-api.yaml Blockchain/Dev/package-lock.json; do
  echo "$f base $(git -C "$R" rev-parse $B:$f 2>&1) head $(git -C "$R" rev-parse $H:$f 2>&1) develop $(git -C "$R" rev-parse $D:$f 2>&1)"
done
echo "--- nginx / ingress configs at head (ls-tree name match)"
git -C "$R" ls-tree -r --name-only $H | /usr/bin/grep -iE 'nginx|ingress|haproxy|traefik|caddy|envoy|\.conf$' | /usr/bin/grep -viE 'node_modules' 
echo "--- commit message head"
git -C "$R" log -1 --format='%B' $H
echo "--- checkout"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ')"
echo "end $(date '+%H:%M:%S %Z')"
