#!/usr/bin/env python3
"""c1_pin_gate66.py — C1 PIN + SCOPE for #1385 (KS-938, T1) at the merge-in head f6b49d68209d. READ verbs only (lib_gate66.git).

  P1  origin (ONE ls-remote, from the checkout with its own core.sshCommand): refs/pull/1385/head == the kit branch == --head;
      develop recorded and compared with --develop                                                   (skipped with --no-remote)
  P2  parents == [79c87b8aaa48 (the PR's previous head), d784b613c81e (develop at the READY)]; 79c87's ONE parent is the original base
      46c3e20cfbd2; d784 is an ancestor of --develop and == merge-base(head, --develop)
  P3  base(d784)..head names EXACTLY the 5 kit paths with the kit +/- (none extra, none missing); three-dot d784...head the same
  P4  head^{tree} == END_TREE 04fa3e0d1b48; CONTROLS: the d784 tree and the --develop tree both differ
  P5  `%(trailers)` RAW bytes == 1 at the head AND at 79c87; CONTROL bf277eead268 == 55 (else the instrument is blind)
  P6  Co-Authored-By lines == 0 in the head and 79c87 messages; CONTROL bf277eead268 >= 1
  P7  head subject == the kit subject (a docs-only merge-in naming d784 and the branch); the PR's commit subject (79c87) == the PR title
  P8  79c87's message: ONE `Refs KS-938` line; the only hyphenated KS key is KS-938; 0 Linear closing words before a KS key; 0 `<kw> #n`
  P9  `git ls-tree` modes == 100644 for all 5 paths
  P10 hooks + skill: `.githooks/pre-push`, `scripts/preflight/preflight.sh`, the test-discipline SKILL.md blobs at head == at d784 ==
      at --develop == kit
  P11 develop's advance d784..--develop is PATH-DISJOINT from the 3 CODE paths and the hook paths (the Q-M precondition); doc paths in
      the advance are EXPECTED (a second docs merge-in) and printed as INFO
Usage: c1_pin_gate66.py --repo <git dir> [--head <sha>] [--develop <sha>] [--no-remote]  |  --selftest --scratch-clone <clone>
rc 0 all PASS / rc 1 any FAIL (or 0 checked) / rc 2 an object is not in --repo (REFUSED BY NAME: `<name> unresolvable`)."""
import io, contextlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate66 import K, git, Tally

KEY_RX = re.compile(r'\bKS-\d+\b')
CLOSE_RX = re.compile(r'\b(close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)\b[^.\n]{0,60}?\bKS-\d+', re.I)
GHCLOSE_RX = re.compile(r'\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+', re.I)
HOOKS = list(K['hook_blobs'].keys())
CODE = K['code_paths']
CONTROL = 'bf277eead268'


def numstat(repo, a, b, three=False):
    ns = {}
    for l in git(repo, 'diff', '--numstat', ('%s...%s' % (a, b)) if three else a, *([] if three else [b])).splitlines():
        x, d, p = l.split('\t', 2)
        ns[p] = [int(x), int(d)]
    return ns


def resolvable(repo, s):
    return bool(s) and git(repo, 'rev-parse', '--verify', '--quiet', s + '^{commit}', check=False)[0] == 0


def blob(repo, rev, p):
    return git(repo, 'rev-parse', '--verify', '--quiet', '%s:%s' % (rev, p), check=False)[1].strip()


