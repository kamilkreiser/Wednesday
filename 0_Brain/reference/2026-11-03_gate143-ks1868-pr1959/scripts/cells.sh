#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959
A=$W/repo/Blockchain/Dev/services/auth; V=$W/repo/Blockchain/Dev/node_modules/.bin/vitest
F1=src/__tests__/ks1868-auth-events-init-catch-unreadable-throw.test.ts
F2=src/__tests__/ks1868-auth-events-redis-error-listener-unreadable-throw.test.ts
SHA=$(shasum -a 256 $A/src/events.ts | cut -d' ' -f1); echo head sha $SHA
$V run --root $A $F1 $F2 > $W/logs/cells_head.log 2>&1; echo head rc=$?
cp $A/src/events.ts $W/logs/events_head.ts.bak
cp $A/src/events_base.ts $A/src/events.ts
$V run --root $A $F1 $F2 > $W/logs/cells_base.log 2>&1; echo base rc=$?
cp $W/logs/events_head.ts.bak $A/src/events.ts
[ "$(shasum -a 256 $A/src/events.ts | cut -d' ' -f1)" = "$SHA" ] && echo restored-ok
