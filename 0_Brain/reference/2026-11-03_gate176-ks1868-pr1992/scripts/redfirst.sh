#!/bin/bash
# redfirst.sh base|head : the PR's 4 new test files against base or head product blobs; JSON report to results/red_<t>.json
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992
PS=$W/repo/Blockchain/Dev/packages/shared
$W/scripts/swap.sh $1 > $W/runs/swap_red_$1.txt
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test \
  $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $PS --reporter=json --outputFile=$W/results/red_$1.json \
  src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts src/__tests__/ks1868-secrets-manager-vault-read-catch-unreadable-throw.test.ts \
  src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts src/__tests__/ks1868-ssrf-guard-safe-outbound-request-catch-unreadable-throw.test.ts > $W/runs/red_$1.txt 2>&1
echo "rc=$?"
