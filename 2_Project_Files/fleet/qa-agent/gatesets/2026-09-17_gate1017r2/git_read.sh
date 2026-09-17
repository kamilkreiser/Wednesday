#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1017 ROUND 2 drafter. Read verbs only (ls-remote, cat-file, log, diff, show, rev-parse,
# merge-base, grep). No merge-tree --write-tree here (it writes objects). stderr kept.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017r2'
H=a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66
R1=cbe29597d11e59f2e1a14519e9ba3dbf6de9a756
B=7e89318bcedbc9a35757d4298ace54a6a23020bd
DV=fa887f382b212b8da4a0a4a556bacb05ea34daaa
GW=Blockchain/Dev/services/api-gateway
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
for c in $H $R1 $B $DV; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
git -C "$R" log -4 --format='%H | parents %P | %an <%ae> | %ad | %s' $H 2>&1
echo "merge-base head develop: $(git -C "$R" merge-base $H $DV 2>&1)"
echo "is r1 ancestor of head: $(git -C "$R" merge-base --is-ancestor $R1 $H 2>&1; echo rc=$?)"
echo "--- diff r1..head numstat/raw"
git -C "$R" diff --numstat --no-renames $R1 $H 2>&1
git -C "$R" diff --raw --no-renames $R1 $H 2>&1
git -C "$R" diff --no-renames $R1 $H > "$GS/diff_r1_to_head.patch" 2>&1
echo "--- diff base..head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H 2>&1
git -C "$R" diff --raw --no-renames $B $H 2>&1
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch" 2>&1
: > "$GS/src/show.err"
for f in middleware/auth.ts middleware/rateLimitEnforce.ts index.ts routes/proxy.ts; do n=$(echo $f | tr / _); git -C "$R" show "${B}:$GW/src/$f" > "$GS/src/B.$n" 2>> "$GS/src/show.err"; git -C "$R" show "${R1}:$GW/src/$f" > "$GS/src/R1.$n" 2>> "$GS/src/show.err"; git -C "$R" show "${H}:$GW/src/$f" > "$GS/src/H.$n" 2>> "$GS/src/show.err"; done
git -C "$R" show "${H}:$GW/src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts" > "$GS/src/H.ks1195.test.ts" 2>> "$GS/src/show.err"
git -C "$R" show "${R1}:$GW/src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts" > "$GS/src/R1.ks1195.test.ts" 2>> "$GS/src/show.err"
git -C "$R" show "${H}:Blockchain/Dev/services/security/src/index.ts" > "$GS/src/H.security_index.ts" 2>> "$GS/src/show.err"
git -C "$R" show "${DV}:Blockchain/Dev/services/originate/src/routes/adminConfig.ts" > "$GS/src/DV.originate_adminConfig.ts" 2>> "$GS/src/show.err"
echo "show.err bytes $(wc -c < "$GS/src/show.err")"; cat "$GS/src/show.err"
for t in $B $R1 $H $DV; do echo "blobs @${t:0:9}: auth $(git -C "$R" rev-parse ${t}:$GW/src/middleware/auth.ts 2>&1) rle $(git -C "$R" rev-parse ${t}:$GW/src/middleware/rateLimitEnforce.ts 2>&1) index $(git -C "$R" rev-parse ${t}:$GW/src/index.ts 2>&1 | cut -c1-9) ks1195test $(git -C "$R" rev-parse ${t}:$GW/src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts 2>&1 | cut -c1-40) ks781 $(git -C "$R" rev-parse ${t}:Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts 2>&1 | cut -c1-9) security $(git -C "$R" rev-parse ${t}:Blockchain/Dev/services/security/src/index.ts 2>&1 | cut -c1-9) | api-gateway tree $(git -C "$R" rev-parse ${t}:$GW | cut -c1-9) shared tree $(git -C "$R" rev-parse ${t}:Blockchain/Dev/packages/shared | cut -c1-9) root tree $(git -C "$R" rev-parse ${t}^{tree} | cut -c1-9)"; done
echo "git_read end $(date '+%H:%M:%S %Z')"
