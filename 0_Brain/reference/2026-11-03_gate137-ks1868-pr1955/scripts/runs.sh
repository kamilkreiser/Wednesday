#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955
R=$G/repo; BASE=9a9bf86967e31166ed4aba863e4c1fc4b763bfe8
PA=Blockchain/Dev/services/anchoring/src/index.ts; PO=Blockchain/Dev/services/originate/src/routes/anchors.ts
TA=Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-message-coercion-unreadable-throw.test.ts
TO=Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts
# head: new tests + whole suites
bash $G/scripts/run.sh anchoring $G/logs/green_head_anchoring src/__tests__/ks1868-anchoring-message-coercion-unreadable-throw.test.ts
bash $G/scripts/run.sh originate $G/logs/green_head_originate --runTestsByPath $R/$TO
bash $G/scripts/run.sh anchoring $G/logs/suite_head_anchoring
bash $G/scripts/run.sh originate $G/logs/suite_head_originate
# base product
git -C $R show $BASE:$PA > $R/$PA; git -C $R show $BASE:$PO > $R/$PO
echo "base product in place: $(git -C $R status --short | tr '\n' ' ')"
bash $G/scripts/run.sh anchoring $G/logs/red_base_anchoring src/__tests__/ks1868-anchoring-message-coercion-unreadable-throw.test.ts
bash $G/scripts/run.sh originate $G/logs/red_base_originate --runTestsByPath $R/$TO
mkdir -p $G/logs/_parked; mv $R/$TA $R/$TO $G/logs/_parked/
bash $G/scripts/run.sh anchoring $G/logs/suite_base_anchoring
bash $G/scripts/run.sh originate $G/logs/suite_base_originate
mv $G/logs/_parked/ks1868-anchoring-message-coercion-unreadable-throw.test.ts $R/$TA
mv $G/logs/_parked/ks1868-anchors-message-coercion-unreadable-throw.test.ts $R/$TO
git -C $R checkout gate137 -- $PA $PO
echo "restored: status=[$(git -C $R status --short | tr '\n' ' ')]"
for f in $PA $PO $TA $TO; do [ "$(git -C $R hash-object $R/$f)" = "$(git -C $R rev-parse pr/1955:$f)" ] && echo "SHA_OK $f" || echo "SHA_BAD $f"; done
date -u > $G/logs/runs.done
