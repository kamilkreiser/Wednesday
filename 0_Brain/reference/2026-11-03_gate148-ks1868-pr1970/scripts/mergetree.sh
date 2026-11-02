#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; HEAD=b078c7f49095e60c91324dc914b3cc3a6d20cba4; DEV=ddd770cab4aa922f5a49376b8bbe5232a94939f7; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf
{
echo "develop moved $MB -> $DEV"; git -C $R log --oneline $MB..$DEV
git -C $R diff --name-only $MB $DEV > $W/logs/develop_moved_paths.log; echo "paths: $(wc -l < $W/logs/develop_moved_paths.log)"; echo "api-gateway paths: $(grep -c services/api-gateway/ $W/logs/develop_moved_paths.log)"; grep services/api-gateway/ $W/logs/develop_moved_paths.log
echo "overlap with PR paths: $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log) | wc -l)"
T=$(git -C $R merge-tree --write-tree $DEV $HEAD); echo "merge-tree rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop.log
diff <(sort $W/logs/merged_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths ($(wc -l < $W/logs/pr_paths.log))"
for f in security rateLimitEnforce audit; do p=Blockchain/Dev/services/api-gateway/src/middleware/$f.ts; [ "$(git -C $R rev-parse $T:$p)" = "$(git -C $R rev-parse $HEAD:$p)" ] && echo "$f blob merged == head"; done
} > $W/logs/merge_tree.log 2>&1
