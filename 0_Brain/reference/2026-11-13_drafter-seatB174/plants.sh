export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB174
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
P_ROOT=$(plant "Blockchain/Dev/package-lock.json" 15438)
P_MCP=$(plant "Blockchain/Dev/services/mcp-server/package-lock.json" 2540)
P_ENF=$(plant "Blockchain/Dev/services/api-gateway/src/services/enforcement.ts" 55)
P_AUTH=$(plant "Blockchain/Dev/services/auth/src/routes/auth.ts" 67)
P_MFA=$(plant "Blockchain/Dev/services/auth/src/routes/mfa.ts" 130)
echo "develop=$DEV"
echo "PLANT root lock hono entry line 15438 vs 2099 (root-lock PR, not queued): $(mt $P_ROOT $(h 2099))"
echo "PLANT enforcement.ts line 55 vs 2224: $(mt $P_ENF $(h 2224))"
echo "PLANT auth.ts line 67 vs 2223: $(mt $P_AUTH $(h 2223))"
echo "PLANT mfa.ts line 130 vs 2098: $(mt $P_MFA $(h 2098))"
echo "CONTROL hono-entry plants vs each queued row:"
for n in 2227 2096 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224; do echo " root-plant vs $n: $(mt $P_ROOT $(h $n)) ; mcp-plant vs $n: $(mt $P_MCP $(h $n))"; done
echo "CONTROL enf plant vs 2223 (unrelated): $(mt $P_ENF $(h 2223))"
echo "CONTROL auth plant vs 2224 (unrelated): $(mt $P_AUTH $(h 2224))"
echo "CONTROL mfa plant vs 2223 (unrelated, same dir): $(mt $P_MFA $(h 2223))"
for n in 2227 2096 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224; do echo "r118 vs $n: $(mt $(h r118) $(h $n))"; done
echo "r118 vs 2225: $(mt $(h r118) $(h 2225))"
echo "r118 vs develop: $(mt $(h r118) $DEV)"
echo "r118 vs 2160: $(mt $(h r118) $(h 2160))"
echo "2099 vs develop: $(mt $(h 2099) $DEV)"

echo "POSITIVE CONTROL root hono plant 15438 vs 2227: $(mt $P_ROOT $(h 2227))"
echo "POSITIVE CONTROL mcp hono plant 2540 vs 2227: $(mt $P_MCP $(h 2227))"
echo "CONTROL root plant on an UNRELATED root-lock line (15000) vs 2227:"
P_OTHER=$(plant "Blockchain/Dev/package-lock.json" 15000)
echo " $(mt $P_OTHER $(h 2227))"
echo "r118 vs 2227: $(mt $(h r118) $(h 2227))"
# squash analog of 2227 on develop, then each row on it
T=$(git -C $C merge-tree --write-tree $DEV $(h 2227))
SQ=$(git -C $C commit-tree $T -p $DEV -m "scratch squash analog 2227")
echo "squash-analog 2227 tree ${T:0:12}"
for n in 2096 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224 2225; do
  A=$(git -C $C merge-tree --write-tree $SQ $(h $n) 2>/dev/null); ra=$?
  B=$(git -C $C merge-tree --write-tree $(h $n) $SQ 2>/dev/null); rb=$?
  echo "on develop+2227: $n rc $ra/$rb tree ${A:0:12} equal=$([ "$A" = "$B" ] && echo yes || echo NO)"
done
# squash analog of 2096 on develop (case B: B173 merges 2096), then 2227 and each row
T6=$(git -C $C merge-tree --write-tree $DEV $(h 2096))
SQ6=$(git -C $C commit-tree $T6 -p $DEV -m "scratch squash analog 2096")
echo "squash-analog 2096 tree ${T6:0:12}"
for n in 2227 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224; do
  A=$(git -C $C merge-tree --write-tree $SQ6 $(h $n) 2>/dev/null); ra=$?
  B=$(git -C $C merge-tree --write-tree $(h $n) $SQ6 2>/dev/null); rb=$?
  echo "on develop+2096: $n rc $ra/$rb tree ${A:0:12} equal=$([ "$A" = "$B" ] && echo yes || echo NO)"
done
