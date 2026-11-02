#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932; R=$G/repo
PA=Blockchain/Dev/services/anchoring/src/index.ts; PO=Blockchain/Dev/services/originate/src/routes/anchors.ts
TA=Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts
TO=Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts
git -C $R show cd9c4a7dd3b8:$PA > $R/$PA; git -C $R show cd9c4a7dd3b8:$PO > $R/$PO
mkdir -p $G/logs/_parked; mv $R/$TA $R/$TO $G/logs/_parked/
node $G/scripts/tsc_lint.js base
mv $G/logs/_parked/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts $R/$TA; mv $G/logs/_parked/ks1868-anchors-route-catches-unreadable-throw.test.ts $R/$TO
git -C $R checkout pr/1932 -- $PA $PO
for f in $PA $PO $TA $TO; do [ "$(git -C $R hash-object $R/$f)" = "$(git -C $R rev-parse pr/1932:$f)" ] && echo "SHA_OK $f" || echo "SHA_BAD $f"; done
echo "status: [$(git -C $R status --short | tr '\n' ' ')]"
