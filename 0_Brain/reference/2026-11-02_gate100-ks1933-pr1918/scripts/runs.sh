#!/bin/bash
# head new-file run; red-first (base webhooks.ts + the new file); base whole suite (base webhooks.ts + base versions of
# the two modified tests, new file excluded); head whole suite. Restores every touched file by sha256 to pr1918.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate100-ks1933-pr1918
R=$G/repo; A=$R/Blockchain/Dev/services/billing; O=$G/logs/runs_outer.log
F1=src/routes/webhooks.ts; F2=src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts; F3=src/__tests__/ks488-c4-webhook-idempotency-fail-closed.test.ts
put(){ git -C $R show $1:Blockchain/Dev/services/billing/$2 > $A/$2; }
: > $O
bash $G/scripts/vt.sh $G/logs/head_new_tests.log ks1933-billing-one-purchase; echo "head_new rc=$?" >> $O
put pr1913 $F1
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log ks1933-billing-one-purchase; echo "red_base rc=$?" >> $O
put pr1913 $F2; put pr1913 $F3
bash $G/scripts/vt.sh $G/logs/base_whole.log --exclude '**/ks1933-billing-one-purchase-*'; echo "base_whole rc=$?" >> $O
for f in $F1 $F2 $F3; do put pr1918 $f; done
bash $G/scripts/vt.sh $G/logs/head_whole.log; echo "head_whole rc=$?" >> $O
git -C $R status --short >> $O; echo "status lines: $(git -C $R status --short | wc -l)" >> $O
