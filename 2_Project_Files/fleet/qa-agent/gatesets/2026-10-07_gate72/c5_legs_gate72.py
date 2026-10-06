#!/usr/bin/env python3
"""c5_legs_gate72.py — RUNS the repo's own gates, installs and suites in the TESTER'S OWN worktrees / isolated copies (never a builder's
worktree, never the shared checkout). Carried from c5_legs_gate70.py; [g72] marks changes. Every command's stdout / stderr / rc goes to
SEPARATE files under --out; the rc is read from the process, never through a pipe. Network: the npm registry (X1).

  legs      --wt WT --expect fail|pass --out DIR   leg 6 `node scripts/audit/audit-gate.mjs` + leg 7 `node scripts/audit/audit-locks.mjs`
            from WT/Blockchain/Dev (scripts/audit deps `npm ci --ignore-scripts` first, only if absent). rc 2 = COULD-NOT-CHECK: NOT RUN.
            --expect fail (BASE CONTROL): leg 6 rc 1 AND leg 7 rc 1 AND each of the three ids printed > 0 times.
            --expect pass (HEAD): rc 0 AND rc 0 AND the three ids printed 0 times — a zero beside the base's count.
  contract  --wt WT --out DIR    `npm run audit:contract`: rc 0, pass == WT's expected-case-count (59), fail 0
  cleanroom --wt WT --out DIR    leg 2: rc 0, the "All N standalone lock(s) pass" line, tracked status identical before/after
  rootci    --wt WT --out DIR    `npm ci --ignore-scripts` at WT/Blockchain/Dev (the ROOT lock, its natural place): rc 0, lock sha256
            identical, and the HOISTED versions of the three packages read off disk
  iso       --wt WT --repo CLONE --base B --out DIR   [g72] EACH CHANGED STANDALONE LOCK INSTALLED AS ITS DOCKERFILE DOES: the lock dir's
            package.json + package-lock.json copied to DIR/iso/<name>/ (NOT under the workspace root: no ancestor package.json, asserted
            — a workspace member's own `npm ci` resolves against the ROOT lock, the builder's own caveat), `npm ci --ignore-scripts`:
            rc 0, lock sha256 unchanged, and the planned package's version READ OFF DISK == the new version
  suites    --wt WT --out DIR --tag base|head [--only a,b]   [g72] isolated copies, Dockerfile-shaped: packages/shared (ci, build, test);
            services/mcp-server and services/anchoring (ci, @secuura/shared symlinked to the isolated built shared — Dockerfile :31/:24 —,
            build, test); frontend/issuer (ci, frontend/shared vendored, SHARED_DIR=./vendor/shared/src — Dockerfile :23-:24 —, build,
            then the BUNDLE probe). Writes DIR/suites_<tag>.json. Vitest summaries parsed into (failed, passed, skipped, total) + the failing
            test names. NOTE: issuer's Dockerfile :18 runs `npm ci --no-audit` WITH install scripts; X1 allows --ignore-scripts only: the
            divergence is named, never hidden.
  wsuites   --wt WT --out DIR --tag base|head   the builder's WORKSPACE mode (root `npm ci --ignore-scripts`, `npm run build
            --workspace=packages/shared`, `npm test` inside each member): KS-562 says threadTokenMint fails "only under root-visible npm
            install" — so the known failure is compared in THIS mode too.
  compare   --a suites_base.json --b suites_head.json   KF: the known failure (threadTokenMint) fails IDENTICALLY at base and head (same
            failing-test set, same error needle), and NOTHING else fails at the head that passes at base; counts printed side by side.
            BD: [g72] BUNDLE DELTA — issuer dist files base vs head by sha256 (pbkdf2 3.1.6 -> 3.1.7 changes only lib/sync.js, which the
            package's `browser` map replaces with lib/sync-browser.js: a byte-identical bundle is a FINDING about the "browser-facing
            surface" claim, not a pass or a fail of this PR — the gate rules it).
  nc        --wt WT --repo CLONE --base B --out DIR   NEGATIVE CONTROLS on the HEAD worktree; each plant ASSERTED LANDED, restored BY
            CONTENT, sha256-verified; `git status --porcelain` empty after:
            NC1 root shell-quote -> its BASE entry (1.9.0)      -> leg 6 rc 1 naming GHSA-pqg4, and NOT 6qxp / 477h (specific)
            NC2 mcp-server sdk -> its BASE entry (1.29.0)       -> leg 7 rc 1 naming GHSA-6qxp, and NOT 477h (specific)
            NC3 packages/shared pbkdf2 -> its BASE entry (3.1.6) -> leg 7 rc 1 naming GHSA-477h (the gate's own third arm)
  --selftest   vitest / TAP parsing, id counting, the rc classification, the compare predicates, the bundle probe (synthetic).
rc 0 / 1 (a FAIL or a NOT RUN) / 2 refused."""
import hashlib, json, os, re, shutil, subprocess, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate72 import K, Tally, git_bytes, outside_forbidden, detect_indent, pkg_name, req, opt

