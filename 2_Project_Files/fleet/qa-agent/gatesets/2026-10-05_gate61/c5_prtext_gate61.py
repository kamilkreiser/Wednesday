#!/usr/bin/env python3
"""c5_prtext_gate61.py — gate61 C5 PR TEXT for #1383 (KS-1401): the PR title + body (GitHub PULLS API, read-only; or --body-file / --title
for a replay) and the head commit message (YOUR scratch clone).
  T1 REFS         exactly ONE `Refs KS-1401` line, 0 other `Refs` lines, and the ticket URL (kit pr_text.url) in the body.
  T2 NO CLOSING   0 closing magic words (close/closes/closed/closing, fix…, resolve…, complete…) followed by KS-1401 or #n, in title, body
                  and commit message. Linear's integration does NOT read negation: "does not close KS-1401" is a closing reference.
                  The drafter's read FAILS this on the real body (README D1).
  T3 OWN KEY      the ONLY hyphenated KS key across title, body and commit message is KS-1401 (KS 1376, KS 1054, KS 4 de-hyphenated).
  T4 TITLE        title == kit squash_subject_declared byte-for-byte, <= 92, no `(#`.
  T5 TEST EVIDENCE a `## Test Evidence` heading.
  T6 NEVER DEMO   the body says 049 never reaches demo (kit never_demo_rx) AND that it lands with the kintsugi deploy (kintsugi_only_rx).
  T7 FIGURES      the body's figures == the kit's (53 passed / 0 failed, 11 cells, 100755, block `22.`, PostgreSQL 15.14) — C3 measures them.
  T8 NOT COVERED  a not-covered section exists and names the live sweep AND the live apply owed (C6 reads the section in full).
  INFO the body's byte / character counts and sha256 against kit pr_body_read (a changed body is printed as BODY CHANGED SINCE DRAFTING).
--selftest  T0 a SYNTHETIC positive control (the real body with its one closing phrase neutralised: the REAL body is reported, not used,
            because it fails T2) PASSES; planted copies each FAIL their named check.
Usage: c5_prtext_gate61.py --repo <clone> [--pr 1383] [--body-file f --title t] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage
Prints `CHECKED <n>`; 0 checked is a FAIL."""
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, git, now, Checks, opt_factory, has_commit, GH, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); PR = opt('--pr', K['pr']); X = K['pr_text']
if not has_commit(REPO, K['head']): print('REFUSING: %s not in %s' % (K['head'][:12], REPO)); raise SystemExit(2)
if opt('--body-file'):
    BODY = open(opt('--body-file'), encoding='utf-8').read(); TITLE = opt('--title', K['squash_subject_declared']); SRC = 'REPLAY %s' % opt('--body-file')
else:
    p = GH().get('pulls/' + PR); BODY = p.get('body') or ''; TITLE = p['title']; SRC = 'API pulls/%s' % PR
MSG = git(REPO, 'log', '-1', '--format=%B', K['head'])
NC_RX = K['not_covered_heading_rx']


def section(body):
    hs = list(re.finditer(NC_RX, body))
    if len(hs) != 1: return None
    rest = body[hs[0].end():]; m = re.search(r'(?m)^## ', rest)
    return rest[:m.start()] if m else rest


