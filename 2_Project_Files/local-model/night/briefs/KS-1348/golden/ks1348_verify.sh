#!/bin/bash
# KS-1348: make the golden (product hunk + new test file), prove strict apply, red at tip / green after /
# tamper, test-inclusive tsc tip vs fixed, lint, whole originate suite. Scratch clone only; restores it.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
C=$S/sparkfeed
W=$S/feed/ks1348
O=$C/Blockchain/Dev/services/originate
R=Blockchain/Dev/services/originate
PF=src/utils/logger.ts
TN=ks1348-production-file-log-lines-are-json.test.ts
TF=src/__tests__/$TN
G=$W/KS-1348.golden.diff
reset() { git -C $C checkout -- $R; rm -f $O/$TF; rm -rf $O/logs; }
run() { (cd $O && npx jest $TF 2>&1 | grep -E '✓|✕|Tests:|error TS|Expected|Received|●.*›|"undefined"' | head -${1:-40}); }
reset
python3 - $C $R/$PF $W/logger.fixed.ts <<'PY'
import sys,subprocess
C,P,out=sys.argv[1:]
t=subprocess.run(['git','-C',C,'show','94c9c7aa9be7:'+P],capture_output=True,text=True,check=True).stdout
a="""// File transports for production
if (nodeEnv === 'production') {
  transports.push(
    new winston.transports.File({ filename: 'logs/error.log', level: 'error', maxsize: 10_000_000, maxFiles: 5 }),
    new winston.transports.File({ filename: 'logs/combined.log', maxsize: 10_000_000, maxFiles: 5 }),
"""
b="""// File transports for production
// KS-1348: each File transport carries its own json() format, as the Console transport does. The
// logger-level format renders nothing, so without it every line written was the literal undefined.
if (nodeEnv === 'production') {
  transports.push(
    new winston.transports.File({ filename: 'logs/error.log', level: 'error', format: combine(json()), maxsize: 10_000_000, maxFiles: 5 }),
    new winston.transports.File({ filename: 'logs/combined.log', format: combine(json()), maxsize: 10_000_000, maxFiles: 5 }),
"""
assert t.count(a)==1; open(out,'w').write(t.replace(a,b))
PY
cp $W/logger.fixed.ts $O/$PF; cp $W/$TN $O/$TF
(git -C $C diff -U1 -- $R/$PF | sed -E 's/^(@@ [^@]* @@).*/\1/; s/^@@ -41,9 \+41,11 @@$/@@ -42,7 +42,9 @@/' | grep -v -x ' ' ; git -C $C diff --no-index -- /dev/null $O/$TF | sed "s#b$O/#b/$R/#; s#^+++ b/.*#+++ b/$R/$TF#; /^diff --git/d; /^new file mode/d; /^index /d") > $W/raw.diff
python3 - $W/raw.diff $G <<'PY'
import sys
lines=open(sys.argv[1]).read().split('\n')
out=[l for l in lines if not l.startswith(('diff --git','index ','new file mode'))]
open(sys.argv[2],'w').write('\n'.join(out))
PY
rm -f $W/raw.diff
cat $G | head -24; grep -c '' $G
reset
echo "== strict apply"
git -C $C apply --check $G; echo "git apply --check rc=$?"
git -C $C apply $G; echo "git apply rc=$?"
cmp $O/$PF $W/logger.fixed.ts && echo "product == logger.fixed.ts"; cmp $O/$TF $W/$TN && echo "test == golden test"
reset
git -C $C show HEAD:$R/$PF > $W/p.tip
python3 -c "import sys;g=open('$G').read();p=g.split('--- /dev/null')[0];open('$W/p.hunks','w').write(p.split('\n',2)[2])"
patch -F0 --dry-run $W/p.tip < $W/p.hunks; echo "patch -F0 product rc=$?"
sed 's/maxsize: 10_000_000, maxFiles: 5 }),$/maxsize: 10_000_000, maxFiles: 6 }),/' $W/p.tip > $W/p.bad; patch -F0 --dry-run $W/p.bad < $W/p.hunks; echo "control (maxFiles altered) patch -F0 rc=$?"
rm -f $W/p.tip $W/p.bad $W/p.hunks
echo "== RED at tip: new test, tip product"
cp $W/$TN $O/$TF; run 40; reset
echo "== GREEN after: golden"
git -C $C apply $G; run 40
echo "== TAMPER: error.log transport loses its format (fixed tree)"
python3 - $O/$PF <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
a="level: 'error', format: combine(json()), maxsize"
print('tamper target count', t.count(a)); open(p,'w').write(t.replace(a,"level: 'error', maxsize"))
PY
run 40
reset; git -C $C apply $G
echo "== test-inclusive tsc: tip vs fixed"
git -C $C checkout -- $R; rm -f $O/$TF
bash $S/feed/tsc_incl.sh $W/tsc_tip.txt
git -C $C apply $G
bash $S/feed/tsc_incl.sh $W/tsc_fixed.txt
diff $W/tsc_tip.txt $W/tsc_fixed.txt && echo "tsc error SETS identical (tip vs fixed)"
(cd $O && node ../../node_modules/typescript/bin/tsc --noEmit -p tsconfig.json; echo "package tsc (as checker A7) rc=$?")
echo "== lint"
(cd $O && npx eslint --max-warnings 0 $TF $PF; echo "eslint --max-warnings 0 test+product rc=$?")
(cd $O && npm run lint 2>&1 | tail -3; echo "npm run lint rc=${PIPESTATUS[0]}")
echo "== whole originate suite, fixed"
(cd $O && npx jest 2>&1 | grep -E '^Tests:|^Test Suites:|✕' | head -20)
ls $O/logs 2>&1 | head -2
reset
git -C $C status --porcelain
