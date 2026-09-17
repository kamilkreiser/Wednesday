#!/usr/bin/env python3
"""drafter_followup_1029.py — separates the load timeouts drafter_run_1029.py recorded from assertion reds, and adds eslint:
(a) the develop 75ad0e55c suite again (run 1: ks864b / ks864c failed at ~5.6 s, STACK_TRACE_ERROR = vitest's 5 s timeout, not an assertion);
(b) D-DOUBLE-ALWAYS again (run 1: +1 db.retry.test.ts at 6.36 s, STACK_TRACE_ERROR) with the same edit, anchor count 1, restore by sha + git diff --quiet;
(c) eslint (Dev flat config) on the head ks1072 test and on develop's, plus a firing control (the head file on stdin with one unused const).
Own clone only. Never rm, never cd."""
import hashlib, json, os, subprocess, datetime
from collections import Counter
GS = os.path.dirname(os.path.abspath(__file__)); OUT = GS + '/out'; PATHS = json.load(open(GS + '/drafter_paths.json'))
REL = 'Blockchain/Dev/services/api-gateway'; KS = 'ks1072-the-latest-anchor-selector-documents-a.test.ts'
def now(f='%Y-%m-%d %H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def gw(t): return PATHS['trees'][t] + '/' + REL
def blob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def vt(t, tag):
    jf = f'{OUT}/vt_{tag}.json'
    with open(f'{OUT}/vt_{tag}.out', 'w') as fo:
        subprocess.run([gw(t) + '/../../node_modules/.bin/vitest', 'run', '--reporter=json', '--outputFile=' + jf], cwd=gw(t), stdout=fo, stderr=subprocess.STDOUT)
    d = json.load(open(jf))
    fails = [(os.path.basename(r['name']), a['title'][:70], round(a.get('duration') or 0), (a['failureMessages'] or [''])[0].splitlines()[0][:110]) for r in d['testResults'] for a in r['assertionResults'] if a['status'] == 'failed']
    return (len(d['testResults']), d['numTotalTests'], d['numPassedTests'], d['numFailedTests'], d['numPendingTests']), fails
P('drafter_followup_1029', now())
s, f = vt('curdev', 'suite_curdev_run2'); P(now('%H:%M:%S'), 'develop 75ad0e55c suite run 2 (files, tests, passed, failed, pending)', s, '| failed', f)
VER = gw('head') + '/src/routes/verification.ts'; WT = PATHS['trees']['head']
A = "      doc = await fetchDocFromAnchorStore(id, authHeader);\n"
orig = open(VER, 'rb').read(); committed = subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + REL + '/src/routes/verification.ts'], capture_output=True, text=True).stdout.strip()
assert blob(orig) == committed; txt = orig.decode(); assert txt.count(A) == 1
open(VER, 'w').write(txt.replace(A, "      await fetchDocFromAnchorStore(id, authHeader); doc = await fetchDocFromAnchorStore(id, authHeader); // qa1029 D-DOUBLE-ALWAYS\n"))
try:
    s, f = vt('head', 'tamper_D-DOUBLE-ALWAYS_run2')
finally:
    open(VER, 'wb').write(orig)
P(now('%H:%M:%S'), 'D-DOUBLE-ALWAYS run 2', s, '| ks1072 reds', sum(1 for x in f if x[0] == KS), '| other', dict(Counter(x[0] for x in f if x[0] != KS)), '| restored sha', blob(open(VER, 'rb').read()) == committed,
  '| git diff --quiet', subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD']).returncode == 0)
for x in f: P('     red', x)
ES = PATHS['trees']['head'] + '/Blockchain/Dev/node_modules/.bin/eslint'
for t in ('head', 'curdev'):
    p = subprocess.run([ES, '--format', 'json', 'services/api-gateway/src/__tests__/' + KS], cwd=PATHS['trees'][t] + '/Blockchain/Dev', capture_output=True, text=True)
    try:
        r = json.loads(p.stdout)[0]; P('eslint', t, 'rc', p.returncode, '| errors', r['errorCount'], 'warnings', r['warningCount'], [(m.get('ruleId'), m['line'], m['message'][:60]) for m in r['messages']][:6])
    except Exception as e:
        P('eslint', t, 'rc', p.returncode, 'UNPARSED', type(e).__name__, p.stdout[:200], p.stderr[:300])
src = open(gw('head') + '/src/__tests__/' + KS).read(); anchor = "const DOC_ID = 'doc-ks1072';\n"; assert src.count(anchor) == 1
p = subprocess.run([ES, '--format', 'json', '--stdin', '--stdin-filename', 'services/api-gateway/src/__tests__/' + KS], input=src.replace(anchor, anchor + 'const qaUnusedControl1029 = 1;\n'), cwd=PATHS['trees']['head'] + '/Blockchain/Dev', capture_output=True, text=True)
try:
    r = json.loads(p.stdout)[0]; P('eslint firing control (head + unused const, stdin) rc', p.returncode, '| errors', r['errorCount'], 'warnings', r['warningCount'], [(m.get('ruleId'), m['line'], m.get('severity'), m['message'][:60]) for m in r['messages']][:4])
except Exception as e:
    P('eslint control UNPARSED', type(e).__name__, p.stdout[:200], p.stderr[:300])
P('drafter_followup_1029 end', now())
