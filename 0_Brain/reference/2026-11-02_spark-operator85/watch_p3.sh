#!/bin/bash
while true; do
  if /usr/bin/grep "o84_p3_" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep -q -E "PASS|FAIL"; then echo found; exit 0; fi
  sleep 60
done
