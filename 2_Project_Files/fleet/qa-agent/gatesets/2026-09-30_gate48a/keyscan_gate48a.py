#!/usr/bin/env python3
"""keyscan_gate48a.py — the DECLARED squash subject (kit.json prs.1354.subject: the PR title verbatim) and the MANDATED squash body (`Refs KS-470`):
  S1 the subject's hyphenated keys (`KS-\\d+`, whole-key) are exactly {KS-470} — no foreign key, no second key
  S2 the declared subject does NOT end in `(#n)` (GitHub appends it)      S3 landed length len(subject) + len(" (#1354)") <= 92
  B1 the body carries `Refs KS-470` exactly once                          B2 no closing keyword before a key (close[sd]/fix(es|ed)/resolve[sd])
  B3 the body's key set == {KS-470}
FLAG lines (a count, never a refusal — the merger COMPOSES the body): FOREIGN hyphenated KS keys, and closing keywords, on the LIVE surfaces
(the PR title and body from gh_read_1.json, and every commit message on the branch in the scratch clone). Non-KS hyphen tokens (GHSA-…) are
INFORMATION. A key scan cannot judge TRUTH: SUBJECT-TRUE-OF-DIFF is the gate's.
Overrides (controls): --subject S --body-file F --prbody-file F. rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate48a.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
res = []; flags = 0; N = K['order'][0]; k = K['prs'][N]; own = set(k['keys']); prim = k['keys'][0]
def chk(tag, ok, msg): res.append(ok); print('%s #%s %s: %s' % ('PASS' if ok else 'FAIL', N, tag, msg))
KRX = r'\bKS-\d+\b'
gh = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))['prs'][N]
P = json.load(open(os.path.join(G, 'pins_gate48a.json'), encoding='utf-8'))
subj = opt('--subject', k['subject'])
body = open(opt('--body-file')).read() if opt('--body-file') else '\n'.join(k['mandated_body_refs'])
sk = set(re.findall(KRX, subj)); land = len(subj) + len(' (#%s)' % N)
chk('S1', sk == {prim}, 'subject keys %s (own %s)' % (sorted(sk), sorted(own)))
chk('S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
chk('S3', land <= 92, 'declared %d, lands at %d (<= 92): %r' % (len(subj), land, subj))
for key in sorted(own):
    c = len(re.findall(r'(?m)^Refs %s$' % re.escape(key), body)); chk('B1 ' + key, c == 1, '`Refs %s` lines: %d' % (key, c))
CLOSE = r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+'
cl = re.findall(CLOSE, body); chk('B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
bk = set(re.findall(KRX, body)); chk('B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
prb = open(opt('--prbody-file')).read() if opt('--prbody-file') else gh['body']
CLN = os.path.join(SP, 'g48a_sp', 'clone')
shas = subprocess.run(['git', '-C', CLN, 'rev-list', '%s..%s' % (P['prs'][N]['merge_base'], P['prs'][N]['head'])], capture_output=True, text=True).stdout.split()
cm = '\n'.join(subprocess.run(['git', '-C', CLN, 'log', '-1', '--format=%B', x], capture_output=True, text=True).stdout for x in shas)
print('INFO #%s live surfaces scanned: PR title, PR body (%d chars), %d commit message(s) on the branch' % (N, len(prb), len(shas)))
for surf, txt in (('PR title', gh['title']), ('PR body', prb), ('branch commit message(s)', cm)):
    ks = set(re.findall(KRX, txt)); f = sorted(ks - own); c2 = re.findall(CLOSE, txt)
    if f or c2: flags += 1
    print('%s #%s %s: keys %s | FOREIGN %s | closing keyword %s' % ('FLAG' if (f or c2) else 'INFO', N, surf, sorted(ks), f or 'none', c2 or 'none'))
    nk = sorted(set(re.findall(r'\b[A-Z][A-Z0-9]*-[0-9a-z]+(?:-[0-9a-z]+)*\b', txt)) - ks)
    if nk: print('INFO #%s %s: non-KS hyphen tokens (information): %s' % (N, surf, ' '.join(nk[:14])))
refs = len(re.findall(r'(?m)^Refs KS-470$', prb)); print('INFO #%s PR body `Refs KS-470` lines: %d | commit message `Refs KS-470` lines: %d' % (N, refs, len(re.findall(r'(?m)^Refs KS-470$', cm))))
print('INFO #%s PR title == declared subject: %s | title %d chars (lands %d) | commit subject == title: %s' % (N, gh['title'] == k['subject'], len(gh['title']), len(gh['title']) + len(' (#%s)' % N), P['prs'][N]['subject_commit'] == gh['title']))
if gh['title'] != k.get('title'): flags += 1; print('FLAG #%s the live PR title moved since kit.json was written: %r' % (N, gh['title']))
nf = res.count(False)
print('KEYSCAN %s: %d checks over %s, %d FAIL, %d FLAG line(s) (live surfaces; the gate rules them)' % ('PASS' if nf == 0 else 'FAIL', len(res), '1 PR', nf, flags))
raise SystemExit(1 if nf else 0)
