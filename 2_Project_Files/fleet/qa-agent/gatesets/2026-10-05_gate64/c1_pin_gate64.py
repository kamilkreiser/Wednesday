#!/usr/bin/env python3
"""c1_pin_gate64.py — C1 PIN + SCOPE for #1389 (KS-1330). READ verbs only (lib_gate64.git); measures, then judges P1-P11.

  P1  origin (ONE ls-remote): refs/pull/1389/head == the kit branch == --head; develop == --develop; AND #1250 UNTOUCHED:
      refs/pull/1250/head == #1250's branch == the kit's 2b8dcb824dd2 (Q-1250: its branch/PR must not move)   (skipped with --no-remote)
  P2  EXACTLY one parent == the kit parent 0f2422925317 (NOT develop: develop advanced one commit, #1387, before the head was cut);
      the parent is an ancestor of --develop and == merge-base(head, develop)
  P3  EXACTLY the 2 kit paths, parent..head, each with the kit +/- (both ways: none extra, none missing); the three-dot develop...head
      names the same 2 paths with the same +/-
  P4  head^{tree} == kit end_tree 273ec1c0ee3a…; CONTROLS: the parent tree and the develop tree both differ
  P5  `%(trailers)` RAW bytes == 1; CONTROL bf277eead268 == 55 (else the instrument is blind)
  P6  Co-Authored-By lines in the head message == 0; CONTROL bf277eead268 carries >= 1 (same instrument)
  P7  subject == kit subject, <= 92 chars, no `(#`
  P8  ONE `Refs KS-1330` line; the ONLY hyphenated KS key in the message is KS-1330 (KS 1302 / 1303 / 1325 de-hyphenated);
      0 Linear closing words before a KS key and 0 GitHub `<kw> #n` in the message
  P9  `git ls-tree` modes == kit (both 100644, as at develop; the runner is invoked as `bash <file>`)
  P10 Kam 20:06 ruling (card secuura-pushgate-three-legs-1005 = a): NO new pre-push leg. `.githooks/pre-push` and
      `scripts/preflight/preflight.sh` blobs at head == at develop == kit; parent..head names 0 paths under .githooks/ or preflight/
  P11 develop's advance parent..develop is PATH-DISJOINT from the 2 kit paths (the Q-M precondition); its paths are printed
  INFO the stale coupling sentence in the commit message ("2 use `read` as a command head") vs the PR body's corrected 0

Usage: c1_pin_gate64.py --repo <git dir> [--head <sha>] [--develop <sha>] [--no-remote]  |  --selftest
rc 0 all PASS / rc 1 any FAIL (or 0 checked)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate64 import K, git, Tally

KEY_RX = re.compile(r'\bKS-\d+\b')
CLOSE_RX = re.compile(r'\b(close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)\b[^.\n]{0,60}?\bKS-\d+', re.I)
GHCLOSE_RX = re.compile(r'\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+', re.I)
HOOKS = list(K['hook_blobs'].keys())
P1250 = K['pr1250']


def numstat(repo, a, b):
    ns = {}
    for l in git(repo, 'diff', '--numstat', a, b).splitlines():
        x, d, p = l.split('\t', 2)
        ns[p] = [int(x), int(d)]
    return ns


def measure(repo, head, develop, remote=True):
    m = {'head': head, 'develop': develop}
    if remote:
        ls = git(repo, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/heads/' + K['branch'], 'refs/pull/%s/head' % K['pr'],
                 'refs/heads/' + P1250['branch'], 'refs/pull/%s/head' % P1250['pr'])
        refs = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
        m['ls'] = {'develop': refs.get('refs/heads/develop'), 'branch': refs.get('refs/heads/' + K['branch']),
                   'pull': refs.get('refs/pull/%s/head' % K['pr']), 'b1250': refs.get('refs/heads/' + P1250['branch']),
                   'p1250': refs.get('refs/pull/%s/head' % P1250['pr'])}
    m['parents'] = git(repo, 'log', '-1', '--format=%P', head).split()
    par = m['parents'][0] if m['parents'] else head
    m['parent_is_ancestor'] = git(repo, 'merge-base', '--is-ancestor', par, develop, check=False)[0] == 0
    m['merge_base'] = git(repo, 'merge-base', head, develop).strip()
    m['numstat'] = numstat(repo, par, head)
    m['numstat3'] = numstat(repo, m['merge_base'], head)   # == `git diff develop...head`
    m['tree'] = git(repo, 'rev-parse', head + '^{tree}').strip()
    m['parent_tree'] = git(repo, 'rev-parse', par + '^{tree}').strip()
    m['develop_tree'] = git(repo, 'rev-parse', develop + '^{tree}').strip()
    m['trailer_bytes'] = len(git(repo, 'log', '-1', '--format=%(trailers)', head).encode())
    ctl = K['trailer_control_commit']
    m['control_trailer_bytes'] = len(git(repo, 'log', '-1', '--format=%(trailers)', ctl).encode())
    m['message'] = git(repo, 'log', '-1', '--format=%B', head)
    m['control_coauthor'] = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', ctl)))
    m['subject'] = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n')
    modes = {}
    for l in git(repo, 'ls-tree', head, '--', *K['files'].keys()).splitlines():
        meta, p = l.split('\t', 1)
        modes[p] = meta.split()[0]
    m['modes'] = modes
    m['hooks_head'] = {p: git(repo, 'rev-parse', '%s:%s' % (head, p)).strip() for p in HOOKS}
    m['hooks_dev'] = {p: git(repo, 'rev-parse', '%s:%s' % (develop, p)).strip() for p in HOOKS}
    m['hook_paths_touched'] = [p for p in git(repo, 'diff', '--name-only', par, head).splitlines()
                               if p.startswith('.githooks/') or '/scripts/preflight/' in p]
    m['advance'] = git(repo, 'diff', '--name-only', par, develop).splitlines()
    return m


def judge(m, t):
    if 'ls' in m:
        L = m['ls']
        t.check('P1', L['pull'] == m['head'] and L['branch'] == m['head'] and L['develop'] == m['develop']
                and L['p1250'] == P1250['head'] and L['b1250'] == P1250['head'],
                'origin pull/%s %s | branch %s | develop %s | #1250 pull %s branch %s (want head %s, develop %s, #1250 %s)' % (
                    K['pr'], str(L['pull'])[:12], str(L['branch'])[:12], str(L['develop'])[:12], str(L['p1250'])[:12],
                    str(L['b1250'])[:12], m['head'][:12], m['develop'][:12], P1250['head'][:12]))
    else:
        t.info('P1', 'skipped (--no-remote): origin NOT read — this run proves nothing about origin or #1250')
    par = m['parents'][0] if m['parents'] else ''
    t.check('P2', m['parents'] == [K['parent']] and m['parent_is_ancestor'] and m['merge_base'] == K['parent'],
            'parents %s (want exactly [%s]); parent ancestor of develop %s; merge-base(head, develop) %s' % (
                [p[:12] for p in m['parents']], K['parent'][:12], m['parent_is_ancestor'], m['merge_base'][:12]))
    want = K['files']
    for lbl, ns in (('P3', m['numstat']), ('P3-3dot', m['numstat3'])):
        extra = sorted(set(ns) - set(want)); missing = sorted(set(want) - set(ns))
        drift = sorted(p for p in want if p in ns and ns[p] != want[p])
        t.check(lbl, not extra and not missing and not drift, '%d paths; extra %s missing %s +/- drift %s' % (
            len(ns), extra, missing, [(p, ns[p], want[p]) for p in drift]))
    t.check('P4', m['tree'] == K['end_tree'] and m['parent_tree'] != m['tree'] and m['develop_tree'] != m['tree'],
            'head tree %s (want %s); CONTROLS parent tree %s %s, develop tree %s %s' % (
                m['tree'][:12], K['end_tree'][:12], m['parent_tree'][:12], 'differs' if m['parent_tree'] != m['tree'] else 'EQUAL (blind)',
                m['develop_tree'][:12], 'differs' if m['develop_tree'] != m['tree'] else 'EQUAL (blind)'))
    t.check('P5', m['trailer_bytes'] == K['trailer_head_bytes_raw'] and m['control_trailer_bytes'] == K['trailer_control_bytes_raw'],
            '%%(trailers) raw head %d byte(s) (want %d); CONTROL %s %d (want %d)' % (
                m['trailer_bytes'], K['trailer_head_bytes_raw'], K['trailer_control_commit'], m['control_trailer_bytes'], K['trailer_control_bytes_raw']))
    co = len(re.findall(r'(?im)^co-authored-by:', m['message']))
    t.check('P6', co == 0 and m['control_coauthor'] >= 1, 'Co-Authored-By in head message %d (want 0); CONTROL %s %d (want >= 1)' % (
        co, K['trailer_control_commit'], m['control_coauthor']))
    s = m['subject']
    t.check('P7', s == K['subject'] and len(s) <= K['subject_max'] and '(#' not in s, 'subject %r, %d chars (want the kit subject, <= %d, no "(#")' % (
        s, len(s), K['subject_max']))
    refs = re.findall(r'(?m)^Refs KS-1330\s*$', m['message']); keys = sorted(set(KEY_RX.findall(m['message'])))
    closes = [x.group(0)[:80] for x in CLOSE_RX.finditer(m['message'])] + [x.group(0) for x in GHCLOSE_RX.finditer(m['message'])]
    t.check('P8', len(refs) == 1 and keys == ['KS-1330'] and not closes,
            '`Refs KS-1330` lines %d (want 1); hyphenated keys %s (want only KS-1330); closing references %s' % (len(refs), keys, closes))
    bad = {p: (m['modes'].get(p), w) for p, w in K['modes'].items() if m['modes'].get(p) != w}
    t.check('P9', not bad, 'modes %s; mismatches %s' % (m['modes'], bad))
    hb = all(m['hooks_head'][p] == m['hooks_dev'][p] == K['hook_blobs'][p] for p in HOOKS)
    t.check('P10', hb and not m['hook_paths_touched'], 'hook blobs head %s == develop %s == kit: %s; hook/preflight paths touched %s' % (
        {os.path.basename(p): v[:12] for p, v in m['hooks_head'].items()}, {os.path.basename(p): v[:12] for p, v in m['hooks_dev'].items()},
        hb, m['hook_paths_touched']))
    hit = sorted(set(m['advance']) & set(K['files']))
    t.check('P11', not hit,
            "develop's advance %s..%s: %d path(s) %s; kit paths among them %s" % (
                K['parent'][:12], m['develop'][:12], len(m['advance']), m['advance'], hit))
    stale = re.search(r'(\d+) use `read`', m['message'])
    t.info('MSG', 'commit message coupling count: %s (the PR body and READY say 0 — the message is STALE if this is not 0; '
                  'it lands only if the squash body carries it)' % (repr(stale.group(0)) if stale else 'no "N use `read`" sentence'))


def good_fixture():
    msg = 'KS-1330: x\n\nRefs KS-1330\n\nKS 1302 and KS 1303 are not closed.\n'
    adv = ['observability/.env.example', K['flow']]
    return {'head': 'a' * 40, 'develop': K['develop'],
            'ls': {'develop': K['develop'], 'branch': 'a' * 40, 'pull': 'a' * 40, 'b1250': P1250['head'], 'p1250': P1250['head']},
            'parents': [K['parent']], 'parent_is_ancestor': True, 'merge_base': K['parent'],
            'numstat': {p: list(v) for p, v in K['files'].items()}, 'numstat3': {p: list(v) for p, v in K['files'].items()},
            'tree': K['end_tree'], 'parent_tree': K['parent_tree'], 'develop_tree': K['develop_tree'],
            'trailer_bytes': 1, 'control_trailer_bytes': 55, 'message': msg, 'control_coauthor': 1, 'subject': K['subject'],
            'modes': dict(K['modes']), 'hooks_head': dict(K['hook_blobs']), 'hooks_dev': dict(K['hook_blobs']),
            'hook_paths_touched': [], 'advance': adv}


def selftest():
    import copy, io, contextlib
    arms = []
    def arm(name, mut, want): arms.append((name, mut, want))
    pp = '.githooks/pre-push'
    arm('base-as-head (develop pinned as head)', lambda m: m.update(parents=['9' * 40], numstat={}, numstat3={}, tree=K['develop_tree'], merge_base=K['develop']), ['P2', 'P3', 'P4'])
    arm('head rebased onto develop (parent == develop)', lambda m: m.update(parents=[K['develop']], merge_base=K['develop']), ['P2'])
    arm('a 3rd path (preflight.sh)', lambda m: m['numstat'].update({'Blockchain/Dev/scripts/preflight/preflight.sh': [3, 0]}), ['P3'])
    arm('+/- drift on the runner (+103/-6)', lambda m: m['numstat'].update({K['runner']: [103, 6]}), ['P3'])
    arm('a path missing (the test)', lambda m: m['numstat3'].pop(K['test']), ['P3-3dot'])
    arm('a merge-in (two parents)', lambda m: m.update(parents=[K['parent'], 'b' * 40]), ['P2'])
    arm('tree == parent tree (blind control)', lambda m: m.update(tree=K['parent_tree']), ['P4'])
    arm('a wrong END_TREE', lambda m: m.update(tree='bc8774cbe5cd409000d8f11f989dbe768050884d'), ['P4'])
    arm('a trailer on the head', lambda m: m.update(trailer_bytes=55), ['P5'])
    arm('blind trailer control', lambda m: m.update(control_trailer_bytes=1), ['P5'])
    arm('Co-Authored-By in the body', lambda m: m.update(message=m['message'] + 'Co-Authored-By: X <x@y>\n'), ['P6'])
    arm('blind co-author control', lambda m: m.update(control_coauthor=0), ['P6'])
    arm('subject carries (#1389)', lambda m: m.update(subject=K['subject'] + ' (#1389)'), ['P7'])
    arm('subject 93 chars', lambda m: m.update(subject='K' * 93), ['P7'])
    arm('a second Refs line', lambda m: m.update(message=m['message'] + 'Refs KS-1330\n'), ['P8'])
    arm('KS-1302 hyphenated', lambda m: m.update(message=m['message'].replace('KS 1302', 'KS-1302')), ['P8'])
    arm('"does not close KS-1330" (negation still closes)', lambda m: m.update(message=m['message'] + 'This does not close KS-1330.\n'), ['P8'])
    arm('runner at 100755', lambda m: m['modes'].update({K['runner']: '100755'}), ['P9'])
    arm('pre-push blob changed at head', lambda m: m['hooks_head'].update({pp: 'e' * 40}), ['P10'])
    arm('a preflight path touched', lambda m: m.update(hook_paths_touched=['Blockchain/Dev/scripts/preflight/preflight.sh']), ['P10'])
    arm("develop's advance touches the runner", lambda m: m['advance'].append(K['runner']), ['P11'])
    arm('origin develop moved', lambda m: m['ls'].update(develop='c' * 40), ['P1'])
    arm('origin pull/1389/head moved', lambda m: m['ls'].update(pull='d' * 40), ['P1'])
    arm('#1250 branch MOVED', lambda m: m['ls'].update(b1250='f' * 40), ['P1'])
    def run(m):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(m, t)
        return t
    t0 = run(good_fixture()); n0 = t0.n
    ok = int(not t0.fails and n0 == 12); total = 1
    print('SELFTEST %s T0 positive control (good fixture): %d checked, fails %s' % ('OK' if ok else 'MISS', n0, t0.fails))
    for name, mut, want in arms:
        m = copy.deepcopy(good_fixture()); mut(m); t = run(m); total += 1
        g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s: want FAIL %s | got FAIL %s' % ('OK' if g else 'MISS', name, want, t.fails))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo')
    if not repo: raise SystemExit('usage: c1_pin_gate64.py --repo <git dir> [--head <sha>] [--develop <sha>] [--no-remote] | --selftest')
    head = opt('--head', K['head']); dev = opt('--develop', K['develop'])
    print('c1_pin_gate64 repo %s head %s develop %s remote %s' % (repo, head, dev, '--no-remote' not in A))
    t = Tally(); judge(measure(repo, head, dev, remote='--no-remote' not in A), t); raise SystemExit(t.end())
