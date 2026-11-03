#!/bin/bash
# suite_agw_alias.sh base|head : whole services/api-gateway suite with harness/vitest.gate177.agwsuite.config.ts (its own settings + @secuura/shared aliases).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
case "$1" in base) D=$W/mut/base/Blockchain/Dev;; head) D=$W/repo/Blockchain/Dev;; *) exit 2;; esac
P=$D/services/api-gateway; mkdir -p $W/tmp/agwa$1; s=$(date +%s)
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp/agwa$1 NODE_ENV=test \
  $P/node_modules/.bin/vitest run --root $P --config $P/vitest.gate177.agwsuite.config.ts --reporter=json --outputFile=$W/results/suite_agwa_$1.json > $W/runs/suite_agwa_$1.txt 2>&1
echo "suite agw-alias $1 rc=$? secs=$(( $(date +%s) - s ))" >> $W/runs/suite_rc.txt
