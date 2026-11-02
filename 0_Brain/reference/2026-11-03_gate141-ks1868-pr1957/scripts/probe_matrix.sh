#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957
T=$W/repo/Blockchain/Dev/node_modules/.bin/tsx
OUT=$W/logs/probe_matrix.jsonl; : > $OUT
CASES="ordinary revokedProxy getterThrows msg42 msgUndefined msgNull msgSymbol msgObjToStringThrows msgObjToString nullValue undefinedValue plainString"
for svc in nft-certificate transfer wallet-connector m365-integration staking; do
 sites="pool"; sites="pool hook_boot hook_retry"
 for site in $sites; do for var in base head; do for c in $CASES; do
  $T $W/scripts/probe_child.ts $svc $var $site $c >> $OUT 2>>$W/logs/probe_matrix.err; echo "rc=$? $svc $var $site $c" >> $W/logs/probe_matrix.rc
 done; done; done
done
echo done > $W/logs/probe_matrix.done
