#!/usr/bin/env python3
"""keyscan_gate42b.py — requirement 5: the DECLARED squash subject and the MANDATED squash body (kit.json `subject` / `mandated_body`).
  S1 subject keys (`KS-\\d+`) ⊆ own keys {KS-530, KS-729, KS-528}     S2 the declared subject does NOT end in `(#n)` (GitHub appends it)
  S3 landed length len(subject) + len(" (#1340)") <= 92                 B1 the body carries `Refs KS-530`, `Refs KS-729`, `Refs KS-528`, one line each
  B2 no closing keyword before a key (close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved, any case)
  B3 the body's key set == the own key set (a FOREIGN hyphenated key — e.g. KS-470 from a leg-6 CLEANUP line, KS-493/KS-635/KS-559 from a row's reason — refuses)
INFO (never a refusal): the keys in the PR title, PR body and the head commit message, as read (gh_pr1340.json / the scratch clone).
Overrides (controls): --subject S --body-file F. rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate42b.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
subj = opt('--subject', K['subject']); body = open(opt('--body-file')).read() if opt('--body-file') else K['mandated_body']
own = set(K['own_keys']); N = K['pr']; res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
sk = set(re.findall(r'KS-\d+', subj)); land = len(subj) + len(' (#%s)' % N)
chk('S1', bool(sk) and sk <= own, 'subject keys %s (own %s)' % (sorted(sk), sorted(own)))
chk('S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
chk('S3', land <= 92, 'declared %d, lands at %d (<= 92)' % (len(subj), land))
for k in sorted(own):
    c = len(re.findall(r'(?m)^Refs %s$' % re.escape(k), body)); chk('B1 ' + k, c == 1, '`Refs %s` lines: %d' % (k, c))
cl = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+', body)
chk('B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
bk = set(re.findall(r'KS-\d+', body)); chk('B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
print('INFO declared subject: %r' % subj)
try:
    pr = json.load(open(os.path.join(SP, 'g42b_sp', 'gh_pr1340.json'), encoding='utf-8'))['pr']
    print('INFO PR title keys %s | PR body keys %s | PR title == declared subject: %s' % (sorted(set(re.findall(r'KS-\d+', pr['title']))), sorted(set(re.findall(r'KS-\d+', pr['body'] or ''))), pr['title'] == subj))
    P = json.load(open(os.path.join(G, 'pins_gate42b.json'), encoding='utf-8'))
    cm = subprocess.run(['git', '-C', os.path.join(SP, 'g42b_sp', 'clone'), 'log', '-1', '--format=%B', P['head']], capture_output=True, text=True).stdout
    print('INFO head commit message keys %s (the merger COMPOSES the squash body; never pastes this)' % sorted(set(re.findall(r'KS-\d+', cm))))
except Exception as e: print('INFO PR/commit key read skipped: %s' % e)
nf = res.count(False)
print('KEYSCAN %s: %d checks, %d FAIL' % ('PASS' if nf == 0 else 'FAIL', len(res), nf))
raise SystemExit(1 if nf else 0)
