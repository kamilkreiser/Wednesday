#!/bin/bash
# KS-1348: stability — the fixed tree's new cell 5x in a worker and 2x --runInBand; the tip's 3x (must red the same 2 every time).
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
C=$S/sparkfeed; W=$S/feed/ks1348; O=$C/Blockchain/Dev/services/originate; R=Blockchain/Dev/services/originate
TF=src/__tests__/ks1348-production-file-log-lines-are-json.test.ts
before=$(ls -d ${TMPDIR:-/tmp}/ks1348-* 2>/dev/null | wc -l)
git -C $C apply $W/KS-1348.golden.diff
for i in 1 2 3 4 5; do (cd $O && npx jest $TF 2>&1 | grep -E '^Tests:'); done
for i in 1 2; do (cd $O && npx jest --runInBand $TF 2>&1 | grep -E '^Tests:'); done
git -C $C checkout -- $R
for i in 1 2 3; do (cd $O && npx jest $TF 2>&1 | grep -E '^Tests:'); done
rm -f $O/$TF
after=$(ls -d ${TMPDIR:-/tmp}/ks1348-* 2>/dev/null | wc -l)
echo "temp dirs left behind: before=$before after=$after"
git -C $C status --porcelain; echo "porcelain lines: $(git -C $C status --porcelain | wc -l)"
