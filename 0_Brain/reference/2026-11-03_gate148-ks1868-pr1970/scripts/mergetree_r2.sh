#!/bin/bash
# Resumed gate 148: merge-tree onto develop 4deb2fc1 (develop moved during the gate). Read-only git verbs + merge-tree --write-tree (objects only).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; HEAD=b078c7f49095e60c91324dc914b3cc3a6d20cba4; DEV=4deb2fc10b7d852194183c08e86e2ecacb7231db; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf
date -u; echo "develop $DEV"
echo "commits $MB..$DEV: $(git -C $R rev-list --count $MB..$DEV)"
git -C $R diff --name-only $MB $DEV > $W/logs/develop_moved_paths_r2.log; echo "paths: $(wc -l < $W/logs/develop_moved_paths_r2.log)"
echo "api-gateway paths: $(grep -c services/api-gateway/ $W/logs/develop_moved_paths_r2.log)"; grep services/api-gateway/ $W/logs/develop_moved_paths_r2.log
echo "fragment paths: $(grep -cE 'fragments/(flow|cheat)/' $W/logs/develop_moved_paths_r2.log)"
echo "overlap with PR paths: $(comm -12 <(sort $W/logs/develop_moved_paths_r2.log) <(sort $W/logs/pr_paths.log) | wc -l)"
T=$(git -C $R merge-tree --write-tree $DEV $HEAD); echo "merge-tree rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop_r2.log
diff <(sort $W/logs/merged_vs_develop_r2.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths ($(wc -l < $W/logs/pr_paths.log))"
while read -r p; do [ "$(git -C $R rev-parse "$T:$p")" = "$(git -C $R rev-parse "$HEAD:$p")" ] && echo "blob merged == head: $p" || echo "BLOB DIFFERS: $p"; done < $W/logs/pr_paths.log
for f in security rateLimitEnforce audit; do p=Blockchain/Dev/services/api-gateway/src/middleware/$f.ts; [ "$(git -C $R rev-parse $MB:$p)" = "$(git -C $R rev-parse $DEV:$p)" ] && echo "$f.ts unchanged on develop since MB" || echo "$f.ts CHANGED on develop"; done
echo "positive control: merge-tree of a known-conflicting pair must exit 1"
git -C $R merge-tree --write-tree $DEV $HEAD >/dev/null; echo "(real) rc=$?"
