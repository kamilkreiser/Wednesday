#!/bin/bash
# Gate 168 probe matrix, base vs head, one process per cell. Requires the repo on branch gate168 (head tree).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate168-ks1961-pr1985
R=$W/repo; M=$R/Blockchain/Dev/services/api-gateway/src/middleware; L=$W/logs
export HOME=$W/home TMPDIR=$W/tmp
TSX=$R/Blockchain/Dev/node_modules/tsx/dist/loader.mjs
[ "$(git -C $R rev-parse HEAD)" = 1e8c43fcaf6c9c6d42946b43c89e419f9d1f3f18 ] || { echo "tree not at head"; exit 1; }
for f in security rateLimitEnforce; do git -C $R show gh/develop:Blockchain/Dev/services/api-gateway/src/middleware/$f.ts > $M/$f.g168base.ts; done
OUT=${1:-$L/probe.jsonl}; : > $OUT; : > $L/probe.rc
run(){ for var in base head; do node --require $R/Blockchain/Dev/node_modules/tsx/dist/cjs/index.cjs $W/scripts/probe.ts $var "$1" "$2" >> $OUT 2>>$L/probe.err; echo "rc=$? $var $1 $2" >> $L/probe.rc; done; }
for v in none ordinary secretError secretString revokedProxy getterThrows secretObject hang; do run bf_fault $v; done
for v in corrupt five arr soonStr attemptsStr blockedNoAttempts blockedNumStr blockedNull nullStr strRec clean proto; do run bf_record $v; done
for v in none ordinary secretError revokedProxy hang; do run bf_lockout $v; done
run bf_429throw none
for v in none ordinary secretError secretString revokedProxy getterThrows secretObject; do run rl_hdr $v; done
run rl_429write x; run rl_committed x
for v in secretError secretString; do run rl_fallback $v; done
for v in ordinary secretString revokedProxy; do run rl_degrade $v; done
run rl_notconnected x; run rl_success x
for v in 1 3 NL1 1.5 0.5 0 -1 99.5 NaN Infinity negInfinity str100 str5 str99 str1e3 obj true arr5 empty missing null pow53 1e15 100 101; do run rl_value $v; done
for v in 60 1 3600 1.5 0.5 0 -1 -60 NaN Infinity str120 str30 obj 120.5 1e300 NL1 missing; do run rl_window "3~$v~8"; run rl_window_mem "3~$v~8"; done
for f in security rateLimitEnforce; do mkdir -p $W/mut/quarantine; mv $M/$f.g168base.ts $W/mut/quarantine/; done
git -C $R status --short > $L/probe_status_after.log
echo done > $L/probe.done
