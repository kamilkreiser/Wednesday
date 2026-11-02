#!/bin/bash
# exits when the count of o84_p3|o85_ rows in done.md exceeds $1
base=$1
while true; do
  n=$(/usr/bin/grep -c -E 'o84_p3|o85_' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md)
  if [ "$n" -gt "$base" ]; then echo "rows=$n"; exit 0; fi
  sleep 60
done
