#!/usr/bin/env python3
"""c3_tests_gate69.py — C3 TESTS for the gate69 BATCH: red-first, the tamper matrix (one arm per conjunct), suite, tsc, plus PR A's
REAL-SHAPE probe and cell-ORDER probe, and PR B's db.retry CLASSIFIER. --pr A|B; THE HEAD IS A PARAMETER (--head). Runs ONLY in the
gate's OWN installed scratch worktree (refused inside !CODING): `git worktree add --detach <wt> <head>` in YOUR clone, then in
<wt>/Blockchain/Dev `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared` (X1). The drafter ran ONLY --selftest.

RUNNERS: PR A = jest (services/originate), PR B = vitest (services/api-gateway). Both read JSON reports; a cell is matched by its kit
title prefix. 0 EXECUTED or a load signature = LOAD FAILURE — never a red, never "not caught".

MODES
  redfirst --pr P --wt WT --out DIR [--expect-red CELL,CELL]   the PRODUCT file(s) overlaid with the MERGE-BASE blob, tests at the head;
           runs the PR's test file + its sibling files (A: ks458; B: ks1195 + the 6 doubles files). The red set per file must equal
           --expect-red (pass YOUR prediction BEFORE running; default the kit's redfirst_expect) BY ASSERTION; everything else green.
           Restored by content; then the head: all green.
  tamper   --pr P --wt WT --out DIR [--only T1,T2]   each kit tamper ALONE at the head: LANDS exactly once; runs the PR's test file;
           strict arms (the author's A/B/C) must red EXACTLY their kit set; gate-own arms print PREDICTION HIT / MISS (a MISS is a
           finding for the report, not a kit failure); restored by content; a final untampered run all green. B also runs the
           doubles tamper DT1 against ks1231 (proves the double is load-bearing).
  suite    --pr P --wt WT --out DIR    the whole service suite at the merge-base (product overlaid) and at the head, SAME binary; 0 NEW reds.
  tsc      --pr P --wt WT --out DIR    `tsc --noEmit -p .` in the service at the head rc 0; --listFilesOnly lists the product file and the
           PR's test file 0 times (TYPE-UNCHECKED, a named NOT TESTED item); planted TS2322 in the product -> rc != 0; restored.
  realshape --pr A --wt WT --out DIR   BEFORE any `prisma generate`: is node_modules/.prisma/client absent in the worktree? If absent,
           `node -e "require('@prisma/client')"` from services/originate — print the REAL error's code and message and evaluate the
           guard's two conjuncts on it (CODE MODULE_NOT_FOUND? MESSAGE names .prisma/client?). Covers the READY's NOT COVERED "no real
           fresh-worktree MODULE_NOT_FOUND" BY RUNTIME. If the client is present: NOT RUN (the kit never deletes it).
  order    --pr A --wt WT --out DIR [--seeds 1,2,3]   jest --randomize --seed S on the ks1305 file: the cells share a module-level
           prismaClient singleton (set by C2's success path) and a jest.mock factory closure — an order-dependent cell is a FINDING.
  dbretry  --pr B --wt WT --out DIR [--runs 3] [--load N]   classifies E 7th's db.retry fake-timer wall-clock timeout: (1) db.retry.test.ts
           blob identical at merge-base and head, and its imports touch no PR path; (2) --runs quiet runs of that file at the head and
           with the product overlaid to the merge-base, durations per cell; (3) one LOADED run each (N CPU-burner python processes for
           the run's duration, then killed — process kill, no file deleted). PRE-EXISTING iff it behaves the same with and without the PR's
           product change under the same load; CAUSED BY THIS CHANGE only if the head differs from the merge-base overlay.
  --selftest [--repo R]   the judges on PLANTED jest / vitest JSON (shape, load failure, 0 executed, wrong red, skipped, strict vs
           predicted tamper) + (with --repo) every tamper LANDS exactly once on the real head blob, and the head test files declare the
           kit's cell count.
rc 0 PASS / 1 FAIL / 2 refused."""
import hashlib, io, contextlib, json, os, re, shutil, subprocess, sys, time
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate69 import K, git, wgit, Tally, outside_forbidden, resolvable, spec

