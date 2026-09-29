#!/usr/bin/env python3
"""predict_gate42.py — MEASURE the gate42 kit (the directory this script lives in; its PR set, tier, class, commit count, declared stacks (NONE),
declared overlaps (NONE), declared no-op paths (NONE) and DECLARED OPEN-PR OVERLAPS (kit.json `dead_open_declared`, mode open_manifest_overlap) are
kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json
(kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub
PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate40's predict (gate39 -> gate38 lineage) and re-keyed for gate42: ONE row of Seat B 43rd's queue, T1 — #1339 KS-1378 the
advisory bump Kam ruled (a) on card secuura-five-new-advisories-block-every-push-0929 (nodemailer 9 -> 10 MAJOR in services/auth, services/originate
and the root; morgan ^1.12.1 in ten services + a root override; ip-address ^10.5.1 overrides; undici ^7.29.1 SCOPED under jsdom): 14 package.json +
14 package-lock.json, ZERO source files. Measured over ITS develop merge-base (develop 8af6ab821600 itself at drafting) and merged over the CURRENT
develop. No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since, read by the PULLS API
every run): hard path-disjoint — EXCEPT the open PRs DECLARED under `dead_open_declared`, whose overlap with #1339 must EQUAL the declared path set
(measured in (c): an undeclared overlap refuses, and so does a declared path that no longer overlaps). The WIDEN census (kit.json `widen_rx` on
titles AND `widen_branch_rx` on branches — Seat B 43rd's `-b43-<n>`) is HARD: an open PR matching either outside this kit refuses.
TIER BY CLASS (kit.json `class`): `dependency-bump` (T1) changes EXACTLY the 28 manifest / lock paths declared below, and no other file.
STANDING REQUIREMENTS: the CROSS-PACKAGE CENSUS — for every changed path, `git grep -l` of its Blockchain/Dev-relative spelling (and its
`<dir>/package-lock.json` / `<dir>/package.json` form) over every *.test.ts / *.test.js / *.test.mjs / *.test.sh / __tests__/*.sh at the head —
the gate runs EVERY suite so named. The LOCK READ: every package-lock.json under Blockchain/Dev at base and head, every copy of nodemailer / morgan /
ip-address / undici by lock path and version, judged against the first patched versions the seat read from the GitHub advisories API (typed from
the commit message: a PREDICTION; the gate's instrument is the repo's own audit legs 6 and 7). The drafter's clean standalone installs are
MEASURED by installprobe_gate42.py (run AFTER this script; its JSON is read here when present).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths) and `noop_paths` are SEPARATE keys; gate42 declares neither,
and (c) asserts that none is needed.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate42 / Seat B 43rd and is checked by rekey_check_gate42.py (which carries its own name in its own token map, and gate40's and gate39's namespaces).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g42_sp/clone.git — `git clone --bare --shared
--no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's
core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout. The scratchpad MUST be on the
Data volume (/private/tmp/...).

BASE-INVARIANT over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY; disjoint from every other open PR except the declared overlaps. READ
probes (PREDICTIONS for the gate, never evidence) are printed. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate42.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib, http.client

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate42.py <scratchpad> [--simulate …]'); sys.exit(9)
SIM = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--simulate' else 'none'
NS = sorted(K['prs']); SIB = K['sibling_batch']; INF = K['inflight']; DOS = K.get('dead_open_declared', {}); ST = K.get('stacks', {})
DOV = K.get('declared_overlap', {}); NOOP = K.get('noop_paths', {})
FAIL = 0
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
QUIET = False   # set only around a control that MUST fire: its planted FAIL prints as `(control fires)` and is not counted
def hard(ok, msg):
    global FAIL
    print('  %s %s' % ('PASS' if ok else ('(control fires)' if QUIET else 'FAIL'), msg))
    if not ok: FAIL += 1
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0: print('  CMD FAILED rc %d: %s\n%s' % (r.returncode, ' '.join(cmd[:6]), r.stderr[-800:])); sys.exit(1)
    return r.stdout
CL = os.path.join(SP, 'g42_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate42 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

print('--- (a) heads and develop: the PULLS API, then ls-remote (the checkout, READ), then a fetch FROM ORIGIN into the scratch clone')
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
def api(u):
    for i in range(4):   # a 5xx from GitHub is retried (3 x 10 s), never read as an answer
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            print('  (GitHub %d on %s — retry %d)' % (e.code, u, i + 1)); time.sleep(10)
        except (urllib.error.URLError, ConnectionError, TimeoutError, http.client.HTTPException) as e:   # a dropped connection is retried, never read as an answer (drafting slip: a RemoteDisconnected killed a simulation)
            if i == 3: raise
            print('  (GitHub transport error %s on %s — retry %d)' % (type(e).__name__, u, i + 1)); time.sleep(10)
OPEN = api('pulls?state=open&per_page=100&sort=created&direction=desc')
NEWOPEN = sorted((str(x['number']) for x in OPEN if str(x['number']) not in set(NS + SIB + INF) | set(DOS)), key=int, reverse=True)
if NEWOPEN: print('  NEW open PR(s) since the kit was drafted, censused here for path-disjointness: %s' % NEWOPEN)
INF = INF + NEWOPEN
WRX = K.get('widen_rx', r'(?!x)x'); WBX = K.get('widen_branch_rx', r'(?!x)x')
WID = [(str(x['number']), x['head']['sha'], x['head']['ref'], x['title']) for x in OPEN if re.match(WRX, x['title']) or re.search(WBX, x['head']['ref'])]
hard(all(w[0] in NS + SIB for w in WID), 'WIDEN census (open PRs whose title matches %r or whose branch matches %r): %s — every one is in this kit (a WIDEN PR outside it needs a re-draft that adds its cell)' % (WRX, WBX, [w[:3] for w in WID] or 'NONE'))
AP = {n: api('pulls/' + n) for n in NS + SIB + INF + sorted(DOS)}
for n in NS:
    if n in ST:
        par = ST[n]
        hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == AP[par]['head']['ref'] and AP[n]['base']['sha'] == AP[par]['head']['sha'],
             '#%s open, not draft, STACKED: API base.ref %s == #%s\'s branch %s AND base.sha %s == #%s\'s head' % (n, AP[n]['base']['ref'], par, AP[par]['head']['ref'], AP[n]['base']['sha'][:12], par))
    else:
        hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == 'develop', '#%s open, not draft, base develop (API; base.sha as GitHub last recorded it %s — informational, the merge-base below is measured)' % (n, AP[n]['base']['sha'][:12]))
for n in INF + sorted(DOS): print('  open #%s (censused, never pinned; its head may move): state %s head %s branch %s base %s' % (n, AP[n]['state'], AP[n]['head']['sha'], AP[n]['head']['ref'], AP[n]['base']['ref']))
BR = {n: 'refs/heads/' + AP[n]['head']['ref'] for n in NS}
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in NS + SIB + INF + sorted(DOS)] + [BR[n] for n in NS]
ls = run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs)
LS = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
env = dict(os.environ)
ssh = subprocess.run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand'], capture_output=True, text=True).stdout.strip()
if ssh: env['GIT_SSH_COMMAND'] = ssh
print('  core.sshCommand present: %s (value not printed)' % bool(ssh))
if not os.path.isdir(CL):
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    run(['git', 'clone', '-q', '--bare', '--shared', '--no-checkout', CHECKOUT, CL]); run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
alt = os.path.join(CL, 'objects', 'info', 'alternates')
altv = open(alt).read().split() if os.path.exists(alt) else []
hard(all(a == CHECKOUT + '/.git/objects' for a in altv), 'the scratch clone borrows objects ONLY from the checkout\'s own store, read-only (alternates %s)' % (altv or 'NONE'))
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g42/develop']
    + ['+refs/pull/%s/head:refs/g42/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g42/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g42/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g42/pull/' + n).strip() == g('rev-parse', 'refs/g42/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
HEX40 = re.compile(r'^[0-9a-f]{40}$')
def have_commit(c): return subprocess.run(['git', '--git-dir', CL, 'cat-file', '-e', c + '^{tree}'], capture_output=True).returncode == 0   # a commit OR a tree (merged trees are read too)
def blob(c, p):
    """the blob at <c>:<p>, None if the path is absent there; a HARD FAIL (never 'different') if <c> is not in the clone"""
    if not have_commit(c):
        hard(False, 'UNFETCHED: commit %s is not in the scratch clone — a blob read of %s there would not be a blob (STANDING_LINES 2026-09-27)' % (c[:12], p)); return 'UNFETCHED'
    rc, o, _ = gq('rev-parse', '--verify', '-q', '%s:%s' % (c, p)); o = o.strip()
    if rc != 0: return None
    if not HEX40.match(o) or g('cat-file', '-t', o).strip() != 'blob':
        hard(False, 'rev-parse %s:%s answered %r — not a blob id' % (c[:12], p, o[:60])); return 'NOTABLOB'
    return o
BOGUS = ''.join('0123456789abcdef'[(int(c, 16) + 7) % 16] for c in DEV)   # a 40-hex sha derived from develop, never develop itself
_f0 = FAIL; QUIET = True
_b = blob(BOGUS, 'README.md'); _fired = (FAIL == _f0 + 1 and _b == 'UNFETCHED'); FAIL = _f0; QUIET = False
hard(_fired and BOGUS != DEV and not have_commit(BOGUS), 'CONTROL (unfetched-object guard): blob() on a sha the clone does not hold (%s…) FIRES as UNFETCHED (%s), never returns a value an equality could read as "different"' % (BOGUS[:12], _b))
def synth(parent, path, body, msg):
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body).strip()
    idx = tempfile.mktemp(prefix='g42idx', dir=os.path.join(SP, 'g42_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE42-SIMULATED-MOVE.txt', 'gate42 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate42 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE42-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate42 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate42 SIMULATION ' + SIM)
    print('  SIMULATION %s: develop := %s (a foreign edit of %s)' % (SIM, DEV, path))
DT = g('rev-parse', DEV + '^{tree}').strip()
print('  develop %s tree %s | %s' % (DEV, DT, g('log', '-1', '--format=%s', DEV).strip()))

print('--- (b) per PR: shape (declared commit count over its develop merge-base, no merge commit), own paths, BASE-INVARIANT over the CURRENT develop')
P = {}
def numstat(a, b): return sorted(g('diff', '--numstat', a, b).strip().splitlines())
for n in NS:
    h = H[n]; dmb = g('merge-base', DEV, h).strip()
    par = ST.get(n)
    cb = H[par] if par else dmb
    if par:
        hard(gq('merge-base', '--is-ancestor', H[par], h)[0] == 0 and dmb == P[par]['develop_merge_base'],
             '#%s STACK: #%s\'s head %s is an ancestor of #%s\'s head, and both share the develop merge-base %s' % (n, par, H[par][:12], n, dmb[:12]))
    cnt = int(g('rev-list', '--count', '%s..%s' % (cb, h)).strip()); merges = g('rev-list', '--merges', '%s..%s' % (cb, h)).split()
    chain = g('rev-list', '--reverse', '%s..%s' % (cb, h)).split()
    hard(cnt == K['prs'][n]['commits'] and not merges and chain and g('rev-parse', chain[0] + '^').strip() == cb,
         '#%s is %d commit(s) (declared %d) on %s %s, no merge commit, the first commit\'s parent == that base' % (n, cnt, K['prs'][n]['commits'], ('#%s\'s head' % par) if par else 'merge-base', cb[:12]))
    own = sorted(g('diff', '--name-only', cb, h).split())
    move = sorted(g('diff', '--name-only', dmb, DEV).split())
    ov = sorted(set(own) & set(move))
    res = {'head': h, 'branch': BR[n], 'merge_base': cb, 'develop_merge_base': dmb, 'stacked_on': par, 'commits': chain, 'paths': own, 'numstat': numstat(cb, h),
           'ahead': int(g('rev-list', '--count', '%s..%s' % (cb if par else DEV, h)).strip()), 'behind': int(g('rev-list', '--count', '%s..%s' % (h, cb if par else DEV)).strip()),
           'move_paths': len(move), 'move_commits': int(g('rev-list', '--count', '%s..%s' % (dmb, DEV)).strip()), 'overlap_with_move': ov,
           'msg_keys': sorted(set(re.findall(r'KS-\d+', g('log', '--format=%B', '%s..%s' % (cb, h))))),
           'subjects': [s for s in g('log', '--reverse', '--format=%s', '%s..%s' % (cb, h)).splitlines()]}
    side = P[par]['merged_tree'] if par else DEV
    rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + cb, side, h)
    hard(rc == 0, '#%s merges CLEAN over %s with its own merge-base %s (merge-tree rc %d; develop moved %d commit(s), %d path(s) since it)' % (n, 'develop', cb[:12], rc, res['move_commits'], len(move)))
    mt = o.split()[0] if (o and rc == 0) else ''; res['merged_tree'] = mt
    if not mt:
        print('  (#%s: not a clean merge — its blob checks are not reachable; REFUSED above)' % n); P[n] = res; continue
    changed = sorted(g('diff', '--name-only', side, mt).split())
    hard(changed == own, '#%s (1) diff(develop, merged) == its own %d path(s) %s' % (n, len(own), own))
    res['merged_blobs'] = {}
    for p in own:
        mbl, hbl = blob(mt, p), blob(h, p)
        hard(mbl == hbl, '#%s (1) merged blob == head blob %s for %s' % (n, (hbl or 'DELETED')[:12], p))
        res['merged_blobs'][p] = {'merged': mbl, 'head': hbl, 'target': 'head blob', 'develop': blob(DEV, p), 'merge_base': blob(cb, p)}
    hard(numstat(side, mt) == res['numstat'], '#%s (2) numstat(develop -> merged) == numstat(merge-base -> head) %s' % (n, res['numstat']))
    modes = g('diff', '--summary', side, mt).strip()
    hard('mode change' not in modes, '#%s no mode change (%s)' % (n, modes.replace('\n', ' | ') or 'none'))
    hard(not ov, '#%s (3) develop move since %s ∩ own paths == %s (no declared overlap, no declared no-op path in this kit)' % (n, dmb[:12], ov or 'EMPTY'))
    P[n] = res
MB = sorted({P[n]['develop_merge_base'] for n in NS})
print('  MERGE-BASES (measured): %s — %s' % ({m[:12]: ['#' + n for n in NS if P[n]['develop_merge_base'] == m] for m in MB}, 'ONE shared merge-base for all %d PRs' % len(NS) if len(MB) == 1 else '%d distinct merge-bases' % len(MB)))
print('  THE DEVELOP MOVE since the oldest merge-base (READ, `git log --first-parent`): %s' % [l for l in g('log', '--first-parent', '--format=%h %s', '%s..%s' % (MB[0], REAL_DEV)).splitlines()][:12])

print('--- (c) NOT STACKED, PAIRWISE disjoint; the declaration keys (declared_overlap = merged_blob_paths class; noop_paths = the squash-stack NO-OP class)')
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g42/pull/' + n).strip()
def paths_of(n):
    h = head_of(n); mb = g('merge-base', REAL_DEV, h).strip(); return set(g('diff', '--name-only', mb, h).split())
OWN = {n: set(P[n]['paths']) for n in NS}
INFP = {n: paths_of(n) for n in INF}
def declared(a, b): return ST.get(b) == a or ST.get(a) == b
for a, b in itertools.combinations(NS, 2):
    ha, hb = head_of(a), head_of(b)
    anc_ab = gq('merge-base', '--is-ancestor', ha, hb)[0] == 0; anc_ba = gq('merge-base', '--is-ancestor', hb, ha)[0] == 0
    mab = g('merge-base', ha, hb).strip()
    hard(not declared(a, b) and not anc_ab and not anc_ba and gq('merge-base', '--is-ancestor', mab, REAL_DEV)[0] == 0, 'NOT STACKED #%s/#%s: neither head is the other\'s ancestor; their merge-base %s is on develop' % (a, b, mab[:12]))
    hard(not (OWN[a] & OWN[b]), 'kit pair #%s/#%s disjoint %s' % (a, b, sorted(OWN[a] & OWN[b]) or ''))
for a in NS:
    for b in INF: hard(not (OWN[a] & INFP[b]), '#%s vs open #%s (head %s) disjoint %s' % (a, b, head_of(b)[:12], sorted(OWN[a] & INFP[b]) or ''))
DOSP = {b: paths_of(b) for b in sorted(DOS)}
for a in NS:
    for b in sorted(DOS):
        meas = sorted(OWN[a] & DOSP[b]); decl = sorted(DOS[b].get('paths', []))
        hard(bool(meas) and meas == decl, 'DECLARED OPEN-PR OVERLAP #%s vs open #%s (head %s, mode %s, NOT in this kit, never merged by it): measured %s == declared %s' % (
            a, b, head_of(b)[:12], DOS[b].get('mode'), [x.replace('Blockchain/Dev/', '') for x in meas], 'EQUAL' if meas == decl else [x.replace('Blockchain/Dev/', '') for x in decl]))
NEED_NOOP = {n: [p for p in P[n]['paths'] if P[n].get('merged_blobs', {}).get(p, {}).get('head') == P[n].get('merged_blobs', {}).get(p, {}).get('develop')] for n in NS}
NEED_OV = {n: [p for p in P[n]['paths'] if P[n].get('merged_blobs', {}).get(p, {}).get('merged') != P[n].get('merged_blobs', {}).get(p, {}).get('head')] for n in NS}
hard(not any(NEED_NOOP.values()) and not NOOP, 'noop_paths: no kit path has head blob == develop blob (a squash no-op) %s, and kit.json declares none %s — a merge tool reads `noop_paths` as EMPTY' % ({k: v for k, v in NEED_NOOP.items() if v} or 'NONE', NOOP or '{}'))
hard(not any(NEED_OV.values()) and not DOV, 'declared_overlap (merged_blob_paths): no kit path merges to a blob other than its head blob %s, and kit.json declares none %s — a merge tool reads `merged_blob_paths` as EMPTY' % ({k: v for k, v in NEED_OV.items() if v} or 'NONE', DOV or '{}'))

print('--- (d) END_TREE over develop, every order (memoised)')
MEMO = {}
def cbase(n): return H[ST[n]] if n in ST else g('merge-base', DEV, H[n]).strip()
def step(t, n):
    k = (t, n)
    if k not in MEMO:
        rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + cbase(n), t, H[n])
        MEMO[k] = o.split()[0] if rc == 0 else None
    return MEMO[k]
def seq(base_tree, order):
    t = base_tree
    for n in order:
        t = step(t, n)
        if t is None: return None
    return t
perms = [o for o in itertools.permutations(NS) if all(o.index(ST[c]) < o.index(c) for c in ST if c in o and ST[c] in o)]
ends = {seq(DT, o) for o in perms}
hard(len(ends) == 1 and None not in ends, 'END_TREE identical in all %d orders (%d distinct merge-tree calls): %s' % (len(perms), len(MEMO), sorted(x or 'CONFLICT' for x in ends)))
END = ends.pop() if len(ends) == 1 else None
st = g('diff', '--shortstat', DT, END).strip() if END else ''
if END:
    endp = sorted(g('diff', '--name-only', DT, END).split()); allown = sorted(set().union(*OWN.values()))
    hard(endp == allown and all(blob(END, p) == P[n]['merged_blobs'][p]['head'] for n in NS for p in P[n]['paths']),
         'END_TREE: diff(develop, END) == the union of the %d own path sets' % len(NS) + '  (%d paths), every END blob == its PR\'s head blob (MG-1: ONE target per file, the head blob)' % len(allown))
RT = {}
print('  END_TREE %s (%s)' % (END, st))

print('--- (e) READ probes (PREDICTIONS for the gate; never evidence, unless the line says the drafter MEASURED it)')
def show(c, p):
    rc, o, _ = gq('show', '%s:%s' % (c, p)); return o if rc == 0 else ''
def pm(lines): return [l for l in lines if l and l[0] in '+-' and not l.startswith(('+++', '---'))]   # NEVER l[:1] in '+-'
def pm_diff(a, b, pth):
    return pm(g('diff', '-U0', a, b, '--', pth).splitlines())
def cmp_seq(x, y): return 'IDENTICAL' if x == y else 'DIFFER'
DR = 'Blockchain/Dev/'
WS = ['', 'frontend/issuer', 'packages/shared', 'services/anchoring', 'services/api-gateway', 'services/auth', 'services/demo-service', 'services/guardian',
      'services/m365-integration', 'services/originate', 'services/prism', 'services/queue', 'services/security', 'services/timestamping']
def wp(w, f): return DR + (w + '/' if w else '') + f
MORGAN10 = ['services/anchoring', 'services/api-gateway', 'services/auth', 'services/demo-service', 'services/guardian', 'services/m365-integration', 'services/prism',
            'services/queue', 'services/security', 'services/timestamping']
NODEMAILER = ['', 'services/auth', 'services/originate']
TIER_OF = {'dependency-bump': 'T1'}
DECL = {'dependency-bump': {'prod': sorted(wp(w, f) for w in WS for f in ('package.json', 'package-lock.json')), 'doc': [], 'tests': []}}
BASELINE = DR + 'scripts/audit/audit-baseline.json'
CLEANUP = ['GHSA-v2v4-37r5-5v8g', 'GHSA-mwp4-54f8-5fhr']
FIVE = ['GHSA-rpw4-54j3-4h4q', 'GHSA-2vr4-cq9g-pvrc', 'GHSA-9f6g-j8ch-79g4', 'GHSA-6vj9-mwq6-2f5v', 'GHSA-3wwx-pv8p-q78v']
PKGS = ('nodemailer', 'morgan', 'ip-address', 'undici')
def vt(v): return tuple(int(x) for x in re.findall(r'\d+', v or '')[:3]) or (0,)
def vulnerable(pkg, v):
    """the seat's advisory ranges (commit message: first patched nodemailer 10.0.2, morgan 1.12.1, ip-address 10.5.1, undici 6.28.1/7.29.1/8.10.2; every
    undici range starts at 6.25.0) — TYPED from the commit message, a PREDICTION; the gate's instrument is audit legs 6 and 7"""
    t = vt(v)
    if pkg == 'nodemailer': return t < (10, 0, 2)
    if pkg == 'morgan': return t < (1, 12, 1)
    if pkg == 'ip-address': return t < (10, 5, 1)
    if pkg == 'undici': return (6, 25, 0) <= t and t < {6: (6, 28, 1), 7: (7, 29, 1), 8: (8, 10, 2)}.get(t[0], (0,))
    return False
