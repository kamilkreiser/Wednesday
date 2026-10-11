#!/usr/bin/env python3
"""c3_cells_gate86.py — the RUN instruments for gate86 (a batch of four PRs). Everything runs in a scratch tree OUTSIDE every git repo (`git archive` of a revision + a COPY of an installed
node_modules for the vitest PRs), never in a builder's worktree and never in the shared checkout. NO npm, NO npx, NO install, NO network: every tool is a binary inside the copied
node_modules/.bin (`vitest`, `tsx`) or `node` / `bash` / `/bin/bash`. Plants are file swaps ASSERTED LANDED and RESTORED by git blob id. Every figure printed is the DRAFTER'S PREDICTION; the gate re-measures.

  prep      --repo R --rev REV --tree T [--deps-from DIR --services a,b,c]   T must not exist (canonical /private/tmp/claude-501/... path under no repo). Extracts REV (Blockchain/Dev, Projects Documents,
                                                                           systemTest/__tests__, .githooks); with --deps-from DIR (a Blockchain/Dev directory somebody else installed: a READ of it) copies
                                                                           node_modules + packages/shared/dist + services/<svc>/node_modules, then `nmcheck`. Without --deps-from: the shell / docs PRs.
  nmcheck   --tree T
  vitest    --tree T --out O --repo R --pr N [--suites]       #1451 / #1452. (G) head product + head tests; (R) BASE *.openapi.ts + head tests = "the tests alone"; each test file's passed / failed from the
                                                              JSON totals AND the summed rows AND the text summary; --suites also runs each whole service at head and with the PR's tests excluded
  mutate    --tree T --out O --repo R --pr N                  #1451 / #1452. Drop ONE `required: true` declaration at a time (11 mutants over the batch): the matching test must go red, every other cell green
  shell     --tree T --out O --repo R --pr N                  #1454 / #1455. (G) head; (R) the BASE product + head test; sibling suites before / after; tamper controls; env -i, /bin/bash
  compose   --clone C --develop D --head 1451=H --head 1452=H --head 1454=H --head 1455=H --out O      merge-tree in YOUR clone: each PR onto develop, the six pairs, and ALL 24 merge orders with the keep-both
                                                              applied to the two docs only; checks the composed docs, the yaml, the code blobs and the ORDER-INDEPENDENCE of the four doc blocks
  regen     --tree T --out O                                  `tsx scripts/generate-openapi.ts --check` on a composed tree (the yaml the keep-both left == what the .openapi.ts files generate) + a tamper control
  docs      --tree T --out O [--expect-blocks 55,56,57,58,59]  html_docs_matrix on the tree + the per-fragment COUNT + drop / duplicate controls (the matrix is blind to both)
  --selftest
rc 0 all pass / 1 a FAIL (a finding, a blind control) / 2 refused."""
import hashlib, itertools, json, os, re, shutil, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate86 import K, PR, Tally, git, wgit, show, blob, req, opt, resolvable, blob_of_bytes, canonical_tmp, must_be_outside, extract, run as lrun, exact_tail_insert, TAIL, HEX40

DEV = 'Blockchain/Dev'; FLOW, CHEAT = K['known_develop_overlap']; YAML = K['shared_yaml']
EXPECT_RED = {  # the READY ledgers: the test files alone at the base product: passed / failed per test file (service)
    '1451': {'anchoring': (3, 2), 'staking': (3, 1), 'transfer': (3, 3)}, '1452': {'analytics': (4, 1), 'm365-integration': (4, 2), 'api-gateway': (3, 2)}}
EXPECT_GREEN = {'1451': {'anchoring': 5, 'staking': 4, 'transfer': 6}, '1452': {'analytics': 5, 'm365-integration': 6, 'api-gateway': 5}}
SHELL_EXPECT = {'1454': {'G': (7, 0, 0), 'R': (3, 4, 1)}, '1455': {'G': (6, 0, 0), 'R': (5, 1, 1)}}   # passed, failed, rc at head / base product + head test
SHELL_SUITE = {'1454': 'Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh', '1455': 'Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh'}
SHELL_PRODUCT = {'1454': 'Blockchain/Dev/scripts/dev-reload.sh', '1455': 'Blockchain/Dev/env.local.example'}
SIBLINGS = ['Blockchain/Dev/scripts/__tests__/stack_guard.test.sh', 'Blockchain/Dev/scripts/__tests__/stack_env.test.sh']


# ---------------------------------------------------------------- helpers
def need_canonical(path, what):
    if not canonical_tmp(os.path.dirname(os.path.abspath(path)) if not os.path.exists(path) else path):
        raise SystemExit('REFUSED: %s %s is not a canonical /private/tmp/claude-501/ path under no git repository' % (what, path))
    must_be_outside(path, what)


def hid(tree, rel):
    fp = os.path.join(tree, rel); return blob_of_bytes(open(fp, 'rb').read()) if os.path.isfile(fp) else ''


class Plant:
    """swap files in the tree for given bytes; assert LANDED (blob id == expected, != before) and restore by blob id."""
    def __init__(self, tree): self.tree = tree; self.orig = {}
    def put(self, rel, data):
        fp = os.path.join(self.tree, rel)
        if rel not in self.orig: self.orig[rel] = open(fp, 'rb').read()
        before = blob_of_bytes(open(fp, 'rb').read()); open(fp, 'wb').write(data if isinstance(data, bytes) else data.encode('utf-8'))
        after = hid(self.tree, rel)
        return before, after, after == blob_of_bytes(data), before != after
    def restore(self):
        bad = []
        for rel, data in self.orig.items():
            fp = os.path.join(self.tree, rel); open(fp, 'wb').write(data)
            if hid(self.tree, rel) != blob_of_bytes(data): bad.append(rel)
        self.orig = {}
        return bad


def svc_of(p): return p.split('/services/')[1].split('/')[0]