HERE = os.path.dirname(os.path.abspath(__file__))
LG = K['legs']; THREE = K['three_ids']; PLAN = K['plan']; SU = K['suites']; KF = K['known_failure']; BU = K['bundle']
TIMEOUT = int(os.environ.get('G72_LEG_TIMEOUT', '1800'))


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def run(cmd, cwd, out, tag, env=None):
    e = dict(os.environ); e.pop('GIT_SSH_COMMAND', None); e.update(env or {})
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT, env=e)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as x:
        rc, so, se = 124, x.stdout or '', (x.stderr or '') + '\nTIMEOUT %ds' % TIMEOUT
        so = so.decode() if isinstance(so, bytes) else so; se = se.decode() if isinstance(se, bytes) else se
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, tag + '.out'), 'w').write(so); open(os.path.join(out, tag + '.err'), 'w').write(se)
    open(os.path.join(out, tag + '.rc'), 'w').write('%d\n' % rc)
    print('RAN %s rc %d (%s in %s) -> %s/%s.{out,err,rc}' % (tag, rc, ' '.join(cmd), cwd, out, tag))
    return rc, so + '\n' + se


def count_ids(text, ids): return dict((i, text.count(i)) for i in ids)


def classify(rc):
    return {0: 'PASS', 1: 'FAIL-FINDINGS', 2: 'COULD-NOT-CHECK (NOT RUN)', 3: 'MALFORMED-BASELINE', 124: 'TIMEOUT (NOT RUN)'}.get(rc, 'rc %d' % rc)


def tap(text):
    g = lambda k: int(m.group(1)) if (m := re.search(r'^(?:#|ℹ) %s (\d+)' % k, text, re.M)) else None
    return {'tests': g('tests'), 'pass': g('pass'), 'fail': g('fail'), 'skipped': g('skipped'), 'todo': g('todo')}


ANSI = re.compile(r'\x1b\[[0-9;]*m')


def vitest(text):
    """[g72] the LAST `Tests  ...` summary line -> {failed, passed, skipped, total}; failing test names from FAIL/× lines."""
    t = ANSI.sub('', text); out = {'failed': 0, 'passed': 0, 'skipped': 0, 'todo': 0, 'total': None, 'failing': []}
    lines = [l for l in t.split('\n') if re.match(r'^\s*Tests\s+\d', l)]
    if not lines: return None
    l = lines[-1]
    for n, w in re.findall(r'(\d+)\s+(failed|passed|skipped|todo)', l): out[w] = int(n)
    m = re.search(r'\((\d+)\)', l); out['total'] = int(m.group(1)) if m else None
    out['failing'] = sorted(set(re.sub(r'\s+\d+m?s$', '', x.strip()) for x in re.findall(r'^\s*(?:FAIL|×|✗)\s+(.+?)\s*$', t, re.M) if '>' in x))
    return out


def dev(wt): return os.path.join(wt, LG['cwd'])


def base_ok(r6, r7, c): return r6 == 1 and r7 == 1 and all(c.get(i, 0) > 0 for i in THREE)


def head_ok(r6, r7, c): return r6 == 0 and r7 == 0 and sum(c.get(i, 0) for i in THREE) == 0


def guard(wt):
    if not outside_forbidden(wt):
        raise SystemExit('REFUSED: %s is under %s — run in YOUR OWN worktree' % (wt, K['forbidden_root']))
    if not os.path.isdir(dev(wt)):
        raise SystemExit('REFUSED: %s has no %s (a --no-checkout clone is not a worktree)' % (wt, LG['cwd']))


def audit_deps(wt, out):
    d = os.path.join(wt, LG['audit_deps_dir'])
    if os.path.isdir(os.path.join(d, 'node_modules', 'semver')):
        print('DEPS scripts/audit/node_modules/semver present'); return 0
    return run(['npm', 'ci', '--ignore-scripts'], d, out, 'auditdeps_npm_ci')[0]