LOADFAIL = ['Test suite failed to run', 'Cannot find module', 'SyntaxError', 'TS6133', 'error TS', 'Failed to load', 'failed to load']


def now(): return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def run(cmd, cwd, prefix, env=None):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    if prefix:
        open(prefix + '.out', 'w').write(p.stdout); open(prefix + '.err', 'w').write(p.stderr); open(prefix + '.rc', 'w').write('%d\n' % p.returncode)
        open(prefix + '.meta', 'w').write('utc %s | wall %.2fs | cwd %s | cmd %s\n' % (now(), time.time() - t0, cwd, ' '.join(cmd)))
    return p.returncode, p.stdout, p.stderr


def report(sp, wt, files, prefix, extra=None):
    """run the PR's runner on files (relative to the suite dir) -> (rc, json-dict)."""
    sd = os.path.join(wt, sp['suite_dir']); jf = prefix + '.json'
    if sp['runner'] == 'jest':
        cmd = ['npx', 'jest', '--ci'] + (extra or []) + files + ['--json', '--outputFile=' + jf]
    else:
        cmd = ['npx', 'vitest', 'run'] + (extra or []) + files + ['--reporter=json', '--outputFile=' + jf]
    rc, o, e = run(cmd, sd, prefix)
    try:
        return rc, json.load(open(jf))
    except Exception as x:
        return rc, {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Test suite failed to run: ' + str(x), 'assertionResults': []}]}


def cells(j):
    out = {}; ferr = []
    for t in j.get('testResults', []):
        msg = t.get('message') or ''; name = os.path.basename(t.get('name', ''))
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in msg for s in LOADFAIL)):
            ferr.append((name, ' '.join(msg.split())[:200]))
        for a in t.get('assertionResults', []):
            fm = re.sub(r'\x1b\[[0-9;]*m', '', ((a.get('failureMessages') or ['']) + [''])[0])
            out[(name, a.get('fullName') or a.get('title', ''))] = (a.get('status'), fm, a.get('duration'))
    return out, ferr


def by_cell(cs, fname, table):
    r = {}
    for (f, title), v in cs.items():
        if f != fname: continue
        for k, pre in table.items():
            if pre in title: r[k] = v
    return r


def executed(cs, fname): return sum(1 for (f, _), v in cs.items() if f == fname and v[0] in ('passed', 'failed'))
def asserted(msg): return any(s in msg for s in ('expect(', 'Expected', 'AssertionError', 'toBe', 'toEqual', 'toThrow'))
def ncells(src): return len(re.findall(r"^\s*it\(", src, re.M))


def tables(sp):
    """{file basename: cell table} for the PR's own files."""
    t = {os.path.basename(sp['test']): sp['cells']}
    if sp['key'] == 'B': t[os.path.basename(sp['ks1195_file'])] = sp['cells_ks1195_repointed']
    return t


def judge_files(t, tag, j, expect, ncell):
    """expect: {basename: [cells that must be RED by assertion]}; ncell: {basename: executed count}. Every other cell in those files green."""
    cs, ferr = cells(j); ok = not ferr; rows = []
    for fname, n in ncell.items():
        ex = executed(cs, fname)
        reds = sorted(f[1][:60] for f, v in cs.items() if f[0] == fname and v[0] == 'failed')
        notpass = [f[1][:60] for f, v in cs.items() if f[0] == fname and v[0] not in ('passed', 'failed')]
        tbl = TABLES.get(fname, {})
        named = by_cell(cs, fname, tbl) if tbl else {}
        red_named = sorted(k for k, v in named.items() if v[0] == 'failed')
        want = sorted(expect.get(fname, []))
        by_assert = all(asserted(named[k][1]) for k in red_named)
        unnamed_red = len(reds) - len(red_named)
        good = ex == n and ex > 0 and red_named == want and unnamed_red == 0 and by_assert and not notpass
        ok &= good
        rows.append('%s EXECUTED %d (want %d) red %s (want %s) by-assertion %s unnamed-red %d skipped/pending %s' % (fname[:40], ex, n, red_named, want, by_assert, unnamed_red, notpass or 'NONE'))
    t.check(tag, ok, ' || '.join(rows) + ' | load failures %s' % (ferr or 'NONE'))
    return ok


