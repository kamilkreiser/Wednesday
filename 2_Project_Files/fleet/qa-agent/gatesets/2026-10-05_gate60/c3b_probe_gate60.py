#!/usr/bin/env python3
"""c3b_probe_gate60.py — gate60 C3b SECURITY PROBE for #1384 (KS-1210): the GATE's OWN 23 cells (c3b_probe_ks1210_gate60.test.ts.txt), run
at develop and at head in YOUR installed scratch worktree; the probe is MOVED out to <out>/quarantine/ after each run (never left, never
deleted). The probe runs the REAL services/oauth over an in-memory oauth_apps table (a mocked ../db answering the service's exact SQL), the
REAL oauthRouter, authenticate() and errorHandler, and a principal matrix: owner / peer (same tenant) / stranger (other tenant) / ORG_ADMIN of
tenant A and B / ISSUER_ADMIN / the four platform roles / a case-variant role / a connector principal.
  B0 HARNESS   no cell failed on 'unmodelled SQL' (the in-memory table met SQL it does not model — a harness gap, not a finding), and X0
               (create then read back through the route) PASSED at both shas.
  B1 DEVELOP   EXACTLY V1 P1 P2 P3 O1 O3 O4 O7 L2 FAIL, each BY ASSERTION (AssertionError / 'expected', never 'Test timed out'); the other
               14 PASS; 23 cells ran, 0 load failures. (The develop run IS the must-fail arm on real code: the cells can see the change.)
  B2 HEAD      23 / 23 pass.
  B3 CLEAN     the probe moved out, `git status --porcelain` empty.
  NOTE         the OBSERVATIONS each sha wrote to $GATE60_OBS_OUT (V1 statuses, P1 role matrix, O1/O2 matrices, O3 bodies, O8 list sizes, the
               legacy L3/L4 facts, H1 the ORG_ADMIN re-point + re-key of a platform admin's admin:write app, R1 the RLS MODEL) — printed,
               never asserted: the gate rules them (README doubts D1-D4).
--selftest  planted vitest JSON: the expected develop shape PASSES B1; O1 green at develop (no flip), V2 red at develop, a load failure, P1 red
            by TIMEOUT, an 'unmodelled SQL' failure (B0), 22 cells each FAIL; 23/23 at head PASSES B2; L1 red at head FAILS B2.
Usage: c3b_probe_gate60.py --repo <clone> --worktree <wt> --out <dir> [--head sha] | --selftest      rc 0 PASS / 1 FAIL / 2 usage"""
import json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, wgit, now, Checks, opt_factory, guard_scratch, guard_out, run, has_commit, move_out, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', K['head']); DEV = K['develop']
G = os.path.dirname(os.path.abspath(__file__)); STRIP = lambda s: re.sub(r'\x1b\[[0-9;]*m', '', s or '')
LOADFAIL = ['Failed to load', 'Cannot find module', 'SyntaxError', 'Failed to resolve import']
ALL = ['X0', 'V1', 'V2', 'V3', 'V4', 'P1', 'P2', 'P3', 'P4', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'L1', 'L2', 'L3', 'L4', 'H1', 'R1']
DEV_RED = ['V1', 'P1', 'P2', 'P3', 'O1', 'O3', 'O4', 'O7', 'L2']


def cells(j):
    c = {}; ferr = []
    for t in j.get('testResults', []):
        if t.get('status') == 'failed' and (not t.get('assertionResults') or any(s in STRIP(t.get('message')) for s in LOADFAIL)):
            ferr.append(STRIP(t.get('message'))[:160])
        for a in t.get('assertionResults', []):
            m = re.search(r'gate60 ([A-Z]\d)\b', a.get('fullName') or a['title'])
            if m: c[m.group(1)] = (a['status'], STRIP(((a.get('failureMessages') or ['']) + [''])[0]))
    return c, ferr


def harness(C, c, tag):
    um = sorted(k for k, v in c.items() if 'unmodelled SQL' in v[1])
    C.chk('B0 harness (%s)' % tag, not um and c.get('X0', ('absent',))[0] == 'passed', 'cells failing on unmodelled SQL %s | X0 create-then-read-back passed: %s' % (um or 'NONE', c.get('X0', ('absent',))[0] == 'passed'))


def judge_dev(C, j):
    c, ferr = cells(j); harness(C, c, 'develop')
    red = sorted(k for k, v in c.items() if v[0] == 'failed'); green = sorted(k for k, v in c.items() if v[0] == 'passed')
    by_assert = all('Test timed out' not in c[k][1] and ('AssertionError' in c[k][1] or 'expected' in c[k][1]) for k in red)
    C.chk('B1 probe at develop', red == sorted(DEV_RED) and green == sorted(set(ALL) - set(DEV_RED)) and by_assert and not ferr and len(c) == len(ALL),
          '%d cell(s) ran (want %d) | red %s (want %s) | every red by assertion: %s | load failures %s' % (len(c), len(ALL), red, sorted(DEV_RED), by_assert, ferr or 'NONE'))
    for k in red: print('INFO B1 %s: %s' % (k, ' '.join(c[k][1].split())[:200]))


def judge_head(C, j):
    c, ferr = cells(j); harness(C, c, 'head'); bad = sorted(k for k, v in c.items() if v[0] != 'passed')
    C.chk('B2 probe at head', len(c) == len(ALL) and not bad and not ferr, '%d cells (want %d), not passed %s | load failures %s' % (len(c), len(ALL), bad or 'NONE', ferr or 'NONE'))
    for k in bad: print('INFO B2 %s: %s' % (k, ' '.join(c[k][1].split())[:200]))


if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    def cl(k, s, m=''): return {'title': 'gate60 %s x' % k, 'fullName': 'gate60 probe KS-1210 gate60 %s x' % k, 'status': s, 'failureMessages': [m] if m else []}
    R = 'AssertionError: expected 201 to be 400 // Object.is equality'
    def J(o, drop=None):
        cs = [cl(k, o.get(k, 'passed'), o.get(k + 'm', R) if o.get(k) == 'failed' else '') for k in ALL if k != drop]
        return {'testResults': [{'name': 'x', 'status': 'failed' if any(c['status'] == 'failed' for c in cs) else 'passed', 'message': '', 'assertionResults': cs}]}
    DS = {k: 'failed' for k in DEV_RED}
    selftest_arm(st, 'D-0 the expected develop shape (positive control)', lambda C: judge_dev(C, J(DS)), None)
    selftest_arm(st, 'D-1 O1 green at develop (no flip)', lambda C: judge_dev(C, J({k: v for k, v in DS.items() if k != 'O1'})), 'B1')
    selftest_arm(st, 'D-2 V2 (a control) red at develop', lambda C: judge_dev(C, J(dict(DS, V2='failed'))), 'B1')
    selftest_arm(st, 'D-3 a load failure', lambda C: judge_dev(C, {'testResults': [{'name': 'x', 'status': 'failed', 'message': 'Failed to load @secuura/shared', 'assertionResults': []}]}), 'B1')
    selftest_arm(st, 'D-4 P1 red by TIMEOUT', lambda C: judge_dev(C, J(dict(DS, P1m='Error: Test timed out in 5000ms. expected'))), 'B1')
    selftest_arm(st, 'D-5 an unmodelled-SQL failure', lambda C: judge_dev(C, J(dict(DS, O7m='Error: gate60 probe db: unmodelled SQL: SELECT 1'))), 'B0')
    selftest_arm(st, 'D-6 22 cells (R1 missing)', lambda C: judge_dev(C, J(DS, drop='R1')), 'B1')
    selftest_arm(st, 'H-0 23/23 at head (positive control)', lambda C: judge_head(C, J({})), None)
    selftest_arm(st, 'H-1 L1 red at head', lambda C: judge_head(C, J({'L1': 'failed'})), 'B2')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)

if not REPO or not WT or not OUT:
    print(__doc__); raise SystemExit(2)
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
WT = guard_scratch(WT, 'worktree'); OUT = guard_out(OUT)
DIST = os.path.join(WT, K['shared_dist'])
if not (os.path.isfile(DIST) and os.path.getsize(DIST) > 0): print('REFUSING: %s missing or empty (install + build shared first)' % DIST); raise SystemExit(2)
if wgit(WT, 'status', '--porcelain').strip(): print('REFUSING: the worktree is not clean'); raise SystemExit(2)
print('c3b_probe_gate60 %s | worktree %s | develop %s | head %s' % (now(), WT, DEV[:12], HEAD[:12]))
SD = os.path.join(WT, K['suite_dir']); PR = os.path.join(SD, 'src', '__tests__', K['probe_name']); Q = os.path.join(OUT, 'quarantine')
VB = os.path.join(WT, K['install_dir'], 'node_modules', '.bin', 'vitest'); C = Checks(); obs = {}
for name, sha in (('develop', DEV), ('head', HEAD)):
    wgit(WT, 'checkout', '--quiet', '--detach', sha)
    shutil.copyfile(os.path.join(G, K['probe_template']), PR); of = os.path.join(OUT, 'c3b_obs_%s.json' % name); jf = os.path.join(OUT, 'c3b_probe_%s.json' % name)
    landed = os.path.isfile(PR) and open(PR, encoding='utf-8').read() == open(os.path.join(G, K['probe_template']), encoding='utf-8').read()
    C.chk('B-LANDED %s' % name, landed, 'the probe is in place at %s, byte-equal to the kit template: %s' % (sha[:12], landed))
    try:
        rc, o, e = run([VB, 'run', os.path.relpath(PR, SD), '--reporter=json', '--outputFile=' + jf], SD, os.path.join(OUT, 'c3b_probe_' + name), env={'GATE60_OBS_OUT': of})
    finally:
        move_out(PR, Q, '%s.%s.%s' % (K['probe_name'], name, now().replace(':', '')))
    try: j = json.load(open(jf))
    except Exception as ex: j = {'testResults': [{'name': 'NO JSON', 'status': 'failed', 'message': 'Failed to load: %s' % ex, 'assertionResults': []}]}
    (judge_dev if name == 'develop' else judge_head)(C, j)
    obs[name] = open(of).read().strip() if os.path.isfile(of) else 'NOT WRITTEN'
stt = wgit(WT, 'status', '--porcelain').strip()
C.chk('B3 probe moved out', not stt and not os.path.exists(PR), 'git status --porcelain %r | probe still in the worktree: %s | quarantined copies in %s' % (stt[:100], os.path.exists(PR), Q))
wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
for k, v in obs.items(): print('NOTE observations at %s (this host, in-memory table; never asserted): %s' % (k, ' '.join(v.split())[:3000]))
n = C.nfail()
print('C3b PROBE %s: %d FAIL of %d checks | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
