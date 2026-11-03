#!/bin/bash
# run.sh base|head [testfile-filter] : swap product files, copy the harness in, run the recorder, write results/q_<t>.jsonl
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992
PS=$W/repo/Blockchain/Dev/packages/shared
t=$1
$W/scripts/swap.sh $t > $W/runs/swap_$t.txt
mkdir -p $PS/src/__gate176__
cp $W/harness/values.ts $W/harness/ssrf.test.ts $W/harness/secrets_indexer.test.ts $W/harness/blockfrost_stub.ts $PS/src/__gate176__/
cp $W/harness/vitest.gate176.config.ts $PS/vitest.gate176.config.ts
: > $W/results/q_$t.jsonl
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test LOG_LEVEL=debug GATE176_OUT=$W/results/q_$t.jsonl GATE176_TAG=$t \
  $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $PS --config $PS/vitest.gate176.config.ts ${2:-} > $W/runs/q_$t.txt 2>&1
echo "rc=$? lines=$(wc -l < $W/results/q_$t.jsonl)"
