#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962
R=$W/repo; DEV=${1:-4d1ab2cb6574e2b221353ac3a1de56d515711aaf}; HD=dba0813c64d00a002c89660a74988754cdbcc40c; B=cc33e702bfd5aa89e11d1b584cc49fd87c854b83
echo "develop=$DEV"; git -C $R log --oneline $B..$DEV
git -C $R diff --name-only $B $DEV > $W/logs/develop_moved_paths.log
git -C $R diff --name-only $B...$HD > $W/logs/pr_paths.log
echo "== PR paths vs squash paths overlap: $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/pr_paths.log) | wc -l)"
echo "positive control (develop paths vs itself): $(comm -12 <(sort $W/logs/develop_moved_paths.log) <(sort $W/logs/develop_moved_paths.log) | wc -l)"
echo "== squash paths under services/transfer:"; grep "services/transfer" $W/logs/develop_moved_paths.log
echo "== merge-tree:"; T=$(git -C $R merge-tree --write-tree $DEV $HD); echo "rc=$? tree=$T"
git -C $R diff --name-only $DEV $T > $W/logs/merged_vs_develop.log
diff <(sort $W/logs/merged_vs_develop.log) <(sort $W/logs/pr_paths.log) && echo "merged-vs-develop paths == PR paths"
p=Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts; echo "product merged/head blob: $(git -C $R rev-parse $T:$p) $(git -C $R rev-parse $HD:$p)"
p=Blockchain/Dev/services/transfer/src/db.ts; echo "db.ts merged/develop/head(base) blob: $(git -C $R rev-parse $T:$p) $(git -C $R rev-parse $DEV:$p) $(git -C $R rev-parse $HD:$p)"
echo "== does the product import db.ts symbols changed by 1957? product imports:"; git -C $R grep -n "from '../db'" $HD -- Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
echo "1957 db.ts hunks touch functions:"; git -C $R diff $B $DEV -- Blockchain/Dev/services/transfer/src/db.ts | grep '^@@'
echo $T > $W/logs/merged_tree_id.log
