#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator45; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
for k in p1 p2 p3 p4; do
  d=$(ls -d $B/ks_1868_o45_${k}_*)
  python3 $S/spark/brief_lint.py $d >$O/lint3_$k.out 2>$O/lint3_$k.err; echo "$k lint rc=$?" >> $O/rounds3.log
  nice -n 10 bash $S/spark/round.sh $d --dry-run >$O/dry3_$k.out 2>$O/dry3_$k.err; rc=$?; echo "$k dry rc=$rc" >> $O/rounds3.log; [ $rc -ne 0 ] && continue
  nice -n 10 bash $S/spark/round.sh $d --control >$O/ctl3_$k.out 2>$O/ctl3_$k.err; rc=$?; echo "$k control rc=$rc" >> $O/rounds3.log; [ $rc -ne 0 ] && continue
  nice -n 10 bash $S/spark/round.sh $d --dry-run >$O/pre3_$k.out 2>$O/pre3_$k.err; rc=$?; echo "$k predry rc=$rc" >> $O/rounds3.log; [ $rc -ne 0 ] && continue
  nice -n 10 bash $S/spark/round.sh $d >$O/rnd3_$k.out 2>$O/rnd3_$k.err; echo "$k round rc=$?" >> $O/rounds3.log
done
echo ALLDONE >> $O/rounds3.log
