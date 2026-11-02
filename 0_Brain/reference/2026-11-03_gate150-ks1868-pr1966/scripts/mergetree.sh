#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate150-ks1868-pr1966; R=$W/repo
git -C $R fetch origin develop > /dev/null 2>&1
git -C $R ls-remote origin refs/heads/develop refs/pull/1966/head
git -C $R rev-parse origin/develop
git -C $R merge-tree --write-tree origin/develop pr1966 > $W/logs/merge_tree.log 2>&1; echo rc=$?; head -5 $W/logs/merge_tree.log
T=$(head -1 $W/logs/merge_tree.log); git -C $R diff --name-only origin/develop $T > $W/logs/merged_vs_develop.log; git -C $R diff --name-only 4d1ab2cb pr1966 > $W/logs/pr_paths.log; diff $W/logs/merged_vs_develop.log $W/logs/pr_paths.log && echo PATHS_EQUAL; wc -l < $W/logs/pr_paths.log; git -C $R merge-base origin/develop pr1966; git -C $R log --oneline 4d1ab2cb..origin/develop | head
