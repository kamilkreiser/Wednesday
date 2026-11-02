#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954; R=$W/repo
git -C $R diff --name-only origin/develop...pr1954 | sort > $W/logs/pr_paths.txt
for n in 1951 1952 1953; do git -C $R diff --name-only origin/develop...pr$n | sort > $W/logs/paths_$n.txt; echo "PR$n files: $(wc -l < $W/logs/paths_$n.txt) shared-with-1954: $(comm -12 $W/logs/pr_paths.txt $W/logs/paths_$n.txt | wc -l)"; done
git -C $R merge-tree --write-tree origin/develop pr1954 > $W/logs/mergetree.log 2>&1; echo mt rc=$?; head -3 $W/logs/mergetree.log
T=$(head -1 $W/logs/mergetree.log); git -C $R diff-tree -r --name-only origin/develop $T | sort > $W/logs/mt_changed.txt; wc -l < $W/logs/mt_changed.txt; diff $W/logs/mt_changed.txt $W/logs/pr_paths.txt && echo SAME_PATHS
git -C $R diff --name-only 9a9bf86967e3 origin/develop | sort > $W/logs/dev_moved.txt; echo "dev moved: $(wc -l < $W/logs/dev_moved.txt) shared with PR: $(comm -12 $W/logs/dev_moved.txt $W/logs/pr_paths.txt | wc -l)"
