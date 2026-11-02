#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
R=$W/repo; L=$W/logs
git -C $R fetch -q origin develop
DEV=$(git -C $R rev-parse origin/develop); echo "develop=$DEV" > $L/merge_tree.log
git -C $R merge-tree --write-tree --name-only pr1938 origin/develop >> $L/merge_tree.log 2>&1; echo "rc=$?" >> $L/merge_tree.log
T=$(sed -n 2p $L/merge_tree.log)
git -C $R diff --name-only origin/develop $T | sort > $L/mt_paths.txt
git -C $R diff --name-only 8f313815f415 pr1938 | sort > $L/pr_paths.txt
diff $L/mt_paths.txt $L/pr_paths.txt > /dev/null && echo PATHS_EQUAL >> $L/merge_tree.log || echo PATHS_DIFFER >> $L/merge_tree.log
echo "pr_paths_also_changed_on_develop_since_base: $(git -C $R diff --name-only 8f313815f415 origin/develop | sort | comm -12 - $L/pr_paths.txt | wc -l)" >> $L/merge_tree.log
echo "pr_paths=$(wc -l < $L/pr_paths.txt) mt_paths=$(wc -l < $L/mt_paths.txt)" >> $L/merge_tree.log
