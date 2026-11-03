#!/bin/bash
# nores.sh : run harness/nores.test.ts at base and head, NODE_ENV test and production. Rows -> results/nores.jsonl
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
PS=$W/repo/Blockchain/Dev/packages/shared
mkdir -p $PS/src/__gate177__; cp $W/harness/nores.test.ts $PS/src/__gate177__/
: > $W/results/nores.jsonl
for t in base head; do $W/scripts/swap.sh $t > /dev/null; for ne in test production; do
  echo "{\"tree\":\"$t\"}" >> $W/results/nores.jsonl
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=$ne GATE177_OUT=$W/results/nores.jsonl \
    $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $PS --config $PS/vitest.gate177.shared.config.ts src/__gate177__/nores.test.ts > $W/runs/nores_${t}_$ne.txt 2>&1; echo "$t $ne rc=$?"
done; done
$W/scripts/swap.sh head > /dev/null
echo "repo clean vs head: $(git -C $W/repo diff --quiet HEAD -- Blockchain/Dev && echo yes || echo NO)"
