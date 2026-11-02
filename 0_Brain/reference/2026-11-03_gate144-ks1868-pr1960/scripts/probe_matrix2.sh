#!/bin/bash
# second pass: prod arm with JSON logs kept whole; listener emitted from an async callback (uncaught path); enforcement family
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; SRC=$R/Blockchain/Dev/services/api-gateway/src
T=$R/Blockchain/Dev/node_modules/.bin/tsx
git -C $R show 2d3b3bb3:Blockchain/Dev/services/api-gateway/src/services/redis.ts > $SRC/services/redis.gate_base.ts
OUT=$W/logs/probe_site2.jsonl; : > $OUT; : > $W/logs/probe2.rc
CASES="ordinary revokedProxy getterThrows msg42 msgNull msgUndefinedObj msgSymbol msgObjToStringThrows nullValue undefinedValue plainString"
for site in connect_prod listener_async; do for var in base head; do for c in $CASES; do
  $T $W/scripts/probe_child.ts site $var $site $c >> $OUT 2>>$W/logs/probe2.err; echo "rc=$? site $var $site $c" >> $W/logs/probe2.rc
done; done; done
OUT2=$W/logs/probe_enforce.jsonl; : > $OUT2
for var in base head; do for trig in none ordinary revokedProxy; do for down in 0 1; do
  $T $W/scripts/probe_child.ts enforce $var $trig $down >> $OUT2 2>>$W/logs/probe2.err; echo "rc=$? enforce $var $trig $down" >> $W/logs/probe2.rc
done; done; done
mv $SRC/services/redis.gate_base.ts $W/logs/_quarantine/redis.gate_base.2.ts
git -C $R status --short > $W/logs/probe2_status_after.log
echo done > $W/logs/probe2.done
