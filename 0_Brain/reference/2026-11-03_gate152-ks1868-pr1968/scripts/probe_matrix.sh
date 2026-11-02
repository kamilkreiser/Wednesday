#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968
R=$W/repo; D=$R/Blockchain/Dev; T=$D/node_modules/.bin/tsx; S=$D/services/vc-issuer
git -C $R show 2f9f7db313b3:Blockchain/Dev/services/vc-issuer/src/db.ts > $S/src/db_base.ts
OUT=$W/logs/probe_matrix.jsonl; : > $OUT; : > $W/logs/probe_matrix.rc; : > $W/logs/probe_matrix.err
CASES="ordinary revokedProxy getterThrows msg42 msgUndefined msgNull msgSymbol msgObjToStringThrows msgObjToString nullValue undefinedValue plainString"
for site in pool hook_boot hook_retry; do for var in base head; do for c in $CASES; do
  $T $W/scripts/probe_child.ts $var $site $c >> $OUT 2>>$W/logs/probe_matrix.err; echo "rc=$? $var $site $c" >> $W/logs/probe_matrix.rc
done; done; done
mv $S/src/db_base.ts $W/logs/_quarantine/db_base_vc-issuer.ts
echo done > $W/logs/probe_matrix.done
