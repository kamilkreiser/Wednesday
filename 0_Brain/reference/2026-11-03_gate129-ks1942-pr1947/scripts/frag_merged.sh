#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947; R=$G/repo; T=$(cat $G/logs/merged_tree_id.txt); M=$G/merged
[ -e $M ] && { echo "merged dir exists"; exit 1; }
mkdir -p $M
git -C $R archive $T "Projects Documents" Blockchain/Dev/scripts | tar -x -C $M; echo "archive rc=$?"
nice -n 10 node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $M > $G/logs/frag_merged.log 2>&1; echo "rc=$?" >> $G/logs/frag_merged.log
tail -3 $G/logs/frag_merged.log
