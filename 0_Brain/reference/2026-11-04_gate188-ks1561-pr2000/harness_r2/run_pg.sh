#!/bin/bash
# Gate 188 r2 PG runner. usage: run_pg.sh <base|r1|r2|cur> <outname> [r2]   (cur = leave the clone's route files as they are, for mutants)
# Overlays the two route blobs of <version> into MY clone, runs the harness with cwd in the workdir, restores the r2 blobs and checks sha256.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000
R=$W/repo; RT=Blockchain/Dev/services/originate/src/routes; O=$R/Blockchain/Dev/services/originate
V=$1; out=$2; exp=$3
case $V in base) S=d92b849ece732cd04e283bfcb0ee9e8bd6989631;; r1) S=d03b03046d76591aec3e5a3aa4176fb4e5b78e04;; r2) S=f702d4da4b69478e82d3d79ea4e8746fae47f2eb;; cur) S=;; *) echo bad; exit 2;; esac
if [ -n "$S" ]; then
  git -C "$R" show "$S:$RT/verification.ts" > "$O/src/routes/verification.ts" || exit 3
  git -C "$R" show "$S:$RT/verificationV2.ts" > "$O/src/routes/verificationV2.ts" || exit 3
fi
rm -f "$W/runs_r2/$out.jsonl"
cd "$W/tmp_r2/cwd" || exit 9
env -i PATH="$PATH" HOME=$W/tmp_r2/home TMPDIR=$W/tmp_r2/tmp LC_ALL=C VERSION=$V OUT="$W/runs_r2/$out.jsonl" EXPECT="$exp" \
  node "$O/node_modules/jest/bin/jest.js" -c "$W/harness_r2/jest.pg.config.js" --cacheDirectory "$W/tmp_r2/jc" --runInBand --verbose > "$W/runs_r2/$out.txt" 2>&1
rc=$?
if [ -n "$S" ]; then
  git -C "$R" checkout -q f702d4da4b69478e82d3d79ea4e8746fae47f2eb -- "$RT/verification.ts" "$RT/verificationV2.ts"
fi
echo "rc=$rc"; grep -E "^(Tests|Test Suites):" "$W/runs_r2/$out.txt"
shasum -a 256 "$O/src/routes/verification.ts" "$O/src/routes/verificationV2.ts" | cut -c1-16
