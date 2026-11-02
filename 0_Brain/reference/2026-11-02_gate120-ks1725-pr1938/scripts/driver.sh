#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
D=$W/repo/Blockchain/Dev; cd $D
for pair in "8f313815f415 base" "pr1938 head"; do
  set -- $pair
  bash $W/scripts/co.sh $1 > /dev/null
  $D/node_modules/.bin/tsx $D/_g120_driver.ts > $W/logs/driver_$2.json 2> $W/logs/driver_$2.err; echo "$2 rc=$?" >> $W/logs/driver_sum.txt
done
cmp $W/logs/driver_base.json $W/logs/driver_head.json && echo BYTE_IDENTICAL >> $W/logs/driver_sum.txt
