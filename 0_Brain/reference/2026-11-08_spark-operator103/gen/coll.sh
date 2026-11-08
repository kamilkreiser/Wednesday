#!/bin/bash
# usage: coll.sh <path-substring>...  -> held READY hits + open-PR hits
N=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator103
for p in "$@"; do
  h=$(/usr/bin/grep -l -F -- "$p" $N/READY_* 2>/dev/null | wc -l)
  pr=$(/usr/bin/grep -c -F -- "$p" $D/prs_cur.json)
  echo "$p  READY_hits=$h  PR_hits=$pr"
done
