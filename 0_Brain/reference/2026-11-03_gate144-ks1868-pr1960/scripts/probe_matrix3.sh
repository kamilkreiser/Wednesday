#!/bin/bash
# third pass (harness fixes): listener_async without a failing connect; enforce with keys()/pipeline() in the stand-in
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960
R=$W/repo; SRC=$R/Blockchain/Dev/services/api-gateway/src
T=$R/Blockchain/Dev/node_modules/.bin/tsx
git -C $R show 2d3b3bb3:Blockchain/Dev/services/api-gateway/src/services/redis.ts > $SRC/services/redis.gate_base.ts
OUT=$W/logs/probe_site3.jsonl; : > $OUT; : > $W/logs/probe3.rc
CASES="ordinary revokedProxy getterThrows msg42 msgNull msgUndefinedObj msgSymbol msgObjToStringThrows nullValue undefinedValue plainString"
for var in base head; do for c in $CASES; do
  $T $W/scripts/probe_child.ts site $var listener_async $c >> $OUT 2>>$W/logs/probe3.err; echo "rc=$? site $var listener_async $c" >> $W/logs/probe3.rc
done; done
OUT2=$W/logs/probe_enforce3.jsonl; : > $OUT2
for var in base head; do for trig in none ordinary revokedProxy getterThrows; do for down in 0 1; do
  $T $W/scripts/probe_child.ts enforce $var $trig $down >> $OUT2 2>>$W/logs/probe3.err; echo "rc=$? enforce $var $trig $down" >> $W/logs/probe3.rc
done; done; done
mv $SRC/services/redis.gate_base.ts $W/logs/_quarantine/redis.gate_base.3.ts
git -C $R status --short > $W/logs/probe3_status_after.log
echo done > $W/logs/probe3.done
