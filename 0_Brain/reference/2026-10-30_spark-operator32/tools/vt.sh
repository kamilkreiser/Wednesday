#!/bin/bash
# vt.sh <test-basename> <outfile> : run one vitest file in the clone, JSON-ish summary to outfile
A=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator32/clone/Blockchain/Dev/services/api-gateway
C=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator32/clone/Blockchain/Dev
$C/node_modules/.bin/vitest run --root $A --reporter=default "src/__tests__/$1" > "$2" 2>&1
echo "rc=$?" >> "$2"
