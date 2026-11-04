#!/bin/bash
# gate 191 runner. usage: run.sh <side-label> <base|head|keep> <test-file-relative-to-vc-issuer...>
# base: product files credentialRepo.ts + revocationResolvers.ts taken from develop 035685291b9d, restored to head after.
# keep: run against whatever product bytes are in the tree (mutant runs).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003; R=$W/repo; V=$R/Blockchain/Dev/services/vc-issuer
SIDE=$1; MODE=$2; shift 2
P1=Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
P2=Blockchain/Dev/services/vc-issuer/src/services/revocationResolvers.ts
mkdir -p $W/logs $W/cwd $W/home $W/tmp
cp $W/gate_tests/gate191-matrix.test.ts $V/src/__tests__/gate191-matrix.test.ts
if [ "$MODE" = base ]; then
  git -C $R show 035685291b9d58ae6ea8ba5f05adf9379f9c2944:$P1 > $R/$P1
  git -C $R show 035685291b9d58ae6ea8ba5f05adf9379f9c2944:$P2 > $R/$P2
fi
OUT=$W/logs/matrix_$SIDE.jsonl; rm -f $OUT
( cd $W/cwd && env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp G191_OUT=$OUT G191_SIDE=$SIDE \
  $R/Blockchain/Dev/node_modules/.bin/vitest run --root $V "$@" --reporter=verbose > $W/logs/run_$SIDE.log 2>&1; echo rc=$? >> $W/logs/run_$SIDE.log )
rm -f $V/src/__tests__/gate191-matrix.test.ts
if [ "$MODE" = base ]; then
  git -C $R checkout -q 8b140178276457116714892fe0cf73b9f1e92c8c -- $P1 $P2
fi
git -C $R status --short > $W/logs/status_after_$SIDE.log
tail -1 $W/logs/run_$SIDE.log
