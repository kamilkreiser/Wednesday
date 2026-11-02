#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925; R=$W/repo; L=$W/logs
git -C $R merge-tree --write-tree origin/develop pr1925 > $L/merge_tree.log 2>&1; echo rc=$? >> $L/merge_tree.log; cat $L/merge_tree.log
T=$(head -1 $L/merge_tree.log)
git -C $R diff-tree -r --name-only origin/develop $T | sort > $L/merge_result_paths.log; wc -l < $L/merge_result_paths.log
diff $L/merge_result_paths.log $L/pr_paths.log && echo SAME_PATHS
git -C $R rev-parse origin/develop
