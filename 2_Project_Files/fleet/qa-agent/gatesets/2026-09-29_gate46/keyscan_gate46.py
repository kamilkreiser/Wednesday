#!/usr/bin/env python3
"""keyscan_gate46.py — the DECLARED squash subject (kit.json prs.1348.subject: the PR title verbatim) and the MANDATED squash body (`Refs KS-1054`,
kit.json mandated_body_refs) for the ONE PR #1348:
  S1 the subject's hyphenated keys (`KS-\\d+`) are exactly {KS-1054} — no foreign key, no second key
  S2 the declared subject does NOT end in `(#n)` (GitHub appends it)      S3 landed length len(subject) + len(" (#1348)") <= 92
  B1 the body carries `Refs KS-1054` exactly once                          B2 no closing keyword before a key (close[sd]/fix(es|ed)/resolve[sd])
  B3 the body's key set == {KS-1054}
FLAG lines (a count, never a refusal of the squash text — the merger COMPOSES the body): hyphenated FOREIGN keys in the live PR TITLE / PR BODY
(gh_read_1.json) and in EVERY commit message on the branch (round 1 AND round 2, the scratch clone) — per STANDING_LINES 2026-09-26 those surfaces
ATTACH a ticket. A key scan cannot judge TRUTH: SUBJECT-TRUE-OF-DIFF is the gate's.
Overrides (controls): --subject S --body-file F --prbody-file F. rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate46.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
res = []; flags = 0
def chk(n, tag, ok, msg): res.append(ok); print('%s #%s %s: %s' % ('PASS' if ok else 'FAIL', n, tag, msg))
gh = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))['prs']
P = json.load(open(os.path.join(G, 'pins_gate46.json'), encoding='utf-8'))
n = '1348'; k = K['prs'][n]; own = set(k['keys']); prim = k['keys'][0]
subj = opt('--subject', k['subject'])
body = open(opt('--body-file')).read() if opt('--body-file') else '\n'.join(k['mandated_body_refs'])
sk = set(re.findall(r'KS-\d+', subj)); land = len(subj) + len(' (#%s)' % n)
chk(n, 'S1', sk == {prim}, 'subject keys %s (own %s)' % (sorted(sk), sorted(own)))
chk(n, 'S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
chk(n, 'S3', land <= 92, 'declared %d, lands at %d (<= 92): %r' % (len(subj), land, subj))
for key in sorted(own):
    c = len(re.findall(r'(?m)^Refs %s$' % re.escape(key), body)); chk(n, 'B1 ' + key, c == 1, '`Refs %s` lines: %d' % (key, c))
CLOSE = r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+'
cl = re.findall(CLOSE, body)
chk(n, 'B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
bk = set(re.findall(r'KS-\d+', body)); chk(n, 'B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
prb = open(opt('--prbody-file')).read() if opt('--prbody-file') else gh[n]['body']
CLN = os.path.join(SP, 'g46_sp', 'clone')
shas = subprocess.run(['git', '-C', CLN, 'rev-list', '%s..%s' % (P['prs'][n]['merge_base'], P['prs'][n]['head'])], capture_output=True, text=True).stdout.split()
surf = [('PR title', gh[n]['title']), ('PR body', prb)] + [('commit %s message' % s[:12], subprocess.run(['git', '-C', CLN, 'log', '-1', '--format=%B', s], capture_output=True, text=True).stdout) for s in shas]
print('INFO #%s live surfaces scanned: PR title, PR body, %d commit message(s) on the branch' % (n, len(shas)))
for name, txt in surf:
    ks = set(re.findall(r'KS-\d+', txt)); f = sorted(ks - own); c2 = re.findall(CLOSE, txt)
    if f: flags += 1
    print('%s #%s %s: keys %s | FOREIGN %s' % ('FLAG' if f else 'INFO', n, name, sorted(ks), f or 'none'))
    if c2: flags += 1; print('FLAG #%s closing keyword on %s: %s' % (n, name, c2))
    nk = sorted(set(re.findall(r'\b[A-Z][A-Z0-9]*-\d+(?:-\d+)?\b', txt)) - ks - set('%s' % x for x in own))
    if nk: print('INFO #%s %s: non-KS hyphen tokens (information): %s' % (n, name, ' '.join(nk[:12])))
print('INFO #%s PR title == declared subject: %s | title %d chars (lands %d) | declared %d chars' % (n, gh[n]['title'] == k['subject'], len(gh[n]['title']), len(gh[n]['title']) + len(' (#%s)' % n), len(k['subject'])))
if gh[n]['title'] != k.get('title'): flags += 1; print('FLAG #%s the live PR title moved since kit.json was written: %r' % (n, gh[n]['title']))
nf = res.count(False)
print('KEYSCAN %s: %d checks over 1 PR, %d FAIL, %d FLAG line(s) (live surfaces; the gate rules them)' % ('PASS' if nf == 0 else 'FAIL', len(res), nf, flags))
raise SystemExit(1 if nf else 0)