def run(repo, head, develop, t, remote=True):
    base = K['base']
    if remote:
        ls = subprocess.run(['git', '-C', K['checkout'], 'ls-remote', 'origin', 'refs/heads/develop', 'refs/heads/' + K['branch'], 'refs/pull/%s/head' % K['pr']], capture_output=True, text=True)
        refs = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.splitlines() if '\t' in l}
        ph, bh, dv = refs.get('refs/pull/%s/head' % K['pr']), refs.get('refs/heads/' + K['branch']), refs.get('refs/heads/develop')
        t.check('P1', ls.returncode == 0 and ph == head == bh, 'ls-remote rc %d: pull/head %s branch %s (want %s); origin develop %s (--develop %s, equal %s)' % (
            ls.returncode, (ph or '')[:12], (bh or '')[:12], head[:12], (dv or '')[:12], develop[:12], dv == develop))
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    pp = git(repo, 'log', '-1', '--format=%P', K['prev_head']).split()
    anc = git(repo, 'merge-base', '--is-ancestor', base, develop, check=False)[0] == 0
    mb = git(repo, 'merge-base', head, develop).strip()
    t.check('P2', par == K['head_parents'] and pp == [K['orig_base']] and anc and mb == base, 'parents %s (want %s); 79c87 parent %s (want %s); d784 ancestor of develop %s; merge-base(head, develop) %s (want %s)' % (
        [p[:12] for p in par], [p[:12] for p in K['head_parents']], [p[:12] for p in pp], K['orig_base'][:12], anc, mb[:12], base[:12]))
    ns = numstat(repo, base, head); ns3 = numstat(repo, base, head, three=True)
    want = {p: list(v) for p, v in K['files'].items()}
    t.check('P3', ns == want and ns3 == want, 'd784..head %d path(s): extra %s missing %s +/- mismatches %s | three-dot equal %s' % (
        len(ns), sorted(set(ns) - set(want)), sorted(set(want) - set(ns)), {p[-40:]: (ns[p], want[p]) for p in ns if p in want and ns[p] != want[p]}, ns3 == want))
    tr = git(repo, 'rev-parse', head + '^{tree}').strip(); bt = git(repo, 'rev-parse', base + '^{tree}').strip(); dt = git(repo, 'rev-parse', develop + '^{tree}').strip()
    t.check('P4', tr == K['end_tree'] and bt != tr and dt != tr, 'head tree %s (want %s); controls: d784 tree %s differs %s, develop tree %s differs %s' % (tr[:12], K['end_tree'][:12], bt[:12], bt != tr, dt[:12], dt != tr))
    tb = lambda c: len(git(repo, 'log', '-1', '--format=%(trailers)', c).encode())
    ctl = tb(CONTROL) if resolvable(repo, CONTROL) else -1
    t.check('P5', tb(head) == 1 and tb(K['prev_head']) == 1 and ctl == 55, 'raw trailer bytes: head %d, 79c87 %d (want 1 / 1); CONTROL %s = %d (want 55)' % (tb(head), tb(K['prev_head']), CONTROL, ctl))
    co = lambda c: len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', c)))
    cco = co(CONTROL) if resolvable(repo, CONTROL) else -1
    t.check('P6', co(head) == 0 and co(K['prev_head']) == 0 and cco >= 1, 'Co-Authored-By: head %d, 79c87 %d (want 0 / 0); CONTROL %s %d (want >= 1)' % (co(head), co(K['prev_head']), CONTROL, cco))
    s = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n'); s2 = git(repo, 'log', '-1', '--format=%s', K['prev_head']).rstrip('\n')
    t.check('P7', s == K['subject'] and s2 == K['pr_title'], 'head subject == kit %s (%d chars) | 79c87 subject == PR title %s' % (s == K['subject'], len(s), s2 == K['pr_title']))
    msg = git(repo, 'log', '-1', '--format=%B', K['prev_head'])
    refs_ = re.findall(r'(?m)^Refs KS-938\s*$', msg); keys = sorted(set(KEY_RX.findall(msg))); cl = CLOSE_RX.findall(msg); gh = GHCLOSE_RX.findall(msg)
    hm = git(repo, 'log', '-1', '--format=%B', head); hkeys = sorted(set(KEY_RX.findall(hm))); hcl = CLOSE_RX.findall(hm) + GHCLOSE_RX.findall(hm)
    t.check('P8', len(refs_) == 1 and keys == ['KS-938'] and not cl and not gh and set(hkeys) <= {'KS-938'} and not hcl,
            "79c87: `Refs KS-938` lines %d, keys %s, closing %s, GH closing %s | head msg keys %s, closing %s" % (len(refs_), keys, cl, gh, hkeys, hcl))
    modes = {p: git(repo, 'ls-tree', head, '--', p).split()[0] for p in K['files']}
    t.check('P9', all(m == K['modes_all'] for m in modes.values()), 'modes %s' % sorted(set(modes.values())))
    hk = {p: (blob(repo, head, p), blob(repo, base, p), blob(repo, develop, p)) for p in HOOKS + [K['skill']]}
    want_b = dict(K['hook_blobs']); want_b[K['skill']] = K['skill_blob']
    t.check('P10', all(v[0] == v[1] == v[2] == want_b[p] for p, v in hk.items()), 'hook + skill blobs head / d784 / develop == kit: %s' % {os.path.basename(p): v[0] == v[1] == v[2] == want_b[p] for p, v in hk.items()})
    adv = git(repo, 'diff', '--name-only', base, develop).splitlines(); hit = sorted(set(adv) & set(CODE + HOOKS))
    docs = sorted(os.path.basename(p)[:30] for p in set(adv) & {K['flow'], K['cheat']})
    t.check('P11', not hit, "develop's advance d784..%s: %d path(s); code / hook paths among them %s" % (develop[:12], len(adv), hit))
    t.info('P11-docs', 'platform-k docs in the advance (EXPECTED: a second docs merge-in is owed): %s' % docs)


