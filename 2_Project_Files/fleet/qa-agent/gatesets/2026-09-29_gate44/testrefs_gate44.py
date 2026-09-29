#!/usr/bin/env python3
"""testrefs_gate44.py — THE TEST CENSUS for gate44: every test file ANYWHERE in the monorepo (Blockchain/** AND systemTest/**) that references a
changed PRODUCT file, read by `git grep` at a NAMED tree (default: the END_TREE in pins_gate44.json; never a working copy). Spelling classes per
changed product file, each printed with its own count so a zero is attributable:
  PATH     the repo path literally, and its tails from Blockchain/Dev/ or the package root (fixed strings);
  BASENAME the file name alone, bounded so `deploy.sh` does not match `az-deploy.sh` and `env.example` does not match `.env.example`
           (-E regex). REQUIRED here: shell suites reach their subjects through variables (`"$AZ/deploy-all.sh"`), which no PATH spelling finds;
  IMPORT   the module specifier a same-package test uses (`aktoRateLimit`, restricted to systemTest/akto);
  SYMBOL   (INFO, never a gate) identifiers the change sits under (`startupMigrations`, `RATE_LIMIT_MAX_REQUESTS`, `derivedRateLimit`, ...).
The CENSUS UNION = PATH + BASENAME + IMPORT.
Test files = *.test.* / *.spec.* / anything under __tests__/, tests/, test/, e2e/ (pathspec globs over Blockchain/ and systemTest/, node_modules excluded).
CONTROLS inside (a census that prints nothing needs a control that prints):
  CT-POS   each PR's own NEW test file that exercises a product file is found (#1346: the ks1054 shell suite; #1347: the akto ks1374 unit file);
  CT-NEG   a nonsense path finds 0;
  CT-TREE  at END, the batch's three NEW test files are absent at develop (the tree argument is honoured);
  CT-KNOWN a pre-existing suite known to read a changed file is listed (bootstrap_env_canonical_template.test.sh reads env.example).
#1347's api-gateway file (ks1374-global-limiter-at-demo-limit.test.ts) reads index.ts and docker-compose.yml, NEITHER a changed path: it is printed
as OWN-TEST-NO-CHANGED-PATH (the gate runs it anyway), never counted as a census hit.
rc 0 when every control holds; rc 1 otherwise. Writes testrefs_gate44.json (or testrefs_gate44.<tree12>.json for another tree) beside this script.
Env G44_TR_GLOB (controls only) replaces the test-file globs. Usage: testrefs_gate44.py <scratchpad> [--tree <sha>]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate44.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g44_sp', 'clone')
TREE = A[A.index('--tree') + 1] if '--tree' in A else P['end_tree']
TESTS = []
for root in ('Blockchain', 'systemTest'):
    TESTS += [':(glob)%s/**/*.test.*' % root, ':(glob)%s/**/*.spec.*' % root, ':(glob)%s/**/__tests__/**' % root, ':(glob)%s/**/tests/**' % root,
              ':(glob)%s/**/test/**' % root, ':(glob)%s/**/e2e/**' % root]
TESTS += [':(exclude,glob)**/node_modules/**']
if os.environ.get('G44_TR_GLOB'): TESTS = [os.environ['G44_TR_GLOB']]   # controls only: a census pointed at nothing must FAIL CT-POS
TESTRX = r'(\.test\.|\.spec\.|/__tests__/|/tests?/|/e2e/)'
def grep(tree, pat, scope=None, regex=False):
    spec = TESTS if not scope else [':(glob)%s/**' % scope, ':(exclude,glob)**/node_modules/**']
    r = subprocess.run(['git', '-C', CL, 'grep', '-l', '-E' if regex else '-F', '-e', pat, tree, '--'] + spec, capture_output=True, text=True)
    if r.returncode not in (0, 1): raise SystemExit('REFUSING: git grep rc %d: %s' % (r.returncode, r.stderr[:200]))
    fs = sorted(set(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l))
    return [f for f in fs if re.search(TESTRX, f)]
B = r'(^|[^A-Za-z0-9_.-])'   # a basename boundary: not preceded by a name character, a dot or a hyphen
SPELL = {
 'Blockchain/Dev/deployment/azure/check-startup-migrations.sh': dict(path=['Blockchain/Dev/deployment/azure/check-startup-migrations.sh', 'deployment/azure/check-startup-migrations.sh'],
     base=[B + r'check-startup-migrations\.sh'], imp=[], scope=None, sym=['startupMigrations']),
 'Blockchain/Dev/deployment/azure/deploy-all.sh': dict(path=['Blockchain/Dev/deployment/azure/deploy-all.sh', 'deployment/azure/deploy-all.sh', 'azure/deploy-all.sh'],
     base=[B + r'deploy-all\.sh'], imp=[], scope=None, sym=['smoke_test', 'HEALTH_BODY']),
 'Blockchain/Dev/deployment/azure/deploy.sh': dict(path=['Blockchain/Dev/deployment/azure/deploy.sh', 'deployment/azure/deploy.sh', 'azure/deploy.sh'],
     base=[B + r'deploy\.sh'], imp=[], scope=None, sym=['verify_deployment', 'API_HEALTH']),
 'Blockchain/Dev/.env.example': dict(path=['Blockchain/Dev/.env.example', 'Dev/.env.example'], base=[r'(^|[^A-Za-z0-9_])\.env\.example'], imp=[], scope=None,
     sym=['RATE_LIMIT_MAX_REQUESTS']),
 'Blockchain/Dev/env.example': dict(path=['Blockchain/Dev/env.example', 'Dev/env.example'], base=[r'(^|[^A-Za-z0-9_.])env\.example'], imp=[], scope=None,
     sym=['RATE_LIMIT_MAX_REQUESTS']),
 'systemTest/akto/src/setup/aktoRateLimit.ts': dict(path=['systemTest/akto/src/setup/aktoRateLimit.ts', 'src/setup/aktoRateLimit'], base=[],
     imp=['aktoRateLimit'], scope='systemTest/akto', sym=['derivedRateLimit', 'PLATFORM_REQUESTS_PER_MINUTE', 'platformRequestsPerMinute']),
}
OWN_POS = {'1346': ['Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh'],
           '1347': ['systemTest/akto/tests/unit/setup/ks1374-platform-limit-from-env.test.ts']}
OWN_NOPATH = {'1347': ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts']}
KNOWN = 'Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh'
out = {'tree': TREE, 'files': {}}; bad = []
print('TEST CENSUS at tree %s (%s)' % (TREE, 'END_TREE' if TREE == P['end_tree'] else 'NOT the END_TREE'))
missing = [f for n in K['order'] for f in P['prs'][n]['files'] if not re.search(TESTRX, f) and f not in SPELL]
if missing: raise SystemExit('REFUSING: product file(s) with no spelling set: %s' % missing)
perpr = {n: set() for n in K['order']}
for n in K['order']:
    for f in P['prs'][n]['files']:
        if re.search(TESTRX, f): continue
        s = SPELL[f]
        ph = sorted(set(h for x in s['path'] for h in grep(TREE, x)))
        bh = sorted(set(h for x in s['base'] for h in grep(TREE, x, regex=True)))
        ih = sorted(set(h for x in s['imp'] for h in grep(TREE, x, scope=s['scope'])))
        sy = {x: grep(TREE, x) for x in s['sym']}
        un = sorted(set(ph + bh + ih)); perpr[n] |= set(un)
        out['files'][f] = {'pr': n, 'path_hits': ph, 'basename_hits': bh, 'import_hits': ih, 'symbol_hits': sy, 'union': un}
        print('== #%s %s' % (n, f))
        print('   PATH     %s: %d file(s)' % (s['path'], len(ph)))
        print('   BASENAME %s: %d file(s)' % (s['base'], len(bh)))
        print('   IMPORT   %s (scope %s): %d file(s)' % (s['imp'], s['scope'], len(ih)))
        for h in un: print('     %s%s' % (h, '   [changed by this batch]' if h in P['union'] else ''))
        for x, hs in sy.items(): print('   SYMBOL %s (INFO): %d test file(s)%s' % (x, len(hs), (': ' + ', '.join(os.path.basename(y) for y in hs[:10]) + (' …' if len(hs) > 10 else '')) if hs else ''))
for n in K['order']:
    if TREE != P['end_tree']: break
    found = [t for t in OWN_POS[n] if t in perpr[n]]
    ok = len(found) == len(OWN_POS[n])
    print('CT-POS #%s its own test(s) found by the census: %d of %d %s' % (n, len(found), len(OWN_POS[n]), 'OK' if ok else 'FAIL'))
    if not ok: bad.append('CT-POS #%s: its own test %s is not found — the census is blind' % (n, sorted(set(OWN_POS[n]) - set(found))))
    for t in OWN_NOPATH.get(n, []):
        print('OWN-TEST-NO-CHANGED-PATH #%s %s (reads no changed path; the gate RUNS it anyway; in the census union: %s)' % (n, t, t in perpr[n]))
neg = grep(TREE, 'Blockchain/Dev/deployment/azure/no-such-script-gate44.sh')
print('CT-NEG a nonsense path: %d file(s) %s' % (len(neg), 'OK' if not neg else 'FAIL'))
if neg: bad.append('CT-NEG found %s' % neg)
allt = sorted(set().union(*perpr.values()))
if TREE == P['end_tree']:
    new_tests = [t for n in K['order'] for t in P['prs'][n]['files'] if re.search(TESTRX, t)]
    newly = [x for x in new_tests if subprocess.run(['git', '-C', CL, 'cat-file', '-e', '%s:%s' % (P['develop'], x)], capture_output=True).returncode != 0]
    print('CT-TREE the batch\'s test files: %d of %d are NEW (absent at develop %s): %s' % (len(newly), len(new_tests), P['develop'][:12], ', '.join(os.path.basename(x) for x in newly)))
    if len(newly) != 3: bad.append('CT-TREE expected the 3 new test files absent at develop, got %d — the tree argument is not being honoured' % len(newly))
    kn = KNOWN in allt
    print('CT-KNOWN %s listed: %s %s' % (os.path.basename(KNOWN), kn, 'OK' if kn else 'FAIL'))
    if not kn: bad.append('CT-KNOWN the pre-existing template suite is not listed — the env.example spelling is blind')
out['all_tests'] = allt; out['own_nopath'] = OWN_NOPATH
print('CENSUS UNION (PATH + BASENAME + IMPORT, at %s): %d test file(s):' % (TREE[:12], len(allt))); [print('  ' + t) for t in allt]
json.dump(out, open(os.path.join(G, 'testrefs_gate44.json' if TREE == P['end_tree'] else 'testrefs_gate44.%s.json' % TREE[:12]), 'w'), indent=1)
print('TESTREFS %s: %d control problem(s)' % ('PASS' if not bad else 'FAIL', len(bad))); [print('  - ' + b) for b in bad]
raise SystemExit(1 if bad else 0)