CTL_V = (vulnerable('nodemailer', '9.1.1') and not vulnerable('nodemailer', '10.0.12') and vulnerable('morgan', '1.12.0') and not vulnerable('morgan', '1.12.1')
         and vulnerable('ip-address', '9.0.5') and vulnerable('ip-address', '10.4.0') and not vulnerable('ip-address', '10.5.1') and not vulnerable('undici', '5.29.0')
         and vulnerable('undici', '7.29.0') and not vulnerable('undici', '7.29.1') and vulnerable('undici', '6.25.0') and not vulnerable('undici', '6.28.1'))
hard(CTL_V, 'CONTROL (the vulnerable-range predicate): 9.1.1 / 1.12.0 / 9.0.5 / 10.4.0 / 7.29.0 / 6.25.0 read VULNERABLE; 10.0.12 / 1.12.1 / 10.5.1 / 5.29.0 / 7.29.1 / 6.28.1 read patched')
def lockrows(c, p):
    t = show(c, p)
    try: j_ = json.loads(t)
    except Exception: return None
    rows = []
    for k, v in (j_.get('packages') or {}).items():
        nm = k.rsplit('node_modules/', 1)[-1] if k else ''
        if nm in PKGS and isinstance(v, dict) and v.get('version'): rows.append((nm, k, v['version']))
    return sorted(rows)
