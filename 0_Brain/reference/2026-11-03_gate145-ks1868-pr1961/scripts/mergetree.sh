#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate145-ks1868-pr1961
R=$W/repo; DEV=${1:-4d1ab2cb6574e2b221353ac3a1de56d515711aaf}; HD=e5e0be51f21d76a10d6d2ceb9f94394b76d60df2
echo "develop=$DEV"
echo "develop log since base:"; git -C $R log --oneline 2d3b3bb3..$DEV
for c in $(git -C $R rev-list 2d3b3bb3..$DEV); do echo "== $(git -C $R log -1 --format='%h %s' $c | cut -c1-110)"; echo "   originate / lock paths:"; git -C $R diff-tree --no-commit-id -r --name-only $c | grep -i "services/originate\|KS-1868-originate\|package-lock" | sed 's/^/     /'; echo "   total paths: $(git -C $R diff-tree --no-commit-id -r --name-only $c | wc -l)"; done
git -C $R diff --name-only 2d3b3bb3 $DEV > $W/logs/develop_moved_paths.log
git -C $R diff --name-only 2d3b3bb3...$HD > $W/logs/pr_paths.log
echo "== PR paths vs squash paths overlap: $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log) | wc -l)"; comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log)
echo "== merge-tree:"; T=$(git -C $R merge-tree --write-tree $DEV $HD); echo "rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop.log
diff <(sort $W/logs/merged_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths"
for p in services/originate/src/services/errorTrackingService.ts services/originate/src/utils/lifecyclePayloadCodec.ts; do echo "$p merged/head blob: $(git -C $R rev-parse $T:Blockchain/Dev/$p) $(git -C $R rev-parse $HD:Blockchain/Dev/$p)"; done
echo "== originate package files diff base..develop:"; git -C $R diff 2d3b3bb3 $DEV -- Blockchain/Dev/services/originate/package.json Blockchain/Dev/services/originate/package-lock.json | grep -E '^[-+]' | grep -v '^[-+][-+]' | head -30
echo "== zod in the PR product files and the modules they import:"; git -C $R grep -n -i "zod" $HD -- Blockchain/Dev/services/originate/src/services/errorTrackingService.ts Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts Blockchain/Dev/services/originate/src/utils/logger.ts Blockchain/Dev/services/originate/src/utils/erasureMarker.ts Blockchain/Dev/services/originate/src/__tests__/ks1868-*; echo "zod grep rc=$? (1 = no hit)"
echo "positive control (zod named somewhere in originate src): $(git -C $R grep -l -i zod $HD -- Blockchain/Dev/services/originate/src | wc -l) files"
