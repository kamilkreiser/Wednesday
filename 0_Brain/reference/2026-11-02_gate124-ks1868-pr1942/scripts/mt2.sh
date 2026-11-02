#!/bin/bash
# gate 124: develop moved during the gate (58b5042c -> fbacb63a); fetch and re-run merge-tree + shared-path checks + union
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; R=$W/repo; L=$W/logs
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350; OLD=58b5042ccdb5a06a213ba53f5d4f7644f5f52549
git -C $R fetch -q origin develop
echo "develop $(git -C $R rev-parse origin/develop)"
git -C $R log --format='%h %s' $OLD..origin/develop
git -C $R diff --name-only $OLD origin/develop | sort > $L/dev_moved2_paths.txt
echo "paths moved $OLD..develop: $(wc -l < $L/dev_moved2_paths.txt | tr -d ' '), shared with PR 1942: $(comm -12 $L/pr_paths.txt $L/dev_moved2_paths.txt | wc -l | tr -d ' ')"
sed 's/^/   /' $L/dev_moved2_paths.txt
T=$(git -C $R merge-tree --write-tree origin/develop pr1942); echo "merge-tree 1942 onto develop rc=$? tree=$T"
git -C $R diff --name-only origin/develop $T | sort > $L/mt2_paths.txt
cmp -s $L/pr_paths.txt $L/mt2_paths.txt && echo SAME_PATHS || echo PATHS_DIFFER
C1=$(git -C $R commit-tree $(git -C $R merge-tree --write-tree origin/develop pr1940) -p origin/develop -p pr1940 -m u1)
C2=$(git -C $R commit-tree $(git -C $R merge-tree --write-tree $C1 pr1941) -p $C1 -p pr1941 -m u2)
U=$(git -C $R merge-tree --write-tree $C2 pr1942); echo "union develop+1940+1941+1942 rc=$? tree=$U"
D1=$(git -C $R commit-tree $T -p origin/develop -p pr1942 -m v1)
D2=$(git -C $R commit-tree $(git -C $R merge-tree --write-tree $D1 pr1941) -p $D1 -p pr1941 -m v2)
U2=$(git -C $R merge-tree --write-tree $D2 pr1940); echo "union develop+1942+1941+1940 rc=$? tree=$U2"
[ "$U" = "$U2" ] && echo UNION_ORDERS_EQUAL || echo UNION_ORDERS_DIFFER
git -C $R ls-remote origin refs/pull/1942/head refs/heads/develop
