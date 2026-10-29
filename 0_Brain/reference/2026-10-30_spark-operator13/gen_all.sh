#!/bin/bash
# regenerates the operator-13 briefs from the clone checked out at the base; usage: gen_all.sh <spec-basename>...
TIP=203734468019feaf44428975b10cf5f799483187
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator13
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs
export GEN_TIP=$TIP GEN_SRC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/7fe6fe98-e251-41b8-83ea-c831f0aa2549/scratchpad/op13/src GEN_OVERWRITE=1
for s in "$@"; do
  python3 -I /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py $R/$s.py
done
