#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate157-ks1868-pr1974
for a in "base pool null test" "head pool null test" "base hookRealRecovery revokedProxy production" "base hookRecovery revokedProxy production" "base hookBoot revokedProxy production" "head hookRealBoot bigintMessage production"; do
  node $W/harness/cell.js $a > $W/logs/smoke.out 2>&1; rc=$?
  echo "== $a rc=$rc"; cut -c1-900 $W/logs/smoke.out
done
