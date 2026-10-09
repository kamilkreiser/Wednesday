#!/usr/bin/env python3
"""c5_legs_gate78.py — RUNS the repo's own gates, installs and suites in the TESTER'S OWN worktrees / isolated copies (never a builder's
worktree, never the shared checkout). Carried from c5_legs_gate72.py; [g78] marks this kit's changes (the issuer bundle and the
KS-562 known-failure machinery are dropped: no frontend lock and no shared member is in scope; `omit` and the 5-arm `nc` are new).
Every command's stdout / stderr / rc goes to SEPARATE files under --out; the rc is read from the process, never through a pipe.
Network: the npm registry (X1).

  legs      --wt WT --expect fail|pass --out DIR   leg 6 `node scripts/audit/audit-gate.mjs` + leg 7 `node scripts/audit/audit-locks.mjs`
            from WT/Blockchain/Dev (scripts/audit deps `npm ci --ignore-scripts` first, only if absent). rc 2 = COULD-NOT-CHECK: NOT RUN.
            --expect fail (BASE CONTROL): leg 6 rc 1 AND leg 7 rc 1 AND each of the three ids printed > 0 times in EACH leg.
            --expect pass (HEAD): rc 0 AND rc 0 AND the three ids printed 0 times — a zero beside the base's count — AND [g78] CONTROL:
            the same output names > 0 OTHER GHSA ids (builder: leg 6 names 15), so the zero is a reading of a printing instrument.
  contract  --wt WT --out DIR    `npm run audit:contract`: rc 0, pass == WT's expected-case-count (59), fail 0
  cleanroom --wt WT --out DIR    leg 2: rc 0, the "All N standalone lock(s) pass" line, tracked status identical before/after
  rootci    --wt WT --out DIR    `npm ci --ignore-scripts` at WT/Blockchain/Dev (the ROOT lock, its natural place): rc 0, lock sha256
            identical, and the HOISTED handlebars version read off disk == 4.7.10 (at a head) — the version is a READING, printed either way
  iso       --wt WT --repo CLONE --base B --out DIR   EACH CHANGED STANDALONE LOCK INSTALLED AS ITS DOCKERFILE DOES: the lock dir's
            package.json + package-lock.json copied to DIR/iso/<name>/ (NOT under the workspace root: no ancestor package.json, asserted
            — a workspace member's own `npm ci` resolves against the ROOT lock), `npm ci --ignore-scripts`: rc 0, lock sha256 unchanged,
            handlebars READ OFF DISK == 4.7.10
  omit      --wt WT --repo CLONE --base B --out DIR --tag head|base   [g78] RUNTIME REACH BY INSTALL: each changed standalone lock copied
            isolated as above, `npm ci --ignore-scripts --omit=dev` (the production install every runner / prune performs): handlebars
            READ OFF DISK (version or ABSENT) per service, compared with kit reach_builder_claims (ships: originate; absent: governance,
            referral, vc-issuer). At --tag base the same install is the CONTROL: originate must show 4.7.9 present (the instrument can say
            yes) and the dev-only services ABSENT (it can say no).
  wsuites   --wt WT --out DIR --tag base|head   the builder's WORKSPACE mode: root `npm ci --ignore-scripts`, `npm run build
            --workspace=packages/shared` (dist/index.js ASSERTED — without it every suite importing @secuura/shared fails to LOAD: the
            drafter's first run read governance 32 tests with 2 of 4 suites failed, quarantined), then each of the four services'
            `npm run build` (tsc; builder: originate rc 0) and unit suite (governance / originate: jest; referral / vc-issuer: vitest) from its own dir; summaries parsed into (failed, passed,
            total) PLUS the suite / file line (suites failed, total) + failing test names; writes DIR/wsuites_<tag>.json.
            NOTE [g78]: the services' tests resolve @secuura/shared through the WORKSPACE, so they cannot run from an isolated copy of a
            standalone lock (the drafter tried: `Cannot find module '@secuura/shared'`). The standalone locks are exercised by `iso` and
            `omit` (installs), not by a suite — say so.
  compare   --a <suites_base.json> --b <suites_head.json>   NOTHING fails at b that passes at a (same failing-test set or a subset), every
            suite has a parsed summary on both sides (NOT RUN is never a pass); counts printed side by side against the builder's claims
  nc        --wt WT --repo CLONE --base B --out DIR   NEGATIVE CONTROLS on the HEAD worktree, [g78] ONE ARM PER CHANGED LOCK (kit nc_arms):
            the lock's handlebars entry put back to its BASE entry ALONE; each plant ASSERTED LANDED (sha256 moved AND the entry == base),
            BOTH legs run; the arm's OWN leg must go rc 1 naming each of the three ids, the OTHER leg must stay rc 0 naming 0 (specificity:
            leg 6 reads only the root lock, leg 7 only the standalone locks — the repo CLAUDE.md's claim, measured). Restored BY CONTENT,
            sha256-verified; `git status --porcelain` empty after.
  --selftest   TAP / jest / vitest parsing, id counting, the rc classification, the compare predicate, the omit table predicate.
rc 0 / 1 (a FAIL or a NOT RUN) / 2 refused."""
import hashlib, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate78 import K, Tally, git_bytes, outside_forbidden, detect_indent, pkg_name, req, opt

