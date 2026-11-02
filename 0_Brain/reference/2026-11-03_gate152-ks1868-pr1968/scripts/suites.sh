#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest; S=$D/services/vc-issuer
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g152; mkdir -p $SC
export TMPDIR=$SC
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 $V run --root $S --maxWorkers=2 "$@" > $log 2>&1; echo "rc=$?" >> $log; }
T1=ks1868-credentialrepo-read-catches-unreadable-throw.test.ts
T2=ks1868-vc-issuer-db-pool-error-and-ready-hook-unreadable-throw.test.ts
P1=$S/src/repositories/credentialRepo.ts; P2=$S/src/db.ts
H1=$(sha $P1); H2=$(sha $P2)
: > $W/logs/suites_restore.log
vt $W/logs/head_new_files.log src/__tests__/$T1 src/__tests__/$T2
vt $W/logs/head_whole.log
git -C $R show 2f9f7db313b3:Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts > $P1
git -C $R show 2f9f7db313b3:Blockchain/Dev/services/vc-issuer/src/db.ts > $P2
vt $W/logs/red_base_new_repo.log src/__tests__/$T1
vt $W/logs/red_base_new_db.log src/__tests__/$T2
vt $W/logs/base_plus_new_whole.log
mv $S/src/__tests__/$T1 $SC/$T1; mv $S/src/__tests__/$T2 $SC/$T2
vt $W/logs/base_whole_excl_new.log
mv $SC/$T1 $S/src/__tests__/$T1; mv $SC/$T2 $S/src/__tests__/$T2
git -C $R checkout -q pr1968 -- Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts Blockchain/Dev/services/vc-issuer/src/db.ts
[ "$(sha $P1)" = "$H1" ] && [ "$(sha $P2)" = "$H2" ] && echo "restore OK" >> $W/logs/suites_restore.log || echo "RESTORE FAIL" >> $W/logs/suites_restore.log
git -C $R status --short >> $W/logs/suites_restore.log
echo done > $W/logs/suites.done
