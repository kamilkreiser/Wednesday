#!/usr/bin/env python3
"""c1_pin_gateD2.py — gateD2 C1: pin the PR from TWO instruments and the commits from the clone (a NEW COPY of c1_pin_gate54a.py, re-keyed for a
TWO-COMMIT PR: Wednesday's 14:2xZ ruling adds a second commit carrying the committed PEM bundle).
  P1 ls-remote origin (from --repo): refs/pull/<PR>/head == HEAD == the PR's branch ref; develop at origin read.
  P2 the PULLS API (read-only GET; GH_TOKEN by name, never printed): open, not merged, base develop, base.sha == develop, head.sha == HEAD,
     head.ref matches kit branch_rx, commits == kit n_commits; mergeable printed (null re-read up to 3x).
  P3 shape: develop..HEAD is exactly kit n_commits (2) commits, LINEAR (each has one parent), the FIRST one's parent == develop, behind 0,
     develop == kit base (else STALE BASE: run repin_base_gateD2.py — every C2-C6 expectation is base-specific; never guessed).
  P4 files: API /files == exactly kit files (14) AND `git diff --numstat develop HEAD` lists the same 14 with the same +/- per path.
     INFO per commit: its own name list (the second commit must ADD the two config/ files); the first commit's numstat vs the builder's claim.
  P4b PATH GATE: every path in develop..HEAD matches kit path_allow_rx (services/timestamping/**, root lock, audit-baseline.json, the two
     platform-k docs); MUST-HIT CONTROL: the same filter over PR 0's diff (kit pr0_parent..pr0_commit) leaves >= 1 path outside it.
  P5 NO TRAILER on EVERY commit in develop..HEAD (`%(trailers)` empty, 0 Co-Authored-By); CONTROL kit trailer_control_commit prints one.
  P6 keys: title, body, branch and EVERY commit message carry KS-1404 as the ONLY hyphenated KS key (branch lower-case), no closing keyword;
     `Refs KS-1404` on its own line in the body.
  P7 PR 0 ABSENT: the anchoring / nft-certificate locks are not in the diff and blob-equal develop == HEAD; MUST-HIT: PR 0's own diff lists
     all 4 of kit pr0_files_all.
  P8 MODES: the 14 paths are 100644 at HEAD (git ls-tree); CONTROL kit mode_control_path reads 100755.
  P9 NO CREDENTIAL FILE / NO .gitignore NEGATION (Wednesday 01:5x AEDT: the bundle is a .crt because preflight leg 9 refuses a tracked
     .pem): 0 .gitignore paths in the diff, 0 added `!` lines, 0 credential-shaped paths (kit credential_ext_rx); CONTROL: the filter flags
     3 planted names. Leg 9 itself (no-tracked-credentials.sh) runs at the head in c2_legs_gateD2.sh `run` (want rc 0).
  INFO END_TREE: HEAD^{tree} (the squash lands on it while develop has not moved); develop^{tree} as the control that differs.
--pr-json f --files-json f: read the PULLS answers from files (offline controls; P2 then says OFFLINE). --base <sha>: judge P3 against this
base instead of kit base (a prediction run on the drafted first commit only; never on the gate).
Usage: c1_pin_gateD2.py --repo <clone> --pr <n> --head <40-hex> [--no-remote]   (rc 0 PASS / 1 FAIL / 2 usage / 3 API)
  --no-remote: skip P1/P2 (no ls-remote, no API) — for the drafter's prediction on an object-store commit before a PR exists."""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, git, now, Checks, gh_token, gh_get, has_commit, count_range

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--repo', '--pr', '--head')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO, PR, HEAD = opt('--repo'), opt('--pr'), opt('--head'); NOREM = '--no-remote' in A
if not re.fullmatch(r'\d+', PR) or not re.fullmatch(r'[0-9a-f]{40}', HEAD):
    print('REFUSING: --pr must be digits and --head 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
KB = opt('--base', K['base'])
C = Checks(); OFF = opt('--pr-json')
if NOREM:
    p = {'state': 'n/a', 'head': {'ref': K['branch_planned'], 'sha': HEAD}, 'base': {'ref': 'develop', 'sha': KB}, 'title': '', 'body': ''}; fl = None; tries = 0
elif OFF:
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
print('c1_pin_gateD2 %s | repo %s | PR #%s | HEAD %s | judged base %s%s' % (now(), REPO, PR, HEAD, KB[:12], ' | NO-REMOTE prediction (P1/P2/P4-API/P6-title-body not judged)' if NOREM else (' | OFFLINE %s' % OFF if OFF else '')))
br = p['head']['ref']
if NOREM:
    dev = KB
else:
    rc, ls, err = git(REPO, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + br, check=False)
    R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
    dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % PR); bh = R.get('refs/heads/' + br)
    C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None, 'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s' % (rc, PR, ph, br, bh, dev, HEAD))
    bok = re.match(K['branch_rx'], br) is not None
    C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['base']['sha'] == dev and p['head']['sha'] == HEAD and bok and p.get('commits') == K['n_commits'],
          'state %s | merged %s | base %s @ %s (== origin develop %s) | head.sha %s | branch %s ~ %s: %s | commits %s (want %d) | mergeable %s (%d read(s)) / %s | title %r' % (
              p['state'], p.get('merged'), p['base']['ref'], str(p['base']['sha'])[:12], p['base']['sha'] == dev, p['head']['sha'], br, K['branch_rx'], bok, p.get('commits'), K['n_commits'],
              p.get('mergeable'), tries, p.get('mergeable_state'), p.get('title')))
