#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893
R=$W/repo
{ echo "START $(date -u +%FT%TZ)"; echo "pr1893 $(git -C $R rev-parse refs/gate/pr1893)"; echo "develop $(git -C $R rev-parse refs/gate/develop)"; } | tee $W/logs/head_start.log
H=$(git -C $R rev-parse refs/gate/pr1893)
[ "$H" = 276564a771713769e86e20928356121fa8c85e84 ] || { echo HEAD MISMATCH STOP; exit 9; }
git -C $R checkout -q refs/gate/pr1893 > $W/logs/checkout.log 2>&1; echo checkout rc=$?; tail -3 $W/logs/checkout.log
git -C $R log --oneline -3 refs/gate/pr1893
git -C $R diff --stat refs/gate/develop refs/gate/pr1893 | tee $W/logs/diffstat.log
git -C $R merge-base refs/gate/develop refs/gate/pr1893
git -C $R rev-parse refs/gate/pr1893^
