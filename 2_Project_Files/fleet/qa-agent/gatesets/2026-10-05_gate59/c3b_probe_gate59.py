#!/usr/bin/env python3
"""c3b_probe_gate59.py — gate59 C3b SECURITY PROBE for #1382 (KS-1005): the GATE's OWN cells (c3b_probe_ks1005_gate59.test.ts.txt), run
at develop and at head in YOUR installed scratch worktree, the probe MOVED out to <out>/quarantine/ after each run (never left, never
deleted). Cells: P1 wrong current password -> 400 + nothing written; P2 right -> 200, the loader SELECT (the first) is the ONLY one naming password_hash, new hash
written and verifying the NEW password only; P3 passwordless -> 404 (Q-1005); P4 the strength gate REACHED ('password1') -> too weak;
P5 pass-the-hash -> 400; P6 (control) no currentPassword -> zod 400 before any SELECT; T1 a timing note (records only).
  B1 at DEVELOP: P1, P2, P4, P5 FAIL BY ASSERTION with the 404 received; P3, P6, T1 PASS; 7 cells ran, 0 load failures.
  B2 at HEAD: 7 / 7 pass.
  B3 the probe moved out, `git status --porcelain` empty.
  NOTE timing (never asserted): medians written by T1 at each sha. The route is self-scoped (req.user.userId from authenticate), so it
       cannot enumerate OTHER accounts; a wrong-vs-right gap is the password hash's own verify cost, and passwordless (404 before verify)
       is faster BY DESIGN. Rule whether that matters; nothing here measures a real network or a gateway.
--selftest  planted vitest JSON: the real develop shape PASSES B1; P3 red at develop, P1 green at develop (no flip), a loadfail, P4 red by
            timeout each FAIL B1; 7/7 at head PASSES B2; P2 red at head FAILS B2.
Usage: c3b_probe_gate59.py --repo <clone> --worktree <wt> --out <dir> [--head sha] | --selftest      rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, wgit, now, Checks, opt_factory, guard_scratch, guard_out, run, has_commit, move_out, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', K['head']); DEV = K['develop']
G = os.path.dirname(os.path.abspath(__file__)); STRIP = lambda s: re.sub(r'\x1b\[[0-9;]*m', '', s or '')
LOADFAIL = ['Failed to load', 'Cannot find module', 'SyntaxError', 'Failed to resolve import']


def cells(j):
    c = {}; ferr = []
    for t in j.get('testResults', []):
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in STRIP(t.get('message')) for s in LOADFAIL)):
            ferr.append(STRIP(t.get('message'))[:160])
        for a in t.get('assertionResults', []):
            m = re.search(r'gate59 (P\d|T\d)', a.get('fullName') or a['title'])
            if m: c[m.group(1)] = (a['status'], STRIP(((a.get('failureMessages') or ['']) + [''])[0]))
    return c, ferr


def judge_dev(C, j):
    c, ferr = cells(j)
    red = all(c.get(p, ('absent', ''))[0] == 'failed' and 'Test timed out' not in c[p][1] and ('AssertionError' in c[p][1] or 'expected' in c[p][1]) and re.search(r'\b404\b', c[p][1]) for p in ('P1', 'P2', 'P4', 'P5'))
    green = all(c.get(p, ('absent',))[0] == 'passed' for p in ('P3', 'P6', 'T1'))
    C.chk('B1 probe at develop', len(c) == 7 and red and green and not ferr, 'cells %s | P1 P2 P4 P5 red BY ASSERTION naming the 404 received: %s | P3 P6 T1 green: %s | load failures %s' % (
        {k: v[0] for k, v in sorted(c.items())}, bool(red), green, ferr or 'NONE'))
    for k, v in sorted(c.items()):
        if v[0] == 'failed': print('INFO B1 %s: %s' % (k, ' '.join(v[1].split())[:180]))


def judge_head(C, j):
    c, ferr = cells(j); bad = sorted(k for k, v in c.items() if v[0] != 'passed')
    C.chk('B2 probe at head', len(c) == 7 and not bad and not ferr, '%d cells, not passed %s | load failures %s' % (len(c), bad or 'NONE', ferr or 'NONE'))
    for k in bad: print('INFO B2 %s: %s' % (k, ' '.join(c[k][1].split())[:180]))


if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    def cl(k, s, m=''): return {'title': 'gate59 %s x' % k, 'fullName': 'gate59 probe KS-1005 gate59 %s x' % k, 'status': s, 'failureMessages': [m] if m else []}
    R404 = 'AssertionError: wrong current password: expected 404 to be 400'
    def J(o):
        cs = [cl(k, o.get(k, 'passed'), o.get(k + 'm', R404) if o.get(k) == 'failed' else '') for k in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'T1')]
        return {'testResults': [{'name': 'x', 'status': 'failed' if any(c['status'] == 'failed' for c in cs) else 'passed', 'message': '', 'assertionResults': cs}]}
    DEVSHAPE = {'P1': 'failed', 'P2': 'failed', 'P4': 'failed', 'P5': 'failed'}
    selftest_arm(st, 'D-0 the expected develop shape (positive control)', lambda C: judge_dev(C, J(DEVSHAPE)), None)
    selftest_arm(st, 'D-1 P3 red at develop', lambda C: judge_dev(C, J(dict(DEVSHAPE, P3='failed'))), 'B1')
    selftest_arm(st, 'D-2 P1 green at develop (no flip)', lambda C: judge_dev(C, J({k: v for k, v in DEVSHAPE.items() if k != 'P1'})), 'B1')
    selftest_arm(st, 'D-3 a load failure', lambda C: judge_dev(C, {'testResults': [{'name': 'x', 'status': 'failed', 'message': 'Failed to load @secuura/shared', 'assertionResults': []}]}), 'B1')
    selftest_arm(st, 'D-4 P4 red by TIMEOUT', lambda C: judge_dev(C, J(dict(DEVSHAPE, P4m='Error: Test timed out in 5000ms. expected 404'))), 'B1')
    selftest_arm(st, 'H-0 7/7 at head (positive control)', lambda C: judge_head(C, J({})), None)
    selftest_arm(st, 'H-1 P2 red at head', lambda C: judge_head(C, J({'P2': 'failed'})), 'B2')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)

if not REPO or not WT or not OUT:
    print(__doc__); raise SystemExit(2)
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
WT = guard_scratch(WT, 'worktree'); OUT = guard_out(OUT)
DIST = os.path.join(WT, K['shared_dist'])
if not (os.path.isfile(DIST) and os.path.getsize(DIST) > 0): print('REFUSING: %s missing or empty (install + build shared first)' % DIST); raise SystemExit(2)
if wgit(WT, 'status', '--porcelain').strip(): print('REFUSING: the worktree is not clean'); raise SystemExit(2)
print('c3b_probe_gate59 %s | worktree %s | develop %s | head %s' % (now(), WT, DEV[:12], HEAD[:12]))
SD = os.path.join(WT, K['suite_dir']); PR = os.path.join(SD, 'src', '__tests__', K['probe_name']); Q = os.path.join(OUT, 'quarantine')
VB = os.path.join(WT, K['install_dir'], 'node_modules', '.bin', 'vitest'); C = Checks(); timing = {}
for name, sha in (('develop', DEV), ('head', HEAD)):
    wgit(WT, 'checkout', '--quiet', '--detach', sha)
    shutil.copyfile(os.path.join(G, K['probe_template']), PR); tf = os.path.join(OUT, 'c3b_timing_%s.json' % name); jf = os.path.join(OUT, 'c3b_probe_%s.json' % name)
    try:
        rc, o, e = run([VB, 'run', os.path.relpath(PR, SD), '--reporter=json', '--outputFile=' + jf], SD, os.path.join(OUT, 'c3b_probe_' + name), env={'GATE59_TIMING_OUT': tf})
    finally:
        move_out(PR, Q, '%s.%s.%s' % (K['probe_name'], name, now().replace(':', '')))
    try: j = json.load(open(jf))
    except Exception as ex: j = {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Failed to load: %s' % ex, 'assertionResults': []}]}
    (judge_dev if name == 'develop' else judge_head)(C, j)
    timing[name] = open(tf).read().strip() if os.path.isfile(tf) else 'NOT WRITTEN'
stt = wgit(WT, 'status', '--porcelain').strip()
C.chk('B3 probe moved out', not stt and not os.path.exists(PR), 'git status --porcelain %r | probe still in the worktree: %s | quarantined copies in %s' % (stt[:100], os.path.exists(PR), Q))
wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
for k, v in timing.items(): print('NOTE timing at %s (medians of 7, ms; this host, mocked db, real password hashing): %s' % (k, v))
n = C.nfail()
print('C3b PROBE %s: %d FAIL of %d checks | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
