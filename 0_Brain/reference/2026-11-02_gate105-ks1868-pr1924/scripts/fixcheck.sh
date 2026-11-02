#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate105-ks1868-pr1924; A=$W/repo/Blockchain/Dev/services/originate; F=$A/src/routes/certifications.ts
h0=$(shasum -a 256 $F | cut -d' ' -f1); cp $F $W/logs/_quarantine/cert_head_fixcheck.ts
perl -0pi -e 's/(\n {8})reason = error instanceof Error \? error\.message : String\(error\);/$1reason = String(error instanceof Error ? error.message : error);/g' $F
echo "replaced: $(grep -c 'reason = String(error instanceof Error ? error.message : error);' $F)"
cp $W/scripts/probe2.test.ts $A/src/__tests__/zz-gate105-fix.test.ts; : > $W/logs/probe2_fix.jsonl
(cd $A && PROBE_OUT=$W/logs/probe2_fix.jsonl npx jest zz-gate105-fix > $W/logs/probe2_fix_jest.log 2>&1); echo rc=$?
(cd $A && npx jest ks1868-certifications > $W/logs/fix_newtests.log 2>&1); echo newtests rc=$?; grep "^Tests:" $W/logs/fix_newtests.log
mv $A/src/__tests__/zz-gate105-fix.test.ts $W/logs/_quarantine/
cp $W/logs/_quarantine/cert_head_fixcheck.ts $F; [ "$(shasum -a 256 $F | cut -d' ' -f1)" = "$h0" ] && echo RESTORE_OK
