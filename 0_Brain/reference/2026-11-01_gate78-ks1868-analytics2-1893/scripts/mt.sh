#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893
git -C $W/repo merge-tree --write-tree refs/gate/develop refs/gate/pr1893 > $W/logs/merge_tree.log 2>&1; echo "rc=$?" >> $W/logs/merge_tree.log
cat $W/logs/merge_tree.log