TABLES = {}


def tamper_verdict(j, fname, ncell):
    cs, ferr = cells(j); ex = executed(cs, fname)
    named = by_cell(cs, fname, TABLES.get(fname, {})); reds = sorted(k for k, v in named.items() if v[0] == 'failed')
    if ex == 0 or ferr: return 'LOAD', reds, ex, ferr
    return ('CAUGHT' if reds else 'NOT CAUGHT'), reds, ex, ferr


def judge_tamper(t, tid, tp, j, fname, ncell):
    v, reds, ex, ferr = tamper_verdict(j, fname, ncell)
    want = sorted(tp['expect'])
    if v == 'LOAD':
        t.check(tid, False, '%s: LOAD FAILURE (0 executed or a load signature) — NEVER "not caught"; fix the tamper, re-run | %s' % (tp['what'][:80], ferr)); return v
    if tp.get('strict'):
        t.check(tid, ex == ncell and reds == want, '%s: EXECUTED %d/%d | %s %s | kit (author\'s claim) %s' % (tp['what'][:80], ex, ncell, v, reds, want))
    else:
        t.check(tid, ex == ncell, '%s: EXECUTED %d/%d | %s %s | drafter PREDICTION %s -> %s' % (tp['what'][:80], ex, ncell, v, reds, want or '[] (blind-spot probe)', 'HIT' if reds == want else 'MISS (a finding to report, with the cells)'))
    return v


def put(wt, p, data): open(os.path.join(wt, p), 'wb').write(data)
def blob(repo, rev, p): return subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, p)], capture_output=True).stdout
def clean(wt): return wgit(wt, 'status', '--porcelain', '--untracked-files=no')[1].strip() == ''


def product_files(sp): return [sp['product_file']]


def own_files(sp):
    if sp['key'] == 'A': return [sp['test']] + list(sp['sibling_tests'])
    return [sp['test'], sp['ks1195_file']] + sp['doubles_files']


def rel(sp, p): return os.path.relpath(p, sp['suite_dir'])


def ncell_map(repo, sp, files):
    return {os.path.basename(p): ncells(blob(repo, sp['head'], p).decode()) for p in files}


def m_redfirst(t, sp, repo, wt, out, expect_override):
    files = own_files(sp); exp = dict(sp['redfirst_expect'])
    if expect_override:
        exp[os.path.basename(sp['test'])] = expect_override
    print('INFO red-first prediction passed BEFORE the run: %s' % exp)
    saved = {p: open(os.path.join(wt, p), 'rb').read() for p in product_files(sp)}
    try:
        for p in product_files(sp): put(wt, p, blob(repo, sp['merge_base'], p))
        t.check('RF0', all(open(os.path.join(wt, p), 'rb').read() == blob(repo, sp['merge_base'], p) for p in product_files(sp)),
                'overlay PROVED present: product == merge-base blob (%s)' % [os.path.basename(p) for p in product_files(sp)])
        rc, j = report(sp, wt, [rel(sp, p) for p in files], os.path.join(out, 'c3_%s_redfirst_base' % sp['key']))
        judge_files(t, 'RF1', j, exp, ncell_map(repo, sp, files))
    finally:
        for p, b in saved.items(): put(wt, p, b)
    t.check('RF1b', all(open(os.path.join(wt, p), 'rb').read() == blob(repo, sp['head'], p) for p in product_files(sp)) and clean(wt), 'restored by content == head blobs; porcelain clean')
    rc, j = report(sp, wt, [rel(sp, p) for p in files], os.path.join(out, 'c3_%s_redfirst_head' % sp['key']))
    judge_files(t, 'RF2', j, {}, ncell_map(repo, sp, files))


