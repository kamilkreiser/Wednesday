#!/bin/bash
# Gate 186. usage: run_repo_files.sh <variant>
# Runs the repo's own ten verification-route test files with mut/<variant>.ts as users.ts.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate186-ks1459-pr1798
A=$G/repo/Blockchain/Dev/services/auth
V=$1
cp "$G/mut/$V.ts" "$A/src/routes/users.ts"
cd "$G/cwd" || exit 9
env -i PATH="$PATH" HOME="$G/home" TMPDIR="$G/tmp" \
  "$G/repo/Blockchain/Dev/node_modules/.bin/vitest" run --root "$A" \
  src/__tests__/ks1018-item3 src/__tests__/ks1018-security-correctness src/__tests__/ks1193-review-read src/__tests__/ks1193-verification-reads \
  src/__tests__/ks1194-a-failed src/__tests__/ks1194-approve-never src/__tests__/ks1194-part2 src/__tests__/ks1236-approve \
  src/__tests__/ks1477-the-verification src/__tests__/ks467-user-admin > "$G/runs/repofiles_$V.out" 2>&1
rc=$?
echo "$V rc=$rc $(grep -E '^ *(Test Files|Tests) ' "$G/runs/repofiles_$V.out" | sed 's/\x1b\[[0-9;]*m//g' | tr -s ' ' | tr '\n' ' ')"
cp "$G/mut/head.ts" "$A/src/routes/users.ts"
exit $rc
