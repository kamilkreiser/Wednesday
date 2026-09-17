#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1019 (KS-1187) tier-1 ROUND 2 delta drafter. Read verbs only
# (ls-remote, cat-file, log, diff, show, rev-parse, merge-base, status --no-optional-locks, worktree list, ls-tree). NO merge-tree --write-tree here.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019r2'
H=82f09c8bd1bfab28e4d23c180cbaffea251685be
R2=4d551f1046b55209b9ca5e4281e2cb9a868f67c2
R1=8b8996f8b290ef55c35721c30f8671f982fa5a91
C1=50a4b749ad83bac865dd4216d56b19dd7bdf50b5
OB=fa887f382b212b8da4a0a4a556bacb05ea34daaa
DV=f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed
BR=refs/heads/feature/ks-1187-security-an-absolute-form-request-target-bypasses-the-ks-843
GW=Blockchain/Dev/services/api-gateway
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "checkout BEFORE: HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
git -C "$R" ls-remote origin $BR refs/pull/1019/head refs/heads/develop refs/pull/1017/head refs/pull/1020/head
for c in $H $R2 $R1 $C1 $OB $DV; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
echo "--- log head (first-parent + all)"
git -C "$R" log -6 --format='%H | parents %P | %an | %ad | %s' $H
echo "--- log develop fa887f382..f8c7aaa39"
git -C "$R" log --format='%H | parents %P | %an | %ad | %s' $OB..$DV
echo "merge-base head develop: $(git -C "$R" merge-base $H $DV 2>&1)"
echo "merge-base r2 develop: $(git -C "$R" merge-base $R2 $DV 2>&1)"
echo "merge-base --is-ancestor develop head rc: $(git -C "$R" merge-base --is-ancestor $DV $H; echo $?)"
echo "--- diff r1..r2 numstat/raw"
git -C "$R" diff --numstat --no-renames $R1 $R2
git -C "$R" diff --raw --no-renames $R1 $R2
git -C "$R" diff --no-renames $R1 $R2 > "$GS/diff_r1_to_r2.patch"
echo "--- diff r2..head (the merge) numstat"
git -C "$R" diff --numstat --no-renames $R2 $H
echo "--- diff develop..head raw (= the PR files at head)"
git -C "$R" diff --numstat --no-renames $DV $H
git -C "$R" diff --raw --no-renames $DV $H
git -C "$R" diff --no-renames $DV $H > "$GS/diff_develop_to_head.patch"
echo "--- diff old-base..develop raw (what develop brought in)"
git -C "$R" diff --raw --no-renames $OB $DV
echo "--- diff old-base..head raw"
git -C "$R" diff --raw --no-renames $OB $H
: > "$GS/src/show.err"
for f in routes/proxy.ts __tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts __tests__/ks843-erasure-scope-gate.test.ts middleware/security.ts config/services.ts; do n=$(echo $f | tr / _); git -C "$R" show "${R1}:${GW}/src/${f}" > "$GS/src/R1.$n" 2>> "$GS/src/show.err"; git -C "$R" show "${H}:${GW}/src/${f}" > "$GS/src/H.$n" 2>> "$GS/src/show.err"; done
echo "show.err bytes $(wc -c < "$GS/src/show.err")"; cat "$GS/src/show.err"
for t in $OB $R1 $R2 $H $DV; do echo "blobs @${t:0:9}: proxy $(git -C "$R" rev-parse ${t}:${GW}/src/routes/proxy.ts 2>&1 | cut -c1-9) ks1187 $(git -C "$R" rev-parse ${t}:${GW}/src/__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts 2>&1 | cut -c1-9) ks843gate $(git -C "$R" rev-parse ${t}:${GW}/src/__tests__/ks843-erasure-scope-gate.test.ts 2>&1 | cut -c1-9) auth $(git -C "$R" rev-parse ${t}:${GW}/src/middleware/auth.ts 2>&1 | cut -c1-9) rle $(git -C "$R" rev-parse ${t}:${GW}/src/middleware/rateLimitEnforce.ts 2>&1 | cut -c1-9) index $(git -C "$R" rev-parse ${t}:${GW}/src/index.ts 2>&1 | cut -c1-9) | api-gateway tree $(git -C "$R" rev-parse ${t}:${GW} | cut -c1-9) shared tree $(git -C "$R" rev-parse ${t}:Blockchain/Dev/packages/shared | cut -c1-9) root tree $(git -C "$R" rev-parse ${t}^{tree})"; done
echo "checkout AFTER: HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
