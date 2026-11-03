#!/bin/bash
# suite.sh shared|agw base|head : whole packages/shared or services/api-gateway suite (its own vitest.config.ts) at develop (mut/base) or the PR head (repo).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
case "$2" in base) D=$W/mut/base/Blockchain/Dev;; head) D=$W/repo/Blockchain/Dev;; *) exit 2;; esac
case "$1" in shared) P=$D/packages/shared; V=$D/node_modules/.bin/vitest;; agw) P=$D/services/api-gateway; V=$P/node_modules/.bin/vitest;; *) exit 2;; esac
mkdir -p $W/tmp/$1$2
s=$(date +%s)
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp/$1$2 NODE_ENV=test \
  $V run --root $P --reporter=json --outputFile=$W/results/suite_$1_$2.json > $W/runs/suite_$1_$2.txt 2>&1
echo "suite $1 $2 rc=$? secs=$(( $(date +%s) - s ))" >> $W/runs/suite_rc.txt
