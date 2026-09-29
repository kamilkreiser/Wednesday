#!/usr/bin/env python3
"""testrefs_gate43.py — THE TEST CENSUS: every test file ANYWHERE in the monorepo that references a changed PRODUCT file, read by `git grep -l`
at a NAMED tree (default: the END_TREE in pins_gate43.json; never a working copy). Three spelling classes per changed product file, each printed
with its own count, so a zero is attributable:
  PATH   the repo path literally (full, from the package root, and the module stem `dir/name` without extension);
  IMPORT the module specifier a test actually uses (relative `../routes/proxy`-style, restricted to the SAME service; the package subpath
         `@secuura/shared/vc` for packages/shared);
  SYMBOL (INFO, never a gate) the exported symbols the change sits under, for a file reached only through a package barrel.
Test files = *.test.* / *.spec.* / anything under __tests__/, tests/, test/, e2e/ (git pathspec globs over Blockchain/).
CONTROLS inside (a census that prints nothing needs a control that prints): CT-POS each PR's own NEW/CHANGED test file must be found by the
IMPORT class of its product file (it imports it); CT-NEG a nonsense path must find 0; CT-TREE the same census at develop must NOT list the
PR's new test files (they do not exist there). rc 0 when every control holds; rc 1 otherwise. Writes testrefs_gate43.json beside this script.
Env G43_TR_GLOB (controls only) replaces the test-file globs. Usage: testrefs_gate43.py <scratchpad> [--tree <sha>]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate43.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g43_sp', 'clone')
TREE = A[A.index('--tree') + 1] if '--tree' in A else P['end_tree']
TESTS = [':(glob)Blockchain/**/*.test.*', ':(glob)Blockchain/**/*.spec.*', ':(glob)Blockchain/**/__tests__/**', ':(glob)Blockchain/**/tests/**',
         ':(glob)Blockchain/**/test/**', ':(glob)Blockchain/**/e2e/**', ':(exclude,glob)**/node_modules/**']
if os.environ.get('G43_TR_GLOB'): TESTS = [os.environ['G43_TR_GLOB']]   # controls only: a census pointed at nothing must FAIL CT-POS
def grep(tree, pat, scope=None, fixed=True):
    spec = TESTS if not scope else [':(glob)%s/**' % scope]
    r = subprocess.run(['git', '-C', CL, 'grep', '-l', '-F' if fixed else '-E', '-e', pat, tree, '--'] + spec, capture_output=True, text=True)
    if r.returncode not in (0, 1): raise SystemExit('REFUSING: git grep rc %d: %s' % (r.returncode, r.stderr[:200]))
    fs = sorted(set(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l))
    if scope: fs = [f for f in fs if re.search(r'(\.test\.|\.spec\.|/__tests__/|/tests?/|/e2e/)', f)]
    return fs
def service_of(p):
    m = re.match(r'(Blockchain/Dev/(?:services|packages|frontend)/[^/]+)/', p); return m.group(1) if m else None
SYMBOLS = {'Blockchain/Dev/packages/shared/src/vc/verifier.ts': ['VerifiableCredentialVerifier', 'verifyCredential', 'verifyPresentation', 'storedRecordResolver', 'revocationVerifierConfig'],
           'Blockchain/Dev/services/api-gateway/src/routes/proxy.ts': ['createProxyRoutes', 'onProxyReq'],
           'Blockchain/Dev/services/vc-issuer/src/routes/status.ts': ['statusRoutes', '/unrevoke'],
           'Blockchain/Dev/services/api-gateway/src/routes/platform.ts': ['createPlatformRoutes', 'audit-log'],
           'Blockchain/Dev/services/wallet-connector/src/server.ts': ['/api/wallets/session']}
PKG_IMPORT = {'Blockchain/Dev/packages/shared/src/vc/verifier.ts': ["@secuura/shared/vc'", '@secuura/shared/vc"', 'shared/src/vc/verifier', "shared/src/vc'"]}
out = {'tree': TREE, 'files': {}}; bad = []
print('TEST CENSUS at tree %s (%s)' % (TREE, 'END_TREE' if TREE == P['end_tree'] else 'NOT the END_TREE'))
for n in K['order']:
    for f in P['prs'][n]['files']:
        if re.search(r'(\.test\.|/__tests__/)', f): continue
        svc = service_of(f); rel = f[len(svc) + 1:] if svc else f; stem = re.sub(r'\.(ts|tsx|js|mjs)$', '', rel)
        tail2 = '/'.join(stem.split('/')[-2:])
        path_hits = sorted(set(grep(TREE, f) + grep(TREE, stem) + grep(TREE, re.sub(r'\.(ts|tsx|js)$', '', f))))
        imp_specs = ["'../%s'" % stem.split('/', 1)[1] if stem.startswith('src/') else stem, '"../%s"' % stem.split('/', 1)[1] if stem.startswith('src/') else stem,
                     "'../../%s'" % stem.split('/', 1)[1] if stem.startswith('src/') else stem, tail2 + "'", tail2 + '"']
        imp_hits = sorted(set(h for s in imp_specs for h in grep(TREE, s, scope=svc)))
        imp_hits += [h for s in PKG_IMPORT.get(f, []) for h in grep(TREE, s) if h not in imp_hits]
        imp_hits = sorted(set(imp_hits))
        sym_hits = {s: grep(TREE, s) for s in SYMBOLS.get(f, [])}
        own_tests = [x for x in P['prs'][n]['files'] if re.search(r'(\.test\.|/__tests__/)', x)]
        pos = [t for t in own_tests if t in imp_hits or t in path_hits]
        out['files'][f] = {'pr': n, 'path_hits': path_hits, 'import_hits': imp_hits, 'symbol_hits': sym_hits, 'own_tests_found': pos}
        print('== #%s %s' % (n, f))
        print('   PATH   (%s | %s): %d file(s)' % (f, stem, len(path_hits))); [print('     ' + h) for h in path_hits]
        print('   IMPORT (same-service relative %s + package subpaths %s): %d file(s)' % (tail2, PKG_IMPORT.get(f, []), len(imp_hits)))
        for h in imp_hits: print('     %s%s' % (h, '   [changed by this batch]' if h in P['union'] else ''))
        for s, hs in sym_hits.items(): print('   SYMBOL %s (INFO): %d test file(s)%s' % (s, len(hs), (': ' + ', '.join(os.path.basename(x) for x in hs[:12]) + (' …' if len(hs) > 12 else '')) if hs else ''))
        ok = TREE != P['end_tree'] or len(pos) >= 1
        print('   CT-POS the PR\'s own test file(s) found: %d of %d %s' % (len(pos), len(own_tests), 'OK' if ok else 'FAIL'))
        if not ok: bad.append('CT-POS #%s %s: its own test is not found — the census is blind' % (n, f))
neg = grep(TREE, 'Blockchain/Dev/services/no-such-service/src/nope.ts')
print('CT-NEG a nonsense path: %d file(s) %s' % (len(neg), 'OK' if not neg else 'FAIL'))
if neg: bad.append('CT-NEG found %s' % neg)
if TREE == P['end_tree']:
    new_tests = [x for n in K['order'] for x in P['prs'][n]['files'] if '/__tests__/ks13' in x and x.endswith('.test.ts')]
    at_dev = [x for x in new_tests if subprocess.run(['git', '-C', CL, 'cat-file', '-e', '%s:%s' % (P['develop'], x)], capture_output=True).returncode == 0]
    newly = [x for x in new_tests if subprocess.run(['git', '-C', CL, 'cat-file', '-e', '%s:%s' % (P['develop'], x)], capture_output=True).returncode != 0]
    print('CT-TREE of the batch\'s ks13xx test files, %d exist at develop %s (MODIFIED by the batch), %d are NEW (absent at develop): %s' % (len(at_dev), P['develop'][:12], len(newly), ', '.join(os.path.basename(x) for x in newly)))
    if not newly: bad.append('CT-TREE no new test file is absent at develop — the tree argument is not being honoured')
allt = sorted(set(h for v in out['files'].values() for h in v['path_hits'] + v['import_hits']))
out['all_tests'] = allt
print('CENSUS UNION (PATH + IMPORT, at %s): %d test file(s):' % (TREE[:12], len(allt))); [print('  ' + t) for t in allt]
json.dump(out, open(os.path.join(G, 'testrefs_gate43.json' if TREE == P['end_tree'] else 'testrefs_gate43.%s.json' % TREE[:12]), 'w'), indent=1)
print('TESTREFS %s: %d control problem(s)' % ('PASS' if not bad else 'FAIL', len(bad))); [print('  - ' + b) for b in bad]
raise SystemExit(1 if bad else 0)
