export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB175
C=$D/clone_work/clone
DEV=$(git -C $C rev-parse origin/develop)
RA=$(git -C $C rev-parse refs/remotes/pr/r118an)
SQ=$RA
for n in 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224 2225 2099 2160 2227; do
  H=$(git -C $C rev-parse refs/remotes/pr/$n)
  MB=$(git -C $C merge-base $DEV $H)
  A=$(git -C $C merge-tree --write-tree $DEV $H 2>/dev/null); ra=$?
  B=$(git -C $C merge-tree --write-tree $H $DEV 2>/dev/null); rb=$?
  CA=$(git -C $C merge-tree --write-tree $SQ $H 2>/dev/null); rca=$?
  CB=$(git -C $C merge-tree --write-tree $H $SQ 2>/dev/null); rcb=$?
  AH=$(git -C $C rev-list --count $MB..$DEV)
  NC=$(git -C $C rev-list --count $MB..$H)
  echo "$n head=${H:0:12} mb=${MB:0:12} ahead=$AH commits=$NC | A rc $ra/$rb tree ${A:0:12} eq=$([ "$A" = "$B" ] && echo yes || echo NO) | onR118 rc $rca/$rcb tree ${CA:0:12} eq=$([ "$CA" = "$CB" ] && echo yes || echo NO)"
done
