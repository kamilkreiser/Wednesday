#!/bin/bash
# Real-process probe matrix on two worktrees (wt/base = 26955bf1, wt/head = pr1969). No product swap in the clone.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g153
KINDS="ordinary string revokedProxy throwingGetter"
for v in base head; do
  for sc in apply award_none award_fresh; do nice -n 5 node $W/scripts/driver.cjs $v $W/wt/$v $sc none > /dev/null 2>&1; done
  nice -n 5 node $W/scripts/driver.cjs $v $W/wt/$v award_fresh none absent > /dev/null 2>&1
  for sc in boot_refverify boot_msverify boot_fraudload award_read award_read_wfail gen_owner gen_all rewards_read; do
    for k in $KINDS; do nice -n 5 node $W/scripts/driver.cjs $v $W/wt/$v $sc $k > /dev/null 2>&1; done
  done
  for k in ordinary revokedProxy; do nice -n 5 node $W/scripts/driver.cjs $v $W/wt/$v award_read $k absent > /dev/null 2>&1; done
done
date > $W/logs/probes.done
