#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1017 (KS-1195) tier-1 ROUND 1 drafter. Read verbs only
# (ls-remote, cat-file, log, diff, show, ls-tree, rev-parse, merge-base, grep). merge-tree --write-tree is NOT used here (it writes objects).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
H=cbe29597d11e59f2e1a14519e9ba3dbf6de9a756
C1=973eb49ef
B=7e89318bcedbc9a35757d4298ace54a6a23020bd
GW=Blockchain/Dev/services/api-gateway
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-1195-api-gateway-per-key-rate-limiter-never-fires refs/pull/1017/head refs/heads/develop refs/pull/1014/head refs/heads/feature/ks-1176-connector-key-level-ranks-as-none
DEVSHA=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
P14=$(git -C "$R" ls-remote origin refs/pull/1014/head | cut -f1)
echo "develop $DEVSHA pull/1014 $P14"
for c in $H $C1 $B $DEVSHA $P14; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
git -C "$R" log -4 --format='%H | parents %P | %an <%ae> | %ad | %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $DEVSHA 2>&1)"
echo "merge-base head pull/1014: $(git -C "$R" merge-base $H $P14 2>&1)"
echo "--- diff base..head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "--- diff base..973eb49ef raw / 973eb49ef..head raw"
git -C "$R" diff --raw --no-renames $B $C1
git -C "$R" diff --raw --no-renames $C1 $H
git -C "$R" diff --no-renames $C1 $H > "$GS/diff_c1_to_head.patch"
echo "--- diff merge-base(base,1014)..pull/1014 raw"
git -C "$R" diff --raw --no-renames $(git -C "$R" merge-base $B $P14) $P14
for f in middleware/auth.ts middleware/rateLimitEnforce.ts index.ts services/redis.ts routes/proxy.ts routes/admin.ts routes/platform.ts routes/verification.ts routes/notifications.ts services/health.ts middleware/audit.ts routes/gdpr.ts; do n=$(echo $f | tr / _); git -C "$R" show "$B:$GW/src/$f" > "$GS/src/B.$n" 2>> "$GS/src/show.err"; git -C "$R" show "$H:$GW/src/$f" > "$GS/src/H.$n" 2>> "$GS/src/show.err"; done
git -C "$R" show "$H:$GW/src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts" > "$GS/src/H.ks1195.test.ts" 2>> "$GS/src/show.err"
git -C "$R" show "$B:$GW/src/__tests__/rateLimitEnforce.test.ts" > "$GS/src/B.rateLimitEnforce.test.ts" 2>> "$GS/src/show.err"
echo "show.err bytes $(wc -c < "$GS/src/show.err")"; cat "$GS/src/show.err"
for t in $B $C1 $H $DEVSHA $P14; do echo "blobs @${t:0:9}: auth $(git -C "$R" rev-parse $t:$GW/src/middleware/auth.ts 2>&1 | cut -c1-9) rle $(git -C "$R" rev-parse $t:$GW/src/middleware/rateLimitEnforce.ts 2>&1 | cut -c1-9) index $(git -C "$R" rev-parse $t:$GW/src/index.ts 2>&1 | cut -c1-9) | api-gateway tree $(git -C "$R" rev-parse $t:$GW | cut -c1-9) shared tree $(git -C "$R" rev-parse $t:Blockchain/Dev/packages/shared | cut -c1-9) root tree $(git -C "$R" rev-parse $t^{tree} | cut -c1-9)"; done
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
