#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957
R=$W/repo; D=$R/Blockchain/Dev; SC=$W/logs/_quarantine
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
for s in nft-certificate transfer wallet-connector m365-integration staking; do
  P=$D/services/$s/src/db.ts; H=$(sha $P)
  T=$(ls $D/services/$s/src/__tests__/ks1868-$s-db-pool*.test.ts)
  git -C $R show origin/develop:Blockchain/Dev/services/$s/src/db.ts > $P
  mv $T $SC/$(basename $T).tmp
  nice -n 10 $D/node_modules/.bin/tsc -p $D/services/$s/tsconfig.gate.json > $W/logs/tsc_base_$s.log 2>&1; echo "rc=$?" >> $W/logs/tsc_base_$s.log
  mv $SC/$(basename $T).tmp $T
  git -C $R show pr1957:Blockchain/Dev/services/$s/src/db.ts > $P
  [ "$(sha $P)" = "$H" ] && r=OK || r=FAIL
  echo "base $s: $(grep -c 'error TS' $W/logs/tsc_base_$s.log) errors; $(tail -1 $W/logs/tsc_base_$s.log); restore $r"
done
