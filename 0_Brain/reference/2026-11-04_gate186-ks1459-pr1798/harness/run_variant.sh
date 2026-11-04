#!/bin/bash
# Gate 186. usage: run_variant.sh <variant>
# mut/<variant>.ts becomes users.ts in the gate clone; the harness is copied in; JSON -> runs/<variant>.json.
# The process cwd is <workdir>/cwd (production loggers write relative logs/), HOME/TMPDIR inside the workdir.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate186-ks1459-pr1798
A=$G/repo/Blockchain/Dev/services/auth
V=$1
cp "$G/mut/$V.ts" "$A/src/routes/users.ts"
cp "$G/harness/gate186-matrix.test.ts" "$A/src/__tests__/gate186-matrix.test.ts"
cd "$G/cwd" || exit 9
env -i PATH="$PATH" HOME="$G/home" TMPDIR="$G/tmp" GATE_OUT="$G/runs/$V.json" \
  "$G/repo/Blockchain/Dev/node_modules/.bin/vitest" run --root "$A" src/__tests__/gate186-matrix.test.ts > "$G/runs/$V.out" 2>&1
rc=$?
echo "$V rc=$rc"
cp "$G/mut/head.ts" "$A/src/routes/users.ts"
exit $rc