def apply_tamper(src, tp):
    c = src.count(tp['from'])
    return c, (src.replace(tp['from'], tp['to'], 1) if c == 1 else src)


def m_tamper(t, sp, repo, wt, out, only):
    fname = os.path.basename(sp['test']); n = ncells(blob(repo, sp['head'], sp['test']).decode())
    arms = dict(sp['tampers']); arms.update(sp.get('doubles_tampers', {}))
    for tid, tp in arms.items():
        if only and tid not in only: continue
        pf = os.path.join(wt, tp['file']); orig = open(pf, 'rb').read(); src = orig.decode()
        c, new = apply_tamper(src, tp)
        if c != 1:
            t.check(tid, False, 'anchor occurs %d time(s) (want 1) — the tamper did NOT land' % c); continue
        try:
            open(pf, 'w').write(new)
            t.check(tid + '-landed', open(pf, 'rb').read() != orig, 'landed; sha256/16 %s -> %s' % (sha(orig)[:16], sha(new)[:16]))
            if 'expect_any_red_in' in tp:
                tf = [p for p in sp['doubles_files'] if os.path.basename(p) == tp['expect_any_red_in']][0]
                rc, j = report(sp, wt, [rel(sp, tf)], os.path.join(out, 'c3_%s_tamper_%s' % (sp['key'], tid)))
                cs, ferr = cells(j); ex = executed(cs, tp['expect_any_red_in']); reds = [f[1][:50] for f, v in cs.items() if v[0] == 'failed']
                t.check(tid, ex > 0 and not ferr and reds, '%s: EXECUTED %d | red %s (want >= 1: the double is LOAD-BEARING) | load %s' % (tp['what'][:80], ex, reds[:4], ferr or 'NONE'))
            else:
                rc, j = report(sp, wt, [rel(sp, sp['test'])], os.path.join(out, 'c3_%s_tamper_%s' % (sp['key'], tid)))
                judge_tamper(t, tid, tp, j, fname, n)
        finally:
            open(pf, 'wb').write(orig)
        t.check(tid + '-restored', open(pf, 'rb').read() == blob(repo, sp['head'], tp['file']) and clean(wt), 'restored by content; porcelain clean')
    rc, j = report(sp, wt, [rel(sp, sp['test'])], os.path.join(out, 'c3_%s_tamper_restored' % sp['key']))
    judge_files(t, 'TR', j, {}, {fname: n})


def m_suite(t, sp, repo, wt, out):
    res = {}
    sd = os.path.join(wt, sp['suite_dir'])
    print('INFO node %s | %s %s' % (run(['node', '--version'], sd, None)[1].strip(), sp['runner'], run(['npx', sp['runner'], '--version'], sd, None)[1].strip()))
    saved = {p: open(os.path.join(wt, p), 'rb').read() for p in product_files(sp)}
    try:
        for p in product_files(sp): put(wt, p, blob(repo, sp['merge_base'], p))
        rc, res['base'] = report(sp, wt, [], os.path.join(out, 'c3_%s_suite_baseoverlay' % sp['key']))
    finally:
        for p, b in saved.items(): put(wt, p, b)
    rc, res['head'] = report(sp, wt, [], os.path.join(out, 'c3_%s_suite_head' % sp['key']))
    fb = {k for k, v in cells(res['base'])[0].items() if v[0] == 'failed'}; fh = {k for k, v in cells(res['head'])[0].items() if v[0] == 'failed'}
    tot = lambda j: (len(j.get('testResults', [])), j.get('numTotalTests'), j.get('numFailedTests'), j.get('numPendingTests'))
    print('INFO suite [files, tests, failed, skipped/pending] base-overlay %s | head %s | claim %s' % (tot(res['base']), tot(res['head']), sp['claims'].get('suite')))
    t.check('S1', not fh and not cells(res['head'])[1] and clean(wt), 'head: failed %d %s | load failures %s (a failure is listed BY NAME; the base-overlay run says whether it pre-exists)' % (
        len(fh), sorted(x[1][:60] for x in fh)[:6], cells(res['head'])[1] or 'NONE'))
    t.check('S2', not (fh - fb), 'NEW reds at head vs base-overlay: %s' % (sorted(x[1][:60] for x in fh - fb) or 'NONE'))


