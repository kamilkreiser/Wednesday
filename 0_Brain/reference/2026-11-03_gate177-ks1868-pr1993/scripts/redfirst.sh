#!/bin/bash
# redfirst.sh base|head : the PR's 4 new test files against base or head product blobs; JSON reports to results/red_<pkg>_<t>.json
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
PS=$W/repo/Blockchain/Dev/packages/shared
AG=$W/repo/Blockchain/Dev/services/api-gateway
$W/scripts/swap.sh $1 > $W/runs/swap_red_$1.txt
E="env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test"
$E $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $PS --reporter=json --outputFile=$W/results/red_shared_$1.json \
  src/__tests__/ks1868-identus-client-resolve-did-catch-unreadable-throw.test.ts src/__tests__/ks1868-service-client-health-check-catch-unreadable-throw.test.ts \
  src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts > $W/runs/red_shared_$1.txt 2>&1; r1=$?
$E $AG/node_modules/.bin/vitest run --root $AG --reporter=json --outputFile=$W/results/red_agw_$1.json \
  src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts > $W/runs/red_agw_$1.txt 2>&1; r2=$?
echo "$1 shared rc=$r1 agw rc=$r2"
