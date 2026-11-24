#!/bin/bash
# QA-POLICY-OWNER-MODE D1 runner (v2 harness: card reason texts and scope labels included).
# The same harness file, built per tree from empty target dirs; two seeds at full size, base and head in parallel;
# then the two planted controls (plantA: a mode-absent card text; plantB: a both-agree allow text) at a small size
# against the base at the same size and seed.
W=/private/tmp/claude-501/qpom
run() { # tree seed n out
  b=$(ls $W/t_$1/release/build/coagent-policy/*/out/zz_qpom_diff-* | head -1)
  s=$(date +%s); QA_FX=$W/fx QA_SEED=$2 QA_N=$3 QA_OUT=$W/d1/$4.txt "$b" --nocapture > $W/d1/$4.log 2>&1
  echo "exit $? secs $(( $(date +%s)-s ))" >> $W/d1/$4.log
}
for seed in 0x51a7e0f0a11ced24 0x9a11c0de20261120; do
  run base $seed 205000 base_$seed & run head $seed 205000 head_$seed & wait
done
run base 0x51a7e0f0a11ced24 20000 small_base & run plantA 0x51a7e0f0a11ced24 20000 small_plantA & run plantB 0x51a7e0f0a11ced24 20000 small_plantB & wait
echo D1 DONE
