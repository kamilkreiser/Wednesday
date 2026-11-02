#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
D=$W/repo/Blockchain/Dev; S=$D/services/originate
E=$W/eslint_tools; mkdir -p $E
echo '{"name":"g128-eslint-tools","private":true}' > $E/package.json
npm install --prefix $E --ignore-scripts --no-audit --no-fund eslint@^10.7.0 @eslint/js@^10.0.1 globals@^17.7.0 typescript-eslint@^8.64.0 typescript@^5.3.3 > $W/logs/eslint_install.log 2>&1; echo install rc=$?
cp $D/eslint.config.mjs $E/eslint.config.mjs
cat > $W/tsconfig.g128.json <<EOT
{ "extends": "$S/tsconfig.json", "compilerOptions": {"noEmit": true, "rootDir": "$S/src", "types": ["jest","node"], "typeRoots": ["$S/node_modules/@types"], "declaration": false, "sourceMap": false}, "include": ["$S/src/**/*"], "exclude": ["$S/node_modules","$S/dist"] }
EOT
$S/node_modules/.bin/tsc -p $S/tsconfig.json --noEmit > $W/logs/tsc_plain_$1.log 2>&1; echo tsc plain rc=$?
$S/node_modules/.bin/tsc -p $W/tsconfig.g128.json > $W/logs/tsc_tests_$1.log 2>&1; echo tsc tests rc=$? errors=$(/usr/bin/grep -c 'error TS' $W/logs/tsc_tests_$1.log)
(cd $E && $E/node_modules/.bin/eslint --config $E/eslint.config.mjs --no-warn-ignored $S/src/services/retentionScheduler.ts $S/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts > $W/logs/eslint_$1.log 2>&1; echo eslint rc=$?)
tail -12 $W/logs/eslint_$1.log
