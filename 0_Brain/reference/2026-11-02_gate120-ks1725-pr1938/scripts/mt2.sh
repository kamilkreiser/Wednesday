#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
R=$W/repo; L=$W/logs
git -C $R merge-tree --write-tree --name-only pr1938 777643aa6e1a29ebe121e4809fb3b16eedf5e552 > $L/merge_tree_777.log 2>&1; echo "rc=$?" >> $L/merge_tree_777.log
T=$(sed -n 1p $L/merge_tree_777.log)
git -C $R diff --name-only 777643aa6e1a29ebe121e4809fb3b16eedf5e552 $T | sort > $L/mt777_paths.txt
diff $L/mt777_paths.txt $L/pr_paths.txt >/dev/null && echo PATHS_EQUAL >> $L/merge_tree_777.log || echo PATHS_DIFFER >> $L/merge_tree_777.log
git -C $R diff --name-only 8f313815f415 777643aa6e1a29ebe121e4809fb3b16eedf5e552 | sort | comm -12 - $L/pr_paths.txt | wc -l >> $L/merge_tree_777.log
