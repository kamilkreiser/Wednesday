#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate101-ks1868-pr1919
R=$W/repo; A=$R/Blockchain/Dev/services/originate; L=$W/logs
FILES="src/routes/systemErrors.ts src/services/errorTrackingService.ts src/repositories/certificationRepo.ts src/repositories/documentRepo.ts src/utils/notificationClient.ts src/routes/metering.ts"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
PAT="ks1868-certification-repo|ks1868-document-repo|ks1868-error-tracking|ks1868-metering|ks1868-notification|ks1868-system-errors"
for f in $FILES; do mkdir -p $L/head_copy/$(dirname $f); cp $A/$f $L/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_before.txt
MB=$(git -C $R merge-base origin/develop pr1919)
# 1 red at base (new tests present, product at base)
for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done
(cd $A && nice npx jest --json --outputFile=$L/red_base.json ks1868- > $L/red_base_new.log 2>&1; echo rc=$? >> $L/red_base_new.log)
# 2 whole suite at base excluding the 6 new test files
(cd $A && nice npx jest --json --outputFile=$L/whole_base.json --testPathIgnorePatterns '/node_modules/' '\.integration\.test\.ts$' 'ks1868-(certification-repo-verify|document-repo-verify|error-tracking-track|metering-usage|notification-client|system-errors-ingest)' > $L/whole_base.log 2>&1; echo rc=$? >> $L/whole_base.log)
for f in $FILES; do cp $L/head_copy/$f $A/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_after.txt; cmp $L/runs_sha_before.txt $L/runs_sha_after.txt && echo RESTORE_OK
# 3 whole suite at head
(cd $A && nice npx jest --json --outputFile=$L/whole_head.json > $L/whole_head.log 2>&1; echo rc=$? >> $L/whole_head.log)
date > $L/runs.done
