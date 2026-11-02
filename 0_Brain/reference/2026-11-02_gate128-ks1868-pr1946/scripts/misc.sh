#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
R=$W/repo
git -C $R grep -nwE "startRetentionScheduler|stopRetentionScheduler|retentionScheduler" pr1946 -- . ':!*.html' ':!*.md' | cut -c1-220 > $W/logs/callers.log; cat $W/logs/callers.log
git -C $R merge-tree --write-tree --name-only pr1946 origin/develop > $W/logs/merge_tree.log 2>&1; echo mt_rc=$?; head -8 $W/logs/merge_tree.log
git -C $R diff --name-only e2a2426d221d origin/develop > $W/logs/dev_files.log; git -C $R diff --name-only e2a2426d221d pr1946 > $W/logs/pr_files.log
echo shared=$(comm -12 <(sort $W/logs/dev_files.log) <(sort $W/logs/pr_files.log)|wc -l) devfiles=$(wc -l <$W/logs/dev_files.log)
git -C $R ls-remote origin refs/heads/develop refs/pull/1946/head
