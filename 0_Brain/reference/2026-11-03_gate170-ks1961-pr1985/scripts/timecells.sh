#!/bin/bash
# Gate 170 timed cells: two bursts 62 s apart, dev / r1 / head, all in parallel, one process per cell.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985
R=$W/repo; M=$R/Blockchain/Dev/services/api-gateway/src/middleware; L=$W/logs; O=$W/runs/time
export HOME=$W/home TMPDIR=$W/tmp
[ "$(git -C $R rev-parse HEAD)" = a0a91f65d0006d1adc69325002e6ddf69abffc2b ] || { echo "tree not at head"; exit 1; }
for f in security rateLimitEnforce; do
  git -C $R show ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.g170dev.ts
  git -C $R show 1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.g170r1.ts
done
mkdir -p $O; : > $L/probe_time.pids
n=0
for v in 3~60~4~62 3~str120~4~62 3~120.5~4~62 3~Infinity~4~62 3~obj~4~62 3~1e300~4~62 3~str30~4~62 3~1.5~4~62 3~-1~4~62 3~missing~4~62 3~0~4~62 \
         str5~60~8~62 1.5~60~8~62 true~60~8~62 arr5~60~8~62 str99~60~8~62 missing~60~8~62; do
  for var in dev r1 head; do n=$((n+1))
    node --require $R/Blockchain/Dev/node_modules/tsx/dist/cjs/index.cjs $W/scripts/probe.ts $var rl_time "$v" > $O/$n.out 2> $O/$n.err &
    echo "$! $var $v" >> $L/probe_time.pids
  done
done
wait
for i in $(seq 1 $n); do cat $O/$i.out; done > $L/probe_time.jsonl
for f in security rateLimitEnforce; do mv -f $M/$f.g170dev.ts $M/$f.g170r1.ts $W/mut/quarantine/; done
git -C $R status --short > $L/probe_time_status_after.log
echo done > $L/probe_time.done
