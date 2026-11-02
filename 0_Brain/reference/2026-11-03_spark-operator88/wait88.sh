#!/bin/bash
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
b=$(/usr/bin/grep -c -i 'o88_' $S/spark/done.md); i=0
while [ $i -lt 11 ]; do n=$(/usr/bin/grep -c -i 'o88_' $S/spark/done.md); [ "$n" -gt "$b" ] && break; sleep 10; i=$((i+1)); done
/usr/bin/grep -i 'o88_' $S/spark/done.md | awk -F'|' '{print $2,substr($3,19,22),substr($4,1,30)}' | tail -${1:-3}; date
