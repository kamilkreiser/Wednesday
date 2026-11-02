#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941; R=$W/repo; L=$W/logs
DEV=0e3a9b65cdd632fbc1783257c6cb9833934e1404; P40=96208f377d1496028f7c6a4eb45a78f91428ed05; P41=33644960bc2270f6850d82dbbf4323780b942b9f; MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
echo "develop=$(git -C $R rev-parse origin/develop) pr1940=$(git -C $R rev-parse pr1940) pr1941=$(git -C $R rev-parse pr1941)"
echo "merge-base(dev,1941)=$(git -C $R merge-base $DEV $P41) merge-base(1940,1941)=$(git -C $R merge-base $P40 $P41) merge-base(dev,1940)=$(git -C $R merge-base $DEV $P40)"
git -C $R diff --name-only $MB...$P41 | sort > $L/paths_1941.txt; git -C $R diff --name-only $MB...$P40 | sort > $L/paths_1940.txt; git -C $R diff --name-only $MB $DEV | sort > $L/paths_dev_move.txt
echo "paths: 1941=$(wc -l < $L/paths_1941.txt) 1940=$(wc -l < $L/paths_1940.txt) develop-move=$(wc -l < $L/paths_dev_move.txt)"
echo "shared 1940/1941: $(comm -12 $L/paths_1940.txt $L/paths_1941.txt | tr '\n' ' ')"; echo "shared dev-move/1941: $(comm -12 $L/paths_dev_move.txt $L/paths_1941.txt | wc -l)  (control dev-move vs itself: $(comm -12 $L/paths_dev_move.txt $L/paths_dev_move.txt | wc -l))"
comm -12 $L/paths_dev_move.txt $L/paths_1941.txt
echo "## A: 1941 onto develop"; T1=$(git -C $R merge-tree --write-tree $DEV $P41); echo "rc=$? tree=$T1"
git -C $R diff-tree -r --name-only $DEV $T1 | sort > $L/mt_dev_1941.paths; diff $L/mt_dev_1941.paths $L/paths_1941.txt && echo SAME_PATHS_1941
echo "## B: 1940 onto develop"; T2=$(git -C $R merge-tree --write-tree $DEV $P40); echo "rc=$? tree=$T2"
echo "## order 1940 then 1941 (commit 1940 merge, then merge 1941)"; C1=$(git -C $R commit-tree $T2 -p $DEV -p $P40 -m 'gate123 scratch: dev+1940'); T3=$(git -C $R merge-tree --write-tree $C1 $P41); echo "rc=$? tree=$T3"
echo "## order 1941 then 1940"; C2=$(git -C $R commit-tree $T1 -p $DEV -p $P41 -m 'gate123 scratch: dev+1941'); T4=$(git -C $R merge-tree --write-tree $C2 $P40); echo "rc=$? tree=$T4"
[ "$T3" = "$T4" ] && echo "BOTH ORDERS SAME TREE $T3"
echo "## 1940 x 1941 directly"; T5=$(git -C $R merge-tree --write-tree $P40 $P41); echo "rc=$? tree=$T5"
git -C $R diff-tree -r --name-only $DEV $T3 | sort > $L/mt_union.paths; sort -u $L/paths_1940.txt $L/paths_1941.txt | diff - $L/mt_union.paths && echo UNION_PATHS_EQ_1940_PLUS_1941
for p in verification.ts verificationV2.ts; do F=Blockchain/Dev/services/originate/src/routes/$p; echo "$p union blob $(git -C $R rev-parse $T3:$F)"; done
# hunk distance in verification.ts
git -C $R diff -U0 $MB $P40 -- Blockchain/Dev/services/originate/src/routes/verification.ts | /usr/bin/grep -i '^@@' > $L/hunks_1940_v.txt; git -C $R diff -U0 $MB $P41 -- Blockchain/Dev/services/originate/src/routes/verification.ts | /usr/bin/grep -i '^@@' > $L/hunks_1941_v.txt
echo "1940 hunks:"; cat $L/hunks_1940_v.txt; echo "1941 hunks:"; cat $L/hunks_1941_v.txt
# union product diff equals 1940 diff + 1941 diff (no line touched by both)
git -C $R diff -U0 $DEV $T3 -- Blockchain/Dev/services/originate/src/routes > $L/union_product_U0.diff
git -C $R show $T3:Blockchain/Dev/services/originate/src/routes/verification.ts > $L/union_verification.ts