def m_tsc(t, sp, repo, wt, out):
    sd = os.path.join(wt, sp['suite_dir'])
    TSC = next((d for d in (os.path.join(sd, 'node_modules/.bin/tsc'), os.path.join(wt, 'Blockchain/Dev/node_modules/.bin/tsc')) if os.path.exists(d)), None)
    if not TSC: t.check('T0', False, 'no tsc in the worktree node_modules — NOT RUN, never a pass'); return
    rc0 = run([TSC, '--noEmit', '-p', '.'], sd, os.path.join(out, 'c3_%s_tsc_head' % sp['key']))[0]
    lf = run([TSC, '--noEmit', '-p', '.', '--listFilesOnly'], sd, os.path.join(out, 'c3_%s_tsc_listfiles' % sp['key']))[1]
    pb = os.path.basename(sp['product_file']); tb = os.path.basename(sp['test'])
    t.check('T1', rc0 == 0, '%s --noEmit -p . rc %d at head' % (TSC, rc0))
    t.check('T2', ('/' + pb) in lf and tb not in lf, '--listFilesOnly: %s listed %s | %s listed %d time(s) (want 0: TYPE-UNCHECKED, a NAMED NOT TESTED item)' % (pb, ('/' + pb) in lf, tb, lf.count(tb)))
    pf = os.path.join(wt, sp['product_file']); orig = open(pf, 'rb').read()
    try:
        open(pf, 'wb').write(orig + b"\nconst __g69: number = 'x';\n"); rc, o, e = run([TSC, '--noEmit', '-p', '.'], sd, os.path.join(out, 'c3_%s_tsc_positive_control' % sp['key']))
    finally:
        open(pf, 'wb').write(orig)
    t.check('T3', rc != 0 and 'TS2322' in o + e and clean(wt), 'planted TS2322 -> rc %d, TS2322 printed %s | restored, clean %s' % (rc, 'TS2322' in o + e, clean(wt)))


def m_realshape(t, sp, repo, wt, out):
    sd = os.path.join(wt, sp['suite_dir'])
    cands = [os.path.join(sd, 'node_modules/.prisma/client'), os.path.join(wt, 'Blockchain/Dev/node_modules/.prisma/client')]
    present = [c for c in cands if os.path.exists(c)]
    if present:
        t.info('RS', 'NOT RUN: the generated client is PRESENT at %s (the kit never deletes it) — run realshape BEFORE any prisma generate' % present); return
    probe = "try{require('@prisma/client');console.log(JSON.stringify({loaded:true}))}catch(e){console.log(JSON.stringify({code:e.code,message:String(e.message).split('\\n')[0]}))}"
    rc, o, e = run(['node', '-e', probe], sd, os.path.join(out, 'c3_A_realshape'))
    try:
        r = json.loads(o.strip().splitlines()[-1])
    except Exception:
        t.check('RS', False, 'probe printed no JSON (rc %d): %r' % (rc, (o + e)[:200])); return
    code_t = r.get('code') == 'MODULE_NOT_FOUND'; msg_t = '.prisma/client' in (r.get('message') or '')
    t.check('RS', code_t and msg_t, 'REAL fresh-worktree error: code %r message %r | CODE conjunct %s | MESSAGE conjunct %s -> the guard %s on the real shape' % (
        r.get('code'), (r.get('message') or '')[:120], code_t, msg_t, 'FIRES' if code_t and msg_t else 'DOES NOT FIRE'))


