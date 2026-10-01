#!/usr/bin/env python3
"""keyscan_gate53.py — requirement 8, for the ONE kit PR (#1369, own key KS-530): the DECLARED squash subject (kit.json prs.<n>.subject, or —
when null — the LIVE PR title from gh_read_1.json) and the MANDATED squash body (`Refs KS-530`):
  S1 the subject's hyphenated keys (`KS-\\d+`, whole-key) are exactly {own}         S2 the declared subject does NOT end in `(#n)`
  S3 landed length len(subject) + len(" (#n)") <= 92                                B1 the body carries `Refs <own>` exactly once, on its own line
  B2 no closing keyword before a key (close[sd]/fix(es|ed)/resolve[sd])             B3 the body's key set == {own}
  L1 the LIVE surfaces (PR title, PR body, every commit message on the branch, the BRANCH NAME) carry NO hyphenated key but the PR's own
     (outside AND inside fences) and NO closing keyword — a FAIL, not a flag
  T1 NO TRAILER: every commit message on the branch has an EMPTY `%(trailers)` and 0 `Co-Authored-By` lines.
     CONTROL (kit trailer_control_commit, #1365's head bf277eead268): the SAME instrument must read a Co-Authored-By trailer there.
  M1 THE METHOD IS STATED PLAINLY (Wednesday's 2026-10-02 ruling, condition 1): the PR body carries every kit method_phrases string
     ("did not produce this edit unaided", "by hand"). The SENTENCES of the body that name npm beside a produce/regenerate verb are printed for the
     gate to read; a key scan cannot judge whether one of them SUGGESTS npm produced the edit unaided — that reading is the gate's.
INFO lines: the de-hyphenated context keys (kit dehyphenated_in_body) present in the PR body. A key scan cannot judge TRUTH: the PR-body claims
are the gate's. A NEW COPY of gate52's keyscan (one PR; M1 added by hand).
Overrides (controls / dry tests): --subject-<n> S --body-file F --prbody-file-<n> F --gh <gh_read json> --pins <name> --trailer-control <sha>
--commit-msg-file-<n> F (stands in for the branch commit messages). rc 0 PASS / rc 1 FAIL. Usage: keyscan_gate53.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
GH = json.load(open(opt('--gh', os.path.join(G, 'gh_read_1.json')), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate53.SIM-%s.json' % opt('--pins') if opt('--pins') else 'pins_gate53.json'), encoding='utf-8'))
CLN = os.path.join(SP, 'g53_sp', 'clone'); KRX = r'\bKS-\d+\b'; CLOSE = r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b[\s:]+KS-\d+'
def git(*a): return subprocess.run(['git', '-C', CLN] + list(a), capture_output=True, text=True).stdout
res = []
def chk(n, tag, ok, msg): res.append(ok); print('%s #%s %s: %s' % ('PASS' if ok else 'FAIL', n, tag, msg))
def trailers(sha): return git('log', '-1', '--format=%(trailers)', sha).strip()
for N in K['order']:
    k = K['prs'][N]; own = set(k['keys']); prim = k['keys'][0]; gh = GH['prs'][N]; pp = P['pr_pins'][N]
    decl = k.get('subject') or gh['title']; subj = opt('--subject-' + N, decl)
    body = open(opt('--body-file')).read() if opt('--body-file') else '\n'.join(k['mandated_body_refs'])
    sk = set(re.findall(KRX, subj)); land = len(subj) + len(' (#%s)' % N)
    print('INFO #%s declared subject source: %s' % (N, 'kit.json' if k.get('subject') else 'the LIVE PR title (kit.json subject is null)'))
    chk(N, 'S1', sk == {prim}, 'subject keys %s (own %s)' % (sorted(sk), sorted(own)))
    chk(N, 'S2', not re.search(r'\(#\d+\)\s*$', subj), 'declared subject carries no (#n) suffix')
    chk(N, 'S3', land <= 92, 'declared %d, lands at %d (<= 92): %r' % (len(subj), land, subj))
    for key in sorted(own):
        c = len(re.findall(r'(?m)^Refs %s$' % re.escape(key), body)); chk(N, 'B1 ' + key, c == 1, '`Refs %s` lines: %d' % (key, c))
    cl = re.findall(CLOSE, body); chk(N, 'B2', not cl, 'closing keyword before a key: %s' % (cl or 'none'))
    bk = set(re.findall(KRX, body)); chk(N, 'B3', bk == own, 'body key set %s | foreign %s' % (sorted(bk), sorted(bk - own) or 'none'))
    prb = open(opt('--prbody-file-' + N)).read() if opt('--prbody-file-' + N) else gh['body']
    shas = git('rev-list', '%s..%s' % (pp['merge_base'], pp['head'])).split()
    cm = open(opt('--commit-msg-file-' + N)).read() if opt('--commit-msg-file-' + N) else '\n'.join(git('log', '-1', '--format=%B', x) for x in shas)
    print('INFO #%s live surfaces scanned: PR title, PR body (%d chars), %d commit message(s) on the branch, the branch name %r' % (N, len(prb), len(shas), gh.get('branch')))
    bad_l = []
    for surf, txt in (('PR title', gh['title']), ('PR body', prb), ('branch commit message(s)', cm), ('branch name', gh.get('branch') or '')):
        ks = set(re.findall(KRX, txt if surf != 'branch name' else txt.upper())); f = sorted(ks - own); c2 = re.findall(CLOSE, txt)
        if f or c2: bad_l.append(surf)
        print('INFO #%s %s: keys %s | FOREIGN %s | closing keyword %s' % (N, surf, sorted(ks), f or 'none', c2 or 'none'))
    chk(N, 'L1 live surfaces', not bad_l, 'surfaces carrying a foreign hyphenated key or a closing keyword: %s' % (bad_l or 'NONE'))
    if opt('--commit-msg-file-' + N):
        tr = [subprocess.run(['git', 'interpret-trailers', '--parse'], input=cm, capture_output=True, text=True).stdout.strip()]
    else: tr = [trailers(x) for x in shas]
    coa = len(re.findall(r'(?im)^co-authored-by:', cm))
    chk(N, 'T1 no trailer', all(t == '' for t in tr) and coa == 0, '%d commit(s): trailers %s | Co-Authored-By lines %d' % (len(tr), [len(t) for t in tr], coa))
    print('INFO #%s de-hyphenated context keys present in the PR body: %s | `Refs %s` whole lines in the PR body: %d | in the commit message: %d' % (
        N, {x: (x in prb) for x in k.get('dehyphenated_in_body', [])}, prim, len(re.findall(r'(?m)^Refs %s$' % prim, prb)), len(re.findall(r'(?m)^Refs %s$' % prim, cm))))
    for p in [x for x in k['files'] if '/__tests__/' in x]:
        fk = sorted(set(re.findall(KRX, git('show', '%s:%s' % (pp['head'], p)))))
        print('INFO #%s committed file %s: hyphenated keys %s (file content, not a squash-body key)' % (N, p.split('/')[-1], fk))
    mp = [x for x in k.get('method_phrases', []) if x not in prb]
    chk(N, 'M1 method stated', not mp and bool(k.get('method_phrases')), 'method phrases %s present in the PR body; missing %s' % (k.get('method_phrases'), mp or 'NONE'))
    for sen in re.split(r'(?<=[.!?])\s+', re.sub(r'\s+', ' ', prb)):
        if re.search(r'\bnpm\b', sen) and re.search(r'(?i)\b(produc|regenerat|generat|rewr|wrote|edit|prun|remov|validat)', sen): print('INFO #%s method sentence: %s' % (N, sen[:240]))
    print('INFO #%s PR title == declared subject: %s | title %d chars (lands %d) | commit subject == title: %s' % (N, gh['title'] == decl, len(gh['title']), len(gh['title']) + len(' (#%s)' % N), pp['subject_commit'] == gh['title']))
ctl = opt('--trailer-control', K['trailer_control_commit']); ct = trailers(ctl)
fired = bool(re.search(r'(?im)^co-authored-by:', ct))
res.append(fired); print('%s T1-CONTROL %s: trailers %d bytes, Co-Authored-By present: %s (the instrument must FIRE here)' % ('PASS' if fired else 'FAIL', ctl[:12], len(ct), fired))
nf = res.count(False)
print('KEYSCAN %s: %d checks over %d PRs, %d FAIL (trailer control %s)' % ('PASS' if nf == 0 else 'FAIL', len(res), len(K['order']), nf, 'FIRED' if fired else 'DID NOT FIRE'))
raise SystemExit(1 if nf else 0)
