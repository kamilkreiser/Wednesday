export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB174
C=$D/clone
DEV=$(git -C $C rev-parse origin/develop)
for n in 2227 2096 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224 2225 2099 2160; do
  H=$(git -C $C rev-parse refs/remotes/pr/$n)
  MB=$(git -C $C merge-base $DEV $H)
  A=$(git -C $C merge-tree --write-tree $DEV $H 2>/dev/null); ra=$?
  B=$(git -C $C merge-tree --write-tree $H $DEV 2>/dev/null); rb=$?
  AH=$(git -C $C rev-list --count $MB..$DEV)
  NC=$(git -C $C rev-list --count $MB..$H)
  echo "$n head=${H:0:12} mb=${MB:0:12} ahead=$AH commits=$NC rcA=$ra rcB=$rb treeA=${A:0:12} treeB=${B:0:12} equal=$([ "$A" = "$B" ] && echo yes || echo NO)"
done
