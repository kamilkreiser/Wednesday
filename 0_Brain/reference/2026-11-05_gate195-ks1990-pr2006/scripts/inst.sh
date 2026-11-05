#!/bin/bash
# gate 194: install deps from the head's lock (npm ci --ignore-scripts), build shared; hermetic env, cwd inside the workdir
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate195-ks1990-pr2006; D=$W/repo/Blockchain/Dev
mkdir -p $W/logs $W/cwd $W/home $W/tmp
cd $W/cwd || exit 9
E="env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp"
$E npm --prefix $D ci --ignore-scripts > $W/logs/npm_ci.log 2>&1; echo ci_rc=$? > $W/logs/npm_ci.rc
$E npm --prefix $D run build --workspace=packages/shared > $W/logs/build_shared.log 2>&1; echo build_rc=$? >> $W/logs/npm_ci.rc
