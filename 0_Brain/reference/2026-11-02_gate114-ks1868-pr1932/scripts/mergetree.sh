#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932; R=$G/repo
DEV=$(git -C $R rev-parse origin/develop); echo "develop $DEV"
git -C $R log --oneline cd9c4a7dd3b8..$DEV | head -20
echo "develop paths past base:"; git -C $R diff --name-only cd9c4a7dd3b8 $DEV > $G/logs/dev_paths.log; wc -l < $G/logs/dev_paths.log
git -C $R diff --name-only cd9c4a7dd3b8 pr/1932 > $G/logs/pr_paths.log
echo "shared paths:"; comm -12 <(sort $G/logs/dev_paths.log) <(sort $G/logs/pr_paths.log) | wc -l
echo "control (dev paths self-intersection):"; comm -12 <(sort $G/logs/dev_paths.log) <(sort $G/logs/dev_paths.log) | wc -l
echo "anchoring/originate-anchors in dev move:"; /usr/bin/grep -i -c -E "services/anchoring/|originate/src/routes/anchors" $G/logs/dev_paths.log
T=$(git -C $R merge-tree --write-tree $DEV pr/1932); echo "merge-tree rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $G/logs/mt_paths.log; diff <(sort $G/logs/mt_paths.log) <(sort $G/logs/pr_paths.log) && echo SAME_PATHS
git -C $R diff --shortstat $DEV $T
for f in Blockchain/Dev/services/anchoring/src/index.ts Blockchain/Dev/services/originate/src/routes/anchors.ts; do [ "$(git -C $R rev-parse $T:$f)" = "$(git -C $R rev-parse pr/1932:$f)" ] && echo "merged blob == PR blob $f"; done
