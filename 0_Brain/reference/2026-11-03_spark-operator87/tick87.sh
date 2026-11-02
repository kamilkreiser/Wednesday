#!/bin/bash
N=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator87; D=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md
b=$(/usr/bin/grep -c -E 'o8[67]_' $D); i=0
while [ $i -lt 24 ]; do n=$(/usr/bin/grep -c -E 'o8[67]_' $D); [ "$n" -gt "$b" ] && break; sleep 5; i=$((i+1)); done
bash $N/advance87.sh | /usr/bin/grep -- '->'
/usr/bin/grep -E 'o8[67]_' $D | awk -F'|' '{print $2 substr($3,1,3) substr($3,26,30) substr($4,1,45)}' | tail -4
date
