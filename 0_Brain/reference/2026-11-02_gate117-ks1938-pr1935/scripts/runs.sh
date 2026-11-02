#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate117-ks1938-pr1935; R=$G/repo
P=Blockchain/Dev/services/originate/src/services/gdprService.ts
T=Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts
bash $G/scripts/run.sh $G/logs/green_head --runTestsByPath $R/$T; echo "green rc=$?"
for i in 2 3; do bash $G/scripts/run.sh $G/logs/green_head_$i --runTestsByPath $R/$T; echo "green$i rc=$?"; done
bash $G/scripts/run.sh $G/logs/suite_head; echo "suite head rc=$?"
node $G/scripts/tsc_lint.js head
git -C $R show 8f313815:$P > $R/$P
bash $G/scripts/run.sh $G/logs/red_base --runTestsByPath $R/$T; echo "red rc=$?"
mkdir -p $G/logs/_parked; mv $R/$T $G/logs/_parked/
bash $G/scripts/run.sh $G/logs/suite_base; echo "suite base rc=$?"
node $G/scripts/tsc_lint.js base
mv $G/logs/_parked/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts $R/$T
git -C $R checkout pr1935 -- $P
for f in $P $T; do [ "$(git -C $R hash-object $R/$f)" = "$(git -C $R rev-parse pr1935:$f)" ] && echo "SHA_OK $f" || echo "SHA_BAD $f"; done
echo "status: [$(git -C $R status --short | tr '\n' ' ')]"