hc = has_commit(REPO, HEAD); dc = has_commit(REPO, dev or '0' * 40)
numstat = []; names = []; chain = []
if not (hc and dc):
    C.chk('P3 shape', False, 'HEAD present %s | develop %s present %s — fetch refs/pull/%s/head and develop into YOUR clone first' % (hc, dev, dc, PR))
else:
    chain = [l.split() for l in git(REPO, 'log', '--format=%H %P', '%s..%s' % (dev, HEAD)).splitlines() if l.strip()]   # newest first
    linear = all(len(c) == 2 for c in chain) and all(chain[i][1] == chain[i + 1][0] for i in range(len(chain) - 1))
    first_parent = chain[-1][1] if chain else None; behind = count_range(REPO, HEAD, dev)
    C.chk('P3 shape', len(chain) == K['n_commits'] and linear and first_parent == dev and behind == 0 and dev == KB,
          'develop..HEAD %d commit(s) (want %d) %s | linear one-parent chain %s | first commit parent %s == develop %s | behind %d | develop == judged base %s: %s%s' % (
              len(chain), K['n_commits'], [c[0][:12] for c in chain], linear, (first_parent or '?')[:12], dev[:12], behind, KB[:12], dev == KB,
              '' if dev == KB else '  <- STALE BASE: repin_base_gateD2.py --new-develop %s (README section 7); never guessed' % dev))
    numstat = [l.split('\t') for l in git(REPO, 'diff', '--numstat', dev, HEAD).splitlines() if l]
    names = [l for l in git(REPO, 'diff', '--name-only', dev, HEAD).splitlines() if l]
    print('INFO END_TREE: HEAD^{tree} %s | develop^{tree} %s (the control that differs)' % (git(REPO, 'rev-parse', HEAD + '^{tree}').strip(), git(REPO, 'rev-parse', dev + '^{tree}').strip()))
    for c in reversed(chain):
        cn = [l for l in git(REPO, 'diff', '--name-status', c[1], c[0]).splitlines() if l]
        print('INFO commit %s (parent %s) %r: %d path(s) %s' % (c[0][:12], c[1][:12], git(REPO, 'log', '-1', '--format=%s', c[0]).strip()[:90], len(cn), [x.replace('\t', ' ') for x in cn]))
    if chain:
        fc = chain[-1][0]
        for l in git(REPO, 'diff', '--numstat', dev, fc).splitlines():
            a, d, f = l.split('\t'); cl = K['numstat_claim_first_commit'].get(f)
            print('INFO P4 first-commit claim %s: +%s/-%s | builder %s%s' % (f, a, d, '+%d/-%d' % tuple(cl) if cl else 'NONE', '' if cl and [int(a), int(d)] == cl else '  <- DIFFERS'))
        if len(chain) >= 2:
            sc = [l.split('\t', 1)[1] for l in git(REPO, 'diff', '--name-status', chain[-1][0], chain[0][0]).splitlines() if l.startswith('A\t')]
            print('INFO second-commit ADDED paths %s | kit expects %s: %s' % (sc, K['files_second_commit_expected'], sorted(sc) == sorted(K['files_second_commit_expected'])))
loc = sorted((x[2], int(x[0]), int(x[1])) for x in numstat if x[0].isdigit())
if fl is None:
    C.chk('P4 files', [x[0] for x in loc] == sorted(K['files']), 'NO-REMOTE: clone numstat %d paths %s | want exactly the %d kit paths | missing %s | extra %s' % (
        len(loc), ['%s +%d/-%d' % x for x in loc], len(K['files']), sorted(set(K['files']) - set(x[0] for x in loc)), sorted(set(x[0] for x in loc) - set(K['files']))))
else:
    api = sorted((f['filename'], f['additions'], f['deletions']) for f in fl)
    C.chk('P4 files', [x[0] for x in api] == sorted(K['files']) and api == loc, 'API %s | clone numstat %s | want exactly %s' % (['%s +%d/-%d' % x for x in api], ['%s +%d/-%d' % x for x in loc], sorted(K['files'])))
rx = re.compile(K['path_allow_rx'])
out = [n for n in names if not rx.search(n)]
ctl = [l for l in git(REPO, 'diff', '--name-only', K['pr0_parent'], K['pr0_commit']).splitlines() if l and not rx.search(l)] if has_commit(REPO, K['pr0_parent']) else []
C.chk('P4b path gate', bool(names) and not out and len(ctl) >= 1, 'paths outside the allow-set %d %s (of %d) | MUST-HIT CONTROL PR 0 diff %s..%s leaves %d outside it %s' % (
    len(out), out, len(names), K['pr0_parent'][:12], K['pr0_commit'][:12], len(ctl), ctl))
