#!/bin/bash
# KS-1349: the 2x2 (test head/fixed x product tip/tamper) + the ticket's own production-only tamper,
# test-inclusive tsc tip vs fixed, lint, whole originate suite. Scratch clone only; restores it.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
C=$S/sparkfeed
W=$S/feed/ks1349
O=$C/Blockchain/Dev/services/originate
TF=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
PF=src/routes/adminConfig.ts
G=$W/KS-1349.golden.diff
run() { (cd $O && npx jest $TF 2>&1 | grep -E '✓|✕|Tests:|error TS|Expected|Received' | head -${1:-40}); }
tamper() { # $1 = dev | prod
python3 - $O/$PF $1 <<'PY'
import sys
p,k=sys.argv[1:]; t=open(p).read()
a="  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
b="  if (process.env.NODE_ENV === '"+("development" if k=="dev" else "production")+"') logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
lines=t.split('\n'); print('tamper', k, 'target count', t.count(a), 'at line', [i+1 for i,l in enumerate(lines) if l==a])
open(p,'w').write(t.replace(a,b))
PY
}
reset() { git -C $C checkout -- Blockchain/Dev/services/originate; }
reset
echo "== R0 tip product + HEAD test"; run 30
tamper dev; echo "== R1 TAMPER(dev-only) + HEAD test  [expect: C1 blind = green]"; run 30; reset
git -C $C apply $G; echo "golden apply rc=$?"
echo "== R2 tip product + FIXED test  [expect: all green]"; run 30
tamper dev; echo "== R3 TAMPER(dev-only) + FIXED test  [expect: C1 x4 red + KS-1334 A1 x2 red]"; run 60
git -C $C checkout -- Blockchain/Dev/services/originate/$PF
tamper prod; echo "== R4 ticket tamper (production-only) + FIXED test"; run 40
reset
tamper prod; echo "== R5 ticket tamper (production-only) + HEAD test  [is the ticket's tamper discriminating?]"; run 40
reset
echo "== test-inclusive tsc: tip vs fixed"
bash $S/feed/tsc_incl.sh $W/tsc_tip.txt
git -C $C apply $G
bash $S/feed/tsc_incl.sh $W/tsc_fixed.txt
diff $W/tsc_tip.txt $W/tsc_fixed.txt && echo "tsc error SETS identical (tip vs fixed)"
echo "== positive control: an unused const in the test file must surface TS6133 in the test-inclusive tsc"
echo 'const ks1349Unused = 1;' >> $O/$TF
bash $S/feed/tsc_incl.sh $W/tsc_ctrl.txt; cat $W/tsc_ctrl.txt
git -C $C checkout -- Blockchain/Dev/services/originate/$TF; git -C $C apply $G
echo "== lint: package eslint (tip warnings vs fixed) and --max-warnings 0 on the test file"
(cd $O && npx eslint --max-warnings 0 $TF; echo "eslint --max-warnings 0 fixed test rc=$?")
(cd $O && npm run lint 2>&1 | tail -3; echo "npm run lint rc=${PIPESTATUS[0]}")
echo "== whole originate suite, fixed"
(cd $O && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:|✕' | head -20)
reset
git -C $C status --porcelain
