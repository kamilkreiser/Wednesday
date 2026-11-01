#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899; R=$W/repo
git -C $R checkout -q refs/gate/pr1899 > $W/logs/checkout.log 2>&1; echo rc=$?
git -C $R diff --stat refs/gate/pr1899^ refs/gate/pr1899 > $W/logs/diffstat.log 2>&1; cat $W/logs/diffstat.log
git -C $R log --oneline -3 refs/gate/pr1899; git -C $R merge-base refs/gate/pr1899 refs/gate/develop; git -C $R rev-parse refs/gate/pr1899^
git -C $R diff refs/gate/pr1899^ refs/gate/pr1899 > $W/logs/pr.diff 2>&1; wc -l $W/logs/pr.diff
