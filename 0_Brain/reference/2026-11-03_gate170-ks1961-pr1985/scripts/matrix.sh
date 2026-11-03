#!/bin/bash
# Gate 170 probe matrix: dev (ca2b2aa) / r1 (1e8c43fc) / head (a0a91f65), one process per cell, 6 in parallel.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985
R=$W/repo; M=$R/Blockchain/Dev/services/api-gateway/src/middleware; L=$W/logs; O=$W/runs/cells
export HOME=$W/home TMPDIR=$W/tmp
[ "$(git -C $R rev-parse HEAD)" = a0a91f65d0006d1adc69325002e6ddf69abffc2b ] || { echo "tree not at head"; exit 1; }
for f in security rateLimitEnforce; do
  git -C $R show ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.g170dev.ts
  git -C $R show 1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.g170r1.ts
done
mkdir -p $O; : > $W/runs/cells.list
add(){ for var in dev r1 head; do echo "$var $1 $2" >> $W/runs/cells.list; done; }
V="1 3 100 101 NL1 1.5 0.5 -1 99.5 Infinity negInfinity str100 str500 str5 str99 str1e3 str120 str0 strSp5 strHex strAbc strSpace obj true arr5 arr pow53 1e15 1e300 big5 numObj5 valueOf5 date"
F="0 NaN false empty missing null negZero big0"
for v in $V $F; do add rl_value "$v~60~105"; done
for v in $F str5 1.5 -1 true NL1 3; do add rl_value_mem "$v~60~105"; done
WV="60 1 3600 1.5 0.5 -1 -60 Infinity negInfinity str120 str30 str5 str0 obj arr arr5 true 120.5 1e300 NL1 big5 numObj5"
WF="0 NaN false empty null missing negZero"
for v in $WV $WF; do add rl_window "3~$v~8"; add rl_window_mem "3~$v~8"; done
for v in ordinary secretError secretString secretObject revokedProxy getterThrows; do add rl_degrade "3~60~6~$v"; done
for v in "100~str5~200" "100~-1~200" "100~1.5~200" "100~true~200" "3~str5~12" "100~str500~400" "100~missing~200" "100~0~200"; do add rl_mixed "$v"; done
for v in none hdrError hdrString hdrObject hdrRevoked jsonThrows statusThrows committed logThrows logThrowsAll; do add bf_429throw $v; done
for v in none ordinary secretError hang; do add bf_lockout $v; add bf_fault $v; done
n=0; while read var cell val; do n=$((n+1)); echo "$n $var $cell $val"; done < $W/runs/cells.list > $W/runs/cells.numbered
cat $W/runs/cells.numbered | xargs -P 6 -L 1 bash -c 'node --require '$R'/Blockchain/Dev/node_modules/tsx/dist/cjs/index.cjs '$W'/scripts/probe.ts "$1" "$2" "$3" > '$O'/$0.out 2> '$O'/$0.err; echo "rc=$? $0 $1 $2 $3" >> '$L'/probe.rc'
for i in $(seq 1 $n); do cat $O/$i.out; done > $L/probe.jsonl
mkdir -p $W/mut/quarantine; for f in security rateLimitEnforce; do mv -f $M/$f.g170dev.ts $M/$f.g170r1.ts $W/mut/quarantine/; done
git -C $R status --short > $L/probe_status_after.log
echo done > $L/probe.done
