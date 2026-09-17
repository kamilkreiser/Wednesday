#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1019 (KS-1187) tier-1 ROUND 1 drafter. Read verbs only
# (ls-remote, cat-file, log, diff, show, rev-parse, merge-base, status --no-optional-locks, worktree list). NO merge-tree --write-tree here (it writes objects).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
H=8b8996f8b290ef55c35721c30f8671f982fa5a91
C1=50a4b749ad83bac865dd4216d56b19dd7bdf50b5
B=fa887f382b212b8da4a0a4a556bacb05ea34daaa
P17=cbe29597d11e59f2e1a14519e9ba3dbf6de9a756
BR=refs/heads/feature/ks-1187-security-an-absolute-form-request-target-bypasses-the-ks-843
GW=Blockchain/Dev/services/api-gateway
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "checkout BEFORE: HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
git -C "$R" ls-remote origin $BR refs/pull/1019/head refs/heads/develop refs/pull/1017/head
for c in $H $C1 $B $P17; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
git -C "$R" log -4 --format='%H | parents %P | %an <%ae> | %ad | %s' $H
echo "merge-base head develop: $(git -C "$R" merge-base $H $B 2>&1)"
echo "merge-base head #1017: $(git -C "$R" merge-base $H $P17 2>&1)"
echo "--- diff base..head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "--- diff base..c1 raw / c1..head raw"
git -C "$R" diff --raw --no-renames $B $C1
git -C "$R" diff --raw --no-renames $C1 $H
git -C "$R" diff --no-renames $C1 $H > "$GS/diff_c1_to_head.patch"
echo "--- diff 7e89318bc..#1017 raw (the sibling)"
git -C "$R" diff --raw --no-renames 7e89318bcedbc9a35757d4298ace54a6a23020bd $P17
: > "$GS/src/show.err"
for f in routes/proxy.ts middleware/normalisePath.ts index.ts middleware/auth.ts __tests__/ks843-erasure-scope-gate.test.ts; do n=$(echo $f | tr / _); git -C "$R" show "${B}:${GW}/src/${f}" > "$GS/src/B.$n" 2>> "$GS/src/show.err"; git -C "$R" show "${H}:${GW}/src/${f}" > "$GS/src/H.$n" 2>> "$GS/src/show.err"; done
git -C "$R" show "${C1}:${GW}/src/__tests__/ks843-erasure-scope-gate.test.ts" > "$GS/src/C1.__tests___ks843-erasure-scope-gate.test.ts" 2>> "$GS/src/show.err"
NEWT=$(git -C "$R" diff --name-only --diff-filter=A $B $H)
echo "new files: $NEWT"
for nf in ${(f)NEWT}; do git -C "$R" show "${H}:${nf}" > "$GS/src/H.new.$(basename $nf)" 2>> "$GS/src/show.err"; done
echo "show.err bytes $(wc -c < "$GS/src/show.err")"; cat "$GS/src/show.err"
for t in $B $C1 $H $P17; do echo "blobs @${t:0:9}: proxy $(git -C "$R" rev-parse ${t}:${GW}/src/routes/proxy.ts 2>&1 | cut -c1-9) normalisePath $(git -C "$R" rev-parse ${t}:${GW}/src/middleware/normalisePath.ts 2>&1 | cut -c1-9) index $(git -C "$R" rev-parse ${t}:${GW}/src/index.ts 2>&1 | cut -c1-9) auth $(git -C "$R" rev-parse ${t}:${GW}/src/middleware/auth.ts 2>&1 | cut -c1-9) ks843gate $(git -C "$R" rev-parse ${t}:${GW}/src/__tests__/ks843-erasure-scope-gate.test.ts 2>&1 | cut -c1-9) | api-gateway tree $(git -C "$R" rev-parse ${t}:${GW} | cut -c1-9) shared tree $(git -C "$R" rev-parse ${t}:Blockchain/Dev/packages/shared | cut -c1-9) root tree $(git -C "$R" rev-parse ${t}^{tree} | cut -c1-9)"; done
echo "checkout AFTER: HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
