#!/bin/bash
# originate (jest, cwd = logs/child_cwd): head new files; head whole; base product + new files (red first); base whole without new files. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964
R=$W/repo; O=$R/Blockchain/Dev/services/originate; SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g149
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
jt(){ log=$1; shift; nice -n 10 node $W/scripts/jest.js "$@" > $log 2>&1; echo "rc=$?" >> $log; }
P=src/routes/documents.ts; REL=Blockchain/Dev/services/originate
T1=ks1868-documents-lookup-routes-message-coercion-unreadable-throw.test.ts; T2=ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts
H=$(sha $O/$P)
jt $W/logs/head_new.log --runTestsByPath $O/src/__tests__/$T1 $O/src/__tests__/$T2
jt $W/logs/head_whole.log --maxWorkers=4
git -C $R show 4d1ab2cb6574:$REL/$P > $O/$P
jt $W/logs/red_base_new.log --runTestsByPath $O/src/__tests__/$T1 $O/src/__tests__/$T2
mv $O/src/__tests__/$T1 $SC/$T1; mv $O/src/__tests__/$T2 $SC/$T2
jt $W/logs/base_whole_excl_new.log --maxWorkers=4
mv $SC/$T1 $O/src/__tests__/$T1; mv $SC/$T2 $O/src/__tests__/$T2
git -C $R show pr1964:$REL/$P > $O/$P
{ [ "$(sha $O/$P)" = "$H" ] && echo "restore OK" || echo "RESTORE FAIL"; git -C $R status --short; } > $W/logs/suites_restore.log
echo done > $W/logs/suites.done
