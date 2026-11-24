#!/bin/bash
W=/private/tmp/claude-501/qpom
. $W/env.sh
export CARGO_TARGET_DIR=$W/t_p1p
for a in "" "--red"; do
  echo "== test-p1p.sh $a start $(date '+%T') heavy=$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh)"
  python3 -B -c 'import os,sys; os.chdir(sys.argv[1]); os.execvp("bash", ["bash", "scripts/test-p1p.sh"] + sys.argv[2:])' $W/clone $a
  echo "== test-p1p.sh $a exit $? end $(date '+%T')"
done
