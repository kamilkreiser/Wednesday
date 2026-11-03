#!/bin/bash
# Gate 168: timed cells (rate over time). rateLimit 3, burst 4, wait 62 s, burst 4. Run in parallel, one process per cell.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985
R=$W/repo; M=$R/Blockchain/Dev/services/api-gateway/src/middleware; L=$W/logs
export HOME=$W/home TMPDIR=$W/tmp
[ "$(git -C $R rev-parse HEAD)" = 1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18 ] || { echo "tree not at head"; exit 1; }
for f in security rateLimitEnforce; do git -C $R show gh/develop:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.g168base.ts; done
: > $L/probe_time.jsonl
for v in 60 str120 120.5 Infinity obj 1e300; do for var in base head; do
  node --require $R/Blockchain/Dev/node_modules/tsx/dist/cjs/index.cjs $W/scripts/probe.ts $var rl_time "3~$v~4~62" > $L/time_${var}_$v.out 2>>$L/probe_time.err &
done; done
wait
cat $L/time_*.out >> $L/probe_time.jsonl
for f in security rateLimitEnforce; do mv -f $M/$f.g168base.ts $W/mut/quarantine/; done
git -C $R status --short > $L/probe_time_status_after.log
echo done > $L/probe_time.done
