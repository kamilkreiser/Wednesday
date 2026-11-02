#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate147-ks1868-pr1963
R=$W/repo; DEV=${1:-2f9f7db313b3423bfe3199bed076e992d2bfe2a3}; HD=8d0e6b054c5c157cf6100104cb630836f4210ae5; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf
echo "develop=$DEV"; git -C $R log --oneline $MB..$DEV
for c in $(git -C $R rev-list $MB..$DEV); do echo "== $(git -C $R log -1 --format='%h %s' $c | cut -c1-110)"; git -C $R diff-tree --no-commit-id -r --name-only $c | sed 's/^/     /'; done
git -C $R diff --name-only $MB $DEV > $W/logs/develop_moved_paths.log
git -C $R diff --name-only $MB...$HD > $W/logs/pr_paths.log
echo "== PR paths vs develop-moved paths overlap: $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log) | wc -l)"
echo "== does develop's move touch kyc / wallet-connector / packages/shared events? $(grep -c 'services/kyc/\|services/wallet-connector/\|packages/shared/src/events' $W/logs/develop_moved_paths.log)"
echo "== merge-tree:"; T=$(git -C $R merge-tree --write-tree $DEV $HD); echo "rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop.log
diff <(sort $W/logs/merged_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths ($(wc -l < $W/logs/pr_paths.log))"
for p in services/kyc/src/userErasedSubscriber.ts services/wallet-connector/src/userErasedSubscriber.ts; do echo "$p merged/head blob: $(git -C $R rev-parse $T:Blockchain/Dev/$p) $(git -C $R rev-parse $HD:Blockchain/Dev/$p)"; done