def m_order(t, sp, repo, wt, out, seeds):
    fname = os.path.basename(sp['test']); n = ncells(blob(repo, sp['head'], sp['test']).decode())
    for s in seeds:
        rc, j = report(sp, wt, [rel(sp, sp['test'])], os.path.join(out, 'c3_A_order_seed%s' % s), ['--randomize', '--seed=%s' % s])
        cs, ferr = cells(j); fails = [f[1][:50] for f, v in cs.items() if v[0] == 'failed']
        t.check('ORD-%s' % s, executed(cs, fname) == n and not fails and not ferr, 'jest --randomize --seed=%s: executed %d/%d | failed %s | load %s (a red here = an ORDER-DEPENDENT cell: a finding)' % (s, executed(cs, fname), n, fails or 'NONE', ferr or 'NONE'))


def m_dbretry(t, sp, repo, wt, out, runs, load):
    f = sp['dbretry_test']; fb = os.path.basename(f)
    bb, hb = blob(repo, sp['merge_base'], f), blob(repo, sp['head'], f)
    # static `from '…'`, require('…'), dynamic import('…') (db.retry.test.ts:36 does `import('../db')`) and vi.mock('…') targets
    imports = re.findall(r"""from\s+['"]([^'"]+)['"]|require\(['"]([^'"]+)['"]\)|import\(['"]([^'"]+)['"]\)|vi\.mock\(['"]([^'"]+)['"]""", hb.decode())
    imp = sorted(set(next(x for x in g if x) for g in imports))
    touches = [p for p in sp['files'] if any(os.path.splitext(os.path.basename(p))[0] in i for i in imp)]
    t.check('DR1', bb == hb and bb and not touches, '%s blob identical merge-base/head %s | imports %s | PR paths among them %s' % (fb, bb == hb, imp, touches or 'none'))
    def one(tag, overlay, loaded):
        saved = {p: open(os.path.join(wt, p), 'rb').read() for p in product_files(sp)}; procs = []
        try:
            if overlay:
                for p in product_files(sp): put(wt, p, blob(repo, sp['merge_base'], p))
            if loaded:
                procs = [subprocess.Popen([sys.executable, '-c', 'while True: pass']) for _ in range(load)]
            rc, j = report(sp, wt, [rel(sp, f)], os.path.join(out, 'c3_B_dbretry_%s' % tag))
        finally:
            for pr in procs: pr.kill()
            for pr in procs: pr.wait()
            for p, b in saved.items(): put(wt, p, b)
        cs, ferr = cells(j)
        fails = [(k[1][-60:], (v[1] or '')[:60]) for k, v in cs.items() if v[0] == 'failed']
        durs = sorted(((v[2] or 0), k[1][-40:]) for k, v in cs.items())[-2:]
        print('INFO dbretry %-22s executed %d | failed %s | slowest %s | load %s' % (tag, executed(cs, fb), fails or 'NONE', durs, ferr or 'NONE'))
        return bool(fails), executed(cs, fb)
    res = {}
    for i in range(runs):
        res.setdefault('head_quiet', []).append(one('head_quiet_%d' % i, False, False))
        res.setdefault('base_quiet', []).append(one('base_quiet_%d' % i, True, False))
    res['head_loaded'] = [one('head_loaded', False, True)]; res['base_loaded'] = [one('base_loaded', True, True)]
    red = {k: sum(1 for r in v if r[0]) for k, v in res.items()}; ex = {k: [r[1] for r in v] for k, v in res.items()}
    same = (red['head_quiet'] > 0) == (red['base_quiet'] > 0) and (red['head_loaded'] > 0) == (red['base_loaded'] > 0)
    cls = 'PRE-EXISTING (head and merge-base product behave the same under the same load)' if same else 'DIFFERS between head and merge-base — CAUSED BY THIS CHANGE until shown otherwise'
    t.check('DR2', all(all(x > 0 for x in v) for v in ex.values()), 'every run executed cells: %s' % ex)
    t.info('DR3', 'red counts %s (of %d quiet runs each, 1 loaded run each with %d CPU burners) -> %s. A loaded red at BOTH = the KS 1328 class in api-gateway' % (red, runs, load, cls))


