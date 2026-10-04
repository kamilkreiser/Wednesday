#!/usr/bin/env python3
"""c1_pin_gate55.py — gate55 C1 PIN for Seat B 58th's PR B (KS-1015). Two instruments for the head (ls-remote + the PULLS API), the commit
read from the clone with READ-ONLY git verbs. A NEW COPY of c1_pin_gate54a.py, re-keyed, plus P3b (head/tree == the drafted head: a MOVED
HEAD is a re-draft) and P8 (0 co-tenant paths).
  P1  ls-remote origin: refs/pull/<PR>/head == HEAD == the branch ref; develop present.
  P2  PULLS API: open, not merged, base.ref develop, base.sha == origin develop, head.sha == HEAD, head.ref == kit branch_rx; mergeable shown.
  P3  shape in the clone: HEAD's ONE parent == develop; ahead 1 / behind 0 (EXACTLY ONE commit over develop); develop == kit base, else
      STALE BASE (every C2-C5 expectation was drafted against kit base: a re-draft, not a pass).
  P3b HEAD == kit expected_head AND HEAD^{tree} == kit expected_tree, else HEAD MOVED since drafting (README section 7: a re-draft).
  P4  files: API /files == clone `git diff --numstat develop HEAD` == EXACTLY the 5 declared paths, +/- equal per path; each vs the builder.
  P5  NO TRAILER: `%(trailers)` on HEAD empty, 0 Co-Authored-By lines; CONTROL kit trailer_control_commit prints one.
  P6  keys: title, body, branch and commit carry hyphenated KS-1015 and NO other hyphenated KS key (branch: lower-case ks-1015); no closing
      keyword; `Refs KS-1015` on its own line in the body. INFO: the de-hyphenated context keys in the body.
  P7  PR 0 (#1373) ABSENT: none of its 4 paths in develop..HEAD, each blob-equal develop == HEAD; MUST-HIT CONTROL: the same filter over
      PR 0's own diff (kit pr0_range) lists 4.
  P8  CO-TENANT ABSENT: 0 paths under kit cotenant_prefixes (services/timestamping/** = Seat D 4th's lane); MUST-HIT CONTROL: the same filter
      over kit cotenant_control_range (Seat D 3rd's pushed KS-1404 head) lists >= 1.
  P9  MODES: the 5 paths 100644 at HEAD (git ls-tree); CONTROL kit mode_control_path 100755.
  INFO END_TREE: HEAD^{tree} (valid while develop == kit base) beside develop^{tree} (the control that differs).
Controls-only inputs: --offline-dir <d> replays the PULLS API from pr_<PR>.json + files_<PR>.json (P2 then says OFFLINE);
--lsremote-file <f> replays an ls-remote listing instead of reading origin (P1 then says REPLAY). A real gate uses neither.
Usage: c1_pin_gate55.py --repo <clone with HEAD present> --pr <n> --head <40-hex> [--offline-dir d] [--lsremote-file f]
rc 0 PASS / 1 FAIL / 2 usage / 3 API"""
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate55 import K, git, now, Checks, GH, has_commit, count_range, blob_id

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--repo', '--pr', '--head')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO, PR, HEAD, OFF, LSF = opt('--repo'), opt('--pr'), opt('--head'), opt('--offline-dir'), opt('--lsremote-file')
if not re.fullmatch(r'\d+', PR or '') or not re.fullmatch(r'[0-9a-f]{40}', HEAD or ''):
    print('REFUSING: --pr must be digits and --head 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
gh = GH(OFF)
p = gh.get('pulls/' + PR); tries = 1
while not OFF and p.get('mergeable') is None and tries < 3:
    time.sleep(10); p = gh.get('pulls/' + PR); tries += 1
fl = gh.pages('pulls/%s/files' % PR)
print('c1_pin_gate55 %s | repo %s | PR #%s | HEAD %s%s%s' % (now(), REPO, PR, HEAD, ' | OFFLINE %s' % OFF if OFF else '', ' | LS-REMOTE REPLAY %s' % LSF if LSF else ''))
C = Checks()
br = p['head']['ref']
if LSF:
    rc, ls = 0, open(LSF, encoding='utf-8').read()
else:
    rc, ls, _ = git(REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + br, check=False)
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % PR); bh = R.get('refs/heads/' + br)
C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None,
      'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s (WHOLE-FIELD equality)' % (rc, PR, ph or 'ABSENT', br, bh or 'ABSENT', dev, HEAD))
