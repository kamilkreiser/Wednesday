#!/bin/bash
# npm ci --ignore-scripts at Blockchain/Dev root of one tree, then build packages/shared
T="$1"; LBL="$2"; G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953
D="$T/Blockchain/Dev"
npm ci --ignore-scripts --no-audit --no-fund --prefix "$D" > "$G/logs/install_$LBL.log" 2>&1; echo "npm ci rc=$?" >> "$G/logs/install_$LBL.log"
node "$D/scripts/fix-libsodium-symlink.js" >> "$G/logs/install_$LBL.log" 2>&1
npm --prefix "$D/packages/shared" run build >> "$G/logs/install_$LBL.log" 2>&1; echo "shared build rc=$?" >> "$G/logs/install_$LBL.log"
echo DONE >> "$G/logs/install_$LBL.log"
