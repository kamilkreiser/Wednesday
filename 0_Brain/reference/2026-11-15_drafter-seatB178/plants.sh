export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB178
C=$D/clone_work/clone
DEV=$(git -C $C rev-parse origin/develop)
export GIT_AUTHOR_NAME=drafter GIT_AUTHOR_EMAIL=d@example.invalid GIT_COMMITTER_NAME=drafter GIT_COMMITTER_EMAIL=d@example.invalid
plant() {
  p="$1"; ln="$2"
  export GIT_INDEX_FILE=$D/clone_work/idx_pl_$(date +%s%N)
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
mt() { a=$(git -C $C merge-tree --write-tree $1 $2 2>/dev/null); ra=$?; b=$(git -C $C merge-tree --write-tree $2 $1 2>/dev/null); rb=$?; echo "rc $ra/$rb"; }
h() { git -C $C rev-parse refs/remotes/pr/$1; }
ROWS="2098 2089 2079 2220 2221 2222 2223 2224"
P_ENF=$(plant "Blockchain/Dev/services/api-gateway/src/services/enforcement.ts" 55)
P_AUTH=$(plant "Blockchain/Dev/services/auth/src/routes/auth.ts" 67)
P_ENF=$(plant "Blockchain/Dev/services/auth/src/routes/mfa.ts" 130)
P_LOGIN=$(plant "Blockchain/Dev/frontend/admin/src/pages/Login.tsx" 82)
P_CONF=$(plant "Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts" 82)
P_TX=$(plant "Blockchain/Dev/services/anchoring/src/cardano/transaction.ts" 60)
echo "develop=$DEV"
echo "PLANT mfa.ts 130 vs 2098: $(mt $P_ENF $(h 2098))"
echo "PLANT Login.tsx 82 vs 2220: $(mt $P_LOGIN $(h 2220))"
echo "PLANT confirmation.ts 82 vs 2081: $(mt $P_CONF $(h 2081))"
echo "PLANT transaction.ts 60 vs 2230: $(mt $P_TX $(h 2230))"
echo "CONTROL mfa plant vs 2223: $(mt $P_ENF $(h 2223))"
echo "CONTROL login plant vs 2221: $(mt $P_LOGIN $(h 2221))"
echo "CONTROL confirmation plant vs 2230: $(mt $P_CONF $(h 2230))"
echo "CONTROL transaction plant vs 2081: $(mt $P_TX $(h 2081))"
# stack: develop + 2081 merged, then 2230 (and reverse)
export GIT_AUTHOR_NAME=drafter GIT_AUTHOR_EMAIL=d@example.invalid GIT_COMMITTER_NAME=drafter GIT_COMMITTER_EMAIL=d@example.invalid
T1=$(git -C $C merge-tree --write-tree $DEV $(h 2081)); C1=$(git -C $C commit-tree $T1 -p $DEV -m scratch-2081)
git -C $C merge-tree --write-tree $C1 $(h 2230) > $D/stack_a.out 2>&1; echo "STACK develop+2081 then 2230: rc $? tree $(head -1 $D/stack_a.out | cut -c1-12)"
T2=$(git -C $C merge-tree --write-tree $DEV $(h 2230)); C2=$(git -C $C commit-tree $T2 -p $DEV -m scratch-2230)
git -C $C merge-tree --write-tree $C2 $(h 2081) > $D/stack_b.out 2>&1; echo "STACK develop+2230 then 2081: rc $? tree $(head -1 $D/stack_b.out | cut -c1-12)"
