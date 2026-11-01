#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911
M=$G/repo/Blockchain/Dev/services/auth/src/routes/auth.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $G/logs/head_auth.ts); [ "$(sha $M)" = "$H1" ] || { echo "not at head"; exit 3; }
bash $G/scripts/vt.sh $G/logs/head_new_tests.log ks1868-auth-; echo "head new tests rc=$?"
cp $G/logs/base_auth.ts $M; echo "base product sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log ks1868-auth-; echo "red rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-auth-*' --exclude '**/node_modules/**'; echo "base whole excl new rc=$?"
cp $G/logs/head_auth.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo status --short
