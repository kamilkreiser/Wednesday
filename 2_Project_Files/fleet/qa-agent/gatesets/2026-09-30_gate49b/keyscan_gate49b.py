#!/usr/bin/env python3
"""keyscan_gate49b.py — for EACH kit PR (kit.json order): the DECLARED squash subject (kit.json prs.<n>.subject, or — when null — the LIVE PR
title from gh_read_1.json) and the MANDATED squash body (`Refs <own key>`):
  S1 the subject's hyphenated keys (`KS-\\d+`, whole-key) are exactly {own key}     S2 the declared subject does NOT end in `(#n)`
  S3 landed length len(subject) + len(" (#n)") <= 92                                B1 the body carries `Refs <key>` exactly once, on its own line
  B2 no closing keyword before a key (close[sd]/fix(es|ed)/resolve[sd])             B3 the body's key set == {own key}
FLAG lines (a count, never a refusal — the merger COMPOSES the body): FOREIGN hyphenated KS keys and closing keywords on the LIVE surfaces
(the PR title, the PR body, every commit message on the branch, the BRANCH NAME). INFO: which foreign keys sit INSIDE a fenced block and which
OUTSIDE; `Refs <key>` on a line of its own in the PR body; the de-hyphenated context keys (kit prs.<n>.dehyphenated_in_body) present.
A key scan cannot judge TRUTH: SUBJECT-TRUE-OF-DIFF and PR-BODY-CLAIMS are the gate's. Overrides (controls): --pr <n> (scan one PR only)
--subject S --body-file F --prbody-file F --gh <gh_read json> --pins <name>. rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate49b.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
GH = json.load(open(opt('--gh', os.path.join(G, 'gh_read_1.json')), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate49b.SIM-%s.json' % opt('--pins') if opt('--pins') else 'pins_gate49b.json'), encoding='utf-8'))
CLN = os.path.join(SP, 'g49b_sp', 'clone'); KRX = r'\bKS-\d+\b'; CLOSE = r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+'
res = []; flags = 0
ORDER = [opt('--pr')] if opt('--pr') else K['order']
for N in ORDER:
    k = K['prs'][N]; own = set(k['keys']); prim = k['keys'][0]; gh = GH['prs'][N]; S = P['prs'][N]
    def chk(tag, ok, msg): res.append(ok); print('%s #%s %s: %s' % ('PASS' if ok else 'FAIL', N, tag, msg))
    decl = k.get('subject') or gh['title']; subj = opt('--subject', decl)
    body = open(opt('--body-file')).read() if opt('--body-file') else '\n'.join(k['mandated_body_refs'])
    sk = set(re.findall(KRX, subj)); land = len(subj) + len(' (#%s)' % N)
    print('INFO #%s (%s) declared subject source: %s' % (N, k['seat'], 'kit.json' if k.get('subject') else 'the LIVE PR title (kit.json subject is null)'))
    chk('S1', sk == {prim}, 'subject keys %s (own %s)' % (sorted(sk), sorted(own)))
    chk('S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
    chk('S3', land <= 92, 'declared %d, lands at %d (<= 92): %r' % (len(subj), land, subj))
    for key in sorted(own):
        c = len(re.findall(r'(?m)^Refs %s$' % re.escape(key), body)); chk('B1 ' + key, c == 1, '`Refs %s` lines: %d' % (key, c))
    cl = re.findall(CLOSE, body); chk('B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
    bk = set(re.findall(KRX, body)); chk('B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
    prb = open(opt('--prbody-file')).read() if opt('--prbody-file') else gh['body']
    shas = subprocess.run(['git', '-C', CLN, 'rev-list', '%s..%s' % (S['merge_base'], S['head'])], capture_output=True, text=True).stdout.split()
    cm = '\n'.join(subprocess.run(['git', '-C', CLN, 'log', '-1', '--format=%B', x], capture_output=True, text=True).stdout for x in shas)
    print('INFO #%s live surfaces scanned: PR title, PR body (%d chars), %d commit message(s) on the branch, the branch name %r' % (N, len(prb), len(shas), gh.get('branch')))
    for surf, txt in (('PR title', gh['title']), ('PR body', prb), ('branch commit message(s)', cm), ('branch name', gh.get('branch') or '')):
        ks = set(re.findall(KRX, txt if surf != 'branch name' else txt.upper())); f = sorted(ks - own); c2 = re.findall(CLOSE, txt)
        if f or c2: flags += 1
        print('%s #%s %s: keys %s | FOREIGN %s | closing keyword %s' % ('FLAG' if (f or c2) else 'INFO', N, surf, sorted(ks), f or 'none', c2 or 'none'))
    fence = re.split(r'(?m)^```.*$', prb); infence = ''.join(fence[1::2]); outfence = ''.join(fence[0::2])
    fi, fo = sorted(set(re.findall(KRX, infence)) - own), sorted(set(re.findall(KRX, outfence)) - own)
    print('INFO #%s PR body FOREIGN hyphenated keys INSIDE a fenced block: %s | OUTSIDE any fence: %s | de-hyphenated context keys present: %s' % (
        N, fi or 'none', fo or 'none', {x: (x in prb) for x in k.get('dehyphenated_in_body', [])} or 'none named'))
    print('INFO #%s PR body `Refs %s` as a whole line: %d | anywhere: %d | commit message `Refs %s` lines: %d' % (N, prim, len(re.findall(r'(?m)^Refs %s$' % prim, prb)), len(re.findall(r'Refs %s\b' % prim, prb)), prim, len(re.findall(r'(?m)^Refs %s$' % prim, cm))))
    print('INFO #%s PR title == declared subject: %s | title %d chars (lands %d) | commit subject == title: %s' % (N, gh['title'] == decl, len(gh['title']), len(gh['title']) + len(' (#%s)' % N), S['subject_commit'] == gh['title']))
nf = res.count(False)
print('KEYSCAN %s: %d checks over %d PR(s), %d FAIL, %d FLAG line(s) (live surfaces; the gate rules them)' % ('PASS' if nf == 0 else 'FAIL', len(res), len(ORDER), nf, flags))
raise SystemExit(1 if nf else 0)
