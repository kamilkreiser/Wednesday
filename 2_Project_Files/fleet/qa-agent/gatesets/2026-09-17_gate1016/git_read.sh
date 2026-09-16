#!/bin/zsh
# git_read.sh — READ-ONLY git reads on the Secuura checkout for the #1016 (KS-1072) tier-1 drafter. Read verbs only.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
H=a226d94fe8c6fbfecb81de415feb645302cdd166
D=523f283c6cd2550263ec9869dc5ee722be40df4e
echo "git_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" ls-remote origin refs/pull/1016/head refs/heads/develop refs/pull/1014/head refs/pull/1015/head > "$GS/src/lsr.tmp" 2>&1; cat "$GS/src/lsr.tmp"
BR=$(git -C "$R" ls-remote origin 2>>"$GS/src/show.err" | /usr/bin/grep "^$H" | /usr/bin/grep refs/heads/ ); echo "branch(es) at head: $BR"
for c in $H $D; do echo "cat-file $c: $(git -C "$R" cat-file -t $c 2>&1)"; done
git -C "$R" log -3 --format='%H | parents %P | %an <%ae> | %ad | %s' $H
P=$(git -C "$R" rev-parse $H^)
echo "parent $P ; merge-base head develop: $(git -C "$R" merge-base $H $D 2>&1)"
echo "--- diff parent..head numstat/raw"
git -C "$R" diff --numstat --no-renames $P $H
git -C "$R" diff --raw --no-renames --abbrev=40 $P $H
git -C "$R" diff --no-renames $P $H > "$GS/diff_base_to_head.patch"
echo "patch lines $(wc -l < "$GS/diff_base_to_head.patch")"
echo "--- develop delta parent..develop"
git -C "$R" log --format='%h %s' $P..$D
git -C "$R" diff --raw --no-renames $P $D
V=Blockchain/Dev/services/api-gateway/src/routes/verification.ts
git -C "$R" show "$H:$V" > "$GS/src/verification_head.ts" 2>> "$GS/src/show.err"
git -C "$R" show "$P:$V" > "$GS/src/verification_base.ts" 2>> "$GS/src/show.err"
T=$(git -C "$R" diff --name-only $P $H | /usr/bin/grep __tests__)
echo "test file: $T"
git -C "$R" show "$H:$T" > "$GS/src/ks1072_head.test.ts" 2>> "$GS/src/show.err"
echo "blob verification.ts base $(git -C "$R" rev-parse $P:$V) head $(git -C "$R" rev-parse $H:$V) develop $(git -C "$R" rev-parse $D:$V)"
echo "wc: $(wc -l < "$GS/src/verification_base.ts") base, $(wc -l < "$GS/src/verification_head.ts") head, $(wc -l < "$GS/src/ks1072_head.test.ts") test"
echo "show.err bytes $(wc -c < "$GS/src/show.err")"
echo "api-gateway tree base $(git -C "$R" rev-parse $P:Blockchain/Dev/services/api-gateway) head $(git -C "$R" rev-parse $H:Blockchain/Dev/services/api-gateway) develop $(git -C "$R" rev-parse $D:Blockchain/Dev/services/api-gateway); shared base $(git -C "$R" rev-parse $P:Blockchain/Dev/packages/shared) head $(git -C "$R" rev-parse $H:Blockchain/Dev/packages/shared) develop $(git -C "$R" rev-parse $D:Blockchain/Dev/packages/shared)"
echo "checkout HEAD $(git -C "$R" rev-parse --short HEAD) branch $(git -C "$R" rev-parse --abbrev-ref HEAD) porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha256 $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) refs $(git -C "$R" for-each-ref | wc -l | tr -d ' ') worktrees_dir $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') worktree_list $(git -C "$R" worktree list | wc -l | tr -d ' ')"
echo "git_read end $(date '+%H:%M:%S %Z')"
