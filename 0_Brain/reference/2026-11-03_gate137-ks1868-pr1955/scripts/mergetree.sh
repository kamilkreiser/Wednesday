#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955; R=$W/repo
DEV=$(git -C $R rev-parse origin/develop); echo "develop $DEV"
git -C $R log --oneline 9a9bf86967e3..$DEV
git -C $R diff --name-only 9a9bf86967e3 $DEV > $W/logs/dev_paths.log; echo "develop paths past merge-base: $(wc -l < $W/logs/dev_paths.log)"
git -C $R diff --name-only 9a9bf86967e3...pr/1955 > $W/logs/pr_paths.log
echo "shared with PR: $(comm -12 <(sort $W/logs/dev_paths.log) <(sort $W/logs/pr_paths.log) | wc -l) (control self: $(comm -12 <(sort $W/logs/dev_paths.log) <(sort $W/logs/dev_paths.log) | wc -l))"
T=$(git -C $R merge-tree --write-tree $DEV pr/1955); echo "merge-tree develop+1955 rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/mt_paths.log; diff <(sort $W/logs/mt_paths.log) <(sort $W/logs/pr_paths.log) && echo SAME_PATHS
git -C $R diff --shortstat $DEV $T
for f in Blockchain/Dev/services/anchoring/src/index.ts Blockchain/Dev/services/originate/src/routes/anchors.ts; do [ "$(git -C $R rev-parse $T:$f)" = "$(git -C $R rev-parse pr/1955:$f)" ] && echo "merged blob == PR blob $f"; done
echo "$T" > $W/logs/mt_tree_develop.txt
