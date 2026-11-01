#!/bin/bash
# red-first (base product + the 3 new files), base whole suite without the new files, base whole with them; restore head.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate95-ks1868-pr1913
R=$G/repo
A=$R/Blockchain/Dev/services/billing
P=$A/src/routes/webhooks.ts
git -C $R show 03977e89a343:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
echo "base product sha256 $(shasum -a 256 $P | awk '{print $1}')" > $G/logs/runs_outer.log
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log ks1868-billing-webhook-stripe; echo "red_base rc=$?" >> $G/logs/runs_outer.log
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-billing-webhook-stripe-*'; echo "base_excl rc=$?" >> $G/logs/runs_outer.log
git -C $R show pr1913:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
echo "restored sha256 $(shasum -a 256 $P | awk '{print $1}')" >> $G/logs/runs_outer.log
git -C $R status --short >> $G/logs/runs_outer.log
