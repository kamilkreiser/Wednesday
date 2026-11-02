#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958
T=$W/repo/Blockchain/Dev/node_modules/.bin/tsx
OUT=$W/logs/probe_matrix.jsonl; : > $OUT; : > $W/logs/probe_matrix.err; : > $W/logs/probe_matrix.rc
CASES="msgBigInt msgCyclic ordinary revokedProxy getterThrows msg42 msgUndefined msgNull msgSymbol msgObjToStringThrows msgObjToString nullValue undefinedValue plainString"
for site in status conf_recover conf_always conf_nocb; do for var in base head; do for c in $CASES; do
 $T $W/scripts/probe_child.ts $site $var $c >> $OUT 2>>$W/logs/probe_matrix.err; echo "rc=$? $site $var $c" >> $W/logs/probe_matrix.rc
done; done; done
echo done > $W/logs/probe_matrix.done