def vt(tree, out, name, svc, args, reporter_text=False, timeout=900):
    """the tree's own vitest binary (no npx) in services/<svc>; -> dict with rc, totals (JSON AND summed rows), failing cell titles, files."""
    sd = os.path.join(tree, DEV, 'services', svc); js = os.path.join(out, name + '.json'); os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, '_tmp'); os.makedirs(tmp, exist_ok=True)
    cmd = [os.path.join(tree, DEV, 'node_modules', '.bin', 'vitest'), 'run'] + list(args)
    cmd += (['--reporter=default', '--reporter=json', '--outputFile.json=' + js] if reporter_text else ['--reporter=json', '--outputFile=' + js])
    if os.path.exists(js): os.remove(js)
    t0 = time.time(); rc, so, se = lrun(cmd, sd, env={'TMPDIR': tmp}, timeout=timeout)
    open(os.path.join(out, name + '.stdout'), 'w').write(so); open(os.path.join(out, name + '.stderr'), 'w').write(se)
    res = {'name': name, 'rc': rc, 'secs': round(time.time() - t0, 1), 'json': os.path.isfile(js), 'stdout': so, 'stderr': se}
    if res['json']:
        j = json.load(open(js)); rows = [(r['name'], a.get('title') or '', a['status']) for r in j['testResults'] for a in r['assertionResults']]
        res.update({'total': j['numTotalTests'], 'passed': j['numPassedTests'], 'failed': j['numFailedTests'], 'files': len(j['testResults']), 'rows': len(rows),
                    'rows_passed': sum(1 for x in rows if x[2] == 'passed'), 'rows_failed': sum(1 for x in rows if x[2] == 'failed'),
                    'failing': [(os.path.basename(x[0]), x[1]) for x in rows if x[2] == 'failed'], 'suites_failed_to_load': [os.path.basename(r['name']) for r in j['testResults'] if r['status'] == 'failed' and not r['assertionResults']]})
        res['consistent'] = res['total'] == res['rows'] and res['passed'] == res['rows_passed'] and res['failed'] == res['rows_failed']
    return res


def line(r):
    if not r.get('json'): return '%s rc=%s NO JSON (a run that wrote no report is NOT RUN, never a pass) stderr: %s' % (r['name'], r['rc'], r['stderr'][-200:].strip())
    return '%s rc=%d %d passed / %d failed of %d in %d file(s); summed rows %d/%d/%d %s; load failures %s; %.1fs' % (r['name'], r['rc'], r['passed'], r['failed'], r['total'], r['files'], r['rows_passed'], r['rows_failed'], r['rows'],
                                                                                                              'AGREE' if r['consistent'] else 'DISAGREE <<<', r['suites_failed_to_load'] or 'none', r['secs'])


# ---------------------------------------------------------------- prep / nmcheck
def nmcheck(tree, svcs=()):
    t = Tally(); lockp = os.path.join(tree, DEV, 'package-lock.json'); hp = os.path.join(tree, DEV, 'node_modules', '.package-lock.json')
    if not (os.path.isfile(lockp) and os.path.isfile(hp)):
        t.check('NM0', False, 'package-lock.json or node_modules/.package-lock.json missing in %s' % tree); return t.end()
    lock = json.load(open(lockp))['packages']; hidl = json.load(open(hp))['packages']
    mism = [k for k, v in hidl.items() if k in lock and lock[k].get('version') != v.get('version')]; extra = [k for k in hidl if k not in lock]
    miss = [k for k, v in lock.items() if k.startswith('node_modules/') and k not in hidl and not v.get('optional') and not v.get('link')]
    t.check('NM1', len(hidl) > 1000 and not mism and not extra and not miss, 'hidden lockfile %d packages vs the revision\'s package-lock.json %d packages: version mismatches %d %s, installed-but-not-in-lock %d, non-optional-in-lock-but-not-installed %d %s' % (len(hidl), len(lock), len(mism), mism[:3], len(extra), len(miss), miss[:3]))
    l2 = dict(lock); l2['node_modules/zz-planted'] = {'version': '0.0.1'}; h2 = dict(hidl); h2['node_modules/zz-planted'] = {'version': '9.9.9'}
    t.check('NM1-CONTROL', [k for k, v in h2.items() if k in l2 and l2[k].get('version') != v.get('version')] == ['node_modules/zz-planted'], 'CONTROL: a planted package at a different version reads as a mismatch (the comparison can fail)')
    for b in ('vitest', 'tsx', 'tsc'):
        fp = os.path.join(tree, DEV, 'node_modules', '.bin', b); t.check('NM2', os.path.exists(fp), 'node_modules/.bin/%s present: %s' % (b, os.path.exists(fp)))
    sh_ = os.path.join(tree, DEV, 'packages', 'shared', 'dist'); t.check('NM4', os.path.isdir(sh_) and any(True for _ in os.scandir(sh_)), 'packages/shared/dist present and non-empty: %s' % os.path.isdir(sh_))
    for s in svcs:
        d = os.path.join(tree, DEV, 'services', s, 'node_modules'); t.check('NM5', os.path.isdir(d), 'services/%s/node_modules present: %s' % (s, os.path.isdir(d)))
    cwd = os.path.join(tree, DEV)
    rc, so, _ = lrun([os.path.join(tree, DEV, 'node_modules', '.bin', 'vitest'), '--version'], cwd); rc3, so3, _ = lrun(['node', '--version'], cwd)
    t.info('NM3', 'versions: vitest %s | node %s (the builders\': vitest 4.1.11, node v24.7.0)' % (so.strip(), so3.strip()))
    return t.end()


