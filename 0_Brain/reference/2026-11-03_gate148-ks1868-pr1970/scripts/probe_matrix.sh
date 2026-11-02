#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970
R=$W/repo; M=$R/Blockchain/Dev/services/api-gateway/src/middleware
T=$R/Blockchain/Dev/node_modules/.bin/tsx
for f in security rateLimitEnforce audit; do git -C $R show 4d1ab2cb:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.gate_base.ts; done
OUT=$W/logs/probe.jsonl; : > $OUT; : > $W/logs/probe.rc; : > $W/logs/probe.err
VALS="none ordinary plainString revokedProxy getterThrows msgNullProto msgSymbol"
for var in base head; do
  for cell in bf rl_redis rl_hdr audit; do for v in $VALS; do
    $T $W/scripts/probe_child.ts $var $cell $v >> $OUT 2>>$W/logs/probe.err; echo "rc=$? $var $cell $v" >> $W/logs/probe.rc
  done; done
  for cell in bf_arm rl_hdr_committed rl_hdr_badmeta; do $T $W/scripts/probe_child.ts $var $cell none >> $OUT 2>>$W/logs/probe.err; echo "rc=$? $var $cell none" >> $W/logs/probe.rc; done
  for cell in bf rl_hdr audit rl_redis; do for v in ordinary revokedProxy; do $T $W/scripts/probe_child.ts $var $cell $v production >> $OUT 2>>$W/logs/probe.err; echo "rc=$? $var $cell $v production" >> $W/logs/probe.rc; done; done
done
mkdir -p $W/logs/_quarantine; for f in security rateLimitEnforce audit; do mv $M/$f.gate_base.ts $W/logs/_quarantine/; done
git -C $R status --short > $W/logs/probe_status_after.log
echo done > $W/logs/probe.done
