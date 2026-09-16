#!/bin/zsh
# census_read.sh — READ-ONLY census at the #1005 head (git grep on the object, never the worktree). Read verbs only.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9
X=(':!**/node_modules/**' ':!**/dist/**' ':!**/build/**' ':!**/*.min.js' ':!**/package-lock.json' ':!**/deploy/assets/**')
echo "census_read $(date '+%Y-%m-%d %H:%M:%S %Z') at $H"
echo "=== C1: every occurrence of the token _source (whole repo tree at head; git grep -w -F: word-bounded both sides; first run used ERE \\b, which git grep ignores here — its positive control read 0, kept as census_read.first-run-control-0-broken-regex.out) — writers AND readers"
git -C "$R" grep -n -I -w -F '_source' $H -- . $X | sed "s/^$H://" | cut -c1-260 
echo "=== C1 count: $(git -C "$R" grep -n -I -w -F '_source' $H -- . $X | wc -l | tr -d ' ')"
echo "=== C1 positive control (same instrument must find the tier-2 writer and the predicate in verification.ts): $(git -C "$R" grep -n -I -w -F '_source' $H -- Blockchain/Dev/services/api-gateway/src/routes/verification.ts | wc -l | tr -d ' ')"
echo "=== C1b: the string anchor_store anywhere (quoted value form)"
git -C "$R" grep -n -I -E "anchor_store" $H -- . $X | sed "s/^$H://" | cut -c1-260
echo "=== C1c: generic source-marker keys that could collide ('_source' as a quoted key, [\"_source\"], _source:)"
git -C "$R" grep -n -I -E "['\"]_source['\"]" $H -- . $X | sed "s/^$H://" | cut -c1-260
echo "=== C2: callers of the document verify route (/api/documents/<id>/verify) outside api-gateway routes"
git -C "$R" grep -n -I -E "documents/[^'\"\` ]*/verify|/verify[\`'\"]" $H -- . $X ':!**/__tests__/**' ':!**/*.test.*' | sed "s/^$H://" | cut -c1-260 | head -120
echo "=== C2 count (non-test): $(git -C "$R" grep -n -I -E "documents/[^'\"\` ]*/verify|/verify[\`'\"]" $H -- . $X ':!**/__tests__/**' ':!**/*.test.*' | wc -l | tr -d ' ')"
echo "=== C3: readers of verificationConfidence / blockchain.anchored / blockchainAnchored outside api-gateway (response consumers)"
git -C "$R" grep -n -I -E "verificationConfidence|blockchainAnchored|blockchain\??\.anchored|blockchain\??\.confidence" $H -- . $X ':!Blockchain/Dev/services/api-gateway/**' ':!**/__tests__/**' ':!**/*.test.*' | sed "s/^$H://" | cut -c1-260 | head -150
echo "=== C4: top-level directories (to name what the census covered)"
git -C "$R" ls-tree --name-only $H
git -C "$R" ls-tree --name-only $H Blockchain/ Blockchain/Dev/ Blockchain/Dev/services/ Blockchain/Dev/apps/ 2>/dev/null
