#!/bin/zsh
# producers_read.sh — READ-ONLY git grep at the round-2 head (by SHA, in the checkout's object store; git grep is a read verb) for every producer of a
# machine authMethod ('api_key' / 'oauth_app'), every mention of rateLimitBucket, and the userId literal `connector:` — non-test source only, then tests
# counted separately. Positive controls on the same instrument: 'authMethod' (must be many) and 'rateLimitBucket' (must hit auth.ts + rateLimitEnforce.ts).
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66
echo "producers_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "--- control: lines naming authMethod anywhere under Blockchain/Dev (non-node_modules), count"
git -C "$R" grep -I -i -c 'authMethod' $H -- 'Blockchain/Dev/**' ':!**/node_modules/**' 2>&1 | awk -F: '{s+=$NF} END {print "authMethod lines", s, "files", NR}'
echo "--- 'api_key' or 'oauth_app' as a string literal near authMethod, NON-TEST source (file:line:text)"
git -C "$R" grep -I -n -i -E "authMethod[^,;]{0,40}['\"\`](api_key|oauth_app)['\"\`]|['\"\`](api_key|oauth_app)['\"\`][^,;]{0,40}authMethod" $H -- 'Blockchain/Dev/**' ':!**/node_modules/**' ':!**/__tests__/**' ':!**/*.test.ts' ':!**/*.spec.ts' ':!**/test/**' ':!**/tests/**' 2>&1
echo "rc=$?"
echo "--- 'oauth_app' literal anywhere NON-TEST (any context)"
git -C "$R" grep -I -n -i "oauth_app" $H -- 'Blockchain/Dev/**' ':!**/node_modules/**' ':!**/__tests__/**' ':!**/*.test.ts' ':!**/*.spec.ts' ':!**/test/**' ':!**/tests/**' 2>&1
echo "rc=$?"
echo "--- same regex in TEST files: count per file"
git -C "$R" grep -I -c -i -E "(api_key|oauth_app)" $H -- '**/__tests__/**' '**/*.test.ts' ':!**/node_modules/**' 2>&1 | head -40
echo "--- rateLimitBucket anywhere (control: must be auth.ts + rateLimitEnforce.ts + the ks1195 test)"
git -C "$R" grep -I -n -i "rateLimitBucket" $H -- 'Blockchain/**' 2>&1
echo "rc=$?"
echo "--- parseTestToken (the test-token branch's producer) and its NODE_ENV gate"
git -C "$R" grep -I -n -i -A12 "export function parseTestToken" $H -- 'Blockchain/Dev/services/api-gateway/src/**' 2>&1 | head -40
echo "--- auth service signers: authMethod set in services/auth/src (non-test)"
git -C "$R" grep -I -n -i "authMethod" $H -- 'Blockchain/Dev/services/auth/src/**' ':!**/__tests__/**' ':!**/*.test.ts' 2>&1 | head -60
echo "producers_read end $(date '+%H:%M:%S %Z')"
