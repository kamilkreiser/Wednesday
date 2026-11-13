export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172
C=$D/clone
DEV=$(git -C $C rev-parse origin/develop)
export GIT_AUTHOR_NAME=drafter GIT_AUTHOR_EMAIL=d@example.invalid GIT_COMMITTER_NAME=drafter GIT_COMMITTER_EMAIL=d@example.invalid
IDX=$D/scratch_index
# plant PATH LINE -> prints scratch commit sha (no ref)
plant() {
  p="$1"; ln="$2"
  rm -f $IDX 2>/dev/null
  export GIT_INDEX_FILE=$IDX
  git -C $C read-tree $DEV
  git -C $C show "$DEV:$p" > $D/scratch_blob.txt
  python3 -I - "$D/scratch_blob.txt" "$ln" <<'PY'
import sys
f,ln=sys.argv[1],int(sys.argv[2])
L=open(f,encoding='utf-8').read().split('\n')
L[ln-1]=L[ln-1]+' PLANTED'
open(f,'w',encoding='utf-8').write('\n'.join(L))
PY
  b=$(git -C $C hash-object -w $D/scratch_blob.txt)
  git -C $C update-index --cacheinfo 100644,$b,"$p"
  t=$(git -C $C write-tree)
  c=$(git -C $C commit-tree $t -p $DEV -m "scratch plant $p:$ln")
  unset GIT_INDEX_FILE
  echo $c
}
mt() { # commit headref
  a=$(git -C $C merge-tree --write-tree $1 $2 2>/dev/null); ra=$?
  b=$(git -C $C merge-tree --write-tree $2 $1 2>/dev/null); rb=$?
  echo "rc $ra/$rb"
}
h() { git -C $C rev-parse refs/remotes/pr/$1; }
P_ROOT=$(plant "Blockchain/Dev/package-lock.json" 6057)
P_MCP=$(plant "Blockchain/Dev/services/mcp-server/package-lock.json" 533)
P_ENF=$(plant "Blockchain/Dev/services/api-gateway/src/services/enforcement.ts" 55)
P_AUTH=$(plant "Blockchain/Dev/services/auth/src/routes/auth.ts" 67)
P_MFA=$(plant "Blockchain/Dev/services/auth/src/routes/mfa.ts" 130)
echo "plants: root=${P_ROOT:0:12} mcp=${P_MCP:0:12} enf=${P_ENF:0:12} auth=${P_AUTH:0:12} mfa=${P_MFA:0:12}"
echo "PLANT root lock line 6057 vs 2226: $(mt $P_ROOT $(h 2226))"
echo "PLANT mcp lock line 533 vs 2226: $(mt $P_MCP $(h 2226))"
echo "PLANT enforcement.ts line 55 vs 2224: $(mt $P_ENF $(h 2224))"
echo "PLANT auth.ts line 67 vs 2223: $(mt $P_AUTH $(h 2223))"
echo "PLANT mfa.ts line 130 vs 2098: $(mt $P_MFA $(h 2098))"
echo "CONTROL root plant vs 2224 (unrelated): $(mt $P_ROOT $(h 2224))"
echo "CONTROL mcp plant vs 2098 (unrelated): $(mt $P_MCP $(h 2098))"
echo "CONTROL enf plant vs 2226 (unrelated): $(mt $P_ENF $(h 2226))"
echo "CONTROL auth plant vs 2224 (unrelated): $(mt $P_AUTH $(h 2224))"
echo "CONTROL mfa plant vs 2223 (unrelated, same dir): $(mt $P_MFA $(h 2223))"
# queue AFTER row 1 (2226) merged: scratch commit = merge tree of 2226 on develop, parent develop
T1=$(git -C $C merge-tree --write-tree $DEV $(h 2226))
D1=$(git -C $C commit-tree $T1 -p $DEV -m "scratch develop after 2226 squash")
echo "D1 (develop + 2226 as one scratch commit) tree=${T1:0:12} commit=${D1:0:12}"
for n in 2098 2097 2096 2095 2090 2089 2079 2220 2221 2222 2223 2224; do
  a=$(git -C $C merge-tree --write-tree $D1 $(h $n) 2>/dev/null); ra=$?
  b=$(git -C $C merge-tree --write-tree $(h $n) $D1 2>/dev/null); rb=$?
  echo "AFTER-2226 $n rc $ra/$rb treeA=${a:0:12} equal=$([ "$a" = "$b" ] && echo yes || echo NO)"
done
# 2226 vs each row directly (both orders) from develop
for n in 2098 2097 2096 2095 2090 2089 2079 2220 2221 2222 2223 2224; do
  echo "r118 vs $n: $(mt $(h r118) $(h $n))"
done
echo "r118 vs 2226: $(mt $(h r118) $(h 2226))"
echo "r118 vs 2225: $(mt $(h r118) $(h 2225))"
echo "r118 vs develop: $(mt $(h r118) $DEV)"
echo "r118 vs D1 (develop+2226): $(mt $(h r118) $D1)"
echo "2099 vs 2226 (informational, not queued): $(mt $(h 2099) $(h 2226))"
# tree conflict info for 2099 vs 2226
git -C $C merge-tree --write-tree --name-only $(h 2099) $(h 2226) | head -5
