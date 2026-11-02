#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958
Dev=$W/repo/Blockchain/Dev; A=$Dev/services/anchoring; S=$A/src
V=$Dev/node_modules/.bin/vitest
P1=$S/anchorStatusUpdate.ts; P2=$S/cardano/confirmation.ts
H1=$(shasum -a 256 $P1|cut -d' ' -f1); H2=$(shasum -a 256 $P2|cut -d' ' -f1)
T1=src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts
T2=src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts
restore(){ cp $S/anchorStatusUpdate_head.keep $P1; cp $S/cardano/confirmation_head.keep $P2
 [ "$(shasum -a 256 $P1|cut -d' ' -f1)" = $H1 ] && [ "$(shasum -a 256 $P2|cut -d' ' -f1)" = $H2 ] && echo "restore True" || echo "restore FALSE"; }
cp $P1 $S/anchorStatusUpdate_head.keep; cp $P2 $S/cardano/confirmation_head.keep
echo "== head new files"; $V run --root $A $T1 $T2 > $W/logs/head_new.log 2>&1; echo rc=$?
echo "== head whole"; $V run --root $A > $W/logs/head_whole.log 2>&1; echo rc=$?
cp $S/anchorStatusUpdate_base.ts $P1; cp $S/cardano/confirmation_base.ts $P2
echo "== base product, new files (red first)"; $V run --root $A $T1 $T2 > $W/logs/red_base_new.log 2>&1; echo rc=$?
echo "== base product, whole minus new files"; $V run --root $A --exclude '**/ks1868-anchor-status-update-catch-unreadable-throw.test.ts' --exclude '**/ks1868-confirmation-wait-catch-unreadable-throw.test.ts' --exclude '**/node_modules/**' > $W/logs/base_whole.log 2>&1; echo rc=$?
restore
echo done > $W/logs/suites.done
