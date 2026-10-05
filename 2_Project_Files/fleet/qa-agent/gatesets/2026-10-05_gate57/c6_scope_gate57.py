#!/usr/bin/env python3
"""c6_scope_gate57.py — gate57 C6: scope, keys and NOT COVERED, per PR, from the PR body (PULLS API, or --body-file the launch action
saved), the title, the branch and the commit message in YOUR clone. Read-only.
  K1 OWN KEY ONLY, HYPHENATED: the hyphenated `KS-<n>` keys in the body, the title and the full commit message == {its own key} (a
     hyphenated foreign key ATTACHES on the board); every foreign key appears de-hyphenated ("KS 1015"). The branch carries its own key.
  K2 NON-CLOSING: `Refs KS-<own>` on its own line, the Linear URL https://linear.app/secuura/issue/KS-<own> present; 0 closing keywords
     (close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved) before any key or #n — so the merge moves no ticket.
  K3 NO CROSS-REPO REFS: 0 `owner/repo#n`, 0 github.com/<org> URLs other than Secuura's own.
  K4 NOT COVERED BY NAME: the body names every kit not_covered_body_rx — both PRs: the §5f live sweep ("live sweep", "5f"); #1381 also the
     DELIVERIES half of KS-1345 (`webhooks.ts:412`).
  K5 THE BODY THE READY DECLARED: sha256(body) prefix == the READY's (kit prs.<k>.ready_body_sha256_prefix).
  K6 CLAIMS IN WORDS: #1380 states its two edits OUTSIDE its own block (the KS 1404 cell count 36, the KS 1015 closing sentence with 28 /
     26); #1381 states the behaviour change (constant 500, the non-UUID userId / 22P02 case, which principals carry one UNMEASURED).
  K7 TIER CONSISTENCY: product (non-test, non-doc) paths in the diff: #1380 0 (T2, test-only), #1381 >= 1 (T1, a behaviour change).
--selftest: planted bodies (a second hyphenated key, "Closes KS-1333", an owner/repo#n ref, the deliveries half dropped, the live sweep
dropped, one byte changed) each FAIL their named check; the real bodies PASS.
Usage: c6_scope_gate57.py --repo <clone> --pr <1380|1381> [--head sha] [--body-file f | --offline-dir d] [--selftest]   rc 0 / 1 / 2 / 3"""
import os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, now, Checks, opt_factory, GH, pr_cfg, has_commit, sha256

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--pr' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); key, P = pr_cfg(opt('--pr')); HEAD = opt('--head', P['ready_head']); CUT = K['cut_base']
OWN = P['ticket']
if not has_commit(REPO, HEAD): print('REFUSING: %s not in %s' % (HEAD[:12], REPO)); raise SystemExit(2)
G_ = os.path.dirname(os.path.abspath(__file__))
CLOSE = re.compile(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[:\s]+(KS-\d+|#\d+)')


def hy(t): return sorted(set(re.findall(r'\bKS-\d+\b', t or '')))


def analyse(body, title, branch, msg, files):
    C = Checks()
    kb, kt, km = hy(body), hy(title), hy(msg)
    dehy = sorted(set(re.findall(r'\bKS (\d+)\b', body)))
    C.chk('K1 own key only', kb == [OWN] and kt == [OWN] and km == [OWN] and OWN.lower() in branch.lower(),
          'hyphenated keys: body %s | title %s | commit message %s (want exactly [%s]) | de-hyphenated foreign keys in the body %s | branch %s carries %s: %s' % (
              kb, kt, km, OWN, ['KS ' + x for x in dehy], branch, OWN.lower(), OWN.lower() in branch.lower()))
    refs = re.search(r'(?m)^\W*Refs %s\W*$' % re.escape(OWN), body) is not None; url = ('https://linear.app/secuura/issue/%s' % OWN) in body
    cl = [m.group(0) for m in CLOSE.finditer(body + '\n' + msg + '\n' + title)]
    C.chk('K2 non-closing', refs and url and not cl, '`Refs %s` on its own line %s | Linear URL %s | closing keywords %s' % (OWN, refs, url, cl or 'NONE'))
    xr = re.findall(r'\b[\w.-]+/[\w.-]+#\d+\b', body); gh = [u for u in re.findall(r'github\.com/([\w.-]+)', body) if u.lower() != 'secuura']
    C.chk('K3 no cross-repo refs', not xr and not gh, 'owner/repo#n %s | github.com/<org> other than Secuura %s' % (xr or 'NONE', gh or 'NONE'))
    nr = re.split(r'(?im)^\*\*NOT run\*\*\s*$', body); sect = nr[1].split('**Migrations')[0] if len(nr) > 1 else ''
    miss = [rx for rx in P['not_covered_body_rx'] if not re.search(rx, sect)]
    C.chk('K4 NOT COVERED by name', bool(sect) and not miss, 'NOT run section %d chars | required %s | missing %s' % (len(sect), P['not_covered_body_rx'], miss or 'NONE'))
    hs = sha256(body)[:16]
    C.chk('K5 the declared body', hs == P['ready_body_sha256_prefix'], 'sha256(body) %s | READY %s' % (hs, P['ready_body_sha256_prefix']))
    if key == 'pr1':
        need = [r'KS 1404', r'\b36\b', r'\b27\b', r'KS 1015', r'\b28\b', r'\b26 remain']
    else:
        need = [r'(?i)constant 500', r'(?i)non-UUID', r'22P02', r'(?i)UNMEASURED']
    gone = [r for r in need if not re.search(r, body)]
    C.chk('K6 claims in words', not gone, 'required statements %s | missing %s' % (need, gone or 'NONE'))
    prod = [f for f in files if not re.search(K['test_path_rx'], f) and f not in K['docs']]
    C.chk('K7 tier consistency', (P['tier'] == 'T2' and not prod) or (P['tier'] == 'T1' and prod), 'tier %s | product paths %s' % (P['tier'], prod or 'NONE'))
    return C


title = git(REPO, 'log', '-1', '--format=%s', HEAD).strip(); msg = git(REPO, 'log', '-1', '--format=%B', HEAD)
files = git(REPO, 'diff', '--name-only', CUT, HEAD).splitlines()
if opt('--body-file'):
    body = open(opt('--body-file'), encoding='utf-8').read(); branch = opt('--branch', 'feature/%s-unknown-b60' % OWN.lower()); src = opt('--body-file')
elif '--selftest' in A:
    body = open(os.path.join(G_, 'sim', 'body_pr%s_drafting.md' % P['number']), encoding='utf-8').read(); branch = 'feature/%s-sim-b60-%s' % (OWN.lower(), key[-1]); src = 'sim/body_pr%s_drafting.md (read 2026-10-05 by the drafter)' % P['number']
else:
    p = GH(opt('--offline-dir')).get('pulls/' + P['number']); body = p.get('body') or ''; branch = p['head']['ref']; title = p['title']; src = 'PULLS API'
print('c6_scope_gate57 %s | %s #%s %s | head %s | body from %s' % (now(), key, P['number'], OWN, HEAD[:12], src))
if '--selftest' in A:
    other = 'KS-1345' if key == 'pr1' else 'KS-1333'
    arms = [('T0 the real body', body, None),
            ('T1 a second hyphenated key', body + '\nSee also %s.\n' % other, 'K1'),
            ('T2 "Closes %s"' % OWN, body.replace('**Refs %s**' % OWN, '**Closes %s**' % OWN), 'K2'),
            ('T3 an owner/repo#n reference', body + '\nCompare Secuura/other-repo#12.\n', 'K3'),
            ('T4 the live sweep dropped from NOT run', re.sub(r'(?i)live sweep', 'sweep', body), 'K4'),
            ('T5 one byte changed', body.replace(' ', '  ', 1), 'K5')]
    if key == 'pr2':
        arms.append(('T6 the deliveries half dropped', body.replace('webhooks.ts:412', 'webhooks.ts').replace('deliveries half', 'other half'), 'K4'))
        arms.append(('T7 the 22P02 case dropped', body.replace('22P02', 'an error'), 'K6'))
    else:
        arms.append(('T6 the KS 1015 edit not stated', body.replace('KS 1015', 'delegation'), 'K6'))
    ok = 0
    for name, b, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(b, title, branch, msg, files)
        f = C.failed(); g = (not f) if want is None else any(x.startswith(want) for x in f); ok += g
        print('SELFTEST %s %s: want %s | failed %s' % ('OK' if g else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        if not g: print(buf.getvalue()[:1200])
    print('SELFTEST %s %d of %d (%s #%s)' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms), key, P['number'])); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(body, title, branch, msg, files); n = C.nfail()
print('C6 SCOPE %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), P['number']))
raise SystemExit(1 if n else 0)
