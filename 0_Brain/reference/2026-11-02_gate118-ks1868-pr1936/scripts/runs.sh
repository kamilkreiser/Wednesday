#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate118-ks1868-pr1936; R=$G/repo
S=Blockchain/Dev/services/originate/src
P1=$S/routes/signatories.ts; P2=$S/routes/thirdPartyVerifiers.ts
T1=$S/__tests__/ks1868-signatories-nominate-catch-o77p2-unreadable-throw.test.ts
T2=$S/__tests__/ks1868-third-party-verifiers-register-approve-catches-o77p3-unreadable-throw.test.ts
for i in 1 2 3; do bash $G/scripts/run.sh $G/logs/green_head_$i --runTestsByPath $R/$T1 $R/$T2; echo "green$i rc=$?"; done
bash $G/scripts/run.sh $G/logs/suite_head; echo "suite head rc=$?"
node $G/scripts/tsc_lint.js head
git -C $R show 8f313815:$P1 > $R/$P1; git -C $R show 8f313815:$P2 > $R/$P2
bash $G/scripts/run.sh $G/logs/red_base --runTestsByPath $R/$T1 $R/$T2; echo "red rc=$?"
mkdir -p $G/logs/_parked; mv $R/$T1 $R/$T2 $G/logs/_parked/
bash $G/scripts/run.sh $G/logs/suite_base; echo "suite base rc=$?"
node $G/scripts/tsc_lint.js base
mv $G/logs/_parked/$(basename $T1) $R/$T1; mv $G/logs/_parked/$(basename $T2) $R/$T2
git -C $R checkout pr1936 -- $P1 $P2
for f in $P1 $P2 $T1 $T2; do [ "$(git -C $R hash-object $R/$f)" = "$(git -C $R rev-parse pr1936:$f)" ] && echo "SHA_OK $f" || echo "SHA_BAD $f"; done
echo "status: [$(git -C $R status --short | tr '\n' ' ')]"
