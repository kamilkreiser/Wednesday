#!/bin/bash
# Gate 163 re-measure: the new file at head, the whole referral suite at head (x2) and base, red-first (base route files
# under head's tests, in MY clone, sha-restored), tsc (service config + tests-included), head and base.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980
R=$W/repo; REL=Blockchain/Dev/services/referral
vt(){ log=$1; shift; nice -n 10 node $W/scripts/vt.cjs "$@" > $log 2>&1; echo "rc=$?" >> $log; }
NEW=src/__tests__/ks1957-award-routes-owner-or-platform.test.ts
KS444=src/__tests__/qualify.validation.test.ts
vt $W/logs/head_new.log $NEW $KS444
vt $W/logs/head_whole.log
vt $W/logs/head_whole_run2.log
G163_ROOT=$W/wt/base/$REL vt $W/logs/base_whole.log
# red first
M=$R/$REL/src/routes/milestones.ts; F=$R/$REL/src/routes/referrals.ts
b1=$(shasum -a 256 $M | awk '{print $1}'); b2=$(shasum -a 256 $F | awk '{print $1}')
git -C $R show 66cbe4e52d5afadc9d13ca141200026cc68d5095:$REL/src/routes/milestones.ts > $M
git -C $R show 66cbe4e52d5afadc9d13ca141200026cc68d5095:$REL/src/routes/referrals.ts > $F
vt $W/logs/red_base_routes_head_tests.log $NEW $KS444
git -C $R checkout -q -- $REL/src/routes/milestones.ts $REL/src/routes/referrals.ts
a1=$(shasum -a 256 $M | awk '{print $1}'); a2=$(shasum -a 256 $F | awk '{print $1}')
{ [ "$b1$b2" = "$a1$a2" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/suites_restore.log
TSC=$R/Blockchain/Dev/node_modules/.bin/tsc
for v in head base; do
  if [ $v = head ]; then P=$R; else P=$W/wt/base; fi
  nice -n 10 $TSC -p $P/$REL/tsconfig.json --noEmit > $W/logs/tsc_service_$v.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_$v.log
  nice -n 10 $TSC -p $W/scripts/tsconfig.tests.$v.json > $W/logs/tsc_tests_$v.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$v.log
done
echo done > $W/logs/suites.done
