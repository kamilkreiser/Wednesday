#!/bin/bash
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/ks1334
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
O=$C/Blockchain/Dev/services/originate
TF=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
PF=src/routes/adminConfig.ts
echo "== TIP: eslint on the two files (warnings)"
(cd $O && npx eslint $TF $PF 2>&1 | tail -4; echo "eslint tip rc=${PIPESTATUS[0]}")
echo "== TIP: whole originate jest suite"
(cd $O && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:')
git -C $C apply $W/KS-1334-A.golden.diff; echo "apply rc=$?"
echo "== FIXED: package lint (npm run lint = eslint src)"
(cd $O && npm run lint 2>&1 | tail -3; echo "npm run lint rc=${PIPESTATUS[0]}")
(cd $O && npx eslint --max-warnings 0 $TF; echo "eslint --max-warnings 0 on the test file rc=$?")
echo "== FIXED: whole originate jest suite"
(cd $O && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:|✕' | head -20)
git -C $C checkout -- Blockchain/Dev/services/originate
git -C $C status --porcelain