def check_wt(sp, wt, out):
    if not wt or not os.path.isdir(wt): print('REFUSED: --wt <worktree> missing'); return False
    if not outside_forbidden(wt) or not outside_forbidden(out): print('REFUSED: worktree / out must lie OUTSIDE %s' % K['forbidden_root']); return False
    h = git(wt, 'rev-parse', 'HEAD').strip()
    if h != sp['head']: print('REFUSED: worktree HEAD %s != the head under test %s' % (h[:12], sp['head'][:12])); return False
    if not clean(wt): print('REFUSED: the worktree is not clean'); return False
    if not os.path.exists(os.path.join(wt, 'Blockchain/Dev/packages/shared/dist/index.js')):
        print('REFUSED: packages/shared/dist/index.js absent — npm ci --ignore-scripts + npm run build --workspace=packages/shared first (X1); a missing dist is a LOAD failure, not a red'); return False
    return True


def selftest(repo):
    ok = n = 0
    def arm(name, fn, want):
        nonlocal ok, n
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): fn(t)
        good = (not t.fails) if want is None else (want in t.fails)
        n += 1; ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, t.fails or 'NONE'))
    for which in ('A', 'B'):
        sp = spec(which, None, '1396' if which == 'B' else None); TABLES.clear(); TABLES.update(tables(sp))
        fname = os.path.basename(sp['test']); cl = sp['cells']; ks = list(cl)
        EM = 'Error: expect(received).toEqual(expected)\nExpected 503'
        def cell(k, s, m=''): return {'title': cl[k] + ' x', 'fullName': 'S ' + cl[k] + ' x', 'status': s, 'failureMessages': [m] if m else [], 'duration': 5}
        def J(cs, msg=''): return {'testResults': [{'name': '/w/src/__tests__/' + fname, 'status': 'failed' if any(c['status'] == 'failed' for c in cs) else 'passed', 'message': msg, 'assertionResults': cs}]}
        rf = sorted(sp['redfirst_expect'][fname]); N = {fname: len(ks)}
        arm('%s red-first claimed shape %s' % (which, rf), lambda t: judge_files(t, 'RF1', J([cell(k, 'failed', EM) if k in rf else cell(k, 'passed') for k in ks]), {fname: rf}, N), None)
        arm('%s red-first LOAD failure is not a red' % which, lambda t: judge_files(t, 'RF1', {'testResults': [{'name': '/w/' + fname, 'status': 'failed', 'message': 'Test suite failed to run\nCannot find module', 'assertionResults': []}]}, {fname: rf}, N), 'RF1')
        arm('%s red-first one red too many' % which, lambda t: judge_files(t, 'RF1', J([cell(k, 'failed', EM) for k in ks]), {fname: rf}, N), 'RF1')
        arm('%s red-first a red with no assertion message' % which, lambda t: judge_files(t, 'RF1', J([cell(k, 'failed', 'TypeError: boom') if k in rf else cell(k, 'passed') for k in ks]), {fname: rf}, N), 'RF1')
        arm('%s a SKIPPED cell is never a pass' % which, lambda t: judge_files(t, 'RF2', J([cell(k, 'skipped' if k == ks[-1] else 'passed') for k in ks]), {}, N), 'RF2')
        tid, tp = next(iter(sp['tampers'].items()))
        sp_strict = dict(tp, strict=True)
        arm('%s tamper %s strict: exactly its set -> PASS' % (which, tid), lambda t: judge_tamper(t, tid, sp_strict, J([cell(k, 'failed', EM) if k in tp['expect'] else cell(k, 'passed') for k in ks]), fname, len(ks)), None)
        arm('%s tamper %s strict: NOT CAUGHT -> FAIL' % (which, tid), lambda t: judge_tamper(t, tid, sp_strict, J([cell(k, 'passed') for k in ks]), fname, len(ks)), tid)
        arm('%s tamper %s: 0 EXECUTED is a LOAD FAILURE -> FAIL' % (which, tid), lambda t: judge_tamper(t, tid, dict(tp, strict=False), {'testResults': [{'name': '/w/' + fname, 'status': 'failed', 'message': 'Test suite failed to run', 'assertionResults': []}]}, fname, len(ks)), tid)
        arm('%s tamper %s predicted (non-strict) MISS is reported, not a kit failure' % (which, tid), lambda t: judge_tamper(t, tid, dict(tp, strict=False), J([cell(k, 'passed') for k in ks]), fname, len(ks)), None)
        if repo:
            arms = dict(sp['tampers']); arms.update(sp.get('doubles_tampers', {}))
            for tid2, tp2 in arms.items():
                src = blob(repo, sp['head'], tp2['file']).decode(); c, new = apply_tamper(src, tp2)
                g = c == 1 and new != src; n += 1; ok += g
                print('SELFTEST %s %s tamper %s LANDS exactly once on the real head %s %s (occurrences %d)' % ('OK' if g else 'MISS', which, tid2, sp['head'][:12], os.path.basename(tp2['file']), c))
            c, _ = apply_tamper(blob(repo, sp['head'], sp['product_file']).decode(), {'from': 'THIS TEXT IS NOT IN THE FILE', 'to': ''})
            n += 1; ok += (c == 0); print('SELFTEST %s %s PLANTED tamper with an absent anchor is NOT landed (occurrences %d)' % ('OK' if c == 0 else 'MISS', which, c))
            nc = ncells(blob(repo, sp['head'], sp['test']).decode()); n += 1; ok += (nc == len(ks))
            print('SELFTEST %s %s head test file declares %d it( cells (kit names %d)' % ('OK' if nc == len(ks) else 'MISS', which, nc, len(ks)))
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); print('CHECKED %d arm(s)' % n)
    return 0 if ok == n else 1