bok = re.match(K['branch_rx'], br) is not None
C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['base']['sha'] == dev and p['head']['sha'] == HEAD and bok,
      'state %s | merged %s | base %s @ %s (== origin develop: %s) | head.sha %s | branch %s matches kit rule: %s | mergeable %s (%d read(s)) / %s | title %r' % (
          p['state'], p.get('merged'), p['base']['ref'], str(p['base']['sha'])[:12], p['base']['sha'] == dev, p['head']['sha'], br, bok,
          p.get('mergeable'), tries, p.get('mergeable_state'), p.get('title')))
hc = has_commit(REPO, HEAD); dc = has_commit(REPO, dev or '0' * 40)
numstat = []; names = []
if not (hc and dc):
    C.chk('P3 shape', False, 'HEAD present in the clone %s | develop %s present %s — fetch refs/pull/%s/head and develop into YOUR clone first' % (hc, dev, dc, PR))
    C.chk('P3b drafted head', False, 'objects missing')
else:
    parents = git(REPO, 'log', '-1', '--format=%P', HEAD).split(); ahead = count_range(REPO, dev, HEAD); behind = count_range(REPO, HEAD, dev)
    C.chk('P3 shape', parents == [dev] and ahead == 1 and behind == 0 and dev == K['base'],
          'parents %s == [develop %s]: %s | ahead %d (want EXACTLY 1) | behind %d (want 0) | develop == kit base %s: %s%s' % (
              [x[:12] for x in parents], dev[:12], parents == [dev], ahead, behind, K['base'][:12], dev == K['base'], '' if dev == K['base'] else '  <- STALE BASE: a re-draft'))
    tree = git(REPO, 'rev-parse', HEAD + '^{tree}').strip()
    C.chk('P3b drafted head', HEAD == K['expected_head'] and tree == K['expected_tree'],
          'HEAD %s == kit expected_head %s: %s | tree %s == kit expected_tree %s: %s%s' % (HEAD[:12], K['expected_head'][:12], HEAD == K['expected_head'], tree[:12],
              K['expected_tree'][:12], tree == K['expected_tree'], '' if HEAD == K['expected_head'] else '  <- HEAD MOVED since drafting (%s): a re-draft' % K.get('superseded_heads', {}).get(HEAD, 'not a head the drafter saw')))
    numstat = [l.split('\t') for l in git(REPO, 'diff', '--numstat', dev, HEAD).splitlines() if l]
    names = [l for l in git(REPO, 'diff', '--name-only', dev, HEAD).splitlines() if l]
    print('INFO END_TREE: HEAD^{tree} %s (parent == develop, so the squash lands on this tree while develop has not moved) | develop^{tree} %s (the control that differs)' % (
        tree, git(REPO, 'rev-parse', dev + '^{tree}').strip()))
api = sorted((f['filename'], f['additions'], f['deletions']) for f in fl); loc = sorted((x[2], int(x[0]), int(x[1])) for x in numstat if x[0].isdigit())
C.chk('P4 files', [x[0] for x in api] == sorted(K['files']) and api == loc,
      'API %d %s | clone numstat %d %s | want exactly the %d declared' % (len(api), ['%s +%d/-%d' % x for x in api], len(loc), ['%s +%d/-%d' % x for x in loc], len(K['files'])))
for f, a, d in loc:
    cl = K['numstat_claim'].get(f)
    print('INFO P4 claim %s: measured +%d/-%d | builder %s%s' % (f, a, d, '+%d/-%d' % tuple(cl) if cl else 'NONE', '' if cl and list(cl) == [a, d] else '  <- DIFFERS'))
