#!/bin/bash
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949
A=$G/repo/Blockchain/Dev/services/auth/src/__tests__
RAISE="--hookTimeout=60000 --testTimeout=30000"
date -u > $G/logs/suites_times.log
$G/scripts/vt.sh $G/logs/suite_head_default.log; echo "head default rc=$? $(date -u +%T)" >> $G/logs/suites_times.log
$G/scripts/vt.sh $G/logs/suite_head_raised.log $RAISE; echo "head raised rc=$? $(date -u +%T)" >> $G/logs/suites_times.log
# base: base product, the 4 new test files moved out
mkdir -p $G/logs/_hold_newtests
for f in $A/ks1868-*-message-coercion-unreadable-throw.test.ts; do mv "$f" $G/logs/_hold_newtests/; done
$G/scripts/swap.sh base > $G/logs/suite_base_swap.log
$G/scripts/vt.sh $G/logs/suite_base_raised.log $RAISE; echo "base raised rc=$? $(date -u +%T)" >> $G/logs/suites_times.log
$G/scripts/vt.sh $G/logs/suite_base_default.log; echo "base default rc=$? $(date -u +%T)" >> $G/logs/suites_times.log
$G/scripts/swap.sh head > $G/logs/suite_restore.log
for f in $G/logs/_hold_newtests/*.test.ts; do mv "$f" $A/; done
git -C $G/repo status --short >> $G/logs/suite_restore.log
echo ALLDONE >> $G/logs/suites_times.log