LG = K['legs']; THREE = K['three_ids']; PLAN = K['plan']; SU = K['suites']; RB = K['reach_builder_claims']
PKG = sorted(PLAN)[0]
TIMEOUT = int(os.environ.get('G78_LEG_TIMEOUT', '1800'))
GHSA = re.compile(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}')


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


def other_ids(text): return sorted(set(GHSA.findall(text)) - set(THREE))


def classify(rc):
    return {0: 'PASS', 1: 'FAIL-FINDINGS', 2: 'COULD-NOT-CHECK (NOT RUN)', 3: 'MALFORMED-BASELINE', 124: 'TIMEOUT (NOT RUN)'}.get(rc, 'rc %d' % rc)


def tap(text):
    g = lambda k: int(m.group(1)) if (m := re.search(r'^(?:#|ℹ) %s (\d+)' % k, text, re.M)) else None
    return {'tests': g('tests'), 'pass': g('pass'), 'fail': g('fail'), 'skipped': g('skipped'), 'todo': g('todo')}


ANSI = re.compile(r'\x1b\[[0-9;]*m')


def suite_summary(text):
    """[g78] jest `Tests:  N failed, M passed, T total` or vitest `Tests  N failed | M passed (T)` -> {failed, passed, skipped, total,
    failing}. The LAST summary line wins. None when no summary line exists (the suite did NOT run)."""
    t = ANSI.sub('', text); out = {'failed': 0, 'passed': 0, 'skipped': 0, 'todo': 0, 'total': None, 'failing': [], 'runner': None,
                                   'suites_failed': 0, 'suites_total': None}
    sl = [l for l in t.split('\n') if re.match(r'^\s*(Test Suites:|Test Files)\s+\d', l)]
    if sl:
        m = re.search(r'(\d+)\s+failed', sl[-1]); out['suites_failed'] = int(m.group(1)) if m else 0
        m = re.search(r'(\d+)\s+total|\((\d+)\)', sl[-1]); out['suites_total'] = int(m.group(1) or m.group(2)) if m else None
    jl = [l for l in t.split('\n') if re.match(r'^\s*Tests:\s+\d', l)]
    vl = [l for l in t.split('\n') if re.match(r'^\s*Tests\s+\d', l)]
    if jl:
        l = jl[-1]; out['runner'] = 'jest'
        for n, w in re.findall(r'(\d+)\s+(failed|passed|skipped|todo)', l): out[w] = int(n)
        m = re.search(r'(\d+)\s+total', l); out['total'] = int(m.group(1)) if m else None
        out['failing'] = sorted(set(x.strip() for x in re.findall(r'^\s*●\s+(.+?)\s*$', t, re.M) if '›' in x))
    elif vl:
        l = vl[-1]; out['runner'] = 'vitest'
        for n, w in re.findall(r'(\d+)\s+(failed|passed|skipped|todo)', l): out[w] = int(n)
        m = re.search(r'\((\d+)\)', l); out['total'] = int(m.group(1)) if m else None
        out['failing'] = sorted(set(re.sub(r'\s+\d+m?s$', '', x.strip()) for x in re.findall(r'^\s*(?:FAIL|×|✗)\s+(.+?)\s*$', t, re.M) if '>' in x))
    else:
        return None
    return out


