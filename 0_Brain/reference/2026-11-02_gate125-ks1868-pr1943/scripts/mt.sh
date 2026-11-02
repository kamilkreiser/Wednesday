#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
R=$W/repo
git -C $R merge-tree --write-tree pr1943 origin/develop > $W/logs/merge_tree.log 2>&1; echo mt rc=$?; head -3 $W/logs/merge_tree.log
git -C $R diff --name-only e2a2426d221d origin/develop > $W/logs/develop_since.log; echo develop-files: $(wc -l < $W/logs/develop_since.log)
git -C $R diff --name-only e2a2426d221d pr1943 > $W/logs/pr_paths.log; cat $W/logs/pr_paths.log
echo shared: $(sort $W/logs/develop_since.log $W/logs/pr_paths.log | uniq -d | wc -l)
echo control-self: $(sort $W/logs/develop_since.log $W/logs/develop_since.log | uniq -d | wc -l)
T=$(head -1 $W/logs/merge_tree.log)
git -C $R diff --name-only origin/develop $T
