#!/bin/bash
# usage: measure.sh <ref> <tag>   (tsc + vitest per touched unit, all anchored to the gate clone)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938
D=$W/repo/Blockchain/Dev; L=$W/logs/$2; mkdir -p $L
cd $D
bash $W/scripts/co.sh $1 > $L/head.txt
$D/node_modules/.bin/tsc -p $D/packages/shared/tsconfig.json > $L/shared_build.log 2>&1; echo "shared build rc=$?" >> $L/shared_build.log
for u in $(cat $W/scripts/units.txt); do
  n=$(echo $u | tr / _)
  cfg=$D/$u/tsconfig.json; [ -f $D/$u/tsconfig.test.json ] && cfg=$D/$u/tsconfig.test.json
  $D/node_modules/.bin/tsc --noEmit -p $cfg > $L/tsc_$n.log 2>&1; echo "$u tsc_errors=$(grep -c 'error TS' $L/tsc_$n.log)" >> $L/tsc_summary.txt
done
echo TSC_DONE >> $L/tsc_summary.txt
for u in $(cat $W/scripts/units.txt); do
  n=$(echo $u | tr / _)
  [ -f $D/$u/vitest.config.ts ] || continue
  cd $D/$u && $D/node_modules/.bin/vitest run --root $D/$u --reporter=json --outputFile=$L/vt_$n.json > $L/vt_$n.log 2>&1; echo "$u rc=$?" >> $L/vt_summary.txt
done
echo DONE >> $L/vt_summary.txt
