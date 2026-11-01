#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893
A=$G/repo/Blockchain/Dev/services/analytics; S=$A/src/services; T=$G/repo/Blockchain/Dev/node_modules/.bin/tsc
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $S/exportService.ts); H2=$(sha $S/scheduledJobs.ts)
nice -n 10 $T -p $G/scripts/tsconfig.tests.json > $G/logs/tsc_head.log 2>&1; echo "rc=$?" >> $G/logs/tsc_head.log
cp $G/logs/base_exportService.ts $S/exportService.ts; cp $G/logs/base_scheduledJobs.ts $S/scheduledJobs.ts
nice -n 10 $T -p $G/scripts/tsconfig.tests_excl_new.json > $G/logs/tsc_base_excl_new.log 2>&1; echo "rc=$?" >> $G/logs/tsc_base_excl_new.log
nice -n 10 $T -p $G/scripts/tsconfig.tests.json > $G/logs/tsc_base_product_all_tests.log 2>&1; echo "rc=$?" >> $G/logs/tsc_base_product_all_tests.log
cp $G/logs/head_exportService.ts $S/exportService.ts; cp $G/logs/head_scheduledJobs.ts $S/scheduledJobs.ts
[ "$(sha $S/exportService.ts)" = "$H1" ] && [ "$(sha $S/scheduledJobs.ts)" = "$H2" ] && echo RESTORE_OK || echo RESTORE_FAIL
