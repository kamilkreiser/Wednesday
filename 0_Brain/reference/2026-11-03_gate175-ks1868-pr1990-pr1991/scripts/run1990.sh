#!/bin/bash
# run1990.sh base|head : swap product files, copy the harness in, run the PR 1990 recorder, write results/p1990_<t>.jsonl
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991
D=$W/repo/Blockchain/Dev
t=$1
$W/scripts/swap.sh $t > $W/runs/swap_$t.txt
mkdir -p $D/packages/shared/src/__gate175__
cp $W/harness/values.ts $W/harness/p1990.test.ts $D/packages/shared/src/__gate175__/
cp $W/harness/vitest.gate175.ps.config.ts $D/packages/shared/vitest.gate175.config.ts
: > $W/results/p1990_$t.jsonl
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp LOG_LEVEL=debug NODE_ENV=test GATE175_OUT=$W/results/p1990_$t.jsonl GATE175_TAG=$t \
  $D/node_modules/.bin/vitest run --root $D/packages/shared --config $D/packages/shared/vitest.gate175.config.ts > $W/runs/p1990_$t.txt 2>&1
echo "rc=$? lines=$(wc -l < $W/results/p1990_$t.jsonl)"
