#!/bin/bash
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1521r1
D=$W/head/Blockchain/Dev; F=$D/services/security/src/index.ts
cp $F $W/index.ts.bak; B=$(shasum -a 256 $F | cut -c1-16)
printf '\nconst __gateCtl: number = "x"; var __gateUnused = 1;\n' >> $F
grep -c __gateCtl $F
(cd $D/services/security && npx tsc --noEmit -p tsconfig.json) > $W/out/tsc-ctl.log 2>&1; echo "tsc CONTROL rc=$? $(grep -c 'error TS' $W/out/tsc-ctl.log) errors"
(cd $D && npx eslint services/security/src/index.ts) > $W/out/eslint-ctl.log 2>&1; echo "eslint CONTROL rc=$? $(grep -cE 'error|warning' $W/out/eslint-ctl.log) lines"
cp $W/index.ts.bak $F; echo "restored $( [ "$(shasum -a 256 $F | cut -c1-16)" = "$B" ] && echo OK || echo FAIL)"
