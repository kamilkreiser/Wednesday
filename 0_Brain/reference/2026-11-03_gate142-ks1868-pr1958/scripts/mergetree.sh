#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958
R=$W/repo
git -C $R fetch origin develop 2>&1
DEV=$(git -C $R rev-parse origin/develop); echo develop=$DEV
git -C $R merge-tree --write-tree origin/develop pr1958; echo rc=$?
TREE=$(git -C $R merge-tree --write-tree origin/develop pr1958)
echo "--- paths differing merged vs develop"; git -C $R diff --name-only origin/develop $TREE | sort > $W/logs/merged_paths.txt; cat $W/logs/merged_paths.txt
echo "--- PR paths (three-dot)"; git -C $R diff --name-only origin/develop...pr1958 | sort > $W/logs/pr_paths.txt; diff $W/logs/merged_paths.txt $W/logs/pr_paths.txt && echo IDENTICAL
echo "--- develop commits since PR base"; git -C $R log --oneline $(git -C $R merge-base origin/develop pr1958)..origin/develop
