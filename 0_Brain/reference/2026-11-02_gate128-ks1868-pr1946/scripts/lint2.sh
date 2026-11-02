#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
D=$W/repo/Blockchain/Dev
test -e $D/node_modules || ln -s $W/eslint_tools/node_modules $D/node_modules
S=services/originate/src
run(){ (cd $D && $D/node_modules/.bin/eslint "$@" > $W/logs/eslint_$TAG.log 2>&1; echo "[$TAG] eslint rc=$?"); tail -6 $W/logs/eslint_$TAG.log; }
TAG=head2; run $S/services/retentionScheduler.ts $S/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts
printf 'debugger;\nconst unusedPlanted = 1;\n' > $D/$S/__tests__/zz_planted_g128.test.ts
TAG=planted2; run $S/__tests__/zz_planted_g128.test.ts
mkdir -p $W/logs/_quarantine; mv $D/$S/__tests__/zz_planted_g128.test.ts $W/logs/_quarantine/
git -C $W/repo status --short | head -3