def legs(wt, expect, out, t, tag='leg'):
    if audit_deps(wt, out) != 0:
        t.check('LEGS', False, 'scripts/audit deps did not install: LOAD FAILURE, NOT RUN'); return {}
    r6, o6 = run(LG['leg6'], dev(wt), out, tag + '6'); r7, o7 = run(LG['leg7'], dev(wt), out, tag + '7')
    c = count_ids(o6 + o7, THREE)
    s6 = re.search(r'audit-gate: (\d+) distinct advisories reported, (\d+) baselined', o6)
    m = re.search(r'audit-locks: (\d+) standalone lockfiles', o7); pk = re.search(r'(\d+) distinct packages pinned', o7)
    mb = re.search(r'(\d+) advisories match, (\d+) already baselined', o7)
    print('LEG6 rc %d %s | %s reported / %s baselined | ids %s' % (r6, classify(r6), s6 and s6.group(1), s6 and s6.group(2), count_ids(o6, THREE)))
    print('LEG7 rc %d %s | %s locks, %s packages, %s match / %s baselined | ids %s' % (
        r7, classify(r7), m and m.group(1), pk and pk.group(1), mb and mb.group(1), mb and mb.group(2), count_ids(o7, THREE)))
    print('BUILDER CLAIMS: %s' % LG['builder_claims'])
    if expect == 'fail':
        t.check('G-BASE', base_ok(r6, r7, c), 'BASE CONTROL: leg 6 rc %d, leg 7 rc %d (want 1 / 1, never 2) | each id printed %s (want each > 0)' % (r6, r7, c))
    else:
        t.check('G-HEAD', head_ok(r6, r7, c), 'HEAD: leg 6 rc %d, leg 7 rc %d (want 0 / 0) | the three ids printed %s (want 0 each; the base control is the other half)' % (r6, r7, c))
    return {'r6': r6, 'r7': r7, 'c': c}


def contract(wt, out, t):
    if audit_deps(wt, out) != 0:
        t.check('C5', False, 'deps did not install: NOT RUN'); return
    rc, o = run(LG['leg5'], dev(wt), out, 'leg5_contract')
    want = int(open(os.path.join(wt, LG['audit_deps_dir'], 'expected-case-count')).read().strip())
    tp = tap(o)
    t.check('C5', rc == 0 and tp['pass'] == want == K['expected_case_count'] and tp['fail'] == 0 and tp['tests'] == want,
            'audit:contract rc %d | TAP %s | expected-case-count file %d (kit %d)' % (rc, tp, want, K['expected_case_count']))


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout


def cleanroom(wt, out, t):
    before = porcelain(wt)
    rc, o = run(LG['leg2'], dev(wt), out, 'leg2_cleanroom')
    after = porcelain(wt); m = re.search(r'All (\d+) standalone lock\(s\) pass', o)
    t.check('C2R', rc == 0 and m is not None and before == after, 'lockfile-cleanroom rc %d | "%s" | tracked-file status identical before/after: %s (%d / %d lines)' % (
        rc, m.group(0) if m else 'the All-N line ABSENT', before == after, before.count('\n'), after.count('\n')))


def disk_version(d, name):
    p = os.path.join(d, 'node_modules', name, 'package.json')
    return json.load(open(p)).get('version') if os.path.isfile(p) else None


def rootci(wt, out, t):
    lock = os.path.join(dev(wt), 'package-lock.json'); a = sha(lock)
    rc, o = run(['npm', 'ci', '--ignore-scripts'], dev(wt), out, 'rootci_npm_ci')
    b = sha(lock); m = re.search(r'added (\d+) packages?', o)
    hv = dict((n, disk_version(dev(wt), n)) for n in PLAN)
    t.check('ROOTCI', rc == 0 and a == b and all(hv[n] == PLAN[n]['new'] for n in PLAN), 'root npm ci --ignore-scripts rc %d | lock sha256 %s -> %s identical %s | %s | hoisted on disk %s' % (
        rc, a[:16], b[:16], a == b, m.group(0) if m else 'no "added N" line', hv))


def ancestors_clean(d):
    p = os.path.dirname(os.path.abspath(d)); hits = []
    while True:
        if os.path.isfile(os.path.join(p, 'package.json')): hits.append(p)
        if p == '/': return hits
        p = os.path.dirname(p)


