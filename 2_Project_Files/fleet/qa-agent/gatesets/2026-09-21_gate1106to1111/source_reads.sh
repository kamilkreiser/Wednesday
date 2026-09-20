#!/bin/bash
# source_reads.sh — READ-ONLY `git show <sha>:<path>` reads in the Secuura checkout at develop cbae988db (every PR-side develop blob is
# identical at 778e6cfe2, shape_1.out) and at each head, for the lines the gate will measure. Nothing written to the checkout.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV=cbae988dbe90ebe556459ada2cb437eaf80e2402
D=Blockchain/Dev; A=$D/services/api-gateway; T=$D/services/timestamping; S=$D/services/security
g() { git -C "$R" "$@"; }
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== api-gateway index.ts at develop: shouldParseBody decl + uses + proxyPaths + the /api/v1 rewrite"
g show $DEV:$A/src/index.ts | grep -n -iE 'shouldParseBody|proxyPaths|/api/v1|express\.json|urlencoded|sanitizeInput|detectSuspiciousRequests' | head -40
echo "--- :405-420"; g show $DEV:$A/src/index.ts | sed -n '405,420p'
echo "--- :455-462"; g show $DEV:$A/src/index.ts | sed -n '455,462p'
echo "--- :555-565"; g show $DEV:$A/src/index.ts | sed -n '555,565p'
echo "--- line count develop / #1108 head"; g show $DEV:$A/src/index.ts | wc -l; g show 4904c081c4f9be776acef78349bc10384f10de35:$A/src/index.ts | wc -l
echo "--- #1108 index.ts diff"; g diff $DEV 4904c081c4f9be776acef78349bc10384f10de35 -- $A/src/index.ts
echo "=== trustHeaders.ts at develop :30-60 (blob $(g rev-parse $DEV:$A/src/utils/trustHeaders.ts))"; g show $DEV:$A/src/utils/trustHeaders.ts | sed -n '30,60p'
echo "=== referrals.ts :50-60 (grep x-wallet-address)"; g show $DEV:$A/src/routes/referrals.ts | grep -n -i 'x-wallet-address' ; g show $DEV:$A/src/routes/referrals.ts | sed -n '50,60p'
echo "=== x-wallet-address across api-gateway src (develop)"; g grep -n -i 'x-wallet-address' $DEV -- "$A/src" | sed "s#$DEV:##"
echo "=== converters.ts at develop :118-140 (blob $(g rev-parse $DEV:$S/src/converters.ts))"; g show $DEV:$S/src/converters.ts | sed -n '118,140p'
echo "--- who imports converters (security src)"; g grep -n -E "from '\./converters'|from '\.\./converters'|converters'" $DEV -- "$S/src" | sed "s#$DEV:##"
echo "=== timestamping index.ts :510-520 (blob $(g rev-parse $DEV:$T/src/index.ts))"; g show $DEV:$T/src/index.ts | sed -n '510,520p'
echo "--- verified: true lines"; g show $DEV:$T/src/index.ts | grep -n 'verified: true'
echo "--- PORT / listen"; g show $DEV:$T/src/index.ts | grep -n -E 'PORT|app\.listen'
echo "=== health.ts :55-60 (blob $(g rev-parse $DEV:$A/src/routes/health.ts))"; g show $DEV:$A/src/routes/health.ts | sed -n '55,60p'
echo "=== preflight.sh :700-712 at develop"; g show $DEV:$D/scripts/preflight/preflight.sh | sed -n '700,712p'
echo "--- at #1109 head :700-713"; g show f592268af36b282029e50ff2fa1ebe2614304b81:$D/scripts/preflight/preflight.sh | sed -n '700,713p'
echo "--- preflight.sh SKIPPED / legs / _note_skip lines at develop"; g show $DEV:$D/scripts/preflight/preflight.sh | grep -n -E '_note_skip|SKIPPED|legs ran|INCOMPLETE|n_ran|env_fail|step "[0-9]+/' | head -60
echo "=== the 8 sibling bash suites + the new one (scripts/__tests__ naming preflight.sh) at #1109 head"
for f in $(g ls-tree --name-only f592268af36b282029e50ff2fa1ebe2614304b81 $D/scripts/__tests__/ | grep '\.test\.sh$'); do g show f592268af36b282029e50ff2fa1ebe2614304b81:$f | grep -q -F preflight.sh && echo "  $f"; done
echo "=== new test file #1108 (94 lines) — it( titles"; g show 4904c081c4f9be776acef78349bc10384f10de35:$A/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts | grep -n -E "^\s*(it|test|describe)\(|listen\(|127\.0\.0\.1|process\.env|status" | head -40
echo "--- :70-80 (LINT-1 line 76)"; g show 4904c081c4f9be776acef78349bc10384f10de35:$A/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts | sed -n '70,80p'
echo "=== #1111 ks1041 test head :113-119"; g show 3d1ea289a0c367af5cd0d060322e46fc900a1c76:$A/src/__tests__/ks1041-vouch-header-strip.test.ts | sed -n '110,119p'
echo "=== #1110 row-converters head :150-164"; g show a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c:$S/src/__tests__/row-converters.test.ts | sed -n '150,164p'
echo "--- its imports"; g show a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c:$S/src/__tests__/row-converters.test.ts | grep -n import
echo "=== #1107 ks740 test head :120-153"; g show 7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30:$T/src/__tests__/ks740-bounded-fanout.test.ts | sed -n '120,153p'
echo "=== #1106 ks480 test head :133-151"; g show 2abc82d11014f00567b75a6b8fab5ec5e78f9df2:$A/src/__tests__/ks480-connector-auth.test.ts | sed -n '133,151p'
echo "=== file line counts (develop -> head)"; for p in "$A/src/__tests__/ks480-connector-auth.test.ts 2abc82d11014f00567b75a6b8fab5ec5e78f9df2" "$T/src/__tests__/ks740-bounded-fanout.test.ts 7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30" "$S/src/__tests__/row-converters.test.ts a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c" "$A/src/__tests__/ks1041-vouch-header-strip.test.ts 3d1ea289a0c367af5cd0d060322e46fc900a1c76"; do set -- $p; echo "  $(basename $1): $(g show $DEV:$1 | wc -l | tr -d ' ') -> $(g show $2:$1 | wc -l | tr -d ' ')"; done
echo "=== sizes+sha256 of the four tamper files at develop"; for p in $A/src/routes/health.ts $T/src/index.ts $S/src/converters.ts $A/src/utils/trustHeaders.ts; do printf '  %s %s bytes sha256 %s blob %s\n' "$(basename $p)" "$(g show $DEV:$p | wc -c | tr -d ' ')" "$(g show $DEV:$p | shasum -a 256 | cut -c1-12)" "$(g rev-parse $DEV:$p | cut -c1-12)"; done
date -u +%Y-%m-%dT%H:%M:%SZ
