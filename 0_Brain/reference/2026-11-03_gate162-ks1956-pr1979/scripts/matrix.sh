#!/bin/bash
# Gate 162 matrix: every cell, base and head, serially, against the g162-pg container.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979
export G162_PGPORT=$(docker port g162-pg 5432 | sed 's/.*://')
L=$W/logs/matrix.log; : > $L
run() { for v in base head; do nice -n 5 node $W/scripts/g162.cjs $v "$1" "$2" >> $L 2>&1; done; }
for c in consecutive concurrent2proc concurrent1proc concurrentNatural legacy progressReadFails awardedReadFails connectionsRefused readFailsBetween progressSaveFails rewardSaveFails qualifyPath ambassador amounts; do run $c pk; done
for m in nouniq absent; do for c in consecutive concurrent2proc qualifyPath amounts; do run $c $m; done; done
echo DONE >> $L
