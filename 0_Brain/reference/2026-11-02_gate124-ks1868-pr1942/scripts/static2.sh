#!/bin/bash
# gate 124: tsc + eslint at head on a clean tree (the first static run overlapped the mutant run and was quarantined), then tsc at base
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350; F=src/routes/certifications.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
echo "product sha at start $(sha $A/$F) (PR head blob sha256 of git show: $(git -C $R show pr1942:Blockchain/Dev/services/originate/$F | shasum -a 256 | awk '{print $1}'))"
git -C $R status --short
TSC=$D/node_modules/.bin/tsc
$TSC -p $A/tsconfig.json --noEmit > $L/tsc_plain_head.log 2>&1; echo "rc=$?" >> $L/tsc_plain_head.log
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_head.log 2>&1; echo "rc=$?" >> $L/tsc_tests_head.log
NEWT=$(git -C $R diff --name-only $MB pr1942 -- Blockchain/Dev/services/originate/src/__tests__ | sed "s#^#$R/#")
node $W/scripts/lint.cjs $A $A/$F $NEWT > $L/eslint_pr_files.log 2>&1; echo "rc=$?" >> $L/eslint_pr_files.log
mkdir -p $L/tsc_base_q $L/head_copy/src/routes; cp $A/$F $L/head_copy/$F; sha $A/$F > $L/tscb_before.txt
git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F
for t in $NEWT; do mv $t $L/tsc_base_q/; done
$TSC -p $W/scripts/tsconfig.tests.json > $L/tsc_tests_base.log 2>&1; echo "rc=$?" >> $L/tsc_tests_base.log
$TSC -p $W/scripts/tsconfig.tests.json --listFilesOnly 2>/dev/null | /usr/bin/grep -c "/services/originate/src/__tests__/.*\.test\.ts$" > $L/tsc_tests_count_base.log
for t in $NEWT; do mv $L/tsc_base_q/$(basename $t) $t; done
cp $L/head_copy/$F $A/$F; sha $A/$F > $L/tscb_after.txt; cmp $L/tscb_before.txt $L/tscb_after.txt && echo TSCB_RESTORE_OK
git -C $R status --short
