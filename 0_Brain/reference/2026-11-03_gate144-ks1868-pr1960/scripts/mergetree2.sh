#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; HEAD=5b08a162249e08c1728894c849d88f8611647b3f; NEW=4d1ab2cb6574e2b221353ac3a1de56d515711aaf
git -C $R fetch -q origin develop
{
echo "develop moved 0bd5e7bf -> $(git -C $R rev-parse origin/develop)"; git -C $R log --oneline 0bd5e7bf..$NEW
git -C $R diff --name-only 0bd5e7bf $NEW > $W/logs/develop_moved2_paths.log; echo "paths: $(wc -l < $W/logs/develop_moved2_paths.log)"; grep -c services/api-gateway/ $W/logs/develop_moved2_paths.log
echo "overlap with PR paths:"; comm -12 <(sort $W/logs/develop_moved2_paths.log) <(sort $W/logs/pr_paths.log) | wc -l
T=$(git -C $R merge-tree --write-tree $NEW $HEAD); echo "merge-tree rc=$? tree=$T"
git -C $R diff --name-only $NEW $T > $W/logs/merged2_vs_develop.log
diff <(sort $W/logs/merged2_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths"
} > $W/logs/merge_tree2.log 2>&1; cat $W/logs/merge_tree2.log
