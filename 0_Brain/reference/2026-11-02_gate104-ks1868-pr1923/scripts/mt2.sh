#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923; R=$W/repo; L=$W/logs/merge_tree_end.log
{
git -C $R fetch -q origin develop; echo fetch rc=$?
git -C $R rev-parse origin/develop
git -C $R merge-base --is-ancestor c0f9af13f94b94d5d4acb7a7708c6dc3b6263231 origin/develop && echo "c0f9af13 is ancestor"
git -C $R log --format='%h %s' c0f9af13f94b94d5d4acb7a7708c6dc3b6263231..origin/develop
T=$(git -C $R merge-tree --write-tree origin/develop pr1923); echo "merge-tree rc=$? tree=$T"
git -C $R diff-tree -r --name-only origin/develop $T | sort > $W/logs/merge_end_paths.log; wc -l < $W/logs/merge_end_paths.log
git -C $R diff --name-only 04ff5262ad526a13c1a0df99480b76860a8d11d1...pr1923 | sort | diff - $W/logs/merge_end_paths.log && echo SAME_PATHS
git -C $R diff --name-only 04ff5262ad526a13c1a0df99480b76860a8d11d1 origin/develop | sort > $W/logs/develop_since_base_end.log; wc -l < $W/logs/develop_since_base_end.log
comm -12 $W/logs/develop_since_base_end.log $W/logs/merge_end_paths.log | wc -l
} > $L 2>&1; cat $L
