#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
D=$W/repo/Blockchain/Dev; V=$D/node_modules/.bin/vitest; A=$D/services/api-gateway
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g144
nice -n 10 $V run --root $A src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts > $W/logs/head_ks1543_alone.log 2>&1; echo "rc=$?" >> $W/logs/head_ks1543_alone.log
nice -n 10 $V run --root $A --maxWorkers=2 > $W/logs/head_whole_rerun.log 2>&1; echo "rc=$?" >> $W/logs/head_whole_rerun.log
echo done > $W/logs/rerun.done
