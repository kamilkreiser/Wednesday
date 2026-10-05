#!/usr/bin/env python3
"""c1_pin_gate57.py — gate57 C1: pin ONE of the two PRs from TWO instruments and the commit from YOUR clone (run it once per PR).
  P1 ls-remote origin (from --repo): refs/pull/<n>/head == HEAD == the PR's branch ref (WHOLE-FIELD); develop at origin read.
  P2 the GitHub PULLS API (read-only GET; GH_TOKEN read BY NAME, never printed): open, not merged, base.ref develop, head.sha == HEAD,
     head.ref matches the PR's branch_rx (its OWN key and -b60-<k>), mergeable printed.
  P3 SHAPE: HEAD has exactly ONE parent == kit cut_base (3ce8cd4026a6); develop at origin == cut_base, or an ADVANCE whose every changed
     path is disjoint from kit all_paths (printed by path; any overlap FAILS: a re-draft).
  P3b TREES: HEAD^{tree} == the READY's head tree (kit prs.<k>.ready_head_tree) when HEAD == the READY head; cut_base^{tree} printed as the
     control that differs. END_TREE: PR 1 == its head tree (merges clean, no merge-in); PR 2's END_TREE is the PREDICTED T2 — C4b's job.
  P4 FILES: `git diff --numstat <cut_base> HEAD` == EXACTLY the kit file set with the kit +/- per path, both ways (missing / extra / wrong
     count each named); the API /files list == the same (skipped with --local-only, said so).
  P5 NO TRAILER: `%(trailers)` empty and 0 Co-Authored-By on HEAD; CONTROL kit trailer_control_commit prints one.
  P6 SUBJECT: HEAD's subject byte-equal to kit prs.<k>.subject, its length == the READY's figure, no `(#` (the GO composes the squash
     subject; GitHub appends ` (#n)` when it lands: the landed length is printed against MG-11's 92).
--local-only: P3-P6 only (no network; P1 / P2 / P4-API are NOT RUN and say so).   --selftest: plants in YOUR scratch clone (it writes SIM
commits there with commit-tree, never a ref): every arm must land on its named check. --selftest needs --repo only.
Usage: c1_pin_gate57.py --repo <your clone> --pr <1380|1381> --head <40-hex> [--local-only]   |   c1_pin_gate57.py --repo <clone> --selftest
rc 0 PASS / 1 FAIL / 2 usage / 3 API"""
import io, contextlib, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, wgit, now, Checks, GH, opt_factory, pr_cfg, has_commit, guard_scratch

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or not ('--selftest' in A or all(x in A for x in ('--pr', '--head'))):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
REPO = opt('--repo'); CUT = K['cut_base']


def trailers(sha):
    t = git(REPO, 'log', '-1', '--format=%(trailers)', sha).strip(); m = git(REPO, 'log', '-1', '--format=%B', sha)
    return t, len(re.findall(r'(?im)^co-authored-by:', m))


