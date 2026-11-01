#!/bin/bash
P=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate97-ks1868-pr1915
G="git -C $P/repo"
$G merge-tree --write-tree origin/develop pr1915 > $P/logs/merge_tree.log 2>&1; echo "RC=$?" >> $P/logs/merge_tree.log
T=$(head -1 $P/logs/merge_tree.log)
$G diff --name-only origin/develop $T > $P/logs/merge_changed.log
echo "shared paths develop-since-base vs PR:" > $P/logs/shared_paths.log
comm -12 <($G diff --name-only 03977e89a343 origin/develop | sort) <($G diff --name-only origin/develop...pr1915 | sort) >> $P/logs/shared_paths.log
echo "develop since base files: $($G diff --name-only 03977e89a343 origin/develop | wc -l)" >> $P/logs/shared_paths.log
$G diff --name-only 03977e89a343 origin/develop | /usr/bin/grep -ci 'nft-certificate' >> $P/logs/shared_paths.log