def changed_locks(repo, base, head):
    return [l for l in subprocess.run(['git', '-C', repo, 'diff', '--name-only', base, head], capture_output=True, text=True).stdout.split()
            if l.endswith('package-lock.json') and l != K['root_lock']]


def head_of(wt): return subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()


def iso(wt, repo, base, out, t):
    head = head_of(wt); ch = changed_locks(repo, base, head); res = []
    print('ISO changed standalone locks: %s' % ch)
    for l in ch:
        name = os.path.dirname(l).split('/')[-1]; d = os.path.join(out, 'iso', name)
        os.makedirs(d, exist_ok=False)
        for f in ('package.json', 'package-lock.json'): shutil.copy2(os.path.join(wt, os.path.dirname(l), f), d)
        anc = ancestors_clean(d)
        a = sha(os.path.join(d, 'package-lock.json'))
        rc, o = run(['npm', 'ci', '--ignore-scripts'], d, out, 'iso_' + name)
        b = sha(os.path.join(d, 'package-lock.json')); m = re.search(r'added (\d+) packages?', o)
        pj = json.loads(git_bytes(repo, head, l))['packages']
        pk = sorted(set(pkg_name(k) for k in pj if pkg_name(k) in PLAN and k.count('node_modules/') == 1))
        on_disk = dict((n, disk_version(d, n)) for n in pk)
        ok = bool(rc == 0 and a == b and not anc and pk and all(on_disk[n] == PLAN[n]['new'] for n in pk))
        res.append(ok)
        print('  %s rc %d lock unchanged %s | ancestor package.json %s | added %s | ON DISK %s' % (l, rc, a == b, anc or 'none', m.group(1) if m else None, on_disk))
    t.check('ISO', bool(res) and all(res), 'isolated npm ci per changed standalone lock (Dockerfile shape): %d/%d rc 0, lock unchanged, no workspace root above, new version ON DISK' % (sum(res), len(res)))


def copytree(src, dst, extra_ignore=()):
    shutil.copytree(src, dst, symlinks=True, ignore=shutil.ignore_patterns('node_modules', 'dist', '.turbo', *extra_ignore))


def bundle_probe(dist_dir):
    files = sorted(glob.glob(os.path.join(dist_dir, 'assets', '*.js')))
    txt = dict((os.path.basename(f), open(f, encoding='utf-8', errors='replace').read()) for f in files)
    lit = dict((s, dict((f, x.count(s)) for f, x in txt.items() if s in x)) for s in BU['pbkdf2_literals'])
    hit = dict((s, sum(x.count(s) for x in txt.values())) for s in BU['must_hit'])
    nohit = dict((s, sum(x.count(s) for x in txt.values())) for s in BU['must_not_hit'])
    manifest = dict((os.path.relpath(p, dist_dir), sha(p)) for p in sorted(glob.glob(os.path.join(dist_dir, '**', '*'), recursive=True)) if os.path.isfile(p))
    return {'js_files': len(files), 'literals': lit, 'must_hit': hit, 'must_not_hit': nohit, 'manifest': manifest}


def literal_provenance(nm_dir):
    """which installed packages carry each pbkdf2 literal (is it pbkdf2-SPECIFIC?)"""
    out = dict((s, set()) for s in BU['pbkdf2_literals'])
    for root, ds, fs in os.walk(nm_dir):
        for f in fs:
            if not f.endswith(('.js', '.cjs', '.mjs')): continue
            try: x = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
            except OSError: continue
            for s in out:
                if s in x:
                    rel = os.path.relpath(root, nm_dir).split(os.sep); out[s].add('/'.join(rel[:2]) if rel[0].startswith('@') else rel[0])
    return dict((s, sorted(v)) for s, v in out.items())


