#!/bin/bash
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992
PS=$W/repo/Blockchain/Dev/packages/shared
t=$1
$W/scripts/swap.sh $t > $W/runs/swap_q2_$t.txt
cp $W/harness/values.ts $W/harness/dispatch.test.ts $PS/src/__gate176__/
cp $W/harness/vitest.gate176.q2.config.ts $PS/vitest.gate176.q2.config.ts
: > $W/results/q2_$t.jsonl
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test GATE176_OUT=$W/results/q2_$t.jsonl GATE176_TAG=$t \
  $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $PS --config $PS/vitest.gate176.q2.config.ts > $W/runs/q2_$t.txt 2>&1
echo "rc=$? lines=$(wc -l < $W/results/q2_$t.jsonl)"