def dev(wt): return os.path.join(wt, LG['cwd'])


def base_ok(r6, r7, c6, c7): return r6 == 1 and r7 == 1 and all(c6.get(i, 0) > 0 for i in THREE) and all(c7.get(i, 0) > 0 for i in THREE)


def head_ok(r6, r7, c, others6, match7):
    """[g78] the zero is a reading only beside a printing control in EACH leg: leg 6 names other GHSA ids; leg 7 prints no ids at a
    pass, so its control is its own `N advisories match` count (> 0: it matched and reported baselined advisories)."""
    return r6 == 0 and r7 == 0 and sum(c.get(i, 0) for i in THREE) == 0 and len(others6) > 0 and (match7 or 0) > 0


def guard(wt):
    if not outside_forbidden(wt):
        raise SystemExit('REFUSED: %s is under %s — run in YOUR OWN worktree' % (wt, K['forbidden_root']))
    if not os.path.isdir(dev(wt)):
        raise SystemExit('REFUSED: %s has no %s (a --no-checkout clone is not a worktree)' % (wt, LG['cwd']))


def guard_out(out):
    if not outside_forbidden(out):
        raise SystemExit('REFUSED: --out %s is under %s — evidence and copies go to YOUR scratch' % (out, K['forbidden_root']))


def audit_deps(wt, out):
    d = os.path.join(wt, LG['audit_deps_dir'])
    if os.path.isdir(os.path.join(d, 'node_modules', 'semver')):
        print('DEPS scripts/audit/node_modules/semver present'); return 0
    return run(['npm', 'ci', '--ignore-scripts'], d, out, 'auditdeps_npm_ci')[0]


def run_legs(wt, out, tag):
    r6, o6 = run(LG['leg6'], dev(wt), out, tag + '6'); r7, o7 = run(LG['leg7'], dev(wt), out, tag + '7')
    return r6, o6, r7, o7


def legs(wt, expect, out, t, tag='leg'):
    if audit_deps(wt, out) != 0:
        t.check('LEGS', False, 'scripts/audit deps did not install: LOAD FAILURE, NOT RUN'); return {}
    r6, o6, r7, o7 = run_legs(wt, out, tag)
    c6, c7 = count_ids(o6, THREE), count_ids(o7, THREE); c = dict((i, c6[i] + c7[i]) for i in THREE)
    s6 = re.search(r'audit-gate: (\d+) distinct advisories reported, (\d+) baselined', o6)
    m = re.search(r'audit-locks: (\d+) standalone lockfiles', o7); pk = re.search(r'(\d+) distinct packages pinned', o7)
    mb = re.search(r'(\d+) advisories match, (\d+) already baselined', o7)
    oth6, oth7 = other_ids(o6), other_ids(o7)
    print('LEG6 rc %d %s | %s reported / %s baselined | ids %s | OTHER GHSA ids named %d' % (r6, classify(r6), s6 and s6.group(1), s6 and s6.group(2), c6, len(oth6)))
    print('LEG7 rc %d %s | %s locks, %s packages, %s match / %s baselined | ids %s | OTHER GHSA ids named %d' % (
        r7, classify(r7), m and m.group(1), pk and pk.group(1), mb and mb.group(1), mb and mb.group(2), c7, len(oth7)))
    print('BUILDER CLAIMS: %s' % LG['builder_claims'])
    if expect == 'fail':
        t.check('G-BASE', base_ok(r6, r7, c6, c7), 'BASE CONTROL: leg 6 rc %d, leg 7 rc %d (want 1 / 1, never 2) | ids in leg 6 %s, in leg 7 %s (want each > 0 in each)' % (r6, r7, c6, c7))
    else:
        m7 = int(mb.group(1)) if mb else None
        t.check('G-HEAD', head_ok(r6, r7, c, oth6, m7), 'HEAD: leg 6 rc %d, leg 7 rc %d (want 0 / 0) | the three ids printed %s (want 0 each; the base control is the other half) | CONTROLS: leg 6 names %d OTHER GHSA ids (want > 0), leg 7 "%s advisories match" (want > 0)' % (
            r6, r7, c, len(oth6), m7))
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
    t.check('ROOTCI', rc == 0 and a == b and all(hv[n] == PLAN[n]['new'] for n in PLAN), 'root npm ci --ignore-scripts rc %d | lock sha256 %s -> %s identical %s | %s | hoisted on disk %s (want %s)' % (
        rc, a[:16], b[:16], a == b, m.group(0) if m else 'no "added N" line', hv, dict((n, PLAN[n]['new']) for n in PLAN)))


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


