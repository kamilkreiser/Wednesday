#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892; L=$W/logs; R=$W/repo; D=$R/Blockchain/Dev/services/demo-service
TSC=$R/Blockchain/Dev/node_modules/.bin/tsc
cat > $W/scripts/tsconfig.gate.json <<EOT
{ "extends": "$D/tsconfig.json",
  "compilerOptions": { "noEmit": true, "rootDir": "$D", "declaration": false, "declarationMap": false, "sourceMap": false },
  "include": ["$D/src/**/*"], "exclude": ["$D/node_modules", "$D/dist"] }
EOT
V=$W/scripts/vt.sh
nice -n 10 $TSC -p $W/scripts/tsconfig.gate.json > $L/tsc_head.log 2>&1; echo "tsc head rc=$?"
bash $V $L/suite_head.log; echo "suite head rc=$?"
git -C $R checkout -q --detach refs/gate/develop; echo "co base rc=$?"; git -C $R rev-parse HEAD
nice -n 10 $TSC -p $W/scripts/tsconfig.gate.json > $L/tsc_base.log 2>&1; echo "tsc base rc=$?"
# base suite: new test file is absent at base
bash $V $L/suite_base.log; echo "suite base rc=$?"
git -C $R checkout -q --detach refs/gate/pr1892; echo "co head rc=$?"; git -C $R rev-parse HEAD
