#!/bin/bash
# Red at tip / green after / tamper / arm / suite / lint for the KS-1346-A golden, in the scratch clone only. Restores the clone.
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed3/ks1346
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
Q=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed3/_quarantine
S=$C/Blockchain/Dev/services/originate
G=$W/KS-1346-A.golden.diff
TF=src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts
P=src/routes/systemErrors.ts
run() { (cd $S && npx jest "$@" 2>&1 | grep -E '✓|✕|Tests:|Test Suites:|Expected|Received' | head -30); }
echo "== RED at tip (new test only)"
cp $W/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts $S/$TF
run $TF
mv $S/$TF $Q/ks1346a.pre-apply.$(date +%H%M%S).ts
echo "== GREEN after golden (git apply strict)"
git -C $C apply $G; echo "git apply rc=$?"
cmp $S/$TF $W/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts && echo "applied test == golden test"
run $TF src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts
echo "== whole originate suite on the fixed tree"
(cd $S && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:')
echo "== lint (package's own: npm run lint; eslint --max-warnings 0 on the two files; tsc --noEmit)"
(cd $S && npm run lint > $W/a_lint_full.out 2>&1; echo "npm run lint rc=$?"; grep -E 'problems' $W/a_lint_full.out | tail -2; grep -n -A3 'systemErrors.ts\|ks1346a' $W/a_lint_full.out | head -8)
(cd $S && npx eslint --max-warnings 0 $TF $P; echo "eslint 2 files rc=$?")
(cd $S && npx tsc --noEmit -p tsconfig.json; echo "tsc rc=$?")
echo "== TAMPER: :95 inspect(err) -> inspect(String(err)) (fixed tree; the import stays used, so the suite still compiles)"
cp $S/$P $Q/systemErrors.fixed.$(date +%H%M%S).ts
python3 - $S/$P <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="    logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(err) });"
b="    logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(String(err)) });"
print('tamper target count', t.count(a), '; at line 95:', t.split('\n')[94]==a); open(p,'w').write(t.replace(a,b))
PY
run $TF
echo "== ARM: inspect() for EVERY non-Error (string throws get quoted) -> the string control A4 must go RED"
python3 - $S/$P <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
b="    logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : inspect(String(err)) });"
c="    logger.error(context, { error: err instanceof Error ? err.message : inspect(err) });"
print('arm count', t.count(b)); open(p,'w').write(t.replace(b,c))
PY
run $TF
echo "== restore clone"
git -C $C checkout -- Blockchain/Dev/services/originate/$P
mv $S/$TF $Q/ks1346a.post.$(date +%H%M%S).ts
git -C $C status --porcelain
