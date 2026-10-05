#!/usr/bin/env python3
"""c5_prtext_gate60.py — gate60 C5 PR TEXT for #1384 (KS-1210): the PR title + body (GitHub PULLS API, read-only; or --body-file / --title for
a replay) and the head commit message in YOUR scratch clone.
  T1 REFS        the body carries a line `Refs KS-1210` and the ticket URL; the head commit message has its `Refs KS-1210` line.
  T2 NO CLOSING  0 closing keywords (close/fix/resolve + KS-1210 or #n) in title, body, commit message (§5f: never Done on offline green).
  T3 OWN KEY     the ONLY hyphenated KS key in title, body and commit message is KS-1210 (KS 855 / KS 451 / KS 431 de-hyphenated).
  T4 TITLE       the PR title == kit squash_subject_declared byte-for-byte (<= 92, no `(#`).
  T5 METHOD      who ran what: a "Run by me (Seat E 3rd)" statement, a "NOT run" list, and red-first attributed to the seat that BUILT it.
  T6 CLAIMS      the body's head sha, base 46c3e20cfbd2, AVAILABLE_SCOPES blob 8995edec6a43, auth.openapi.ts blob 2c356c3c7877, the ks949
                 blob 4f03e6f4f132, oauth.ts 3ae75ea1351a -> 72819e0e7622 all == the kit (C1 / C2 / C3 measure them).
  T7 RULINGS     Q-1210 as ruled: the nine, {admin:read, admin:write} platform-only (403), owner-or-admin 404 on the four by-id routes,
                 certifications:write + webhooks:manage NOT privileged, the KS 855 coupling.
  T8 BEYOND      behaviour changes BEYOND the ticket are stated: the DELETE of an id that does not exist now answers 404 (was 200). The
                 product comment in routes/oauth.ts (the DELETE handler) says this is "stated in the PR body" — the drafter's read FAILS it.
  INFO           the six destructive scopes the brief asked the body to NAME (subjects:erase, documents:revoke, documents:delete,
                 certifications:revoke, certifications:delete, issuer-certs:revoke) — named or only counted; byte / char counts + sha256.
--selftest  BASELINE-AWARE (T8 fails at the real body): T0 the REAL body passes everything else; planted bodies each FAIL their named check:
            Refs line removed (T1), `Closes KS-1210` (T2), `KS-855` hyphenated (T3), title `… (#1384)` (T4), "Run by me" removed (T5),
            the head sha altered (T6), the webhooks:manage ruling removed (T7); and a planted DELETE-404 sentence makes T8 PASS (its control).
Usage: c5_prtext_gate60.py --repo <clone> [--pr 1384] [--body-file f --title t] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage"""
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, git, now, Checks, opt_factory, has_commit, GH, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); PR = opt('--pr', K['pr']); X = K['pr_text']
if not has_commit(REPO, K['head']): print('REFUSING: %s not in %s' % (K['head'][:12], REPO)); raise SystemExit(2)
if opt('--body-file'):
    BODY = open(opt('--body-file'), encoding='utf-8').read(); TITLE = opt('--title', K['squash_subject_declared']); SRC = 'REPLAY %s' % opt('--body-file')
else:
    p = GH().get('pulls/' + PR); BODY = p.get('body') or ''; TITLE = p['title']; SRC = 'API pulls/%s' % PR
MH = git(REPO, 'log', '-1', '--format=%B', K['head'])
SIX = ['subjects:erase', 'documents:revoke', 'documents:delete', 'certifications:revoke', 'certifications:delete', 'issuer-certs:revoke']


