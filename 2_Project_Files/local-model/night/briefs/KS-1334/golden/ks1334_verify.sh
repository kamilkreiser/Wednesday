#!/bin/bash
# KS-1334 A: red at tip / green after / tamper / arm R3 / lint, scratch clone only; restores the clone.
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/ks1334
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
O=$C/Blockchain/Dev/services/originate
TF=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
PF=src/routes/adminConfig.ts
G=$W/KS-1334-A.golden.diff
MODE=${1:-all}
run() { (cd $O && npx jest $TF 2>&1 | grep -E '✓|✕|Tests:|Test Suites:|error TS|●.*›' | grep -v '^\s*$' | head -${2:-40}); }
if [ "$MODE" = all ] || [ "$MODE" = red ]; then
echo "== RED at tip: modified test, tip product"
cp $W/ks730c.A.ts $O/$TF
run
git -C $C checkout -- Blockchain/Dev/services/originate
fi
if [ "$MODE" = all ] || [ "$MODE" = green ]; then
echo "== GREEN: golden applied (git apply strict)"
git -C $C apply $G; echo "git apply rc=$?"
cmp $O/$TF $W/ks730c.A.ts && echo "test == golden ks730c.A.ts"
cmp $O/$PF $W/adminConfig.A.ts && echo "product == golden adminConfig.A.ts"
run
echo "== tsc (originate) and eslint on the two files"
(cd $O && npx tsc --noEmit -p tsconfig.json 2>&1 | tail -5; echo "tsc rc=${PIPESTATUS[0]}")
(cd $O && npx eslint --max-warnings 0 $TF $PF; echo "eslint rc=$?")
echo "== TAMPER on the fixed tree: :113 back to the tip's leak line"
python3 - $O/$PF <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="    fail500(res, 'Admin config request failed (POST /api/admin/refresh-tenants)', err);"
b="    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err?.message || 'Refresh failed' } });"
print('tamper target count', t.count(a)); open(p,'w').write(t.replace(a,b))
PY
run
git -C $C checkout -- $O/$PF 2>/dev/null || git -C $C checkout -- Blockchain/Dev/services/originate/$PF
git -C $C apply --include=Blockchain/Dev/services/originate/$PF $G; echo "re-apply product rc=$?"
echo "== ARM R3 on the fixed tree: fail500 logs only under production"
python3 - $O/$PF <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
b="  if (process.env.NODE_ENV === 'production') logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
print('R3 target count', t.count(a)); open(p,'w').write(t.replace(a,b))
PY
run
echo "== restore"
git -C $C checkout -- Blockchain/Dev/services/originate
git -C $C status --porcelain
fi
