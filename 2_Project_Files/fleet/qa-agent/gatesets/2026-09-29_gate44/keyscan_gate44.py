#!/usr/bin/env python3
"""keyscan_gate44.py — the DECLARED squash subject (the PR title verbatim, kit.json prs.<n>.subject) and the MANDATED squash body (the `Refs <key>`
lines, kit.json prs.<n>.mandated_body_refs) for EACH of the two PRs:
  S1 the subject's hyphenated keys (`KS-\\d+`) are exactly {the PR's PRIMARY key} (its first own key) — no foreign key, no second key
  S2 the declared subject does NOT end in `(#n)` (GitHub appends it)      S3 landed length len(subject) + len(" (#n)") <= 92
  B1 the body carries `Refs <key>` once per own key                        B2 no closing keyword before a key (close[sd]/fix(es|ed)/resolve[sd])
  B3 the body's key set == the own key set
FLAG lines (a count, never a refusal of the squash text — the merger COMPOSES the body): hyphenated FOREIGN keys in the live PR TITLE / PR BODY
(gh_read_1.json) and in the head COMMIT MESSAGE (the scratch clone) — per STANDING_LINES 2026-09-26 those surfaces ATTACH a ticket.
Overrides (controls): --pr N --subject S --body-file F --prbody-file F (a stand-in PR body for the FLAG scan). rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate44.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
only = opt('--pr'); res = []; flags = 0
def chk(n, tag, ok, msg): res.append(ok); print('%s #%s %s: %s' % ('PASS' if ok else 'FAIL', n, tag, msg))
gh = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))['prs']
P = json.load(open(os.path.join(G, 'pins_gate44.json'), encoding='utf-8'))
for n in K['order']:
    if only and n != only: continue
    k = K['prs'][n]; own = set(k['keys']); prim = k['keys'][0]
    subj = opt('--subject', k['subject']) if only else k['subject']
    body = open(opt('--body-file')).read() if (only and opt('--body-file')) else '\n'.join(k['mandated_body_refs'])
    sk = set(re.findall(r'KS-\d+', subj)); land = len(subj) + len(' (#%s)' % n)
    chk(n, 'S1', sk == {prim}, 'subject keys %s (primary %s; own %s)' % (sorted(sk), prim, sorted(own)))
    chk(n, 'S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
    chk(n, 'S3', land <= 92, 'declared %d, lands at %d (<= 92): %r' % (len(subj), land, subj))
    for key in sorted(own):
        c = len(re.findall(r'(?m)^Refs %s$' % re.escape(key), body)); chk(n, 'B1 ' + key, c == 1, '`Refs %s` lines: %d' % (key, c))
    cl = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+', body)
    chk(n, 'B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
    bk = set(re.findall(r'KS-\d+', body)); chk(n, 'B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
    prb = open(opt('--prbody-file')).read() if (only and opt('--prbody-file')) else gh[n]['body']
    tk = set(re.findall(r'KS-\d+', gh[n]['title'])); bdk = set(re.findall(r'KS-\d+', prb))
    cm = subprocess.run(['git', '-C', os.path.join(SP, 'g44_sp', 'clone'), 'log', '-1', '--format=%B', P['prs'][n]['head']], capture_output=True, text=True).stdout
    ck = set(re.findall(r'KS-\d+', cm)); cl2 = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+', prb + '\n' + cm)
    for surf, ks in (('PR title', tk), ('PR body', bdk), ('head commit message', ck)):
        f = sorted(ks - own)
        if f: flags += 1
        print('%s #%s %s: keys %s | FOREIGN %s' % ('FLAG' if f else 'INFO', n, surf, sorted(ks), f or 'none'))
    if cl2: flags += 1; print('FLAG #%s closing keyword on a live surface (PR body / commit): %s' % (n, cl2))
    print('INFO #%s PR title == declared subject: %s' % (n, gh[n]['title'] == k['subject']))
nf = res.count(False)
print('KEYSCAN %s: %d checks over %s, %d FAIL, %d FLAG line(s) (live surfaces; the gate rules them)' % ('PASS' if nf == 0 else 'FAIL', len(res), only or '2 PRs', nf, flags))
raise SystemExit(1 if nf else 0)
