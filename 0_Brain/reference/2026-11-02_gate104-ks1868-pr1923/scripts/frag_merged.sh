#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923; WT=$W/apply_wt
T=$(head -1 $W/logs/merge_tree.log)
git -C $WT read-tree -u --reset $T && git -C $WT write-tree
(cd $WT && node Blockchain/Dev/scripts/docs-fragments.mjs check > $W/logs/frag_merged.log 2>&1; echo rc=$? >> $W/logs/frag_merged.log); tail -3 $W/logs/frag_merged.log
