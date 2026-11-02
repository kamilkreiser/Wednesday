#!/bin/bash
N=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator86; D=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md
b=$(/usr/bin/grep -c o86_ $D); i=0
while [ $i -lt 20 ]; do n=$(/usr/bin/grep -c o86_ $D); [ "$n" -gt "$b" ] && break; sleep 5; i=$((i+1)); done
bash $N/advance86.sh | /usr/bin/grep -- '->'
/usr/bin/grep -i o86_ $D | awk -F'|' '{print $2 substr($3,28,30) substr($4,1,45)}' | tail -4
date
