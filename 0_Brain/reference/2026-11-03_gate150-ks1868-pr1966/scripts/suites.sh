#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate150-ks1868-pr1966
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g150; mkdir -p $SC
export TMPDIR=$SC
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ svc=$1; log=$2; shift 2; nice -n 10 $V run --root $D/services/$svc --maxWorkers=2 "$@" > $log 2>&1; echo "rc=$?" >> $log; }
newf(){ case $1 in prism) echo ks1868-prism-db-pool-error-and-ready-hook-unreadable-throw.test.ts;; *) echo ks1868-$1-db-pool-error-listener-unreadable-throw.test.ts;; esac; }
: > $W/logs/suites_restore.log
for svc in prism timestamping security; do
  P=$D/services/$svc/src/db.ts; REL=Blockchain/Dev/services/$svc/src/db.ts
  TB=$(newf $svc); T=$D/services/$svc/src/__tests__/$TB
  H=$(sha $P)
  vt $svc $W/logs/head_whole_$svc.log
  git -C $R show 4d1ab2cb:$REL > $P
  vt $svc $W/logs/red_base_new_$svc.log src/__tests__/$TB
  vt $svc $W/logs/base_plus_new_whole_$svc.log
  mv $T $SC/$TB
  vt $svc $W/logs/base_whole_excl_new_$svc.log
  mv $SC/$TB $T
  git -C $R show pr1966:$REL > $P
  [ "$(sha $P)" = "$H" ] && echo "$svc restore OK" >> $W/logs/suites_restore.log || echo "$svc RESTORE FAIL" >> $W/logs/suites_restore.log
  git -C $R status --short >> $W/logs/suites_restore.log
done
echo done > $W/logs/suites.done