def suites(wt, out, tag, only, t):
    res = {'tag': tag, 'head': head_of(wt)}; base = os.path.join(out, 'suites_' + tag)
    os.makedirs(base, exist_ok=False)
    want = [x for x in ('shared', 'mcp-server', 'anchoring', 'issuer') if not only or x in only]
    sh = os.path.join(base, 'shared'); copytree(os.path.join(wt, SU['shared']['dir']), sh)
    r1, _ = run(['npm', 'ci', '--ignore-scripts'], sh, out, '%s_shared_ci' % tag)
    r2, _ = run(SU['shared']['build'], sh, out, '%s_shared_build' % tag)
    built = os.path.isfile(os.path.join(sh, 'dist', 'index.js'))
    res['shared_prep'] = {'ci': r1, 'build': r2, 'dist_index_js': built, 'pbkdf2_on_disk': disk_version(sh, 'pbkdf2')}
    print('SHARED prep ci %d build %d dist/index.js %s pbkdf2 on disk %s' % (r1, r2, built, res['shared_prep']['pbkdf2_on_disk']))
    if 'shared' in want:
        if not os.path.exists(os.path.join(sh, 'node_modules', '.bin', 'vitest')):
            res['shared'] = {'not_runnable_isolated': 'vitest is not a dependency of packages/shared (it comes from the workspace root): run it in `wsuites`'}
            print('SHARED test NOT RUNNABLE ISOLATED: node_modules/.bin/vitest absent (drafter, 2026-10-06T21:21Z: rc 127 `vitest: command not found`) — wsuites runs it')
        else:
            rc, o = run(SU['shared']['test'], sh, out, '%s_shared_test' % tag); res['shared'] = {'test_rc': rc, 'vitest': vitest(o)}
    for s in ('mcp-server', 'anchoring'):
        if s not in want: continue
        d = os.path.join(base, s); copytree(os.path.join(wt, SU[s]['dir']), d)
        rc, _ = run(['npm', 'ci', '--ignore-scripts'], d, out, '%s_%s_ci' % (tag, s))
        os.makedirs(os.path.join(d, 'node_modules', '@secuura'), exist_ok=True)
        lk = os.path.join(d, 'node_modules', '@secuura', 'shared')
        if not os.path.lexists(lk): os.symlink(sh, lk)
        rb, _ = run(SU[s]['build'], d, out, '%s_%s_build' % (tag, s))
        rt, o = run(SU[s]['test'], d, out, '%s_%s_test' % (tag, s))
        res[s] = {'ci': rc, 'build': rb, 'test_rc': rt, 'vitest': vitest(o), 'on_disk': dict((n, disk_version(d, n)) for n in PLAN if disk_version(d, n)),
                  'error_needle': o.count(KF['error_needle'])}
    if 'issuer' in want:
        d = os.path.join(base, 'issuer'); copytree(os.path.join(wt, SU['issuer']['dir']), d)
        for src, dst in SU['issuer']['vendor']: copytree(os.path.join(wt, src), os.path.join(d, dst))
        rc, _ = run(['npm', 'ci', '--ignore-scripts'], d, out, '%s_issuer_ci' % tag)
        rb, _ = run(SU['issuer']['build'], d, out, '%s_issuer_build' % tag, env=SU['issuer']['env'])
        bp = bundle_probe(os.path.join(d, 'dist')) if rb == 0 else None
        res['issuer'] = {'ci': rc, 'build': rb, 'pbkdf2_on_disk': disk_version(d, 'pbkdf2'), 'bundle': bp,
                         'provenance': literal_provenance(os.path.join(d, 'node_modules')) if rc == 0 else None}
        if bp:
            print('BUNDLE %d js | literals %s | must-hit %s | must-not-hit %s' % (bp['js_files'], bp['literals'], bp['must_hit'], bp['must_not_hit']))
            print('PROVENANCE (which installed packages carry each literal) %s' % res['issuer']['provenance'])
    jf = os.path.join(out, 'suites_%s.json' % tag); json.dump(res, open(jf, 'w'), indent=1); print('JSON %s' % jf)
    for s in want:
        r = res.get(s, {}); print('SUITE %s %s' % (s, {k: v for k, v in r.items() if k not in ('bundle', 'provenance')}))
    ok = res['shared_prep']['build'] == 0 and built
    for s in ('shared', 'mcp-server', 'anchoring'):
        if s in want and 'not_runnable_isolated' not in res[s]: ok &= res[s].get('vitest') is not None and res[s].get('build', 0) == 0
    if 'issuer' in want:
        bp = res['issuer']['bundle']
        ok &= res['issuer']['build'] == 0 and bool(bp) and all(v > 0 for v in bp['must_hit'].values()) and not any(bp['must_not_hit'].values())
    t.check('SUITES-%s' % tag.upper(), ok, 'every requested suite RAN (a summary was parsed), builds rc 0, bundle controls fired (must-hit > 0, must-not-hit 0) — red tests are ruled by `compare`, not here')


