#!/bin/bash
# usage: tsc.sh <ref> <tag>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958
Dev=$W/repo/Blockchain/Dev; A=$Dev/services/anchoring
mkdir -p $W/_stash; mv $A/src/anchorStatusUpdate_base.ts $A/src/cardano/confirmation_base.ts $W/_stash/ 2>/dev/null
git -C $W/repo checkout -q $1 || exit 1
git -C $W/repo rev-parse HEAD
cat > $A/tsconfig.gate.json <<'J'
{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true, "rootDir": "." }, "include": ["src/**/*"], "exclude": ["node_modules","dist"] }
J
$Dev/node_modules/.bin/tsc -p $A/tsconfig.gate.json --noEmit > $W/logs/tsc_$2.log 2>&1; echo tsc rc=$?
/usr/bin/grep -c "error TS" $W/logs/tsc_$2.log
/usr/bin/grep "error TS" $W/logs/tsc_$2.log | head
mv $W/_stash/*base.ts $A/src/ 2>/dev/null; mv $A/src/confirmation_base.ts $A/src/cardano/ 2>/dev/null
mv $A/tsconfig.gate.json $W/_stash/tsconfig.gate.$2.json
