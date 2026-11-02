#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
cd $G/repo/Blockchain/Dev && npm install --no-save --ignore-scripts --no-audit --no-fund --no-package-lock --workspaces=false --include-workspace-root @eslint/js typescript-eslint globals eslint > $G/logs/npm_eslint.log 2>&1
echo "rc=$?"; tail -3 $G/logs/npm_eslint.log
ls node_modules/@eslint/js node_modules/typescript-eslint 2>&1 | head -3
git -C $G/repo status --short | head
