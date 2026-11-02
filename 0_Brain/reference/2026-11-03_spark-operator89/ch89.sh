#!/bin/bash
# ch89.sh <pN> <LABEL>: checker verdict lines + byte-compare, then hold in the same action (only if a PASS (7/7) row exists)
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator89
k=$1
bash $O/chk89.sh $k > $O/chk_$k.out 2>&1; cat $O/chk_$k.out | cut -c1-170 | /usr/bin/grep -E 'run=|golden|FAIL|SUMMARY|suite'
if /usr/bin/grep -q 'rc=0 (0 = byte-identical)' $O/chk_$k.out; then bash $O/hold89.sh $k KS-1868 "$2" > $O/hold_$k.log 2>&1; cat $O/hold_$k.log | cut -c1-330; else echo "NOT HELD: patch differs from golden or no row"; fi
