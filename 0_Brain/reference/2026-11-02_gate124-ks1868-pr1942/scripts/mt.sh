#!/bin/bash
# gate 124: merge-tree onto develop, path checks, overlap with PRs 1940/1941, union in two orders (object-only writes in OUR clone)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; R=$W/repo; L=$W/logs
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
echo "develop $(git -C $R rev-parse origin/develop)"
T=$(git -C $R merge-tree --write-tree origin/develop pr1942); echo "merge-tree 1942 onto develop rc=$? tree=$T"
git -C $R diff --name-only $MB pr1942 | sort > $L/pr_paths.txt
git -C $R diff --name-only origin/develop $T | sort > $L/mt_paths.txt
cmp -s $L/pr_paths.txt $L/mt_paths.txt && echo SAME_PATHS || echo PATHS_DIFFER
git -C $R diff --name-only $MB origin/develop | sort > $L/dev_moved_paths.txt
echo "develop moved paths since base: $(wc -l < $L/dev_moved_paths.txt | tr -d ' '), shared with PR: $(comm -12 $L/pr_paths.txt $L/dev_moved_paths.txt | wc -l | tr -d ' ') (control, develop vs itself: $(comm -12 $L/dev_moved_paths.txt $L/dev_moved_paths.txt | wc -l | tr -d ' '))"
echo "commits base..develop: $(git -C $R rev-list --count $MB..origin/develop)"
a=$(git -C $R rev-parse $MB:Blockchain/Dev/services/originate/src/routes/certifications.ts); b=$(git -C $R rev-parse origin/develop:Blockchain/Dev/services/originate/src/routes/certifications.ts)
echo "certifications.ts blob base=$a develop=$b"
for p in 1940 1941; do
  git -C $R diff --name-only $(git -C $R merge-base pr$p pr1942) pr$p | sort > $L/pr${p}_paths.txt
  echo "PR $p merge-base $(git -C $R merge-base pr$p pr1942 | cut -c1-12) paths $(wc -l < $L/pr${p}_paths.txt | tr -d ' '), shared with 1942: $(comm -12 $L/pr_paths.txt $L/pr${p}_paths.txt | wc -l | tr -d ' ')"
  sed 's/^/   /' $L/pr${p}_paths.txt
done
C1=$(git -C $R commit-tree $(git -C $R merge-tree --write-tree origin/develop pr1940) -p origin/develop -p pr1940 -m u1)
C2=$(git -C $R commit-tree $(git -C $R merge-tree --write-tree $C1 pr1941) -p $C1 -p pr1941 -m u2)
U=$(git -C $R merge-tree --write-tree $C2 pr1942); echo "union develop+1940+1941+1942 rc=$? tree=$U"
D1=$(git -C $R commit-tree $T -p origin/develop -p pr1942 -m v1)
D2=$(git -C $R commit-tree $(git -C $R merge-tree --write-tree $D1 pr1941) -p $D1 -p pr1941 -m v2)
U2=$(git -C $R merge-tree --write-tree $D2 pr1940); echo "union develop+1942+1941+1940 rc=$? tree=$U2"
[ "$U" = "$U2" ] && echo UNION_ORDERS_EQUAL || echo UNION_ORDERS_DIFFER