def wsuites(wt, out, tag, t):
    res = {'tag': tag, 'head': head_of(wt), 'mode': 'workspace'}
    r0, _ = run(['npm', 'ci', '--ignore-scripts'], dev(wt), out, '%s_ws_root_ci' % tag)
    r1, _ = run(['npm', 'run', 'build', '--workspace=packages/shared'], dev(wt), out, '%s_ws_shared_build' % tag)
    built = os.path.isfile(os.path.join(dev(wt), 'packages', 'shared', 'dist', 'index.js'))
    res['prep'] = {'root_ci': r0, 'shared_build': r1, 'dist_index_js': built, 'hoisted': dict((n, disk_version(dev(wt), n)) for n in PLAN)}
    for s in ('shared', 'mcp-server', 'anchoring'):
        rt, o = run(SU[s]['test'], os.path.join(wt, SU[s]['dir']), out, '%s_ws_%s_test' % (tag, s))
        res[s] = {'test_rc': rt, 'vitest': vitest(o), 'error_needle': o.count(KF['error_needle'])}
        print('WSUITE %s %s' % (s, res[s]))
    jf = os.path.join(out, 'wsuites_%s.json' % tag); json.dump(res, open(jf, 'w'), indent=1); print('JSON %s' % jf)
    t.check('WSUITES-%s' % tag.upper(), r0 == 0 and built and all(res[s]['vitest'] for s in ('shared', 'mcp-server', 'anchoring')),
            'workspace mode: root ci %d, shared dist/index.js %s, every suite summary parsed' % (r0, built))


def kf_compare(a, b):
    """-> (ok, why). The known failure must fail identically at both; nothing NEW fails at b."""
    why = []
    for s in ('shared', 'mcp-server', 'anchoring'):
        if 'not_runnable_isolated' in (a.get(s) or {}) and 'not_runnable_isolated' in (b.get(s) or {}): continue
        va, vb = (a.get(s) or {}).get('vitest'), (b.get(s) or {}).get('vitest')
        if va is None or vb is None: why.append('%s: a summary is missing (NOT RUN)' % s); continue
        new = sorted(set(vb['failing']) - set(va['failing']))
        if new or vb['failed'] > va['failed']: why.append('%s: NEW failures at b %s (%d vs %d)' % (s, new, vb['failed'], va['failed']))
    ka = (a.get(KF['suite']) or {}).get('vitest') or {}; kb = (b.get(KF['suite']) or {}).get('vitest') or {}
    fa = [x for x in ka.get('failing', []) if KF['needle'] in x]; fb = [x for x in kb.get('failing', []) if KF['needle'] in x]
    if fa != fb: why.append('known failure differs: a %s b %s' % (fa, fb))
    return not why, why, fa, fb


def bundle_delta(a, b):
    ma = ((a.get('issuer') or {}).get('bundle') or {}).get('manifest'); mb = ((b.get('issuer') or {}).get('bundle') or {}).get('manifest')
    if ma is None or mb is None: return None
    return {'identical': ma == mb, 'only_a': sorted(set(ma) - set(mb)), 'only_b': sorted(set(mb) - set(ma)),
            'changed': sorted(k for k in set(ma) & set(mb) if ma[k] != mb[k]), 'files': (len(ma), len(mb))}


def compare(fa, fb, t):
    a = json.load(open(fa)); b = json.load(open(fb))
    for s in ('shared', 'mcp-server', 'anchoring'):
        print('COUNTS %-10s a(%s) %s | b(%s) %s' % (s, a['tag'], (a.get(s) or {}).get('vitest'), b['tag'], (b.get(s) or {}).get('vitest')))
    ok, why, ka, kb = kf_compare(a, b)
    t.check('KF', ok, 'the known failure %s behaves IDENTICALLY at a and b (failing: a %s | b %s), nothing else new %s' % (KF['needle'], ka, kb, why or ''))
    t.info('KF-MODE', '%s: the known failure is %s in this mode (KS-562: "fails only under root-visible npm install" — expect it in wsuites, '
           'not in the isolated suites)' % (a.get('mode', 'isolated'), 'PRESENT' if ka else 'ABSENT at both sides'))
    for s in ('shared', 'mcp-server', 'anchoring'):
        if 'not_runnable_isolated' in (a.get(s) or {}): t.info('NR-%s' % s, 'NOT RUN in this mode: %s' % a[s]['not_runnable_isolated'])
    bd = bundle_delta(a, b)
    if bd is None: t.info('BD', 'NOT RUN: an issuer bundle is missing from one side')
    else: t.info('BD', 'issuer dist base vs head: byte-identical %s | files %s | changed %s | only-a %s | only-b %s — RULE what it says about the "browser-facing surface" sentence' % (
        bd['identical'], bd['files'], bd['changed'][:6], bd['only_a'][:4], bd['only_b'][:4]))


