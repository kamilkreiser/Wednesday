#!/bin/bash
# Gate 186: merge-tree predictions, run ONLY in the gate's own clone (repo/).
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate186-ks1459-pr1798
R=$G/repo
echo "develop=$(git -C $R rev-parse refs/gate/develop) pr1798=$(git -C $R rev-parse refs/gate/pr1798) pr1796=$(git -C $R rev-parse refs/gate/pr1796)"
echo "== A: 1798 onto develop"
git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1798; echo "rc=$?"
T1=$(git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1798 | head -1)
echo "== B: 1796 onto develop"
git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1796; echo "rc=$?"
T2=$(git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1796 | head -1)
echo "== C: 1798 onto (develop+1796)  [synthetic commit object in the gate clone only]"
C2=$(git -C $R commit-tree $T2 -p refs/gate/develop -p refs/gate/pr1796 -m "gate186 synthetic develop+1796")
git -C $R merge-tree --write-tree $C2 refs/gate/pr1798; echo "rc=$?"
TC=$(git -C $R merge-tree --write-tree $C2 refs/gate/pr1798 | head -1)
echo "== D: 1796 onto (develop+1798)"
C1=$(git -C $R commit-tree $T1 -p refs/gate/develop -p refs/gate/pr1798 -m "gate186 synthetic develop+1798")
git -C $R merge-tree --write-tree $C1 refs/gate/pr1796; echo "rc=$?"
TD=$(git -C $R merge-tree --write-tree $C1 refs/gate/pr1796 | head -1)
echo "C tree == D tree (order-independent): $([ "$TC" = "$TD" ] && echo yes || echo NO)"
echo "== users.ts in combined tree vs the two PRs: hunks present"
git -C $R show $TC:Blockchain/Dev/services/auth/src/routes/users.ts > $G/scratch/users_combined.ts
/usr/bin/grep -c "const LEVEL_ORDER: readonly string\[\] = VERIFICATION_LEVEL_ORDER;" $G/scratch/users_combined.ts
git -C $R diff refs/gate/develop refs/gate/pr1796 -- Blockchain/Dev/services/auth/src/routes/users.ts | /usr/bin/grep '^+[^+]' > $G/scratch/p1796_plus.txt
n=0; m=0; while IFS= read -r l; do n=$((n+1)); /usr/bin/grep -qF -- "${l:1}" $G/scratch/users_combined.ts && m=$((m+1)); done < $G/scratch/p1796_plus.txt
echo "1796 added users.ts lines present in combined: $m/$n"
echo "== CONTROL: a planted conflicting edit must make merge-tree rc!=0"
P=$(git -C $R show refs/gate/pr1798:Blockchain/Dev/services/auth/src/routes/users.ts | sed 's/^const LEVEL_ORDER: readonly string\[\] = VERIFICATION_LEVEL_ORDER;$/const LEVEL_ORDER: readonly string[] = ["PLANTED"];/' | git -C $R hash-object -w --stdin)
TP=$(git -C $R ls-tree refs/gate/develop | git -C $R mktree)  # same root tree, rebuilt
# build a develop-child commit whose users.ts differs on the LEVEL_ORDER line
git -C $R read-tree --index-output=$G/tmp/idx refs/gate/develop
GIT_INDEX_FILE=$G/tmp/idx git -C $R update-index --cacheinfo 100644,$P,Blockchain/Dev/services/auth/src/routes/users.ts
TX=$(GIT_INDEX_FILE=$G/tmp/idx git -C $R write-tree)
CX=$(git -C $R commit-tree $TX -p refs/gate/develop -m "gate186 planted conflict control")
git -C $R merge-tree --write-tree $CX refs/gate/pr1798 > $G/scratch/control_mt.txt; echo "control rc=$? (expect 1)"
head -1 $G/scratch/control_mt.txt | cut -c1-12
/usr/bin/grep -c CONFLICT $G/scratch/control_mt.txt
