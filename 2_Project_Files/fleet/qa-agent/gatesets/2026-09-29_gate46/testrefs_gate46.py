#!/usr/bin/env python3
"""testrefs_gate46.py — THE TEST CENSUS for gate46: every test file ANYWHERE in the monorepo (Blockchain/** AND systemTest/**) that references the ONE
changed PRODUCT file of #1348 (Blockchain/Dev/deployment/azure/deploy.sh; the other changed path is the ks1054 test itself), read by `git grep` at a
NAMED tree (default: the END_TREE in pins_gate46.json; never a working copy). Spelling classes, each printed with its own count:
  PATH     the repo path literally, and its tails (fixed strings);
  BASENAME `deploy.sh` bounded so it does not match `az-deploy.sh` / `pre-deploy.sh` / `deploy-all.sh` (-E regex). REQUIRED: the shell suite reaches
           deploy.sh through a variable (`"$AZ/deploy.sh"`), which no PATH spelling finds (gate45: PATH 0, BASENAME 1);
  SYMBOL   (INFO, never a gate) `verify_deployment`, `Post-deploy verification`, `# ── Summary ─`.
The CENSUS UNION = PATH + BASENAME.
Test files = *.test.* / *.spec.* / anything under __tests__/, tests/, test/, e2e/ (pathspec globs over Blockchain/ and systemTest/, node_modules excluded).
CONTROLS inside (a census that prints nothing needs a control that prints):
  CT-POS   the PR's own ks1054 shell suite is found (via BASENAME);
  CT-NEG   a nonsense path finds 0;
  CT-TREE  the tree argument is honoured: at END the ks1054 test blob == the head's (round 2) and != develop's (round 2 changed it).
rc 0 when every control holds; rc 1 otherwise. Writes testrefs_gate46.json (or testrefs_gate46.<tree12>.json for another tree) beside this script.
Env G46_TR_GLOB (controls only) replaces the test-file globs. Usage: testrefs_gate46.py <scratchpad> [--tree <sha>]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate46.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g46_sp', 'clone')
TREE = A[A.index('--tree') + 1] if '--tree' in A else P['end_tree']
TESTS = []
for root in ('Blockchain', 'systemTest'):
    TESTS += [':(glob)%s/**/*.test.*' % root, ':(glob)%s/**/*.spec.*' % root, ':(glob)%s/**/__tests__/**' % root, ':(glob)%s/**/tests/**' % root,
              ':(glob)%s/**/test/**' % root, ':(glob)%s/**/e2e/**' % root]
TESTS += [':(exclude,glob)**/node_modules/**']
if os.environ.get('G46_TR_GLOB'): TESTS = [os.environ['G46_TR_GLOB']]   # controls only: a census pointed at nothing must FAIL CT-POS
TESTRX = r'(\.test\.|\.spec\.|/__tests__/|/tests?/|/e2e/)'
def grep(tree, pat, regex=False):
    r = subprocess.run(['git', '-C', CL, 'grep', '-l', '-E' if regex else '-F', '-e', pat, tree, '--'] + TESTS, capture_output=True, text=True)
    if r.returncode not in (0, 1): raise SystemExit('REFUSING: git grep rc %d: %s' % (r.returncode, r.stderr[:200]))
    fs = sorted(set(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l))
    return [f for f in fs if re.search(TESTRX, f)]
PROD = 'Blockchain/Dev/deployment/azure/deploy.sh'
OWN = 'Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh'
PATHS = [PROD, 'deployment/azure/deploy.sh', 'azure/deploy.sh']
BASE = [r'(^|[^A-Za-z0-9_.-])deploy\.sh']
SYM = ['verify_deployment', 'Post-deploy verification', '# ── Summary ─']
bad = []
print('TEST CENSUS at tree %s (%s)' % (TREE, 'END_TREE' if TREE == P['end_tree'] else 'NOT the END_TREE'))
missing = [f for f in P['prs']['1348']['files'] if not re.search(TESTRX, f) and f != PROD]
if missing: raise SystemExit('REFUSING: product file(s) with no spelling set: %s' % missing)
ph = sorted(set(h for x in PATHS for h in grep(TREE, x)))
bh = sorted(set(h for x in BASE for h in grep(TREE, x, regex=True)))
sy = {x: grep(TREE, x) for x in SYM}
un = sorted(set(ph + bh))
print('== #1348 %s' % PROD)
print('   PATH     %s: %d file(s)' % (PATHS, len(ph)))
print('   BASENAME %s: %d file(s)' % (BASE, len(bh)))
for h in un: print('     %s%s' % (h, '   [changed by #1348]' if h in P['union'] else ''))
for x, hs in sy.items(): print('   SYMBOL %r (INFO): %d test file(s)%s' % (x, len(hs), (': ' + ', '.join(os.path.basename(y) for y in hs[:10])) if hs else ''))
pos = OWN in un
print('CT-POS #1348 its own test found by the census: %s %s' % (pos, 'OK' if pos else 'FAIL'))
if not pos: bad.append('CT-POS: its own test %s is not found — the census is blind' % OWN)
neg = grep(TREE, 'Blockchain/Dev/deployment/azure/no-such-script-gate46.sh')
print('CT-NEG a nonsense path: %d file(s) %s' % (len(neg), 'OK' if not neg else 'FAIL'))
if neg: bad.append('CT-NEG found %s' % neg)
if TREE == P['end_tree']:
    blob = lambda t: subprocess.run(['git', '-C', CL, 'rev-parse', '%s:%s' % (t, OWN)], capture_output=True, text=True).stdout.strip()
    be, bhd, bdv = blob(TREE), blob(P['prs']['1348']['head']), blob(P['develop'])
    ok = be == bhd and be != bdv and re.fullmatch(r'[0-9a-f]{40}', be or '') is not None
    print('CT-TREE the ks1054 test blob at END %s == head %s: %s | != develop %s: %s %s' % (be[:12], bhd[:12], be == bhd, bdv[:12], be != bdv, 'OK' if ok else 'FAIL'))
    if not ok: bad.append('CT-TREE the tree argument is not honoured (END blob %s, head %s, develop %s)' % (be, bhd, bdv))
out = {'tree': TREE, 'files': {PROD: {'pr': '1348', 'path_hits': ph, 'basename_hits': bh, 'symbol_hits': sy, 'union': un}}, 'all_tests': un}
print('CENSUS UNION (PATH + BASENAME, at %s): %d test file(s):' % (TREE[:12], len(un))); [print('  ' + t) for t in un]
json.dump(out, open(os.path.join(G, 'testrefs_gate46.json' if TREE == P['end_tree'] else 'testrefs_gate46.%s.json' % TREE[:12]), 'w'), indent=1)
print('TESTREFS %s: %d control problem(s)' % ('PASS' if not bad else 'FAIL', len(bad))); [print('  - ' + b) for b in bad]
raise SystemExit(1 if bad else 0)