def local(C, key, P, HEAD, dev):
    if not has_commit(REPO, HEAD):
        for t in ('P3 shape', 'P3b trees', 'P4 files (clone)', 'P5 no trailer', 'P6 subject'):
            C.chk(t, False, 'HEAD %s is not in the clone — fetch refs/pull/%s/head into YOUR clone first' % (HEAD[:12], P['number']))
        return
    parents = git(REPO, 'log', '-1', '--format=%P', HEAD).split()
    adv = ''
    if dev and dev != CUT:
        if has_commit(REPO, dev):
            moved = sorted(set(git(REPO, 'diff', '--name-only', CUT, dev).splitlines()))
            hit = sorted(set(moved) & set(K['all_paths']) | set(p for p in moved if p.startswith('Projects Documents/')))
            adv = ' | develop ADVANCED %s -> %s: %d path(s) moved, overlapping kit paths %s' % (CUT[:12], dev[:12], len(moved), hit or 'NONE')
            dev_ok = not hit and git(REPO, 'merge-base', '--is-ancestor', CUT, dev, check=False)[0] == 0
        else:
            dev_ok = False; adv = ' | develop %s NOT in the clone: fetch it' % dev[:12]
    else:
        dev_ok = True
    C.chk('P3 shape', parents == [CUT] and dev_ok, 'parents %s (want exactly [cut_base %s]) | develop at origin %s%s' % (
        [x[:12] for x in parents], CUT[:12], (dev or 'NOT READ (--local-only)')[:12], adv))
    ht = git(REPO, 'rev-parse', HEAD + '^{tree}').strip(); bt = git(REPO, 'rev-parse', CUT + '^{tree}').strip()
    claim = P['ready_head_tree'] if HEAD == P['ready_head'] else None
    C.chk('P3b trees', ht != bt and (claim is None or ht == claim), 'HEAD^{tree} %s | cut_base^{tree} %s (control, differs: %s) | READY head tree %s%s | END_TREE %s' % (
        ht, bt, ht != bt, claim or '(HEAD is not the READY head)', '' if claim is None else ' == measured: %s' % (ht == claim),
        (('== the head tree (PR 1 merges clean)' if not dev or dev == CUT else 'NOT the head tree: develop advanced, C4b X1 prints the landed tree') if key == 'pr1'
         else 'PREDICTED %s at cut_base (C4b re-derives it%s)' % (P['ready_end_tree'], '' if not dev or dev == CUT else '; STALE at the advanced develop'))))
    ns = {}
    for l in git(REPO, 'diff', '--numstat', CUT, HEAD).splitlines():
        a, d, p = l.split('\t', 2); ns[p] = [int(a), int(d)]
    want = {p: list(v) for p, v in P['files'].items()}
    if os.environ.get('G57_FILES_DROP'):
        want.pop(os.environ['G57_FILES_DROP'], None); print('CONTROL OVERRIDE G57_FILES_DROP: P4 MUST FAIL')
    miss = sorted(set(want) - set(ns)); extra = sorted(set(ns) - set(want)); wrong = sorted(p for p in set(ns) & set(want) if ns[p] != want[p])
    C.chk('P4 files (clone)', not miss and not extra and not wrong, '%d path(s) | MISSING %s | EXTRA %s | WRONG +/- %s' % (
        len(ns), miss or 'NONE', extra or 'NONE', ['%s %s want %s' % (p, ns[p], want[p]) for p in wrong] or 'NONE'))
    for p in sorted(ns):
        print('INFO P4 %s +%d/-%d' % (p, ns[p][0], ns[p][1]))
    ct, cn = trailers(K['trailer_control_commit']); t, n = trailers(HEAD)
    C.chk('P5 no trailer', t == '' and n == 0 and cn >= 1, 'HEAD trailers %r (%d Co-Authored-By) | CONTROL %s prints %r (%d)' % (t, n, K['trailer_control_commit'], ct[:60], cn))
    subj = git(REPO, 'log', '-1', '--format=%s', HEAD).rstrip('\n'); landed = len(subj) + len(' (#%s)' % P['number'])
    C.chk('P6 subject', subj == P['subject'] and len(subj) == P['subject_len_ready'] and '(#' not in subj and landed <= 92,
          'subject %r (%d chars; READY says %d; kit byte-equal %s) | contains "(#" %s | lands as %d chars with " (#%s)" (MG-11 <= 92)' % (
              subj, len(subj), P['subject_len_ready'], subj == P['subject'], '(#' in subj, landed, P['number']))


def api(C, key, P, HEAD, gh):
    p = gh.get('pulls/' + P['number']); tries = 1
    while p.get('mergeable') is None and tries < 3:
        time.sleep(10); p = gh.get('pulls/' + P['number']); tries += 1
    br = p['head']['ref']
    rc, ls, err = git(REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % P['number'], 'refs/heads/' + br, check=False)
    R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
    dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % P['number']); bh = R.get('refs/heads/' + br)
    C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None, 'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s' % (
        rc, P['number'], ph, br, bh, dev, HEAD))
    brok = re.match(P['branch_rx'], br) is not None
    C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['head']['sha'] == HEAD and brok,
          'state %s | merged %s | base %s @ %s | head.sha %s | branch %s matches %s: %s | mergeable %s (%d read(s)) / %s | title %r' % (
              p['state'], p.get('merged'), p['base']['ref'], p['base']['sha'][:12], p['head']['sha'], br, P['branch_rx'], brok,
              p.get('mergeable'), tries, p.get('mergeable_state'), p.get('title')))
    fl = gh.pages('pulls/%s/files' % P['number'])
    apis = {f['filename']: [f['additions'], f['deletions']] for f in fl}
    want = {q: list(v) for q, v in P['files'].items()}
    C.chk('P4 files (API)', apis == want, 'API %d path(s) == kit set with +/- per path: %s | MISSING %s | EXTRA %s' % (
        len(apis), apis == want, sorted(set(want) - set(apis)) or 'NONE', sorted(set(apis) - set(want)) or 'NONE'))
    return dev


