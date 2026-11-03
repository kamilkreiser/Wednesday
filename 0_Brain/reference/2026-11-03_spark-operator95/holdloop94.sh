#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator95; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
echo started $(date) pid $$ >> $O/holdloop95.log
i=0
while [ $i -lt 400 ] && [ ! -e $O/STOP ]; do
 while read k lab; do
  [ -z "$k" ] && continue
  [ -e $O/hold_$k.log ] && continue
  n=$(/usr/bin/grep "o95_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep -c "PASS (7/7)")
  if [ "$n" -ge 1 ]; then bash $O/ch95.sh $k "$lab" > $O/ch_$k.out 2>&1; echo "$(date +%T) $k held-attempt" >> $O/holdloop95.log; fi
 done < $O/labels95.txt
 sleep 20; i=$((i+1))
done
echo exited $(date) >> $O/holdloop95.log
