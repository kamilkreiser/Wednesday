#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
S=$W/repo/Blockchain/Dev/services/originate; PF=$S/src/services/retentionScheduler.ts
SAVE=$(shasum -a 256 $PF|cut -d' ' -f1)
git -C $W/repo show e2a2426d221d:Blockchain/Dev/services/originate/src/services/retentionScheduler.ts > $PF
$S/node_modules/.bin/tsc -p $W/tsconfig.g128.json > $W/logs/tsc_tests_base.log 2>&1; echo base tsc rc=$? errors=$(/usr/bin/grep -c 'error TS' $W/logs/tsc_tests_base.log)
git -C $W/repo checkout -q -- Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
echo restore=$([ "$(shasum -a 256 $PF|cut -d' ' -f1)" = "$SAVE" ] && echo OK || echo BAD)
echo 'export const g128planted: number = "x";' > $S/src/zz_planted.ts
$S/node_modules/.bin/tsc -p $W/tsconfig.g128.json > $W/logs/tsc_planted.log 2>&1; echo planted tsc rc=$? errors=$(/usr/bin/grep -c 'error TS' $W/logs/tsc_planted.log)
mkdir -p $W/logs/_quarantine; mv $S/src/zz_planted.ts $W/logs/_quarantine/zz_planted.ts
E=$W/eslint_tools
printf 'debugger;\nvar a = 1;\n' > $S/src/zz_planted_lint.ts
(cd $E && $E/node_modules/.bin/eslint --config $E/eslint.config.mjs --no-warn-ignored $S/src/zz_planted_lint.ts > $W/logs/eslint_planted.log 2>&1; echo planted eslint rc=$?); tail -4 $W/logs/eslint_planted.log
mv $S/src/zz_planted_lint.ts $W/logs/_quarantine/zz_planted_lint.ts
T=$(git -C $W/repo merge-tree --write-tree pr1946 origin/develop)
echo tree=$T
git -C $W/repo diff --name-only origin/develop $T | tee $W/logs/mt_changed.log
git -C $W/repo status --short | head
git -C $W/repo ls-remote origin refs/heads/develop refs/pull/1946/head | tee $W/logs/head_end.log; date -u >> $W/logs/head_end.log
ps -axo pid,command | /usr/bin/grep -i "gate128" | /usr/bin/grep -v grep | head
