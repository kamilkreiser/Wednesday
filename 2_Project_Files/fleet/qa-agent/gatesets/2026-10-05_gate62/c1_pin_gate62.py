#!/usr/bin/env python3
"""c1_pin_gate62.py — C1 PIN for #1387 (KS-1388 s1). READ verbs only (lib_gate62.git); measures, then judges P1-P9.

  P1  origin (ls-remote, ONE read): refs/pull/1387/head == the kit branch == --head; develop == --develop      (skipped with --no-remote)
  P2  EXACTLY one parent, == --develop (single-parent head, no merge-in)
  P3  EXACTLY the 5 kit paths, each with the kit +/- by `git diff --numstat develop head` (both ways: no extra, none missing)
  P4  head^{tree} == kit end_tree; CONTROL develop^{tree} differs; the tree is NOT the fabricated 0c0f8e5e… of the first READY
  P5  `%(trailers)` RAW bytes == 1 (the bare newline); CONTROL bf277eead268 raw bytes == 55 (else the instrument is blind)
  P6  Co-Authored-By lines in the head message == 0; CONTROL bf277eead268 carries >= 1 (case-insensitive, same instrument)
  P7  subject == kit subject, <= 92 chars, no `(#`
  P8  ONE `Refs KS-1388`; the ONLY hyphenated KS key in the message is KS-1388 (others de-hyphenated)
  P9  `git ls-tree` modes == kit (the test 100755; core.filemode is false in the checkout, so never ls -l)

Usage: c1_pin_gate62.py --repo <git dir> [--head <sha>] [--develop <sha>] [--no-remote]  |  --selftest
rc 0 all PASS / rc 1 any FAIL (or 0 checked)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate62 import K, git, Tally

KEY_RX = re.compile(r'\bKS-\d+\b')


def measure(repo, head, develop, remote=True):
    m = {'head': head, 'develop': develop}
    if remote:
        ls = git(repo, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/heads/' + K['branch'], 'refs/pull/%s/head' % K['pr'])
        refs = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
        m['ls'] = {'develop': refs.get('refs/heads/develop'), 'branch': refs.get('refs/heads/' + K['branch']),
                   'pull': refs.get('refs/pull/%s/head' % K['pr'])}
    m['parents'] = git(repo, 'log', '-1', '--format=%P', head).split()
    ns = {}
    for l in git(repo, 'diff', '--numstat', develop, head).splitlines():
        a, d, p = l.split('\t', 2)
        ns[p] = [int(a), int(d)]
    m['numstat'] = ns
    m['tree'] = git(repo, 'rev-parse', head + '^{tree}').strip()
    m['develop_tree'] = git(repo, 'rev-parse', develop + '^{tree}').strip()
    m['trailer_bytes'] = len(git(repo, 'log', '-1', '--format=%(trailers)', head).encode())
    ctl = K['trailer_control_commit']
    m['control_trailer_bytes'] = len(git(repo, 'log', '-1', '--format=%(trailers)', ctl).encode())
    msg = git(repo, 'log', '-1', '--format=%B', head)
    m['message'] = msg
    m['control_coauthor'] = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', ctl)))
    m['subject'] = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n')
    modes = {}
    for l in git(repo, 'ls-tree', head, '--', *K['files'].keys()).splitlines():
        meta, p = l.split('\t', 1)
        modes[p] = meta.split()[0]
    m['modes'] = modes
    return m


def judge(m, t):
    if 'ls' in m:
        t.check('P1', m['ls']['pull'] == m['head'] and m['ls']['branch'] == m['head'] and m['ls']['develop'] == m['develop'],
                'origin pull/%s %s | branch %s | develop %s (want head %s, develop %s)' % (
                    K['pr'], str(m['ls']['pull'])[:12], str(m['ls']['branch'])[:12], str(m['ls']['develop'])[:12], m['head'][:12], m['develop'][:12]))
    else:
        t.info('P1', 'skipped (--no-remote): origin NOT read — this run proves nothing about origin')
    t.check('P2', m['parents'] == [m['develop']], 'parents %s (want exactly [%s])' % ([p[:12] for p in m['parents']], m['develop'][:12]))
    want = {p: v for p, v in K['files'].items()}
    extra = sorted(set(m['numstat']) - set(want)); missing = sorted(set(want) - set(m['numstat']))
    drift = sorted(p for p in want if p in m['numstat'] and m['numstat'][p] != want[p])
    t.check('P3', not extra and not missing and not drift, '%d paths; extra %s missing %s +/- drift %s' % (
        len(m['numstat']), extra, missing, [(p, m['numstat'][p], want[p]) for p in drift]))
    t.check('P4', m['tree'] == K['end_tree'] and m['develop_tree'] != m['tree'] and not m['tree'].startswith(K['fabricated_tree_prefix']),
            'head tree %s (want %s); CONTROL develop tree %s %s; fabricated prefix %s %s' % (
                m['tree'][:12], K['end_tree'][:12], m['develop_tree'][:12], 'differs' if m['develop_tree'] != m['tree'] else 'EQUAL (control blind)',
                K['fabricated_tree_prefix'], 'absent' if not m['tree'].startswith(K['fabricated_tree_prefix']) else 'PRESENT'))
    t.check('P5', m['trailer_bytes'] == K['trailer_head_bytes_raw'] and m['control_trailer_bytes'] == K['trailer_control_bytes_raw'],
            '%%(trailers) raw head %d byte(s) (want %d); CONTROL %s %d (want %d)' % (
                m['trailer_bytes'], K['trailer_head_bytes_raw'], K['trailer_control_commit'], m['control_trailer_bytes'], K['trailer_control_bytes_raw']))
    co = len(re.findall(r'(?im)^co-authored-by:', m['message']))
    t.check('P6', co == 0 and m['control_coauthor'] >= 1, 'Co-Authored-By in head message %d (want 0); CONTROL %s %d (want >= 1)' % (
        co, K['trailer_control_commit'], m['control_coauthor']))
    s = m['subject']
    t.check('P7', s == K['subject'] and len(s) <= K['subject_max'] and '(#' not in s, 'subject %r, %d chars (want the kit subject, <= %d, no "(#")' % (
        s, len(s), K['subject_max']))
    refs = re.findall(r'(?m)^Refs KS-1388\s*$', m['message']); keys = sorted(set(KEY_RX.findall(m['message'])))
    t.check('P8', len(refs) == 1 and keys == ['KS-1388'], '`Refs KS-1388` lines %d (want 1); hyphenated keys %s (want only KS-1388)' % (len(refs), keys))
    bad = {p: (m['modes'].get(p), w) for p, w in K['modes'].items() if m['modes'].get(p) != w}
    t.check('P9', not bad, 'modes %s; mismatches %s' % (m['modes'], bad))


def good_fixture():
    msg = 'KS-1388: x\n\nKS 971 is fine.\n\nRefs KS-1388\n'
    return {'head': 'a' * 40, 'develop': K['develop'],
            'ls': {'develop': K['develop'], 'branch': 'a' * 40, 'pull': 'a' * 40},
            'parents': [K['develop']], 'numstat': {p: list(v) for p, v in K['files'].items()}, 'tree': K['end_tree'],
            'develop_tree': K['develop_tree'], 'trailer_bytes': 1, 'control_trailer_bytes': 55, 'message': msg,
            'control_coauthor': 1, 'subject': K['subject'], 'modes': dict(K['modes'])}


def selftest():
    import copy
    arms = []
    def arm(name, mut, want):
        arms.append((name, mut, want))
    arm('base-as-head (develop pinned as head)', lambda m: m.update(parents=['9' * 40], numstat={}, tree=K['develop_tree']), ['P2', 'P3', 'P4'])
    arm('a 6th path', lambda m: m['numstat'].update({'observability/docker-compose.yml': [1, 1]}), ['P3'])
    arm('+/- drift on the cheat sheet (+35/-3)', lambda m: m['numstat'].update({K['cheat']: [35, 3]}), ['P3'])
    arm('a path missing', lambda m: m['numstat'].pop(K['test']), ['P3'])
    arm('a merge-in (two parents)', lambda m: m.update(parents=[K['develop'], 'b' * 40]), ['P2'])
    arm('the FABRICATED tree 0c0f8e5e', lambda m: m.update(tree='0c0f8e5e' + 'f' * 32), ['P4'])
    arm('tree == develop tree (blind control)', lambda m: m.update(tree=K['develop_tree']), ['P4'])
    arm('a trailer on the head', lambda m: m.update(trailer_bytes=55), ['P5'])
    arm('blind trailer control (0 bytes)', lambda m: m.update(control_trailer_bytes=1), ['P5'])
    arm('Co-Authored-By in the body', lambda m: m.update(message=m['message'] + 'Co-Authored-By: X <x@y>\n'), ['P6'])
    arm('blind co-author control', lambda m: m.update(control_coauthor=0), ['P6'])
    arm('subject carries (#1387)', lambda m: m.update(subject=K['subject'] + ' (#1387)'), ['P7'])
    arm('subject 93 chars', lambda m: m.update(subject='K' * 93), ['P7'])
    arm('a second Refs line', lambda m: m.update(message=m['message'] + 'Refs KS-1388\n'), ['P8'])
    arm('KS-971 hyphenated', lambda m: m.update(message=m['message'].replace('KS 971', 'KS-971')), ['P8'])
    arm('test file at 100644', lambda m: m['modes'].update({K['test']: '100644'}), ['P9'])
    arm('origin develop moved', lambda m: m['ls'].update(develop='c' * 40), ['P1'])
    arm('origin pull/head moved', lambda m: m['ls'].update(pull='d' * 40), ['P1'])
    import io, contextlib
    def run(m):
        t = Tally(); buf = io.StringIO()
        with contextlib.redirect_stdout(buf): judge(m, t)
        return t
    t0 = run(good_fixture())
    ok = 0; total = 1
    print('SELFTEST %s T0 positive control (good fixture): %d checked, fails %s' % ('OK' if not t0.fails and t0.n == 9 else 'MISS', t0.n, t0.fails))
    ok += (not t0.fails and t0.n == 9)
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
    if not repo: raise SystemExit('usage: c1_pin_gate62.py --repo <git dir> [--head <sha>] [--develop <sha>] [--no-remote] | --selftest')
    head = opt('--head', K['head']); dev = opt('--develop', K['develop'])
    print('c1_pin_gate62 repo %s head %s develop %s remote %s' % (repo, head, dev, '--no-remote' not in A))
    t = Tally(); judge(measure(repo, head, dev, remote='--no-remote' not in A), t); raise SystemExit(t.end())
