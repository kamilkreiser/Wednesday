#!/usr/bin/env python3
"""c1_pin_gate54f.py — gate54f C1: pin the PR from TWO instruments and the commit from the clone.
  P1 ls-remote origin (from --repo): refs/pull/<PR>/head == HEAD == the PR's branch ref; develop at origin == the PR's base sha (read below).
  P2 the GitHub PULLS API (read-only GET; GH_TOKEN read BY NAME from the Secuura .env, never printed): state open, not merged, base.ref develop,
     head.sha == HEAD, head.ref matches kit branch_rx; mergeable printed (null is re-read up to 3x).
  P3 shape in the clone: merge-base(HEAD, develop) == develop (0 behind), ahead == 1 (one commit), develop == kit base (else STALE BASE:
     every C2-C6 expectation was drafted against kit base, so a moved develop is a re-draft, not a pass).
  P4 files: the API /files list == exactly kit files (4) AND `git diff --numstat develop HEAD` lists the same 4 with the same +/- per path.
  P5 NO TRAILER: `git log -1 --format=%(trailers)` on HEAD empty AND 0 `Co-Authored-By` lines in the whole message; CONTROL in the same
     run: the same command on kit trailer_control_commit prints a Co-Authored-By trailer (the instrument can see one).
  P6 keys: PR title, body, branch and commit message carry the hyphenated key KS-1403 and NO other hyphenated KS key (KS-1404 lives in the
     baseline FILE only); no closing keyword (close/fix/resolve + KS-1403 or #n); `Refs KS-1403` on its own line in the body.
Usage: c1_pin_gate54f.py --repo <your clone, HEAD fetched into it> --pr <n> --head <40-hex>   (rc 0 PASS / 1 FAIL / 2 usage / 3 API)"""
import json, os, re, sys, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54f import K, git, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--repo', '--pr', '--head')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO, PR, HEAD = opt('--repo'), opt('--pr'), opt('--head')
if not re.fullmatch(r'\d+', PR) or not re.fullmatch(r'[0-9a-f]{40}', HEAD):
    print('REFUSING: --pr must be digits and --head 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
tok = ''
for l in open(K['secuura_env'], encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
if not tok: print('REFUSING: GH_TOKEN not found by name in the Secuura .env'); raise SystemExit(3)
def get(u):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/%s/%s' % (K['gh_repo'], u),
                headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: print('API %s HTTP %d' % (u, e.code)); raise SystemExit(3)
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if i == 3: print('API %s unreachable: %s' % (u, e)); raise SystemExit(3)
            print('RETRY %s: %s' % (u, e), file=sys.stderr)
        time.sleep(10)
print('c1_pin_gate54f %s | repo %s | PR #%s | HEAD %s' % (now(), REPO, PR, HEAD))
C = Checks()
p = get('pulls/' + PR); tries = 1
while p.get('mergeable') is None and tries < 3: time.sleep(10); p = get('pulls/' + PR); tries += 1
br = p['head']['ref']
rc, ls, err = git(REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + br, check=False)
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % PR); bh = R.get('refs/heads/' + br)
C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None,
      'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s (WHOLE-FIELD equality)' % (rc, PR, ph, br, bh, dev, HEAD))
C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['head']['sha'] == HEAD and re.match(K['branch_rx'], br) is not None,
      'state %s | merged %s | base %s | head.sha %s | branch %s matches %s: %s | mergeable %s (%d read(s)) / %s | title %r' % (
          p['state'], p.get('merged'), p['base']['ref'], p['head']['sha'], br, K['branch_rx'], re.match(K['branch_rx'], br) is not None,
          p.get('mergeable'), tries, p.get('mergeable_state'), p.get('title')))
rcc, _, _ = git(REPO, 'cat-file', '-e', HEAD + '^{commit}', check=False); rcd, _, _ = git(REPO, 'cat-file', '-e', (dev or '0' * 40) + '^{commit}', check=False)
if rcc or rcd:
    C.chk('P3 shape', False, 'HEAD present in the clone %s | develop %s present %s — fetch refs/pull/%s/head and develop into YOUR clone first' % (not rcc, dev, not rcd, PR))
    numstat = []
else:
    mb = git(REPO, 'merge-base', HEAD, dev).strip(); ahead = int(git(REPO, 'rev-list', '--count', '%s..%s' % (dev, HEAD)).strip())
    behind = int(git(REPO, 'rev-list', '--count', '%s..%s' % (HEAD, dev)).strip())
    C.chk('P3 shape', mb == dev and ahead == 1 and behind == 0 and dev == K['base'],
          'merge-base %s == develop %s: %s | ahead %d (want 1) | behind %d | develop == kit base %s: %s%s' % (
              mb[:12], dev[:12], mb == dev, ahead, behind, K['base'][:12], dev == K['base'], '' if dev == K['base'] else '  <- STALE BASE: a re-draft'))
    numstat = [l.split('\t') for l in git(REPO, 'diff', '--numstat', dev, HEAD).splitlines() if l]
    print('INFO END_TREE: HEAD^{tree} %s (parent == develop, so the squash lands on this tree while develop has not moved) | develop^{tree} %s (the control that differs)' % (
        git(REPO, 'rev-parse', HEAD + '^{tree}').strip(), git(REPO, 'rev-parse', dev + '^{tree}').strip()))
fl = []; pg = 1
while True:
    b = get('pulls/%s/files?per_page=100&page=%d' % (PR, pg)); fl += b
    if len(b) < 100: break
    pg += 1
api = sorted((f['filename'], f['additions'], f['deletions']) for f in fl); loc = sorted((x[2], int(x[0]), int(x[1])) for x in numstat if x[0].isdigit())
C.chk('P4 files', [x[0] for x in api] == sorted(K['files']) and api == loc,
      'API %s | clone numstat %s | want exactly %s' % (['%s +%d/-%d' % x for x in api], ['%s +%d/-%d' % x for x in loc], sorted(K['files'])))
def trailers(sha):
    t = git(REPO, 'log', '-1', '--format=%(trailers)', sha).strip(); m = git(REPO, 'log', '-1', '--format=%B', sha)
    return t, len(re.findall(r'(?im)^co-authored-by:', m)), m
ct, cn, _ = trailers(K['trailer_control_commit'])
if not rcc:
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
C.chk('P6 Refs line', re.search(r'(?m)^Refs %s\s*$' % own, body) is not None, '`Refs %s` on its own line in the PR body: %s' % (own, re.search(r'(?m)^Refs %s\s*$' % own, body) is not None))
n = C.nfail()
print('PIN %s: %d FAIL of %d checks | PR #%s | HEAD %s | develop %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], (dev or '?')[:12]))
raise SystemExit(1 if n else 0)