def iso_copy(wt, l, d):
    os.makedirs(d, exist_ok=False)
    for f in ('package.json', 'package-lock.json'): shutil.copy2(os.path.join(wt, os.path.dirname(l), f), d)


def iso(wt, repo, base, out, t):
    head = head_of(wt); ch = changed_locks(repo, base, head); res = []
    print('ISO changed standalone locks (base %s .. worktree HEAD %s): %s' % (base[:12], head[:12], ch))
    for l in ch:
        name = os.path.dirname(l).split('/')[-1]; d = os.path.join(out, 'iso', name)
        iso_copy(wt, l, d); anc = ancestors_clean(d)
        a = sha(os.path.join(d, 'package-lock.json'))
        rc, o = run(['npm', 'ci', '--ignore-scripts'], d, out, 'iso_' + name)
        b = sha(os.path.join(d, 'package-lock.json')); m = re.search(r'added (\d+) packages?', o)
        on_disk = dict((n, disk_version(d, n)) for n in PLAN)
        ok = bool(rc == 0 and a == b and not anc and all(on_disk[n] == PLAN[n]['new'] for n in PLAN))
        res.append(ok)
        print('  %s rc %d lock unchanged %s | ancestor package.json %s | added %s | ON DISK %s' % (l, rc, a == b, anc or 'none', m.group(1) if m else None, on_disk))
    t.check('ISO', len(res) == len(K['pr']['numstat']) - 1 and all(res), 'isolated npm ci per changed standalone lock (Dockerfile shape): %d/%d rc 0, lock unchanged, no workspace root above, the new version ON DISK (kit: %d standalone locks)' % (
        sum(res), len(res), len(K['pr']['numstat']) - 1))


def omit_table_ok(table, tag):
    """[g78] table {service: version-or-None}. head: shipping services carry the NEW version, the others carry nothing.
    base (CONTROL): shipping services carry an OLD version (the instrument can say yes), the others nothing (it can say no)."""
    why = []
    for svc in RB['images_shipping']:
        s = svc.split('/')[-1]; v = table.get(s, 'NOT MEASURED')
        want = [PLAN[PKG]['new']] if tag == 'head' else PLAN[PKG]['old']
        if v not in want: why.append('%s: %s (want %s)' % (s, v, want))
    for svc in RB['not_shipping']:
        s = svc.split('/')[-1]; v = table.get(s, 'NOT MEASURED')
        if v is not None: why.append('%s: %s (want ABSENT)' % (s, v))
    return not why, why


