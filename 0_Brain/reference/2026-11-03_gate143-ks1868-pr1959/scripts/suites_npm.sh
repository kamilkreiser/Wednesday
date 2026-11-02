#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959
A=$W/repo/Blockchain/Dev/services/auth; V=$W/repo/Blockchain/Dev/node_modules/.bin/vitest
T=$A/src/__tests__; Q=$W/logs/_quarantine; mkdir -p $Q
SHA=$(shasum -a 256 $A/src/events.ts | cut -d' ' -f1)
nice -n 5 npm --prefix $A test -- --run > $W/logs/suite_head_run1.log 2>&1; echo head1 rc=$? > $W/logs/suite_head_run1.rc
nice -n 5 npm --prefix $A test -- --run > $W/logs/suite_head_run2.log 2>&1; echo head2 rc=$? > $W/logs/suite_head_run2.rc
cp $A/src/events.ts $Q/events_head.ts
cp $A/src/events_base.ts $A/src/events.ts
mv $T/ks1868-auth-events-init-catch-unreadable-throw.test.ts $T/ks1868-auth-events-redis-error-listener-unreadable-throw.test.ts $Q/
nice -n 5 npm --prefix $A test -- --run > $W/logs/suite_base_run1.log 2>&1; echo base1 rc=$? > $W/logs/suite_base_run1.rc
cp $Q/events_head.ts $A/src/events.ts
mv $Q/ks1868-auth-events-init-catch-unreadable-throw.test.ts $Q/ks1868-auth-events-redis-error-listener-unreadable-throw.test.ts $T/
[ "$(shasum -a 256 $A/src/events.ts | cut -d' ' -f1)" = "$SHA" ] && echo restored-ok > $W/logs/suite_restore.ok
echo done > $W/logs/suites.done