CTL_PM = (cmp_seq(pm(['+a', '-b', '+c', '']), pm(['+a', '-b', '+c'])) == 'IDENTICAL' and cmp_seq(pm(['+a', '-b', '+c']), pm(['+a', '-b', '+C'])) == 'DIFFER' and len([l for l in ['+a', ''] if l[:1] in '+-']) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, "CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in '+-'` would have counted the empty line — the kit uses `l and l[0] in '+-'`")
def grep_l(rev, frag, *globs):
    rc_, o_, _ = gq('grep', '-l', '-F', frag, rev, '--', *globs); return sorted(x.split(':', 1)[1] for x in o_.strip().splitlines() if x)
TGLOBS = ('Blockchain/Dev/*.test.ts', 'Blockchain/Dev/*.test.js', 'Blockchain/Dev/*.test.mjs', 'Blockchain/Dev/*.test.sh', 'Blockchain/Dev/*/__tests__/*.sh')
IPJ = os.path.join(GS, 'installprobe_gate42.json'); IPR = json.load(open(IPJ)) if os.path.exists(IPJ) else None
PROBES, MEAS = {}, {}
for n in NS:
    h = H[n]; cb = P[n]['merge_base']; cls = K['prs'][n]['class']; out = []; MEAS[n] = {}
    d = DECL[cls]
    hard(sorted(P[n]['paths']) == sorted(d['prod'] + d['doc'] + d['tests']) and TIER_OF[cls] == K['prs'][n]['tier'],
         '#%s TIER BY CLASS %s (%s): changes EXACTLY the %d declared manifest / lock paths (%d workspaces x package.json + package-lock.json)' % (n, cls, TIER_OF[cls], len(d['prod']), len(WS)))
    hard(all(os.path.basename(p) in ('package.json', 'package-lock.json') for p in P[n]['paths']), '#%s ZERO source files: every own path is a package.json or a package-lock.json' % n)
    # the manifests, verbatim +/- (READ)
    for w in WS:
        out.append('MANIFEST %s: %s' % (w or '(root)', [l.strip() for l in pm_diff(cb, h, wp(w, 'package.json'))]))
    mg = {w: [re.sub(r'\s+', '', l) for l in pm_diff(cb, h, wp(w, 'package.json')) if '"morgan"' in l] for w in WS}
    mdecl = sorted(w for w in WS[1:] if json.loads(show(h, wp(w, 'package.json')) or '{}').get('dependencies', {}).get('morgan'))
    hard(mdecl == MORGAN10 and all(mg[w] == ['-"morgan":"^1.10.0",', '+"morgan":"^1.12.1",'] for w in MORGAN10) and mg[''] == ['+"morgan":"^1.12.1",'],
         '#%s MORGAN: the declarers at head are EXACTLY the ten (%s); each moves `"morgan": "^1.10.0"` -> `"^1.12.1"`; the root adds the override `"morgan": "^1.12.1"` (the seat: redundant now, kept as a guard — the EOVERRIDE source)' % (n, ', '.join(x.split('/')[-1] for x in MORGAN10)))
    nmd = {w: json.loads(show(h, wp(w, 'package.json')) or '{}').get('dependencies', {}).get('nodemailer') for w in NODEMAILER}
    nmb = {w: json.loads(show(cb, wp(w, 'package.json')) or '{}').get('dependencies', {}).get('nodemailer') for w in NODEMAILER}
    hard(all(v == '^10.0.12' for v in nmd.values()) and all(v == '^9.0.3' for v in nmb.values()), '#%s NODEMAILER declared base -> head (root, auth, originate): %s -> %s' % (n, nmb, nmd))
    rj = json.loads(show(h, wp('', 'package.json')) or '{}'); ij = json.loads(show(h, wp('frontend/issuer', 'package.json')) or '{}')
    ov = {'root': {k: rj.get('overrides', {}).get(k) for k in ('morgan', 'ip-address', 'jsdom', 'undici')}, 'frontend/issuer': ij.get('overrides'),
          'packages/shared': json.loads(show(h, wp('packages/shared', 'package.json')) or '{}').get('overrides', {}).get('ip-address'),
          'services/anchoring': json.loads(show(h, wp('services/anchoring', 'package.json')) or '{}').get('overrides', {}).get('ip-address')}
    hard(ov['root']['undici'] is None and ov['root']['jsdom'] == {'undici': '^7.29.1'} and (ov['frontend/issuer'] or {}).get('jsdom') == {'undici': '^7.29.1'} and not (ov['frontend/issuer'] or {}).get('undici'),
         '#%s UNDICI override SCOPED to jsdom (root and frontend/issuer: `jsdom: {undici: ^7.29.1}`, NO top-level `undici` override): %s' % (n, ov))
    out.append('OVERRIDES at head (READ): %s' % ov)
    # every lock under Blockchain/Dev, base and head: each copy of the four packages by path and version
    locks_h = sorted(x for x in g('ls-tree', '-r', '--name-only', h, 'Blockchain/Dev').split() if x.endswith('package-lock.json') and '/node_modules/' not in x)
    locks_b = sorted(x for x in g('ls-tree', '-r', '--name-only', cb, 'Blockchain/Dev').split() if x.endswith('package-lock.json') and '/node_modules/' not in x)
    hard(locks_h == locks_b, '#%s the lock SET is unchanged base -> head (%d package-lock.json under Blockchain/Dev; the PR edits 14 of them, adds / removes none)' % (n, len(locks_h)))
    VB, VH, unparsed, per = [], [], [], {}
    for lp in locks_h:
        rb, rh = lockrows(cb, lp), lockrows(h, lp)
        if rb is None or rh is None: unparsed.append(lp); continue
        VB += [(lp,) + r for r in rb if vulnerable(r[0], r[2])]; VH += [(lp,) + r for r in rh if vulnerable(r[0], r[2])]
        if lp in P[n]['paths']:
            per[lp] = {pk: ('%s -> %s' % (sorted({r[2] for r in rb if r[0] == pk}) or '-', sorted({r[2] for r in rh if r[0] == pk}) or '-')) for pk in PKGS if any(r[0] == pk for r in rb + rh)}
    hard(not unparsed, '#%s every lock parses as JSON at base and head (unparsed: %s)' % (n, unparsed or 'none'))
    hard(bool(VB), '#%s CONTROL (the lock read CAN see a vulnerable copy): at the BASE %d vulnerable copies across %d locks, e.g. %s' % (n, len(VB), len({x[0] for x in VB}), VB[:4]))
    ld = show(h, DR + 'scripts/audit/lock-discovery.mjs'); m_ = re.search(r'OUT_OF_SCOPE_LOCKS = new Map\(\[(.*?)\n\]\);', ld, re.S)
    OOS = sorted(set(re.findall(r"^  \[\n    '([^']+)',", m_.group(1), re.M))) if m_ else []
    inscope = lambda lp: not any(lp == o + '/package-lock.json' or lp.startswith(o + '/') for o in OOS)
    VHin, VHout = [x for x in VH if inscope(x[0])], [x for x in VH if not inscope(x[0])]
    hard(bool(OOS) and not VHin, '#%s at the HEAD ZERO copies of nodemailer / morgan / ip-address / undici in a vulnerable range across the %d IN-SCOPE locks under Blockchain/Dev (READ; the seat: "Zero vulnerable copies of any of the four remain"; out-of-scope trees READ from lock-discovery.mjs OUT_OF_SCOPE_LOCKS: %s): %s' % (n, len([x for x in locks_h if inscope(x)]), OOS, VHin[:6] or 'NONE'))
    out.append('OUT-OF-SCOPE LOCKS (READ, lock-discovery.mjs OUT_OF_SCOPE_LOCKS at head: %s — leg 7 does NOT audit them): copies in a vulnerable range by the seat\'s typed ranges at the head: %s — the seat\'s "zero vulnerable copies" is true IN SCOPE; the gate says whether that copy is inside the advisory\'s real range and whether the claim needs the qualifier' % (OOS, VHout or 'NONE'))
    MEAS[n]['out_of_scope_vulnerable'] = VHout
    for lp in sorted(per): out.append('LOCK %s (READ, base -> head): %s' % (lp.replace(DR, ''), per[lp]))
    # nodemailer: what each of the three declaring locks resolves at the top level
    nml = {w or '(root)': ([r[2] for r in (lockrows(cb, wp(w, 'package-lock.json')) or []) if r[1] == 'node_modules/nodemailer'], [r[2] for r in (lockrows(h, wp(w, 'package-lock.json')) or []) if r[1] == 'node_modules/nodemailer']) for w in NODEMAILER}
    hard(all(b_ == ['9.1.1'] and len(h_) == 1 and vt(h_[0])[0] == 10 and vt(h_[0]) >= (10, 0, 2) for b_, h_ in nml.values()), '#%s NODEMAILER in the three declaring locks, node_modules/nodemailer base -> head: %s (a lock that says 10.x is NOT proof that 10.x RUNS — requirement 1)' % (n, nml))
    tyn = {s: json.loads(show(h, wp(s, 'package-lock.json')) or '{}').get('packages', {}).get('node_modules/@types/nodemailer', {}).get('version') for s in ('services/auth', 'services/originate')}
    out.append('TYPES (READ): @types/nodemailer at head %s beside nodemailer 10, which ships its OWN bundled declarations (10.0.0 "migrate to TypeScript"; 10.0.11 "restore the layout of @types/nodemailer in the bundled declarations") — the gate says which declarations tsc resolves for `import nodemailer from \'nodemailer\'` and `nodemailer.Transporter`' % tyn)
    # undici: the ROOT copy untouched, every jsdom-nested copy patched
    ru = lambda c, lp: [(r[1], r[2]) for r in (lockrows(c, lp) or []) if r[0] == 'undici']
    ub, uh = ru(cb, wp('', 'package-lock.json')), ru(h, wp('', 'package-lock.json'))
    top_b = [v for k, v in ub if k == 'node_modules/undici']; top_h = [v for k, v in uh if k == 'node_modules/undici']
    hard(top_b == top_h and len(top_h) == 1 and not vulnerable('undici', top_h[0]), '#%s UNDICI root copy node_modules/undici UNTOUCHED base -> head (%s -> %s) and outside every vulnerable range' % (n, top_b, top_h))
    jz = {lp.replace(DR, ''): ([x for x in ru(cb, lp) if 'jsdom' in x[0]], [x for x in ru(h, lp) if 'jsdom' in x[0]]) for lp in (wp('', 'package-lock.json'), wp('frontend/issuer', 'package-lock.json'))}
    nonj = {lp.replace(DR, ''): (sorted(x for x in ru(cb, lp) if 'jsdom' not in x[0]), sorted(x for x in ru(h, lp) if 'jsdom' not in x[0])) for lp in (wp('', 'package-lock.json'), wp('frontend/issuer', 'package-lock.json'))}
    hard(all(not any(vulnerable('undici', v) for k, v in hh) for bb, hh in jz.values()) and all(bb == hh for bb, hh in nonj.values()),
         '#%s UNDICI jsdom-nested copies base -> head %s; every NON-jsdom undici copy unchanged base -> head %s' % (n, jz, {k: v[1] for k, v in nonj.items()}))
    # ip-address: the @cardano-sdk nested copies and the 9.x copy
    ipb, iph = {}, {}
    for lp in locks_h:
        for r in (lockrows(cb, lp) or []):
            if r[0] == 'ip-address': ipb.setdefault(r[2], []).append('%s:%s' % (lp.replace(DR, ''), r[1]))
        for r in (lockrows(h, lp) or []):
            if r[0] == 'ip-address': iph.setdefault(r[2], []).append('%s:%s' % (lp.replace(DR, ''), r[1]))
    cardb = sorted(x for v in ipb.values() for x in v if '@cardano-sdk' in x); cardh = sorted(x for v in iph.values() for x in v if '@cardano-sdk' in x)
    hard(not any(vt(v)[0] == 9 for v in iph) and any(vt(v)[0] == 9 for v in ipb), '#%s IP-ADDRESS: a 9.x copy at the BASE (%s) and NONE at the head (versions at head: %s)' % (n, sorted(v for v in ipb if vt(v)[0] == 9), sorted(iph)))
    out.append('IP-ADDRESS (READ): versions base %s -> head %s; @cardano-sdk-nested copies base %d -> head %d (head: %s)' % ({k: len(v) for k, v in sorted(ipb.items())}, {k: len(v) for k, v in sorted(iph.items())}, len(cardb), len(cardh), cardh[:6]))
    # the audit baseline: NOT edited; the two CLEANUP rows present; none of the five new advisories baselined
    bb_, bh_ = blob(cb, BASELINE), blob(h, BASELINE)
    bt = show(h, BASELINE)
    hard(bb_ == bh_ and bb_ and all(x in bt for x in CLEANUP) and not any(x in bt for x in FIVE),
         '#%s AUDIT BASELINE %s BYTE-IDENTICAL base -> head (blob %s): no row added or edited; the two rows leg 6 now advises removing (%s) are STILL in it; none of the five new advisories is baselined' % (n, BASELINE.replace(DR, ''), (bh_ or 'ABSENT')[:12], ', '.join(CLEANUP)))
    # the audit legs, READ from preflight.sh at head: leg 6 = the npm-audit gate over the hoisted root tree, leg 7 = the standalone-lock audit
    pf = show(h, DR + 'scripts/preflight/preflight.sh').split('\n'); pj = json.loads(show(h, wp('', 'package.json')) or '{}').get('scripts', {})
    out.append('AUDIT LEGS (READ, preflight.sh at head): leg 6 :%s `%s`; leg 7 :%s `%s`; npm scripts audit:gate=`%s` audit:locks=`%s` audit:contract=`%s` — the gate RE-RUNS both legs at the head and at END_TREE (they call the npm advisory API)' % (
        [i + 1 for i, l in enumerate(pf) if re.match(r'^#\s+6\. ', l)], next((l.strip('# ') for l in pf if re.match(r'^#\s+6\. ', l)), '?')[:60], [i + 1 for i, l in enumerate(pf) if re.match(r'^#\s+7\. ', l)],
        next((l.strip('# ') for l in pf if re.match(r'^#\s+7\. ', l)), '?')[:60], pj.get('audit:gate'), pj.get('audit:locks'), pj.get('audit:contract')))
    # the nodemailer call sites (READ, head): unchanged by the PR; ONE createTransport per service
    for s in ('services/auth', 'services/originate'):
        ep = DR + s + '/src/services/email.ts'; et = show(h, ep)
        hard(blob(cb, ep) == blob(h, ep) and et.count('nodemailer.createTransport(') == 1 and et.count('.sendMail(') == 1,
             '#%s %s email.ts BYTE-IDENTICAL base -> head, ONE createTransport at :%s and ONE sendMail at :%s (the two call sites requirement 3 checks against the 9 -> 10 changelog)' % (
                 n, s, [i + 1 for i, l in enumerate(et.split('\n')) if 'nodemailer.createTransport(' in l], [i + 1 for i, l in enumerate(et.split('\n')) if '.sendMail(' in l]))
    # morgan call sites (READ, head)
    mc = [x for x in gq('grep', '-n', '-F', "morgan('", h, '--', 'Blockchain/Dev/services/*/src/*.ts', 'Blockchain/Dev/services/*/src/**/*.ts')[1].strip().splitlines() if x]
    out.append("MORGAN CALL SITES (READ, head): %s — every one the 'combined' preset (quoted referrer + user-agent: the advisory's quoted fields)" % [x.split(':', 1)[1][:90] for x in mc])
    # the CROSS-PACKAGE CENSUS: any test naming a changed path by its Blockchain/Dev-relative spelling
    cz = {}
    for p in P[n]['paths']:
        rel = p[len(DR):]; hits = set()
        for frag in (rel, './' + rel):
            for f in grep_l(h, frag, *TGLOBS): hits.add(f)
        if hits: cz[rel] = sorted(hits)
    broad = grep_l(h, 'package-lock.json', *TGLOBS)
    out.append('CROSS-PACKAGE CENSUS (READ, `git grep -l -F` of each changed path\'s Blockchain/Dev-relative spelling over *.test.ts|js|mjs|sh and __tests__/*.sh at head): %s | tests naming ANY package-lock.json (lock discovery / audit contract; the gate runs them): %s' % (cz or 'NONE by exact path', broad))
    MEAS[n]['census'] = {'exact': cz, 'broad': broad}
    # the suites a changed lock can break: every workspace whose lock changed, with its test script (READ)
    st_ = {}
    for w in WS[1:]:
        sj = json.loads(show(h, wp(w, 'package.json')) or '{}').get('scripts', {})
        st_[w] = sj.get('test')
    out.append('SUITES OWED (requirement 7; every workspace whose lock changed, its `test` script READ at head): %s — plus services/auth and services/originate on nodemailer 10 (requirement 2) and the root install' % st_)
    MEAS[n]['suites'] = st_
    # originate's `Cannot find module '../routes/anchors'` (the seat's PRE-EXISTING claim): READ what exists at base and head
    ob = [x for x in g('ls-tree', '-r', '--name-only', cb, DR + 'services/originate/src').split() if re.search(r'/(routes/anchors|services/provenance)\.(ts|js)$', x)]
    oh = [x for x in g('ls-tree', '-r', '--name-only', h, DR + 'services/originate/src').split() if re.search(r'/(routes/anchors|services/provenance)\.(ts|js)$', x)]
    imp = grep_l(h, "'../routes/anchors'", DR + 'services/originate/src/*.ts', DR + 'services/originate/src/**/*.ts')
    oj = json.loads(show(h, wp('services/originate', 'package.json')) or '{}'); ocfg = [os.path.basename(x) for x in g('ls-tree', '--name-only', h, DR + 'services/originate/').split() if re.search(r'(jest|vitest)[^/]*\.config\.[cm]?[jt]s$', x)]
    njm = len([x for x in grep_l(h, 'jest.mock(', DR + 'services/originate/src/*.test.ts', DR + 'services/originate/src/**/*.test.ts')]); nvi = len(grep_l(h, "from 'vitest'", DR + 'services/originate/src/*.test.ts', DR + 'services/originate/src/**/*.test.ts'))
    out.append("ORIGINATE '../routes/anchors' (READ): the modules exist at base %s and head %s (no source file changes); %d file(s) import '../routes/anchors' at head (e.g. %s). ORIGINATE'S RUNNER IS JEST, NOT VITEST: `test` = %r, devDependencies %s, config files %s; %d test file(s) call jest.mock( and %d import from 'vitest' — the seat's '93 files, no tests' reads like a VITEST run over a JEST suite (a PREDICTION): the gate runs `npm test` in services/originate (the runner its package.json names) at the BASE and the head" % (
        [os.path.basename(x) for x in ob], [os.path.basename(x) for x in oh], len(imp), [os.path.basename(x) for x in imp[:3]], oj.get('scripts', {}).get('test'),
        {d_: v_ for d_, v_ in oj.get('devDependencies', {}).items() if 'jest' in d_ or 'vitest' in d_}, ocfg, njm, nvi))
    MEAS[n]['originate_runner'] = oj.get('scripts', {}).get('test')
    # Kam's card (READ only)
    try:
        dj = json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json', encoding='utf-8')); found = {}
        def walk(x):
            if isinstance(x, dict):
                if x.get('id') in ('secuura-five-new-advisories-block-every-push-0929',):
                    found[x['id']] = '%s %s at %s' % (x.get('status'), x.get('ruled_choice'), x.get('ruled_ts'))
                for vv in x.values(): walk(vv)
            elif isinstance(x, list):
                for vv in x: walk(vv)
        walk(dj)
    except Exception as e: found = {'READ FAILED': str(e)[:80]}
    hard(found.get('secuura-five-new-advisories-block-every-push-0929', '').startswith('ruled a'), "#%s Kam's card (READ, decisions.json): %s" % (n, found))
    if IPR and '_summary' in IPR:
        out.append('THE CLEAN INSTALLS (MEASURED by the drafter, installprobe_gate42.py -> installprobe_1.out / installprobe_gate42.json; standalone `npm ci --ignore-scripts` of each service lock, npm %s, node %s; controls %s): %s — the gate re-measures from the ROOT install the suites run from' % (
            IPR.get('npm'), IPR.get('node'), 'ALL PASS' if all(IPR.get('controls', {}).values()) else IPR.get('controls'), IPR['_summary']))
        MEAS[n]['installprobe'] = {'summary': IPR['_summary']}
    else: out.append('THE CLEAN INSTALLS: installprobe_gate42.json ABSENT — UNMEASURED by the drafter')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))
ORDER_PROOF = {}
res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT, 'merge_bases': MB,
       'end_tree': END, 'end_tree_with_sibling': None, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES, 'measured': MEAS,
       'stacks': ST, 'retarget': RT, 'declared_overlap': DOV, 'noop_paths': NOOP, 'sibling_paths': {}, 'sibling_heads': {},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': {}, 'dead_open_declared': {b: {'head': head_of(b), 'state': AP[b]['state'], 'title': AP[b]['title'], 'overlap': sorted(set().union(*OWN.values()) & DOSP[b])} for b in sorted(DOS)},
       'titles': {n: AP[n]['title'] for n in NS}, 'merge_order': K['merge_order'], 'order_proof': ORDER_PROOF}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | merge-bases %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, [m[:12] for m in MB]))
sys.exit(1 if FAIL else 0)
