#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941; R=$W/repo; A=$R/Blockchain/Dev/services/originate; L=$W/logs; T=23fee71fa9ccd7edd9c417dd5b6bf31d73e011e1
FILES="src/routes/verification.ts src/routes/verificationV2.ts"
for f in $FILES; do shasum -a 256 $A/$f; done > $L/union_sha_before.txt
for f in $FILES; do git -C $R show $T:Blockchain/Dev/services/originate/$f > $A/$f; done
T40=$(git -C $R diff --name-only e2a2426d221d pr1940 -- Blockchain/Dev/services/originate/src/__tests__)
for t in $T40; do git -C $R show pr1940:$t > $R/$t; echo "$t" >> $L/union_added_tests.txt; done
N=""; for t in $T40; do N="$N $(basename $t .test.ts)"; done
bash $W/scripts/jest.sh $L/union_new.json $L/union_new.log $N ks1868-verification-v2-chain-fact-catch-o78p3 ks1868-verification-v2-guards-coerce-message-o79b3 ks1868-verification-verify-file-guard-coerces-message-o79b2 ks1868-verification-verify-hash-status-guards-coerce-message-o79b1
bash $W/scripts/jest.sh $L/union_whole.json $L/union_whole.log
$R/Blockchain/Dev/node_modules/.bin/tsc -p $W/scripts/tsconfig.tests.json > $L/union_tsc.log 2>&1; echo rc=$? >> $L/union_tsc.log
for t in $T40; do mv $R/$t $L/_quarantine/; done
git -C $R checkout -- Blockchain/Dev/services/originate/src/routes
for f in $FILES; do shasum -a 256 $A/$f; done > $L/union_sha_after.txt; cmp $L/union_sha_before.txt $L/union_sha_after.txt && echo UNION_RESTORE_OK
git -C $R status --short