def main(repo, head, develop, remote):
    for name, s in (('head', head), ('develop', develop), ('base', K['base']), ('previous head', K['prev_head'])):
        if not resolvable(repo, s):
            print('REFUSED: %s unresolvable: %r is not a commit in %s — fetch it BY SHA into YOUR clone' % (name, s, repo)); return 2
    t = Tally(); run(repo, head, develop, t, remote); return t.end()


def selftest(clone):
    ok = total = 0
    def rep(c, m):
        nonlocal ok, total
        total += 1; ok += bool(c); print('SELFTEST %s %s' % ('OK' if c else 'MISS', m))
    def cap(*a):
        with contextlib.redirect_stdout(io.StringIO()) as b: r = main(*a)
        return r, b.getvalue()
    dv = K['develop_at_draft']
    r, o = cap(clone, K['head'], dv, False); rep(r == 0, 'positive: the real head on develop %s (no remote): rc %d %s' % (dv[:12], r, [l for l in o.splitlines() if l.startswith(('FAIL', 'CHECKED'))]))
    r, o = cap(clone, K['head'], K['base'], False)
    rep(r == 0 and 'advance d784..d784b613c81e: 0 path(s)' in o, 'must-NOT-fire: develop == d784 (the READY develop, no advance): rc %d, fails %s' % (r, [l[:8] for l in o.splitlines() if l.startswith('FAIL')]))
    r, o = cap(clone, K['prev_head'], dv, False)
    fails = [l.split()[1] for l in o.splitlines() if l.startswith('FAIL ')]
    rep(r == 1 and {'P2', 'P3', 'P4', 'P7'} <= set(fails), 'CONTROL head = 79c87 (the pre-merge-in head): want FAIL P2 P3 P4 P7 | got %s' % fails)
    r, o = cap(clone, K['head'], 'f' * 40, False); rep(r == 2 and 'develop unresolvable' in o, 'REFUSES an absent develop BY NAME: %r' % o.strip()[:100])
    r, o = cap(K['checkout'], K['head'], dv, False)
    rep((r == 2 and 'develop unresolvable' in o) or r == 0, 'the shared checkout (develop %s present: %s): rc %d %r' % (dv[:12], r != 2, r, o.strip()[:100]))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A:
        c = opt('--scratch-clone')
        if not c: print('--selftest needs --scratch-clone <clone holding develop>'); raise SystemExit(2)
        raise SystemExit(selftest(c))
    raise SystemExit(main(opt('--repo', K['checkout']), opt('--head', K['head']), opt('--develop', K['develop_at_draft']), '--no-remote' not in A))
