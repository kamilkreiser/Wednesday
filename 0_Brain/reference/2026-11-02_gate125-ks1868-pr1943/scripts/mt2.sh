#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
R=$W/repo
git -C $R fetch origin develop > $W/logs/fetch2.log 2>&1; echo fetch rc=$?
git -C $R rev-parse origin/develop
git -C $R merge-tree --write-tree pr1943 origin/develop > $W/logs/merge_tree_new.log 2>&1; echo mt rc=$?
T=$(head -1 $W/logs/merge_tree_new.log); echo tree $T
git -C $R diff --name-only origin/develop $T
git -C $R diff --name-only e2a2426d221d origin/develop > $W/logs/develop_since_new.log; echo develop files $(wc -l < $W/logs/develop_since_new.log)
echo shared $(sort $W/logs/develop_since_new.log $W/logs/pr_paths.log | uniq -d | wc -l)
git -C $R rev-list --count 3e688ee239f2..origin/develop
