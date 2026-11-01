#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912
R=$G/repo; M=$R/Blockchain/Dev/services/security/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW="ks1868-security-key-register-save ks1868-security-key-revoke-save ks1868-security-admin-scopes-put"
H1=$(sha $M); echo "head sha $H1"
bash $G/scripts/vt.sh $G/logs/head_new_tests.log $NEW; echo "head new rc=$?"
cp $G/logs/base_index.ts $M; echo "base sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log $NEW; echo "red rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-security-key-register-save*' --exclude '**/ks1868-security-key-revoke-save*' --exclude '**/ks1868-security-admin-scopes-put*' --exclude '**/*.integration.test.ts' --exclude '**/node_modules/**'; echo "base whole excl rc=$?"
cp $G/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912/repo status --short
