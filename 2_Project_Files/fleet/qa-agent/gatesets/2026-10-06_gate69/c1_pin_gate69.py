#!/usr/bin/env python3
"""c1_pin_gate69.py — C1 PIN for the gate69 BATCH. READ verbs only. --pr A|B; THE HEAD IS A PARAMETER (--head, or env G69_HEAD_A /
G69_HEAD_B; default A head_expected / B head_expected). --b-pr N names PR B's number (kit: 1396).

  P1  origin: refs/pull/<n>/head == refs/heads/<branch> == --head (ls-remote from the SHARED CHECKOUT's origin; --no-remote skips, named)
  P2  the chain.  A: ONE parent == kit parents (3f9ff4e1e1b9); merge-base(head, develop) == 3f9f.
                  B: head ONE parent == the merge c6564b8ff04f; the merge's parents == [e16c3133c296, 3f9ff4e1e1b9] and its tree ==
                     9c6cf0171127; e16c's ONE parent == 22b268143a63; AND the merge is CLEAN: `git merge-tree` of its two parents in the
                     clone gives exactly its tree (a hand edit inside a merge commit would FAIL this; needs a writable clone, else NOT RUN)
                  both: merge-base(head, develop) == the kit merge_base unless develop moved (then: kit merge_base is an ancestor of it)
  P3  merge-base..head names EXACTLY the kit files; numstat per file == kit (A: db.ts 19 0; ks1305 test 119 0; flow 90 0; cheat 41 0)
  P3b B only: e16c..merge adds ONLY develop's paths (22b2..3f9f) and merge..head names ONLY flow, cheat, ks1195 (the title change)
  P4  END_TREE == kit (A 924908aeefe1, B e034a458fa52) — recorded either way; CONTROL: != the merge-base tree
  P5  every non-merge commit in merge-base..head (+ B's merge): %(trailers) CONTENT 0 / RAW 1; CONTROL bf277eead268 53 / 55
  P6  0 Co-Authored-By in every commit message
  P7  every commit subject <= 92 and carries the PR's key; the kit subject(s) match exactly; the subject + " (#<n>)" length printed
  P8  every commit body: only the PR's key hyphenated, 0 closing references; ONE `Refs <key>` in the code commit
  P9  every kit path mode 100644 at the head
  P10 pre-push / preflight / SKILL.md blobs at head == kit == develop (NO-NEW-LEG)
  P11 merge-base..develop touches none of the PR's code paths and no hook path
Refuses BY NAME (rc 2): `head unresolvable`, `develop unresolvable`, `merge-base unresolvable`.
Usage: c1_pin_gate69.py --pr A|B [--repo R] [--head H] [--develop D] [--b-pr N] [--no-remote] | --selftest --repo R
rc 0 PASS / 1 FAIL / 2 refused"""
import io, contextlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate69 import K, git, wgit, Tally, resolvable, outside_forbidden, spec

CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+(#\d+|KS-\d+)', re.I)


def tr_bytes(repo, c):
    raw = git(repo, 'log', '-1', '--format=%(trailers)', c)
    return len(raw.rstrip('\n').encode()), len(raw.encode())


def names(repo, a, b): return [x for x in git(repo, 'diff', '--name-only', a, b).splitlines() if x]


def run(repo, sp, D, remote, t):
    head, base = sp['head'], sp['merge_base']
    for nm, s in (('head', head), ('develop', D), ('merge-base', base)):
        if not resolvable(repo, s):
            print('C1 REFUSED: %s unresolvable: %s not a commit in %s — fetch it BY SHA into YOUR clone (X7)' % (nm, s, repo)); return 2
    # P1
    if remote and sp.get('pr') and sp.get('branch'):
        rc, o, e = git(K['checkout'], 'ls-remote', 'origin', 'refs/pull/%s/head' % sp['pr'], 'refs/heads/%s' % sp['branch'], check=False)
        got = dict((l.split('\t')[1], l.split('\t')[0]) for l in o.splitlines() if '\t' in l)
        ph, bh = got.get('refs/pull/%s/head' % sp['pr']), got.get('refs/heads/%s' % sp['branch'])
        t.check('P1', rc == 0 and ph == head and bh == head, 'ls-remote rc %d | pull/%s/head %s | branch %s | want %s' % (rc, sp['pr'], ph, bh, head[:12]))
    else:
        t.info('P1', 'NOT RUN (--no-remote, or the PR number / branch not supplied: pr=%s branch=%s)' % (sp.get('pr'), sp.get('branch')))
    # P2
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    mb = git(repo, 'merge-base', head, D).strip()
    mb_ok = mb == base or (git(repo, 'merge-base', '--is-ancestor', base, mb, check=False)[0] == 0)
    if sp['key'] == 'A':
        t.check('P2', par == sp['parents'] and mb_ok, 'parents %s (want %s) | merge-base with develop %s (kit %s)' % ([p[:12] for p in par], [p[:12] for p in sp['parents']], mb[:12], base[:12]))
    else:
        ch = sp['chain']
        mpar = git(repo, 'log', '-1', '--format=%P', ch['merge']).split() if resolvable(repo, ch['merge']) else []
        mtree = git(repo, 'rev-parse', ch['merge'] + '^{tree}').strip() if mpar else None
        cpar = git(repo, 'log', '-1', '--format=%P', ch['code']).split() if resolvable(repo, ch['code']) else []
        if outside_forbidden(repo) and len(mpar) == 2:
            rc, o, e = wgit(repo, 'merge-tree', '--write-tree', mpar[0], mpar[1]); clean = (rc == 0 and o.split('\n', 1)[0].strip() == mtree)
            cl = 'git merge-tree of its parents rc %d tree %s == its tree %s' % (rc, o.split('\n', 1)[0].strip()[:12], clean)
        else:
            clean = False; cl = 'CLEAN-MERGE check NOT RUN (repo inside the forbidden root or merge absent) — a FAIL, never a pass'
        t.check('P2', par == [ch['merge']] and mpar == ch['merge_parents'] and mtree == ch['merge_tree'] and cpar == [ch['code_parent']] and clean and mb_ok,
                'head parents %s (want [%s]) | merge parents %s tree %s (want %s) | code commit parent %s | %s | merge-base with develop %s' % (
                    [p[:12] for p in par], ch['merge'][:12], [p[:12] for p in mpar], str(mtree)[:12], ch['merge_tree'][:12], [p[:12] for p in cpar], cl, mb[:12]))
    # P3
    nm = names(repo, base, head)
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).splitlines():
        a, d, p = l.split('\t'); ns[p] = [int(a), int(d)]
    want_ns = sp.get('numstat')
    ok3 = sorted(nm) == sorted(sp['files']) and (want_ns is None or all(ns.get(p) == v for p, v in want_ns.items()))
    t.check('P3', ok3, '%d path(s) (kit %d); extra %s missing %s | numstat %s%s' % (len(nm), len(sp['files']), sorted(set(nm) - set(sp['files'])), sorted(set(sp['files']) - set(nm)),
            {os.path.basename(p)[:28]: v for p, v in ns.items()}, '' if want_ns is None else ' (kit pins %s)' % {os.path.basename(p)[:28]: v for p, v in want_ns.items()}))
    if sp['key'] == 'B':
        ch = sp['chain']
        dev_adv = set(names(repo, ch['code_parent'], base))
        m_adds = set(names(repo, ch['code'], ch['merge']))
        last = set(names(repo, ch['merge'], head))
        dbl = sum(ns.get(p, [0, 0])[0] for p in sp['doubles_files']), sum(ns.get(p, [0, 0])[1] for p in sp['doubles_files'])
        t.check('P3b', m_adds <= dev_adv and last == {K['flow'], K['cheat'], sp['ks1195_file']} and list(dbl) == sp['doubles_numstat_total'],
                'merge adds %d path(s), all from 22b2..3f9f: %s | merge..head %s | the 6 doubles files total +%d/-%d (kit %s)' % (
                    len(m_adds), m_adds <= dev_adv, sorted(os.path.basename(x)[:30] for x in last), dbl[0], dbl[1], sp['doubles_numstat_total']))
    # P4
    tree = git(repo, 'rev-parse', head + '^{tree}').strip(); btree = git(repo, 'rev-parse', base + '^{tree}').strip()
    want_tree = sp.get('end_tree') or sp.get('head_standin_tree')
    t.check('P4', tree == want_tree and tree != btree, 'END_TREE %s (kit %s) | CONTROL merge-base tree %s differs %s' % (tree, str(want_tree)[:12], btree[:12], tree != btree))
    # P5-P8
    commits = git(repo, 'rev-list', '%s..%s' % (base, head)).split()
    commits = [c for c in commits if c in (sp.get('commits') or []) or sp['key'] == 'B' and c in sp['chain'].values()] or commits
    cc, cr = tr_bytes(repo, K['trailer_control'])
    rows5, rows6, rows7, rows8 = [], [], [], []; ok5 = ok6 = ok7 = ok8 = True
    refs_total = 0
    for c in commits:
        content, raw = tr_bytes(repo, c); rows5.append('%s %d/%d' % (c[:12], content, raw)); ok5 &= (content, raw) == (0, 1)
        body = git(repo, 'log', '-1', '--format=%B', c)
        co = len(re.findall(r'(?im)^co-authored-by:', body)); rows6.append('%s %d' % (c[:12], co)); ok6 &= co == 0
        subj = git(repo, 'log', '-1', '--format=%s', c).rstrip('\n'); ismerge = len(git(repo, 'log', '-1', '--format=%P', c).split()) > 1
        if not ismerge:
            exp = sp.get('subject') if sp['key'] == 'A' else sp['subjects'].get(c)
            good = len(subj) <= K['subject_max'] and sp['ticket'] in subj and (exp is None or subj == exp)
            rows7.append('%s %d chars%s%s' % (c[:12], len(subj), ' (+ " (#%s)" = %d)' % (sp['pr'], len(subj) + len(' (#%s)' % sp['pr'])) if sp.get('pr') else '', '' if exp is None or subj == exp else ' != kit subject'))
            ok7 &= good
            keys = sorted(set(re.findall(r'\bKS-\d+\b', body))); clos = CLOSING.findall(body)
            refs = len(re.findall(r'(?m)^\s*Refs %s\b' % re.escape(sp['ticket']), body)); refs_total += refs
            rows8.append('%s keys %s closing %d Refs %d' % (c[:12], keys, len(clos), refs)); ok8 &= keys == [sp['ticket']] and not clos
        else:
            rows7.append('%s MERGE subject %r (squashed away)' % (c[:12], subj[:60]))
    t.check('P5', ok5 and (cc, cr) == (K['trailer_control_content_bytes'], K['trailer_control_raw_bytes']),
            'trailers content/raw per commit %s (want 0/1) | CONTROL %s %d/%d (want 53/55)' % (rows5, K['trailer_control'], cc, cr))
    t.check('P6', ok6, 'Co-Authored-By per commit %s' % rows6)
    t.check('P7', ok7, 'subjects %s (<= %d, carry %s)' % (rows7, K['subject_max'], sp['ticket']))
    t.check('P8', ok8 and refs_total == 1, 'per commit %s | `Refs %s` lines in total %d (want 1)' % (rows8, sp['ticket'], refs_total))
    # P9
    modes = {p: git(repo, 'ls-tree', head, '--', p).split(' ')[0] for p in sp['files']}
    t.check('P9', all(m == '100644' for m in modes.values()), 'modes %s' % sorted(set(modes.values())))
    # P10
    rows = []; ok = True
    for p, b in K['hook_blobs'].items():
        h = git(repo, 'rev-parse', '%s:%s' % (head, p)).strip(); d = git(repo, 'rev-parse', '%s:%s' % (D, p)).strip()
        ok &= h == b == d; rows.append('%s head %s dev %s kit %s' % (os.path.basename(p), h[:12], d[:12], b[:12]))
    t.check('P10', ok, 'NO-NEW-LEG: %s' % rows)
    # P11
    adv = set(names(repo, base, D)); hit = sorted(adv & (set(sp['code_paths']) | set(K['hook_blobs'])))
    t.check('P11', not hit, 'merge-base..develop %d path(s); PR code / hook paths among them %s (develop %s)' % (len(adv), hit or 'none', D[:12]))
    return None


