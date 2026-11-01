#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899
{ git -C $W/repo merge-tree --write-tree refs/gate/develop refs/gate/pr1899; echo "rc=$?"; } > $W/logs/merge_tree.log 2>&1
cat $W/logs/merge_tree.log
git -C $W/repo diff --name-only d7691f35312ea158f043e87a3227e477cccb183d refs/gate/develop > $W/logs/develop_since_d7691f35_files.log 2>&1
git -C $W/repo log --oneline d7691f35312ea158f043e87a3227e477cccb183d..refs/gate/develop > $W/logs/develop_since_d7691f35_log.log 2>&1
git -C $W/repo diff --name-only refs/gate/pr1899^ refs/gate/pr1899 > $W/logs/pr_files.log
echo "overlap (PR files vs develop-since files):"; comm -12 <(sort $W/logs/pr_files.log) <(sort $W/logs/develop_since_d7691f35_files.log) | tee $W/logs/overlap.log; echo "(end overlap)"
wc -l $W/logs/develop_since_d7691f35_files.log; cat $W/logs/develop_since_d7691f35_log.log