def _revert_entry(path, key, base_entry):
    raw = open(path, 'rb').read(); n = detect_indent(raw.decode()); j = json.loads(raw)
    j['packages'][key] = base_entry
    open(path, 'wb').write((json.dumps(j, indent=n, ensure_ascii=False) + '\n').encode())
    return raw


def nc(wt, repo, base, out, t):
    guard(wt)
    if audit_deps(wt, out) != 0:
        t.check('NC', False, 'deps did not install: NOT RUN'); return
    arms = (('NC1', K['root_lock'], 'node_modules/shell-quote', 'leg6', 'GHSA-pqg4-j6r4-53mv', ['GHSA-6qxp-vccf-f47h', 'GHSA-477h-4r7f-fvrx']),
            ('NC2', 'Blockchain/Dev/services/mcp-server/package-lock.json', 'node_modules/@modelcontextprotocol/sdk', 'leg7', 'GHSA-6qxp-vccf-f47h', ['GHSA-477h-4r7f-fvrx', 'GHSA-pqg4-j6r4-53mv']),
            ('NC3', 'Blockchain/Dev/packages/shared/package-lock.json', 'node_modules/pbkdf2', 'leg7', 'GHSA-477h-4r7f-fvrx', ['GHSA-6qxp-vccf-f47h', 'GHSA-pqg4-j6r4-53mv']))
    for cid, lock_rel, key, leg, want, notwant in arms:
        p = os.path.join(wt, lock_rel); h0 = sha(p)
        be = json.loads(git_bytes(repo, base, lock_rel))['packages'][key]
        orig = _revert_entry(p, key, be)
        landed = sha(p) != h0 and json.loads(open(p, 'rb').read())['packages'][key] == be
        r, o = run(LG[leg], dev(wt), out, '%s_%s' % (cid.lower(), leg)) if landed else (None, '')
        open(p, 'wb').write(orig); rest = sha(p) == h0
        c = count_ids(o, [want] + notwant)
        t.check(cid, landed and r == 1 and c[want] > 0 and not any(c[x] for x in notwant) and rest,
                '%s %s reverted to its BASE entry %s (landed %s) -> %s rc %s naming %s %d times, the others %s (want 0) | restored sha256-identical %s' % (
                    lock_rel.replace('Blockchain/Dev/', ''), pkg_name(key), be.get('version'), landed, leg, r, want, c[want], dict((x, c[x]) for x in notwant), rest))
    pc = porcelain(wt)
    t.check('NC-CLEAN', pc == '', '`git status --porcelain --untracked-files=no` after the arms: %d lines' % pc.count('\n'))


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(tap('# tests 59\n# pass 59\n# fail 0\n') == {'tests': 59, 'pass': 59, 'fail': 0, 'skipped': None, 'todo': None}, 'TAP summary parsed')
    rep(tap('ℹ tests 59\nℹ pass 59\nℹ fail 0\n')['pass'] == 59, 'spec-reporter summary parsed')
    rep(tap('ok 1\n')['pass'] is None, 'PLANTED a TAP with no summary yields None (C5 then FAILS)')
    v = vitest(' FAIL  src/__tests__/threadTokenMint.test.ts > parameterises mint + spend with a deterministic per-seed policyId\n'
               ' Test Files  1 failed | 47 passed (48)\n      Tests  1 failed | 361 passed (362)\n')
    rep(v and v['failed'] == 1 and v['passed'] == 361 and v['total'] == 362 and len(v['failing']) == 1, 'vitest: Tests line (not Test Files) + failing name parsed: %s' % v)
    rep(vitest('      Tests  945 passed | 2 skipped (947)\n')['skipped'] == 2, 'vitest 4 prints skipped AFTER passed: parsed (STANDING_LINES 2026-09-25)')
    rep(vitest('no summary here') is None, 'PLANTED output with no Tests line yields None (a suite that printed nothing did NOT run)')
    rep(classify(2).endswith('(NOT RUN)') and classify(124).endswith('(NOT RUN)'), 'rc 2 and a timeout classify as NOT RUN')
    c3 = dict((i, 1) for i in THREE)
    rep(head_ok(0, 0, dict((i, 0) for i in THREE)) and not head_ok(0, 0, dict(c3)), 'G-HEAD: zero ids passes; a head still naming an id FAILS')
    rep(not head_ok(2, 0, {}), 'PLANTED leg 6 rc 2 (COULD-NOT-CHECK) FAILS G-HEAD')
    rep(base_ok(1, 1, c3) and not base_ok(2, 1, c3) and not base_ok(1, 1, dict(c3, **{THREE[0]: 0})), 'G-BASE: rc 1/1 with EVERY id passes; rc 2 and a missing id both FAIL')
    va = {'tag': 'base', 'shared': {'vitest': {'failed': 0, 'failing': []}}, 'mcp-server': {'vitest': {'failed': 0, 'failing': []}},
          'anchoring': {'vitest': {'failed': 1, 'failing': ['src/__tests__/threadTokenMint.test.ts > x']}}}
    rep(kf_compare(va, json.loads(json.dumps(va)))[0], 'KF: identical known failure at both passes')
    vb = json.loads(json.dumps(va)); vb['anchoring']['vitest'] = {'failed': 2, 'failing': ['src/__tests__/threadTokenMint.test.ts > x', 'src/a.test.ts > y']}
    rep(not kf_compare(va, vb)[0], 'PLANTED a NEW failure at the head FAILS KF')
    vc = json.loads(json.dumps(va)); vc['anchoring']['vitest'] = {'failed': 0, 'failing': []}
    rep(not kf_compare(va, vc)[0], 'PLANTED known failure absent at the head FAILS KF (not identical — rule it, do not celebrate it)')
    ve = json.loads(json.dumps(va)); ve['anchoring']['vitest'] = {'failed': 0, 'failing': []}
    rep(kf_compare(ve, json.loads(json.dumps(ve)))[0], 'KF: known failure ABSENT at BOTH sides (isolated mode) is identical -> passes, and KF-MODE says so')
    vf = json.loads(json.dumps(va)); vf['shared'] = {'not_runnable_isolated': 'x'}
    rep(kf_compare(vf, json.loads(json.dumps(vf)))[0] and not kf_compare(vf, va)[0], 'KF: a suite NOT RUNNABLE on both sides is skipped by name; on one side only it FAILS')
    vd = json.loads(json.dumps(va)); del vd['mcp-server']
    rep(not kf_compare(va, vd)[0], 'PLANTED a missing suite summary FAILS KF (NOT RUN is never a pass)')
    m1 = {'issuer': {'bundle': {'manifest': {'a.js': '1'}}}}; m2 = {'issuer': {'bundle': {'manifest': {'a.js': '2'}}}}
    rep(bundle_delta(m1, m1)['identical'] and bundle_delta(m1, m2)['changed'] == ['a.js'], 'BD: identical / changed manifests classified')
    rep(not outside_forbidden(K['forbidden_root'] + '/x') and outside_forbidden('/private/tmp/x'), 'the worktree guard refuses the forbidden root')
    rep(ancestors_clean('/private/tmp/claude-zz-nonexistent/a/b') == [], 'ancestor package.json scan: a clean scratch path has none')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    t = Tally()
    try:
        if A[0] == 'compare':
            compare(req(A, '--a'), req(A, '--b'), t); return t.end()
        wt = os.path.abspath(req(A, '--wt')); out = os.path.abspath(req(A, '--out')); guard(wt)
        print('C5 %s in worktree %s at HEAD %s' % (A[0], wt, head_of(wt)))
        if A[0] == 'legs':
            if opt(A, '--expect') not in ('fail', 'pass'): print('REFUSED: --expect fail|pass'); return 2
            legs(wt, opt(A, '--expect'), out, t)
        elif A[0] == 'contract': contract(wt, out, t)
        elif A[0] == 'cleanroom': cleanroom(wt, out, t)
        elif A[0] == 'rootci': rootci(wt, out, t)
        elif A[0] == 'iso': iso(wt, req(A, '--repo'), req(A, '--base', True), out, t)
        elif A[0] == 'suites': suites(wt, out, req(A, '--tag'), (opt(A, '--only') or '').split(',') if opt(A, '--only') else None, t)
        elif A[0] == 'wsuites': wsuites(wt, out, req(A, '--tag'), t)
        elif A[0] == 'nc': nc(wt, req(A, '--repo'), req(A, '--base', True), out, t)
        else: print(__doc__); return 2
    except SystemExit as e:
        print(e); return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
