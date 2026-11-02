#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941
R=$W/repo; A=$R/Blockchain/Dev/services/originate; L=$W/logs; J=$W/scripts/jest.sh
FILES="src/routes/verification.ts src/routes/verificationV2.ts"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
NEW="ks1868-verification-v2-chain-fact-catch-o78p3 ks1868-verification-v2-guards-coerce-message-o79b3 ks1868-verification-verify-file-guard-coerces-message-o79b2 ks1868-verification-verify-hash-status-guards-coerce-message-o79b1"
IGN='(ks1868-verification-v2-chain-fact-catch-o78p3|ks1868-verification-v2-guards-coerce-message-o79b3|ks1868-verification-verify-file-guard-coerces-message-o79b2|ks1868-verification-verify-hash-status-guards-coerce-message-o79b1)'
mkdir -p $L/head_copy/src/routes
for f in $FILES; do cp $A/$f $L/head_copy/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_before.txt
for f in $FILES; do git -C $R show $MB:Blockchain/Dev/services/originate/$f > $A/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_base.txt
uptime > $L/load_runs.log
bash $J $L/red_base.json $L/red_base_new.log $NEW
bash $J $L/whole_base.json $L/whole_base.log --testPathIgnorePatterns '/node_modules/' '\.integration\.test\.ts$' "$IGN"
uptime >> $L/load_runs.log
for f in $FILES; do cp $L/head_copy/$f $A/$f; done
for f in $FILES; do sha $A/$f; done > $L/runs_sha_after.txt; cmp $L/runs_sha_before.txt $L/runs_sha_after.txt && echo RESTORE_OK > $L/runs_restore.log
bash $J $L/whole_head.json $L/whole_head.log
uptime >> $L/load_runs.log
git -C $R status --short > $L/runs_status_end.log
date > $L/runs.done
