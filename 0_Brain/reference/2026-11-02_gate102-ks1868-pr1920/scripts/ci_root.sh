#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
D=$G/repo/Blockchain/Dev
cd "$D" && npm ci --ignore-scripts --workspace=@secuura/shared --workspace=services/analytics --include-workspace-root=false > $G/logs/npm_ci3.log 2>&1
echo "rc=$?" >> $G/logs/npm_ci3.log
tail -4 $G/logs/npm_ci3.log
ls -la node_modules/@secuura
cat packages/shared/package.json | grep -n '"build"\|"main"\|"types"'
cd packages/shared && node ../../node_modules/typescript/bin/tsc > $G/logs/shared_build.log 2>&1; echo "shared build rc=$?"; tail -3 $G/logs/shared_build.log
ls dist | head -3
