#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917
A=$W/repo/Blockchain/Dev/services/tenant-provisioning; TSC=$W/repo/Blockchain/Dev/node_modules/.bin/tsc; T=$A/src/__tests__
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
C=$A/tsconfig.zz-gate99-tests.json
printf '{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true, "rootDir": "." }, "include": ["src/**/*"], "exclude": ["node_modules", "dist"] }\n' > $C
nice -n 10 $TSC -p $C > $W/logs/tsc_tests_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_head.log
F=$(ls $T/ks1868-tenant-provisioning-*.test.ts | head -1); cp "$F" $W/logs/_orig_test.ts
printf '\nconst GATE99_BAD: number = "x";\n' >> "$F"
nice -n 10 $TSC -p $C > $W/logs/tsc_tests_planted.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_planted.log
cp $W/logs/_orig_test.ts "$F"; [ "$(sha "$F")" = "$(sha $W/logs/_orig_test.ts)" ] && echo test restore OK
cp $W/logs/base_index.ts $A/src/index.ts; mkdir -p $W/logs/_stash2; mv $T/ks1868-tenant-provisioning-*.test.ts $W/logs/_stash2/
nice -n 10 $TSC -p $C > $W/logs/tsc_tests_base.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_base.log
mv $W/logs/_stash2/*.test.ts $T/; cp $W/logs/head_index.ts $A/src/index.ts
mv $C $W/logs/_quarantine/
[ "$(sha $A/src/index.ts)" = "$(sha $W/logs/head_index.ts)" ] && echo RESTORE_OK
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo status --short
