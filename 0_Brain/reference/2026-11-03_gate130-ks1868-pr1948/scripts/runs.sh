#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948
S=$W/repo/Blockchain/Dev/services/security/src
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $S/index.ts); H2=$(sha $S/db.ts)
bash $W/scripts/vt.sh $W/logs/head_new_tests.log ks1868-security-db-message ks1868-security-audit-event-message ks1868-security-validate-message; echo "head new rc=$?"
cp $W/logs/base_index.ts $S/index.ts; cp $W/logs/base_db.ts $S/db.ts
bash $W/scripts/vt.sh $W/logs/red_base_new_tests.log ks1868-security-db-message ks1868-security-audit-event-message ks1868-security-validate-message; echo "red rc=$?"
bash $W/scripts/vt.sh $W/logs/base_whole_excl_new.log --exclude '**/ks1868-security-*-message-coercion-*' --exclude '**/*.integration.test.ts' --exclude '**/node_modules/**'; echo "base whole excl rc=$?"
cp $W/logs/head_index.ts $S/index.ts; cp $W/logs/head_db.ts $S/db.ts
[ "$(sha $S/index.ts)" = "$H1" ] && [ "$(sha $S/db.ts)" = "$H2" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948/repo status --short
bash $W/scripts/vt.sh $W/logs/after_whole.log; echo "after whole rc=$?"
