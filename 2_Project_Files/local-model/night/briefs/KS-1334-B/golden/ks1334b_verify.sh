#!/bin/bash
# KS-1334 part B: strict apply, red at tip / green after / tamper / arm R3 / test-inclusive tsc / lint / suite,
# plus the KS-1349 collision (both goldens, both orders). Scratch clone only; restores it.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
C=$S/sparkfeed
W=$S/feed/ks1334b
O=$C/Blockchain/Dev/services/originate
TF=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
PF=src/routes/adminConfig.ts
G=$W/KS-1334-B.golden.diff
G49=$S/feed/ks1349/KS-1349.golden.diff
run() { (cd $O && npx jest $TF 2>&1 | grep -E '✕|Tests:|error TS|Expected|Received|●.*›' | head -${1:-40}); }
reset() { git -C $C checkout -- Blockchain/Dev/services/originate; }
reset
echo "== strict apply"
git -C $C apply --check $G; echo "git apply --check rc=$?"
git -C $C apply $G; echo "git apply rc=$?"
cmp $O/$PF $W/adminConfig.B.ts && echo "product == adminConfig.B.ts"
cmp $O/$TF $W/ks730c.B.ts && echo "test == ks730c.B.ts"
reset
git -C $C show HEAD:Blockchain/Dev/services/originate/$PF > $W/p.tip; git -C $C show HEAD:Blockchain/Dev/services/originate/$TF > $W/t.tip
python3 - $G $W <<'PY'
import sys,re
g,w=sys.argv[1:]; parts=re.split(r'(?m)^(?=--- a/)', open(g).read()); parts=[p for p in parts if p]
for p,name in zip(parts,('p','t')): open(f'{w}/{name}.hunks','w').write(p.split('\n',2)[2])
PY
patch -F0 --dry-run $W/p.tip < $W/p.hunks; echo "patch -F0 product rc=$?"
patch -F0 --dry-run $W/t.tip < $W/t.hunks; echo "patch -F0 test rc=$?"
sed 's/      failed,/      failed ,/' $W/p.tip > $W/p.bad; patch -F0 --dry-run $W/p.bad < $W/p.hunks; echo "control (:2028 altered) patch -F0 rc=$?"
rm -f $W/p.tip $W/t.tip $W/p.bad $W/p.hunks $W/t.hunks
echo "== RED at tip: FIXED test, tip product"
cp $W/ks730c.B.ts $O/$TF; run 60; reset
echo "== GREEN after: golden"
git -C $C apply $G; run 60
echo "== TAMPER: :2031 back to the tip's leak line (fixed tree)"
python3 - $O/$PF <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="    fail500(res, 'Admin config request failed (POST /api/admin/seed-demo-users)', err);"
b="    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"
print('tamper target count', t.count(a)); open(p,'w').write(t.replace(a,b))
PY
run 60
git -C $C checkout -- Blockchain/Dev/services/originate/$PF; git -C $C apply --include=Blockchain/Dev/services/originate/$PF $G; echo "re-apply product rc=$?"
echo "== ARM R3: fail500 logs only under production (fixed tree)"
python3 - $O/$PF <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
b="  if (process.env.NODE_ENV === 'production') logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
print('R3 target count', t.count(a)); open(p,'w').write(t.replace(a,b))
PY
run 80
reset
echo "== test-inclusive tsc: tip vs fixed"
bash $S/feed/tsc_incl.sh $W/tsc_tip.txt
git -C $C apply $G
bash $S/feed/tsc_incl.sh $W/tsc_fixed.txt
diff $W/tsc_tip.txt $W/tsc_fixed.txt && echo "tsc error SETS identical (tip vs fixed)"
echo "== lint"
(cd $O && npx eslint --max-warnings 0 $TF; echo "eslint --max-warnings 0 fixed test rc=$?")
(cd $O && npx eslint $PF 2>&1 | grep -E 'warning|error' ; echo "eslint product (warnings listed) rc=${PIPESTATUS[0]}")
(cd $O && npm run lint 2>&1 | tail -3; echo "npm run lint rc=${PIPESTATUS[0]}")
echo "== whole originate suite, fixed"
(cd $O && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:|✕' | head -20)
reset
echo "== whole originate suite, tip"
(cd $O && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:|✕' | head -20)
eslint_tip=$(cd $O && npx eslint $PF 2>&1 | grep -cE 'warning'); echo "eslint product tip warnings=$eslint_tip"
echo "== COLLISION with KS-1349: order B then 1349"
git -C $C apply $G; echo "B rc=$?"; git -C $C apply $G49; echo "1349 on B rc=$?"; cp $O/$TF $W/order1.ts; run 40
reset
echo "== COLLISION: order 1349 then B"
git -C $C apply $G49; echo "1349 rc=$?"; git -C $C apply $G; echo "B on 1349 rc=$?"; cmp $O/$TF $W/order1.ts && echo "both orders -> identical test file"
reset
git -C $C status --porcelain
