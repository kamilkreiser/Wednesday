#!/usr/bin/env python3
"""c1_pin_gate58.py — gate58 C1: pin the PR from TWO instruments and the commit from YOUR clone.
  P1 ls-remote origin (from --repo): refs/pull/<PR>/head == HEAD == the PR's branch ref (WHOLE-FIELD); develop at origin read.
  P2 the GitHub PULLS API (read-only GET; GH_TOKEN read BY NAME from the Secuura .env, never printed): open, not merged, base.ref develop,
     base.sha == develop at origin, head.sha == HEAD, head.ref matches kit branch_rx; mergeable printed (null re-read up to 3x).
  P3 shape in the clone: HEAD has exactly ONE parent and it == develop at origin == kit base (else STALE BASE: every C2-C6 expectation
     was drafted against kit base, so a moved develop is a RE-DRAFT); ahead 1, behind 0.
  P3b END_TREE: HEAD^{tree} (the landed tree while develop == base) printed beside develop^{tree} (the control that differs); when HEAD ==
     the READY's head, HEAD^{tree} must == the READY's claimed END_TREE (kit ready_claims.end_tree).
  P4 files: the API /files list == EXACTLY kit files (7 paths) AND `git diff --numstat develop HEAD` in the clone lists the same 7 with the
     same +/- per path. Equality BOTH ways (missing and extra are each named).
  P5 NO TRAILER: `git log -1 --format=%(trailers)` on HEAD empty AND 0 `Co-Authored-By` lines; CONTROL in the same run: the same command
     on kit trailer_control_commit prints a Co-Authored-By (the instrument can see one).
  (Key scan of title / body / commit / branch is C6's K1-K4.)
Controls-only override: G58_FILES_DROP=<path> removes one path from the EXPECTED set (a planted wrong expectation: P4 must FAIL naming it).
Usage: c1_pin_gate58.py --repo <your clone, HEAD + develop fetched into it> --pr <n> --head <40-hex>   (rc 0 PASS / 1 FAIL / 2 usage / 3 API)"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate58 import K, git, now, Checks, gh_token, gh_get, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--repo', '--pr', '--head')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
REPO, PR, HEAD = opt('--repo'), opt('--pr'), opt('--head')
if not re.fullmatch(r'\d+', PR or '') or not re.fullmatch(r'[0-9a-f]{40}', HEAD or ''):
    print('REFUSING: --pr must be digits and --head 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
tok = gh_token()
if not tok: print('REFUSING: GH_TOKEN not found by name in the Secuura .env'); raise SystemExit(3)
get = lambda u: gh_get(u, tok)
WANT = sorted(K['files'])
if os.environ.get('G58_FILES_DROP'):
    WANT = [p for p in WANT if p != os.environ['G58_FILES_DROP']]
    print('CONTROL OVERRIDE G58_FILES_DROP: the expected set has %d paths (dropped %s) — P4 MUST FAIL' % (len(WANT), os.environ['G58_FILES_DROP']))
print('c1_pin_gate58 %s | repo %s | PR #%s | HEAD %s' % (now(), REPO, PR, HEAD))
C = Checks()
p = get('pulls/' + PR); tries = 1
while p.get('mergeable') is None and tries < 3: time.sleep(10); p = get('pulls/' + PR); tries += 1
br = p['head']['ref']
rc, ls, err = git(REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + br, check=False)
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % PR); bh = R.get('refs/heads/' + br)
C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None,
      'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s (WHOLE-FIELD equality)' % (rc, PR, ph, br, bh, dev, HEAD))
brok = re.match(K['branch_rx'], br) is not None
C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['base']['sha'] == dev and p['head']['sha'] == HEAD and brok,
      'state %s | merged %s | base %s @ %s (== develop at origin %s) | head.sha %s | branch %s matches %s: %s | mergeable %s (%d read(s)) / %s | title %r' % (
          p['state'], p.get('merged'), p['base']['ref'], p['base']['sha'][:12], p['base']['sha'] == dev, p['head']['sha'], br, K['branch_rx'], brok,
          p.get('mergeable'), tries, p.get('mergeable_state'), p.get('title')))
rcc, _, _ = git(REPO, 'cat-file', '-e', HEAD + '^{commit}', check=False)
rcd, _, _ = git(REPO, 'cat-file', '-e', (dev or '0' * 40) + '^{commit}', check=False)
numstat = []
if rcc or rcd:
    C.chk('P3 shape', False, 'HEAD present in the clone %s | develop %s present %s — fetch refs/pull/%s/head and develop into YOUR clone first' % (not rcc, dev, not rcd, PR))
    C.chk('P3b END_TREE', False, 'not measurable: HEAD or develop absent from the clone')
else:
    parents = git(REPO, 'log', '-1', '--format=%P', HEAD).split()
    ahead = int(git(REPO, 'rev-list', '--count', '%s..%s' % (dev, HEAD)).strip()); behind = int(git(REPO, 'rev-list', '--count', '%s..%s' % (HEAD, dev)).strip())
    C.chk('P3 shape', parents == [dev] and ahead == 1 and behind == 0 and dev == K['base'],
          'parents %s (want exactly [develop %s]) | ahead %d (want 1) | behind %d (want 0) | develop == kit base %s: %s%s' % (
              [x[:12] for x in parents], dev[:12], ahead, behind, K['base'][:12], dev == K['base'], '' if dev == K['base'] else '  <- STALE BASE: a re-draft'))
    ht = git(REPO, 'rev-parse', HEAD + '^{tree}').strip(); dt = git(REPO, 'rev-parse', dev + '^{tree}').strip()
    rcl = K['ready_claims']; claim = rcl['end_tree'] if HEAD == rcl['head'] else None
    C.chk('P3b END_TREE', ht != dt and (claim is None or ht == claim),
          'HEAD^{tree} %s (the landed tree while develop has not moved) | develop^{tree} %s (control, differs: %s) | READY claim %s%s' % (
              ht, dt, ht != dt, claim or '(HEAD is not the READY head; no claim to compare)', '' if claim is None else (' == measured: %s' % (ht == claim))))
    numstat = [l.split('\t') for l in git(REPO, 'diff', '--numstat', dev, HEAD).splitlines() if l]
fl = []; pg = 1
while True:
    b = get('pulls/%s/files?per_page=100&page=%d' % (PR, pg)); fl += b
    if len(b) < 100: break
    pg += 1
api = sorted((f['filename'], f['additions'], f['deletions']) for f in fl); loc = sorted((x[2], int(x[0]), int(x[1])) for x in numstat if x[0].isdigit())
an = [x[0] for x in api]
miss = sorted(set(WANT) - set(an)); extra = sorted(set(an) - set(WANT))
C.chk('P4 files', an == WANT and api == loc,
      'API %d path(s) | clone numstat %d | API == numstat (+/- per path) %s | MISSING from the PR %s | EXTRA in the PR %s | totals API +%d/-%d' % (
          len(api), len(loc), api == loc, miss or 'NONE', extra or 'NONE', sum(x[1] for x in api), sum(x[2] for x in api)))
for x in api:
    print('INFO P4 %s +%d/-%d' % x)


def trailers(sha):
    t = git(REPO, 'log', '-1', '--format=%(trailers)', sha).strip(); m = git(REPO, 'log', '-1', '--format=%B', sha)
    return t, len(re.findall(r'(?im)^co-authored-by:', m))


ct, cn = trailers(K['trailer_control_commit'])
if not rcc:
    ht_, hn = trailers(HEAD)
    C.chk('P5 no trailer', ht_ == '' and hn == 0 and cn >= 1, 'HEAD trailers %r (%d Co-Authored-By) | CONTROL %s prints %r (%d)' % (ht_, hn, K['trailer_control_commit'], ct[:60], cn))
else:
    C.chk('P5 no trailer', False, 'HEAD not in the clone | CONTROL %s prints %r (%d)' % (K['trailer_control_commit'], ct[:60], cn))
n = C.nfail()
print('PIN %s: %d FAIL of %d checks | PR #%s | HEAD %s | develop %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], (dev or '?')[:12]))
raise SystemExit(1 if n else 0)
