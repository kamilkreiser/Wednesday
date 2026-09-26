#!/bin/bash
# Red at tip / green after / tamper / lint for the akto golden, in the scratch clone only. Restores the clone at the end.
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/akto
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
Q=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/_quarantine
G=$W/KS-1337-akto.golden.diff
TF=tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts
P=systemTest/akto/tests/preSuiteSetup.ts
A=$C/systemTest/akto
run() { (cd $A && npx vitest run --config vitest.unit.config.ts $TF 2>&1 | grep -E '✓|×|Tests |Expected|Received' | head -12); }
echo "== RED at tip (test file only)"
cp $W/ks1337-preSuiteSetupPathWithASpace.test.ts $A/$TF
run
echo "== GREEN after golden (git apply strict, whole diff)"
mv $A/$TF $Q/akto.pre-apply.$(date +%H%M%S).ts
git -C $C apply $G; echo "git apply rc=$?"
cmp $A/$TF $W/ks1337-preSuiteSetupPathWithASpace.test.ts && echo "applied test == golden test"
run
echo "== whole akto unit suite on the fixed tree"
(cd $A && npx vitest run --config vitest.unit.config.ts 2>&1 | grep -E 'Test Files|Tests ' )
echo "== lint (package's own: tsc + eslint on the two files)"
(cd $A && npx tsc -p tsconfig.json --noEmit; echo "tsc rc=$?")
(cd $A && npx eslint --config eslint.config.js --max-warnings 0 $TF tests/preSuiteSetup.ts; echo "eslint rc=$?")
(cd $A && npx prettier --check --editorconfig $TF tests/preSuiteSetup.ts; echo "prettier rc=$?")
echo "== TAMPER: :37 back to .pathname (fixed tree)"
cp $C/$P $Q/preSuiteSetup.fixed.$(date +%H%M%S).ts
python3 - $C/$P <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="    const step = fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url));"
b="    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;"
print('tamper target count', t.count(a)); open(p,'w').write(t.replace(a,b))
PY
run
echo "== ARM: decodeURIComponent(pathname) alternative (should be GREEN: the cell tests behaviour, not the idiom)"
python3 - $C/$P <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
b="    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;"
c="    const step = decodeURIComponent(new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname);"
open(p,'w').write(t.replace(b,c))
PY
run
echo "== restore clone"
git -C $C checkout -- $P
mv $A/$TF $Q/akto.post.$(date +%H%M%S).ts
git -C $C status --porcelain