def judge(key, HEAD, dev=None, gh=None, quiet=False):
    P = K['prs'][key]; C = Checks(quiet=quiet)
    if gh is not None:
        dev = api(C, key, P, HEAD, gh)
    else:
        print('NOT RUN P1 / P2 / P4 (API): --local-only (no network) — the gate MUST run without it')
    local(C, key, P, HEAD, dev)
    return C


if '--selftest' in A:
    guard_scratch(REPO, 'self-test clone')
    H1, H2 = K['prs']['pr1']['ready_head'], K['prs']['pr2']['ready_head']
    for h in (H1, H2, CUT):
        if not has_commit(REPO, h): print('REFUSING: %s not in %s — fetch both PR heads and develop first' % (h[:12], REPO)); raise SystemExit(2)
    env = {'GIT_AUTHOR_NAME': 'g57', 'GIT_AUTHOR_EMAIL': 'g57@sim', 'GIT_COMMITTER_NAME': 'g57', 'GIT_COMMITTER_EMAIL': 'g57@sim',
           'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}
    def sim(tree, parent, msg):
        return wgit(REPO, 'commit-tree', tree, '-p', parent, '-m', msg, env=env).strip()
    t1 = git(REPO, 'rev-parse', H1 + '^{tree}').strip(); s1 = K['prs']['pr1']['subject']
    arms = [
        ('T0 PR 1 at its READY head', 'pr1', H1, None, None),
        ('T1 PR 2 at its READY head', 'pr2', H2, None, None),
        ('T2 PR 1 judged as PR 2 (wrong file set + subject)', 'pr2', H1, None, 'P4'),
        ('T3 a trailer on the commit (Co-Authored-By)', 'pr1', sim(t1, CUT, s1 + '\n\nCo-Authored-By: Sim <sim@x>'), None, 'P5'),
        ('T4 subject carries " (#1380)"', 'pr1', sim(t1, CUT, s1 + ' (#1380)'), None, 'P6'),
        ('T5 parent is not cut_base (stacked on PR 2)', 'pr1', sim(t1, H2, s1), None, 'P3'),
        ('T6 develop advanced by a commit touching a kit doc', 'pr1', H1, H2, 'P3'),
        ('T7 develop advanced by a disjoint commit (allowed)', 'pr1', H1, sim(git(REPO, 'rev-parse', CUT + '^{tree}').strip(), CUT, 'SIM disjoint advance (empty)'), None),
        ('T8 one-character subject change', 'pr1', sim(t1, CUT, s1.replace('number', 'numbr')), None, 'P6'),
    ]
    ok = 0
    for name, key, h, dev, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = judge(key, h, dev=dev)
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        for l in buf.getvalue().splitlines():
            if l.startswith('FAIL') or not good: print('    ' + l[:240])
    os.environ['G57_FILES_DROP'] = list(K['prs']['pr1']['files'])[0]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): C = judge('pr1', H1)
    del os.environ['G57_FILES_DROP']
    good = 'P4 files (clone)' in C.failed(); ok += good; print('SELFTEST %s T9 G57_FILES_DROP (a planted wrong expectation): want FAIL on P4 | failed %s' % ('OK' if good else 'MISS', C.failed() or 'NONE'))
    n = len(arms) + 1
    print('SELFTEST %s %d of %d (local checks P3-P6; P1 / P2 / P4-API need the network and are exercised only by a real run)' % ('OK' if ok == n else 'BROKEN', ok, n))
    raise SystemExit(0 if ok == n else 1)

key, P = pr_cfg(opt('--pr')); HEAD = opt('--head')
if not re.fullmatch(r'[0-9a-f]{40}', HEAD or ''):
    print('REFUSING: --head must be 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
print('c1_pin_gate57 %s | repo %s | %s #%s %s %s | HEAD %s' % (now(), REPO, key, P['number'], P['ticket'], P['tier'], HEAD))
C = judge(key, HEAD, gh=None if '--local-only' in A else GH())
n = C.nfail()
print('PIN %s: %d FAIL of %d checks | #%s | HEAD %s%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), P['number'], HEAD[:12], ' | LOCAL ONLY: P1 / P2 / P4-API NOT RUN' if '--local-only' in A else ''))
raise SystemExit(1 if n else 0)
