#!/bin/bash
# regenerates the five operator-11 briefs at the base given as $1 (default: the base below); output = night/briefs (own new dirs only)
TIP=${1:-5a5c4d2b353fa4091762630df8bfaea26d6b9245}
export GEN_TIP=$TIP GEN_OVERWRITE=1
for s in spec1827 spec1828 spec1817 spec1817b; do python3 -I /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk_testonly.py /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator11/$s.py; done
python3 -I /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk2.py /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator11/spec1818.py
for d in ks_1827_p1_byid_spread_live ks_1828_p1_signhash_other_verbs ks_1817_p1_fallback_text ks_1817_p1b_no_message ks_1818_p1_logger_guard; do
  sed -i '' '/^Tip:/s/on 2026-10-28/on 2026-10-30/' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/$d/KS-*.md
  grep -q '^ctx=' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/$d/spark.pins || echo 'ctx=65536' >> /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/$d/spark.pins
done
