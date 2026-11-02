#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
MB=fcfa5dfdba9b5fe1b4a7c4619403ff3d0e2fe54c; FILES="src/routes/verification.ts src/routes/verificationV2.ts"
mkdir -p $L/tsc_base_q
for f in $FILES; do shasum -a 256 $A/$f; done > $L/tscb_before.txt
for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done
for t in v2-route-catches-p1 verify-file-route-catch-p2 verify-hash-status-route-catches-p1; do mv $A/src/__tests__/ks1868-verification-$t-unreadable-throw.test.ts $L/tsc_base_q/; done
(cd $A && $D/node_modules/.bin/tsc -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_base.log 2>&1; echo "rc=$?" >> $L/tsc_tests_base.log)
(cd $A && $D/node_modules/.bin/tsc -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/src/__tests__/.*\.test\.ts$" >> $L/tsc_tests_base.log)
mv $L/tsc_base_q/*.test.ts $A/src/__tests__/
git -C $R checkout -- Blockchain/Dev/services/originate/src/routes
for f in $FILES; do shasum -a 256 $A/$f; done > $L/tscb_after.txt; cmp $L/tscb_before.txt $L/tscb_after.txt && echo RESTORE_OK; git -C $R status --short
