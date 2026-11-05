#!/bin/bash
# usage: run.sh <side> <base|head|keep>   (keep = whatever product bytes are in the tree, for mutants)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006; R=$W/repo; S=$R/Blockchain/Dev/services/originate
BASE=07a2d62be6a09c9cd504864d1cf1906543d55317; HEAD=6311c141f99e5ade8d94e60ee15b0c80006a52cd
P=Blockchain/Dev/services/originate/src/routes/adminConfig.ts
SIDE=$1; MODE=$2
mkdir -p $W/runs $W/scratch/_quarantine
cp $W/gate_tests/gate195-matrix.test.ts $S/src/__tests__/gate195-matrix.test.ts
if [ "$MODE" = base ]; then git -C $R show $BASE:$P > $R/$P; fi
echo "product blob $(git -C $R hash-object $R/$P) base=$(git -C $R rev-parse $BASE:$P) head=$(git -C $R rev-parse $HEAD:$P)" > $W/logs/blob_$SIDE.log
OUT=$W/runs/matrix_$SIDE.jsonl; : > $OUT
cd $W/cwd || exit 9
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp G195_OUT=$OUT G195_SIDE=$SIDE \
  $R/Blockchain/Dev/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js gate195-matrix > $W/logs/run_$SIDE.log 2>&1
echo rc=$? >> $W/logs/run_$SIDE.log
mv $S/src/__tests__/gate195-matrix.test.ts $W/scratch/_quarantine/gate195-matrix.$SIDE.test.ts
if [ "$MODE" = base ]; then git -C $R show $HEAD:$P > $R/$P; fi
echo "restored equal head: $([ "$(git -C $R hash-object $R/$P)" = "$(git -C $R rev-parse $HEAD:$P)" ] && echo yes || echo NO); status: $(git -C $R status --short | wc -l)" >> $W/logs/run_$SIDE.log
tail -12 $W/logs/run_$SIDE.log; wc -l $OUT
