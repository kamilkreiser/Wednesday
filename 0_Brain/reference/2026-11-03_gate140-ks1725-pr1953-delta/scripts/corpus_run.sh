#!/bin/bash
# base (develop 2d3b3bb3, zod 3.25.76) -> inputs; head pass 1 -> pairmap; head pass 2 with pairmap. LBL suffix: plain | enums
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta; S=$G/scripts; L=$G/logs; LBL=$1
node $S/corpus_side.cjs base $G/repo_base/Blockchain/Dev $L/corpus_base_$LBL.json > $L/corpus_base_$LBL.log 2>&1; echo "base rc=$?" >> $L/corpus_base_$LBL.log
node $S/corpus_side.cjs head $G/repo/Blockchain/Dev $L/corpus_head_$LBL.json $L/corpus_base_$LBL.inputs.json > $L/corpus_head1_$LBL.log 2>&1; echo "head1 rc=$?" >> $L/corpus_head1_$LBL.log
python3 $S/corpus_cmp.py $LBL pairmap > $L/pairmap_$LBL.log 2>&1
node $S/corpus_side.cjs head $G/repo/Blockchain/Dev $L/corpus_head_$LBL.json $L/corpus_base_$LBL.inputs.json $L/pairmap_$LBL.json > $L/corpus_head_$LBL.log 2>&1; echo "head rc=$?" >> $L/corpus_head_$LBL.log
python3 $S/corpus_cmp.py $LBL > $L/corpus_cmp_$LBL.log 2>&1
python3 $S/categorize.py $LBL > $L/categories_$LBL.log 2>&1
echo DONE $LBL