def judge(C, body, title, msg):
    own = re.findall(X['refs_line_rx'], body); refs = re.findall(X['any_refs_rx'], body)
    C.chk('T1 refs', len(own) == 1 and len(refs) == 1 and X['url'] in body, '`Refs KS-1401` lines %d | all Refs lines %s | ticket URL present %s' % (len(own), refs, X['url'] in body))
    cl = [(n, m.group(0)) for n, t in (('title', title), ('body', body), ('commit msg', msg)) for m in re.finditer(X['closing_rx'], t)]
    C.chk('T2 no closing magic word', not cl, 'closing references %s' % (cl or 'NONE'))
    for n, m in cl:
        i = body.find(m) if n == 'body' else -1
        print('INFO T2 %s: ...%s...' % (n, ' '.join(body[max(0, i - 60):i + 80].split()) if i >= 0 else m))
    keys = sorted(set(k for t in (title, body, msg) for k in re.findall(r'\bKS-\d+\b', t)))
    C.chk('T3 own key only', keys == [X['own_key']], 'hyphenated keys %s (want [%s]) | de-hyphenated in the body %s' % (keys, X['own_key'], sorted(set(re.findall(r'\bKS \d+\w?\b', body))) or 'NONE'))
    d = K['squash_subject_declared']
    C.chk('T4 title == declared subject', title == d and len(title) <= K['subject_max'] and '(#' not in title, 'title %r (%d chars) | declared %r' % (title, len(title), d))
    C.chk('T5 Test Evidence', re.search(X['test_evidence_rx'], body) is not None, '`## Test Evidence` heading present: %s' % (re.search(X['test_evidence_rx'], body) is not None))
    nd = re.search(X['never_demo_rx'], body); ko = re.search(X['kintsugi_only_rx'], body)
    C.chk('T6 never demo', nd is not None and ko is not None, 'never-demo sentence %r | kintsugi deploy named %s' % (nd.group(0) if nd else None, ko is not None))
    fg = {k: v in body for k, v in X['figures'].items()}
    C.chk('T7 figures == kit', all(fg.values()), ' | '.join('%s: %s' % kv for kv in fg.items()))
    sec = section(body); ls_ = bool(sec and re.search(K['not_covered_required']['live_sweep_5f'], sec)); la = bool(sec and re.search(K['not_covered_required']['live_apply_owed'], sec))
    C.chk('T8 not covered: live apply + live sweep owed', sec is not None and ls_ and la, 'section present %s | live sweep named %s | live apply / apply round named %s' % (sec is not None, ls_, la))


print('c5_prtext_gate61 %s | %s | clone %s' % (now(), SRC, REPO))
b8 = BODY.encode('utf-8'); sh = hashlib.sha256(b8).hexdigest(); pb = K['pr_body_read']
print('INFO body %d bytes / %d characters, sha256 %s%s | title %r' % (len(b8), len(BODY), sh, '' if sh == pb['sha256'] else ' — BODY CHANGED SINCE DRAFTING (kit %s)' % pb['sha256'][:16], TITLE))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    CLEAN = re.sub(X['closing_rx'], lambda m: 'does-not-move ' + m.group(m.lastindex), BODY)
    print('INFO SYNTHETIC positive control: the real body with %d closing phrase(s) neutralised' % len(re.findall(X['closing_rx'], BODY)))
    def pl(old, new, src=None):
        s = CLEAN if src is None else src
        assert s.count(old) >= 1, 'plant anchor absent: %r' % old[:60]
        return s.replace(old, new, 1)
    J = lambda b, t=None, m=None: (lambda C: judge(C, b, TITLE if t is None else t, MSG if m is None else m))
    selftest_arm(st, 'T0 the SYNTHETIC clean body (positive control)', J(CLEAN), None)
    selftest_arm(st, 'T0r the REAL body (reported: the drafter predicts T2 fails)', J(BODY), 'T2' if re.search(X['closing_rx'], BODY) else None)
    selftest_arm(st, 'T1 the Refs line removed', J(pl('Refs KS-1401', 'Ticket: see link')), 'T1')
    selftest_arm(st, 'T1b a second Refs line', J(CLEAN + '\nRefs KS 1376\n'), 'T1')
    selftest_arm(st, 'T2 `Closes KS-1401` appended', J(CLEAN + '\nCloses KS-1401\n'), 'T2')
    selftest_arm(st, 'T2b `fixes #1383` in the commit message', J(CLEAN, m=MSG + '\nfixes #1383\n'), 'T2')
    selftest_arm(st, 'T3 KS 1376 hyphenated', J(pl('KS 1376', 'KS-1376')), 'T3')
    selftest_arm(st, 'T4 title with (#1383)', J(CLEAN, t=TITLE + ' (#1383)'), 'T4')
    selftest_arm(st, 'T5 Test Evidence heading removed', J(re.sub(X['test_evidence_rx'], '## Evidence', CLEAN)), 'T5')
    selftest_arm(st, 'T6 the never-demo sentence removed', J(re.sub(X['never_demo_rx'], 'reaches', CLEAN)), 'T6')
    selftest_arm(st, 'T7 a figure drifted (52 passed)', J(CLEAN.replace(X['figures']['53 passed'], '52 passed, 1 failed')), 'T7')
    selftest_arm(st, 'T8 the not-covered heading removed', J(re.sub(NC_RX, '## Leftovers', CLEAN)), 'T8')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)
C = Checks(); judge(C, BODY, TITLE, MSG); n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C5 PR TEXT %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 and C.res else 'FAIL', n, len(C.res), PR))
raise SystemExit(1 if n or not C.res else 0)
