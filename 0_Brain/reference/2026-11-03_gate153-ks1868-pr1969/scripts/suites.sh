#!/bin/bash
# referral (vitest): head new files; head whole; base product (4 files) + new files (red first); base whole without new files. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969
R=$W/repo; REL=Blockchain/Dev/services/referral; T=$R/$REL; SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g153
BASE=26955bf1b828113fcfe29b6bd6e371dbe28b5360
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 node $W/scripts/vt.cjs "$@" > $log 2>&1; echo "rc=$?" >> $log; }
PS="src/db.ts src/services/milestoneService.ts src/services/referralService.ts src/services/fraudDetection.ts"
NEW=$(cd $T && ls src/__tests__/ks1868-*.test.ts)
before=$(for p in $PS; do sha $T/$p; done)
vt $W/logs/head_new.log $NEW
vt $W/logs/head_whole.log
vt $W/logs/head_whole_run2.log
for p in $PS; do git -C $R show $BASE:$REL/$p > $T/$p; done
vt $W/logs/red_base_new.log $NEW
mkdir -p $SC/newtests; for n in $NEW; do mv $T/$n $SC/newtests/; done
vt $W/logs/base_whole_excl_new.log
for n in $NEW; do mv $SC/newtests/$(basename $n) $T/$n; done
for p in $PS; do git -C $R show pr1969:$REL/$p > $T/$p; done
after=$(for p in $PS; do sha $T/$p; done)
{ [ "$before" = "$after" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/suites_restore.log
echo done > $W/logs/suites.done
