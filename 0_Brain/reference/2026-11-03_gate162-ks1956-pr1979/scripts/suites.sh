#!/bin/bash
# Gate 162 re-measure: referral vitest suite at head (x2), base whole, red-first (base product + head tests), tsc.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979
vt(){ log=$1; shift; nice -n 10 node $W/scripts/vt.cjs "$@" > $log 2>&1; echo "rc=$?" >> $log; }
# head (wt/head) and base (wt/base) trees, untouched
G162_ROOT=$W/wt/head/Blockchain/Dev/services/referral vt $W/logs/head_whole.log
G162_ROOT=$W/wt/head/Blockchain/Dev/services/referral vt $W/logs/head_whole_run2.log
G162_ROOT=$W/wt/base/Blockchain/Dev/services/referral vt $W/logs/base_whole.log
# red first: base product milestoneService.ts under head's tests, in MY clone (repo/), sha-restored
R=$W/repo; REL=Blockchain/Dev/services/referral; P=$R/$REL/src/services/milestoneService.ts
before=$(shasum -a 256 $P | awk '{print $1}')
git -C $R show 66cbe4e52d5afadc9d13ca141200026cc68d5095:$REL/src/services/milestoneService.ts > $P
vt $W/logs/red_base_product_head_tests.log src/__tests__/ks1956-milestone-awarded-once-per-user.test.ts src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts
git -C $R show pr1979:$REL/src/services/milestoneService.ts > $P
after=$(shasum -a 256 $P | awk '{print $1}')
{ [ "$before" = "$after" ] && echo "restore OK $after" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/suites_restore.log
# tsc: service config (src, tests excluded) and a tests-included config, head and base
TSC=$R/Blockchain/Dev/node_modules/.bin/tsc
for v in head base; do
  nice -n 10 $TSC -p $W/wt/$v/$REL/tsconfig.json --noEmit > $W/logs/tsc_service_$v.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_$v.log
  nice -n 10 $TSC -p $W/scripts/tsconfig.tests.$v.json > $W/logs/tsc_tests_$v.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$v.log
done
echo done > $W/logs/suites.done
