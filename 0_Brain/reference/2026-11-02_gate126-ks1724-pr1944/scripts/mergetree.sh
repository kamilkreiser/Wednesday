#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
R=$W/repo; L=$W/logs
git -C $R fetch -q origin refs/pull/1938/head:refs/gate/pr1938 refs/heads/develop:refs/gate/develop
git -C $R log -3 --format='%h ad=%aI cd=%cI %s' refs/gate/pr1944
git -C $R log -1 --format='%h ad=%aI cd=%cI %s' refs/gate/pr1938
echo "develop now $(git -C $R rev-parse refs/gate/develop)"
echo '---- merge-tree onto develop'
git -C $R merge-tree --write-tree --name-only refs/gate/develop refs/gate/pr1944 > $L/merge_tree_develop.log 2>&1; echo rc=$? >> $L/merge_tree_develop.log; cat $L/merge_tree_develop.log
T=$(head -1 $L/merge_tree_develop.log)
git -C $R diff --name-only refs/gate/develop $T | sort > $L/merged_vs_develop_paths.log
git -C $R diff --name-only c70f339063ee refs/gate/pr1944 | sort > $L/pr_paths.log
echo "merged-vs-develop paths == PR paths: $(cmp -s $L/merged_vs_develop_paths.log $L/pr_paths.log && echo EQUAL || echo DIFFERENT) ($(wc -l < $L/merged_vs_develop_paths.log) vs $(wc -l < $L/pr_paths.log))"
echo '---- merge-tree with 1938'
git -C $R merge-tree --write-tree --name-only refs/gate/pr1938 refs/gate/pr1944 > $L/merge_tree_1938.log 2>&1; echo rc=$? >> $L/merge_tree_1938.log; head -2 $L/merge_tree_1938.log; tail -1 $L/merge_tree_1938.log
echo '---- develop since mb'
git -C $R log --oneline c70f339063ee..refs/gate/develop
git -C $R diff --name-only c70f339063ee refs/gate/develop | sort > $L/develop_moved_paths.log
echo "develop moved paths: $(wc -l < $L/develop_moved_paths.log); shared with PR: $(comm -12 $L/develop_moved_paths.log $L/pr_paths.log | wc -l)"
comm -12 $L/develop_moved_paths.log $L/pr_paths.log
