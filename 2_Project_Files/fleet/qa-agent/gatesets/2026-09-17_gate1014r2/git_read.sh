#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1014 ROUND 2 (KS-1176) tier-1 delta drafter. Read verbs only
# (ls-remote, cat-file, log, diff, show, ls-tree, rev-parse, merge-base). merge-tree --write-tree is NOT used here (it writes objects).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'
H=9ba0caf78b8ddb737541df38303b776c982521d2
R1=616c766a57a51238450c99bbf1d59bb109e3841c
B=e0f41a8fafd64fa31524390cfeab320e822f3d15
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/heads/feature/ks-1176-connector-key-level-ranks-as-none refs/pull/1014/head refs/heads/develop refs/pull/1016/head refs/pull/1015/head
DEVSHA=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
P16=$(git -C "$R" ls-remote origin refs/pull/1016/head | cut -f1)
echo "develop $DEVSHA pull/1016 $P16"
for c in $H $R1 $B $DEVSHA $P16; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
git -C "$R" log -4 --format='%H | parents %P | %an <%ae> | %ad | %s' $H
echo "--- develop log since base"
git -C "$R" log --format='%H | parents %P | %ad | %s' $B..$DEVSHA
echo "merge-base head develop: $(git -C "$R" merge-base $H $DEVSHA 2>&1)"
echo "merge-base head pull/1016: $(git -C "$R" merge-base $H $P16 2>&1)"
echo "--- diff r1head..head numstat/raw"
git -C "$R" diff --numstat --no-renames $R1 $H
git -C "$R" diff --raw --no-renames $R1 $H
git -C "$R" diff --no-renames $R1 $H > "$GS/diff_r1head_to_head.patch"
echo "r1->r2 patch lines $(wc -l < "$GS/diff_r1head_to_head.patch")"
echo "--- diff base..head numstat/raw"
git -C "$R" diff --numstat --no-renames $B $H
git -C "$R" diff --raw --no-renames $B $H
git -C "$R" diff --no-renames $B $H > "$GS/diff_base_to_head.patch"
echo "--- diff base..develop raw"
git -C "$R" diff --raw --no-renames $B $DEVSHA
echo "--- diff merge-base(head,1016)..pull/1016 raw"
git -C "$R" diff --raw --no-renames $(git -C "$R" merge-base $H $P16) $P16
git -C "$R" diff --no-renames $(git -C "$R" merge-base $H $P16) $P16 > "$GS/diff_pr1016.patch"
for f in services/enforcement.ts routes/verification.ts; do n=$(echo $f | tr / _); for t in H R1 B; do eval s=\$$t; git -C "$R" show "$s:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/$t.$n" 2>> "$GS/src/show.err"; done; git -C "$R" show "$DEVSHA:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/DEV.$n" 2>> "$GS/src/show.err"; git -C "$R" show "$P16:Blockchain/Dev/services/api-gateway/src/$f" > "$GS/src/P16.$n" 2>> "$GS/src/show.err"; done
git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts" > "$GS/src/H.ks1176.test.ts" 2>> "$GS/src/show.err"
git -C "$R" show "$R1:Blockchain/Dev/services/api-gateway/src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts" > "$GS/src/R1.ks1176.test.ts" 2>> "$GS/src/show.err"
echo "show.err bytes $(wc -c < "$GS/src/show.err")"
for t in $B $R1 $H $DEVSHA $P16; do echo "blobs @${t:0:9}: enforcement $(git -C "$R" rev-parse $t:Blockchain/Dev/services/api-gateway/src/services/enforcement.ts 2>&1 | cut -c1-9) verification $(git -C "$R" rev-parse $t:Blockchain/Dev/services/api-gateway/src/routes/verification.ts 2>&1 | cut -c1-9) ks1176 $(git -C "$R" rev-parse $t:Blockchain/Dev/services/api-gateway/src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts 2>&1 | cut -c1-9) | api-gateway tree $(git -C "$R" rev-parse $t:Blockchain/Dev/services/api-gateway | cut -c1-9) shared tree $(git -C "$R" rev-parse $t:Blockchain/Dev/packages/shared | cut -c1-9) root tree $(git -C "$R" rev-parse $t^{tree} | cut -c1-9)"; done
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