def omit(wt, repo, base, out, tag, t):
    head = head_of(wt); ch = changed_locks(repo, base, head) if tag == 'head' else changed_locks(repo, base, K['pr']['head_expected'])
    table = {}; rcs = {}
    print('OMIT (%s) worktree HEAD %s: production installs of %s' % (tag, head[:12], ch))
    for l in ch:
        name = os.path.dirname(l).split('/')[-1]; d = os.path.join(out, 'omit_%s' % tag, name)
        iso_copy(wt, l, d); anc = ancestors_clean(d)
        a = sha(os.path.join(d, 'package-lock.json'))
        rc, o = run(['npm', 'ci', '--ignore-scripts', '--omit=dev'], d, out, 'omit_%s_%s' % (tag, name))
        b = sha(os.path.join(d, 'package-lock.json'))
        table[name] = disk_version(d, PKG); rcs[name] = (rc, a == b, anc)
        nm = os.path.isdir(os.path.join(d, 'node_modules'))
        print('  %s --omit=dev rc %d lock unchanged %s ancestors %s node_modules present %s | %s ON DISK: %s' % (l, rc, a == b, anc or 'none', nm, PKG, table[name] or 'ABSENT'))
    ok, why = omit_table_ok(table, tag)
    allrc = all(r[0] == 0 and r[1] and not r[2] for r in rcs.values()) and len(rcs) == len(K['pr']['numstat']) - 1
    t.check('OMIT-%s' % tag.upper(), ok and allrc, 'RUNTIME REACH BY INSTALL (%s): %s ON DISK after `npm ci --omit=dev` %s | every install rc 0, lock unchanged, isolated: %s %s' % (
        tag, PKG, dict((k, v or 'ABSENT') for k, v in table.items()), allrc, why or ''))
    json.dump({'tag': tag, 'head': head, 'table': table}, open(os.path.join(out, 'omit_%s.json' % tag), 'w'), indent=1)


def copytree(src, dst):
    shutil.copytree(src, dst, symlinks=True, ignore=shutil.ignore_patterns('node_modules', 'dist', 'coverage', '.turbo'))


def wsuites(wt, out, tag, t):
    res = {'tag': tag, 'head': head_of(wt), 'mode': 'workspace'}
    r0, _ = run(['npm', 'ci', '--ignore-scripts'], dev(wt), out, '%s_ws_root_ci' % tag)
    r1, _ = run(['npm', 'run', 'build', '--workspace=packages/shared'], dev(wt), out, '%s_ws_shared_build' % tag)
    built = os.path.isfile(os.path.join(dev(wt), 'packages', 'shared', 'dist', 'index.js'))
    res['prep'] = {'root_ci': r0, 'shared_build': r1, 'dist_index_js': built, 'hoisted': disk_version(dev(wt), PKG)}
    print('PREP root ci %d | shared build %d | packages/shared/dist/index.js %s | %s hoisted %s' % (r0, r1, built, PKG, res['prep']['hoisted']))
    for s, cfg in SU.items():
        rb, _ = run(cfg['build'], os.path.join(wt, cfg['dir']), out, '%s_ws_%s_build' % (tag, s))
        rt, o = run(cfg['test'], os.path.join(wt, cfg['dir']), out, '%s_ws_%s_test' % (tag, s), env={'CI': 'true'})
        res[s] = {'build_rc': rb, 'test_rc': rt, 'summary': suite_summary(o)}
        print('WSUITE %s build rc %d | test rc %d %s (builder: %s)' % (s, rb, rt, res[s]['summary'], cfg['builder_claim']))
    jf = os.path.join(out, 'wsuites_%s.json' % tag); json.dump(res, open(jf, 'w'), indent=1); print('JSON %s' % jf)
    t.check('WSUITES-%s' % tag.upper(), r0 == 0 and r1 == 0 and built and all(res[s]['summary'] and res[s]['build_rc'] == 0 for s in SU),
            'workspace mode: root ci rc %d, shared build rc %d, dist/index.js %s, per service (build rc, summary parsed): %s — red tests are ruled by `compare`, not here' % (
                r0, r1, built, dict((s, (res[s]['build_rc'], bool(res[s]['summary']))) for s in SU)))


