#!/bin/bash
# Gate 192: run the PG15 harness against whatever verification.ts the clone holds. usage: pgrun.sh <version-label>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004
V="$1"; OUT=$W/runs/pg_$V.jsonl; rm -f "$OUT"
F=$W/repo/Blockchain/Dev/services/originate/src/routes/verification.ts
echo "verification.ts sha256 $(shasum -a 256 $F | cut -c1-16)" > $W/runs/pg_$V.log
cd $W/cwd || exit 9
env -i PATH="$PATH" HOME=$W/home TMPDIR=$W/tmp VERSION="$V" OUT="$OUT" \
  $W/repo/Blockchain/Dev/node_modules/.bin/jest -c $W/pgcell/jest.pg.config.js --runInBand >> $W/runs/pg_$V.log 2>&1
echo "rc=$?" >> $W/runs/pg_$V.log
echo "rows $(wc -l < $OUT)" >> $W/runs/pg_$V.log
