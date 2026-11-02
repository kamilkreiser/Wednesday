#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921
R=$G/repo; M=$R/Blockchain/Dev/services/kyc/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $G/logs/head_index.ts); [ "$(sha $M)" = "$H1" ] || { echo NOT_HEAD; exit 9; }
NEW="ks1868-kyc-save-image|ks1868-kyc-verify-db-ready"
bash $G/scripts/vt.sh $G/logs/head_new_tests.log ks1868-kyc-save-image-attestation ks1868-kyc-verify-db-ready-boot-probe; echo "head new rc=$?"
cp $G/logs/mergebase_index.ts $M; echo "base sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log ks1868-kyc-save-image-attestation ks1868-kyc-verify-db-ready-boot-probe; echo "red rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-kyc-save-image-attestation-*' --exclude '**/ks1868-kyc-verify-db-ready-*' --exclude '**/node_modules/**'; echo "base whole excl new rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_incl_new.log; echo "base whole incl new rc=$?"
cp $G/logs/head_index.ts $M; [ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921/repo status --short
