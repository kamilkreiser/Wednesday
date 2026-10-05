#!/usr/bin/env python3
"""c1_pin_gate68.py — C1 PIN for #1393 ROUND 2 (KS-1278), gate68. READ verbs only. THE HEAD IS A PARAMETER (--head or env G68_HEAD;
default the kit's STAND-IN 97ce2f337ae6, used only for the kit's own dry run / self-test).

  P1  origin: refs/pull/1393/head == branch == --head (ls-remote from the SHARED CHECKOUT's origin; --no-remote skips it, named)
  P2  the chain: head == 97ce2f (stand-in) with ONE parent 4a1620588819, OR head has ONE parent 97ce2f337ae6 (Wednesday's ONE released
      follow-up); 97ce2f^ == 4a16; 4a16^ == 32e058975d4e; merge-base(head, develop) == 32e058975d4e
  P3  32e0..head names EXACTLY the 6 kit paths (two-dot == three-dot vs develop); 4a16..head subset of the 4 round-2 paths
  P3b (follow-up only) 97ce2f..head names only the released paths (test, cheat, flow): a product path there = FAIL (re-read the product)
  P4  tree recorded; == the stand-in tree when head is the stand-in; != round 1's tree (CONTROL)
  P5  every commit in 4a16..head: %(trailers) CONTENT 0 / RAW 1 byte; CONTROL bf277eead268 CONTENT 53 / RAW 55 (both instruments)
  P6  0 Co-Authored-By in every commit of 4a16..head
  P7  97ce2f's subject == the kit's round-2 subject, <= 92; every commit subject <= 92 and carries KS-1278
  P8  every commit: only KS-1278 hyphenated, 0 closing references (close/fix/resolve + #n|KS-n); 97ce2f carries ONE `Refs KS-1278`
  P9  the 6 paths are mode 100644 at head
  P10 pre-push / preflight / SKILL.md blobs == kit at head, 32e0, develop
  P11 32e0..develop touches no kit code path and no hook path
Refuses BY NAME (rc 2): `head unresolvable`, `round-1 head unresolvable`, `branch base unresolvable`.
Usage: c1_pin_gate68.py [--repo R] [--head H] [--develop D] [--no-remote] | --selftest [--repo R]     rc 0 PASS / 1 FAIL / 2 refused"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate68 import K, git, Tally, resolvable

CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+(#\d+|KS-\d+)', re.I)


def tr_bytes(repo, c):
    raw = git(repo, 'log', '-1', '--format=%(trailers)', c)
    return len(raw.rstrip('\n').encode()), len(raw.encode())


def run(repo, head, develop, remote, t):
    r1, bb, st = K['round1_head'], K['branch_base'], K['head_standin']
    for n, s in (('head', head), ('round-1 head', r1), ('branch base', bb)):
        if not resolvable(repo, s): print('C1 REFUSED: %s unresolvable: %s not in %s' % (n, s, repo)); return 'UNRESOLVABLE'
    head = git(repo, 'rev-parse', head + '^{commit}').strip()
    if remote:
        ls = git(K['checkout'], 'ls-remote', 'origin', 'refs/heads/develop', 'refs/heads/' + K['branch'], 'refs/pull/%s/head' % K['pr'])
        m = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
        ph, bh, od = m.get('refs/pull/%s/head' % K['pr']), m.get('refs/heads/' + K['branch']), m.get('refs/heads/develop')
        t.check('P1', ph == head and bh == head, 'origin pull/head %s branch %s == --head %s; origin develop %s' % (str(ph)[:12], str(bh)[:12], head[:12], od))
    else:
        t.info('P1', 'NOT CHECKED here (--no-remote): origin was read by the caller')
    dev_ok = bool(develop) and resolvable(repo, develop)
    par = lambda c: git(repo, 'log', '-1', '--format=%P', c).split()
    is_st = head == st
    chain = (par(head) == [r1]) if is_st else (par(head) == [st] and resolvable(repo, st) and par(st) == [r1])
    mb = git(repo, 'merge-base', head, develop).strip() if dev_ok else None
    t.check('P2', chain and par(r1) == [bb] and (mb == bb or not dev_ok),
            '%s; head parents %s; 97ce2f^ %s; 4a16^ %s (want %s); merge-base(head, develop) %s%s' % (
                'head IS the stand-in 97ce2f' if is_st else 'head is a FOLLOW-UP (want ONE parent 97ce2f)', [p[:12] for p in par(head)],
                [p[:12] for p in par(st)] if resolvable(repo, st) else 'ABSENT', [p[:12] for p in par(r1)], bb[:12], str(mb)[:12],
                '' if dev_ok else ' — develop %s NOT in %s, named' % (develop, repo)))
    two = sorted(git(repo, 'diff', '--name-only', bb, head).splitlines())
    three = sorted(git(repo, 'diff', '--name-only', '%s...%s' % (develop, head)).splitlines()) if dev_ok else None
    r2 = sorted(git(repo, 'diff', '--name-only', r1, head).splitlines())
    t.check('P3', two == sorted(K['files']) and (three is None or three == two) and set(r2) <= set(K['r2_files_vs_round1']) and r2,
            '32e0..head %d path(s) == kit 6: %s; develop...head %s; 4a16..head %d path(s) %s subset of the 4 round-2 paths' % (
                len(two), two == sorted(K['files']), 'same' if three == two else three, len(r2), [os.path.basename(x)[:40] for x in r2]))
    if not is_st:
        fu = sorted(git(repo, 'diff', '--name-only', st, head).splitlines())
        bad = [p for p in fu if p not in K['followup_expected_paths']]
        t.check('P3b', fu and not bad, '97ce2f..head %d path(s) %s; OUTSIDE the released follow-up (product?) %s' % (
            len(fu), [os.path.basename(x)[:40] for x in fu], bad or 'none'))
    tr = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tr != K['round1_tree'] and (not is_st or tr == K['head_standin_tree']), 'tree %s%s; CONTROL round-1 tree %s differs' % (
        tr, ' == stand-in tree' if is_st and tr == K['head_standin_tree'] else '', K['round1_tree'][:12]))
    commits = git(repo, 'rev-list', '--reverse', '%s..%s' % (r1, head)).split()
    trs = {c[:12]: tr_bytes(repo, c) for c in commits}
    rc, o, e = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'], check=False)
    ctl = (len(o.rstrip('\n').encode()), len(o.encode())) if rc == 0 else None
    t.check('P5', commits and all(v == (0, 1) for v in trs.values()) and ctl == (K['trailer_control_content_bytes'], K['trailer_control_raw_bytes']),
            '%%(trailers) (content, raw) per commit %s (want (0, 1)); CONTROL %s = %s (want (53, 55))' % (trs, K['trailer_control'], ctl))
    msgs = {c: git(repo, 'log', '-1', '--format=%B', c) for c in commits}
    co = {c[:12]: len(re.findall(r'(?im)^co-authored-by:', m)) for c, m in msgs.items()}
    t.check('P6', bool(commits) and not any(co.values()), 'Co-Authored-By per commit %s%s' % (co, '' if commits else ' — 0 COMMITS in 4a16..head: vacuous, FAIL'))
    subj = {c[:12]: m.split('\n', 1)[0] for c, m in msgs.items()}
    s97 = git(repo, 'log', '-1', '--format=%s', st).rstrip('\n') if resolvable(repo, st) else None
    t.check('P7', bool(commits) and s97 == K['subject_r2'] and len(s97) <= 92 and all(len(s) <= 92 and 'KS-1278' in s for s in subj.values()),
            '97ce2f subject == kit %s (%s chars); every subject <= 92 with KS-1278: %s' % (s97 == K['subject_r2'], len(s97 or ''), {k: len(v) for k, v in subj.items()}))
    keys = {c[:12]: sorted(set(re.findall(r'\bKS-\d+\b', m))) for c, m in msgs.items()}
    clo = {c[:12]: CLOSING.findall(m) for c, m in msgs.items()}
    refs97 = len(re.findall(r'(?m)^Refs KS-1278$', msgs.get(st, git(repo, 'log', '-1', '--format=%B', st))))
    t.check('P8', bool(commits) and all(v == ['KS-1278'] for v in keys.values()) and not any(clo.values()) and refs97 == 1,
            'hyphenated keys per commit %s; closing refs %s; 97ce2f `Refs KS-1278` lines %d' % (keys, {k: v for k, v in clo.items() if v} or 'none', refs97))
    modes = {p: (git(repo, 'ls-tree', head, '--', p).split() or ['ABSENT'])[0] for p in K['files']}
    t.check('P9', set(modes.values()) == {'100644'}, 'modes %s' % sorted(set(modes.values())))
    revs = [('head', head), ('branch base', bb)] + ([('develop', develop)] if dev_ok else [])
    bad = ['%s@%s' % (p, n) for n, r in revs for p, b in list(K['hook_blobs'].items()) + [(K['skill'], K['skill_blob'])]
           if git(repo, 'rev-parse', '%s:%s' % (r, p)).strip() != b]
    t.check('P10', not bad, 'pre-push / preflight / SKILL.md at %s == kit: %s' % ([n for n, _ in revs], bad or 'all'))
    if dev_ok:
        adv = git(repo, 'diff', '--name-only', bb, develop).splitlines()
        hit = sorted(set(adv) & (set(K['code_paths']) | set(K['hook_blobs'])))
        t.check('P11', not hit, '32e0..develop %d path(s); kit code / hook paths among them %s' % (len(adv), hit or 'none'))
    else:
        t.info('P11', 'NOT CHECKED: develop %s not in %s' % (develop, repo))
    print('INFO commits 4a16..head: %s | head %s tree %s' % ([c[:12] for c in commits], head, tr))
    return 'DONE'


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    repo = opt('--repo', K['checkout'])
    head = opt('--head', os.environ.get('G68_HEAD', K['head_expected']))
    if '--selftest' in A:
        import io, contextlib
        res = []
        def rep(c, m): res.append(c); print('%s %s' % ('PASS' if c else 'FAIL', m))
        b = io.StringIO()
        t = Tally()
        with contextlib.redirect_stdout(b): run(repo, K['head_standin'], K['develop_at_draft'], False, t)
        rep(not t.fails and t.n == 10, 'POSITIVE: the stand-in head passes P2-P11 (%d checked, fails %s)' % (t.n, t.fails))
        t = Tally()
        with contextlib.redirect_stdout(b): run(repo, K['round1_head'], K['develop_at_draft'], False, t)
        rep({'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'} <= set(t.fails), 'PLANTED: round-1 head 4a16 as --head FAILS P2 P3 P4 P5 P6 P7 P8 (0 commits is never a vacuous pass) (got %s)' % t.fails)
        t = Tally()
        with contextlib.redirect_stdout(b): run(repo, K['branch_base'], K['develop_at_draft'], False, t)
        rep({'P2', 'P3', 'P5'} <= set(t.fails), 'PLANTED: the branch base 32e0 as --head FAILS P2 P3 P5 (got %s)' % t.fails)
        t = Tally(); b = io.StringIO()
        with contextlib.redirect_stdout(b): r = run(repo, 'f' * 40, K['develop_at_draft'], False, t)
        rep(r == 'UNRESOLVABLE' and 'head unresolvable' in b.getvalue(), 'absent head refuses BY NAME: %r' % b.getvalue().strip()[:90])
        print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1
    t = Tally()
    r = run(repo, head, opt('--develop', K['develop_at_draft']), '--no-remote' not in A, t)
    if r == 'UNRESOLVABLE': return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
