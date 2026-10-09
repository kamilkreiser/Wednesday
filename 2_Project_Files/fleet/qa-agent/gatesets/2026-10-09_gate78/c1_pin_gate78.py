#!/usr/bin/env python3
"""c1_pin_gate78.py — C1 PIN for #1435 (KS-1452). Read verbs only. Carried from c1_pin_gate72.py; [g72] marks gate72's changes,
[g78] this kit's (P8b the sibling ticket; the tooling list is kit.json's, 28 paths).

EVERY PIN IS A REQUIRED ARGUMENT (no default; a wrong value FAILS its check — the wrong-value arms are in --selftest and KIT_REPORT):
  --repo R --head H --base B --develop D --end-tree T --parents-n N   [--no-remote]

  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  [g72 split, STANDING_LINES R 5th] head is a commit | it has EXACTLY --parents-n parents | first parent == --base
  P2b develop descends from --base; merge-base(head, develop) printed
  P3  base..head paths == EXACTLY the kit's 5 with the kit numstat (+18 -18), every lock +N -N
  P4  END_TREE == --end-tree, and == kit end_tree (both printed; a --end-tree that disagrees with the head FAILS)
  P5  %(trailers) CONTENT 0 bytes on the head; CONTROL bf277eead268 prints > 0
  P6  0 Co-Authored-By in the message; CONTROL carries >= 1
  P7  subject == kit subject, <= 84, key first; squash length (+ " (#1435)") <= 92
  P8  only KS-1452 hyphenated in the message; 0 closing-family words before a key / #n
  P8b [g78] the SIBLING ticket KS-1453 (filed by the builder, NOT built) is named only UNHYPHENATED ("KS 1453", >= 1 mention) and 0
      times hyphenated in the message — a hyphenated foreign key ATTACHES the PR to that ticket (STANDING_LINES :278-:279)
  P9  every changed path 100644 at base and head, no add / delete / mode change (diff --summary empty)
  P10 NO-NEW-LEG [g72 via ls-tree, absent = its own state]: every kit tooling path (hooks, preflight, cleanroom, audit scripts, THE
      BASELINE blob 4af041e8d74a, expected-case-count, the root + the 4 member manifests, the mobile lock + manifest, the 4 service
      Dockerfiles, the 3 workflows that went red or pending on the head, the skill, CLAUDE.md) has the SAME (mode, blob) at base, head
      and develop, and is PRESENT
  P10b the baseline blob == kit baseline_blob (4af041e8d74a) at head
  P11 0 manifests (package.json) and 0 non-lock paths changed; mobile/secuura-app 0 paths
  P12 base..develop disjoint from the PR's 5 paths and the tooling paths
  --selftest   planted arms (incl. the wrong-value arms for every required pin): each must FAIL.
rc 0 all pass / 1 a FAIL / 2 refused (missing argument, unresolvable sha)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate78 import K, Tally, git, resolvable, blob, req, opt

P = K['pr']
CLOSING = re.compile(K['closing_rx'], re.I)


def numstat_ok(got, want):
    bad = []
    if set(got) != set(want):
        bad.append('paths: extra %s missing %s' % (sorted(set(got) - set(want))[:5], sorted(set(want) - set(got))[:5]))
    for p, v in got.items():
        if p in want and list(v) != list(want[p]):
            bad.append('%s %s != kit %s' % (p, v, want[p]))
        if p.endswith('package-lock.json') and v[0] != v[1]:
            bad.append('%s not +N -N (%s)' % (p, v))
    return bad


def msg_findings(msg):
    keys = sorted(set(re.findall(r'\bKS-\d+\b', msg)))
    return keys, CLOSING.findall(msg), len(re.findall(r'(?im)^co-authored-by:', msg))


def sibling_mentions(msg, sib):
    """[g78] (hyphenated count, unhyphenated count) of the sibling key, e.g. KS-1453 vs KS 1453."""
    n = sib.split('-', 1)[1]
    return len(re.findall(r'\bKS-%s\b' % n, msg)), len(re.findall(r'\bKS %s\b' % n, msg))


def parse_numstat(text):
    out = {}
    for l in text.strip('\n').split('\n'):
        if l:
            a, d, p = l.split('\t'); out[p] = [int(a), int(d)]
    return out


def parents_ok(parents, n, base):
    """[g72] three facts, each its own reason (a whole-%P compare is false by construction on a merge)."""
    why = []
    if len(parents) != n: why.append('parent count %d != %d' % (len(parents), n))
    if not parents or parents[0] != base: why.append('first parent %s != base %s' % ((parents or ['NONE'])[0][:12], base[:12]))
    return why


def tooling_moved(readings):
    """readings: {path: (base, head, develop)} of '<mode> <blob>' or '' (absent). FAIL on any difference AND on absent anywhere."""
    return ['%s %s' % (p, [x[-12:] if x else 'ABSENT' for x in r]) for p, r in readings.items() if not (r[0] and r[0] == r[1] == r[2])]


def run(repo, head, base, develop, end_tree, n_par, remote):
    t = Tally()
    for s, n in ((head, 'head'), (base, 'base'), (develop, 'develop'), (K['trailer_control'], 'trailer control')):
        if not resolvable(repo, s):
            print('REFUSED: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (n, s, repo)); return 2
    if remote:
        ls = git(repo, 'ls-remote', K['github_url'], 'refs/pull/%s/head' % P['pr'], 'refs/heads/' + P['branch'])
        refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in ls.strip().split('\n') if '\t' in l)
        a, b = refs.get('refs/pull/%s/head' % P['pr'], 'ABSENT'), refs.get('refs/heads/' + P['branch'], 'ABSENT')
        t.check('P1', a == head and b == head, 'origin pull/head %s branch %s == head %s' % (a[:12], b[:12], head[:12]))
    else:
        t.info('P1', 'NOT RUN by name (--no-remote): the caller read origin itself')
    typ = git(repo, 'cat-file', '-t', head).strip()
    parents = git(repo, 'log', '-1', '--format=%P', head).split()
    why = parents_ok(parents, n_par, base)
    t.check('P2', typ == 'commit' and not why, 'type %s | %d parent(s) (want %d) | first %s (want %s) %s' % (
        typ, len(parents), n_par, (parents or ['NONE'])[0][:12], base[:12], why or ''))
    mb = git(repo, 'merge-base', head, develop).strip()
    anc = git(repo, 'merge-base', '--is-ancestor', base, develop, check=False)[0] == 0
    t.check('P2b', anc, 'develop %s descends from the base %s; merge-base(head, develop) = %s' % (develop[:12], base[:12], mb[:12]))
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head))
    bad = numstat_ok(ns, P['numstat'])
    t.check('P3', not bad, '%d paths, +%d -%d (kit %d paths +%d -%d) %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()),
            P['file_count'], P['adds_dels'][0], P['adds_dels'][1], bad[:4] or 'exact'))
    tree = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tree == end_tree, 'END_TREE %s == --end-tree %s (kit %s: %s)' % (tree[:12], end_tree[:12], P['end_tree'][:12], tree == P['end_tree']))
    tr = git(repo, 'log', '-1', '--format=%(trailers)', head)
    ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'])
    t.check('P5', tr.strip() == '' and ctl.strip() != '', 'trailers content %d bytes (raw %d) | CONTROL %s content %d bytes' % (
        len(tr.strip()), len(tr), K['trailer_control'], len(ctl.strip())))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    keys, closing, co = msg_findings(msg)
    co_ctl = msg_findings(git(repo, 'log', '-1', '--format=%B', K['trailer_control']))[2]
    t.check('P6', co == 0 and co_ctl >= 1, 'Co-Authored-By in the message %d | CONTROL %s carries %d' % (co, K['trailer_control'], co_ctl))
    subj = msg.split('\n', 1)[0]; sq = len(subj) + len(' (#%s)' % P['pr'])
    t.check('P7', subj == P['subject'] and len(subj) <= P['subject_max_commit'] and subj.startswith(P['ticket'] + ':') and sq <= P['squash_max'],
            'subject %r %d chars (<= %d), squash %d (<= %d), == kit %s' % (subj, len(subj), P['subject_max_commit'], sq, P['squash_max'], subj == P['subject']))
    t.check('P8', keys == [P['ticket']] and not closing, 'hyphenated keys in the message %s (want only %s) | closing %s | de-hyphenated mentions %d' % (
        keys, P['ticket'], closing or 'none', len(re.findall(r'\bKS \d+\b', msg))))
    sib_h, sib_u = sibling_mentions(msg, P['sibling_ticket'])
    t.check('P8b', sib_h == 0 and sib_u >= 1, 'sibling %s: hyphenated %d (want 0) | unhyphenated %d (want >= 1, the builder\'s deliberate form)' % (
        P['sibling_ticket'], sib_h, sib_u))
    modes = []
    for rev in (base, head):
        for l in git(repo, 'ls-tree', '-r', rev, '--', *sorted(ns)).strip().split('\n'):
            if l: modes.append(l.split()[0])
    summ = git(repo, 'diff', '--summary', base, head).strip()
    t.check('P9', set(modes) == {'100644'} and len(modes) == 2 * len(ns) and summ == '', 'modes %s over %d blob readings (want 100644 x %d) | diff --summary %r' % (
        sorted(set(modes)), len(modes), 2 * len(ns), summ[:80]))
    readings = dict((p, tuple(blob(repo, r, p) for r in (base, head, develop))) for p in K['tooling_paths_unchanged'])
    moved = tooling_moved(readings)
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling paths present and identical at base / head / develop %s' % (len(readings), moved[:4] or ''))
    bl = blob(repo, head, K['baseline_path'])
    t.check('P10b', bl.endswith(K['baseline_blob']), 'baseline %s at head == kit %s' % (bl or 'ABSENT', K['baseline_blob'][:12]))
    other = [p for p in ns if not p.endswith('package-lock.json')]
    man = [p for p in ns if p.endswith('package.json')]
    mob = [p for p in ns if any(p.startswith(d + '/') for d in K['out_of_scope_lock_dirs'])]
    t.check('P11', not other and not man and not mob, 'non-lock paths %s | manifests %s | mobile paths %s' % (other or 0, man or 0, mob or 0))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    hit = sorted(set(adv) & (set(ns) | set(K['tooling_paths_unchanged'])))
    t.check('P12', not hit, 'base..develop: %d path(s), %d shared with the PR / tooling %s' % (len(adv), len(hit), hit[:5]))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    want = {'a/package-lock.json': [3, 3], 'b/package-lock.json': [5, 5]}
    rep(not numstat_ok(dict(want), want), 'numstat: the exact set passes')
    rep(numstat_ok(dict(want, **{K['baseline_path']: [1, 0]}), want), 'PLANTED baseline path in the diff FAILS')
    rep(numstat_ok({'a/package-lock.json': [4, 3], 'b/package-lock.json': [5, 5]}, {'a/package-lock.json': [4, 3], 'b/package-lock.json': [5, 5]}), 'PLANTED lock +4 -3 FAILS (not +N -N)')
    rep(numstat_ok({'a/package-lock.json': [3, 3]}, want), 'PLANTED missing lock FAILS')
    b = 'b' * 40
    rep(not parents_ok([b], 1, b), 'parents: one parent == base passes')
    rep(parents_ok([b, 'c' * 40], 1, b), 'PLANTED merge commit (2 parents, first == base) FAILS on the count')
    rep(parents_ok(['c' * 40], 1, b), 'WRONG-VALUE ARM --base FAILS the first-parent check')
    rep(parents_ok([b], 2, b), 'WRONG-VALUE ARM --parents-n 2 FAILS')
    rep(not tooling_moved({'x': ('100644 a', '100644 a', '100644 a')}), 'tooling: identical present blobs pass')
    rep(tooling_moved({'x': ('', '', '')}), 'PLANTED absent-everywhere tooling path FAILS (absent is a state, never a pass)')
    rep(tooling_moved({'x': ('100644 a', '100644 a', '100755 a')}), 'PLANTED mode change on develop FAILS')
    k, c, co = msg_findings('KS-1452: x\n\nRefs KS-1452\nfiled as KS 1453; KS 767.\n'); rep(k == ['KS-1452'] and not c and co == 0, 'message: de-hyphenated keys are not keys')
    k, c, co = msg_findings('KS-1452: x\n\nFixes KS-1453.\nCo-Authored-By: X <x@y>\n')
    rep(k == ['KS-1452', 'KS-1453'] and c and co == 1, 'PLANTED `Fixes KS-1453` + Co-Authored-By: second key, closing word and trailer all FIRE')
    rep(sibling_mentions('filed as KS 1453 and not touched', 'KS-1453') == (0, 1), 'P8b: the unhyphenated sibling passes')
    rep(sibling_mentions('filed as KS-1453 and not touched', 'KS-1453')[0] == 1, 'PLANTED hyphenated sibling KS-1453 FIRES P8b')
    rep(sibling_mentions('no sibling named', 'KS-1453') == (0, 0), 'PLANTED sibling absent: P8b FAILS (>= 1 wanted: the builder said it names it)')
    rep(sibling_mentions('KS 14530 and KS-14531', 'KS-1453') == (0, 0), 'P8b word boundary: KS 14530 / KS-14531 are not KS 1453')
    for a in (['--repo', 'x'], ['--repo', 'x', '--head', 'abc']):
        try:
            req(a, '--head', hex40=True); rep(False, 'required --head missing/short was ACCEPTED')
        except SystemExit:
            rep(True, 'REQUIRED-ARG ARM %s -> refused' % a)
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        repo = req(A, '--repo'); head = req(A, '--head', True); base = req(A, '--base', True); develop = req(A, '--develop', True)
        end_tree = req(A, '--end-tree', True); n_par = int(req(A, '--parents-n'))
    except SystemExit as e:
        print(e); return 2
    print('C1 #%s head %s base %s develop %s end-tree %s parents-n %d repo %s' % (P['pr'], head, base, develop, end_tree, n_par, repo))
    return run(repo, head, base, develop, end_tree, n_par, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
