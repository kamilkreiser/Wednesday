#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941; R=$W/repo; L=$W/logs
git -C $R fetch -q origin develop 2>$L/fetch_dev2.err; ND=$(git -C $R rev-parse origin/develop)
echo "develop now $ND"; echo "base e2a2426d ancestor of new develop: $(git -C $R merge-base --is-ancestor e2a2426d221d $ND && echo yes)"
git -C $R log --oneline 0e3a9b65cdd6..$ND | head
git -C $R diff --name-only 0e3a9b65cdd6 $ND | sort > $L/paths_dev_move2.txt; echo "move2 paths $(wc -l < $L/paths_dev_move2.txt); shared with 1941: $(comm -12 $L/paths_dev_move2.txt $L/paths_1941.txt | wc -l); shared with 1940: $(comm -12 $L/paths_dev_move2.txt $L/paths_1940.txt | wc -l)"
T=$(git -C $R merge-tree --write-tree $ND pr1941); echo "1941 onto new develop rc=$? tree=$T"; git -C $R diff-tree -r --name-only $ND $T | sort | diff - $L/paths_1941.txt && echo SAME_PATHS_1941
T2=$(git -C $R merge-tree --write-tree $ND pr1940); echo "1940 onto new develop rc=$? tree=$T2"
C=$(git -C $R commit-tree $T2 -p $ND -p pr1940 -m scratch); T3=$(git -C $R merge-tree --write-tree $C pr1941); echo "union (1940 then 1941) rc=$? $T3"
C2=$(git -C $R commit-tree $T -p $ND -p pr1941 -m scratch); T4=$(git -C $R merge-tree --write-tree $C2 pr1940); echo "union (1941 then 1940) rc=$? $T4"; [ "$T3" = "$T4" ] && echo BOTH_ORDERS_SAME
git -C $R ls-remote origin refs/pull/1941/head
