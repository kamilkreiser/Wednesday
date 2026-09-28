#!/usr/bin/env python3
"""predict_gate36.py — MEASURE the gate36 kit (the directory this script lives in; its PR set, tiers, classes, commit counts, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate35's predict (gate34 -> gate33 lineage) and re-keyed for gate36: the four rows of Seat B 38th's round, NONE stacked, all on develop
d9ce1403d158 — T1: #1323 KS-1129 item 4 LIVESCAN (api-gateway routes/verification.ts: the LIVE chain-scan read gets the three shape guards KS-1069 gave the
persisted read; a Spark READY) and #1324 KS-1124 O1 MINTMERGE (originate routes/documents.ts: the thread-token cache write re-reads the document and
merges into the blob as persisted; a Spark READY; it NARROWS the overwrite race and does not close it); T2: #1325 KS-1227 (TEST-ONLY, the ks1072 witness
keeps count-every-stub-request, a note and a reworded message; seat-written) and #1326 KS-1351 item 1 (TYPES-ONLY, a SecuuraCredentialStatus extension
declares the revocation fields + a let -> const at vc-issuer credentialRepo.ts:95; seat-written). Each PR is measured over ITS OWN develop merge-base and
merged over the CURRENT develop (merge-tree with that merge-base). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json
`inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles AND
`widen_branch_rx` on branches) is HARD: an open PR matching either outside this kit refuses.

TIER BY CLASS (kit.json `class`): `verify-claim` / `blob-write` (T1) change EXACTLY ONE runtime product file and one test file; `test-only` (T2) changes NO
product file; `types-only` (T2) changes EXACTLY the two declared product files (shared vc/types.ts, vc-issuer credentialRepo.ts) and no test file — its
no-runtime-change claim is MEASURED by emitprobe_gate36.py (run AFTER this script; its JSON is read here when present).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths: a merged blob DIFFERENT from the head's) and `noop_paths` (the
squash-stack NO-OP: head == merged == develop) are SEPARATE keys; gate36 declares neither, and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
VERIFIED BYTES == USED BYTES (STANDING_LINES 2026-09-27): every READY / golden is read ONCE into memory, its sha256 printed, and those SAME bytes are
compared and applied (written to a scratch file whose sha256 is re-asserted equal at the point of use).
`git apply --check` (STANDING_LINES 2026-09-27, "`patch -F0` is not `git apply --check`"): every golden is verified with `git apply --cached` in a
scratch index seeded from the merge-base tree (strict: no --recount, no fuzz, no -C) — the tool the seat applies with — never with GNU patch.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate36 / Seat B 38th and is checked by rekey_check_gate36.py (which carries its own name in its own token map).
TWO ROWS HAVE NO READY (#1325, #1326 — seat-written, READ in the seat's ITEM 4 / ITEM 5 records): their READY-identity lines say so; nothing is compared.
A RED-ARM ANCHOR that is not byte-unique as a single line (credentialRepo.ts `const result = …` occurs at :95 AND at :118, getByHash) is located by
the line AND its predecessor line (a two-line anchor), and the probe says so.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g36_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into
THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate36.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate36.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g36_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate36 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g36/develop']
    + ['+refs/pull/%s/head:refs/g36/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g36/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g36/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g36/pull/' + n).strip() == g('rev-parse', 'refs/g36/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g36idx', dir=os.path.join(SP, 'g36_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE36-SIMULATED-MOVE.txt', 'gate36 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate36 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE36-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate36 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate36 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g36/pull/' + n).strip()
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
    """split a unified diff into {(old path, new path): [lines]} by '--- ' / '+++ ' header pairs"""
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
    written are the bytes verified (sha256 at the point of use). Returns ({path: blob} or None, message)."""
    W = os.path.join(SP, 'g36_sp'); fp = tempfile.mktemp(prefix='g36apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16])
    idx = tempfile.mktemp(prefix='g36gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=e3)
    rchk = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', '--check', fp], capture_output=True, text=True, env=e3)
    if rchk.returncode != 0: return None, '`git apply --cached --check` REFUSES at %s (rc %d): %s [bytes used sha256 %s == verified]' % (base[:12], rchk.returncode, rchk.stderr.strip()[:220].replace('\n', ' / '), used[:16])
    ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', fp], capture_output=True, text=True, env=e3)
    if ra.returncode != 0: return None, 'apply rc %d after a passing --check: %s' % (ra.returncode, ra.stderr.strip()[:160])
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
    return {p: blob(t_, p) for p in paths}, '`git apply --cached --check` rc 0 and apply rc 0 at %s (strict) [bytes used sha256 %s == verified]' % (base[:12], used[:16])
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
NIGHT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
BRIEFS = NIGHT + 'briefs/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
# the READY each PR was raised from, NAMED (never globbed: the 09-17 Ornith KS-1227 READY sits in the same directory and is NOT this round's — #1325 and
# #1326 were written by the seat, READ in its ITEM 4 / ITEM 5 records); None = no READY
READY = {
 '1323': NIGHT + 'READY_KS-1129-KS-1129-LIVESCAN-R1_spark-dsv4flash_BRIEFED-CODEPATCH-KS1129-LIVESCAN-SHAPE-GUARDS-PASS-7of7_2026-09-28.diff.md',
 '1324': NIGHT + 'READY_KS-1124-KS-1124-MINTMERGE-R1_spark-dsv4flash_BRIEFED-CODEPATCH-KS1124-MINT-MERGE-STORED-PASS-7of7_2026-09-28.diff.md',
 '1325': None,
 '1326': None,
}
# the canonical bytes each READY PR must equal — the brief-writer's golden (== the Spark checker's patch.diff, READ at drafting) — verified with
# `git apply --cached --check` at the merge-base
GOLDEN = {
 '1323': [BRIEFS + 'KS-1129-livescan/KS-1129.golden.diff'],
 '1324': [BRIEFS + 'KS-1124-mintmerge/KS-1124.golden.diff'],
}
CHECKER = {'1323': 'spark_secuura_2026-09-28_KS-1129-LIVESCAN-R1', '1324': 'spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1'}
GW = 'Blockchain/Dev/services/api-gateway/src/'
O = 'Blockchain/Dev/services/originate/src/'
VERIF, WIT = GW + 'routes/verification.ts', GW + '__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
DOCS, ASYNC = O + 'routes/documents.ts', O + 'services/anchorStateSync.ts'
VCT, CREPO = 'Blockchain/Dev/packages/shared/src/vc/types.ts', 'Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts'
CREPO_T = 'Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts'
# the line(s) each red arm is planted at — FROM the brief / the PR body / the seat record (READ), re-located here by exact WHOLE-LINE match at head,
# develop and END_TREE. A 4th field, when present, is the PREDECESSOR line (a two-line anchor for a line that is not byte-unique alone)
TAMPER = {
 '1323': [(VERIF, "          if (j.verified === true && !j.simulated) {", 607, 'the strict verified / simulated guard (the brief\'s arm: `if (j.verified) {` -> L1, L6 red, 2 of 20)'),
          (VERIF, "            liveTxHash = typeof liveHash === 'string' && !/^(tx_sim_|mock_tx_|tx_)/.test(liveHash) ? liveHash : null;", 609, 'the placeholder-hash guard (the brief\'s arm: `liveTxHash = liveHash;` -> L2 red, 1 of 20)'),
          (VERIF, "            liveBlockHeight = typeof blockNum === 'number' && Number.isInteger(blockNum) && blockNum > 0 ? blockNum : null;", 611, 'the integer-height guard (the brief\'s arm: `blockNum != null ? Number(blockNum) : null` -> L3, L4, L5 red, 3 of 20)')],
 '1324': [(DOCS, "                ...(current?.blockchain || document.blockchain || {}),", 802, 'the merge spread (the brief\'s arm: `...((current?.blockchain && document.blockchain) || {}),` -> M1 red, 1 of 6; the seat\'s arm reverts spread + declaration together — reverting the spread alone is a TS6133 LOAD failure)'),
          (DOCS, "            const current = await getDocument(id, tenantId).catch(() => null);", 799, 'the read-back (a gate arm: a getDocument that REJECTS -> the `.catch(() => null)` fallback writes the create-time copy again; say which cell, if any, reds)')],
 '1325': [(WIT, "  expect(anchorStoreUrls, 'KS-1180: tier 2 was ASKED once - exactly one anchor-store read of this document').toEqual(['/api/anchors/document/' + DOC_ID]);", 140, 'the witness message (the seat\'s coupling arm: reword it, leave R1 at the old string -> R1 red, 1 of 8)'),
          (WIT, "      expect(witness).toContain('KS-1180: tier 2 was ASKED once');", 208, 'R1\'s expected substring (a gate arm: restore the OLD message here -> R1 red)')],
 '1326': [(VCT, "  credentialStatus?: SecuuraCredentialStatus;", 136, 'the narrowing (a gate arm: remove it, REBUILD packages/shared -> the four TS2339 return)'),
          (VCT, "  revoked?: boolean;", 51, 'one declared field (a gate arm: remove it, rebuild shared -> TS2339 at 72:63 and 142:39 only)'),
          (CREPO, "      const result = await query<{ credential: SecuuraCredential }>(", 95, 'item 2 (a gate arm: `const` -> `let` -> eslint prefer-const 1 problem)', "      // Exact match")],
}
def locate(c, p, line, prev=None):
    if not c: return []
    L = show(c, p).split('\n'); return [i + 1 for i, l in enumerate(L) if l == line and (prev is None or (i > 0 and L[i - 1] == prev))]
def its(s): return re.findall(r"^\s*it(?:\.each\([^)]*\))?\(\s*'([^']{0,120})", s, re.M)
def grep_rev(rev, rx, *paths):
    rc_, o_, _ = gq('grep', '-n', '-I', '-E', rx, rev, '--', *paths); return [x for x in o_.strip().splitlines() if x]
PROBES = {}
MEAS = {}
# the comparator's own controls, once (STANDING_LINES 2026-09-27): identical pair IDENTICAL, one token DIFFER, and the empty-string trap caught
_x = ['+a', '-b', '+c']; _y = ['+a', '-b', '+C']
_trap = [l for l in ['+a', ''] if l[:1] in '+-']
CTL_PM = (cmp_seq(pm(_x + ['']), pm(_x)) == 'IDENTICAL' and cmp_seq(pm(_x), pm(_y)) == 'DIFFER' and len(_trap) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, 'CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in \'+-\'` would have counted the empty line (%d vs %d) — the kit uses `l and l[0] in \'+-\'`' % (len(_trap), len(pm(['+a', '']))))
EPJ = os.path.join(GS, 'emitprobe_gate36.json'); EP = json.load(open(EPJ)) if os.path.exists(EPJ) else None
TIER_OF = {'verify-claim': 'T1', 'blob-write': 'T1', 'test-only': 'T2', 'types-only': 'T2'}
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []; cls = K['prs'][n].get('class', '?')
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    tests = [p for p in P[n]['paths'] if p not in prod]
    out.append(('PRODUCT files %s (changed +/- lines %s); TEST files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests])) if prod else 'NO product file changed (test-only): every changed path is a test file %s' % [os.path.basename(p) for p in tests])
    hard(K['prs'][n]['tier'] == TIER_OF.get(cls), '#%s tier %s == the tier its class %s carries (%s)' % (n, K['prs'][n]['tier'], cls, TIER_OF.get(cls)))
    if cls in ('verify-claim', 'blob-write'):
        hard(len(prod) == 1 and len(tests) == 1 and not prod[0].endswith('.openapi.ts'), '#%s (T1, class %s) changes exactly ONE runtime product file %s and ONE test file %s' % (n, cls, prod, [os.path.basename(t) for t in tests]))
    elif cls == 'test-only':
        hard(not prod and len(tests) == 1, '#%s (T2, test-only) changes NO product file and exactly one test file %s' % (n, [os.path.basename(t) for t in tests]))
    elif cls == 'types-only':
        hard(sorted(prod) == sorted([VCT, CREPO]) and not tests, '#%s (T2, types-only) changes EXACTLY the two declared product files %s and no test file %s' % (n, [os.path.basename(p) for p in prod], tests or ''))
    # --- the TAMPER / red-arm anchor(s), whole-line (two-line where declared), at head, develop and END_TREE
    for tt_ in TAMPER[n]:
        tf, tl, tline, tsrc = tt_[:4]; prev = tt_[4] if len(tt_) > 4 else None
        lh, ld, le = locate(h, tf, tl, prev), locate(REAL_DEV, tf, tl, prev), locate(END, tf, tl, prev)
        single_h = locate(h, tf, tl)
        bl = {'head': blob(h, tf), 'develop': blob(REAL_DEV, tf), 'END': blob(END, tf) if END else None}
        hard(len(lh) == 1 and len(le) == 1, '#%s RED-ARM ANCHOR (%s) is byte-unique %s in %s at head %s AND on END_TREE %s%s' % (n, tsrc, 'as a TWO-LINE anchor (with its predecessor line; the line alone occurs at %s)' % single_h if prev else 'as a whole line', tf.split('/src/')[1], lh, le, (' (the brief / seat said :%d)' % tline) if tline else ''))
        out.append('RED-ARM ANCHOR (READ, %s; %s): `%s` in %s — head %s | develop %s | END_TREE %s%s; blob of %s at head %s, develop %s, END %s (%s)' % (
            'TWO-LINE match: the line alone occurs at %s at head, so the gate anchors on it WITH its predecessor `%s`' % (single_h, prev.strip()) if prev else 'whole-line match',
            tsrc, tl.strip()[:110], tf.split('/src/')[1], lh, ld, le, (' | the brief / seat said :%d' % tline) if tline else '', os.path.basename(tf), (bl['head'] or '-')[:12], (bl['develop'] or '-')[:12], (bl['END'] or '-')[:12],
            'the SAME file at head and on END_TREE' if bl['head'] == bl['END'] else 'the file DIFFERS between head and END_TREE — the gate plants at BOTH'))
    # --- READY identity: the READY's ```diff block (READ once) vs the head's +/- lines, per file, in order (the files the READY names)
    rp = READY[n]
    if rp is None:
        out.append('READY IDENTITY: NONE — #%s was written by Seat B 38th itself (its ITEM %s record), not from a local-model READY; there is no golden and no checker patch to compare. Its figures are claims in its PR body and seat record, graded by the gate like any seat claim' % (n, {'1325': '4', '1326': '5'}.get(n, '?')))
        MEAS[n] = {'ready': None}
    elif not os.path.exists(rp):
        hard(False, '#%s READY %s ABSENT' % (n, rp)); PROBES[n] = out; continue
    else:
        rs, rl, glued = ready_block(rp)
        secs = sections('\n'.join(rl)); rpm = {os.path.basename(sec_path(s)[1]): pm(s[2:]) for s in secs}
        hpm_all = {os.path.basename(p): pm_diff(cb, h, p) for p in P[n]['paths']}
        hpm = {k: v for k, v in hpm_all.items() if k in rpm}
        outside = sorted(set(hpm_all) - set(rpm))
        # NET +/- identity (kept from the copied tool: a golden may re-write an unchanged line as a -/+ pair that `git diff -U0` never shows)
        def net(ls):
            ls = list(ls); out_ = []
            for l in ls:
                if l[0] == '-' and ('+' + l[1:]) in ls[ls.index(l):]: continue
                out_.append(l)
            for l in [x for x in ls if x[0] == '-' and ('+' + x[1:]) in ls[ls.index(x):]]:
                out_.remove('+' + l[1:])
            return out_
        rpm_raw = rpm; rpm = {k: net(v) for k, v in rpm.items()}
        hard(net(['+a', '-b', '+b', '+c']) == ['+a', '+c'] and net(['-b', '+c']) == ['-b', '+c'], 'CONTROL (the net comparator): an identical -b/+b pair cancels, a real -b/+c edit does not')
        # SLIDE: an inserted block that begins or ends with a blank line can be represented with the blank at EITHER end (the brief wrote `});` then
        # a blank; `git diff -U0` of the resulting blobs may put it at the other end). The same lines, in a different order, per file: compared as a MULTISET
        # and reported as SLIDE-EQUAL — never as IDENTICAL — with the golden's strict apply + blob equality below as the discriminating instrument
        def slide_eq(a, b): return sorted(a) == sorted(b)
        exact = rpm == hpm
        same = exact or (set(rpm) == set(hpm) and all(slide_eq(rpm[k], hpm[k]) for k in rpm))
        hard(slide_eq(['+', '+a', '+});'], ['+a', '+});', '+']) and not slide_eq(['+a', '+});', '+'], ['+a', '+}));', '+']), 'CONTROL (the slide comparator): a blank line moved to the other end of an insertion reads SLIDE-EQUAL; a one-token mutation reads DIFFER')
        mut = {k: list(v) for k, v in hpm.items()}; k0 = sorted(mut)[0]; mut[k0][-1] = mut[k0][-1] + ' '
        ctl = (hpm == hpm and mut != hpm and not all(slide_eq(rpm.get(k, []), mut[k]) for k in mut))
        rblock = ('\n'.join(rl).rstrip('\n') + '\n').encode('utf-8')
        gsame = sha256b(rblock) == sha256b(open(GOLDEN[n][0], 'rb').read())
        ck = os.path.join(RUNS, CHECKER[n], 'out.md.checker', 'patch.diff')
        csame = os.path.exists(ck) and sha256b(open(ck, 'rb').read()) == sha256b(open(GOLDEN[n][0], 'rb').read())
        hard(same and ctl and not outside, '#%s == its READY (%s, bytes sha256 %s — read once, these bytes compared): NET +/- lines per file %s (raw %s) vs head %s -> %s; head files OUTSIDE the READY %s (none allowed this round); controls (head vs itself IDENTICAL, a one-token mutation DIFFER): %s' % (
            n, os.path.basename(rp)[:70], rs[:16], {k: len(v) for k, v in rpm.items()}, {k: len(v) for k, v in rpm_raw.items()}, {k: len(v) for k, v in hpm.items()}, 'IDENTICAL' if exact else ('SLIDE-EQUAL (%s)' % sorted(k for k in rpm if rpm[k] != hpm.get(k)) if same else 'DIFFER'), outside or 'NONE', ctl))
        out.append('READY IDENTITY (MEASURED, `git diff -U0` merge-base -> head vs the READY block NETTED of identical -/+ pairs (%d cancelled), `l and l[0] in \'+-\'`): %s over %s — the READY block\'s bytes == the golden: %s; the Spark checker\'s patch.diff == the golden: %s — %s' % (
            sum(len(rpm_raw[k]) - len(rpm[k]) for k in rpm), 'IDENTICAL' if exact else ('SLIDE-EQUAL — the same +/- lines per file, ORDER differing in %s only (an insertion slide: the inserted block\'s blank line sits at the OTHER END of the block in the brief than in `git diff -U0`); the golden\'s strict apply below is blob-exact' % sorted(k for k in rpm if rpm[k] != hpm.get(k)) if same else 'DIFFER'), sorted(rpm), gsame, csame, ('the READY\'s closing fence is GLUED to its last diff line %r: stripped as the seat stripped it' % glued[1]) if glued else 'no glued fence'))
        MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_identical': exact, 'ready_slide_equal': same, 'ready_bytes_eq_golden': gsame, 'checker_eq_golden': csame, 'glued_fence': bool(glued), 'outside_ready': outside}
        # --- GOLDEN: `git apply --cached --check` then apply, STRICT, at the merge-base; the blobs must equal the head's
        gb = open(GOLDEN[n][0], 'rb').read()
        gs = sha256b(gb)
        ab_, am = git_apply_at(cb, gb, gs, P[n]['paths'], 'g%s' % n)
        gexact = ab_ is not None and all(ab_[p] == blob(h, p) for p in P[n]['paths'])
        hard(gexact, '#%s == its canonical bytes %s (%d B, sha256 %s, read once): %s -> every blob == head: %s' % (n, ' + '.join(x.replace(BRIEFS, 'briefs/') for x in GOLDEN[n]), len(gb), gs[:16], am, gexact))
        out.append('GOLDEN APPLY (MEASURED, `git apply --cached --check` then apply, strict, at the merge-base %s; %s): %s -> blobs == head: %s' % (cb[:12], ' + '.join(os.path.basename(x) for x in GOLDEN[n]), am, gexact))
        MEAS[n].update({'golden': GOLDEN[n], 'golden_sha256': gs, 'golden_exact': gexact, 'apply': am})
    # --- cells (READ): every test file the PR touches, at the merge-base and at head
    for t in tests:
        tt, t0 = show(h, t), show(cb, t)
        out.append('CELLS (READ, %s): %d `it(`/`it.each(` entries at the merge-base, %d at head; NEW at head: %s' % (os.path.basename(t), len(its(t0)), len(its(tt)), [x[:80] for x in its(tt) if x not in its(t0)] or 'NONE'))
    svc = K['prs'][n]['service']
    pkg = show(REAL_DEV, 'Blockchain/Dev/' + svc + '/package.json')
    out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r; scripts.lint = %r' % (svc, (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1], (re.search(r'"lint"\s*:\s*"([^"]*)"', pkg) or [None, 'ABSENT'])[1]))
    # --- per-class READ probes
    if cls == 'verify-claim':
        vf = show(h, VERIF).split('\n')
        readers = grep_rev(END or REAL_DEV, r'anchors/verify/', GW, ':!*__tests__*')
        ctl_r = grep_rev(END or REAL_DEV, r'persistedTxHashIsReal', GW, ':!*__tests__*')
        hard(len(ctl_r) > 0 and len([x for x in readers if 'fetch(' in x]) == 1, 'CONTROL + census (READ): the grep finds `persistedTxHashIsReal` (%d hits > 0), and api-gateway src (tests excluded) holds exactly ONE live `anchors/verify/` fetch: %s' % (len(ctl_r), [x.split(':', 2)[1] for x in readers if 'fetch(' in x]))
        out.append('THE LIVE READERS (READ, api-gateway src on END_TREE, tests excluded): `anchors/verify/` %s — ONE fetch; the guards cover every live chain-scan reader in the gateway as READ (the ticket\'s "gateway chain-scan readers (a held surface)" is plural — the gate says whether any other reader exists, e.g. in anchoring or originate, and whether the HOLD was ever recorded)' % [x.split(':', 2)[1] + ':' + x.split(':', 2)[2].strip()[:70] for x in readers])
        rxl = [i + 1 for i, l in enumerate(vf) if "/^(tx_sim_|mock_tx_|tx_)/" in l]
        lenc = [i + 1 for i, l in enumerate(vf) if 'persistedTxHash.length > 0' in l]
        out.append('GUARD PARITY (READ, verification.ts at head): the placeholder regex `/^(tx_sim_|mock_tx_|tx_)/` at %s (live and persisted: the SAME rule; `tx_` subsumes the two longer prefixes); the persisted read also demands `length > 0` (:%s) — the live read reaches an empty string only through `j.txHash || j.transactionHash || …`, which skips it, so null (READ: say whether any live shape reaches `\'\'`); NEITHER read demands 64-hex — any other non-prefixed string (\'abc\', \'0x…\') is a hash to both' % (rxl, lenc))
        mix = [(i + 1, l.strip()[:90]) for i, l in enumerate(vf) if l.strip().startswith(('const txHash = liveTxHash', 'const blockHeight = liveBlockHeight', "source: liveTxHash ?", 'confirmedAt: liveConfirmedAt', 'const liveAnchored'))]
        lca = [i + 1 for i, l in enumerate(vf) if l.strip().startswith('liveConfirmedAt = j.confirmedAt')]
        out.append('MIXED-ECHO (READ, verification.ts at head): %s; `liveConfirmedAt` is set at %s inside the verified branch WHETHER OR NOT the hash / height guards accepted — so a reply whose hash is refused still echoes its confirmedAt, and a reply whose HASH passes but HEIGHT is refused yields `source: \'cardano-live\'` with the LIVE hash beside the PERSISTED height (liveAnchored false; `on-chain` then rests on persistedAnchored alone). The claim (`verified` / `confidence`) is what this PR guards; the echoed fields are presentation — the gate measures both and says whether the mixed echo misleads a verifier' % (mix, lca))
        out.append('STRICT HEIGHT (READ, the PR body: "L5 is a behaviour choice"): a numeric-STRING live height is refused where develop coerced it; `blockNumber ?? blockHeight ?? anchor.blockHeight` — a string `blockNumber` does NOT fall back to a numeric `blockHeight` (?? stops at a non-null string). The producer: anchoring emits a number since #1220 (the brief, anchorReadback.ts:134 — the gate READS it at END_TREE and says what a pg BIGINT round-trip returns)')
    if cls == 'blob-write':
        dc = show(h, DOCS).split('\n')
        writes = []
        for i, l in enumerate(dc):
            m = re.match(r'^\s*(?:await\s+)?updateDocument\(id, tenantId, \{\s*(.*)$', l)
            if m:
                blk = ' '.join(x.strip() for x in dc[i:i + 4])
                bm = re.search(r'blockchain:\s*(\{\s*\.\.\.[^,]*|\{\s*[a-zA-Z]+:|[A-Za-z_]+)', blk)
                if bm: writes.append((i + 1, bm.group(1)[:60]))
        mint = [i + 1 for i, l in enumerate(dc) if '.then(async (entry) => {' in l]
        gate = [i + 1 for i, l in enumerate(dc) if "process.env.STATE_THREAD_NFT_ENABLED === 'true' &&" in l]
        out.append('THE BLOB WRITERS ON THE CREATE PATH (READ, documents.ts at head: every `updateDocument(id, tenantId, { … blockchain: … })` and what its blob starts with): %s — the thread-token write (the mint callback at %s, gated at %s on STATE_THREAD_NFT_ENABLED AND SIMULATE_ANCHORING !== \'true\') now spreads the re-read blob; the others REPLACE the column wholesale' % (writes, mint, gate))
        cf = [i + 1 for i, l in enumerate(show(h, ASYNC).split('\n')) if '...carriedForward(' in l]
        out.append('WHAT REMAINS (READ — the PR NARROWS the race and does not close it; the gate measures each): (R1) the WINDOW — a write landing between the read-back (:799) and updateDocument\'s own read + write is still lost (updateDocument re-reads at documentRepo.ts:537 but writes the blob this callback built); (R2) THE MIRROR — the anchor-accept write (`blockchain: initial`, documents.ts ~:913) and the anchor_failed write (~:928) REPLACE the column wholesale and do NOT carry threadToken, so a thread-token write that lands FIRST is erased by them (KS-1074 carried threadToken forward in anchorStateSync.ts at %s, not on the create path) — the O1 bug in the other direction, untouched here; (R3) READ FAILURE — `.catch(() => null)` falls back to the create-time copy, i.e. the pre-PR overwrite, when the read-back rejects; (R4) the updateDocument is not awaited and its rejection is swallowed (`.catch(() => {})`), as before. The atomic fix (a JSONB merge in documentRepo) is an UNRULED design choice (the commit message says so)' % cf)
    if cls == 'test-only':
        w0, w1 = show(cb, WIT), show(h, WIT)
        def msg_and_sub(t):
            m = re.search(r"expect\(anchorStoreUrls, '([^']*)'\)", t); s_ = re.search(r"expect\(witness\)\.toContain\('([^']*)'\)", t)
            return (m.group(1) if m else None, s_.group(1) if s_ else None)
        (m0, s0), (m1, s1) = msg_and_sub(w0), msg_and_sub(w1)
        hard(bool(m0 and s0 and m1 and s1) and s0 in m0 and s1 in m1 and s1 not in m0, '#%s COUPLING (READ): R1\'s expected substring is IN the witness message at the merge-base (%r in %r) AND at head (%r in %r), and the head substring is NOT in the old message (so the two lines really moved together)' % (n, s0, (m0 or '')[:60], s1, (m1 or '')[:60]))
        out.append('THE COUPLING (READ): witness message at the merge-base %r -> head %r; R1\'s toContain %r -> %r (a SHORTER prefix: any change AFTER "ASKED once" no longer reds R1 — the gate says whether that loosening matters). Cell count unchanged (%d -> %d `it(`), as a test-only reword should be; the try/finally detach and R2 (R-1029-3) are ALREADY at develop (READ), so KS-1227\'s remaining item is the counting-rule DECISION — say whether this PR discharges the ticket\'s Definition of done (it says Refs)' % (m0, m1, s0, s1, len(its(w0)), len(its(w1))))
        env_set = grep_rev(REAL_DEV, r"ANCHORING_SERVICE_URL", GW + '__tests__/')
        out.append('WHO POINTS ANCHORING_SERVICE_URL (READ, api-gateway __tests__ at develop): %s — the comment says "today only R1 does" for THIS stub; the gate re-reads it and says whether #1323 (same service, the live read R1 exercises) changes what R1 counts (READ: R1 counts REQUESTS, not replies, so no)' % sorted({x.split(':', 2)[1].split('/')[-1] for x in env_set}))
    if cls == 'types-only':
        rd = grep_rev(END or REAL_DEV, r'credentialStatus\??\.(revoked|revokedAt|revocationReason)', 'Blockchain/Dev', ':!*node_modules*')
        out.append('THE READERS OF THE THREE FIELDS (READ, Blockchain/Dev on END_TREE): %s — the four TS2339 sites the ticket names are credentialRepo.test.ts 72 / 142 / 143 / 144; the issuer portal reads `credentialStatus?.revoked` (the seat: issuer frontend tsc rc 0)' % [x.split(':')[1].replace('Blockchain/Dev/', '') + ':' + x.split(':')[2] for x in rd])
        # POSIX ERE only: this git's grep -E has no \b (and no \s) — a false zero (gate35's drafting lesson); the control below must be > 0
        imp = grep_rev(END or REAL_DEV, r'SecuuraCredential([^A-Za-z]|$)', 'Blockchain/Dev', ':!*node_modules*', ':!*__tests__*', ':!*.test.*')
        hard(len(imp) > 0, 'CONTROL (the consumer grep can find a consumer): `SecuuraCredential` source-line hits %d > 0 (credentialRepo.ts alone names it, READ)' % len(imp))
        out.append('THE NARROWING\'S REACH (READ, Blockchain/Dev on END_TREE, tests excluded): %d source lines in %d files name `SecuuraCredential` (every one is a type-check consumer of the narrowed credentialStatus: %s) — a narrowing of an OPTIONAL property to a subtype with only OPTIONAL additions accepts every VCCredentialStatus value, so no assignment should newly fail; the gate type-checks EVERY consumer of @secuura/shared with shared REBUILT (the seat\'s trap: vc-issuer resolves @secuura/shared to dist/, so an unrebuilt shared reads "4 -> 4")' % (len(imp), len({x.split(':')[1] for x in imp}), sorted({x.split(':')[1].replace('Blockchain/Dev/', '').split('/src/')[0] for x in imp})))
        out.append('KS-1352 IS NOT THIS PR (READ, the seat\'s ITEM 1 and card secuura-ks1352-revoked-credentials-still-verify, OPEN): declaring `revoked` on the type does not make verify READ it — a revoked credential still verifies by either route; the gate says so in the #1326 verdict line, and says whether the declaration makes that defect easier to fix or merely easier to overlook')
        if EP and '_summary' in EP:
            out.append('NO RUNTIME CHANGE — THE EMIT (MEASURED by the drafter, emitprobe_gate36.py -> emitprobe_1.out: each changed file transpiled with the checkout\'s typescript and the package\'s OWN tsconfig compilerOptions, merge-base vs head vs END_TREE): %s; controls %s' % (EP['_summary'], EP.get('_controls')))
            MEAS[n]['emitprobe'] = {'summary': EP.get('_summary'), 'controls': EP.get('_controls')}
        else: out.append('NO RUNTIME CHANGE — THE EMIT: emitprobe_gate36.json ABSENT — UNMEASURED by the drafter')
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
