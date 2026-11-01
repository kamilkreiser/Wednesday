#!/bin/bash
# Q3: ks949 alone at head; base product whole suite WITH the new files (same file count/load as after); head whole again.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911
M=$G/repo/Blockchain/Dev/services/auth/src/routes/auth.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $G/logs/head_auth.ts); [ "$(sha $M)" = "$H1" ] || { echo "not at head"; exit 3; }
bash $G/scripts/vt.sh $G/logs/ks949_alone_head.log ks949; echo "ks949 alone head rc=$?"
cp $G/logs/base_auth.ts $M; echo "base product sha $(sha $M)"
bash $G/scripts/vt.sh $G/logs/ks949_alone_base.log ks949; echo "ks949 alone base rc=$?"
bash $G/scripts/vt.sh $G/logs/base_whole_incl_new.log; echo "base whole incl new rc=$?"
cp $G/logs/head_auth.ts $M; [ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
bash $G/scripts/vt.sh $G/logs/after_whole_2.log; echo "after whole 2 rc=$?"
node $G/scripts/tsc_lint.js
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo status --short
