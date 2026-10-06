#!/usr/bin/env python3
"""c1_pin_gate70.py — C1 PIN for #1397 (KS-1425). THE HEAD IS A PARAMETER (--head). Read verbs only.

  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote, skipped by name with --no-remote)
  P2  ONE parent == the kit base 4eaf; merge-base(head, --develop) printed; develop descends from the base
  P3  base..head paths == EXACTLY the kit's 37 with the kit numstat (36 package-lock.json + the baseline), and every lock is +N -N
  P4  END_TREE == kit end_tree
  P5  %(trailers) CONTENT 0 bytes on the head; CONTROL bf277eead268 prints > 0 (the instrument can see a trailer)
  P6  0 Co-Authored-By in the message; CONTROL: the trailer-control commit carries 1
  P7  subject == kit subject, <= 84, key first; squash length (+ " (#1397)") <= 92
  P8  only KS-1425 hyphenated in the message; 0 closing-family words before a key / #n
  P9  every path 100644 at base and head (no mode change, no new file, no deletion)
  P10 NO-NEW-LEG: every kit tooling path (hooks, preflight, cleanroom, the audit scripts, expected-case-count, the root manifest,
      the mobile lock, the skill) has the SAME blob at head and at the base — and at --develop
  P11 0 manifests (package.json) and 0 non-lock / non-baseline paths changed
  P12 base..develop disjoint from the PR's 37 paths and the tooling paths (a moved develop that touched them re-gates)
  --selftest   planted arms on synthetic numstat / messages: each must FAIL.
rc 0 all pass / 1 a FAIL."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate70 import K, Tally, git, resolvable

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


def msg_findings(msg, key):
    keys = sorted(set(re.findall(r'\bKS-\d+\b', msg)))
    return keys, CLOSING.findall(msg), len(re.findall(r'(?im)^co-authored-by:', msg))


def parse_numstat(text):
    out = {}
    for l in text.strip('\n').split('\n'):
        if l:
            a, d, p = l.split('\t'); out[p] = [int(a), int(d)]
    return out


def run(repo, head, develop, remote):
    t = Tally(); base = P['parents'][0]
    for s, n in ((head, 'head'), (base, 'base'), (develop, 'develop')):
        if not resolvable(repo, s):
            print('REFUSED: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (n, s, repo)); return 2
    if remote:
        ls = git(repo, 'ls-remote', K['github_url'], 'refs/pull/%s/head' % P['pr'], 'refs/heads/' + P['branch'])
        refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in ls.strip().split('\n') if '\t' in l)
        t.check('P1', refs.get('refs/pull/%s/head' % P['pr']) == head and refs.get('refs/heads/' + P['branch']) == head,
                'origin pull/head %s branch %s == head %s' % (refs.get('refs/pull/%s/head' % P['pr'], 'ABSENT')[:12], refs.get('refs/heads/' + P['branch'], 'ABSENT')[:12], head[:12]))
    else:
        t.info('P1', 'NOT RUN by name (--no-remote): the caller read origin itself')
    parents = git(repo, 'log', '-1', '--format=%P', head).split()
    t.check('P2', parents == [base], 'parents %s == [%s]' % ([x[:12] for x in parents], base[:12]))
    mb = git(repo, 'merge-base', head, develop).strip()
    anc = git(repo, 'merge-base', '--is-ancestor', base, develop, check=False)[0] == 0
    t.check('P2b', anc, 'develop %s descends from the base %s; merge-base(head, develop) = %s' % (develop[:12], base[:12], mb[:12]))
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head))
    bad = numstat_ok(ns, P['numstat'])
    t.check('P3', not bad, '%d paths, +%d -%d (kit %d paths +%d -%d) %s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()),
            P['file_count'], P['adds_dels'][0], P['adds_dels'][1], bad[:4] or 'exact'))
    tree = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', tree == P['end_tree'], 'END_TREE %s == kit %s' % (tree[:12], P['end_tree'][:12]))
    tr = git(repo, 'log', '-1', '--format=%(trailers)', head)
    ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control'])
    t.check('P5', tr.strip() == '' and ctl.strip() != '', 'trailers content %d bytes (raw %d) | CONTROL %s content %d bytes' % (
        len(tr.strip()), len(tr), K['trailer_control'], len(ctl.strip())))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    keys, closing, co = msg_findings(msg, P['ticket'])
    co_ctl = msg_findings(git(repo, 'log', '-1', '--format=%B', K['trailer_control']), '')[2]
    t.check('P6', co == 0 and co_ctl >= 1, 'Co-Authored-By in the message %d | CONTROL %s carries %d' % (co, K['trailer_control'], co_ctl))
    subj = msg.split('\n', 1)[0]; sq = len(subj) + len(' (#%s)' % P['pr'])
    t.check('P7', subj == P['subject'] and len(subj) <= P['subject_max_commit'] and subj.startswith(P['ticket'] + ':') and sq <= P['squash_max'],
            'subject %r %d chars (<= %d), squash %d (<= %d), == kit %s' % (subj, len(subj), P['subject_max_commit'], sq, P['squash_max'], subj == P['subject']))
    t.check('P8', keys == [P['ticket']] and not closing, 'hyphenated keys in the message %s (want only %s) | closing %s | de-hyphenated mentions %d' % (
        keys, P['ticket'], closing or 'none', len(re.findall(r'\bKS \d+\b', msg))))
    modes = []
    for rev in (base, head):
        for l in git(repo, 'ls-tree', '-r', rev, '--', *sorted(ns)).strip().split('\n'):
            modes.append(l.split()[0])
    summ = git(repo, 'diff', '--summary', base, head).strip()
    t.check('P9', set(modes) == {'100644'} and len(modes) == 2 * len(ns) and summ == '', 'modes %s over %d blob readings (want 100644 x %d) | diff --summary %r' % (
        sorted(set(modes)), len(modes), 2 * len(ns), summ[:80]))
    moved = []
    for p in K['tooling_paths_unchanged']:
        b = [git(repo, 'rev-parse', '%s:%s' % (r, p), check=False)[1].strip() for r in (base, head, develop)]
        if not (b[0] and b[0] == b[1] == b[2]): moved.append('%s %s' % (p, [x[:12] for x in b]))
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling paths identical at base / head / develop %s' % (len(K['tooling_paths_unchanged']), moved[:3] or ''))
    other = [p for p in ns if not (p.endswith('package-lock.json') or p == K['baseline_path'])]
    man = [p for p in ns if p.endswith('package.json')]
    t.check('P11', not other and not man and K['baseline_path'] in ns, 'non-lock non-baseline paths %s | manifests %s' % (other or 0, man or 0))
    adv = [l for l in git(repo, 'diff', '--name-only', base, develop).split('\n') if l]
    hit = sorted(set(adv) & (set(ns) | set(K['tooling_paths_unchanged'])))
    t.check('P12', not hit, 'base..develop: %d path(s), %d shared with the PR / tooling %s' % (len(adv), len(hit), hit[:5]))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    want = {'a/package-lock.json': [3, 3], K['baseline_path']: [14, 0]}
    rep(not numstat_ok(dict(want), want), 'numstat: the exact set passes')
    rep(numstat_ok({'a/package-lock.json': [3, 3], K['baseline_path']: [14, 0], 'x.ts': [1, 0]}, want), 'PLANTED extra path FAILS')
    rep(numstat_ok({'a/package-lock.json': [4, 3], K['baseline_path']: [14, 0]}, {'a/package-lock.json': [4, 3], K['baseline_path']: [14, 0]}), 'PLANTED lock +4 -3 FAILS (not +N -N)')
    rep(numstat_ok({'a/package-lock.json': [3, 3]}, want), 'PLANTED missing baseline FAILS')
    k, c, co = msg_findings('KS-1425: x\n\nGate owners KS 470, KS 531.\n', 'KS-1425'); rep(k == ['KS-1425'] and not c and co == 0, 'message: de-hyphenated keys are not keys')
    k, c, co = msg_findings('KS-1425: x\n\nFixes KS-1403.\nCo-Authored-By: X <x@y>\n', 'KS-1425')
    rep(k == ['KS-1403', 'KS-1425'] and c and co == 1, 'PLANTED `Fixes KS-1403` + a Co-Authored-By line: second key, closing word and trailer all FIRE')
    k, c, co = msg_findings('closes: #1397', 'KS-1425'); rep(bool(c), 'PLANTED `closes: #1397` FIRES')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if '--selftest' in A: return selftest()
    if not opt('--repo'): print(__doc__); return 2
    head = opt('--head', P['head_expected']); develop = opt('--develop', K['develop_at_draft'])
    print('C1 #%s head %s develop %s repo %s' % (P['pr'], head, develop, opt('--repo')))
    return run(opt('--repo'), head, develop, '--no-remote' not in A)


if __name__ == '__main__':
    sys.exit(main())
