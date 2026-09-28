#!/usr/bin/env python3
"""predict_gate38.py — MEASURE the gate38 kit (the directory this script lives in; its PR set, tiers, classes, commit counts, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate37's predict (gate36 -> gate35 lineage) and re-keyed for gate38: the two rows of Seat B 40th's round, NONE stacked, both on develop
0d156d12cc0f (gate37's #1328 squash) while develop has moved on to 3d706c21f65e by two MERGE commits (#1329 KS-1354, #1331 KS-1365 — neither ours) —
T1 x2: #1330 KS-1352 (verify-truth: the shared VC verifier consults two id-keyed revocation resolvers — the stored issuer record and the status list's
own bit — so a credential revoked by EITHER route fails POST /api/credentials/verify and POST /api/presentations/verify; an id with no record ABSTAINS;
plus a BACKLOG.md entry) and #1332 KS-1054 (schema-startup: 039 guards `auth_find_oauth_app_by_client_id` on oauth_apps existing and its owner/grant
loop skips an absent function; runStartupMigrations returns and records a summary that /health and /health/ready report, codes unchanged; four test
annotations widened). Both SEAT-WRITTEN (no local-model READY, no golden). Each PR is measured over ITS OWN develop merge-base and merged over the CURRENT
develop (merge-tree with that merge-base). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened
since, read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles AND `widen_branch_rx` on branches — Seat
B 40th's `-b40-<n>`) is HARD: an open PR matching either outside this kit refuses (ADDENDUM 1's possible #1333 / #1334 would land here).

TIER BY CLASS (kit.json `class`): `verify-truth` (T1) changes EXACTLY the five declared product files, BACKLOG.md and one test file; `schema-startup` (T1)
changes EXACTLY the four declared product files and five test files. STANDING REQUIREMENTS (Wednesday's ledger, 2026-09-29): (1) the PRE-EXISTING red —
`packages/shared` 1 failed / 945 since #1327, the KS-764 revoke call-site guard — is emulated here by its own regex over security index.ts at the
merge-base, develop, each head and END_TREE (with a control), so the gate can name it PRE-EXISTING unless a PR changes its count; (2) the CROSS-PACKAGE
CENSUS: for every changed file, `git grep -l` of its file name and `<parent>/<stem>` over every *.test.ts / *.test.js / *.test.sh / __tests__/*.sh in
Blockchain/Dev at the head — the gate runs EVERY suite so named. #1332's real-Postgres behaviour is MEASURED by pgprobe_gate38.py (run AFTER this
script; its JSON is read here when present).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths) and `noop_paths` are SEPARATE keys; gate38 declares neither,
and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate38 / Seat B 40th and is checked by rekey_check_gate38.py (which carries its own name in its own token map).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g38_sp/clone.git — `git clone --bare --shared
--no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's
core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate38.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib, http.client

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate38.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g38_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate38 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g38/develop']
    + ['+refs/pull/%s/head:refs/g38/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g38/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g38/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g38/pull/' + n).strip() == g('rev-parse', 'refs/g38/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g38idx', dir=os.path.join(SP, 'g38_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE38-SIMULATED-MOVE.txt', 'gate38 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate38 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE38-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate38 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate38 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g38/pull/' + n).strip()
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
    W = os.path.join(SP, 'g38_sp'); fp = tempfile.mktemp(prefix='g38apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16]), None
    idx = tempfile.mktemp(prefix='g38gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
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
# the READY each PR was raised from, NAMED (never globbed). gate38: BOTH rows are SEAT-WRITTEN (Seat B 40th's ITEM 1 and ITEM 2) — no local-model READY,
# no golden, no checker patch. Their READY FOR QA MAILS (message ids in kit README / capture) are claims, captured verbatim, never a patch to compare.
# (ADDENDUM 1's two possible raises — KS-1124 F4, the KS-888 validate log-only pin — WOULD carry night/READY_KS-1124-F4_* / READY_KS-888-VALIDATE-LOGONLY_*;
# they are NOT in this kit: see README.)
# ADDENDUM 1's raises carry a local-model READY each, keyed here by TICKET (a PR number is not known until it is raised): the PR diff must EQUAL the
# canonical patch (the checker's patch.diff == the brief's golden == the READY's diff block), applied STRICT at the merge-base.
READY_BY_KEY = {
 'KS-1124': (NIGHT + 'READY_KS-1124-F4_spark-dsv4flash_BRIEFED-CODEPATCH-KS1124-F4-SAVE-FAILED-STATUS-PASS-7of7_2026-09-29.diff.md', BRIEFS + 'KS-1124-F4/KS-1124.golden.diff', 'spark_secuura_2026-09-28_KS-1124-F4'),
 'KS-888': (NIGHT + 'READY_KS-888-VALIDATE-LOGONLY_spark-dsv4flash_BRIEFED-TESTONLY-KS888-VALIDATE-LOGONLY-PIN-PASS-7of7_2026-09-29.diff.md', BRIEFS + 'KS-888-validate-logonly/KS-888.golden.diff', 'spark_secuura_2026-09-28_KS-888-VALIDATE-LOGONLY'),
}
READY = {n: READY_BY_KEY.get(K['prs'][n]['keys'][0], (None,))[0] for n in NS}
GOLDEN = {n: [READY_BY_KEY[K['prs'][n]['keys'][0]][1]] for n in NS if K['prs'][n]['keys'][0] in READY_BY_KEY}
CHECKER = {n: READY_BY_KEY[K['prs'][n]['keys'][0]][2] for n in NS if K['prs'][n]['keys'][0] in READY_BY_KEY}
ORIG = 'Blockchain/Dev/services/originate/src/'
CERT, CT543 = ORIG + 'routes/certifications.ts', ORIG + '__tests__/ks543-certify-boundary-strip.test.ts'
SEC888T = 'Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts'
SHV = 'Blockchain/Dev/packages/shared/src/vc/verifier.ts'
VCI = 'Blockchain/Dev/services/vc-issuer/src/'
CRED, PRES, STAT, RSLV = VCI + 'routes/credentials.ts', VCI + 'routes/presentations.ts', VCI + 'routes/status.ts', VCI + 'services/revocationResolvers.ts'
VT = VCI + '__tests__/ks1352-revoked-credential-fails-verify.test.ts'
BACKLOG = 'BACKLOG.md'
GW = 'Blockchain/Dev/services/api-gateway/src/'
SMIG, HLTH, SMS = GW + 'startup-migrations.ts', GW + 'services/health.ts', GW + 'services/startupMigrationStatus.ts'
M039 = 'Blockchain/Dev/migrations/039_rls_fail_closed.sql'
GT = GW + '__tests__/ks1054-startup-migration-failure-on-health.test.ts'
WIDENED = [GW + '__tests__/' + f for f in ('ks1062-startup-migrations-tenant-summary-first-error.test.ts', 'ks1125-api-gateway-startup-migrations-the-tenant.test.ts',
                                           'ks1128-platform-tenant-seed-failure-warns.test.ts', 'ks1272-platform-dedup-uuid-tenant-id.test.ts')]
KS764 = 'Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts'
SECIDX = 'Blockchain/Dev/services/security/src/index.ts'
HANDWRITTEN = {}
# the line(s) each red arm is planted at — FROM the READY mails' arms (READ), re-located here by exact WHOLE-LINE match at head, develop and END_TREE. A 5th
# field, when present, is the PREDECESSOR line (a two-line anchor, for a text that occurs twice).
TAMPER = {
 '1330': [(SHV, "        if (record.found && record.revoked) {", 479, 'the stored-record arm (the seat\'s arm a: never reports revoked -> RED R1 R2, 2 of 6)'),
          (SHV, "        if (listed.found && listed.revoked) {", 498, 'the status-list arm (arm b: never reports revoked -> RED R3, 1 of 6)'),
          (SHV, "        this.config.storedRecordResolver ||", 151, 'the widened gate that runs checkStatus without a submitted credentialStatus (a GATE arm: remove the two resolver disjuncts -> a document with NO credentialStatus verifies again)'),
          (SHV, "      return { valid: errors.length === 0, errors };", 509, 'the no-credentialStatus return (a GATE arm: put back `{ valid: true, errors: [] }` -> the arms are discarded when the submitted document omits credentialStatus)', "      // submitted document happened to carry no credentialStatus."),
          (CRED, "      ...revocationVerifierConfig(),", 346, 'the credentials/verify wiring (a GATE arm: removed -> the route is inert again)'),
          (PRES, "          ...revocationVerifierConfig(),", 293, 'the presentations/verify wiring (a GATE arm: removed -> a revoked credential inside a presentation verifies again; the seat drove NO presentation cell)')],
 '1332': [(M039, "    EXECUTE $ddl$", 243, 'the oauth_apps table guard around the function CREATE (the seat\'s arm A: guard removed -> RED S1 only; on a REAL bare database the base\'s boot-1 failure returns)'),
          (M039, "    IF to_regprocedure(fn) IS NULL THEN", 278, 'the owner/grant loop guard (arm B: removed -> RED S2 only; on a REAL bare database the loop fails on the absent function)'),
          (SMIG, "  return recordStartupMigrations({ applied: totalApplied, failed: totalFailed });", 1272, 'the ONE record per run (arm C latches it: RED H2 H3 H4 H5 — the seat predicted H3 and measured wider)'),
          (HLTH, "      startupMigrations: getStartupMigrations(),", 94, '/health\'s field (arm D: dropped -> RED H0 H1 H2 H3 H5)', "      // orchestrator acts on it, which is option (b) by another road."),
          (HLTH, "      startupMigrations: getStartupMigrations(),", 199, '/health/ready\'s field (arm E: dropped -> RED H4 only)', "      // `service_healthy` conditions gate dependents on it.")],
 '1333': [(CERT, "          ...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),", 474, 'the ISSUE route\'s failed-status spread (removed -> RED F4-1 only)', "          // gateway maps to off-chain-only; a statusless 'pending-onchain' blob would show as pending forever."),
          (CERT, "          ...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),", 1212, 'the RECERTIFY route\'s failed-status spread (removed -> RED F4-2 only)', "          // rule as the issue route: the gateway maps it to off-chain-only instead of pending forever.")],
 '1334': [(SECIDX, "    logger.error('DB save API key failed', { error: err?.message });", 332, 'the ONE log line a failed usage write emits (PRODUCT, untouched by the PR — the gate\'s arms: removed / doubled / carrying k.keyHash -> V2 reds)'),
          (SECIDX, "  await dbSaveApiKey(apiKey);", 1369, 'validate\'s usage write with NO opt-in (PRODUCT, untouched — the REFUSE arm: `{ rethrow: true }` + a 503 -> V1 x3 red)')],
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
PGJ = os.path.join(GS, 'pgprobe_gate38.json'); PG = json.load(open(PGJ)) if os.path.exists(PGJ) else None
TIER_OF = {'verify-truth': 'T1', 'schema-startup': 'T1', 'certify-status': 'T1', 'test-only-pin': 'T2'}
DECL = {'verify-truth': {'prod': sorted([SHV, CRED, PRES, STAT, RSLV]), 'doc': [BACKLOG], 'tests': [VT]},
        'schema-startup': {'prod': sorted([M039, SMIG, HLTH, SMS]), 'doc': [], 'tests': sorted([GT] + WIDENED)},
        'certify-status': {'prod': [CERT], 'doc': [], 'tests': [CT543]},
        'test-only-pin': {'prod': [], 'doc': [], 'tests': [SEC888T]}}
# THE CROSS-PACKAGE CENSUS (Wednesday's standing requirement 2, 2026-09-29): for EVERY file a PR changes, `git grep -l '<fragment>' -- '*.test.ts' '*.test.js'`
# over the WHOLE Blockchain/Dev tree at the head (fragments: the file name, and `<parent dir>/<stem>`); plus the shell / script suites that name it
# (`*.test.sh`, `*.sh` under a __tests__ dir) — the gate RUNS every suite that references a changed path, not only the changed service's.
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
def pkg_of(f):
    m = re.match(r'Blockchain/Dev/((services|packages)/[^/]+)/', f)
    return m.group(1) if m else ('/'.join(f.split('/')[:3]) if f.startswith('Blockchain/Dev/') else f.split('/')[0])
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []; cls = K['prs'][n].get('class', '?')
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p and not p.endswith('.md')]
    docs = [p for p in P[n]['paths'] if p.endswith('.md')]
    tests = [p for p in P[n]['paths'] if p not in prod and p not in docs]
    out.append('PRODUCT files %s (changed +/- lines %s); TEST files %s; DOC files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests], docs or 'NONE'))
    hard(K['prs'][n]['tier'] == TIER_OF.get(cls), '#%s tier %s == the tier its class %s carries (%s)' % (n, K['prs'][n]['tier'], cls, TIER_OF.get(cls)))
    d_ = DECL[cls]
    hard(sorted(prod) == d_['prod'] and sorted(docs) == d_['doc'] and sorted(tests) == d_['tests'], '#%s (T1, class %s) changes EXACTLY the declared product files %s, doc files %s and test files %s' % (
        n, cls, [os.path.basename(p) for p in prod], docs, [os.path.basename(t) for t in tests]))
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
        out.append('READY IDENTITY: NONE — #%s was written by Seat B 40th itself (ITEM %s), not from a local-model READY; there is no golden and no checker patch to compare. Its READY FOR QA mail (captured verbatim) and its PR body are claims, graded by the gate like any seat claim' % (n, '1' if n == '1330' else '2'))
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
        hard(gsame and csame, '#%s the READY block\'s bytes == the golden %s (sha256 %s, %d B) == the Spark checker\'s patch.diff (the CANONICAL patch): %s / %s' % (n, GOLDEN[n][0].replace(BRIEFS, 'briefs/'), gs[:16], len(gb), gsame, csame))
        secs = sections('\n'.join(rl)); rpm = {sec_path(s)[1]: net(pm(s[2:])) for s in secs}
        ab_, am, gtree = git_apply_at(cb, gb, gs, P[n]['paths'], 'g%s' % n)
        exact = {p: (ab_ is not None and ab_[p] == blob(h, p)) for p in P[n]['paths']}
        resid = {p: pm(g('diff', '-U0', gtree, h, '--', p).splitlines()) if gtree else None for p in P[n]['paths']}
        nonnoop = gtree is not None and all(blob(gtree, p) != blob(cb, p) for p in P[n]['paths'])
        hard(ab_ is not None and all(exact.values()) and all(v == [] for v in resid.values()) and nonnoop and set(rpm) == set(P[n]['paths']),
             '#%s == its CANONICAL patch EXACTLY: %s; every blob == head %s; diff(golden-applied, head) EMPTY in every path; the patch touches exactly the PR\'s paths %s; control (the apply is not a no-op: every applied blob differs from the merge-base\'s): %s' % (
                 n, am, {os.path.basename(p): v for p, v in exact.items()}, sorted(set(rpm)) == sorted(P[n]['paths']), nonnoop))
        hpm = {p: pm_diff(cb, h, p) for p in P[n]['paths']}
        ident = {p: ('IDENTICAL' if rpm.get(p, []) == hpm[p] else 'SLIDE-EQUAL (same lines, another order)' if sorted(rpm.get(p, [])) == sorted(hpm[p]) else 'DIFFER') for p in P[n]['paths']}
        hard(all(v != 'DIFFER' for v in ident.values()), '#%s READY +/- identity per file (net of identical -/+ pairs): %s' % (n, {os.path.basename(p): v for p, v in ident.items()}))
        out.append('READY IDENTITY (MEASURED): %s (sha256 %s) — its diff block == the golden %s == the checker\'s patch.diff (the CANONICAL patch): %s / %s; `git apply --cached --check` then apply, STRICT, at the merge-base %s: %s -> every blob == head: %s; diff(golden-applied, head) EMPTY: %s; +/- identity %s; %s' % (
            os.path.basename(rp), rs[:16], GOLDEN[n][0].replace(BRIEFS, 'briefs/'), gsame, csame, cb[:12], am, all(exact.values()), all(v == [] for v in resid.values()), {os.path.basename(p): v for p, v in ident.items()},
            ('the READY\'s closing fence is GLUED to its last diff line %r: stripped' % glued[1]) if glued else 'no glued fence'))
        MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_bytes_eq_golden': gsame, 'checker_eq_golden': csame, 'golden': GOLDEN[n], 'golden_sha256': gs,
                   'apply': am, 'blobs_eq_head': exact, 'residue_empty': all(v == [] for v in resid.values()), 'identity': ident}
    # --- cells (READ): every test file the PR touches, at the merge-base and at head
    for t in tests:
        tt, t0 = show(h, t), show(cb, t)
        d0, d1 = describes(t0), describes(tt)
        out.append('CELLS (READ, %s): %d `it(`/`it.each(` entries at the merge-base, %d at head; NEW at head: %s; GONE at head: %s; describe %s -> %s' % (
            os.path.basename(t), len(its(t0)), len(its(tt)), [x[:80] for x in its(tt) if x not in its(t0)][:12] or 'NONE', [x[:80] for x in its(t0) if x not in its(tt)] or 'NONE', d0[:3], d1[:3]))
    svc = K['prs'][n]['service']
    pkg = show(REAL_DEV, 'Blockchain/Dev/' + svc + '/package.json')
    out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r; scripts.lint = %r' % (svc, (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1], (re.search(r'"lint"\s*:\s*"([^"]*)"', pkg) or [None, 'ABSENT'])[1]))
    # --- the cross-package census (standing requirement 2)
    cz = census(h, P[n]['paths'])
    pk = sorted({pkg_of(f) for v in cz.values() for f in v} | {pkg_of(p) for p in P[n]['paths'] if p.startswith('Blockchain/')})
    out.append('CROSS-PACKAGE CENSUS (READ, `git grep -l -F` over Blockchain/Dev at head, fragments = file name and <parent>/<stem>, globs *.test.ts *.test.js *.test.sh __tests__/*.sh): %s — the suites the gate RUNS for #%s: %s' % (
        {os.path.relpath(p, 'Blockchain/Dev') if p.startswith('Blockchain/') else p: [os.path.relpath(f, 'Blockchain/Dev') for f in v] or 'NONE' for p, v in cz.items()}, n, pk))
    MEAS[n]['cross_package'] = {'files': cz, 'packages': pk}
    # --- the KS-764 guard (standing requirement 1: pre-existing red, NAMED): emulate its two security revoke regexes at develop / head / END, READ
    rw = re.compile(r'isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(')
    k764 = {lab: bool(rw.search(show(c, SECIDX))) for lab, c in (('merge-base', cb), ('develop', REAL_DEV), ('head', h), ('END_TREE', END))}
    _ctl = bool(rw.search('apiKey.isActive = false;\n  await dbSaveApiKey(apiKey);'))
    hard(_ctl and not any(k764.values()), '#%s KS-764 PRE-EXISTING RED (READ, the guard\'s own CALL_SITES regex `isActive\\s*=\\s*false;[\\s\\S]{0,80}dbSaveApiKey\\(` over security index.ts): matches %s — NO match anywhere on the line (the red is develop\'s since #1327 and neither PR touches security index.ts: %s); control (the pre-#1327 idiom) matches: %s' % (
        n, k764, SECIDX not in P[n]['paths'], _ctl))
    alw = {lab: ('services/api-gateway/src/startup-migrations.ts' in show(c, KS764)) for lab, c in (('develop', REAL_DEV), ('head', h))}
    sm_h = show(h, SMIG); sm_d = show(REAL_DEV, SMIG)
    ment = {lab: (bool(re.search(r'svc_api_keys', t_)) and bool(re.search(r'is_active', t_)), bool(re.search(r'UPDATE\s+svc_api_keys\s+SET\s+is_active\s*=\s*false', t_, re.I)) or bool(rw.search(t_))) for lab, t_ in (('develop', sm_d), ('head', sm_h))}
    out.append('KS-764 GUARD (READ, standing requirement 1): develop carries `packages/shared` 1 failed / 945 since #1327 — the CALL_SITES cell (ks764-key-revoke-call-site-guard.test.ts, CALL_SITES :77 / REVOKE_WRITES :97; the failing `it` is \'CALL_SITES matches every revoke surface…\' :263); the security regex matches nowhere (%s), so the SAME one cell reds at develop, at #%s\'s head and on END_TREE unless a PR changes it — PRE-EXISTING, not a NO GO against this kit (its fix is held separately). Its allowlist NON_REVOKE_MENTIONS names startup-migrations.ts (develop %s, head %s); startup-migrations.ts (mentions svc_api_keys AND is_active, matches a REVOKE_WRITES idiom): develop %s, head %s — the gate RUNS the guard at #%s\'s head and reports the drift cell (\'no file mentions svc_api_keys + is_active except…\' and \'every allowlisted non-revoke really is present…\')' % (
        k764, n, alw['develop'], alw['head'], ment['develop'], ment['head'], n))
    MEAS[n]['ks764'] = {'security_regex_matches': k764, 'allowlist_names_startup_migrations': alw, 'startup_migrations_mention_and_revoke': ment}
    # --- per-class probes
    if cls == 'verify-truth':
        v0, v1 = show(cb, SHV), show(h, SHV)
        added = [l[1:] for l in pm_diff(cb, h, SHV) if l[0] == '+']
        pushes = [l.strip() for l in added if 'errors.push(' in l]
        found_conds = [l.strip() for l in added if re.search(r'\bfound\b', l) and l.strip().startswith('if (')]
        WANT_PUSH = sorted(['errors.push(', "errors.push('Credential has been revoked in the status list');", 'errors.push(`Failed to check credential status: ${error}`);', 'errors.push(`Failed to check credential status: ${error}`);'])
        hard(sorted(pushes) == WANT_PUSH and sorted(found_conds) == sorted(['if (record.found && record.revoked) {', 'if (listed.found && listed.revoked) {']),
             '#%s PASS-THROUGH IS EXACTLY WHAT SHIPS (READ, the verifier diff): the only NEW failure conditions are the two `found && revoked` tests %s and the resolvers\' own throw — the `errors.push(` lines ADDED are EXACTLY %d: the stored-record revoke (a multi-line call), the status-list revoke, and one `Failed to check credential status` per arm\'s catch; an id the resolver reports `found: false` pushes NOTHING on either arm' % (n, found_conds, len(pushes)))
        rv_msgs = [l.strip()[:70] for l in added if 'revoked' in l and ('`Credential has been revoked' in l or "'Credential has been revoked" in l)]
        out.append('PASS-THROUGH (READ; the card secuura-ks1352-unknown-credential-id-verify-policy is OPEN, default a = pass-through; KS-1368 filed): for `found: false` BOTH arms abstain (no error); the failures ADDED are `record.found && record.revoked` (%s) and `listed.found && listed.revoked` (the status list), plus a resolver THROW, which pushes `Failed to check credential status: …` and FAILS the credential (fail-CLOSED on a resolver error — wider than pass-through? the gate says whether a DB-less getById can throw, READ credentialRepo getById / loadFromDb); the gate measures that an unknown id verifies exactly as at develop (C2) and nothing wider: a known-not-revoked id, a known-revoked id by each route, an unknown id WITH and WITHOUT a submitted credentialStatus, and a status-list entry revoked for an id with no stored record' % rv_msgs)
        cond0 = [l for l in v0.split('\n') if 'this.config.checkStatus && credential.credentialStatus' in l]
        out.append('THE GATE WIDENED (READ, verifier.ts): develop runs checkStatus only `if (this.config.checkStatus && credential.credentialStatus)` (%d line) — head also when either new resolver is configured, and the no-credentialStatus return now carries the arms\' errors (`{ valid: errors.length === 0, errors }` where develop returned `{ valid: true, errors: [] }`). The INDEX-keyed `statusListResolver` branch below is unchanged; `checkStatus` defaults TRUE in the constructor (:81), so presentations/verify (which passes ONLY the resolvers) now checks status too' % len(cond0))
        rg = {'credentials.ts': locate(h, CRED, "      ...revocationVerifierConfig(),"), 'presentations.ts': locate(h, PRES, "          ...revocationVerifierConfig(),")}
        callers = [x for x in grep_rev(h, r'verifyCredential\(|new VerifiableCredentialVerifier\(|createVerifier\(', 'Blockchain/Dev/services', 'Blockchain/Dev/packages') if '__tests__' not in x and '/vc/verifier.ts' not in x]
        out.append('THE WIRING (READ): revocationVerifierConfig() spread at credentials.ts %s and presentations.ts %s; EVERY other non-test caller of the shared verifier at head: %s — any caller NOT wired still verifies a revoked credential (the gate names each and says whether it is reachable)' % (
            rg['credentials.ts'], rg['presentations.ts'], [x.split(':', 1)[1].split('/Dev/')[1] + ':' + x.split(':')[2] for x in callers if 'credentials.ts' not in x and 'presentations.ts' not in x] or 'NONE'))
        prism = grep_rev(h, r"app\.post\('/api/credentials/verify'", 'Blockchain/Dev/services/prism/src')
        gwr = grep_rev(h, r"router\.(use|post)\('/api/(credentials|presentations/verify|presentations|status)'", 'Blockchain/Dev/services/api-gateway/src/routes/proxy.ts')
        out.append('THE GATEWAY PATHS (READ, api-gateway proxy.ts at head): %s — /api/credentials, /api/presentations and /api/status reach vc-issuer; a SECOND `POST /api/credentials/verify` exists in services/prism (%s) with its own checks and NO revocation check — the gateway does not route /api/credentials there (READ), so it is reachable only on prism\'s own port: the gate says whether it is a finding for this PR (a sibling of the defect, out of KS-1352\'s two named routes) or a follow-up. The seat left `/api/verification/*` (originate: DOCUMENT verification) and `/api/batch/verify` (document hashes) UNREAD — the gate reads both and says whether either verifies a CREDENTIAL' % (
            [x.split(':')[2] + ' ' + x.split(':', 3)[3].strip()[:60] for x in gwr], [x.split('/Dev/')[1][:60] for x in prism]))
        sm = show(h, STAT)
        ge = [i + 1 for i, l in enumerate(show(h, 'Blockchain/Dev/packages/shared/src/vc/status.ts').split('\n')) if re.match(r'\s*(getEntry|isRevoked)\(credentialId: string\)', l)]
        out.append('ID-KEYED STATUS BIT (READ): statusListRevocation(credentialId) walks every manager in `statusListManagers` and answers `found` by `manager.getEntry(credentialId)` (shared vc/status.ts getEntry / isRevoked keyed by credentialId at %s) — so a status-list revoke keyed by the SAME id the stored record uses; the index-keyed statusListResolver is untouched. `found: false` for an id allocated in ANOTHER replica (process state; the seat says so)' % ge)
        bk = show(h, BACKLOG); bk0 = show(cb, BACKLOG)
        bkeys = sorted(set(re.findall(r'KS-\d+', ''.join(l[1:] for l in pm_diff(cb, h, BACKLOG) if l[0] == '+'))))
        out.append('BACKLOG.md IN A KS-1352 PR (READ): +%d lines recording the PRE-EXISTING packages/shared red (the KS-764 guard) — a DOC file outside the ticket\'s product scope; its added lines carry hyphenated keys %s AS CONTENT (a squash body quoting them would attach foreign tickets). The gate says whether a BACKLOG entry belongs in this PR (a finding, scope) — the body says "BACKLOG.md records a RED that is NOT from this change"' % (len([l for l in pm_diff(cb, h, BACKLOG) if l[0] == '+']), bkeys))
        MEAS[n]['verify'] = {'new_failure_conditions': found_conds, 'errors_push_added': len(pushes), 'wiring': rg, 'backlog_keys': bkeys}
    if cls == 'schema-startup':
        s1, s0 = show(h, SMIG), show(cb, SMIG)
        m1 = show(h, M039)
        trk = {'records on success': "INSERT INTO _secuura_migrations (filename) VALUES ($1)" in s1, 'skips a recorded file': "SELECT 1 FROM _secuura_migrations WHERE filename = $1 LIMIT 1" in s1}
        nt = re.findall(r"RAISE NOTICE '(KS-1054: oauth_apps absent[^']*)'", m1)
        hard(all(trk.values()) and len(nt) == 1, '#%s THE TRACKER (READ, startup-migrations.ts applyFileMigrations at head): %s — a file that SUCCEEDS is recorded and never re-run' % (n, trk))
        out.append('FRESH-DB-039-NEVER-COMPLETES (READ — a PREDICTED DEFECT the gate MUST measure on a REAL bare database): on a database WITHOUT oauth_apps at stage 1 the head\'s 039 takes the guard\'s ELSE branch, RAISEs a NOTICE, and SUCCEEDS — so applyFileMigrations RECORDS `039_rls_fail_closed.sql` in `_secuura_migrations` (%s) and every later boot SKIPS it. The NOTICE says %r — READ, nothing re-runs a recorded file, so `auth_find_oauth_app_by_client_id` would NEVER be created there, and the oauth_apps grant / policy block (039 :160-:165, table-guarded since before this PR) is skipped for good too. At the merge-base the same database FAILS 039 on boot 1 (not recorded) and applies it WHOLE on boot 2, once CORE has created oauth_apps. Callers of the function: %s. The gate runs the two-sided drill: fresh bare DB at base vs head, boot TWICE each, then reads `to_regprocedure(\'auth_find_oauth_app_by_client_id(text)\')`, the oauth_apps policy, and `_secuura_migrations`' % (
            trk, nt[0][:150] if nt else None, [x.split('/Dev/')[1][:70] for x in grep_rev(h, r'auth_find_oauth_app_by_client_id\(\$1\)', 'Blockchain/Dev/services') if '__tests__' not in x]))
        di = grep_rev(h, r'CREATE TABLE IF NOT EXISTS oauth_apps', 'Blockchain/Dev/docker/init', 'Blockchain/Dev/migrations')
        out.append('WHICH FRESH DATABASES (READ): oauth_apps is created by docker/init %s (a docker-compose stack\'s Postgres runs init/ at its FIRST start, BEFORE the gateway — there the guard is INERT and 039 runs whole on boot 1) and by the gateway\'s CORE_MIGRATIONS (stage 2); NO migrations/*.sql creates it. The boot-1 failure — and the new skip — happen only on a database the gateway meets WITHOUT docker/init (a managed Azure database, a restored or hand-made one): the gate says which deployed databases those are' % [x.split('/Dev/')[1][:60] for x in di])
        catches = [(i + 1, l.strip()) for i, l in enumerate(s1.split('\n')) if re.match(r"\s*log\('warn', '(Main|Platform) DB migrations failed'", l)]
        after = {ln: s1.split('\n')[ln] .strip() for ln, _ in catches}
        out.append('CORE-THROW-READS-CLEAN (READ): the file-stage catches add `totalFailed += 1` (:1010, :1025) — the stage-2 CORE catches do NOT: %s each followed by %s — so a main or platform CORE run that THROWS (not one that counts a failure) records `failed` without it; and `recordStartupMigrations` is called ONCE (:1272) with `{ applied, failed }` only — the `error?` field the summary declares ("Present only when a stage threw") is NEVER set (callers passing `error`: %d); (provisionAppRole, which runs just before the record, catches its own errors — READ.) The drafter\'s real-Postgres run (THE POSTGRES below) shows the SHARPER case: on a bare database the head\'s boot 2 records `failed: 0` while auth_find_oauth_app_by_client_id and the oauth_apps_auth_lookup policy are ABSENT for good — /health reads CLEAN over a database 039 never completed. The gate drives each and says whether any is a finding against "a stage that THREW never reports clean"' % (
            catches, list(after.values()), len(re.findall(r'recordStartupMigrations\(\{[^}]*error', s1))))
        hc = [i + 1 for i, l in enumerate(show(h, HLTH).split('\n')) if 'res.status(ready ? 200 : 503)' in l]
        out.append('/health AND /health/ready (READ, health.ts at head): both carry `startupMigrations: getStartupMigrations()` (:94, :199); /health/ready\'s code is still `res.status(ready ? 200 : 503)` (%s) and `ready` does not read the field — the gate SERVES both on a real listener (port 0) after a failing and a clean run, and reads the bodies as served: `{ ran, applied, failed, lastRunAt }` (+ `error`?), `ran: false` before any run, SET not latched across two runs' % hc)
        rb = [x.split(':')[2] for x in grep_rev(h, r'runStartupMigrations\(\)', GW + 'index.ts')]
        out.append('WHO READS THE RESULT (READ): runStartupMigrations() is called from api-gateway index.ts at %s (runDbBootTasks — initDb\'s onReady hook, and the KS-377 background retry); the deploy scripts\' /health checks (deploy-all.sh:281 — OUT OF SCOPE, ruled; deploy.sh:823) do NOT read `startupMigrations.failed` at this head (the gate greps them) — so a failed migration reads on /health but no deploy fails on it yet: the ruling\'s "the deploy reads as failed" half is a follow-up' % rb)
        wid = {os.path.basename(p): pm_diff(cb, h, p) for p in WIDENED}
        def _wok(v):
            mi = [l for l in v if l[0] == '-']; pl = [l for l in v if l[0] == '+']
            return len(mi) == 1 and 'Promise<void>' in mi[0] and len([l for l in pl if 'Promise<unknown>' in l]) == 1 and all(l.lstrip('+').strip().startswith('//') or 'Promise<unknown>' in l for l in pl)
        hard(all(_wok(v) for v in wid.values()) and not _wok(['-a', '+b']),
             '#%s THE FOUR WIDENED ANNOTATIONS (READ): each file changes ONE `-` line (Promise<void>) for ONE `+` Promise<unknown> line plus comment lines only (control: a non-annotation pair is refused): %s' % (n, {k: '-%d/+%d' % (len([l for l in v if l[0] == '-']), len([l for l in v if l[0] == '+'])) for k, v in wid.items()}))
        out.append('TS2322 x4 (READ; the seat: "the including program was 29 errors at the pristine tip, 33 with my change, 29 again after widening"): the gate type-checks api-gateway with `exclude: []` at the launch develop, #%s\'s head and END_TREE, lists the program (every touched file in it), and compares the WHOLE error SET (not the count): delta must be zero, and none of the 29 may be in a touched file' % n)
        hk = [x.split('@@')[1].strip() for x in g('diff', cb, h, '--', M039).splitlines() if x.startswith('@@')]
        hs = [i + 1 for i, l in enumerate(s1.split('\n')) if 'KS-1054 — WHY STAGE 2 STILL RUNS SECOND' in l]
        out.append('THE ":5-21" HEADER (READ): the READYs say the decision is recorded in "the `:5-21` header" — 039\'s diff hunks are %s (the guard and the loop ONLY; 039 :1-:24 is byte-unchanged: KS-458\'s header), while startup-migrations.ts — whose OWN header :5-:21 describes the stage order — gained the KS-1054 record at :%s. The gate says which file the brief\'s ":5-21" named and whether the record is where it was asked for' % (hk, hs))
        if PG and '_summary' in PG:
            R_ = PG['runs']; rd = lambda k: {kk: R_[k].get('db', {}).get(kk) for kk in ('tracked_039', 'fn_auth_find_oauth_app_by_client_id', 'oauth_apps_auth_lookup_policy')}
            out.append('THE POSTGRES (MEASURED by the drafter, pgprobe_gate38.py -> pgprobe_1.out / pgprobe_gate38.json: the REAL runStartupMigrations from the scratch clone at the merge-base and at the head, run by node + the checkout\'s tsx CJS hook on %s over a UNIX SOCKET ONLY (listen_addresses=\'\', lsof 0 inet sockets), a fresh BARE database per side booted TWICE, and a docker/init-seeded one booted once): %s — BARE-base boot 1 %s, boot 2 %s; BARE-head boot 1 %s (recorded %s), boot 2 %s (recorded %s); INIT-head boot 1 %s; controls %s. FRESH-DB-039-NEVER-COMPLETES is therefore a MEASURED regression of the bare-database END STATE (the base heals at boot 2, the head never does) traded against a boot-1 fail-OPEN window the base had — the gate re-measures it and RULES it' % (
                PG.get('engine', '?')[:40], PG['_summary'], rd('BARE-base boot 1'), rd('BARE-base boot 2'), rd('BARE-head boot 1'), json.dumps(R_['BARE-head boot 1'].get('recorded')), rd('BARE-head boot 2'), json.dumps(R_['BARE-head boot 2'].get('recorded')), rd('INIT-head boot 1'), PG['controls']))
            MEAS[n]['pgprobe'] = {'summary': PG['_summary']}
        else: out.append('THE POSTGRES: pgprobe_gate38.json ABSENT — UNMEASURED by the drafter')
    if cls == 'certify-status':
        c1 = show(h, CERT)
        sites = [i + 1 for i, l in enumerate(c1.split('\n')) if "...(anchoringStatus === 'failed' ? { status: 'failed' } : {})," in l]
        conf = [i + 1 for i, l in enumerate(c1.split('\n')) if "confidence: 'pending-onchain'," in l]
        hard(len(sites) == 2, '#%s TWO ROUTES (READ): the failed-status spread occurs exactly twice at head %s (issue, recertify), each inside a `confidence: \'pending-onchain\'` blob %s' % (n, sites, conf))
        rd = {x.split(':', 1)[1].split('/Dev/')[1].split(':')[0] + ':' + x.split(':')[2]: x.split(':', 3)[3].strip()[:90] for x in grep_rev(h, r"status === 'failed'|status !== 'anchor_failed'|status === 'anchor_failed'", 'Blockchain/Dev/services/originate/src', 'Blockchain/Dev/services/api-gateway/src') if '__tests__' not in x}
        out.append('THE READERS OF THE NEW LITERAL (READ, at head): %s — originate\'s verify paths read `failed || anchor_failed` as failed; documents.ts :1098 / :1532 (anchored) and :1338 (the retry guard) read only `anchor_failed`, so a bare \'failed\' reads ANCHORED and NOT retryable there (the READY and the body both say so: "Nothing gets worse" — the blob had no status before). The gate says whether a CERTIFICATION blob ever reaches documents.ts (certificationRepo vs documentRepo) and what the api-gateway maps \'failed\' to (verification.ts ~:232) — served, not read' % rd)
        out.append('NOT A STATUS FIELD ONLY (READ): the saved blob keeps `confidence: \'pending-onchain\'` beside `status: \'failed\'` — the gate reads every consumer of `confidence` and says whether a failed anchor still presents as pending anywhere (Kam ruled b: the status, not the confidence — option a relabelled confidence)')
        k1293 = grep_l(h, 'ANCHORING_SERVICE_URL', 'Blockchain/Dev/services/originate/src/__tests__/*.test.ts')
        out.append('THE HERMETIC GATE (READ): the cells are APPENDED to ks543 because "a new file that sets ANCHORING_SERVICE_URL reddens ks1293\'s hermetic gate" (the body) — originate test files naming ANCHORING_SERVICE_URL at head: %s; the gate runs ks1293\'s hermetic cell at the head and END_TREE and says it stays green' % [os.path.basename(x) for x in k1293])
    if cls == 'test-only-pin':
        prodtouch = [p_ for p_ in P[n]['paths'] if '__tests__' not in p_]
        hard(not prodtouch, '#%s TEST-ONLY (READ): no product path in the PR %s' % (n, prodtouch or 'NONE'))
        out.append('TEST-ONLY CONTRADICTION (READ): the PR body says the cells are "GREEN at the untouched tip by design" (validate already logs-only: index.ts :1369 no opt-in, :332 the one log line, :336 rethrow only on opt-in); the READY\'s checker verdict says "RED-FIRST: … fails at the untouched tip (1 failed / 19 run; … assertion reds)" — both cannot be true of the same bytes. The gate runs the ks888 file at the merge-base with the PR\'s cells, names any red cell and its assertion, and rules which claim holds (a red at the tip would mean the pin asserts behaviour the product lacks). All discrimination is in the ARMS (the body: log line removed / doubled / carrying the key hash / the REFUSE shape installed) — the gate re-runs each on the PRODUCT file in its own worktree and restores by bytes')
        out.append('KS-888 ON THE SAME FILE AS #1327 (READ): the cells land in ks888-failed-mint-save-issues-no-key.test.ts, whose describe #1327 (MERGED) renamed; the fullName of every new cell carries that describe — the gate greps every fleet list for the new titles as for #1327\'s. The UNMEASURED doubt the READY carries: validate\'s upsert writes is_active from memory (index.ts :316-:318), so a stale replica could undo another replica\'s revoke — the gate reads it and says whether it is a finding (a TICKET, not this PR)')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT, 'merge_bases': MB,
       'end_tree': END, 'end_tree_with_sibling': None, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES, 'measured': MEAS,
       'stacks': ST, 'retarget': RT, 'declared_overlap': DOV, 'noop_paths': NOOP, 'sibling_paths': {}, 'sibling_heads': {},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': {}, 'dead_open_declared': {},
       'titles': {n: AP[n]['title'] for n in NS}}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | merge-bases %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, [m[:12] for m in MB]))
sys.exit(1 if FAIL else 0)
