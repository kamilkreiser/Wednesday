#!/bin/bash
# Red at tip / green after / tamper / arm / suite / lint for the KS-1347 ks732 golden, in the scratch clone only. Restores the clone.
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed3/ks1347
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
Q=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed3/_quarantine
S=$C/Blockchain/Dev/services/auth
G=$W/KS-1347-ks732.golden.diff
TF=src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts
P=src/__tests__/ks732-mfa-disable-proof.test.ts
run() { (cd $S && npx vitest run "$@" 2>&1 | grep -E '✓|×|Test Files|Tests |AssertionError|Expected|Received|Error:|%20' | head -24); }
echo "== baseline: ks732 at tip"; run $P
echo "== RED at tip (new test only)"
cp $W/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts $S/$TF
run $TF
mv $S/$TF $Q/ks1347.pre-apply.$(date +%H%M%S).ts
echo "== GREEN after golden (git apply strict, whole diff)"
git -C $C apply $G; echo "git apply rc=$?"
cmp $S/$TF $W/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts && echo "applied test == golden test"
run $TF $P
echo "== whole auth suite on the fixed tree"
(cd $S && npx vitest run 2>&1 | grep -E 'Test Files|Tests ' )
echo "== lint (package's own: npm run lint = eslint src; eslint --max-warnings 0 on the two files; tsc -p tsconfig.json --noEmit)"
(cd $S && npm run lint > $W/lint_full.out 2>&1; echo "npm run lint rc=$?"; grep -E 'problems|error' $W/lint_full.out | tail -3)
(cd $S && npx eslint --max-warnings 0 $TF $P; echo "eslint 2 files rc=$?")
(cd $S && npx tsc -p tsconfig.json --noEmit; echo "tsc rc=$?")
echo "== TAMPER: :317 back to .pathname (fixed tree)"
cp $S/$P $Q/ks732.fixed.$(date +%H%M%S).ts
python3 - $S/$P <<'PY'
import sys
p=sys.argv[1]; L=open(p).read().split('\n')
a="      fileURLToPath(new URL('../auth.openapi.ts', import.meta.url)), 'utf8',"
b="      new URL('../auth.openapi.ts', import.meta.url).pathname, 'utf8',"
print('line 317 is fixed text:', L[316]==a, '; fixed text count', L.count(a)); L[316]=b; open(p,'w').write('\n'.join(L))
PY
run $TF
echo "== ARM: decodeURIComponent(pathname) at all three sites (should be GREEN: the cell tests behaviour, not the idiom)"
git -C $C checkout -- Blockchain/Dev/services/auth/$P
python3 - $S/$P <<'PY'
import sys,re
p=sys.argv[1]; t=open(p).read()
n=0
for f in ["../auth.openapi.ts","../routes/mfa.ts"]:
    a=f"new URL('{f}', import.meta.url).pathname, 'utf8',"
    b=f"decodeURIComponent(new URL('{f}', import.meta.url).pathname), 'utf8',"
    n+=t.count(a); t=t.replace(a,b)
print('arm replaced', n); open(p,'w').write(t)
PY
run $TF
echo "== restore clone"
git -C $C checkout -- Blockchain/Dev/services/auth/$P
mv $S/$TF $Q/ks1347.post.$(date +%H%M%S).ts
git -C $C status --porcelain
