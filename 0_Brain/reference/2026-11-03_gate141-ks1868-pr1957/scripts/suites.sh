#!/bin/bash
# per service: head whole; base-product + new tests (new file alone, then whole); base without new file (whole). sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957
R=$W/repo; D=$R/Blockchain/Dev; V=$D/node_modules/.bin/vitest
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9ee83091-a095-4b37-9c10-a5738ac0ba5f/scratchpad/g141; mkdir -p $SC
export TMPDIR=$SC
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ svc=$1; log=$2; shift 2; nice -n 10 $V run --root $D/services/$svc --maxWorkers=2 "$@" > $log 2>&1; echo "rc=$?" >> $log; }
for svc in nft-certificate transfer wallet-connector m365-integration staking; do
  P=$D/services/$svc/src/db.ts; REL=Blockchain/Dev/services/$svc/src/db.ts
  T=$(ls $D/services/$svc/src/__tests__/ks1868-*db-pool*.test.ts); TB=$(basename $T)
  H=$(sha $P)
  vt $svc $W/logs/head_whole_$svc.log
  git -C $R show 2d3b3bb3:$REL > $SC/base_$svc.ts
  cp $SC/base_$svc.ts $P
  vt $svc $W/logs/red_base_new_$svc.log src/__tests__/$TB
  vt $svc $W/logs/base_plus_new_whole_$svc.log
  mv $T $SC/$TB
  vt $svc $W/logs/base_whole_excl_new_$svc.log
  mv $SC/$TB $T
  git -C $R show pr1957:$REL > $P
  [ "$(sha $P)" = "$H" ] && echo "$svc restore OK" >> $W/logs/suites_restore.log || echo "$svc RESTORE FAIL" >> $W/logs/suites_restore.log
  git -C $R status --short >> $W/logs/suites_restore.log
done
echo done > $W/logs/suites.done
