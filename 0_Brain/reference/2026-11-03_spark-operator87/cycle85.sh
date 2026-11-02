#!/bin/bash
# wait up to ~150 s for a new o85/o84_p3 row in done.md; then advance and print the last rows
base=$(/usr/bin/grep -c -E 'o84_p3|o85_' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md)
i=0
while [ $i -lt 5 ]; do
  n=$(/usr/bin/grep -c -E 'o84_p3|o85_' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md)
  [ "$n" -gt "$base" ] && break
  sleep 30; i=$((i+1))
done
bash /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator85/advance85.sh
/usr/bin/grep -E 'o84_p3|o85_' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md | tail -2 | cut -c1-200
date
