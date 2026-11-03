#!/bin/bash
# Gate 163: the combined tree (develop df0d1f8e4 + PR 1980 + PR 1979; both orders give the same tree) as a worktree of MY clone,
# node_modules linked; whole referral suite + tsc there, then the principal matrix through the real service (ver=combined).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980
R=$W/repo; D=$R/Blockchain/Dev; REL=Blockchain/Dev/services/referral
C=$(cat $W/logs/combined_commit.txt)
echo "develop moved shared/lockfiles? $(git -C $R diff --name-only 66cbe4e52d5afadc9d13ca141200026cc68d5095 gh/develop -- Blockchain/Dev/packages/shared Blockchain/Dev/package-lock.json Blockchain/Dev/package.json $REL/package.json | wc -l)"
[ -d $W/wt/combined ] || git -C $R worktree add -q --detach $W/wt/combined $C; echo "combined wt $(git -C $W/wt/combined rev-parse HEAD) tree $(git -C $W/wt/combined rev-parse HEAD^{tree})"
T=$W/wt/combined/Blockchain/Dev
[ -e $T/node_modules ] || ln -s $D/node_modules $T/node_modules
[ -e $T/services/referral/node_modules ] || ln -s $D/services/referral/node_modules $T/services/referral/node_modules
[ -e $T/packages/shared/node_modules ] || ln -s $D/packages/shared/node_modules $T/packages/shared/node_modules
[ -e $T/packages/shared/dist ] || ln -s $D/packages/shared/dist $T/packages/shared/dist
G163_ROOT=$W/wt/combined/$REL nice -n 10 node $W/scripts/vt.cjs > $W/logs/combined_whole.log 2>&1; echo "rc=$?" >> $W/logs/combined_whole.log
sed -e 's#\.\./repo/Blockchain/Dev/services#../wt/combined/Blockchain/Dev/services#g' $W/scripts/tsconfig.tests.head.json > $W/scripts/tsconfig.tests.combined.json
nice -n 10 $D/node_modules/.bin/tsc -p $W/scripts/tsconfig.tests.combined.json > $W/logs/tsc_tests_combined.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_combined.log
grep -a -E "Test Files|Tests |rc=" $W/logs/combined_whole.log; echo "tsc combined: $(grep -a -c -i 'error TS' $W/logs/tsc_tests_combined.log) errors $(tail -1 $W/logs/tsc_tests_combined.log)"
