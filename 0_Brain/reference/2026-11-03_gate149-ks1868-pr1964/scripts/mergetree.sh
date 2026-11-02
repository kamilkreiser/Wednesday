#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964
R=$W/repo; BASE=4d1ab2cb6574e2b221353ac3a1de56d515711aaf; DEV=${1:-26955bf1b828113fcfe29b6bd6e371dbe28b5360}; HD=25c437f49fbb677db09828e4f74c5ff3230ecdc4
echo "develop=$DEV"
echo "develop log since base:"; git -C $R log --oneline $BASE..$DEV
for c in $(git -C $R rev-list $BASE..$DEV); do echo "== $(git -C $R log -1 --format='%h %s' $c | cut -c1-110)"; echo "   paths:"; git -C $R diff-tree --no-commit-id -r --name-only $c | sed 's/^/     /'; done
git -C $R diff --name-only $BASE $DEV > $W/logs/develop_moved_paths.log
git -C $R diff --name-only $BASE...$HD > $W/logs/pr_paths.log
echo "== PR paths vs squash paths overlap: $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log) | wc -l)"; comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log)
echo "positive control (develop paths vs develop paths): $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/develop_moved_paths.log) | wc -l)"
echo "== merge-tree:"; T=$(git -C $R merge-tree --write-tree $DEV $HD); echo "rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop.log
diff <(sort $W/logs/merged_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths ($(wc -l < $W/logs/pr_paths.log))"
for p in services/originate/src/routes/documents.ts; do echo "$p merged/head blob: $(git -C $R rev-parse $T:Blockchain/Dev/$p) $(git -C $R rev-parse $HD:Blockchain/Dev/$p)"; done
echo "== does the PR's product import any develop-changed module? documents.ts imports of errorTracking / lifecyclePayloadCodec:"
git -C $R grep -n -i "errorTrackingService\|lifecyclePayloadCodec" $HD -- Blockchain/Dev/services/originate/src/routes/documents.ts Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts
