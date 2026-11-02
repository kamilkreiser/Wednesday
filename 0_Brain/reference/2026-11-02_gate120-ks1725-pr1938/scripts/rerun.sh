#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
D=$W/repo/Blockchain/Dev; L=$W/logs/rerun_$1; mkdir -p $L
ref=pr1938; [ "$1" = base ] && ref=8f313815f415
bash $W/scripts/co.sh $ref > $L/head.txt
cd $D/services/auth && $D/node_modules/.bin/vitest run --root $D/services/auth ks949-platform-admin-seed-identity > $L/ks949.log 2>&1; echo "ks949 rc=$?" >> $L/sum.txt
cd $D/packages/shared && $D/node_modules/.bin/vitest run --root $D/packages/shared threadToken > $L/thread.log 2>&1; echo "thread rc=$?" >> $L/sum.txt
for u in governance originate; do
 cd $D/services/$u && $D/node_modules/.bin/jest --rootDir $D/services/$u --json --outputFile=$L/jest_$u.json > $L/jest_$u.log 2>&1; echo "$u jest rc=$?" >> $L/sum.txt
done
echo DONE >> $L/sum.txt