def suites_compare(a, b):
    why = []
    for s in SU:
        va, vb = (a.get(s) or {}).get('summary'), (b.get(s) or {}).get('summary')
        if va is None or vb is None: why.append('%s: a summary is missing (NOT RUN)' % s); continue
        new = sorted(set(vb['failing']) - set(va['failing']))
        if new or vb['failed'] > va['failed']: why.append('%s: NEW failures at b %s (%d vs %d)' % (s, new, vb['failed'], va['failed']))
        if vb.get('suites_failed', 0) > va.get('suites_failed', 0): why.append('%s: MORE suites / files failed to run at b (%d vs %d)' % (s, vb.get('suites_failed', 0), va.get('suites_failed', 0)))
    return not why, why


def compare(fa, fb, t):
    a = json.load(open(fa)); b = json.load(open(fb))
    for s, cfg in SU.items():
        print('COUNTS %-10s a(%s %s) %s | b(%s %s) %s | builder %s' % (s, a['tag'], a.get('mode'), (a.get(s) or {}).get('summary'), b['tag'], b.get('mode'),
                                                                  (b.get(s) or {}).get('summary'), cfg['builder_claim']))
    ok, why = suites_compare(a, b)
    t.check('SUITES-CMP', ok and a.get('mode') == b.get('mode'), 'mode %s vs %s; nothing fails at b that passes at a, every summary present on both sides %s' % (a.get('mode'), b.get('mode'), why or ''))


def _revert_entry(path, key, base_entry):
    raw = open(path, 'rb').read(); n = detect_indent(raw.decode()); j = json.loads(raw)
    j['packages'][key] = base_entry
    open(path, 'wb').write((json.dumps(j, indent=n, ensure_ascii=False) + '\n').encode())
    return raw


def nc_ok(r_own, c_own, r_other, c_other):
    return r_own == 1 and all(c_own.get(i, 0) > 0 for i in THREE) and r_other == 0 and not any(c_other.get(i, 0) for i in THREE)