def trailers(sha):
    t = git(REPO, 'log', '-1', '--format=%(trailers)', sha).strip(); m = git(REPO, 'log', '-1', '--format=%B', sha)
    return t, len(re.findall(r'(?im)^co-authored-by:', m)), m
ct, cn, _ = trailers(K['trailer_control_commit'])
msgs = {}
if chain:
    bad = []
    for c in chain:
        t, nn, m = trailers(c[0]); msgs[c[0][:12]] = m
        if t or nn: bad.append((c[0][:12], t[:60], nn))
    C.chk('P5 no trailer', not bad and cn >= 1, 'commits with a trailer or Co-Authored-By: %s of %d | CONTROL %s prints %r (%d)' % (bad or 'NONE', len(chain), K['trailer_control_commit'], ct[:60], cn))
else:
    C.chk('P5 no trailer', False, 'no commits read | CONTROL %s prints %r (%d)' % (K['trailer_control_commit'], ct[:60], cn))
own = K['ticket']; body = p.get('body') or ''
surf = {'branch': br}
if not NOREM: surf.update({'title': p.get('title') or '', 'body': body})
for k, m in msgs.items(): surf['commit %s' % k] = m
for s, t in surf.items():
    ks = sorted(set(re.findall(r'\bKS-\d+\b', t))); cl = re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[:\s]+(KS-\d+|#\d+)', t)
    C.chk('P6 keys %s' % s, (ks == [own] or (s == 'branch' and ks == [] and own.lower() in t)) and not cl, 'hyphenated keys %s (want exactly [%s]) | closing keyword %s' % (ks, own, cl or 'NONE'))
if not NOREM:
    rl = re.search(r'(?m)^Refs %s\s*$' % own, body) is not None
    C.chk('P6 Refs line', rl, '`Refs %s` on its own line in the PR body: %s' % (own, rl))
    print('INFO P6 de-hyphenated keys in the body (context): %s' % sorted(set(re.findall(r'\bKS \d+\b', body))))
if hc and dc:
    hit = sorted(set(names) & set(K['pr0_files_absent']))
    ctl4 = [l for l in git(REPO, 'diff', '--name-only', K['pr0_parent'], K['pr0_commit']).splitlines() if l in K['pr0_files_all']] if has_commit(REPO, K['pr0_parent']) else []
    def bl(c, f):
        rc2, o, _ = git(REPO, 'cat-file', '-e', '%s:%s' % (c, f), check=False)
        return git(REPO, 'rev-parse', '%s:%s' % (c, f)).strip() if rc2 == 0 else 'ABSENT'
    eq = {f.split('/')[-2]: bl(dev, f) == bl(HEAD, f) for f in K['pr0_files_absent']}
    C.chk('P7 PR 0 locks absent', not hit and all(eq.values()) and len(ctl4) == 4, 'anchoring / nft-certificate locks in develop..HEAD: %s | blob-equal %s | MUST-HIT PR 0 diff lists %d of 4' % (hit or 'NONE', eq, len(ctl4)))
    modes = {}
    for f in K['files'] + [K['mode_control_path']]:
        o = git(REPO, 'ls-tree', HEAD, '--', f).strip(); modes[f] = o.split()[0] if o else 'ABSENT'
    pm = [modes[f] for f in K['files']]; cm = modes[K['mode_control_path']]
    C.chk('P8 modes', all(m == '100644' for m in pm) and cm == '100755', 'the %d paths %s | CONTROL %s %s (want 100755)' % (len(pm), sorted(set(pm)) if len(set(pm)) == 1 else pm, K['mode_control_path'], cm))
else:
    C.chk('P7 PR 0 locks absent', False, 'objects missing'); C.chk('P8 modes', False, 'objects missing')
if names:
    crx = re.compile(K['credential_ext_rx'])
    gi = [nm for nm in names if nm.endswith('.gitignore')]
    neg = []
    for g_ in gi:
        neg += [l for l in git(REPO, 'diff', dev, HEAD, '--', g_).splitlines() if l.startswith('+!')]
    cred = [nm for nm in names if crx.search(nm)]
    ctl = [x for x in ('a/b/key.pem', 'c/.env.local', 'd/id_rsa', K['bundle']) if crx.search(x)]
    C.chk('P9 no credential file, no .gitignore negation', not gi and not neg and not cred and ctl == ['a/b/key.pem', 'c/.env.local', 'd/id_rsa'],
          '.gitignore paths in develop..HEAD %s | added `!` negation lines %s | credential-shaped paths %s | the bundle %s is a .crt (not matched) | CONTROL the filter flags 3 of 3 planted names %s; RUNTIME: preflight leg 9 (%s) rc 0 at the head is run by c2_legs_gateD2.sh run' % (
              gi or 'NONE', neg or 'NONE', cred or 'NONE', K['bundle'].split('/')[-1], ctl, K['leg9'].split('/')[-1]))
n = C.nfail()
print('PIN %s: %d FAIL of %d checks | PR #%s | HEAD %s | develop %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], (dev or '?')[:12]))
raise SystemExit(1 if n else 0)
