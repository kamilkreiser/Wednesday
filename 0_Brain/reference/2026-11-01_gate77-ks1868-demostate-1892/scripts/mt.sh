#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892; L=$W/logs; R=$W/repo
git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1892 > $L/merge_tree.log 2>&1; echo rc=$?
