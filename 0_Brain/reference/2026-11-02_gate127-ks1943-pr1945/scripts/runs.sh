#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945; R=$W/repo; L=$W/logs
A=$R/Blockchain/Dev/services/originate/src/__tests__
T1=$A/ks1943-retention-sweep-unit-all-or-nothing.test.ts; T2=$A/ks1943-platform-scope-transaction-helper.test.ts; T3=$A/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts
bash $W/scripts/swap.sh head || exit 9
for i in 1 2 3; do bash $W/scripts/run.sh $L/green_head_$i --runTestsByPath $T1 $T2 $T3; echo "green$i rc=$?"; done
bash $W/scripts/run.sh $L/suite_head; echo "suite head rc=$?"
bash $W/scripts/swap.sh base || exit 9
bash $W/scripts/run.sh $L/red_base_sweep --runTestsByPath $T1; echo "red sweep rc=$?"
bash $W/scripts/run.sh $L/red_base_helper --runTestsByPath $T2; echo "red helper rc=$?"
bash $W/scripts/run.sh $L/base_ks1938_headtest --runTestsByPath $T3; echo "ks1938 test (head version) on base product rc=$?"
mkdir -p $L/_parked; mv $T1 $T2 $L/_parked/
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/repo show 0e3a9b65cdd6:Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts > $T3
bash $W/scripts/run.sh $L/suite_base; echo "suite base rc=$?"
mv $L/_parked/ks1943-retention-sweep-unit-all-or-nothing.test.ts $L/_parked/ks1943-platform-scope-transaction-helper.test.ts $A/
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/repo show pr1945:Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts > $T3
bash $W/scripts/swap.sh head
for f in $T1 $T2 $T3; do rel=${f#$R/}; [ "$(git -C $R hash-object $f)" = "$(git -C $R rev-parse pr1945:$rel)" ] && echo "SHA_OK $rel" || echo "SHA_BAD $rel"; done
echo "status: [$(git -C $R status --short | tr '\n' ' ')]"
