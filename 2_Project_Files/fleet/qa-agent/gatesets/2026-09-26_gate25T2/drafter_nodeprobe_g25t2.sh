#!/bin/bash
# drafter_nodeprobe_g25t2.sh — the drafter's LIVE probe of #1273's namesVerbAsRouteToken (PREDICTION, never the gate's evidence). The function body is
# EXTRACTED from the head blob of ks978-published-contract-organizationuuid.test.ts at b800791a3295 (read from the scratch clone, never retyped — the
# extraction is asserted to have found exactly one definition) and run under plain node over shapes the cells do not carry. The verb set is a FIXED
# LIST here (version, revoke, share, anchor, transfer-custody), not the registry — the gate runs the real cell.
set -u
CL="${1:?usage: drafter_nodeprobe_g25t2.sh <scratch clone.git>}"
SRC="$(git --git-dir "$CL" show b800791a3295f048b40f920435b080a270c65106:Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts)"
FN="$(printf '%s\n' "$SRC" | awk '/^const namesVerbAsRouteToken = /{p=1} p{print} p&&/^};/{exit}')"
N="$(printf '%s\n' "$FN" | grep -c 'const namesVerbAsRouteToken')"
echo "extracted definitions: $N (want 1); lines: $(printf '%s\n' "$FN" | wc -l | tr -d ' ')"
[ "$N" = 1 ] || { echo "EXTRACTION FAILED"; exit 2; }
JS="$(printf '%s\n' "$FN" | sed -e 's/(description: string, verb: string): boolean/(description, verb)/')"
node -e "$JS
const verbs = ['version','revoke','share','anchor','transfer-custody'];
const cases = [
 ['CONTROL cell fixture: back-quoted', 'Send it to the \`version\` route instead; see docs/VOCABULARY.md.'],
 ['CONTROL cell fixture: ordinary prose', 'A new version of this list is not kept here.'],
 ['back-quoted span ENDING in the verb', 'Use \`subversion\` here.'],
 ['back-quoted prose ending in the verb', 'The \`a new version\` wording.'],
 ['closing+opening back-quote pairing', 'See \`enum\` for the version\` list\`.'],
 ['bare prose share (declared NOT caught)', 'share must use its own route.'],
 ['hyphenated inside a longer token', 'the pre-transfer-custody-check step'],
 ['slash-delimited mid-path', 'POST /api/documents/{id}/revoke/confirm'],
];
for (const [what, d] of cases) console.log(what.padEnd(42), '->', JSON.stringify(verbs.filter(v => namesVerbAsRouteToken(d, v))));
" 2>&1
echo "rc=$?"
