#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943; D=$W/repo/Blockchain/Dev
npm ci --ignore-scripts --prefix $D/packages/shared > $W/logs/npm_ci_shared.log 2>&1; echo ci rc=$?
$D/packages/shared/node_modules/.bin/tsc -p $D/packages/shared/tsconfig.json > $W/logs/build_shared.log 2>&1; echo build rc=$?
mkdir -p $D/services/originate/node_modules/@secuura
ln -s $D/packages/shared $D/services/originate/node_modules/@secuura/shared; echo ln rc=$?
ls $D/packages/shared/dist | head -3