def selftest(repo):
    ok = n = 0
    def arm(name, which, head, want_fail, extra=None, D=None):
        nonlocal ok, n
        t = Tally(); sp = spec(which, head, '1396' if which == 'B' else None)
        if extra: sp.update(extra)
        with contextlib.redirect_stdout(io.StringIO()): r = run(repo, sp, D or K['develop_at_draft'], False, t)
        good = (not t.fails and r is None) if want_fail is None else (set(want_fail) <= set(t.fails))
        n += 1; ok += good
        print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want_fail is None else 'FAIL on %s' % want_fail, t.fails or 'NONE'))
    arm('A at its kit head', 'A', None, None)
    # MEASURED DEFECT (drafter, 2026-10-06): e16c3133c296's body hyphenates KS-1231 and KS-1233, e6eb53fe2658's hyphenates KS-938 —
    # the READY's 'Only KS-1256 is hyphenated in ... both commit messages' is FALSE. The arm pins that P8 FIRES on the real head.
    arm('B at its kit head (P8 FIRES on the measured foreign hyphenated keys)', 'B', None, ['P8'])
    arm('PLANTED: A checked at B\'s head', 'A', K['prs']['B']['head_expected'], ['P2', 'P3', 'P4', 'P7'])
    arm('PLANTED: B checked at A\'s head', 'B', K['prs']['A']['head_expected'], ['P2', 'P3', 'P4'])
    arm('PLANTED: B checked at its MERGE commit (docs absent)', 'B', K['prs']['B']['chain']['merge'], ['P2', 'P3', 'P3b', 'P4'])
    arm('PLANTED: A with a numstat pin of db.ts 18 1', 'A', None, ['P3'], {'numstat': {K['prs']['A']['product_file']: [18, 1]}})
    arm('PLANTED: B against a develop = A\'s head with db.ts declared a B code path (a develop advance touching it)', 'B', None, ['P11'],
        {'code_paths': K['prs']['B']['code_paths'] + [K['prs']['A']['product_file']]}, K['prs']['A']['head_expected'])
    t = Tally()
    with contextlib.redirect_stdout(io.StringIO()): r = run(repo, spec('A', 'f' * 40), K['develop_at_draft'], False, t)
    n += 1; g = r == 2 and t.n == 0; ok += g; print('SELFTEST %s absent head refuses BY NAME, 0 checks' % ('OK' if g else 'MISS'))
    k = sorted(set(re.findall(r'\bKS-\d+\b', 'Refs KS-1305. See KS 1422 and KS 458.'))); c = CLOSING.findall('Fixes KS-1422')
    n += 1; g = k == ['KS-1305'] and bool(c); ok += g; print('SELFTEST %s key scan: de-hyphenated keys are not keys; `Fixes KS-1422` is a closing reference' % ('OK' if g else 'MISS'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); print('CHECKED %d arm(s)' % n)
    return 0 if ok == n else 1


def main():
    A = sys.argv[1:]
    if not A or '--help' in A: print(__doc__); return 2
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    repo = opt('--repo', K['checkout'])
    if '--selftest' in A: return selftest(repo)
    which = opt('--pr', 'A')
    if which not in ('A', 'B'): print('unknown --pr'); return 2
    sp = spec(which, opt('--head'), opt('--b-pr') if which == 'B' else None, opt('--branch'))
    D = opt('--develop', K['develop_at_draft'])
    print('c1_pin_gate69 PR %s #%s %s | head %s | develop %s | repo %s' % (which, sp.get('pr'), sp['ticket'], sp['head'], D[:12], repo))
    t = Tally(); r = run(repo, sp, D, '--no-remote' not in A, t)
    if r == 2: print('CHECKED 0 (refused by name)'); return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
