#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate105-ks1868-pr1924
R=$W/repo; A=$R/Blockchain/Dev/services/originate; L=$W/logs
FILES="src/routes/certifications.ts"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
MB=fcfa5dfdba9b5fe1b4a7c4619403ff3d0e2fe54c
NEW="ks1868-certifications-read-route-catches-p1 ks1868-certifications-revoke-verify-share-route-catches-p2 ks1868-certifications-recertify-route-catch-p3"
mkdir -p $L/head_copy/src/routes
for f in $FILES; do cp $A/$f $L/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_before.txt
for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done
(cd $A && nice npx jest --forceExit --json --outputFile=$L/red_base.json $NEW > $L/red_base_new.log 2>&1; echo rc=$? >> $L/red_base_new.log)
(cd $A && nice npx jest --json --outputFile=$L/whole_base.json --testPathIgnorePatterns '/node_modules/' '\.integration\.test\.ts$' 'ks1868-certifications-(read-route-catches-p1|revoke-verify-share-route-catches-p2|recertify-route-catch-p3)' > $L/whole_base.log 2>&1; echo rc=$? >> $L/whole_base.log)
for f in $FILES; do cp $L/head_copy/$f $A/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_after.txt; cmp $L/runs_sha_before.txt $L/runs_sha_after.txt && echo RESTORE_OK
(cd $A && nice npx jest --json --outputFile=$L/head_new.json $NEW > $L/head_new_tests.log 2>&1; echo rc=$? >> $L/head_new_tests.log)
(cd $A && nice npx jest --json --outputFile=$L/whole_head.json > $L/whole_head.log 2>&1; echo rc=$? >> $L/whole_head.log)
date > $L/runs.done
