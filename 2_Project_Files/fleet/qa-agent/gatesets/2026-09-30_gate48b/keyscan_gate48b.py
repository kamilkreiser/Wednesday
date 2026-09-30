#!/usr/bin/env python3
"""keyscan_gate48b.py — for EACH kit PR (#1354 KS-470, #1355 KS-1378): the DECLARED squash subject (kit.json prs.<n>.subject, or — when kit.json
leaves it null — the LIVE PR title from gh_read_1.json) and the MANDATED squash body (`Refs <own key>`):
  S1 the subject's hyphenated keys (`KS-\\d+`, whole-key) are exactly {own key}    S2 the declared subject does NOT end in `(#n)`
  S3 landed length len(subject) + len(" (#n)") <= 92                                B1 the body carries `Refs <own key>` exactly once, on its own line
  B2 no closing keyword before a key (close[sd]/fix(es|ed)/resolve[sd])             B3 the body's key set == {own key}
FLAG lines (a count, never a refusal — the merger COMPOSES the body): FOREIGN hyphenated KS keys, and closing keywords, on the LIVE surfaces
(the PR title and body from gh_read_1.json, every commit message on the branch). Non-KS hyphen tokens (GHSA-…) are INFORMATION. #1355's body
carries leg 6's CLEANUP block VERBATIM (KS-470 / KS-559 / KS-729, by design; the READY measured Linear attached none while fenced): an INFO line
says which foreign keys sit INSIDE a fenced block and which OUTSIDE (an outside one is the real FLAG). A key scan cannot judge TRUTH:
SUBJECT-TRUE-OF-DIFF is the gate's. Overrides (controls): --pr <n> (scan ONE PR) --subject S --body-file F --prbody-file F.
rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate48b.py <scratchpad> [--pr n] [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
GH = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8')); P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))
CLN = os.path.join(SP, 'g48b_sp', 'clone'); KRX = r'\bKS-\d+\b'; CLOSE = r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+'
res = []; flags = 0; ORDER = [opt('--pr')] if opt('--pr') else K['order']
for N in ORDER:
    k = K['prs'][N]; own = set(k['keys']); prim = k['keys'][0]; gh = GH['prs'][N]
    def chk(tag, ok, msg): res.append(ok); print('%s #%s %s: %s' % ('PASS' if ok else 'FAIL', N, tag, msg))
    decl = k.get('subject') or gh['title']
    subj = opt('--subject', decl)
    body = open(opt('--body-file')).read() if opt('--body-file') else '\n'.join(k['mandated_body_refs'])
    sk = set(re.findall(KRX, subj)); land = len(subj) + len(' (#%s)' % N)
    print('INFO #%s declared subject source: %s' % (N, 'kit.json' if k.get('subject') else 'the LIVE PR title (kit.json subject is null)'))
    chk('S1', sk == {prim}, 'subject keys %s (own %s)' % (sorted(sk), sorted(own)))
    chk('S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
    chk('S3', land <= 92, 'declared %d, lands at %d (<= 92): %r' % (len(subj), land, subj))
    for key in sorted(own):
        c = len(re.findall(r'(?m)^Refs %s$' % re.escape(key), body)); chk('B1 ' + key, c == 1, '`Refs %s` lines: %d' % (key, c))
    cl = re.findall(CLOSE, body); chk('B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
    bk = set(re.findall(KRX, body)); chk('B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
    prb = open(opt('--prbody-file')).read() if opt('--prbody-file') else gh['body']
    shas = subprocess.run(['git', '-C', CLN, 'rev-list', '%s..%s' % (P['prs'][N]['merge_base'], P['prs'][N]['head'])], capture_output=True, text=True).stdout.split()
    cm = '\n'.join(subprocess.run(['git', '-C', CLN, 'log', '-1', '--format=%B', x], capture_output=True, text=True).stdout for x in shas)
    print('INFO #%s live surfaces scanned: PR title, PR body (%d chars), %d commit message(s) on the branch' % (N, len(prb), len(shas)))
    for surf, txt in (('PR title', gh['title']), ('PR body', prb), ('branch commit message(s)', cm)):
        ks = set(re.findall(KRX, txt)); f = sorted(ks - own); c2 = re.findall(CLOSE, txt)
        if f or c2: flags += 1
        print('%s #%s %s: keys %s | FOREIGN %s | closing keyword %s' % ('FLAG' if (f or c2) else 'INFO', N, surf, sorted(ks), f or 'none', c2 or 'none'))
        nk = sorted(set(re.findall(r'\b[A-Z][A-Z0-9]*-[0-9a-z]+(?:-[0-9a-z]+)*\b', txt)) - ks)
        if nk: print('INFO #%s %s: non-KS hyphen tokens (information): %s' % (N, surf, ' '.join(nk[:14])))
    fence = re.split(r'(?m)^```.*$', prb); infence = ''.join(fence[1::2]); outfence = ''.join(fence[0::2])
    fi, fo = sorted(set(re.findall(KRX, infence)) - own), sorted(set(re.findall(KRX, outfence)) - own)
    print('INFO #%s PR body FOREIGN hyphenated keys INSIDE a fenced block: %s (%d occurrence(s)) | OUTSIDE any fence: %s (%d) | de-hyphenated context keys present: %s' % (
        N, fi, sum(len(re.findall(r'\b%s\b' % re.escape(x), infence)) for x in fi), fo or 'none', sum(len(re.findall(r'\b%s\b' % re.escape(x), outfence)) for x in fo),
        {x: (x in prb) for x in k.get('dehyphenated_in_body', [])} or 'n/a'))
    print('INFO #%s PR body `Refs %s` as a whole line: %d | anywhere: %d | commit message `Refs %s` lines: %d' % (N, prim, len(re.findall(r'(?m)^Refs %s$' % prim, prb)), len(re.findall(r'Refs %s\b' % prim, prb)), prim, len(re.findall(r'(?m)^Refs %s$' % prim, cm))))
    print('INFO #%s PR title == declared subject: %s | title %d chars (lands %d) | commit subject == title: %s' % (N, gh['title'] == decl, len(gh['title']), len(gh['title']) + len(' (#%s)' % N), P['prs'][N]['subject_commit'] == gh['title']))
    if k.get('title') and gh['title'] != k['title']: flags += 1; print('FLAG #%s the live PR title moved since kit.json was written: %r' % (N, gh['title']))
    if re.search(r'build[- ]tree only', subj, re.I): flags += 1; print('FLAG #%s the declared subject says "build-tree only": gate48a measured undici INSTALLED in the issuer image builder stage; under Kam\'s permanent acceptance the gate rules whether the phrase is TRUE of the diff' % N)
nf = res.count(False)
print('KEYSCAN %s: %d checks over %d PR(s), %d FAIL, %d FLAG line(s) (live surfaces; the gate rules them)' % ('PASS' if nf == 0 else 'FAIL', len(res), len(ORDER), nf, flags))
raise SystemExit(1 if nf else 0)
