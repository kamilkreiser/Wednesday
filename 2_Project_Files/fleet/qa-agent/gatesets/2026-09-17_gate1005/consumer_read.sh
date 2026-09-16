#!/bin/zsh
# consumer_read.sh — READ-ONLY: who calls the gateway's POST /api/documents/:id/verify (the route #1005 changes)? git grep on the head object.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9
X=(':!**/node_modules/**' ':!**/dist/**' ':!**/build/**' ':!**/deploy/assets/**' ':!**/assets/index-*.js' ':!**/package-lock.json')
echo "consumer_read $(date '+%Y-%m-%d %H:%M:%S %Z') at $H"
PAT='documents/\$\{[^}]*\}/verify|documents/:id/verify|documents/\{id\}/verify|documents/\{documentId\}/verify|documents/'"'"' *\+ *[A-Za-z_.]+ *\+ *'"'"'/verify'
echo "=== K1 all hits (code + docs + tests), path-prefixed; count by top dir after"
git -C "$R" grep -n -I -E "$PAT" $H -- . $X | sed "s/^$H://" | cut -c1-230
echo "=== K1 count: $(git -C "$R" grep -n -I -E "$PAT" $H -- . $X | wc -l | tr -d ' ')"
echo "=== K1 positive control (the route definition verification.ts:469 must be found): $(git -C "$R" grep -n -I -E "$PAT" $H -- Blockchain/Dev/services/api-gateway/src/routes/verification.ts | wc -l | tr -d ' ')"
echo "=== K1 by extension (code only: ts tsx js mjs py dart php gs kt swift)"
git -C "$R" grep -n -I -E "$PAT" $H -- '*.ts' '*.tsx' '*.js' '*.mjs' '*.py' '*.dart' '*.php' '*.gs' '*.kt' '*.swift' $X | sed "s/^$H://" | cut -c1-230
echo "=== K2: frontend verifier + outlook-addin: which verify URL each calls"
git -C "$R" grep -n -I -E "verify" $H -- Blockchain/Dev/frontend/verifier/src Blockchain/Dev/frontend/outlook-addin/src ':!**/__tests__/**' ':!**/*.test.*' | sed "s/^$H://" | /usr/bin/grep -i -E "fetch|post\(|url|/verify" | cut -c1-200
echo "=== K3: gateway routing: who owns /api/verification/verify (the portal's route) vs /api/documents/:id/verify"
git -C "$R" grep -n -I -E "verification/verify|proxyPaths|'/api/verification'" $H -- Blockchain/Dev/services/api-gateway/src/index.ts Blockchain/Dev/services/api-gateway/src/routes/proxy.ts | sed "s/^$H://" | cut -c1-200 | head -30
echo "=== K4: frontend/shared verify schema (the comment that names both routes)"
git -C "$R" show $H:Blockchain/Dev/frontend/shared/src/schemas/verify.ts | sed -n '1,40p'
echo "=== K5: originate verification route: does it read the gateway handler? (grep persistedAnchored / carve-out in originate)"
git -C "$R" grep -n -I -E "persistedAnchored|isAnchoredHonestly" $H -- Blockchain/Dev/services ':!Blockchain/Dev/services/api-gateway/**' | sed "s/^$H://" | cut -c1-200 | head
