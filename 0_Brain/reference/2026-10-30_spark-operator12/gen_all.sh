#!/bin/bash
# regenerates the KS-1830 briefs at the base given as $1 (default below); output = night/briefs (own new dirs only)
TIP=${1:-d7ddfa1f64336602a3441964f636e7d57a20c1d7}
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator12
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs
export GEN_TIP=$TIP GEN_OVERWRITE=1
for ch in plus slash; do
  CH=$ch python3 -I /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk_testonly.py $R/spec1830.py
  d=$B/ks_1830_p1_$ch
  sed -i '' '/^Tip:/s/on 2026-10-28/on 2026-10-30/' $d/KS-*.md
  grep -q '^ctx=' $d/spark.pins || echo 'ctx=65536' >> $d/spark.pins
done
