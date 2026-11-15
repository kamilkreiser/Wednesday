export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB178
C=$D/clone_work/clone
DEV=$(git -C $C rev-parse origin/develop)
echo "develop $DEV tree $(git -C $C rev-parse origin/develop^{tree})"
for n in 2220 2221 2222 2098 2079 2223 2224 2081 2230; do
  H=$(git -C $C rev-parse refs/remotes/pr/$n)
  MB=$(git -C $C merge-base $DEV $H)
  A=$(git -C $C merge-tree --write-tree $DEV $H 2>/dev/null); ra=$?
  B=$(git -C $C merge-tree --write-tree $H $DEV 2>/dev/null); rb=$?
  AH=$(git -C $C rev-list --count $MB..$DEV)
  NC=$(git -C $C rev-list --count $MB..$H)
  NF=$(git -C $C diff --name-only $MB $H | wc -l | tr -d ' ')
  echo "$n head=${H:0:12} mb=${MB:0:12} ahead=$AH commits=$NC files=$NF | rc $ra/$rb tree ${A:0:12} eq=$([ "$A" = "$B" ] && echo yes || echo NO)"
done
echo "--- 2081 vs 2230 (head vs head; merge-tree with each other)"
H1=$(git -C $C rev-parse refs/remotes/pr/2081); H2=$(git -C $C rev-parse refs/remotes/pr/2230)
git -C $C merge-tree --write-tree $H1 $H2 > $D/mt_2081_2230.out 2>&1; echo "2081+2230 direct rc=$?"; head -8 $D/mt_2081_2230.out
git -C $C merge-tree --write-tree $H2 $H1 > /dev/null 2>&1; echo "reverse rc=$?"
echo "--- file lists"
for n in 2081 2230; do H=$(git -C $C rev-parse refs/remotes/pr/$n); MB=$(git -C $C merge-base $DEV $H); echo "PR $n mb ${MB:0:12}"; git -C $C diff --numstat $MB $H; done
