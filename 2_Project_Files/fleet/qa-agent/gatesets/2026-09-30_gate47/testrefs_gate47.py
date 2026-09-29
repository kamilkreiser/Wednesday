#!/usr/bin/env python3
"""testrefs_gate47.py — THE TEST CENSUS for gate47: every test file ANYWHERE in the monorepo (Blockchain/** AND systemTest/**) that references a
changed PRODUCT file of #1349 or #1350, read by `git grep` at a NAMED tree (default: the END_TREE in pins_gate47.json; never a working copy).
Product files (the two test files are the PRs' own):
  #1349 systemTest/akto/src/setup/aktoRateLimit.ts
  #1350 Blockchain/Dev/deployment/azure/check-startup-migrations.sh, deploy-all.sh, deploy.sh
Spelling classes, each printed with its own count per product file:
  PATH     the repo path literally, and its tails (fixed strings);
  BASENAME the basename bounded so `deploy.sh` does not match `az-deploy.sh` / `pre-deploy.sh` / `deploy-all.sh`, and `aktoRateLimit` matches an
           extension-less TS import specifier (`…/setup/aktoRateLimit'` / `.js'`) (-E regex). REQUIRED: the ks1054 shell suite reaches the scripts
           through a variable (`"$AZ/deploy.sh"`), which no PATH spelling finds (gate45/46: PATH 0, BASENAME 1);
  SYMBOL   (INFO, never a gate) the exported / called names: isLocalScanTarget, derivedRateLimit, platformRequestsPerMinute; verify_deployment,
           smoke_skip, smoke_test, startupMigrations.
The CENSUS UNION = PATH + BASENAME, per product file and overall.
Test files = *.test.* / *.spec.* / anything under __tests__/, tests/, test/, e2e/ (pathspec globs over Blockchain/ and systemTest/, node_modules excluded).
CONTROLS inside (a census that prints nothing needs a control that prints):
  CT-POS   each PR's own test file is found by the census of its own product file(s);
  CT-NEG   a nonsense path finds 0;
  CT-TREE  the tree argument is honoured: at END the #1349 test blob == its head's and is ABSENT at develop (a new file); the ks1054 test blob at
           END == #1350's head's and != develop's (#1350 changed it).
rc 0 when every control holds; rc 1 otherwise. Writes testrefs_gate47.json (or testrefs_gate47.<tree12>.json for another tree) beside this script.
Env G47_TR_GLOB (controls only) replaces the test-file globs. Usage: testrefs_gate47.py <scratchpad> [--tree <sha>]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate47.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g47_sp', 'clone')
TREE = A[A.index('--tree') + 1] if '--tree' in A else P['end_tree']
TESTS = []
for root in ('Blockchain', 'systemTest'):
    TESTS += [':(glob)%s/**/*.test.*' % root, ':(glob)%s/**/*.spec.*' % root, ':(glob)%s/**/__tests__/**' % root, ':(glob)%s/**/tests/**' % root,
              ':(glob)%s/**/test/**' % root, ':(glob)%s/**/e2e/**' % root]
TESTS += [':(exclude,glob)**/node_modules/**']
if os.environ.get('G47_TR_GLOB'): TESTS = [os.environ['G47_TR_GLOB']]   # controls only: a census pointed at nothing must FAIL CT-POS
TESTRX = r'(\.test\.|\.spec\.|/__tests__/|/tests?/|/e2e/)'
def grep(tree, pat, regex=False):
    r = subprocess.run(['git', '-C', CL, 'grep', '-l', '-E' if regex else '-F', '-e', pat, tree, '--'] + TESTS, capture_output=True, text=True)
    if r.returncode not in (0, 1): raise SystemExit('REFUSING: git grep rc %d: %s' % (r.returncode, r.stderr[:200]))
    fs = sorted(set(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l))
    return [f for f in fs if re.search(TESTRX, f)]
AZ = 'Blockchain/Dev/deployment/azure/'
OWN49 = 'systemTest/akto/tests/unit/setup/ks1374-n1347-11-scan-target-override.test.ts'
OWN50 = 'Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh'
SPELL = {
 'systemTest/akto/src/setup/aktoRateLimit.ts': dict(pr='1349', own=OWN49, paths=['systemTest/akto/src/setup/aktoRateLimit.ts', 'src/setup/aktoRateLimit.ts', 'setup/aktoRateLimit.ts'],
     base=[r'''(^|[^A-Za-z0-9_.-])aktoRateLimit(\.(ts|js))?['"]'''], sym=['isLocalScanTarget', 'derivedRateLimit', 'platformRequestsPerMinute']),
 AZ + 'check-startup-migrations.sh': dict(pr='1350', own=OWN50, paths=[AZ + 'check-startup-migrations.sh', 'deployment/azure/check-startup-migrations.sh', 'azure/check-startup-migrations.sh'],
     base=[r'(^|[^A-Za-z0-9_.-])check-startup-migrations\.sh'], sym=['startupMigrations', 'PASS-WITH-SKIP']),
 AZ + 'deploy-all.sh': dict(pr='1350', own=OWN50, paths=[AZ + 'deploy-all.sh', 'deployment/azure/deploy-all.sh', 'azure/deploy-all.sh'],
     base=[r'(^|[^A-Za-z0-9_.-])deploy-all\.sh'], sym=['smoke_skip', 'smoke_test', 'SMOKE TEST RESULTS']),
 AZ + 'deploy.sh': dict(pr='1350', own=OWN50, paths=[AZ + 'deploy.sh', 'deployment/azure/deploy.sh', 'azure/deploy.sh'],
     base=[r'(^|[^A-Za-z0-9_.-])deploy\.sh'], sym=['verify_deployment', 'Post-deploy verification', '# ── Summary ─']),
}
bad = []
print('TEST CENSUS at tree %s (%s)' % (TREE, 'END_TREE' if TREE == P['end_tree'] else 'NOT the END_TREE'))
prods = [f for n in K['order'] for f in P['prs'][n]['files'] if not re.search(TESTRX, f)]
missing = [f for f in prods if f not in SPELL]
if missing: raise SystemExit('REFUSING: product file(s) with no spelling set: %s' % missing)
OUT = {'tree': TREE, 'files': {}}; allt = set(); own_hit = {}
for prod in prods:
    s = SPELL[prod]
    ph = sorted(set(h for x in s['paths'] for h in grep(TREE, x)))
    bh = sorted(set(h for x in s['base'] for h in grep(TREE, x, regex=True)))
    sy = {x: grep(TREE, x) for x in s['sym']}
    un = sorted(set(ph + bh)); allt |= set(un)
    print('== #%s %s' % (s['pr'], prod))
    print('   PATH     %s: %d file(s)' % (s['paths'], len(ph)))
    print('   BASENAME %s: %d file(s)' % (s['base'], len(bh)))
    for h in un: print('     %s%s' % (h, '   [changed by #%s]' % s['pr'] if h in P['union'] else ''))
    for x, hs in sy.items(): print('   SYMBOL %r (INFO): %d test file(s)%s' % (x, len(hs), (': ' + ', '.join(os.path.basename(y) for y in hs[:8])) if hs else ''))
    OUT['files'][prod] = {'pr': s['pr'], 'path_hits': ph, 'basename_hits': bh, 'symbol_hits': sy, 'union': un}
    own_hit.setdefault(s['pr'], set()).update(un)
for n, own in (('1349', OWN49), ('1350', OWN50)):
    pos = own in own_hit.get(n, set())
    print('CT-POS #%s its own test found by the census: %s %s' % (n, pos, 'OK' if pos else 'FAIL'))
    if not pos: bad.append('CT-POS: #%s its own test %s is not found — the census is blind' % (n, own))
neg = grep(TREE, 'Blockchain/Dev/deployment/azure/no-such-script-gate47.sh')
print('CT-NEG a nonsense path: %d file(s) %s' % (len(neg), 'OK' if not neg else 'FAIL'))
if neg: bad.append('CT-NEG found %s' % neg)
if TREE == P['end_tree']:
    blob = lambda t, p: subprocess.run(['git', '-C', CL, 'rev-parse', '--verify', '-q', '%s:%s' % (t, p)], capture_output=True, text=True).stdout.strip()
    e49, h49, d49 = blob(TREE, OWN49), blob(P['prs']['1349']['head'], OWN49), blob(P['develop'], OWN49)
    e50, h50, d50 = blob(TREE, OWN50), blob(P['prs']['1350']['head'], OWN50), blob(P['develop'], OWN50)
    ok = e49 == h49 and d49 == '' and re.fullmatch(r'[0-9a-f]{40}', e49 or '') is not None and e50 == h50 and e50 != d50 and re.fullmatch(r'[0-9a-f]{40}', e50 or '') is not None
    print('CT-TREE #1349 test blob at END %s == head %s: %s | at develop %s | #1350 ks1054 test blob at END %s == head %s: %s | != develop %s: %s %s' % (
        e49[:12], h49[:12], e49 == h49, d49[:12] or 'ABSENT', e50[:12], h50[:12], e50 == h50, d50[:12], e50 != d50, 'OK' if ok else 'FAIL'))
    if not ok: bad.append('CT-TREE the tree argument is not honoured')
OUT['all_tests'] = sorted(allt)
print('CENSUS UNION (PATH + BASENAME, at %s): %d test file(s):' % (TREE[:12], len(allt))); [print('  ' + t) for t in sorted(allt)]
json.dump(OUT, open(os.path.join(G, 'testrefs_gate47.json' if TREE == P['end_tree'] else 'testrefs_gate47.%s.json' % TREE[:12]), 'w'), indent=1)
print('TESTREFS %s: %d control problem(s)' % ('PASS' if not bad else 'FAIL', len(bad))); [print('  - ' + b) for b in bad]
raise SystemExit(1 if bad else 0)
