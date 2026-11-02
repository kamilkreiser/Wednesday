#!/bin/bash
# originate (jest): head new files; head whole; base products + new files (red first); base whole without new files. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate145-ks1868-pr1961
R=$W/repo; O=$R/Blockchain/Dev/services/originate; SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g145
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
jt(){ log=$1; shift; nice -n 10 node $W/scripts/jest.js "$@" > $log 2>&1; echo "rc=$?" >> $log; }
P1=src/services/errorTrackingService.ts; P2=src/utils/lifecyclePayloadCodec.ts; REL=Blockchain/Dev/services/originate
T1=ks1868-error-tracking-get-recent-errors-catch-unreadable-throw.test.ts; T2=ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts
H1=$(sha $O/$P1); H2=$(sha $O/$P2)
jt $W/logs/head_new.log --runTestsByPath $O/src/__tests__/$T1 $O/src/__tests__/$T2
jt $W/logs/head_whole.log --maxWorkers=4
for p in $P1 $P2; do git -C $R show 2d3b3bb3:$REL/$p > $O/$p; done
jt $W/logs/red_base_new.log --runTestsByPath $O/src/__tests__/$T1 $O/src/__tests__/$T2
mv $O/src/__tests__/$T1 $SC/$T1; mv $O/src/__tests__/$T2 $SC/$T2
jt $W/logs/base_whole_excl_new.log --maxWorkers=4
mv $SC/$T1 $O/src/__tests__/$T1; mv $SC/$T2 $O/src/__tests__/$T2
for p in $P1 $P2; do git -C $R show pr1961:$REL/$p > $O/$p; done
{ [ "$(sha $O/$P1)" = "$H1" ] && [ "$(sha $O/$P2)" = "$H2" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/suites_restore.log
echo done > $W/logs/suites.done
