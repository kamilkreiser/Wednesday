#!/bin/bash
# QA-POLICY-NOTES: run one harness (da|db) for one tree and seed. Fixture pre-created (QA_N=1) so parallel runs only read it.
# usage: run_diff.sh <da|db> <tree> <seed> <n> <outname>
W=/private/tmp/claude-501/qpn
k=$1; t=$2; seed=$3; n=$4; o=$5
mkdir -p $W/d_$k
b=$(ls $W/t_$t/release/build/coagent-policy/*/out/zz_qpn_$k-* | grep -v '\.d$' | head -1)
s=$(date +%s)
QA_FX=$W/fx QA_SEED=$seed QA_N=$n QA_OUT=$W/d_$k/$o.txt "$b" --nocapture > $W/d_$k/$o.log 2>&1
echo "exit $? secs $(( $(date +%s)-s )) bin $b" >> $W/d_$k/$o.log
