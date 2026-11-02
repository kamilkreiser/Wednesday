#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate105-ks1868-pr1924; R=$W/repo
git -C $R merge-tree --write-tree origin/develop pr1924 > $W/logs/merge_tree.log 2>&1; echo rc=$? >> $W/logs/merge_tree.log; cat $W/logs/merge_tree.log
T=$(head -1 $W/logs/merge_tree.log)
git -C $R diff-tree -r --name-only origin/develop $T > $W/logs/merge_result_paths.log; wc -l < $W/logs/merge_result_paths.log
git -C $R diff --name-only origin/develop...pr1924 | sort > $W/logs/pr_paths.log; sort $W/logs/merge_result_paths.log | diff - $W/logs/pr_paths.log && echo SAME_PATHS
git -C $R diff --name-only $(git -C $R merge-base origin/develop pr1924) origin/develop | sort > $W/logs/develop_since_base.log; wc -l < $W/logs/develop_since_base.log; comm -12 $W/logs/develop_since_base.log $W/logs/pr_paths.log | wc -l
git -C $R log --format='%H %an <%ae> %s' -1 pr1924