def prep(A):
    repo = req(A, '--repo'); rev = req(A, '--rev', True); tree = req(A, '--tree'); deps = opt(A, '--deps-from'); svcs = [s for s in (opt(A, '--services', '') or '').split(',') if s]
    need_canonical(tree, 'tree')
    if os.path.exists(tree): print('REFUSED: %s exists (build each attempt in its own new directory; never reuse or delete)' % tree); return 2
    if not resolvable(repo, rev): print('REFUSED: %s not in %s' % (rev, repo)); return 2
    os.makedirs(tree); n = extract(repo, rev, [DEV, 'Projects Documents', 'systemTest/__tests__', '.githooks'], tree)
    print('extracted %d files of %s into %s' % (n, rev[:12], tree)); t = Tally()
    t.check('PREP-NOREPO', canonical_tmp(tree) and not os.path.exists(os.path.join(tree, '.git')), 'the tree is outside every git repository (no .git on any parent): %s' % canonical_tmp(tree))
    probe = [DEV + '/package-lock.json', YAML, FLOW, CHEAT]; same = [(q, hid(tree, q) == blob(repo, rev, q).split()[-1][:40] if blob(repo, rev, q) else False) for q in probe]
    t.check('PREP-BLOBS', all(v for _, v in same), 'the tree\'s files equal the revision\'s blobs (recomputed ids vs ls-tree) for %s' % [(os.path.basename(q)[:24], v) for q, v in same])
    if deps:
        for rel in ['node_modules', 'packages/shared/dist'] + ['services/%s/node_modules' % s for s in svcs]:
            src = os.path.join(deps, rel)
            if not os.path.isdir(src): print('REFUSED: %s is not a directory' % src); return 2
            dst = os.path.join(tree, DEV, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            cp = subprocess.run(['cp', '-R', src, dst], capture_output=True, text=True)
            if cp.returncode != 0: print('REFUSED: cp -R %s failed: %s' % (src, cp.stderr[:200])); return 2
        print('copied node_modules + packages/shared/dist + %s from %s' % (['services/%s/node_modules' % s for s in svcs], deps))
        return 0 if (nmcheck(tree, svcs) == 0 and t.end() == 0) else 1
    return t.end()


# ---------------------------------------------------------------- vitest (contract PRs)
def vitest(A):
    n = req(A, '--pr'); P = PR(n); tree = req(A, '--tree'); out = req(A, '--out'); repo = req(A, '--repo'); t = Tally()
    if n not in EXPECT_RED: raise SystemExit('REFUSED: vitest is for #1451 / #1452')
    base, head = P['base'], P['head_expected']; code = [p for p, v in P['paths'].items() if p.endswith('.openapi.ts')]; tests = [p for p, v in P['paths'].items() if v['role'] == 'test']
    pl = Plant(tree)
    ok0 = True
    t.check('V0', ok0 and all(hid(tree, p) == blob_of_bytes(show(repo, head, p).encode()) for p in code + tests), 'the tree holds the HEAD bytes of the %d .openapi.ts and %d test files (blob ids recomputed from the files vs git show of the head)' % (len(code), len(tests)))
    for tp in tests:
        svc = svc_of(tp); name = os.path.basename(tp); rel = 'src/__tests__/' + name
        g = vt(tree, out, 'G_%s' % svc, svc, [rel], reporter_text=True)
        t.check('V-G-%s' % svc, g.get('json') and g['consistent'] and g['rc'] == 0 and (g['passed'], g['failed']) == (EXPECT_GREEN[n][svc], 0) and not g['suites_failed_to_load'], 'G (head product + head test) %s: %s | want %d passed / 0 failed' % (name[:40], line(g), EXPECT_GREEN[n][svc]))
        landed = [pl.put(p, show(repo, base, p)) for p in code if svc_of(p) == svc]
        okl = all(x[3] and x[2] for x in landed) if landed else False
        r = vt(tree, out, 'R_%s' % svc, svc, [rel], reporter_text=True)
        msgs = sorted(set(re.findall(r'(expected [^\n]{0,50}? to (?:be|equal) [^\n/]{0,20})', r['stdout'] + r['stderr'])))[:3]
        wp, wf = EXPECT_RED[n][svc]
        t.check('V-R-%s' % svc, bool(okl and r.get('json') and r['consistent'] and r['rc'] == 1 and (r['passed'], r['failed']) == (wp, wf) and not r['suites_failed_to_load']), 'R (BASE .openapi.ts + head test) %s | plant LANDED (blob changed, bytes == git show base): %s | %s | want %d passed / %d failed (the READY) | assertion messages %s' % (name[:40], okl, line(r), wp, wf, msgs))
        if r.get('json'): t.info('V-R-%s-NAMES' % svc, 'red cells: %s' % [x[1][:70] for x in r['failing']])
        bad = pl.restore(); t.check('V-RESTORE-%s' % svc, not bad and all(hid(tree, p) == blob_of_bytes(show(repo, head, p).encode()) for p in code), 'restored by blob id to the head bytes: %s' % (not bad))
    if '--suites' in A:
        for svc in sorted(EXPECT_GREEN[n]):
            names = [os.path.basename(p) for p in tests if svc_of(p) == svc]
            h = vt(tree, out, 'SUITE_head_%s' % svc, svc, [], reporter_text=True)
            b = vt(tree, out, 'SUITE_without_pr_tests_%s' % svc, svc, ['--exclude', '**/node_modules/**'] + sum([['--exclude', '**/' + x] for x in names], []), reporter_text=True)
            d = (h['total'] - b['total']) if h.get('json') and b.get('json') else None
            t.check('V-SUITE-%s' % svc, bool(h.get('json') and b.get('json') and d == EXPECT_GREEN[n][svc] and h['failed'] - b['failed'] == 0), 'whole service %s: head %s || the PR\'s test file excluded %s || delta tests %s (want %d) and delta failed %s (want 0: no new red; pre-existing reds are the same in both)' % (svc, line(h)[:130], line(b)[:130], d, EXPECT_GREEN[n][svc], (h['failed'] - b['failed']) if d is not None else 'n/a'))
            if h.get('json'): t.info('V-SUITE-%s-RED' % svc, 'failing cells at head (pre-existing if the same without the PR): %s' % [x[0][:34] + '::' + x[1][:40] for x in h['failing']][:5])
    else:
        t.info('V-SUITE', 'NOT RUN by name (no --suites): the whole-service before / after runs; the READY quotes anchoring 365 -> 370 (1 failed both), staking 61 -> 65, transfer 85 -> 91; analytics 32 -> 37, m365 57 -> 63, api-gateway 869 -> 874')
    return t.end()


# ---------------------------------------------------------------- mutate (contract PRs): drop ONE declaration at a time
def decl_sites(text):
    """-> [(kind, start, end, path_string, method)] one per `required: true` declaration added by the PR: kind 'line' (a `required: true,` line with its comment line) or 'inline' (`, required: true }`)."""
    L = text.split('\n'); out = []; off = [0]
    for l in L: off.append(off[-1] + len(l) + 1)
    def op_of(i):
        pth = meth = None
        for k in range(i, -1, -1):
            if pth is None and re.match(r"\s*path:\s*['\"]([^'\"]+)['\"]", L[k]): pth = re.match(r"\s*path:\s*['\"]([^'\"]+)['\"]", L[k]).group(1)
            if meth is None and re.match(r"\s*method:\s*['\"](\w+)['\"]", L[k]): meth = re.match(r"\s*method:\s*['\"](\w+)['\"]", L[k]).group(1)
            if pth and meth: break
        return pth, meth
    for i, l in enumerate(L):
        if l.strip() == 'required: true,' and i > 0 and re.match(r'\s*// KS-\d+', L[i - 1]):
            out.append(('line', off[i - 1], off[i + 1], *op_of(i)))
        elif ', required: true }' in l and i > 0 and re.match(r'\s*// KS-\d+', L[i - 1]):
            s = off[i] + l.index(', required: true }'); out.append(('inline', s, s + len(', required: true'), *op_of(i)))
    return out


def mutate(A):
    n = req(A, '--pr'); P = PR(n); tree = req(A, '--tree'); out = req(A, '--out'); repo = req(A, '--repo'); t = Tally()
    if n not in EXPECT_RED: raise SystemExit('REFUSED: mutate is for #1451 / #1452')
    head = P['head_expected']; code = [p for p in P['paths'] if p.endswith('.openapi.ts')]; tot = 0
    for cp in code:
        svc = svc_of(cp); txt = show(repo, head, cp); sites = decl_sites(txt); tot += len(sites)
        tp = [p for p, v in P['paths'].items() if v['role'] == 'test' and svc_of(p) == svc][0]; rel = 'src/__tests__/' + os.path.basename(tp)
        t.check('M-SITES-%s' % svc, len(sites) >= 1 and all(s[3] for s in sites), '%s: %d declaration site(s) found in the head file: %s' % (os.path.basename(cp), len(sites), [(s[0], s[3], s[4]) for s in sites]))
        g = vt(tree, out, 'MG_%s' % svc, svc, [rel])
        for k, (kind, s, e, pth, meth) in enumerate(sites):
            pl = Plant(tree); new = txt[:s] + txt[e:]; landed = pl.put(cp, new)
            r = vt(tree, out, 'M_%s_%d' % (svc, k), svc, [rel]); bad = pl.restore()
            hit = [x for x in r.get('failing', []) if re.search(re.escape(pth) + r'(?![\w/{-])', x[1])]
            ok = bool(landed[2] and landed[3] and not bad and r.get('json') and r['consistent'] and r['failed'] >= 1 and hit and not r['suites_failed_to_load'])
            t.check('M-%s-%d' % (svc, k), ok, 'drop the %s declaration for %s %s: plant LANDED %s; guard test %d passed / %d failed; red cell(s) naming that path: %d %s; other red cells: %s; restored by blob id: %s' % (
                kind, (meth or '?').upper(), pth, bool(landed[2] and landed[3]), r.get('passed', -1), r.get('failed', -1), len(hit), [x[1][:46] for x in hit][:2], [x[1][:40] for x in r.get('failing', []) if x not in hit][:2] or 'none', not bad))
        t.check('M-CONTROL-%s' % svc, g.get('json') and g['rc'] == 0 and g['failed'] == 0, 'CONTROL (unmutated head, same file): %s' % line(g))
    t.check('M-TOTAL', tot == P['declared_ops'], 'declaration sites found over the three files: %d == the declared %d operations' % (tot, P['declared_ops']))
    return t.end()


# ---------------------------------------------------------------- shell (#1454 / #1455)
def run_shell(tree, out, name, rel, locale=None):
    """run a shell suite with /bin/bash under a minimal environment from the tree dir. -> dict rc, passes, fails, summary line."""
    os.makedirs(out, exist_ok=True); home = os.path.join(out, '_home'); os.makedirs(home, exist_ok=True); tmp = os.path.join(out, '_tmp'); os.makedirs(tmp, exist_ok=True)
    env = {'HOME': home, 'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'TMPDIR': tmp}
    if locale: env['LC_ALL'] = locale
    p = subprocess.run(['/usr/bin/env', '-i'] + ['%s=%s' % kv for kv in env.items()] + ['/bin/bash', os.path.join(tree, rel)], capture_output=True, cwd=tree)
    so = p.stdout.decode('utf-8', 'replace'); se = p.stderr.decode('utf-8', 'replace')
    open(os.path.join(out, name + '.stdout'), 'w').write(so); open(os.path.join(out, name + '.stderr'), 'w').write(se)
    ok = len(re.findall(r'^(?:ok\s|PASS:)', so, re.M)); bad = len(re.findall(r'^(?:FAIL\s|FAIL:)', so, re.M)); summ = re.findall(r'(\d+) passed, (\d+) failed', so)
    return {'name': name, 'rc': p.returncode, 'ok': ok, 'bad': bad, 'summary': summ[-1] if summ else None, 'tail': so.strip().split('\n')[-1][:100] if so.strip() else '', 'stderr': se[-200:], 'stdout': so, 'fails': [l for l in so.split('\n') if re.match(r'(FAIL\s|FAIL:)', l)]}


def shell(A):
    n = req(A, '--pr'); P = PR(n); tree = req(A, '--tree'); out = req(A, '--out'); repo = req(A, '--repo'); t = Tally()
    if n not in SHELL_SUITE: raise SystemExit('REFUSED: shell is for #1454 / #1455')
    suite, prod = SHELL_SUITE[n], SHELL_PRODUCT[n]; base, head = P['base'], P['head_expected']; pl = Plant(tree); want = SHELL_EXPECT[n]
    t.check('SH0', hid(tree, prod) == blob_of_bytes(show(repo, head, prod).encode()) and hid(tree, suite) == blob_of_bytes(show(repo, head, suite).encode()) and hid(tree, prod) == P['paths'][prod]['head_blob'][:40], 'the tree holds the HEAD bytes of %s and %s (blob ids)' % (os.path.basename(prod), os.path.basename(suite)))
    t.info('SH-BASH', '/bin/bash is %s' % subprocess.run(['/bin/bash', '--version'], capture_output=True, text=True).stdout.split('\n')[0])
    g = run_shell(tree, out, 'G_%s' % n, suite)
    t.check('SH-G', g['rc'] == want['G'][2] and (g['ok'], g['bad']) == want['G'][:2] and (g['summary'] is None or tuple(map(int, g['summary'])) == want['G'][:2]), 'G (head product + head suite) rc %d, lines ok/PASS %d, FAIL %d, summary line %s (want %d passed / %d failed, rc %d); last line: %s' % (g['rc'], g['ok'], g['bad'], g['summary'], want['G'][0], want['G'][1], want['G'][2], g['tail']))
    lan = pl.put(prod, show(repo, base, prod)); r = run_shell(tree, out, 'R_%s' % n, suite); bad = pl.restore()
    t.check('SH-R', bool(lan[2] and lan[3] and not bad and r['rc'] == want['R'][2] and (r['ok'], r['bad']) == want['R'][:2]), 'R (BASE %s + head suite = "the test alone") plant LANDED %s; rc %d, ok/PASS %d, FAIL %d (want %d passed / %d failed, rc %d); restored by blob id: %s' % (os.path.basename(prod), bool(lan[2] and lan[3]), r['rc'], r['ok'], r['bad'], want['R'][0], want['R'][1], want['R'][2], not bad))
    t.info('SH-R-NAMES', 'red cells: %s' % [x[:110] for x in r['fails']])
    if n == '1454':
        txt = show(repo, head, prod); a = 'CONTAINER="${STACK_PREFIX}-$SVC"'
        if txt.count(a) != 1: t.check('SH-MUT1', False, 'anchor %r found %d times (want 1)' % (a, txt.count(a)))
        else:
            lan = pl.put(prod, txt.replace(a, 'CONTAINER="secuura-$SVC"')); m = run_shell(tree, out, 'MUT_literal_%s' % n, suite); bad = pl.restore()
            t.check('SH-MUT1', bool(lan[2] and lan[3] and not bad and m['rc'] == 1 and m['bad'] >= 1), 'tamper: the head script with the slot-1 literal back in CONTAINER: plant LANDED %s; rc %d, FAIL %d (want a red); restored: %s' % (bool(lan[2] and lan[3]), m['rc'], m['bad'], not bad))
    else:
        txt = show(repo, head, prod)
        lan = pl.put(prod, txt.rstrip('\n') + '\nAPI_GATEWAY_PORT=6882\n'); m = run_shell(tree, out, 'MUT_key_%s' % n, suite); bad = pl.restore()
        t.check('SH-MUT1', bool(lan[2] and lan[3] and not bad and m['rc'] == 1 and m['bad'] >= 1), 'tamper: the key re-inserted into the REAL template in the tree: plant LANDED %s; rc %d, FAIL %d (want cell 5 red: %s); restored by blob id: %s' % (bool(lan[2] and lan[3]), m['rc'], m['bad'], [x[:70] for x in m['fails']][:1], not bad))
    gg = run_shell(tree, out, 'G2_%s' % n, suite)
    t.check('SH-G-AFTER', gg['rc'] == want['G'][2] and (gg['ok'], gg['bad']) == want['G'][:2], 'G again after the restores (the tree is back to head): rc %d, %d ok / %d FAIL' % (gg['rc'], gg['ok'], gg['bad']))
    sib_done = []
    for s in SIBLINGS:
        fp = os.path.join(tree, s)
        if not os.path.isfile(fp): t.info('SH-SIB', '%s ABSENT in the tree: not run' % s); continue
        txt = open(fp, encoding='utf-8', errors='replace').read()
        if re.search(r'bootstrap-env\.sh|env\.example', txt): t.info('SH-SIB', '%s names bootstrap-env.sh / env.example: NOT RUN by the hold' % os.path.basename(s)); continue
        a = run_shell(tree, out, 'SIB_head_%s' % os.path.basename(s), s); lan2 = pl.put(prod, show(repo, base, prod)); bb = run_shell(tree, out, 'SIB_base_%s' % os.path.basename(s), s); bad2 = pl.restore(); sib_done.append((s, a))
        same = sorted(a['fails']) == sorted(bb['fails']) and (a['ok'], a['bad']) == (bb['ok'], bb['bad'])
        t.check('SH-SIB-%s' % os.path.basename(s), bool(same and not bad2 and a['ok'] >= 1 and (lan2[3] or True)), 'sibling %s: head rc %d, %d ok / %d FAIL; with the BASE %s in the same tree rc %d, %d ok / %d FAIL; identical FAIL sets (no regression from the PR): %s; restored: %s%s' % (
            os.path.basename(s), a['rc'], a['ok'], a['bad'], os.path.basename(prod), bb['rc'], bb['ok'], bb['bad'], same, not bad2, (' | FAIL lines present at BOTH (read them: the scratch tree is not a git repo, so a cell that asks git answers differently): %s' % [x[:80] for x in a['fails']]) if a['fails'] else ''))
    t.check('SH-SIB-ANY', len(sib_done) >= 1, 'at least one sibling suite ran (a sibling check that ran none is not a pass): %d' % len(sib_done))
    return t.end()


# ---------------------------------------------------------------- compose
def sh_git(clone, args, env=None, inp=None):
    must_be_outside(clone, 'git %s' % args[0]); e = dict(os.environ); e.pop('GIT_SSH_COMMAND', None); e.update(env or {})
    e.setdefault('GIT_AUTHOR_NAME', 'gate86'); e.setdefault('GIT_AUTHOR_EMAIL', 'gate86@invalid'); e.setdefault('GIT_COMMITTER_NAME', 'gate86'); e.setdefault('GIT_COMMITTER_EMAIL', 'gate86@invalid')
    p = subprocess.run(['git', '-C', clone] + list(args), capture_output=True, env=e, input=inp)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def merge_tree(clone, a, b):
    rc, o, e = sh_git(clone, ['merge-tree', '--write-tree', '--name-only', a, b]); lines = o.split('\n'); tree = lines[0].strip(); names = []
    for l in lines[1:]:
        if not l.strip(): break
        names.append(l.strip())
    return rc, tree, names, e


def read_blob(clone, commit_or_tree, path):
    rc, o, e = sh_git(clone, ['show', '%s:%s' % (commit_or_tree, path)]); return o if rc == 0 else None


def keep_both(ours_doc, fragment):
    """the MERGE SEAT's keep-both for a tail append: `ours_doc` (ends with the closing tags) + the PR's fragment inserted immediately before them. Refuses a duplicate or a doc without the tail."""
    if not ours_doc.endswith(TAIL): raise ValueError('doc does not end with the closing tags')
    if fragment in ours_doc: raise ValueError('fragment already present')
    return ours_doc[:-len(TAIL)] + fragment + TAIL


def tree_with(clone, base_tree, updates):
    """a new tree = base_tree with {path: blob_sha} replaced (a temp index; write verbs in YOUR clone only)."""
    idx = os.path.join(tempfile.mkdtemp(prefix='g86idx', dir='/private/tmp/claude-501'), 'index'); env = {'GIT_INDEX_FILE': idx}
    rc, o, e = sh_git(clone, ['read-tree', base_tree], env); assert rc == 0, e
    for p, b in updates.items():
        rc, o, e = sh_git(clone, ['update-index', '--cacheinfo', '100644,%s,%s' % (b, p)], env); assert rc == 0, e
    rc, o, e = sh_git(clone, ['write-tree'], env); assert rc == 0, e
    return o.strip()


def hash_blob(clone, text):
    rc, o, e = sh_git(clone, ['hash-object', '-w', '--stdin'], inp=text.encode('utf-8')); assert rc == 0, e
    return o.strip()


def commit_of(clone, tree, parents, msg):
    args = ['commit-tree', tree] + sum([['-p', p] for p in parents], []) + ['-m', msg]; rc, o, e = sh_git(clone, args); assert rc == 0, e
    return o.strip()


def fragment_of(clone, n, doc):
    P = PR(n); b = read_blob(clone, P['base'], doc); h = read_blob(clone, P['head_expected'], doc); ok, frag, why = exact_tail_insert(b, h)
    assert ok, (n, doc, why); return frag


def compose(A):
    clone = req(A, '--clone'); dev = req(A, '--develop', True); out = req(A, '--out'); heads = dict(a.split('=') for i, a in enumerate(A) if i and A[i - 1] == '--head'); t = Tally()
    must_be_outside(clone, 'compose clone'); os.makedirs(out, exist_ok=True)
    if sorted(heads) != sorted(K['prs']): raise SystemExit('REFUSED: --head for exactly %s' % sorted(K['prs']))
    for n, h in heads.items():
        if h != PR(n)['head_expected']: raise SystemExit('REFUSED: #%s --head differs from the kit pin (a wrong value: re-draft)' % n)
        if not resolvable(clone, h): raise SystemExit('REFUSED: %s not in %s (fetch BY SHA into the clone)' % (h[:12], clone))
    if not resolvable(clone, dev): raise SystemExit('REFUSED: develop %s not in %s' % (dev[:12], clone))
    DOCS = [FLOW, CHEAT]; frags = {(n, d): fragment_of(clone, n, d) for n in heads for d in DOCS}
    # --- single and pairwise merges (INFO: what a plain merge does)
    for n in sorted(heads):
        rc, tr, names, e = merge_tree(clone, dev, heads[n]); t.info('C-SOLO-%s' % n, 'develop + #%s: rc %d, conflicted paths %s' % (n, rc, [x.split('/')[-1][:34] for x in names]))
    for a, b in itertools.combinations(sorted(heads), 2):
        rc, tr, names, e = merge_tree(clone, heads[a], heads[b]); t.info('C-PAIR-%s-%s' % (a, b), '#%s vs #%s: rc %d, conflicted paths %s' % (a, b, rc, [x.split('/')[-1][:34] for x in names]))
    # --- control: a conflict OUTSIDE the docs is classified as such
    dtree = sh_git(clone, ['log', '-1', '--format=%T', dev])[1].strip(); se = 'Blockchain/Dev/scripts/stack_env.sh'; orig = read_blob(clone, dev, se)
    ca = commit_of(clone, tree_with(clone, dtree, {se: hash_blob(clone, orig + '# gate86 control A\n')}), [dev], 'ctl A'); cb = commit_of(clone, tree_with(clone, dtree, {se: hash_blob(clone, orig + '# gate86 control B\n')}), [dev], 'ctl B')
    rc, tr, names, e = merge_tree(clone, ca, cb)
    t.check('C-CONTROL-CODE', rc == 1 and names == [se], 'CONTROL: two synthetic commits editing the same tail of stack_env.sh read rc %d with conflicted %s (a code conflict is detectable by this instrument)' % (rc, names))
    rc, tr, names, e = merge_tree(clone, dev, dev); t.check('C-CONTROL-NOOP', rc == 0 and names == [], 'CONTROL: develop merged with itself reads rc %d, no conflicts' % rc)
    # --- all 24 orders, memoised by prefix; docs keep-both applied by this instrument (the MERGE SEAT does it in reality)
    dev_docs = {d: read_blob(clone, dev, d) for d in DOCS}; memo = {}; steps = []
    dev_commit = dev
    def advance(prefix):
        if prefix in memo: return memo[prefix]
        if not prefix: memo[prefix] = (dev_commit, None); return memo[prefix]
        cur, _ = advance(prefix[:-1]); n = prefix[-1]; rc, tr, names, e = merge_tree(clone, cur, heads[n])
        upd = {}; status = 'clean'
        if rc == 1:
            if not set(names) <= set(DOCS): memo[prefix] = (None, {'rc': rc, 'names': names, 'status': 'UNRESOLVABLE (conflict outside the docs)'}); return memo[prefix]
            for d in names: upd[d] = hash_blob(clone, keep_both(read_blob(clone, cur, d), frags[(n, d)]))
            tr = tree_with(clone, tr, upd); status = 'keep-both on %d doc(s)' % len(names)
        elif rc != 0:
            memo[prefix] = (None, {'rc': rc, 'names': names, 'status': 'merge-tree error: ' + e[:80]}); return memo[prefix]
        c = commit_of(clone, tr, [cur, heads[n]], 'gate86 compose %s' % '-'.join(prefix)); memo[prefix] = (c, {'rc': rc, 'names': names, 'status': status}); return memo[prefix]
    leaves = {}
    for order in itertools.permutations(sorted(heads)): leaves[order] = advance(order)
    t.check('C-ORDERS', len(leaves) == 24 and all(v[0] for v in leaves.values()), '%d merge orders composed; %d fully resolved by keep-both on the two docs; unresolvable: %s' % (len(leaves), sum(1 for v in leaves.values() if v[0]), [('-'.join(k), v[1]['status']) for k, v in leaves.items() if not v[0]][:3]))
    # per-position conflict statistics over the trie
    stat = {}
    for pref, (c, info) in memo.items():
        if info: stat.setdefault(len(pref), []).append((pref[-1], info['rc'], len(info['names'])))
    for pos in sorted(stat): t.info('C-POS-%d' % pos, 'merge position %d over all prefixes: rc0 %d, rc1 %d (docs-only conflicts: %s distinct (PR,n-docs) cases)' % (pos, sum(1 for x in stat[pos] if x[1] == 0), sum(1 for x in stat[pos] if x[1] == 1), sorted(set((x[0], x[2]) for x in stat[pos] if x[1] == 1))))
    # --- composed-state checks on every leaf
    order_ok = True; docs_sets = {}; nondoc_sets = set(); allfrags = {d: sorted(frags[(n, d)] for n in heads) for d in DOCS}
    pr_paths = {n: [p for p in PR(n)['paths'] if p not in DOCS] for n in heads}
    for order, (c, info) in leaves.items():
        if not c: order_ok = False; continue
        tr = sh_git(clone, ['log', '-1', '--format=%T', c])[1].strip(); tag = '-'.join(order)
        for d in DOCS:
            doc = read_blob(clone, c, d); rest = doc
            for n in order:
                if rest.count(frags[(n, d)]) != 1: order_ok = False
                rest = rest.replace(frags[(n, d)], '', 1)
            if rest != dev_docs[d]: order_ok = False
            docs_sets.setdefault(d, set()).add(hash_blob(clone, doc))
        for n in heads:
            for p in pr_paths[n]:
                if p == YAML: continue
                if blob(clone, c, p).split()[-1:] != blob(clone, heads[n], p).split()[-1:]: order_ok = False
        nd = tuple(sorted((p, blob(clone, c, p)) for p in set(sum(pr_paths.values(), [])) if p != YAML)); nondoc_sets.add(nd)
        y = sh_git(clone, ['diff', '--numstat', dev, c, '--', YAML])[1].split(); yadd = (int(y[0]), int(y[1])) if y else (0, 0)
        if yadd != (11, 0): order_ok = False
    t.check('C-COMPOSED', order_ok, 'every one of the 24 composed states: each of the 4 fragments present ONCE in each doc, composed minus the four fragments == develop\'s doc byte for byte, every non-doc non-yaml path blob == that PR\'s head blob, and the yaml differs from develop by exactly +11/-0 lines')
    t.check('C-NONDOC-IDENTICAL', len(nondoc_sets) == 1, 'the non-doc paths (code, tests, scripts, templates) are IDENTICAL across all 24 orders: %d distinct state(s)' % len(nondoc_sets))
    yblobs = {blob(clone, c, YAML) for c, _ in leaves.values() if c}; t.check('C-YAML-IDENTICAL', len(yblobs) == 1, 'the yaml blob is IDENTICAL across all 24 orders (the two PRs\' hunks are disjoint): %d distinct blob(s) %s' % (len(yblobs), [y.split()[-1][:12] for y in yblobs]))
    # --- order-independence of the four doc blocks: the SET of blocks is the same; the document order is not
    for d in DOCS:
        t.check('C-DOCS-SET-%s' % ('flow' if d == FLOW else 'cheat'), order_ok, '%s: %d distinct composed document(s) over 24 orders; all contain the same four fragments once each (checked above); only the ORDER of the appended blocks differs' % (d.split('/')[-1][:44], len(docs_sets[d])))
        t.check('C-DOCS-DISTINCT-%s' % ('flow' if d == FLOW else 'cheat'), len(docs_sets[d]) == 24, 'CONTROL: the order of the appended blocks is OBSERVABLE (24 orders give %d distinct documents), so an order-insensitive checker would be blind here' % len(docs_sets[d]))
    nat = ('1451', '1452', '1454', '1455'); rev = tuple(reversed(nat))
    for tag, o in (('natural', nat), ('reverse', rev)):
        c = leaves[o][0]; open(os.path.join(out, 'composed_%s.sha' % tag), 'w').write(c + '\n')
        nums = re.findall(r'<h2>(\d+)\. ', read_blob(clone, c, FLOW))
        t.info('C-TAIL-%s' % tag, 'order %s: flow-doc heading numbers in document order (last 9): %s ; composed commit %s' % ('-'.join(o), nums[-9:], c[:12]))
    t.info('C-STEPS-%s' % 'natural', 'natural order steps: %s' % [(p[-1], memo[p][1]['rc'], memo[p][1]['status']) for p in [nat[:i] for i in range(1, 5)]])
    t.info('C-STEPS-reverse', 'reverse order steps: %s' % [(p[-1], memo[p][1]['rc'], memo[p][1]['status']) for p in [rev[:i] for i in range(1, 5)]])
    # --- negative controls on the composed-state checks
    c0 = leaves[nat][0]; d0 = read_blob(clone, c0, FLOW); dup = d0[:-len(TAIL)] + frags[('1451', FLOW)] + TAIL
    t.check('C-CONTROL-DUP', dup.count(frags[('1451', FLOW)]) == 2 and d0.count(frags[('1451', FLOW)]) == 1, 'CONTROL: a planted duplicate of block 55 reads count 2 where the composed document reads 1')
    try: keep_both(d0, frags[('1451', FLOW)]); ok = False
    except ValueError: ok = True
    t.check('C-CONTROL-KEEPBOTH', ok, 'CONTROL: keep_both REFUSES to insert a fragment that is already present')
    return t.end()


# ---------------------------------------------------------------- regen / docs
def regen(A):
    tree = req(A, '--tree'); out = req(A, '--out'); t = Tally(); os.makedirs(out, exist_ok=True); cwd = os.path.join(tree, DEV); tsx = os.path.join(cwd, 'node_modules', '.bin', 'tsx')
    if not os.path.exists(tsx): raise SystemExit('REFUSED: tsx missing in %s (prep with --deps-from)' % tree)
    stmp = tempfile.mkdtemp(prefix='g', dir='/private/tmp/claude-501')      # SHORT: tsx binds a unix socket under TMPDIR (path limit ~104 bytes)
    rc, so, se = lrun([tsx, 'scripts/generate-openapi.ts', '--check'], cwd, env={'TMPDIR': stmp}); open(os.path.join(out, 'regen.out'), 'w').write(so); open(os.path.join(out, 'regen.err'), 'w').write(se)
    t.check('RG1', rc == 0 and 'EINVAL' not in se, '`tsx scripts/generate-openapi.ts --check` on the tree: rc %d (0 = the yaml equals what the registered .openapi.ts files generate); last stdout line: %s | stderr tail: %s' % (rc, (so.strip().split('\n') or [''])[-1][:140], se.strip()[-120:]))
    ypath = os.path.join(cwd, 'docs/openapi/secuura-api.yaml'); orig = open(ypath, 'rb').read(); pl = Plant(tree); L = orig.decode().split('\n')
    idx = [i for i, l in enumerate(L) if l == '        required: true' and L[i - 1].strip() == 'requestBody:']
    if not idx: t.check('RG2', False, 'no `requestBody:` + `required: true` pair to tamper with'); return t.end()
    new = '\n'.join(L[:idx[0]] + L[idx[0] + 1:]); lan = pl.put(DEV + '/docs/openapi/secuura-api.yaml', new)
    rc2, so2, se2 = lrun([tsx, 'scripts/generate-openapi.ts', '--check'], cwd, env={'TMPDIR': stmp}); bad = pl.restore(); open(os.path.join(out, 'regen_tamper.out'), 'w').write(so2 + '\n--stderr--\n' + se2)
    t.check('RG2', bool(lan[2] and lan[3] and not bad) and rc2 == 1 and 'EINVAL' not in se2 and (so2 + se2).strip() != (so + se).strip(), 'TAMPER CONTROL: one `required: true` line removed from the tree\'s yaml (plant LANDED %s): --check rc %d (want 1) with a message that DIFFERS from the clean run\'s (so an infrastructure failure cannot pass as a detection): %r; restored by blob id: %s' % (bool(lan[2] and lan[3]), rc2, (so2 + se2).strip()[-100:], not bad))
    rc3, _, _ = lrun([tsx, 'scripts/generate-openapi.ts', '--check'], cwd, env={'TMPDIR': stmp}); t.check('RG3', rc3 == rc, 'after the restore the check reads rc %d again (== the first reading %d)' % (rc3, rc))
    return t.end()


def docs(A):
    tree = req(A, '--tree'); out = req(A, '--out'); exp = [int(x) for x in (opt(A, '--expect-blocks', '55,56,57,58,59')).split(',')]; t = Tally(); os.makedirs(out, exist_ok=True)
    p = subprocess.run(['/bin/bash', os.path.join(tree, 'systemTest/__tests__/html_docs_matrix.test.sh')], capture_output=True, cwd=tree, env=dict(os.environ, TMPDIR=out)); so = p.stdout.decode('utf-8', 'replace')
    ok = len(re.findall(r'^\s+ok\s', so, re.M)); bad = len(re.findall(r'^\s+FAIL\s', so, re.M)); open(os.path.join(out, 'matrix.out'), 'w').write(so)
    t.check('DM1', p.returncode == 0 and bad == 0 and ok >= 1, 'html_docs_matrix on the tree: rc %d, %d ok / %d FAIL (the READYs: 12 / 0; the tally is NOT well-formedness evidence)' % (p.returncode, ok, bad))
    fl = open(os.path.join(tree, FLOW), encoding='utf-8').read(); ch = open(os.path.join(tree, CHEAT), encoding='utf-8').read(); nums = [int(x) for x in re.findall(r'<h2>(\d+)\. ', fl)]
    t.check('DM2', all(nums.count(b) == 1 for b in exp) and len(nums) == len(set(nums)), 'COUNT per flow block in the tree: %s; all heading numbers distinct: %s; document-order tail %s' % ({b: nums.count(b) for b in exp}, len(nums) == len(set(nums)), nums[-8:]))
    keys = [PR(n)['cheat_key'] for n in sorted(K['prs'])]; heads = re.findall(r'<h2>([^<]*)</h2>', ch)
    t.info('DM3', 'cheat <h2> counts naming each key in the tree: %s (earlier pieces of the same ticket may also be present)' % {k: len([h for h in heads if k in h]) for k in keys})
    drop = fl.replace(re.search(r'<h2>58\. .*?(?=<h2>|\Z)', fl, re.S).group(0), '', 1) if 58 in nums else fl
    t.check('DM4-CONTROL', (58 not in exp) or ([int(x) for x in re.findall(r'<h2>(\d+)\. ', drop)].count(58) == 0 and nums.count(58) == 1), 'CONTROL: dropping block 58 from an in-memory copy reads COUNT 0 where the tree reads 1 (the matrix cannot see this; the COUNT can)')
    return t.end()


# ---------------------------------------------------------------- selftest
def selftest():
    t = Tally()
    tree = tempfile.mkdtemp(prefix='g86self', dir='/private/tmp/claude-501'); os.makedirs(os.path.join(tree, 'a')); open(os.path.join(tree, 'a/f.txt'), 'w').write('one\n'); pl = Plant(tree)
    r = pl.put('a/f.txt', 'two\n'); t.check('S1', r[2] and r[3] and open(os.path.join(tree, 'a/f.txt')).read() == 'two\n', 'Plant.put lands and reports changed')
    t.check('S2', pl.restore() == [] and open(os.path.join(tree, 'a/f.txt')).read() == 'one\n', 'Plant.restore returns the original bytes')
    r2 = pl.put('a/f.txt', 'one\n'); t.check('S3', r2[2] and not r2[3], 'a no-op plant is reported NOT changed (an anchor that did not change anything cannot pass as a tamper)')
    txt = "sharedRegistry.registerPath({\n  method: 'post',\n  path: '/api/x',\n  request: {\n    body: {\n      content: {},\n      // KS-1: c\n      required: true,\n    },\n  },\n});\nsharedRegistry.registerPath({\n  method: 'post',\n  path: '/api/y',\n  request: {\n    // KS-1: c\n    body: { content: {} }, required: true },\n  },\n});\n"
    s = decl_sites(txt); t.check('S4', [(x[0], x[3], x[4]) for x in s] == [('line', '/api/x', 'post'), ('inline', '/api/y', 'post')], 'decl_sites finds a line-style and an inline declaration with their paths: %s' % [(x[0], x[3]) for x in s])
    m1 = txt[:s[0][1]] + txt[s[0][2]:]; m2 = txt[:s[1][1]] + txt[s[1][2]:]
    t.check('S5', 'required: true,' not in m1 and m1.count('required: true') == 1 and m2.count('required: true') == 1 and 'body: { content: {} } },' in m2, 'dropping one site leaves exactly the other')
    t.check('S6', keep_both('x' + TAIL, 'FRAG\n') == 'xFRAG\n' + TAIL, 'keep_both inserts before the closing tags')
    try: keep_both('xFRAG\n' + TAIL, 'FRAG\n'); ok = False
    except ValueError: ok = True
    t.check('S7', ok, 'keep_both refuses a duplicate')
    t.check('S8', len(list(itertools.permutations(['1451', '1452', '1454', '1455']))) == 24, '4! = 24 merge orders')
    d = tempfile.mkdtemp(prefix='g86self2', dir='/private/tmp/claude-501'); fp = os.path.join(d, 't.sh'); open(fp, 'w').write("#!/bin/bash\nprintf 'ok   a\\nok   b\\nFAIL c\\nx: 2 passed, 1 failed\\n'; exit 1\n")
    r = run_shell(d, os.path.join(d, 'o'), 'self', 't.sh'); t.check('S9', r['rc'] == 1 and (r['ok'], r['bad']) == (2, 1) and r['summary'] == ('2', '1'), 'run_shell counts ok / FAIL lines and reads the summary under env -i: %s' % ((r['rc'], r['ok'], r['bad'], r['summary']),))
    return t.end()


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--selftest' in A: sys.exit(selftest())
    cmds = {'prep': prep, 'vitest': vitest, 'mutate': mutate, 'shell': shell, 'compose': compose, 'regen': regen, 'docs': docs, 'nmcheck': lambda a: nmcheck(req(a, '--tree'))}
    if not A or A[0] not in cmds: print(__doc__); sys.exit(2)
    sys.exit(cmds[A[0]](A[1:]))
