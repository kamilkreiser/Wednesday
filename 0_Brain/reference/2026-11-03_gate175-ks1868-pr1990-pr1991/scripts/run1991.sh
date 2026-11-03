#!/bin/bash
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991
D=$W/repo/Blockchain/Dev
t=$1
$W/scripts/swap.sh $t > $W/runs/swap_$t.txt
mkdir -p $D/services/shared/src/__gate175__
cp $W/harness/values.ts $W/harness/p1991_stores.test.ts $W/harness/p1991_pool.test.ts $D/services/shared/src/__gate175__/
cp $W/harness/vitest.gate175.ss.config.ts $D/services/shared/vitest.gate175.config.ts
: > $W/results/p1991_$t.jsonl
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp LOG_LEVEL=debug NODE_ENV=test GATE175_OUT=$W/results/p1991_$t.jsonl GATE175_TAG=$t \
  $D/node_modules/.bin/vitest run --root $D/services/shared --config $D/services/shared/vitest.gate175.config.ts > $W/runs/p1991_$t.txt 2>&1
echo "rc=$? lines=$(wc -l < $W/results/p1991_$t.jsonl)"