def judge(C, body, title, mh):
    C.chk('T1 refs', re.search(X['refs_line_rx'], body) is not None and X['url'] in body and re.search(r'(?m)^Refs KS-1210\s*$', mh) is not None,
          'body `Refs KS-1210` line: %s | ticket URL: %s | commit `Refs KS-1210` line: %s' % (re.search(X['refs_line_rx'], body) is not None, X['url'] in body, re.search(r'(?m)^Refs KS-1210\s*$', mh) is not None))
    cl = [(n, m.group(0)) for n, t in (('title', title), ('body', body), ('commit msg', mh)) for m in re.finditer(X['closing_rx'], t)]
    C.chk('T2 no closing keyword', not cl, 'closing keywords %s' % (cl or 'NONE'))
    keys = sorted(set(k for t in (title, body, mh) for k in re.findall(r'\bKS-\d+\b', t)))
    C.chk('T3 own key only', keys == [X['own_key']], 'hyphenated KS keys across title / body / commit message: %s (want [%s]) | de-hyphenated in the body: %s' % (
        keys, X['own_key'], sorted(set(re.findall(r'\bKS \d+\b', body))) or 'NONE'))
    d = K['squash_subject_declared']
    C.chk('T4 title == declared subject', title == d and len(title) <= K['subject_max'] and '(#' not in title, 'title %r (%d chars) | declared %r' % (title, len(title), d))
    m = {'run by me (Seat E 3rd)': bool(re.search(r'(?i)run by me \(Seat E 3rd\)', body)), 'a NOT run list': bool(re.search(r'(?m)^\*\*NOT run:?\*\*|^NOT run', body)),
         'red-first attributed to the building seat': bool(re.search(r'(?i)red-first.{0,200}(seat that built it|that seat\'s)', body, re.S))}
    C.chk('T5 method stated', all(m.values()), ' | '.join('%s: %s' % kv for kv in m.items()))
    c6 = {'head sha': K['head'] in body, 'base 46c3e20cfbd2': K['develop'][:12] in body, 'AVAILABLE_SCOPES blob 8995edec6a43': '8995edec6a43' in body,
          'auth.openapi.ts blob 2c356c3c7877': '2c356c3c7877' in body, 'ks949 blob 4f03e6f4f132': '4f03e6f4f132' in body, 'oauth.ts 3ae75ea1351a -> 72819e0e7622': '3ae75ea1351a' in body and '72819e0e7622' in body}
    C.chk('T6 claims == kit', all(c6.values()), ' | '.join('%s: %s' % kv for kv in c6.items()))
    r = {'the nine': bool(re.search(r'(?i)\bnine\b', body)), 'admin pair platform-only 403': '{admin:read, admin:write}' in body and '403' in body,
         'owner-or-admin 404 on the four by-id routes': bool(re.search(r'(?i)four by-id routes', body)) and '404' in body,
         'certifications:write + webhooks:manage NOT privileged': 'certifications:write' in body and 'webhooks:manage' in body and bool(re.search(r'(?i)\bnot\*?\*?\s*privileged', body)),
         'KS 855 coupling': 'KS 855' in body}
    C.chk('T7 rulings stated', all(r.values()), ' | '.join('%s: %s' % kv for kv in r.items()))
    b8 = bool(re.search(r'(?i)(does not exist|non-?existent|missing).{0,160}(DELETE|delete)|(DELETE|delete).{0,200}(does not exist|non-?existent).{0,120}404', body, re.S))
    C.chk('T8 behaviour beyond the ticket stated', b8, 'the body states that DELETE of an id that does not exist now answers 404 (was 200): %s — routes/oauth.ts\'s DELETE comment says it is "stated in the PR body"' % b8)
    print('INFO the six destructive scopes the brief asked the body to name: named %s of 6 (%s) | "six destructive scopes" counted: %s' % (
        sum(s in body for s in SIX), [s for s in SIX if s in body] or 'NONE', bool(re.search(r'(?i)six destructive scopes', body))))


print('c5_prtext_gate60 %s | %s | clone %s' % (now(), SRC, REPO))
b8 = BODY.encode('utf-8')
print('INFO body %d bytes / %d characters, sha256 %s (kit pr_body_read %s) | title %r' % (len(b8), len(BODY), hashlib.sha256(b8).hexdigest(), K['pr_body_read']['sha256'][:16], TITLE))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    Cb = Checks(True); judge(Cb, BODY, TITLE, MH); BASE = set(Cb.failed())
    print('SELFTEST BASELINE: the real body fails %s — an arm counts only a NEW failure of its named check' % (sorted(BASE) or 'NOTHING'))
    def pl(old, new):
        assert BODY.count(old) >= 1, 'plant anchor absent: %r' % old[:60]
        return BODY.replace(old, new, 1)
    def narm(name, fn, want):
        def wrapped(C):
            C2 = Checks(True); fn(C2)
            for tag, ok in C2.tags: C.chk(tag, ok or tag in BASE, '(baseline-aware)')
        return selftest_arm(st, name, wrapped, want)
    narm('T0 the REAL body, baseline-aware (positive control)', lambda C: judge(C, BODY, TITLE, MH), None)
    narm('T1 the Refs line removed', lambda C: judge(C, pl('Refs KS-1210\n', 'Ticket:\n'), TITLE, MH), 'T1')
    narm('T2 `Closes KS-1210` added', lambda C: judge(C, BODY + '\nCloses KS-1210\n', TITLE, MH), 'T2')
    narm('T3 KS-855 hyphenated', lambda C: judge(C, pl('## Relationship to KS 855', '## Relationship to KS-855'), TITLE, MH), 'T3')
    narm('T4 title with (#1384)', lambda C: judge(C, BODY, TITLE + ' (#1384)', MH), 'T4')
    narm('T5 "Run by me" removed', lambda C: judge(C, pl('Run by me (Seat E 3rd)', 'Run'), TITLE, MH), 'T5')
    narm('T6 the head sha altered', lambda C: judge(C, BODY.replace(K['head'], K['head'][:-1] + ('0' if K['head'][-1] != '0' else '1')), TITLE, MH), 'T6')
    narm('T7 the webhooks:manage ruling removed', lambda C: judge(C, BODY.replace('webhooks:manage', 'webhooks'), TITLE, MH), 'T7')
    def t8c(C):
        Cx = Checks(True); judge(Cx, BODY + '\nA DELETE of an id that does not exist now answers 404 (it answered 200).\n', TITLE, MH)
        for t, ok in Cx.tags:
            if t.startswith('T8'): C.chk(t, ok, '(T8 only: the planted sentence must make it pass)')
    selftest_arm(st, 'T8c CONTROL a planted DELETE-404 sentence makes T8 pass', t8c, None)
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, BODY, TITLE, MH); n = C.nfail()
print('C5 PR TEXT %s: %d FAIL of %d checks | #%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR))
raise SystemExit(1 if n else 0)
