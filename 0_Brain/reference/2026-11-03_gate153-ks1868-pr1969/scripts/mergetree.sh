#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969
R=$W/repo; DEV=$1; HD=15c17034b256d52ac54194912ec560a2d75f1cad; B=26955bf1b828113fcfe29b6bd6e371dbe28b5360
echo "develop=$DEV"; git -C $R log --oneline $B..$DEV
git -C $R diff --name-only $B $DEV > $W/logs/develop_moved_paths_${DEV:0:8}.log
git -C $R diff --name-only $B...$HD > $W/logs/pr_paths.log
echo "== PR paths vs develop-moved paths overlap: $(comm -12 <(sort $W/logs/develop_moved_paths_${DEV:0:8}.log) <(sort $W/logs/pr_paths.log) | wc -l)"
echo "positive control (develop paths vs itself): $(comm -12 <(sort $W/logs/develop_moved_paths_${DEV:0:8}.log) <(sort $W/logs/develop_moved_paths_${DEV:0:8}.log) | wc -l)"
echo "== develop-moved paths under services/referral:"; grep "services/referral" $W/logs/develop_moved_paths_${DEV:0:8}.log
echo "== develop-moved paths under packages/shared: $(grep -c 'packages/shared' $W/logs/develop_moved_paths_${DEV:0:8}.log)"
echo "== merge-tree:"; T=$(git -C $R merge-tree --write-tree $DEV $HD); echo "rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop_${DEV:0:8}.log
diff <(sort $W/logs/merged_vs_develop_${DEV:0:8}.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths ($(wc -l < $W/logs/pr_paths.log))"
for p in db.ts services/milestoneService.ts services/referralService.ts services/fraudDetection.ts; do q=Blockchain/Dev/services/referral/src/$p; echo "$p merged/head blob: $(git -C $R rev-parse $T:$q) $(git -C $R rev-parse $HD:$q)"; done
echo $T > $W/logs/merged_tree_id_${DEV:0:8}.log
