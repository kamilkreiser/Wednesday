#!/bin/bash
# suite.sh base|head : whole packages/shared suite (its own vitest.config.ts) at develop (mut/base worktree) or the PR head (repo).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992
case "$1" in base) D=$W/mut/base/Blockchain/Dev;; head) D=$W/repo/Blockchain/Dev;; *) exit 2;; esac
mkdir -p $W/tmp/$1
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp/$1 NODE_ENV=test \
  $D/node_modules/.bin/vitest run --root $D/packages/shared --reporter=json --outputFile=$W/results/suite_$1.json > $W/runs/suite_$1.txt 2>&1
echo "suite $1 rc=$?" >> $W/runs/suite_rc.txt
