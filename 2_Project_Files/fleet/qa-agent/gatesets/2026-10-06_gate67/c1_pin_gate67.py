#!/usr/bin/env python3
"""c1_pin_gate67.py — C1 PIN for #1394 (KS-723), gate67. READ verbs only (any repo holding the objects; the shared checkout is fine).

  P1 origin: refs/pull/1394/head == branch == the head (ls-remote from the SHARED CHECKOUT's origin, whatever --repo is; skipped with --no-remote, named) and origin develop printed
  P2 ONE parent == the base d784b613c81e; merge-base(head, develop) == d784 (develop named if not in the repo)
  P3 base..head names EXACTLY the 5 kit paths; develop...head (3-dot) the same 5
  P4 tree == END_TREE 644f23f36231 (CONTROL: the base tree differs)
  P5 %(trailers) raw 1 byte (CONTROL bf277eead268 prints 55)        P6 0 Co-Authored-By
  P7 subject == the PR title, <= 92 chars                            P8 one `Refs KS-723` line, only KS-723 hyphenated, 0 closing words
  P9 the 5 paths are mode 100644                                      P10 pre-push / preflight / SKILL.md blobs == kit at head, base, develop
  P11 base..develop touches no kit code path and no hook path (named NOT CHECKED if develop is absent)
Refuses BY NAME (rc 2): `head unresolvable`, `base unresolvable`.
Usage: c1_pin_gate67.py [--repo R] [--head H] [--develop D] [--no-remote] | --selftest     rc 0 PASS / 1 FAIL / 2 refused"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate67 import K, git, Tally, resolvable


def run(repo, head, develop, remote, t):
    base = K['base']
    for n, s in (('head', head), ('base', base)):
        if not resolvable(repo, s): print('C1 REFUSED: %s unresolvable: %s not in %s' % (n, s, repo)); return 'UNRESOLVABLE'
    head = git(repo, 'rev-parse', head + '^{commit}').strip()
    if remote:
        ls = git(K['checkout'], 'ls-remote', 'origin', 'refs/heads/develop', 'refs/heads/' + K['branch'], 'refs/pull/%s/head' % K['pr'])
        m = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
        ph, bh, od = m.get('refs/pull/%s/head' % K['pr']), m.get('refs/heads/' + K['branch']), m.get('refs/heads/develop')
        t.check('P1', ph == head and bh == head, 'origin pull/head %s branch %s == head %s; origin develop %s' % (str(ph)[:12], str(bh)[:12], head[:12], od))
    else:
        t.info('P1', 'NOT CHECKED here (--no-remote): origin was read by the caller')
    dev_ok = bool(develop) and resolvable(repo, develop)
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    mb = git(repo, 'merge-base', head, develop).strip() if dev_ok else None
    t.check('P2', par == [base] and (mb == base or not dev_ok), 'parents %s (want [%s]); merge-base(head, develop) %s%s' % (
        [p[:12] for p in par], base[:12], str(mb)[:12], '' if dev_ok else ' — develop %s NOT in %s, named' % (develop, repo)))
    two = sorted(git(repo, 'diff', '--name-only', base, head).splitlines())
    three = sorted(git(repo, 'diff', '--name-only', '%s...%s' % (develop, head)).splitlines()) if dev_ok else None
    t.check('P3', two == sorted(K['files']) and (three is None or three == two), 'base..head %d path(s) == kit 5: %s; develop...head %s' % (len(two), two == sorted(K['files']), 'same' if three == two else three))
    tr = git(repo, 'rev-parse', head + '^{tree}').strip(); btr = git(repo, 'rev-parse', base + '^{tree}').strip()
    t.check('P4', tr == K['end_tree'] and btr != K['end_tree'], 'tree %s == END_TREE %s; CONTROL base tree %s differs' % (tr[:12], K['end_tree'][:12], btr[:12]))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', head).encode())
    rc, o, e = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'], check=False)
    ctl = len(o.encode()) if rc == 0 else None
    t.check('P5', tb == 1 and ctl not in (None, 1), '%%(trailers) raw %d byte(s); CONTROL %s prints %s' % (tb, K['trailer_control'], ctl))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    t.check('P6', not re.search(r'(?im)^co-authored-by:', msg), 'Co-Authored-By lines %d' % len(re.findall(r'(?im)^co-authored-by:', msg)))
    subj = msg.split('\n', 1)[0]
    t.check('P7', subj == K['pr_title'] and len(subj) <= 92, 'subject == PR title %s, %d chars' % (subj == K['pr_title'], len(subj)))
    refs = re.findall(r'(?m)^Refs KS-723$', msg); keys = set(re.findall(r'\bKS-\d+\b', msg))
    closing = re.findall(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+(#\d+|KS-\d+)', msg, re.I)
    t.check('P8', len(refs) == 1 and keys == {'KS-723'} and not closing, 'Refs KS-723 lines %d; hyphenated keys %s; closing %s' % (len(refs), sorted(keys), closing))
    modes = {p: (git(repo, 'ls-tree', head, '--', p).split() or ['ABSENT'])[0] for p in K['files']}
    t.check('P9', set(modes.values()) == {'100644'}, 'modes %s' % sorted(set(modes.values())))
    revs = [('head', head), ('base', base)] + ([('develop', develop)] if dev_ok else [])
    bad = ['%s@%s' % (p, n) for n, r in revs for p, b in list(K['hook_blobs'].items()) + [(K['skill'], K['skill_blob'])]
           if git(repo, 'rev-parse', '%s:%s' % (r, p)).strip() != b]
    t.check('P10', not bad, 'pre-push / preflight / SKILL.md at %s == kit: %s' % ([n for n, _ in revs], bad or 'all'))
    if dev_ok:
        adv = git(repo, 'diff', '--name-only', base, develop).splitlines()
        hit = sorted(set(adv) & (set(K['code_paths']) | set(K['hook_blobs'])))
        t.check('P11', not hit, 'base..develop %d path(s); kit code / hook paths among them %s' % (len(adv), hit or 'none'))
    else:
        t.info('P11', 'NOT CHECKED: develop %s not in %s' % (develop, repo))
    return 'DONE'


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    repo = opt('--repo', K['checkout'])
    if '--selftest' in A:
        import io, contextlib
        res = []
        def rep(c, m): res.append(c); print('%s %s' % ('PASS' if c else 'FAIL', m))
        t = Tally(); b = io.StringIO()
        with contextlib.redirect_stdout(b): run(repo, K['head'], K['develop_at_draft'], False, t)
        rep(not t.fails and t.n == 10, 'POSITIVE: the head passes P2-P11 (%d checked, fails %s)' % (t.n, t.fails))
        t = Tally()
        with contextlib.redirect_stdout(b): run(repo, K['base'], K['develop_at_draft'], False, t)
        rep({'P2', 'P3', 'P4', 'P7'} <= set(t.fails), 'CONTROL: the base as head FAILS P2 P3 P4 P7 (got %s)' % t.fails)
        t = Tally(); b = io.StringIO()
        with contextlib.redirect_stdout(b): r = run(repo, 'f' * 40, K['develop_at_draft'], False, t)
        rep(r == 'UNRESOLVABLE' and 'head unresolvable' in b.getvalue(), 'absent head refuses BY NAME: %r' % b.getvalue().strip()[:90])
        print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1
    t = Tally()
    r = run(repo, opt('--head', K['head']), opt('--develop', K['develop_at_draft']), '--no-remote' not in A, t)
    if r == 'UNRESOLVABLE': return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
