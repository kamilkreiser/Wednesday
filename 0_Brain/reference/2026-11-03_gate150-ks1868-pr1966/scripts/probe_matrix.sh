#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate150-ks1868-pr1966
R=$W/repo; D=$R/Blockchain/Dev; T=$D/node_modules/.bin/tsx
for s in prism timestamping security; do git -C $R show 4d1ab2cb:Blockchain/Dev/services/$s/src/db.ts > $D/services/$s/src/db_base.ts; done
OUT=$W/logs/probe_matrix.jsonl; : > $OUT; : > $W/logs/probe_matrix.rc
CASES="ordinary revokedProxy getterThrows msg42 msgUndefined msgNull msgSymbol msgObjToStringThrows msgObjToString nullValue undefinedValue plainString"
for svc in prism timestamping security; do
 sites="pool hook_boot hook_retry"; [ $svc = timestamping ] && sites="pool"
 for site in $sites; do for var in base head; do for c in $CASES; do
  $T $W/scripts/probe_child.ts $svc $var $site $c >> $OUT 2>>$W/logs/probe_matrix.err; echo "rc=$? $svc $var $site $c" >> $W/logs/probe_matrix.rc
 done; done; done
done
for s in prism timestamping security; do mv $D/services/$s/src/db_base.ts $W/logs/_quarantine/db_base_$s.ts; done
echo done > $W/logs/probe_matrix.done