def main():
    A = sys.argv[1:]
    if not A or '--help' in A: print(__doc__); return 2
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if '--selftest' in A: return selftest(opt('--repo'))
    mode = A[0]; which = opt('--pr', 'A')
    sp = spec(which, opt('--head'), opt('--b-pr') if which == 'B' else None)
    TABLES.clear(); TABLES.update(tables(sp))
    repo = opt('--repo'); wt = opt('--wt'); out = opt('--out')
    if not (repo and wt and out): print(__doc__); return 2
    for nm, s in (('head', sp['head']), ('merge-base', sp['merge_base'])):
        if not resolvable(repo, s): print('REFUSED: %s unresolvable: %s' % (nm, s)); return 2
    os.makedirs(out, exist_ok=True)
    if not check_wt(sp, wt, out): return 2
    print('c3_tests_gate69 %s PR %s %s | %s | head %s | merge-base %s | wt %s' % (mode, which, sp['ticket'], now(), sp['head'][:12], sp['merge_base'][:12], wt))
    t = Tally()
    if mode == 'redfirst': m_redfirst(t, sp, repo, wt, out, (opt('--expect-red') or '').split(',') if opt('--expect-red') else None)
    elif mode == 'tamper': m_tamper(t, sp, repo, wt, out, (opt('--only') or '').split(',') if opt('--only') else None)
    elif mode == 'suite': m_suite(t, sp, repo, wt, out)
    elif mode == 'tsc': m_tsc(t, sp, repo, wt, out)
    elif mode == 'realshape' and which == 'A': m_realshape(t, sp, repo, wt, out)
    elif mode == 'order' and which == 'A': m_order(t, sp, repo, wt, out, (opt('--seeds') or '1,2,3').split(','))
    elif mode == 'dbretry' and which == 'B': m_dbretry(t, sp, repo, wt, out, int(opt('--runs', '3')), int(opt('--load', str(os.cpu_count() or 8))))
    else: print('unknown mode %r for PR %s' % (mode, which)); return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
