#!/bin/bash
# QA-POLICY-AT: the comparer's red controls, one after the other: build (own empty target), run seed 1, compare to the seed-1 base.
W=/private/tmp/claude-501/qpa; unset TT
for n in Q1 P1 P2 P3; do
  T=pl/d$n
  bash $W/h/build.sh $T > $W/dout/plant_${n}_build.log 2>&1
  echo "$n build: $(grep -c Compiling $W/dout/plant_${n}_build.log) compiled; $(grep -E 'Compiling coagent-policy|^rc' $W/dout/plant_${n}_build.log | tr '\n' ' ')"
  bash $W/h/run_diff.sh $T 0x9a7c20261126aaa1 $W/dout/plant_${n}.jsonl 0 > $W/dout/plant_${n}_run.log 2>&1
  python3 -B -I $W/h/cmp_qpa.py $W/dout/s1_base.jsonl $W/dout/plant_${n}.jsonl $W/dout/cmp_plant_${n}.txt > $W/dout/cmp_plant_${n}.out 2>&1
  echo "$n compare exit $?: $(head -3 $W/dout/cmp_plant_${n}.out | tr '\n' ' ') $(grep -E 'FAIL (words|exact|prefix|extras)' $W/dout/cmp_plant_${n}.txt | tr '\n' ' ') $(grep RESULT $W/dout/cmp_plant_${n}.txt | tail -1)"
done
