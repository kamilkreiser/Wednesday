#!/usr/bin/env python3
"""c1_pin_gate54a.py — gate54a C1: pin the PR from TWO instruments and the commit from the clone (a NEW COPY of c1_pin_gate54f.py, re-keyed).
  P1 ls-remote origin (from --repo): refs/pull/<PR>/head == HEAD == the PR's branch ref; develop at origin == the PR's base sha.
  P2 the GitHub PULLS API (read-only GET; GH_TOKEN read BY NAME from the Secuura .env, never printed): state open, not merged, base.ref
     develop, base.sha == develop, head.sha == HEAD, head.ref matches kit branch_rx; mergeable printed (null is re-read up to 3x).
  P3 shape in the clone: HEAD's ONE parent == develop, ahead 1 / behind 0 (counted with `git log a..b`, no rev-list), develop == kit base (else
     STALE BASE: every C2-C6 expectation was drafted against kit base, so a moved develop is a re-draft, not a pass).
  P4 files: the API /files list == exactly kit files (5) AND `git diff --numstat develop HEAD` lists the same 5 with the same +/- per path;
     INFO: each +/- against the builder's kit numstat_claim.
  P5 NO TRAILER: `git log -1 --format=%(trailers)` on HEAD empty AND 0 `Co-Authored-By` lines in the whole message; CONTROL in the same run:
     the same command on kit trailer_control_commit prints a Co-Authored-By trailer (the instrument can see one).
  P6 keys: PR title, body, branch and commit message carry the hyphenated key KS-1402 and NO other hyphenated KS key (the branch carries it
     lower-case); no closing keyword (close/fix/resolve + KS-n or #n); `Refs KS-1402` on its own line in the body.
  P7 PR 0 ABSENT: none of kit pr0_files_absent (root lock, two service locks, audit-baseline.json) is in `git diff --name-only develop HEAD`,
     and each is BLOB-EQUAL develop == HEAD; MUST-HIT CONTROL: the same filter over PR 0's own diff (kit base_parent .. kit pr0_commit) = 4.
  P8 MODES: the 5 paths are 100644 at HEAD (git ls-tree; core.filemode is false); CONTROL kit mode_control_path reads 100755.
  INFO END_TREE: HEAD^{tree} (parent == develop, so the squash lands on this tree while develop has not moved); develop^{tree} as the control.
--pr-json <file> + --files-json <file>: read the PULLS API answers from files instead (controls / offline replays; P2 then says OFFLINE).
Usage: c1_pin_gate54a.py --repo <clone, HEAD present in it> --pr <n> --head <40-hex>   (rc 0 PASS / 1 FAIL / 2 usage / 3 API)"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54a import K, git, now, Checks, gh_token, gh_get, has_commit, count_range

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--repo', '--pr', '--head')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO, PR, HEAD = opt('--repo'), opt('--pr'), opt('--head')
if not re.fullmatch(r'\d+', PR) or not re.fullmatch(r'[0-9a-f]{40}', HEAD):
    print('REFUSING: --pr must be digits and --head 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
OFF = opt('--pr-json')
if OFF:
    p = json.load(open(OFF)); tries = 0; fl = json.load(open(opt('--files-json')))
else:
    tok = gh_token()
    if not tok: print('REFUSING: GH_TOKEN not found by name in the Secuura .env'); raise SystemExit(3)
    p = gh_get('pulls/' + PR, tok); tries = 1
    while p.get('mergeable') is None and tries < 3: time.sleep(10); p = gh_get('pulls/' + PR, tok); tries += 1
    fl = []; pg = 1
    while True:
        b = gh_get('pulls/%s/files?per_page=100&page=%d' % (PR, pg), tok); fl += b
        if len(b) < 100: break
        pg += 1
print('c1_pin_gate54a %s | repo %s | PR #%s | HEAD %s%s' % (now(), REPO, PR, HEAD, ' | OFFLINE PR json %s' % OFF if OFF else ''))
C = Checks()
br = p['head']['ref']
rc, ls, err = git(REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + br, check=False)
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % PR); bh = R.get('refs/heads/' + br)
C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None,
      'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s (WHOLE-FIELD equality)' % (rc, PR, ph, br, bh, dev, HEAD))
bok = re.match(K['branch_rx'], br) is not None
C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['base']['sha'] == dev and p['head']['sha'] == HEAD and bok,
      'state %s | merged %s | base %s @ %s (== origin develop: %s) | head.sha %s | branch %s matches %s: %s | mergeable %s (%d read(s)) / %s | title %r' % (
          p['state'], p.get('merged'), p['base']['ref'], str(p['base']['sha'])[:12], p['base']['sha'] == dev, p['head']['sha'], br, K['branch_rx'], bok,
          p.get('mergeable'), tries, p.get('mergeable_state'), p.get('title')))
hc = has_commit(REPO, HEAD); dc = has_commit(REPO, dev or '0' * 40)
numstat = []; names = []
if not (hc and dc):
    C.chk('P3 shape', False, 'HEAD present in the clone %s | develop %s present %s — fetch refs/pull/%s/head and develop into YOUR clone first' % (hc, dev, dc, PR))
else:
    parents = git(REPO, 'log', '-1', '--format=%P', HEAD).split(); ahead = count_range(REPO, dev, HEAD); behind = count_range(REPO, HEAD, dev)
    C.chk('P3 shape', parents == [dev] and ahead == 1 and behind == 0 and dev == K['base'],
          'parents %s == [develop %s]: %s | ahead %d (want 1) | behind %d (want 0) | develop == kit base %s: %s%s' % (
              [x[:12] for x in parents], dev[:12], parents == [dev], ahead, behind, K['base'][:12], dev == K['base'], '' if dev == K['base'] else '  <- STALE BASE: a re-draft'))
    numstat = [l.split('\t') for l in git(REPO, 'diff', '--numstat', dev, HEAD).splitlines() if l]
    names = [l for l in git(REPO, 'diff', '--name-only', dev, HEAD).splitlines() if l]
    print('INFO END_TREE: HEAD^{tree} %s (parent == develop, so the squash lands on this tree while develop has not moved) | develop^{tree} %s (the control that differs)' % (
        git(REPO, 'rev-parse', HEAD + '^{tree}').strip(), git(REPO, 'rev-parse', dev + '^{tree}').strip()))
api = sorted((f['filename'], f['additions'], f['deletions']) for f in fl); loc = sorted((x[2], int(x[0]), int(x[1])) for x in numstat if x[0].isdigit())
C.chk('P4 files', [x[0] for x in api] == sorted(K['files']) and api == loc,
      'API %s | clone numstat %s | want exactly %s' % (['%s +%d/-%d' % x for x in api], ['%s +%d/-%d' % x for x in loc], sorted(K['files'])))
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
    msg = ''; C.chk('P5 no trailer', False, 'HEAD not in the clone | CONTROL %s prints %r (%d) — the instrument works' % (K['trailer_control_commit'], ct[:60], cn))
body = p.get('body') or ''; own = K['ticket']
surf = {'title': p.get('title') or '', 'body': body, 'branch': br, 'commit': msg}
for s, t in surf.items():
    ks = sorted(set(re.findall(r'\bKS-\d+\b', t))); cl = re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[:\s]+(KS-\d+|#\d+)', t)
    C.chk('P6 keys %s' % s, (ks == [own] or (s == 'branch' and ks == [] and own.lower() in t)) and not cl,
          'hyphenated keys %s (want exactly [%s]) | closing keyword %s' % (ks, own, cl or 'NONE'))
rl = re.search(r'(?m)^Refs %s\s*$' % own, body) is not None
C.chk('P6 Refs line', rl, '`Refs %s` on its own line in the PR body: %s' % (own, rl))
dek = sorted(set(re.findall(r'\bKS \d+\b', body)))
print('INFO P6 de-hyphenated keys in the body (context, not squash keys): %s' % dek)
if hc and dc:
    hit = sorted(set(names) & set(K['pr0_files_absent']))
    ctl = [l for l in git(REPO, 'diff', '--name-only', K['base_parent'], K['pr0_commit']).splitlines() if l in K['pr0_files_absent']] if has_commit(REPO, K['base_parent']) else []
    def blob(c, f):
        rc2, o, _ = git(REPO, 'rev-parse', '%s:%s' % (c, f), check=False); return o.strip() if rc2 == 0 else 'ABSENT'
    eq = {f: blob(dev, f) == blob(HEAD, f) for f in K['pr0_files_absent']}
    C.chk('P7 PR 0 absent', not hit and all(eq.values()) and len(ctl) == 4,
          'PR 0 paths in develop..HEAD: %s (want none) | blob-equal develop == HEAD: %s | MUST-HIT CONTROL %s..%s lists %d of 4 (%s)' % (
              hit or 'NONE', eq, K['base_parent'][:12], K['pr0_commit'][:12], len(ctl), ctl))
    modes = {}
    for f in K['files'] + [K['mode_control_path']]:
        o = git(REPO, 'ls-tree', HEAD, '--', f).strip(); modes[f] = o.split()[0] if o else 'ABSENT'
    pm = [modes[f] for f in K['files']]; cm = modes[K['mode_control_path']]
    C.chk('P8 modes', all(m == '100644' for m in pm) and cm == '100755',
          'the 5 paths %s (want 100644 each) | CONTROL %s %s (want 100755)' % (pm, K['mode_control_path'], cm))
else:
    C.chk('P7 PR 0 absent', False, 'objects missing — fetch first'); C.chk('P8 modes', False, 'objects missing — fetch first')
n = C.nfail()
print('PIN %s: %d FAIL of %d checks | PR #%s | HEAD %s | develop %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], (dev or '?')[:12]))
raise SystemExit(1 if n else 0)
