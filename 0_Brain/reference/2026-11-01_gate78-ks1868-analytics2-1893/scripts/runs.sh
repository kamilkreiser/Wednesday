#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893
R=$G/repo; S=src/services; A=$R/Blockchain/Dev/services/analytics
P=Blockchain/Dev/services/analytics/$S
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
E=$A/$S/exportService.ts; J=$A/$S/scheduledJobs.ts
H1=$(sha $E); H2=$(sha $J); echo "head sha $H1 $H2" | tee $G/logs/product_sha.log
# base product
git -C $R show refs/gate/develop:$P/exportService.ts > $G/logs/base_exportService.ts
git -C $R show refs/gate/develop:$P/scheduledJobs.ts > $G/logs/base_scheduledJobs.ts
cp $E $G/logs/head_exportService.ts; cp $J $G/logs/head_scheduledJobs.ts
# (1) head new tests
bash $G/scripts/vt.sh $G/logs/head_new_tests.log ks1868-export-service-db-save ks1868-scheduled-jobs-save-alert-rule; echo "head new tests rc=$?"
# (2) red-first: base product + new tests
cp $G/logs/base_exportService.ts $E; cp $G/logs/base_scheduledJobs.ts $J
echo "base product sha $(sha $E) $(sha $J)"
bash $G/scripts/vt.sh $G/logs/red_base_new_tests.log ks1868-export-service-db-save ks1868-scheduled-jobs-save-alert-rule; echo "red rc=$?"
# whole suite at base product, new tests excluded
bash $G/scripts/vt.sh $G/logs/base_whole_excl_new.log --exclude '**/ks1868-export-service-db-save*' --exclude '**/ks1868-scheduled-jobs-save-alert-rule*'; echo "base whole rc=$?"
# restore
cp $G/logs/head_exportService.ts $E; cp $G/logs/head_scheduledJobs.ts $J
[ "$(sha $E)" = "$H1" ] && [ "$(sha $J)" = "$H2" ] && echo RESTORE_OK || echo RESTORE_FAIL
echo "status:"; git -C $R status --short
# head whole
bash $G/scripts/vt.sh $G/logs/after_whole.log; echo "after whole rc=$?"
