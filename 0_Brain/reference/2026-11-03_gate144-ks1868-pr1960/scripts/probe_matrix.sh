#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; SRC=$R/Blockchain/Dev/services/api-gateway/src
T=$R/Blockchain/Dev/node_modules/.bin/tsx
git -C $R show 2d3b3bb3:Blockchain/Dev/services/api-gateway/src/services/redis.ts > $SRC/services/redis.gate_base.ts
OUT=$W/logs/probe_site.jsonl; : > $OUT; : > $W/logs/probe.rc
CASES="ordinary revokedProxy getterThrows msg42 msgNull msgUndefinedObj msgSymbol msgObjToStringThrows nullValue undefinedValue plainString"
for site in listener connect_dev connect_prod; do for var in base head; do for c in $CASES; do
  $T $W/scripts/probe_child.ts site $var $site $c >> $OUT 2>>$W/logs/probe.err; echo "rc=$? site $var $site $c" >> $W/logs/probe.rc
done; done; done
OUT2=$W/logs/probe_family.jsonl; : > $OUT2
for var in base head; do for trig in none ordinary revokedProxy getterThrows; do for down in 0 1; do
  $T $W/scripts/probe_child.ts family $var $trig $down >> $OUT2 2>>$W/logs/probe.err; echo "rc=$? family $var $trig $down" >> $W/logs/probe.rc
done; done; done
mkdir -p $W/logs/_quarantine; mv $SRC/services/redis.gate_base.ts $W/logs/_quarantine/
git -C $R status --short > $W/logs/probe_status_after.log
echo done > $W/logs/probe.done