def trailers(sha):
    t = git(REPO, 'log', '-1', '--format=%(trailers)', sha).strip(); m = git(REPO, 'log', '-1', '--format=%B', sha)
    return t, len(re.findall(r'(?im)^co-authored-by:', m)), m
ct, cn, _ = trailers(K['trailer_control_commit'])
if hc:
    ht, hn, msg = trailers(HEAD)
    C.chk('P5 no trailer', ht == '' and hn == 0 and cn >= 1, 'HEAD trailers %r (%d Co-Authored-By) | CONTROL %s prints %r (%d)' % (ht, hn, K['trailer_control_commit'], ct[:60], cn))
else:
    msg = ''; C.chk('P5 no trailer', False, 'HEAD not in the clone | CONTROL %s prints %d Co-Authored-By' % (K['trailer_control_commit'], cn))
body = p.get('body') or ''; own = K['ticket']
for s, t in (('title', p.get('title') or ''), ('body', body), ('branch', br), ('commit', msg)):
    ks = sorted(set(re.findall(r'\bKS-\d+\b', t))); cl = re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[:\s]+(KS-\d+|#\d+)', t)
    C.chk('P6 keys %s' % s, (ks == [own] or (s == 'branch' and ks == [] and own.lower() in t)) and not cl,
          'hyphenated keys %s (want exactly [%s]) | closing keyword %s' % (ks, own, cl or 'NONE'))
rl = re.search(r'(?m)^Refs %s\s*$' % own, body) is not None
C.chk('P6 Refs line', rl, '`Refs %s` on its own line in the PR body: %s' % (own, rl))
print('INFO P6 de-hyphenated keys in the body (context, never squash keys): %s' % sorted(set(re.findall(r'\bKS \d+\b', body))))
if hc and dc:
    hit = sorted(set(names) & set(K['pr0_files_absent']))
    a0, b0 = K['pr0_range']
    ctl = [l for l in git(REPO, 'diff', '--name-only', a0, b0).splitlines() if l in K['pr0_files_absent']] if has_commit(REPO, b0) else []
    eq = {f.split('/')[-2] + '/' + f.split('/')[-1]: blob_id(REPO, dev, f) == blob_id(REPO, HEAD, f) for f in K['pr0_files_absent']}
    C.chk('P7 PR 0 absent', not hit and all(eq.values()) and len(ctl) == 4,
          'PR 0 paths in develop..HEAD: %s (want none) | blob-equal develop == HEAD: %s | MUST-HIT CONTROL %s..%s lists %d of 4' % (hit or 'NONE', eq, a0[:12], b0[:12], len(ctl)))
    pre = tuple(K['cotenant_prefixes'])
    cot = [n for n in names if n.startswith(pre)]
    c0, c1 = K['cotenant_control_range']
    cctl = [l for l in git(REPO, 'diff', '--name-only', c0, c1).splitlines() if l.startswith(pre)] if has_commit(REPO, c1) else []
    C.chk('P8 co-tenant absent', not cot and len(cctl) >= 1,
          'paths under %s in develop..HEAD: %s (want none) | MUST-HIT CONTROL %s..%s lists %d' % (list(pre), cot or 'NONE', c0[:12], c1[:12], len(cctl)))
    modes = {}
    for f in K['files'] + [K['mode_control_path']]:
        o = git(REPO, 'ls-tree', HEAD, '--', f).strip(); modes[f] = o.split()[0] if o else 'ABSENT'
    pm = [modes[f] for f in K['files']]; cm = modes[K['mode_control_path']]
    C.chk('P9 modes', all(m == '100644' for m in pm) and cm == '100755', 'the 5 paths %s (want 100644 each) | CONTROL %s %s (want 100755)' % (pm, K['mode_control_path'], cm))
else:
    for t in ('P7 PR 0 absent', 'P8 co-tenant absent', 'P9 modes'):
        C.chk(t, False, 'objects missing — fetch first')
n = C.nfail()
print('PIN %s: %d FAIL of %d checks | PR #%s | HEAD %s | develop %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], (dev or '?')[:12]))
raise SystemExit(1 if n else 0)
