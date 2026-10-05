#!/usr/bin/env python3
"""c5_prtext_gate59.py — gate59 C5 PR TEXT for #1382 (KS-1005): the PR title + body (GitHub PULLS API, read-only; or --body-file /
--title for a replay) and the two commit messages (built 4346bc7fbdf8, merge-in head) in YOUR scratch clone.
  T1 REFS        the body carries a line starting `Refs KS-1005` and the ticket URL (kit pr_text.url); the BUILT commit message has a
                 `Refs KS-1005` line (it is what the squash body will carry).
  T2 NO CLOSING  0 closing keywords (close/fix/resolve + KS-1005 or #n) in title, body, both commit messages (§5f: the ticket never
                 moves to Done on offline green).
  T3 OWN KEY     the ONLY hyphenated KS key in title, body and both commit messages is KS-1005 (foreign keys de-hyphenated: KS 749,
                 KS 1333 ...).
  T4 TITLE       the PR title == kit squash_subject_declared byte-for-byte (<= 92, no `(#`).
  T5 METHOD      the body states WHO ran WHAT: a by-this-seat list, a by-the-previous-seat list marked NOT re-run, and a NOT run list.
  T6 CLAIMS      the body's head sha, END_TREE, both parents, "exactly four paths", "0 trailers" all == kit (C1 measured them).
  INFO the body's byte and character counts and sha256 (the READY quotes none).
--selftest  T0 the REAL body PASSES; planted bodies each FAIL their named check: Refs line removed (T1), `Closes KS-1005` (T2), `KS-1210`
            hyphenated (T3), title `... (#1382)` (T4), the previous-seat attribution removed (T5), the head sha altered (T6).
Usage: c5_prtext_gate59.py --repo <clone> [--pr 1382] [--body-file f --title t] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage"""
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, git, now, Checks, opt_factory, has_commit, GH, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); PR = opt('--pr', K['pr']); X = K['pr_text']
for s in (K['head'], K['built']):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
if opt('--body-file'):
    BODY = open(opt('--body-file'), encoding='utf-8').read(); TITLE = opt('--title', K['squash_subject_declared']); SRC = 'REPLAY %s' % opt('--body-file')
else:
    p = GH().get('pulls/' + PR); BODY = p.get('body') or ''; TITLE = p['title']; SRC = 'API pulls/%s' % PR
MB = git(REPO, 'log', '-1', '--format=%B', K['built']); MH = git(REPO, 'log', '-1', '--format=%B', K['head'])


def judge(C, body, title, mb, mh):
    C.chk('T1 refs', re.search(X['refs_line_rx'], body) is not None and X['url'] in body and re.search(r'(?m)^Refs KS-1005\s*$', mb) is not None,
          'body `Refs KS-1005` line: %s | ticket URL: %s | built commit `Refs KS-1005` line: %s' % (re.search(X['refs_line_rx'], body) is not None, X['url'] in body, re.search(r'(?m)^Refs KS-1005\s*$', mb) is not None))
    cl = [(n, m.group(0)) for n, t in (('title', title), ('body', body), ('built msg', mb), ('merge msg', mh)) for m in re.finditer(X['closing_rx'], t)]
    C.chk('T2 no closing keyword', not cl, 'closing keywords %s' % (cl or 'NONE'))
    keys = sorted(set(k for t in (title, body, mb, mh) for k in re.findall(r'\bKS-\d+\b', t)))
    C.chk('T3 own key only', keys == [X['own_key']], 'hyphenated KS keys across title / body / both commit messages: %s (want [%s]) | de-hyphenated foreign keys in the body: %s' % (
        keys, X['own_key'], sorted(set(re.findall(r'\bKS \d+\b', body))) or 'NONE'))
    d = K['squash_subject_declared']
    C.chk('T4 title == declared subject', title == d and len(title) <= K['subject_max'] and '(#' not in title, 'title %r (%d chars) | declared %r' % (title, len(title), d))
    m = {'by this seat': bool(re.search(r'(?i)ran \(by me', body)), 'previous seat, NOT re-run': bool(re.search(r'(?i)previous seat', body) and re.search(r'(?i)not re-run', body)),
         'a NOT run list': bool(re.search(r'(?m)^\*\*NOT run:?\*\*|^NOT run', body))}
    C.chk('T5 method stated', all(m.values()), ' | '.join('%s: %s' % kv for kv in m.items()))
    cl6 = {'head sha': K['head'] in body, 'END_TREE': K['end_tree'] in body, 'built parent': K['built'][:12] in body, 'develop parent': K['develop'][:12] in body,
           'exactly four paths': bool(re.search(r'(?i)exactly four paths', body)), '0 trailers': bool(re.search(r'0 trailers', body))}
    C.chk('T6 claims == kit', all(cl6.values()), ' | '.join('%s: %s' % kv for kv in cl6.items()))


print('c5_prtext_gate59 %s | %s | clone %s' % (now(), SRC, REPO))
b8 = BODY.encode('utf-8')
print('INFO body %d bytes / %d characters, sha256 %s | title %r' % (len(b8), len(BODY), hashlib.sha256(b8).hexdigest(), TITLE))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    def pl(old, new, src=None):
        s = BODY if src is None else src
        assert s.count(old) >= 1, 'plant anchor absent: %r' % old[:60]
        return s.replace(old, new, 1)
    selftest_arm(st, 'T0 the REAL body (positive control)', lambda C: judge(C, BODY, TITLE, MB, MH), None)
    selftest_arm(st, 'T1 the Refs line removed', lambda C: judge(C, pl('Refs KS-1005 —', 'Ticket:'), TITLE, MB, MH), 'T1')
    selftest_arm(st, 'T2 `Closes KS-1005` added', lambda C: judge(C, BODY + '\nCloses KS-1005\n', TITLE, MB, MH), 'T2')
    selftest_arm(st, 'T3 KS-1210 hyphenated', lambda C: judge(C, BODY + '\nSee also KS-1210.\n', TITLE, MB, MH), 'T3')
    selftest_arm(st, 'T4 title with (#1382)', lambda C: judge(C, BODY, TITLE + ' (#1382)', MB, MH), 'T4')
    selftest_arm(st, 'T5 previous-seat attribution removed', lambda C: judge(C, re.sub(r'(?i)previous seat', 'team', BODY), TITLE, MB, MH), 'T5')
    selftest_arm(st, 'T6 the head sha altered', lambda C: judge(C, BODY.replace(K['head'], K['head'][:-1] + ('0' if K['head'][-1] != '0' else '1')), TITLE, MB, MH), 'T6')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, BODY, TITLE, MB, MH); n = C.nfail()
print('C5 PR TEXT %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR))
raise SystemExit(1 if n else 0)
