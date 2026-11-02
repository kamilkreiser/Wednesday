#!/bin/bash
# kyc + wallet-connector (vitest, --root anchored, cwd = logs/child_cwd): head new file; head whole; base product + new file (red first); base whole without the new file. sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate147-ks1868-pr1963
R=$W/repo; D=$R/Blockchain/Dev; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf; Q=$W/logs/_quarantine/suites
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
vt(){ log=$1; shift; nice -n 10 node $W/scripts/vt.js "$@" > $log 2>&1; echo "rc=$?" >> $log; }
for s in kyc wallet-connector; do
  S=$D/services/$s; P=$S/src/userErasedSubscriber.ts; T=src/__tests__/ks1868-$s-user-erased-handler-failed-catch-unreadable-throw.test.ts
  HP=$(sha $P); HT=$(sha $S/$T)
  vt $W/logs/${s}_head_new.log $s $T
  vt $W/logs/${s}_head_whole.log $s
  git -C $R show $MB:Blockchain/Dev/services/$s/src/userErasedSubscriber.ts > $P
  vt $W/logs/${s}_red_base_new.log $s $T
  mv $S/$T $Q/
  vt $W/logs/${s}_base_whole_excl_new.log $s
  mv $Q/$(basename $T) $S/$T
  git -C $R show pr1963:Blockchain/Dev/services/$s/src/userErasedSubscriber.ts > $P
  { [ "$(sha $P)" = "$HP" ] && [ "$(sha $S/$T)" = "$HT" ] && echo "$s restore OK" || echo "$s RESTORE FAIL"; } >> $W/logs/suites_restore.log
done
git -C $R status --short >> $W/logs/suites_restore.log
echo done > $W/logs/suites.done
