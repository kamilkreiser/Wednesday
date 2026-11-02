#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941; D=$W/repo/Blockchain/Dev; A=$D/services/originate; L=$W/logs
NEWT=$(git -C $W/repo diff --name-only e2a2426d221d pr1941 -- Blockchain/Dev/services/originate/src/__tests__ | sed "s#^#$W/repo/#")
node $W/scripts/lint.cjs $A $A/src/routes/verification.ts $A/src/routes/verificationV2.ts $NEWT > $L/eslint_pr_files.log 2>&1; echo rc=$? >> $L/eslint_pr_files.log