def nc(wt, repo, base, out, t):
    guard(wt)
    if audit_deps(wt, out) != 0:
        t.check('NC', False, 'deps did not install: NOT RUN'); return
    key = 'node_modules/%s' % PKG
    for cid, lock_rel, own, other in K['nc_arms']:
        p = os.path.join(wt, lock_rel); h0 = sha(p)
        be = json.loads(git_bytes(repo, base, lock_rel))['packages'][key]
        orig = _revert_entry(p, key, be)
        landed = sha(p) != h0 and json.loads(open(p, 'rb').read())['packages'][key] == be
        if landed:
            r6, o6, r7, o7 = run_legs(wt, out, '%s_leg' % cid.lower())
        else:
            r6 = r7 = None; o6 = o7 = ''
        open(p, 'wb').write(orig); rest = sha(p) == h0
        R = {'leg6': (r6, count_ids(o6, THREE)), 'leg7': (r7, count_ids(o7, THREE))}
        t.check(cid, landed and rest and nc_ok(R[own][0], R[own][1], R[other][0], R[other][1]),
                '%s %s put back to its BASE entry %s ALONE (landed %s) -> %s rc %s ids %s (want rc 1, each > 0) | %s rc %s ids %s (want rc 0, all 0) | restored sha256-identical %s' % (
                    lock_rel.replace('Blockchain/Dev/', ''), PKG, be.get('version'), landed, own, R[own][0], R[own][1], other, R[other][0], R[other][1], rest))
    pc = porcelain(wt)
    t.check('NC-CLEAN', pc == '', '`git status --porcelain --untracked-files=no` after the arms: %d lines' % pc.count('\n'))


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(tap('# tests 59\n# pass 59\n# fail 0\n') == {'tests': 59, 'pass': 59, 'fail': 0, 'skipped': None, 'todo': None}, 'TAP summary parsed')
    rep(tap('ℹ tests 59\nℹ pass 59\nℹ fail 0\nℹ duration_ms 0.028459\n')['pass'] == 59, 'spec-reporter summary parsed (a timing value carrying "59" is not read)')
    rep(tap('ok 1\n')['pass'] is None, 'PLANTED a TAP with no summary yields None (C5 then FAILS)')
    j = suite_summary('Test Suites: 1 failed, 95 passed, 96 total\nTests:       2 failed, 1091 passed, 1093 total\n  ● Offers › rejects a negative offset\n')
    rep(j and j['runner'] == 'jest' and j['failed'] == 2 and j['passed'] == 1091 and j['total'] == 1093 and j['failing'] == ['Offers › rejects a negative offset'],
        'jest: the Tests: line (not Test Suites:) + the failing name parsed: %s' % j)
    v = suite_summary(' FAIL  src/a.test.ts > b > c\n Test Files  1 failed | 16 passed (17)\n      Tests  1 failed | 158 passed (159)\n')
    rep(v and v['runner'] == 'vitest' and v['failed'] == 1 and v['passed'] == 158 and v['total'] == 159 and len(v['failing']) == 1, 'vitest: Tests line (not Test Files) parsed: %s' % v)
    rep(suite_summary('      Tests  157 passed | 2 skipped (159)\n')['skipped'] == 2, 'vitest prints skipped AFTER passed: parsed')
    js = suite_summary('Test Suites: 2 failed, 2 passed, 4 total\nTests:       32 passed, 32 total\n')
    rep(js['suites_failed'] == 2 and js['suites_total'] == 4 and js['failed'] == 0, 'jest: 0 failed TESTS but 2 of 4 SUITES failed to load is SEEN (the drafter\'s first-run trap): %s' % js)
    vs = suite_summary(' Test Files  3 failed | 14 passed (17)\n      Tests  24 passed | 24 skipped (48)\n')
    rep(vs['suites_failed'] == 3 and vs['suites_total'] == 17, 'vitest: 3 of 17 FILES failed to load is SEEN')
    rep(suite_summary('no summary here') is None, 'PLANTED output with no Tests line yields None (a suite that printed nothing did NOT run)')
    rep(classify(2).endswith('(NOT RUN)') and classify(124).endswith('(NOT RUN)'), 'rc 2 and a timeout classify as NOT RUN')
    z = dict((i, 0) for i in THREE); one = dict((i, 1) for i in THREE)
    rep(head_ok(0, 0, z, ['GHSA-aaaa-bbbb-cccc'], 7), 'G-HEAD: zero ids with both printing controls passes')
    rep(not head_ok(0, 0, z, [], 7), 'PLANTED leg 6 naming NO other id (a silent instrument) FAILS G-HEAD')
    rep(not head_ok(0, 0, z, ['x'], None), 'PLANTED leg 7 with no `N advisories match` line FAILS G-HEAD')
    rep(not head_ok(0, 0, z, ['x'], 0), 'PLANTED leg 7 matching 0 advisories (a blind query) FAILS G-HEAD')
    rep(not head_ok(0, 0, dict(z, **{THREE[0]: 1}), ['x'], 7), 'PLANTED a head still naming an id FAILS G-HEAD')
    rep(not head_ok(2, 0, z, ['x'], 7), 'PLANTED leg 6 rc 2 (COULD-NOT-CHECK) FAILS G-HEAD')
    rep(base_ok(1, 1, one, one) and not base_ok(2, 1, one, one) and not base_ok(1, 1, one, dict(one, **{THREE[2]: 0})), 'G-BASE: rc 1/1 with EVERY id in EACH leg passes; rc 2 and an id missing from one leg both FAIL')
    rep(other_ids('GHSA-8r5x-fm3f-whwj GHSA-abcd-efgh-ijkl GHSA-abcd-efgh-ijkl') == ['GHSA-abcd-efgh-ijkl'], 'other_ids: the three excluded, duplicates collapsed')
    rep(nc_ok(1, one, 0, z), 'NC: own leg red naming all three, other leg green naming none passes')
    rep(not nc_ok(1, one, 1, one), 'PLANTED other leg ALSO red (not specific) FAILS the arm')
    rep(not nc_ok(0, z, 0, z), 'PLANTED own leg green (the plant did nothing) FAILS the arm')
    rep(not nc_ok(1, dict(one, **{THREE[1]: 0}), 0, z), 'PLANTED own leg red without one of the three FAILS the arm')
    rep(omit_table_ok({'originate': '4.7.10', 'governance': None, 'referral': None, 'vc-issuer': None}, 'head')[0], 'OMIT head: originate 4.7.10, others ABSENT passes')
    rep(not omit_table_ok({'originate': '4.7.10', 'governance': '4.7.10', 'referral': None, 'vc-issuer': None}, 'head')[0], 'PLANTED governance shipping handlebars FAILS OMIT')
    rep(not omit_table_ok({'originate': None, 'governance': None, 'referral': None, 'vc-issuer': None}, 'head')[0], 'PLANTED originate ABSENT (the instrument says no to everything) FAILS OMIT')
    rep(not omit_table_ok({'originate': '4.7.10', 'governance': None, 'referral': None}, 'head')[0], 'PLANTED a service NOT MEASURED FAILS OMIT')
    rep(omit_table_ok({'originate': '4.7.9', 'governance': None, 'referral': None, 'vc-issuer': None}, 'base')[0], 'OMIT base CONTROL: originate 4.7.9 passes')
    rep(not omit_table_ok({'originate': '4.7.10', 'governance': None, 'referral': None, 'vc-issuer': None}, 'base')[0], 'OMIT base CONTROL: a base showing 4.7.10 FAILS')
    sa = {'tag': 'base', 'mode': 'workspace', 'governance': {'summary': {'failed': 0, 'failing': []}}, 'originate': {'summary': {'failed': 0, 'failing': []}},
          'referral': {'summary': {'failed': 0, 'failing': []}}, 'vc-issuer': {'summary': {'failed': 0, 'failing': []}}}
    rep(suites_compare(sa, json.loads(json.dumps(sa)))[0], 'compare: identical green passes')
    sb = json.loads(json.dumps(sa)); sb['originate']['summary'] = {'failed': 1, 'failing': ['x › y']}
    rep(not suites_compare(sa, sb)[0], 'PLANTED a NEW failure at b FAILS compare')
    sc = json.loads(json.dumps(sa)); del sc['referral']
    rep(not suites_compare(sa, sc)[0], 'PLANTED a missing suite summary FAILS compare (NOT RUN is never a pass)')
    sd = json.loads(json.dumps(sa)); sd['governance']['summary'] = {'failed': 0, 'failing': [], 'suites_failed': 2}
    rep(not suites_compare(sa, sd)[0], 'PLANTED 2 suites failing to LOAD at b (0 failed tests) FAILS compare')
    rep(not outside_forbidden(K['forbidden_root'] + '/x') and outside_forbidden('/private/tmp/x'), 'the worktree / out guard refuses the forbidden root (lexical; no path is created)')
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
        wt = os.path.abspath(req(A, '--wt')); out = os.path.abspath(req(A, '--out')); guard(wt); guard_out(out)
        print('C5 %s in worktree %s at HEAD %s' % (A[0], wt, head_of(wt)))
        if A[0] == 'legs':
            if opt(A, '--expect') not in ('fail', 'pass'): print('REFUSED: --expect fail|pass'); return 2
            legs(wt, opt(A, '--expect'), out, t)
        elif A[0] == 'contract': contract(wt, out, t)
        elif A[0] == 'cleanroom': cleanroom(wt, out, t)
        elif A[0] == 'rootci': rootci(wt, out, t)
        elif A[0] == 'iso': iso(wt, req(A, '--repo'), req(A, '--base', True), out, t)
        elif A[0] == 'omit':
            tag = req(A, '--tag')
            if tag not in ('head', 'base'): print('REFUSED: --tag head|base'); return 2
            omit(wt, req(A, '--repo'), req(A, '--base', True), out, tag, t)
        elif A[0] == 'wsuites': wsuites(wt, out, req(A, '--tag'), t)
        elif A[0] == 'nc': nc(wt, req(A, '--repo'), req(A, '--base', True), out, t)
        else: print(__doc__); return 2
    except SystemExit as e:
        print(e); return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
