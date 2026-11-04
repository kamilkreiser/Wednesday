#!/bin/bash
# gate 194 runner. usage: run.sh <side-label> <base|head|keep> [extra vitest files relative to vc-issuer...]
# base: product files credentialRepo.ts + routes/credentials.ts overlaid from develop e899463d2a0b, restored from the head blob after
#       (git show > file; blob id checked against the head's ls-tree). keep: whatever product bytes are in the tree (mutant runs).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959; R=$W/repo; V=$R/Blockchain/Dev/services/vc-issuer
BASE=e899463d2a0b1b30f2cff46b23d001622620029a; HEAD=a968818a0038727399663775722017c130d4cb08
SIDE=$1; MODE=$2; shift 2
P1=Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
P2=Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts
mkdir -p $W/logs $W/cwd $W/home $W/tmp
cp $W/gate_tests/gate194-matrix.test.ts $V/src/__tests__/gate194-matrix.test.ts
if [ "$MODE" = base ]; then
  git -C $R show $BASE:$P1 > $R/$P1
  git -C $R show $BASE:$P2 > $R/$P2
  echo "overlay: $(git -C $R hash-object $R/$P1) $(git -C $R hash-object $R/$P2) want $(git -C $R rev-parse $BASE:$P1) $(git -C $R rev-parse $BASE:$P2)" > $W/logs/overlay_$SIDE.log
fi
OUT=$W/logs/matrix_$SIDE.jsonl; rm -f $OUT
cd $W/cwd || exit 9
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp G194_OUT=$OUT G194_SIDE=$SIDE \
  $R/Blockchain/Dev/node_modules/.bin/vitest run --root $V src/__tests__/gate194-matrix.test.ts "$@" --reporter=verbose > $W/logs/run_$SIDE.log 2>&1
echo rc=$? >> $W/logs/run_$SIDE.log
rm -f $V/src/__tests__/gate194-matrix.test.ts
if [ "$MODE" = base ]; then
  git -C $R show $HEAD:$P1 > $R/$P1
  git -C $R show $HEAD:$P2 > $R/$P2
fi
echo "restored blobs equal head: $([ "$(git -C $R hash-object $R/$P1)" = "$(git -C $R rev-parse $HEAD:$P1)" ] && [ "$(git -C $R hash-object $R/$P2)" = "$(git -C $R rev-parse $HEAD:$P2)" ] && echo yes || echo NO)" >> $W/logs/run_$SIDE.log
git -C $R status --short > $W/logs/status_after_$SIDE.log
echo "status lines: $(wc -l < $W/logs/status_after_$SIDE.log)" >> $W/logs/run_$SIDE.log
tail -3 $W/logs/run_$SIDE.log
