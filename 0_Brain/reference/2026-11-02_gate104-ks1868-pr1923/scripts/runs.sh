#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923
R=$W/repo; A=$R/Blockchain/Dev/services/originate; L=$W/logs
FILES="src/routes/signatories.ts src/routes/thirdPartyVerifiers.ts src/services/retentionScheduler.ts"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
MB=04ff5262ad526a13c1a0df99480b76860a8d11d1
mkdir -p $L/head_copy/src/routes $L/head_copy/src/services
for f in $FILES; do cp $A/$f $L/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_before.txt
for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done
(cd $A && nice npx jest --json --outputFile=$L/red_base.json ks1868-retention-scheduler-run-enforcement-p3 ks1868-signatories-read-routes-p1 ks1868-signatories-write-routes-p2 ks1868-third-party-verifiers-admin-routes-p3 ks1868-third-party-verifiers-verify-routes-p4 > $L/red_base_new.log 2>&1; echo rc=$? >> $L/red_base_new.log)
(cd $A && nice npx jest --json --outputFile=$L/whole_base.json --testPathIgnorePatterns '/node_modules/' '\.integration\.test\.ts$' 'ks1868-(retention-scheduler-run-enforcement-p3|signatories-read-routes-p1|signatories-write-routes-p2|third-party-verifiers-admin-routes-p3|third-party-verifiers-verify-routes-p4)' > $L/whole_base.log 2>&1; echo rc=$? >> $L/whole_base.log)
for f in $FILES; do cp $L/head_copy/$f $A/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_after.txt; cmp $L/runs_sha_before.txt $L/runs_sha_after.txt && echo RESTORE_OK
(cd $A && nice npx jest --json --outputFile=$L/head_new.json ks1868-retention-scheduler-run-enforcement-p3 ks1868-signatories-read-routes-p1 ks1868-signatories-write-routes-p2 ks1868-third-party-verifiers-admin-routes-p3 ks1868-third-party-verifiers-verify-routes-p4 > $L/head_new_tests.log 2>&1; echo rc=$? >> $L/head_new_tests.log)
(cd $A && nice npx jest --json --outputFile=$L/whole_head.json > $L/whole_head.log 2>&1; echo rc=$? >> $L/whole_head.log)
date > $L/runs.done
