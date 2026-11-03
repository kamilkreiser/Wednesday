#!/bin/bash
# run.sh base|head : swap the product files, copy the harness in, run the shared recorder (Q1,Q3,Q4a) and the
# api-gateway recorder (Q4b). Rows -> results/q_<t>.jsonl
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
PS=$W/repo/Blockchain/Dev/packages/shared
AG=$W/repo/Blockchain/Dev/services/api-gateway
t=$1
$W/scripts/swap.sh $t > $W/runs/swap_$t.txt
mkdir -p $PS/src/__gate177__ $AG/src/__gate177__
cp $W/harness/values.ts $W/harness/verifier.test.ts $W/harness/clients.test.ts $PS/src/__gate177__/
cp $W/harness/values.ts $W/harness/dashboard.test.ts $AG/src/__gate177__/
cp $W/harness/vitest.gate177.shared.config.ts $PS/
cp $W/harness/vitest.gate177.agw.config.ts $AG/
: > $W/results/q_$t.jsonl
E="env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test LOG_LEVEL=debug GATE177_OUT=$W/results/q_$t.jsonl GATE177_TAG=$t"
$E $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $PS --config $PS/vitest.gate177.shared.config.ts > $W/runs/q_shared_$t.txt 2>&1; r1=$?
$E $AG/node_modules/.bin/vitest run --root $AG --config $AG/vitest.gate177.agw.config.ts > $W/runs/q_agw_$t.txt 2>&1; r2=$?
echo "shared rc=$r1 agw rc=$r2 lines=$(wc -l < $W/results/q_$t.jsonl)"
