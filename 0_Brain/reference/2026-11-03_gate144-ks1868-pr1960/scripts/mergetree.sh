#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; DEV=0bd5e7bf62ac81e15450dd712e0427c4cede918c; HEAD=5b08a162249e08c1728894c849d88f8611647b3f
{
echo "develop log since base:"; git -C $R log --oneline 2d3b3bb3..$DEV
for c in $(git -C $R rev-list 2d3b3bb3..$DEV); do echo "== $c paths touching api-gateway or PR paths:"; git -C $R diff-tree --no-commit-id -r --name-only $c | grep -E "services/api-gateway|KS-1868-gateway-redis" ; echo "(api-gateway count: $(git -C $R diff-tree --no-commit-id -r --name-only $c | grep -c services/api-gateway/))"; done
echo "== PR paths vs squash paths overlap:"
git -C $R diff --name-only 2d3b3bb3 $DEV > $W/logs/develop_moved_paths.log
git -C $R diff --name-only 2d3b3bb3...$HEAD > $W/logs/pr_paths.log
comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log); echo "overlap count: $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log) | wc -l)"
echo "== merge-tree:"; T=$(git -C $R merge-tree --write-tree $DEV $HEAD); echo "rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop.log
diff <(sort $W/logs/merged_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths"
echo "== redis.ts in merged tree equals head blob:"; git -C $R rev-parse $T:Blockchain/Dev/services/api-gateway/src/services/redis.ts $HEAD:Blockchain/Dev/services/api-gateway/src/services/redis.ts
echo "== api-gateway package.json / lock changes in develop since base:"; git -C $R diff --stat 2d3b3bb3 $DEV -- Blockchain/Dev/services/api-gateway/package.json Blockchain/Dev/package-lock.json | tail -3
} > $W/logs/merge_tree.log 2>&1
cat $W/logs/merge_tree.log
