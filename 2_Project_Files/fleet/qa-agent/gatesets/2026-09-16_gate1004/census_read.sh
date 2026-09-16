#!/bin/zsh
# census_read.sh — READ-ONLY git grep census at head 6d077d3fe for #1004. Positive controls: the definition sites.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=6d077d3fe35cd5f3c09d394553d320e97b1abe32
echo "census_read $(date '+%Y-%m-%d %H:%M:%S %Z') tree $H"
echo "## A. safeOutboundRequest — every textual hit in Blockchain/Dev (non-node_modules), incl tests"
git -C "$R" grep -n 'safeOutboundRequest' $H -- 'Blockchain/Dev' ':!**/node_modules/**' ':!**/dist/**' | sed "s/^$H://"
echo "## B. imports of ssrf-guard or security exports by path"
git -C "$R" grep -n -E "ssrf-guard|security/ssrf" $H -- 'Blockchain/Dev' ':!**/node_modules/**' ':!**/dist/**' | sed "s/^$H://"
echo "## C. the other exports: assertSafeOutboundUrl / resolvePublicAddresses / checkUrlLiteral / assertResolvedHostPublic / pinnedLookup / classifyAddress"
for s in assertSafeOutboundUrl resolvePublicAddresses checkUrlLiteral assertResolvedHostPublic pinnedLookup classifyAddress classifyIPv4 classifyIPv6 SafeOutboundFailureReason; do
  echo "-- $s: $(git -C "$R" grep -c "$s" $H -- 'Blockchain/Dev' ':!**/node_modules/**' ':!**/dist/**' | wc -l | tr -d ' ') files"
  git -C "$R" grep -n "$s" $H -- 'Blockchain/Dev' ':!**/node_modules/**' ':!**/dist/**' ':!Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts' | sed "s/^$H://" | cut -c1-220
done
echo "## D. reason branches: .reason === / 'blocked' / 'request_failed' outside ssrf-guard.ts"
git -C "$R" grep -n -E "'blocked'|\"blocked\"|'request_failed'|\"request_failed\"|\.reason\b" $H -- 'Blockchain/Dev/services' 'Blockchain/Dev/packages' ':!**/node_modules/**' ':!**/dist/**' ':!Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts' | sed "s/^$H://" | cut -c1-240
echo "## E. shared index re-exports"
git -C "$R" grep -n -E "ssrf|security" $H -- 'Blockchain/Dev/packages/shared/src/index.ts' 'Blockchain/Dev/packages/shared/src/security/index.ts' | sed "s/^$H://" | cut -c1-200
echo "## F. dns/promises mocks in tests (who mocks lookup)"
git -C "$R" grep -n -E "vi.mock\('dns|jest.mock\('dns|dns/promises" $H -- 'Blockchain/Dev' ':!**/node_modules/**' ':!**/dist/**' | sed "s/^$H://" | cut -c1-200
echo "## G. 203.0.113 / 198.51.100 / TEST-NET literal use in tests"
git -C "$R" grep -n -c -E "203\.0\.113|198\.51\.100|192\.0\.2\." $H -- 'Blockchain/Dev' ':!**/node_modules/**' | sed "s/^$H://"
echo "## H. fake timers in shared tests touching the guard"
git -C "$R" grep -n -E "useFakeTimers" $H -- 'Blockchain/Dev/packages/shared/src' | sed "s/^$H://"
