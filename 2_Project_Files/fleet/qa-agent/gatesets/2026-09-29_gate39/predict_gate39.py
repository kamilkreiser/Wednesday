#!/usr/bin/env python3
"""predict_gate39.py — MEASURE the gate39 kit (the directory this script lives in; its PR set, tiers, classes, commit counts, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate38's predict (gate37 -> gate36 lineage) and re-keyed for gate39: the two rows of Seat B 41st's queue, NONE stacked, on TWO
different develop merge-bases — #1337 on develop 215cc6875e2b itself (gate38's #1334 squash) and #1332 on 0d156d12cc0f (gate37's #1328 squash; round 2
is a fast-forward of round 1's f5381338) — T2 + T1: #1337 KS-888 (test-only-guard: the KS-764 revoke call-site guard's security pattern, both copies,
widened to the revoke shape #1327 introduced; a Spark golden, the PR must EQUAL the held checker patch) and #1332 KS-1054 ROUND 2 (schema-startup: a
new 038a file migration creates the four CORE tables before 039; the CORE-stage catches count; the summary's `error` is set). Each PR is measured over
ITS OWN develop merge-base and merged over the CURRENT develop (merge-tree with that merge-base). No sibling kit. The in-flight census is EVERY OTHER
OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json
`widen_rx` on titles AND `widen_branch_rx` on branches — Seat B 41st's `-b41-<n>`) is HARD: an open PR matching either outside this kit refuses.

MERGE ORDER (Wednesday's commission): #1337 FIRST. END_TREE is proven order-independent (every order); the ORDER is fixed because #1332's branch carries
the pre-existing KS-764 guard red that #1337 fixes. (e) proves it by EMULATION (READ): the guard's old and new security revoke patterns over security
index.ts on every intermediate develop of BOTH orders, each with a control arm set (save deleted, flip after save, a statement between).
TIER BY CLASS (kit.json `class`): `test-only-guard` (T2) changes EXACTLY one test file and no product byte; `schema-startup` (T1) changes EXACTLY the
five declared product files and six test files. STANDING REQUIREMENTS (Wednesday's ledger, 2026-09-29): (1) the PRE-EXISTING red — `packages/shared`
1 failed / 945 since #1327 — must be GREEN on END_TREE after #1337; (2) the CROSS-PACKAGE CENSUS: for every changed file, `git grep -l` of its file name
and `<parent>/<stem>` over every *.test.ts / *.test.js / *.test.sh / __tests__/*.sh in Blockchain/Dev at the head — the gate runs EVERY suite so named.
#1332's real-Postgres behaviour on the THREE fresh-database paths is MEASURED by pgprobe_gate39.py (run AFTER this script; its JSON is read here when
present).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths) and `noop_paths` are SEPARATE keys; gate39 declares neither,
and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate39 / Seat B 41st and is checked by rekey_check_gate39.py (which carries its own name in its own token map).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g39_sp/clone.git — `git clone --bare --shared
--no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's
core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout. The scratchpad MUST be on the
Data volume (/private/tmp/...): /Volumes/DevMASTER is full.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate39.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib, http.client

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate39.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g39_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate39 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g39/develop']
    + ['+refs/pull/%s/head:refs/g39/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g39/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g39/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g39/pull/' + n).strip() == g('rev-parse', 'refs/g39/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g39idx', dir=os.path.join(SP, 'g39_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE39-SIMULATED-MOVE.txt', 'gate39 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate39 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE39-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate39 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate39 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g39/pull/' + n).strip()
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
def readbytes(path):
    b = open(path, 'rb').read(); return b, sha256b(b)
def sections(text):
    """split a unified diff into [[header lines + body]] by '--- ' / '+++ ' header pairs"""
    out, cur, L = [], None, text.splitlines()
    i = 0
    while i < len(L):
        if L[i].startswith('--- ') and i + 1 < len(L) and L[i + 1].startswith('+++ '):
            cur = [L[i], L[i + 1]]; out.append(cur); i += 2; continue
        if cur is not None: cur.append(L[i])
        i += 1
    return out
def sec_path(sec):
    a, b = sec[0][4:].split('\t')[0], sec[1][4:].split('\t')[0]
    return (a[2:] if a.startswith('a/') else a), (b[2:] if b.startswith('b/') else b)
def git_apply_at(base, diffbytes, sha_expected, paths, tag):
    """`git apply --cached` (STRICT: no --recount, no fuzz, no -C) of EXACTLY <diffbytes> onto <base>'s tree in a scratch index; asserts the bytes
    written are the bytes verified (sha256 at the point of use). Returns ({path: blob} or None, message, tree or None)."""
    W = os.path.join(SP, 'g39_sp'); fp = tempfile.mktemp(prefix='g39apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16]), None
    idx = tempfile.mktemp(prefix='g39gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=e3)
    rchk = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', '--check', fp], capture_output=True, text=True, env=e3)
    if rchk.returncode != 0: return None, '`git apply --cached --check` REFUSES at %s (rc %d): %s [bytes used sha256 %s == verified]' % (base[:12], rchk.returncode, rchk.stderr.strip()[:220].replace('\n', ' / '), used[:16]), None
    ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', fp], capture_output=True, text=True, env=e3)
    if ra.returncode != 0: return None, 'apply rc %d after a passing --check: %s' % (ra.returncode, ra.stderr.strip()[:160]), None
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
    return {p: blob(t_, p) for p in paths}, '`git apply --cached --check` rc 0 and apply rc 0 at %s (strict) [bytes used sha256 %s == verified]' % (base[:12], used[:16]), t_
def ready_block(path):
    """READ a local-model READY file ONCE; return (bytes sha256, the ```diff block's lines, whether a GLUED closing fence was stripped, which line)"""
    b, s = readbytes(path); t = b.decode('utf-8')
    m = re.search(r'```diff\n(.*)', t, re.S); blk = m.group(1) if m else ''
    L = blk.split('\n'); glued = None
    for i, l in enumerate(L):
        if l == '```': L = L[:i]; break
        if l.endswith('```') and l[0:1] in ('+', '-', ' '):
            glued = (i, l[-40:]); L = L[:i] + [l[:-3]]; break
    return s, L, glued
def net(ls):
    """cancel identical -x/+x pairs (a golden may carry an unchanged line as a -/+ pair that `git diff -U0` never shows: the brief's +29/-4 vs git's +28/-3)"""
    ls = list(ls); out_ = []
    for l in ls:
        if l[0] == '-' and ('+' + l[1:]) in ls[ls.index(l):]: continue
        out_.append(l)
    for l in [x for x in ls if x[0] == '-' and ('+' + x[1:]) in ls[ls.index(x):]]:
        out_.remove('+' + l[1:])
    return out_
NIGHT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
BRIEFS = NIGHT + 'briefs/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
# the READY each PR was raised from, NAMED (never globbed), keyed by TICKET. gate39: #1337 (KS-888) is from a local-model READY — its PR diff must EQUAL
# the canonical patch (the Spark checker's held patch.diff == the brief's golden == the READY's diff block), applied STRICT at its merge-base.
# #1332 is SEAT-WRITTEN (Seat B 41st's ITEM 2): no local-model READY, no golden; its READY FOR QA MAIL is a claim, captured verbatim.
READY_BY_KEY = {
 'KS-888': (NIGHT + 'READY_KS-888-KS764-GUARD_spark-dsv4flash_BRIEFED-TESTONLY-KS764-GUARD-ACCEPTS-KS888-REVOKE-SHAPE-PASS-7of7_2026-09-29.diff.md',
            BRIEFS + 'KS-764-guard-ks888-shape/KS-888.golden.diff', 'spark_secuura_2026-09-28_KS-764-GUARD-KS888-SHAPE'),
}
READY = {n: READY_BY_KEY.get(K['prs'][n]['keys'][0], (None,))[0] for n in NS}
GOLDEN = {n: [READY_BY_KEY[K['prs'][n]['keys'][0]][1]] for n in NS if K['prs'][n]['keys'][0] in READY_BY_KEY}
CHECKER = {n: READY_BY_KEY[K['prs'][n]['keys'][0]][2] for n in NS if K['prs'][n]['keys'][0] in READY_BY_KEY}
KS764 = 'Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts'
SECIDX = 'Blockchain/Dev/services/security/src/index.ts'
GW = 'Blockchain/Dev/services/api-gateway/src/'
SMIG, HLTH, SMS = GW + 'startup-migrations.ts', GW + 'services/health.ts', GW + 'services/startupMigrationStatus.ts'
MIGD = 'Blockchain/Dev/migrations/'
M039, M038A = MIGD + '039_rls_fail_closed.sql', MIGD + '038a_ks1054_core_tables_before_039.sql'
GT, GT2 = GW + '__tests__/ks1054-startup-migration-failure-on-health.test.ts', GW + '__tests__/ks1054r2-core-throw-and-error-field.test.ts'
WIDENED = [GW + '__tests__/' + f for f in ('ks1062-startup-migrations-tenant-summary-first-error.test.ts', 'ks1125-api-gateway-startup-migrations-the-tenant.test.ts',
                                           'ks1128-platform-tenant-seed-failure-warns.test.ts', 'ks1272-platform-dedup-uuid-tenant-id.test.ts')]
RUNMIG = 'Blockchain/Dev/scripts/run-migrations.sh'
FOUR = ('oauth_apps', 'svc_webhooks', 'certifications', 'charge_events')
NEWPAT = "revokeWrite: /isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m,"
# the line(s) each red arm is planted at — FROM the READY mails' arms / the brief-writer's arms (READ), re-located here by exact WHOLE-LINE match at head,
# develop and END_TREE. A 5th field, when present, is the PREDECESSOR line (a two-line anchor, for a text that occurs twice).
TAMPER = {
 '1337': [(KS764, '    ' + NEWPAT, 84, 'the CALL_SITES security pattern (the widened one; put the 80-char window back -> RED the CALL_SITES cell only, as at develop)'),
          (KS764, '  /isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m,', 104, 'the REVOKE_WRITES copy (the sweep\'s own pattern; the brief-writer\'s doubt 4: the sweep equality finds security index.ts through the rotate UPDATE too)'),
          (SECIDX, '  apiKey.isActive = false;', 1286, 'the revoke flip (PRODUCT, untouched — the seat\'s arm C moves it after the save: the new pattern must RED)'),
          (SECIDX, '    await dbSaveApiKey(apiKey, { rethrow: true });', 1293, 'the revoke save (PRODUCT, untouched — arm A deletes it, arm B puts a statement before it: each must RED 1 of 15; the same text with SIX spaces is the mint\'s :1141)', '  try {')],
 '1332': [(M038A, 'CREATE TABLE IF NOT EXISTS oauth_apps (', 50, 'the new pre-039 creator of oauth_apps (the seat\'s arm: 038a deleted -> RED S3 only; on a REAL bare database round 1\'s permanent skip returns)'),
          (M039, '    EXECUTE $ddl$', 243, 'round 1\'s oauth_apps guard around the function CREATE (unchanged in round 2; with 038a it takes the THEN branch on every path)'),
          (M039, '    IF to_regprocedure(fn) IS NULL THEN', 278, 'round 1\'s owner/grant loop guard (unchanged in round 2)'),
          (SMIG, '    totalFailed += 1;', 1113, 'the MAIN CORE-stage catch now counts (N-1332-2; the seat\'s arm -> RED C1)', "    // - the exact \"clean\" claim the ticket exists to prevent."),
          (SMIG, '      totalFailed += 1;', 1217, 'the PLATFORM CORE-stage catch now counts (N-1332-2, platform side — NO seat cell drives it: the gate\'s own arm)', '      // KS-1054 (gate38 N-1332-2): same defect, platform side.'),
          (SMIG, '  return recordStartupMigrations({ applied: totalApplied, failed: totalFailed, error: totalError });', 1296, 'the ONE record per run, now with `error` (N-1332-3; the seat\'s arm drops `error: totalError` -> RED C2; gate38\'s arm F replaces the record -> N-1332-4)'),
          (HLTH, '      startupMigrations: getStartupMigrations(),', 94, '/health\'s field (round 1, unchanged)', "      // orchestrator acts on it, which is option (b) by another road."),
          (HLTH, '      startupMigrations: getStartupMigrations(),', 199, '/health/ready\'s field (round 1, unchanged)', "      // `service_healthy` conditions gate dependents on it.")],
}
def locate(c, p, line, prev=None):
    if not c: return []
    L = show(c, p).split('\n'); return [i + 1 for i, l in enumerate(L) if l == line and (prev is None or (i > 0 and L[i - 1] == prev))]
def its(s): return re.findall(r"^\s*it(?:\.each\([^)]*\))?\(\s*'([^']{0,140})", s, re.M)
def describes(s): return re.findall(r"^\s*describe\(\s*'([^']{0,200})'", s, re.M)
def grep_rev(rev, rx, *paths):
    rc_, o_, _ = gq('grep', '-n', '-I', '-E', rx, rev, '--', *paths); return [x for x in o_.strip().splitlines() if x]
def grep_l(rev, frag, *globs):
    rc_, o_, _ = gq('grep', '-l', '-F', frag, rev, '--', *globs); return sorted(x.split(':', 1)[1] for x in o_.strip().splitlines() if x)
PROBES = {}
MEAS = {}
# the comparator's own controls, once (STANDING_LINES 2026-09-27): identical pair IDENTICAL, one token DIFFER, and the empty-string trap caught
_x = ['+a', '-b', '+c']; _y = ['+a', '-b', '+C']
_trap = [l for l in ['+a', ''] if l[:1] in '+-']
CTL_PM = (cmp_seq(pm(_x + ['']), pm(_x)) == 'IDENTICAL' and cmp_seq(pm(_x), pm(_y)) == 'DIFFER' and len(_trap) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, 'CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in \'+-\'` would have counted the empty line (%d vs %d) — the kit uses `l and l[0] in \'+-\'`' % (len(_trap), len(pm(['+a', '']))))
PGJ = os.path.join(GS, 'pgprobe_gate39.json'); PG = json.load(open(PGJ)) if os.path.exists(PGJ) else None
TIER_OF = {'test-only-guard': 'T2', 'schema-startup': 'T1'}
DECL = {'test-only-guard': {'prod': [], 'doc': [], 'tests': [KS764]},
        'schema-startup': {'prod': sorted([M038A, M039, SMIG, HLTH, SMS]), 'doc': [], 'tests': sorted([GT, GT2] + WIDENED)}}
# THE CROSS-PACKAGE CENSUS (Wednesday's standing requirement 2, 2026-09-29): for EVERY file a PR changes, `git grep -l '<fragment>' -- '*.test.ts' '*.test.js'`
# over the WHOLE Blockchain/Dev tree at the head (fragments: the file name, and `<parent dir>/<stem>`); plus the shell / script suites that name it
# (`*.test.sh`, `*.sh` under a __tests__ dir) — the gate RUNS every suite that references a changed path, not only the changed service's. A NEW migration
# file is named by no test yet, so the census ALSO lists every suite that reads the migrations DIRECTORY (`migrations/` / `MIGRATIONS_DIR` / `readdirSync`
# over it) — 038a's lexical position is what those suites see.
def census(h, own):
    rows = {}
    for p in own:
        b = os.path.basename(p); stem = b.rsplit('.', 1)[0]; par = os.path.basename(os.path.dirname(p)) or '.'
        hits = set()
        for frag in (b, par + '/' + stem):
            for f in grep_l(h, frag, 'Blockchain/Dev/*.test.ts', 'Blockchain/Dev/*.test.js', 'Blockchain/Dev/*.test.sh', 'Blockchain/Dev/*/__tests__/*.sh'):
                if f != p: hits.add(f)
        rows[p] = sorted(hits)
    return rows
def dir_readers(h):
    out_ = set()
    for frag in ("migrations/*.sql", "'migrations'", "migrations/", 'MIGRATIONS_DIR', 'run-migrations.sh'):
        for f in grep_l(h, frag, 'Blockchain/Dev/*.test.ts', 'Blockchain/Dev/*.test.js', 'Blockchain/Dev/*.test.sh', 'Blockchain/Dev/*/__tests__/*.sh'):
            out_.add(f)
    return sorted(out_)
def pkg_of(f):
    m = re.match(r'Blockchain/Dev/((services|packages)/[^/]+)/', f)
    return m.group(1) if m else ('/'.join(f.split('/')[:3]) if f.startswith('Blockchain/Dev/') else f.split('/')[0])

# --- THE KS-764 GUARD, EMULATED (standing requirement 1 and the MERGE ORDER): the guard's OLD and NEW security revoke patterns (JS regexes; Python's
# `re` reads them identically here: character classes, `^` under re.M == JS /m, `.` excludes \n in both) over security index.ts; the new one is READ
# from the guard file at #1337's head, never typed (a typed copy is only its CONTROL: they must be byte-equal).
OLDRX = re.compile(r'isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(')
def js_rx(line):
    m = re.search(r'/(.*)/([a-z]*),\s*$', line); src, fl = m.group(1), m.group(2)
    return re.compile(src, re.M if 'm' in fl else 0), src
def guard_patterns(c):
    t = show(c, KS764); ls_ = t.split('\n')
    cs = [l for l in ls_ if l.strip().startswith('revokeWrite: /isActive')]
    rw = [l for l in ls_ if l.strip().startswith('/isActive')]
    return cs, rw
H1337 = H.get('1337') if '1337' in H else None
_cs, _rw = guard_patterns(H1337) if H1337 else ([], [])
NEWRX, NEWSRC = js_rx(_cs[0]) if _cs else (None, '')
hard(len(_cs) == 1 and len(_rw) == 1 and _cs[0].strip() == NEWPAT and js_rx(_rw[0])[1] == NEWSRC,
     'KS-764 EMULATION SOURCE: #1337\'s head carries EXACTLY one CALL_SITES security pattern and one REVOKE_WRITES copy, byte-equal to each other and to the kit\'s typed control copy (%d / %d)' % (len(_cs), len(_rw)))
SEC_DEV = show(REAL_DEV, SECIDX)
def arms_of(t):
    """the brief-writer's arms, planted IN MEMORY on security index.ts: each must make the NEW pattern miss"""
    # WHOLE-LINE anchors: the save text also occurs at :1141 with SIX spaces (the mint), so the save is anchored with its `  try {` predecessor
    flip, save = '\n  apiKey.isActive = false;\n', '\n  try {\n    await dbSaveApiKey(apiKey, { rethrow: true });\n'
    assert t.count(flip) == 1 and t.count(save) == 1, 'arm anchors not unique (flip %d, save %d)' % (t.count(flip), t.count(save))
    return {'A save deleted': t.replace(save, '\n  try {\n'),
            'B a statement between': t.replace(flip, flip + '  apiKey.isActive = !decision.allow;\n'),
            'C flip moved after save': t.replace(flip, '\n').replace(save, save + '  apiKey.isActive = false;\n'),
            'D save commented out': t.replace(save, '\n  try {\n    // await dbSaveApiKey(apiKey, { rethrow: true });\n'),
            'E early return between': t.replace(flip, flip + '  return;\n')}
if NEWRX is not None and SEC_DEV:
    arms = arms_of(SEC_DEV)
    armres = {k: bool(NEWRX.search(v)) for k, v in arms.items()}
    loose = re.compile(r'isActive\s*=\s*false;[\s\S]{0,2000}dbSaveApiKey\(')
    looseres = {k: bool(loose.search(v)) for k, v in arms.items()}
    hard(bool(NEWRX.search(SEC_DEV)) and not OLDRX.search(SEC_DEV) and not any(armres.values()) and any(looseres.values()),
         'KS-764 EMULATED (READ): at develop security index.ts the OLD pattern misses (the PRE-EXISTING red: %s) and the NEW pattern matches (%s); every in-memory arm makes the NEW pattern MISS %s; control — the brief-writer\'s rejected LOOSE window [\\s\\S]{0,2000} still matches under %s' % (
             bool(OLDRX.search(SEC_DEV)), bool(NEWRX.search(SEC_DEV)), armres, [k for k, v in looseres.items() if v]))
    MEAS['ks764_emulation'] = {'old_at_develop': bool(OLDRX.search(SEC_DEV)), 'new_at_develop': bool(NEWRX.search(SEC_DEV)), 'arms_new': armres, 'arms_loose': looseres}
print('--- (d2) THE MERGE ORDER, proven: every intermediate develop of every order, its tree, and the KS-764 guard state on it (EMULATED, READ)')
ORDER_PROOF = {}
if END and NEWRX is not None:
    for o in perms:
        t = DT; states = []
        for n in o:
            t = step(t, n)
            gf = show(t, KS764); sx = show(t, SECIDX)
            pat_old = 'isActive\\s*=\\s*false;[\\s\\S]{0,80}dbSaveApiKey\\(' in gf
            pat_new = NEWPAT in gf
            red = (pat_old and not OLDRX.search(sx)) or (pat_new and not NEWRX.search(sx)) or not (pat_old or pat_new)
            states.append({'after': '#' + n, 'tree': t, 'guard_pattern': 'NEW' if pat_new else 'OLD' if pat_old else '?', 'CALL_SITES_cell': 'RED (emulated)' if red else 'GREEN (emulated)'})
        ORDER_PROOF[' -> '.join('#' + n for n in o)] = states
        print('  ORDER %s: %s' % (' -> '.join('#' + n for n in o), ' | '.join('after %s tree %s guard %s CALL_SITES %s' % (s['after'], s['tree'][:12], s['guard_pattern'], s['CALL_SITES_cell']) for s in states)))
    mo = ' -> '.join('#' + n for n in K['merge_order'])
    hard(mo in ORDER_PROOF and all(s['CALL_SITES_cell'].startswith('GREEN') for s in ORDER_PROOF[mo]) and ORDER_PROOF[mo][-1]['tree'] == END,
         'THE COMMISSIONED MERGE ORDER %s keeps the CALL_SITES cell GREEN (emulated) on EVERY intermediate develop and ends at END_TREE %s' % (mo, END[:12]))
    other = [k for k in ORDER_PROOF if k != mo]
    hard(all(ORDER_PROOF[k][-1]['tree'] == END for k in ORDER_PROOF) and all(ORDER_PROOF[k][0]['CALL_SITES_cell'].startswith('RED') for k in other),
         'the OTHER order(s) %s end at the SAME END_TREE, but leave develop RED (emulated: the old pattern still in the guard) between the two squashes — the reason for #1337 FIRST' % other)
    MEAS['order_proof'] = ORDER_PROOF
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []; cls = K['prs'][n].get('class', '?')
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p and not p.endswith('.md')]
    docs = [p for p in P[n]['paths'] if p.endswith('.md')]
    tests = [p for p in P[n]['paths'] if p not in prod and p not in docs]
    out.append('PRODUCT files %s (changed +/- lines %s); TEST files %s; DOC files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests], docs or 'NONE'))
    hard(K['prs'][n]['tier'] == TIER_OF.get(cls), '#%s tier %s == the tier its class %s carries (%s)' % (n, K['prs'][n]['tier'], cls, TIER_OF.get(cls)))
    d_ = DECL[cls]
    hard(sorted(prod) == d_['prod'] and sorted(docs) == d_['doc'] and sorted(tests) == d_['tests'], '#%s (%s, class %s) changes EXACTLY the declared product files %s, doc files %s and test files %s' % (
        n, K['prs'][n]['tier'], cls, [os.path.basename(p) for p in prod], docs, [os.path.basename(t) for t in tests]))
    # --- the TAMPER / red-arm anchor(s), whole-line (two-line where declared), at head, develop and END_TREE
    for tt_ in TAMPER[n]:
        tf, tl, tline, tsrc = tt_[:4]; prev = tt_[4] if len(tt_) > 4 else None
        lh, ld, le = locate(h, tf, tl, prev), locate(REAL_DEV, tf, tl, prev), locate(END, tf, tl, prev)
        sub_h = [i + 1 for i, l in enumerate(show(h, tf).split('\n')) if l.strip() == tl.strip()]
        bl = {'head': blob(h, tf), 'develop': blob(REAL_DEV, tf), 'END': blob(END, tf) if END else None}
        hard(len(lh) == 1 and len(le) == 1, '#%s RED-ARM ANCHOR (%s) is byte-unique as a whole line%s (indentation included) in %s at head %s AND on END_TREE %s (the seat / drafter said :%d)' % (n, tsrc[:90], ' WITH its predecessor line' if prev else '', tf.split('/Dev/')[-1], lh, le, tline))
        out.append('RED-ARM ANCHOR (READ; %s): `%s`%s in %s — head %s | develop %s | END_TREE %s | said :%d; the SAME text with ANY indentation occurs at %s at head%s; blob of %s at head %s, develop %s, END %s (%s)' % (
            tsrc, tl.strip()[:110], (' after `%s`' % prev.strip()[:70]) if prev else '', tf.split('/Dev/')[-1], lh, ld, le, tline, sub_h,
            ' — the text occurs MORE THAN ONCE: plant by the TWO-LINE anchor (with its predecessor), never by substring' if len(sub_h) > 1 else '',
            os.path.basename(tf), (bl['head'] or '-')[:12], (bl['develop'] or '-')[:12], (bl['END'] or '-')[:12], 'the SAME file at head and on END_TREE' if bl['head'] == bl['END'] else 'the file DIFFERS between head and END_TREE — the gate plants at BOTH'))
    rp = READY[n]
    if rp is None:
        out.append('READY IDENTITY: NONE — #%s was written by Seat B 41st itself (ITEM 2, round 2 on round 1\'s branch), not from a local-model READY; there is no golden and no checker patch to compare. Its READY FOR QA mail (captured verbatim) and its PR body are claims, graded by the gate like any seat claim' % n)
        MEAS[n] = {'ready': None}
    elif not os.path.exists(rp):
        hard(False, '#%s READY %s ABSENT' % (n, rp)); MEAS[n] = {'ready': 'ABSENT'}
    else:
        rs, rl, glued = ready_block(rp)
        rblock = ('\n'.join(rl).rstrip('\n') + '\n').encode('utf-8')
        gb = open(GOLDEN[n][0], 'rb').read(); gs = sha256b(gb)
        ck = os.path.join(RUNS, CHECKER[n], 'out.md.checker', 'patch.diff')
        gsame = sha256b(rblock) == gs
        csame = os.path.exists(ck) and sha256b(open(ck, 'rb').read()) == gs
        nblk = len(re.findall(r'```diff\n', open(rp, encoding='utf-8').read()))
        hard(gsame and csame and nblk == 1, '#%s the READY\'s ONE ```diff block (%d found) bytes == the golden %s (sha256 %s, %d B) == the Spark checker\'s held patch.diff %s (the CANONICAL patch): %s / %s' % (n, nblk, GOLDEN[n][0].replace(BRIEFS, 'briefs/'), gs[:16], len(gb), ck.replace(RUNS, 'runs/'), gsame, csame))
        secs = sections('\n'.join(rl)); rpm = {sec_path(s)[1]: net(pm(s[2:])) for s in secs}
        ab_, am, gtree = git_apply_at(cb, gb, gs, P[n]['paths'], 'g%s' % n)
        exact = {p: (ab_ is not None and ab_[p] == blob(h, p)) for p in P[n]['paths']}
        resid = {p: pm(g('diff', '-U0', gtree, h, '--', p).splitlines()) if gtree else None for p in P[n]['paths']}
        nonnoop = gtree is not None and all(blob(gtree, p) != blob(cb, p) for p in P[n]['paths'])
        # the seat's own correction: a HUNK-OFFSET mutation is NOT a control for `git apply --check` (it searches for the offset); a CONTEXT-line one is
        ctxmut = re.sub(r'(?m)^ (    // enough to mean nothing, so each site names its own write\.)$', r' \1X', gb.decode('utf-8'), count=1).encode('utf-8')
        offmut = re.sub(r'(?m)^@@ -76,3 \+76,10 @@', '@@ -70,3 +70,10 @@', gb.decode('utf-8'), count=1).encode('utf-8')
        cm = git_apply_at(cb, ctxmut, sha256b(ctxmut), P[n]['paths'], 'ctx%s' % n)[0] if ctxmut != gb else 'UNPLANTED'
        om = git_apply_at(cb, offmut, sha256b(offmut), P[n]['paths'], 'off%s' % n)[0] if offmut != gb else 'UNPLANTED'
        hard(ab_ is not None and all(exact.values()) and all(v == [] for v in resid.values()) and nonnoop and set(rpm) == set(P[n]['paths']) and cm is None,
             '#%s == its CANONICAL patch EXACTLY: %s; every blob == head %s; diff(golden-applied, head) EMPTY in every path; the patch touches exactly the PR\'s paths %s; control (the apply is not a no-op): %s; CONTROL (a CONTEXT-line mutation of the golden REFUSES `git apply --check`): %s; the seat\'s correction, re-measured — a HUNK-OFFSET mutation %s' % (
                 n, am, {os.path.basename(p): v for p, v in exact.items()}, sorted(set(rpm)) == sorted(P[n]['paths']), nonnoop, cm is None, 'STILL APPLIES (not a control)' if isinstance(om, dict) else 'refuses' if om is None else om))
        hpm = {p: pm_diff(cb, h, p) for p in P[n]['paths']}
        ident = {p: ('IDENTICAL' if rpm.get(p, []) == hpm[p] else 'SLIDE-EQUAL (same lines, another order)' if sorted(rpm.get(p, [])) == sorted(hpm[p]) else 'DIFFER') for p in P[n]['paths']}
        hard(all(v != 'DIFFER' for v in ident.values()), '#%s READY +/- identity per file (net of identical -/+ pairs): %s' % (n, {os.path.basename(p): v for p, v in ident.items()}))
        out.append('READY IDENTITY (MEASURED): %s (sha256 %s) — its ONE diff block == the golden %s == the checker\'s held patch.diff (the CANONICAL patch, runs/%s): %s / %s; `git apply --cached --check` then apply, STRICT, at the merge-base %s: %s -> every blob == head: %s; diff(golden-applied, head) EMPTY: %s; +/- identity %s; %s; a context-line mutation refuses: %s; a hunk-offset mutation %s (the seat\'s correction holds: offset is NOT a control)' % (
            os.path.basename(rp), rs[:16], GOLDEN[n][0].replace(BRIEFS, 'briefs/'), CHECKER[n], gsame, csame, cb[:12], am, all(exact.values()), all(v == [] for v in resid.values()), {os.path.basename(p): v for p, v in ident.items()},
            ('the READY\'s closing fence is GLUED to its last diff line %r: stripped' % glued[1]) if glued else 'no glued fence', cm is None, 'still applies' if isinstance(om, dict) else 'refuses'))
        MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_bytes_eq_golden': gsame, 'checker_eq_golden': csame, 'golden': GOLDEN[n], 'golden_sha256': gs,
                   'apply': am, 'blobs_eq_head': exact, 'residue_empty': all(v == [] for v in resid.values()), 'identity': ident, 'ctx_mutation_refuses': cm is None, 'offset_mutation_applies': isinstance(om, dict)}
    # --- cells (READ): every test file the PR touches, at the merge-base and at head
    for t in tests:
        tt, t0 = show(h, t), show(cb, t)
        d0, d1 = describes(t0), describes(tt)
        out.append('CELLS (READ, %s): %d `it(`/`it.each(` entries at the merge-base, %d at head; NEW at head: %s; GONE at head: %s; describe %s -> %s' % (
            os.path.basename(t), len(its(t0)), len(its(tt)), [x[:80] for x in its(tt) if x not in its(t0)][:14] or 'NONE', [x[:80] for x in its(t0) if x not in its(tt)] or 'NONE', d0[:3], d1[:3]))
    svc = K['prs'][n]['service']
    pkg = show(REAL_DEV, 'Blockchain/Dev/' + svc + '/package.json')
    out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r; scripts.lint = %r' % (svc, (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1], (re.search(r'"lint"\s*:\s*"([^"]*)"', pkg) or [None, 'ABSENT'])[1]))
    # --- the cross-package census (standing requirement 2)
    cz = census(h, P[n]['paths'])
    extra = dir_readers(h) if cls == 'schema-startup' else []
    pk = sorted({pkg_of(f) for v in cz.values() for f in v} | {pkg_of(p) for p in P[n]['paths'] if p.startswith('Blockchain/')} | {pkg_of(f) for f in extra})
    out.append('CROSS-PACKAGE CENSUS (READ, `git grep -l -F` over Blockchain/Dev at head, fragments = file name and <parent>/<stem>, globs *.test.ts *.test.js *.test.sh __tests__/*.sh): %s%s — the suites the gate RUNS for #%s: %s' % (
        {os.path.relpath(p, 'Blockchain/Dev') if p.startswith('Blockchain/') else p: [os.path.relpath(f, 'Blockchain/Dev') for f in v] or 'NONE' for p, v in cz.items()},
        ('; and the suites that read the migrations DIRECTORY (fragments migrations/*.sql, \'migrations\', migrations/, MIGRATIONS_DIR, run-migrations.sh — 038a is named by no test but these see its position): %s' % [os.path.relpath(f, 'Blockchain/Dev') for f in extra]) if extra else '', n, pk))
    MEAS[n]['cross_package'] = {'files': cz, 'packages': pk, 'migrations_dir_readers': extra}
    # --- the KS-764 guard at this head and on END_TREE (standing requirement 1), emulated
    if NEWRX is not None:
        gs_ = {lab: ('NEW' if NEWPAT in show(c, KS764) else 'OLD') for lab, c in (('merge-base', cb), ('develop', REAL_DEV), ('head', h), ('END_TREE', END))}
        sx_ = {lab: show(c, SECIDX) for lab, c in (('merge-base', cb), ('develop', REAL_DEV), ('head', h), ('END_TREE', END))}
        cell = {lab: ('GREEN' if ((gs_[lab] == 'NEW' and NEWRX.search(sx_[lab])) or (gs_[lab] == 'OLD' and OLDRX.search(sx_[lab]))) else 'RED') for lab in gs_}
        alw = {lab: ('services/api-gateway/src/startup-migrations.ts' in show(c, KS764)) for lab, c in (('develop', REAL_DEV), ('head', h), ('END_TREE', END))}
        ment = {lab: (bool(re.search(r'svc_api_keys', show(c, SMIG))) and bool(re.search(r'is_active', show(c, SMIG))), any(r.search(show(c, SMIG)) for r in (re.compile(r'UPDATE\s+svc_api_keys\s+SET\s+is_active\s*=\s*false', re.I), NEWRX, OLDRX))) for lab, c in (('develop', REAL_DEV), ('head', h), ('END_TREE', END))}
        want = {'1337': {'head': 'GREEN', 'END_TREE': 'GREEN', 'develop': 'RED'}, '1332': {'head': 'RED', 'END_TREE': 'GREEN', 'develop': 'RED'}}[n]
        hard(all(cell[k] == v for k, v in want.items()) and all(m_[0] and not m_[1] for m_ in ment.values()) and all(alw.values()),
             '#%s KS-764 CALL_SITES cell (EMULATED — the guard file\'s own pattern over security index.ts): %s (guard pattern %s) — want %s; startup-migrations.ts (allowlisted in NON_REVOKE_MENTIONS: %s) still mentions svc_api_keys AND is_active and matches NO revoke pattern: %s' % (n, cell, gs_, want, alw, ment))
        out.append('KS-764 GUARD (EMULATED, READ; standing requirement 1): the CALL_SITES cell per tree %s with the guard pattern %s; startup-migrations.ts (mentions svc_api_keys + is_active, matches a revoke pattern) %s — the allowlist\'s drift cells (\'no file mentions svc_api_keys + is_active except…\', \'every allowlisted non-revoke really is present…\') read those two facts; the gate RUNS the real guard file at develop, this head and END_TREE and names each red cell by assertion' % (cell, gs_, ment))
        MEAS[n]['ks764'] = {'cell': cell, 'pattern': gs_, 'startup_migrations_mention_and_revoke': ment, 'allowlist_names_startup_migrations': alw}
    # --- per-class probes
    if cls == 'test-only-guard':
        prodtouch = [p_ for p_ in P[n]['paths'] if '__tests__' not in p_]
        hard(not prodtouch, '#%s TEST-ONLY (READ): no product path in the PR %s' % (n, prodtouch or 'NONE'))
        # THE SWEEP, emulated: every non-test .ts/.js under services/* and packages/* at END_TREE that either REVOKE_WRITES pattern matches (the drift
        # cell's equality), and every file that mentions svc_api_keys AND is_active (the allowlist cell's set)
        rc_, o_, _ = gq('ls-tree', '-r', '--name-only', END, 'Blockchain/Dev/services', 'Blockchain/Dev/packages') if END else (1, '', 'no END_TREE')   # a refused merge has no END: the sweep is skipped, the refusal is already counted
        srcs = [f for f in o_.split() if re.search(r'\.(ts|js)$', f) and '__tests__' not in f and '/node_modules/' not in f and '.test.' not in f and '/dist/' not in f]
        upd = re.compile(r'UPDATE\s+svc_api_keys\s+SET\s+is_active\s*=\s*false', re.I)
        hitsw = {'UPDATE': [], 'NEW': [], 'OLD': []}; mention = []
        for f in srcs:
            t_ = show(END, f)
            if upd.search(t_): hitsw['UPDATE'].append(f.split('/Dev/')[1])
            if NEWRX.search(t_): hitsw['NEW'].append(f.split('/Dev/')[1])
            if OLDRX.search(t_): hitsw['OLD'].append(f.split('/Dev/')[1])
            if 'svc_api_keys' in t_ and 'is_active' in t_: mention.append(f.split('/Dev/')[1])
        out.append('THE SWEEP ON END_TREE (EMULATED, READ; %d non-test .ts/.js files under services/* and packages/*): the rotate/UPDATE pattern matches %s; the NEW security pattern matches %s; the OLD one %s. Files mentioning svc_api_keys AND is_active: %s — the gate compares with the guard\'s CALL_SITES + NON_REVOKE_MENTIONS and RUNS the drift cells. The brief-writer\'s doubt 4 (pre-existing): security index.ts is found by the UPDATE pattern too (the rotate :273), so REVOKE_WRITES[1] can drift unseen by the equality — only the per-site loop catches it (the seat named it a candidate, not filed)' % (
            len(srcs), hitsw['UPDATE'], hitsw['NEW'], hitsw['OLD'] or 'NONE', mention))
        MEAS[n]['sweep_end'] = {'files': len(srcs), 'matches': hitsw, 'mentions': mention}
        out.append('THE ARMS (READ from the READY and the brief-writer\'s README; EMULATED above): A save deleted, B a statement between flip and save, C flip moved after save — the seat: each reds "14 passed / 1 failed" (not a loadfail); the brief-writer\'s extra arms (save commented out, save replaced by memApiKeys.set, early return) each 1 failed / 15; the builder tamper (keyRevokePolicy.ts :17 gains an UPDATE svc_api_keys literal) 2 failed / 15. The gate re-runs A-C on the PRODUCT file in its own worktree, restores by bytes, and adds the gate arm: the NEW pattern put back to the 80-char window at #1337\'s head -> the CALL_SITES cell reds exactly as at develop')
        out.append('A4 CONTRADICTION (READ): the READY\'s own A4 line records "2 failed / 15 run" at the untouched tip; the seat measured "1 failed / 14 passed (15)" and the brief-writer "1 failed / 15" — the gate runs the guard file at develop and names every red cell with its assertion')
        out.append('ESLINT (READ, the seat): `eslint src` in packages/shared reads "36 problems (1 error, 35 warnings)" at the tip AND with the change — the one error is the KS 703 control-byte guard (`539:36 … no-control-regex`, BACKLOG) — PRE-EXISTING, a delta of zero proven by stash-and-restore; the gate re-measures the delta, not the ownership')
    if cls == 'schema-startup':
        s1, s0, r1 = show(h, SMIG), show(cb, SMIG), show(P[n]['commits'][0], SMIG)
        m38a = show(h, M038A)
        trk = {'records on success': "INSERT INTO _secuura_migrations (filename) VALUES ($1)" in s1, 'skips a recorded file': "SELECT 1 FROM _secuura_migrations WHERE filename = $1 LIMIT 1" in s1}
        hard(all(trk.values()), '#%s THE TRACKER (READ, startup-migrations.ts applyFileMigrations at head): %s — a file that SUCCEEDS is recorded and never re-run' % (n, trk))
        rm = show(h, RUNMIG)
        rmt = {'skips a recorded file': "SELECT 1 FROM _secuura_migrations WHERE filename = '$fname' LIMIT 1;" in rm, 'records ON CONFLICT DO NOTHING': 'ON CONFLICT (filename) DO NOTHING' in rm, 'one pass, lex glob': 'for f in migrations/*.sql; do' in rm, 'no CORE stage': 'CORE' not in rm}
        hard(all(rmt.values()), '#%s THE COMPOSE RUNNER (READ, scripts/run-migrations.sh at head): %s — the seat\'s shape-(b) argument (the container path has no CORE stage, so only a pre-039 FILE can create the four tables there)' % (n, rmt))
        # --- 038a's lexical position under every sort the runners use
        names = sorted(os.path.basename(x) for x in g('ls-tree', '--name-only', h, MIGD).split() if x.endswith('.sql'))
        i38a = names.index(os.path.basename(M038A))
        punct_ign = sorted(names, key=lambda s: (re.sub(r'[^0-9a-z]', '', s.lower()), s))
        j38a = punct_ign.index(os.path.basename(M038A))
        hard(names[i38a - 1] == '038_rls_consolidate_policy.sql' and names[i38a + 1] == '039_rls_fail_closed.sql',
             '#%s 038a\'s LEXICAL POSITION (READ; byte order == JS Array.prototype.sort() in loadMigrations :95-:97 == `for f in migrations/*.sql` under the C / POSIX locale, and musl (node:24-alpine, the migrations image) collates by bytes): %s < 038a < %s' % (n, names[i38a - 1], names[i38a + 1]))
        out.append('038a UNDER A LOCALE COLLATION (READ — a PREDICTED RISK the gate MEASURES): the gateway sorts by UTF-16 code unit (`.sort()`, byte order for ASCII) and the migrations image is node:24-alpine (musl: strcoll == strcmp); but `sh scripts/run-migrations.sh` run by hand on a glibc host under en_US.UTF-8 (punctuation IGNORED at the first level) would glob %s — 038a %s. 038 (KS-173\'s tenant_isolation consolidation) names all four tables; run BEFORE 038a it skips them (\'table does not exist\'), run AFTER it declares their permissive policy (039 then flips it). The gate globs `migrations/*.sql` under `sh` with LC_ALL=C and LC_ALL=en_US.UTF-8 on this host, says which order each gives, and whether any runner a deploy uses can put 038a before 038' % (
            punct_ign[max(0, j38a - 1):j38a + 2], 'BEFORE 038_rls_consolidate_policy.sql' if punct_ign.index('038_rls_consolidate_policy.sql') > j38a else 'after 038 (no change)'))
        # --- DDL parity: 038a vs CORE's own CREATE TABLE for the four tables (at head, at the develop 038a names, and at the merge-base)
        def ddl_of(text, tbl, core):
            if core:
                m = re.search(r'`CREATE TABLE IF NOT EXISTS %s \((.*?)\n\s*\)`' % tbl, text, re.S)
                if not m: m = re.search(r'CREATE TABLE IF NOT EXISTS %s \((.*?)\n\s*\)' % tbl, text, re.S)
            else:
                m = re.search(r'CREATE TABLE IF NOT EXISTS %s \((.*?)\n\s*\);' % tbl, text, re.S)
            return re.sub(r'\s+', ' ', m.group(1)).strip() if m else None
        par = {}
        for tbl in FOUR:
            a = ddl_of(m38a, tbl, False)
            par[tbl] = {'038a_vs_core_head': a is not None and a == ddl_of(s1, tbl, True), 'core_head_vs_develop': ddl_of(s1, tbl, True) == ddl_of(show(REAL_DEV, SMIG), tbl, True), 'core_head_vs_merge_base': ddl_of(s1, tbl, True) == ddl_of(s0, tbl, True)}
        _ctl = ddl_of(m38a.replace('client_id VARCHAR(64)', 'client_id VARCHAR(63)'), 'oauth_apps', False) != ddl_of(s1, 'oauth_apps', True)
        hard(all(all(v.values()) for v in par.values()) and _ctl,
             '#%s DDL PARITY (READ, whitespace-normalised TEXT): 038a\'s CREATE TABLE == CORE\'s own (startup-migrations.ts at head) for each of the four tables, and CORE\'s text is identical at head, at develop and at the merge-base %s; control (varying(64) -> (63) in 038a) DIFFERS: %s — TEXT, not schema: the gate proves the SCHEMA by pg_dump on a real PostgreSQL' % (n, par, _ctl))
        # --- which migrations reference the four tables, and on which side of 038a they sort
        ref = [os.path.basename(x.split(':', 1)[1]) for x in (gq('grep', '-l', '-w', '-E', '|'.join(FOUR), h, '--', MIGD + '*.sql')[1].strip().splitlines())]
        before = [x for x in ref if x < os.path.basename(M038A)]; after = [x for x in ref if x > os.path.basename(M038A) and x != os.path.basename(M038A)]
        out.append('THE MIGRATIONS THAT NAME THE FOUR TABLES (READ, `git grep -l -w` at head): %d below 038a %s and %d above it %s (the seat: "12 migrations reference these four tables"). Below 038a they run BEFORE the tables exist on pass 1 exactly as at develop — but a FAILED file is not recorded, so on pass 2 (the next boot, or a second run-migrations.sh) each re-runs AGAINST 038a\'s tables: that is the BEHAVIOUR CHANGE the seat reports as "006, 008 and 047 now succeed" (006 / 008 alter svc_webhooks.secret_v2; 047 adds oauth_apps_app_type_vocabulary). The gate reads every one of them, drives each path, and says per migration: fails-then-applies, applies at pass 1, or unchanged — and whether the table each ALTERs ends in the SAME schema as CORE\'s (the pg_dump equality)' % (len(before), before, len(after), after))
        nt = re.findall(r"RAISE NOTICE '(KS-1054: oauth_apps absent[^']*)'", show(h, M039))
        out.append('ROUND 1\'s 039 GUARD, KEPT (READ): 039 is byte-identical to round 1 (%s); its ELSE branch (NOTICE %r) is now unreachable on every path that runs 038a first — reachable only where 038a is SKIPPED or FAILS (a pre-existing database that already recorded 039 never re-runs it: round-1-era databases keep whatever 039 did there). The gate says whether a database that booted round 1\'s 039 (recorded, work skipped) is healed by round 2 — READ: 038a creates the tables but 039 is recorded and never re-runs, so NO' % (
            'blob %s == round 1\'s %s' % ((blob(h, M039) or '-')[:12], (blob(P[n]['commits'][0], M039) or '-')[:12]) if blob(h, M039) == blob(P[n]['commits'][0], M039) else 'CHANGED since round 1', nt[0][:120] if nt else None))
        catches = {'main CORE catch counts': "    log('warn', 'Main DB migrations failed', { error: err?.message });" in s1 and s1.count('    totalFailed += 1;\n    noteError(err?.message);') == 1,
                   'platform CORE catch counts': s1.count('      totalFailed += 1;\n      noteError(err?.message);') == 1,
                   'record carries error': 'recordStartupMigrations({ applied: totalApplied, failed: totalFailed, error: totalError })' in s1,
                   'first error wins': 'if (totalError === undefined && msg) totalError = String(msg).substring(0, 200);' in s1}
        hard(all(catches.values()), '#%s N-1332-2 / N-1332-3 (READ, startup-migrations.ts at head): %s' % (n, catches))
        out.append('N-1332-2 / N-1332-3 (READ): %s — the seat drives the MAIN catch only (C1 / C2 in ks1054r2, a pool whose end() throws); NO cell drives the PLATFORM catch (:1217) — the gate drives both on a real PostgreSQL (a platform URL) or with the seat\'s harness, and reads the recorded `failed` and `error`. N-1332-4 (gate38: arm F, the run->record wiring, reddened 0 of 9): ks1054r2 C1/C2 now read runStartupMigrations()\'s RETURN — the gate re-runs arm F (`return getStartupMigrations()` at :1296) and says whether C0-C3 now pin the wiring. The error field\'s bound: C3 (substring 200 — the gate reads `noteError` and `firstError`, both 200)' % catches)
        out.append('N-1332-5 (READ; UNRAISED by ruling for a successor — NOT a NO GO this round): deploy.sh :823 and deploy-all.sh :281 at head %s read `startupMigrations`: the gate greps them and notes it' % ('DO' if grep_rev(h, r'startupMigrations', 'Blockchain/Dev/deployment', 'Blockchain/Dev/scripts') else 'do NOT'))
        out.append('THE COMPOSE RUNNER STILL EXITS 3 (READ from the seat\'s own drill log, not the READY: run-migrations.sh on a bare database at round 2 reads "Summary: applied=45 failed=5" then "applied=47 failed=3" — 026 / 027 / 028 (rights_holders) fail on every pass, pre-existing): the `migrations` service gates dependents on `service_completed_successfully`, which a rc 3 fails — the gate measures the runner\'s rc and names every failing file per pass, and says which are PRE-EXISTING (identical at the merge-base)')
        hs = [i + 1 for i, l in enumerate(s1.split('\n')) if 'KS-1054' in l and ('WHY STAGE 2 STILL RUNS SECOND' in l or 'ROUND 2' in l.upper())]
        out.append('THE SEAT\'S "SECOND PASS CHANGES NONE OF THOSE FIVE" (READ): its drill table measures five facts (039 recorded, the function, the policy, tenant_isolation count, the four tables) — its own log shows the runner APPLIED 2 more files on pass 2 (45 -> 47: 006 and 008 succeed only once 038a\'s svc_webhooks exists). The gate\'s "a second boot changes nothing" is over the WHOLE schema (pg_dump) and `_secuura_migrations`, on each path, and names every row that changes')
        wid = {os.path.basename(p): pm_diff(cb, h, p) for p in WIDENED}
        def _wok(v):
            mi = [l for l in v if l[0] == '-']; pl = [l for l in v if l[0] == '+']
            return len(mi) == 1 and 'Promise<void>' in mi[0] and len([l for l in pl if 'Promise<unknown>' in l]) == 1 and all(l.lstrip('+').strip().startswith('//') or 'Promise<unknown>' in l for l in pl)
        hard(all(_wok(v) for v in wid.values()) and not _wok(['-a', '+b']),
             '#%s THE FOUR WIDENED ANNOTATIONS (READ, round 1, unchanged): each file changes ONE `-` line (Promise<void>) for ONE `+` Promise<unknown> line plus comment lines only (control: a non-annotation pair is refused): %s' % (n, {k: '-%d/+%d' % (len([l for l in v if l[0] == '-']), len([l for l in v if l[0] == '+'])) for k, v in wid.items()}))
        r12 = sorted(g('diff', '--name-only', P[n]['commits'][0], h).split())
        out.append('ROUND 2 DELTA (READ, round 1 %s -> head %s, a fast-forward): %s — round 1\'s other files (039, health.ts, startupMigrationStatus.ts, ks1054 H0-H5 / S0-S2, the four annotations) carry forward from gate38\'s measurement; ks1054 gains S3 and rewrites S0 / S1 (the seat\'s `filesBelow()` letter-suffix blind spot)' % (P[n]['commits'][0][:12], h[:12], [os.path.basename(x) for x in r12]))
        if PG and '_summary' in PG:
            out.append('THE POSTGRES (MEASURED by the drafter, pgprobe_gate39.py -> pgprobe_1.out / pgprobe_gate39.json, %s, unix socket only): %s — the gate re-measures every path and RULES' % (PG.get('engine', '?')[:40], {k: v for k, v in PG['_summary'].items()}))
            MEAS[n]['pgprobe'] = {'summary': PG['_summary']}
        else: out.append('THE POSTGRES: pgprobe_gate39.json ABSENT — UNMEASURED by the drafter')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT, 'merge_bases': MB,
       'end_tree': END, 'end_tree_with_sibling': None, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES, 'measured': MEAS,
       'stacks': ST, 'retarget': RT, 'declared_overlap': DOV, 'noop_paths': NOOP, 'sibling_paths': {}, 'sibling_heads': {},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': {}, 'dead_open_declared': {},
       'titles': {n: AP[n]['title'] for n in NS}, 'merge_order': K['merge_order'], 'order_proof': ORDER_PROOF}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | merge-bases %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, [m[:12] for m in MB]))
sys.exit(1 if FAIL else 0)
