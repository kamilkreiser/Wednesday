#!/bin/bash
# The 4 new test files + the login probe with develop's auth errorHandler.ts (the only develop change on their import path) in place.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949
R=$G/repo; E=Blockchain/Dev/services/auth/src/middleware/errorHandler.ts
H0=$(shasum -a 256 $R/$E | awk '{print $1}')
git -C $R show origin/develop:$E > $R/$E
$G/scripts/vt.sh $G/logs/merged_new_tests.log src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts src/__tests__/ks1868-issuer-certs-message-coercion-unreadable-throw.test.ts src/__tests__/ks1868-oauth-message-coercion-unreadable-throw.test.ts --hookTimeout=60000 --testTimeout=30000; echo "merged new tests rc=$?"
git -C $R show pr1949:$E > $R/$E
[ "$(shasum -a 256 $R/$E | awk '{print $1}')" = "$H0" ] && echo "errorHandler restored" || echo "RESTORE FAIL"
git -C $R status --short
