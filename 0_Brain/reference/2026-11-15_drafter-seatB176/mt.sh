export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB176
C=$D/clone_work/clone
DEV=$(git -C $C rev-parse origin/develop)
echo "develop $DEV tree $(git -C $C rev-parse origin/develop^{tree}) parents: $(git -C $C rev-list --parents -n1 origin/develop)"
for n in 2098 2089 2079 2220 2221 2222 2223 2224 2228 2225 2099 2160; do
  H=$(git -C $C rev-parse refs/remotes/pr/$n)
  MB=$(git -C $C merge-base $DEV $H)
  A=$(git -C $C merge-tree --write-tree $DEV $H 2>/dev/null); ra=$?
  B=$(git -C $C merge-tree --write-tree $H $DEV 2>/dev/null); rb=$?
  AH=$(git -C $C rev-list --count $MB..$DEV)
  NC=$(git -C $C rev-list --count $MB..$H)
  NF=$(git -C $C diff --name-only -z $MB $H | tr -cd '\0' | wc -c | tr -d ' ')
  echo "$n head=${H:0:12} mb=${MB:0:12} ahead=$AH commits=$NC files=$NF | rc $ra/$rb tree ${A:0:12} eq=$([ "$A" = "$B" ] && echo yes || echo NO)"
done
