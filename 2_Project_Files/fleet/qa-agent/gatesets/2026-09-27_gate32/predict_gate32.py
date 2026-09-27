#!/usr/bin/env python3
"""predict_gate32.py — MEASURE the gate32 kit (the directory this script lives in; its PR set, tiers, commit counts, declared stacks (NONE), declared
overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this script.
Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate31's predict_gate31.py (gate30T1 -> gate29 lineage) and re-keyed for gate32: SIX rows, all T2, all raised by Seat B 34th from
local-model READYs, NONE stacked — #1304 KS-1227 (test-only, the ks1072 api-gateway cells edited in place), #1305 KS-1090 R2-3 (a NEW api-gateway cell,
renamed at raise), #1306 KS-1205 F3 (a NEW api-gateway cell on an AUTH surface: no auth product byte may change), #1307 KS-1212 (a NEW api-gateway cell,
renamed at raise), #1308 KS-1108 (systemTest/akto secrets.ts + a NEW akto unit cell with a RULED 16-line lint departure) and #1309 KS-1196 (api-gateway
routes/admin.ts: document-type ids to crypto.randomUUID + a NEW cell). The kit PRs branch from an OLDER develop than the one read now, by design: each is
measured over ITS OWN develop merge-base and merged over the CURRENT develop (merge-tree with that merge-base). No sibling kit. The in-flight census is
EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN census
(kit.json `widen_rx` on titles AND `widen_branch_rx` on branches) is HARD: an open PR matching either outside this kit refuses.

DECLARATIONS (STANDING_LINES 2026-09-27, "a no-op path and an overlap path are different declarations"): kit.json `declared_overlap` (the
merged_blob_paths class: a merged blob DIFFERENT from the head's) and `noop_paths` (the squash-stack NO-OP class: head == merged == develop) are SEPARATE
keys; gate32 declares neither, and (c) asserts that no pair needs one. Every exception key a merge tool would read is printed with its value.

UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): `git rev-parse <sha>:<path>` on a commit the clone does not hold can echo its argument instead of failing.
blob() therefore asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a different blob"), and accepts only a 40-hex
answer whose `cat-file -t` is `blob`. A control in (a) proves the guard fires on a sha the clone does not hold.

VERIFIED BYTES == USED BYTES (STANDING_LINES 2026-09-27): every golden / READY file is read ONCE into memory, its sha256 printed, and those SAME bytes are
the ones compared, split and applied (written to a scratch file whose sha256 is re-asserted equal at the point of use).

`git apply --check` (STANDING_LINES 2026-09-27, "`patch -F0` is not `git apply --check`"): every golden is verified with `git apply --cached` in a
scratch index seeded from the merge-base tree (strict: no --recount, no fuzz, no -C) — the tool the seat applies with — never with GNU patch.

Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g32_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates; git never writes through an
alternate), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed).
Nothing is written into the checkout. Node is used READ-ONLY for one runtime fact (#1309: is `crypto.randomUUID` a global in a CommonJS module).

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate32.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate32.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g32_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate32 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g32/develop']
    + ['+refs/pull/%s/head:refs/g32/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g32/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g32/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g32/pull/' + n).strip() == g('rev-parse', 'refs/g32/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g32idx', dir=os.path.join(SP, 'g32_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE32-SIMULATED-MOVE.txt', 'gate32 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate32 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE32-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate32 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate32 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g32/pull/' + n).strip()
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
         'END_TREE: diff(develop, END) == the union of the six own path sets (%d paths), every END blob == its PR\'s head blob (MG-1: ONE target per file, the head blob)' % len(allown))
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
    W = os.path.join(SP, 'g32_sp'); fp = tempfile.mktemp(prefix='g32apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16])
    idx = tempfile.mktemp(prefix='g32gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
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
def ready_path(key):
    c = sorted(f for f in os.listdir(NIGHT) if f.startswith('READY_%s' % key) and f.endswith('.diff.md'))
    return (NIGHT + c[0]) if len(c) == 1 else None
GW = 'Blockchain/Dev/services/api-gateway/src/'
VER, PROXY, AUTH, ADMIN = GW + 'routes/verification.ts', GW + 'routes/proxy.ts', GW + 'middleware/auth.ts', GW + 'routes/admin.ts'
SEC, AKTO_T = 'systemTest/akto/src/config/secrets.ts', 'systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts'
TAMPER = {   # the product line each test-only cell's red is driven by — FROM the brief (READ), re-located here by exact whole-line match
 '1304': (VER, "    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';", 585, 'briefs/KS-1227-R15-TEST-ONLY-WITNESS-TRYFINALLY-PIN.md ## Tampers (Line 585 at 581ed7fa1)'),
 '1305': (PROXY, "      if (GATEWAY_VOUCH_SECRET && VOUCH_RECIPIENTS.has(serviceKey)) {", 275, 'briefs/KS-1090.md ## Tamper (line 275 at 581c9db0d)'),
 '1306': (AUTH, "        rateLimitBucket: `api_key:${createHash('sha256').update('secuura-rate-limit-bucket\\0').update(apiKey).digest('hex')}`,", 300, 'briefs/KS-1205.md ## Tamper (line 300 at f8c7aaa39; the seat measured :313 at 94c9c7aa9be7)'),
 '1307': (PROXY, "  const erasureDoorCaseSensitive = Boolean((erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive);", 808, 'briefs/KS-1212.md ## Tamper (line 808 at 581c9db0d)'),
}
def locate(c, p, line):
    L = show(c, p).split('\n'); return [i + 1 for i, l in enumerate(L) if l == line]
PROBES = {}
MEAS = {}
# the comparator's own controls, once (STANDING_LINES 2026-09-27): identical pair IDENTICAL, one token DIFFER, and the empty-string trap caught
_x = ['+a', '-b', '+c']; _y = ['+a', '-b', '+C']
_trap = [l for l in ['+a', ''] if l[:1] in '+-']
CTL_PM = (cmp_seq(pm(_x + ['']), pm(_x)) == 'IDENTICAL' and cmp_seq(pm(_x), pm(_y)) == 'DIFFER' and len(_trap) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, 'CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in \'+-\'` would have counted the empty line (%d vs %d) — the kit uses `l and l[0] in \'+-\'`' % (len(_trap), len(pm(['+a', '']))))
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    tests = [p for p in P[n]['paths'] if p not in prod]
    out.append(('PRODUCT files %s (changed +/- lines %d); TEST files %s' % ([os.path.basename(p) for p in prod], len(pm_diff(cb, h, prod[0])) if len(prod) == 1 else sum(len(pm_diff(cb, h, p)) for p in prod), [os.path.basename(p) for p in tests])) if prod else 'NO product file changed (test-only): every changed path is a test file %s' % [os.path.basename(p) for p in tests])
    key = K['prs'][n]['keys'][0]
    if n in TAMPER:
        tf, tl, tline, tsrc = TAMPER[n]
        hard(not prod, '#%s is TEST-ONLY as declared: no product path in %s' % (n, P[n]['paths']))
        lh, ld, le = locate(h, tf, tl), locate(REAL_DEV, tf, tl), (locate(END, tf, tl) if END else [])
        bl = {'head': blob(h, tf), 'develop': blob(REAL_DEV, tf), 'END': blob(END, tf) if END else None}
        hard(len(lh) == 1 and len(le) == 1, '#%s TAMPER ANCHOR (%s) is byte-unique as a whole line in %s at head %s AND on END_TREE %s (the brief said :%d)' % (n, tsrc, tf.replace(GW, ''), lh, le, tline))
        out.append('TAMPER ANCHOR (READ, whole-line match; %s): `%s` in %s — head %s | develop %s | END_TREE %s | the brief said :%d; blob of %s at head %s, develop %s, END %s (%s)' % (
            tsrc, tl.strip()[:120], tf.replace(GW, ''), lh, ld, le, tline, os.path.basename(tf), (bl['head'] or '-')[:12], (bl['develop'] or '-')[:12], (bl['END'] or '-')[:12],
            'the SAME file at head and on END_TREE' if bl['head'] == bl['END'] else 'the file DIFFERS between head (%s) and END_TREE — the gate runs the tamper at BOTH' % cb[:12]))
    rp = ready_path(key)
    if n in ('1304', '1305', '1306', '1307'):
        if not rp: hard(False, '#%s READY for %s: not exactly one READY_%s*.diff.md in %s' % (n, key, key, NIGHT)); PROBES[n] = out; continue
        rs, rl, glued = ready_block(rp)
        secs = sections('\n'.join(rl))
        rpm = [pm(s[2:]) for s in secs]
        hpm = [pm_diff(cb, h, p) for p in tests]
        rnames = [sec_path(s)[1] for s in secs]
        same = len(rpm) == len(hpm) and all(x == y for x, y in zip(rpm, hpm))
        mut = [list(x) for x in hpm];
        if mut and mut[0]: mut[0][-1] = mut[0][-1] + ' '
        ctl = (cmp_seq(hpm, hpm) == 'IDENTICAL' and cmp_seq(hpm, mut) == 'DIFFER')
        hard(same and ctl, '#%s == its READY (%s, bytes sha256 %s — read once, these bytes compared): the +/- line sequence per file %s vs head %s -> %s; controls (head vs itself IDENTICAL, head vs a one-token mutation DIFFER): %s' % (
            n, os.path.basename(rp), rs[:16], [len(x) for x in rpm], [len(x) for x in hpm], cmp_seq(rpm, hpm), ctl))
        out.append('READY IDENTITY (MEASURED by the drafter, `git diff -U0` merge-base -> head vs the READY block, `l and l[0] in \'+-\'`): %s — READY path(s) %s -> PR path(s) %s%s; %s' % (
            cmp_seq(rpm, hpm), [os.path.basename(x) for x in rnames], [os.path.basename(x) for x in tests], ' (RENAMED at raise)' if [os.path.basename(x) for x in rnames] != [os.path.basename(x) for x in tests] else ' (same name)',
            ('the READY\'s closing fence is GLUED to its last diff line %r (line %d of the block): stripped here as the seat stripped it' % (glued[1], glued[0])) if glued else 'no glued fence'))
        MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'identical': same, 'glued_fence': bool(glued)}
    if n == '1304':
        tt = show(h, tests[0]); t0 = show(cb, tests[0])
        its = lambda s: re.findall(r"^\s*it\('([^']{0,110})", s, re.M)
        out.append('CELLS (READ): merge-base %d `it(` -> head %d; new titles %s; `finally {` in postTier2 at head: %s; `anchorServer.off(\'request\', onAnchorStoreRequest)` inside a finally: %s; R1 stubs ANCHORING_SERVICE_URL with vi.stubEnv + vi.unstubAllEnvs in a finally: %s' % (
            len(its(t0)), len(its(tt)), [x for x in its(tt) if x not in its(t0)], 'finally {' in tt[:tt.find("describe(")] if 'describe(' in tt else '?',
            bool(re.search(r"finally \{\s*anchorServer\.off\('request', onAnchorStoreRequest\)", tt)), bool(re.search(r"vi\.stubEnv\('ANCHORING_SERVICE_URL'[\s\S]{0,400}finally \{\s*vi\.unstubAllEnvs\(\)", tt))))
        vh = show(h, VER).split('\n')
        out.append('THE TAMPERED LINE\'S READER (READ, verification.ts at head): `ANCHORING_SERVICE_URL` occurs at %s; the brief\'s R2 is a CONTROL (no product tamper reaches the try/finally), so the tamper reds EXACTLY R1 — "1 failed / 7 passed of 8" (seat, i1-RED.out)' % [i + 1 for i, l in enumerate(vh) if 'ANCHORING_SERVICE_URL' in l][:6])
    if n == '1305':
        tt = show(h, tests[0])
        out.append('TITLE vs DIFF (READ): the PR title says %r; the ONE file it adds is %s, whose cells pin that the x-gateway-vouch header reaches originate and NO other service key (NAMES %d keys) — the title names the ticket\'s OTHER half (R2-2, tsconfig excludes tests), which this diff does not touch (the PR body says so itself: "the builder\'s filename described the ticket\'s *other* half"). Wednesday\'s addendum keeps the title as the declared subject (lands at 86); the mismatch is put to her (README §6) and the gate rules on it' % (
            AP[n]['title'], os.path.basename(tests[0]), len(re.findall(r"'[a-zA-Z]+'", (re.search(r"const NAMES = \[([^\]]*)\]", tt) or [None, ''])[1]))))
        ph = show(h, PROXY).split('\n')
        out.append('THE VOUCH MINT (READ, proxy.ts at head): `VOUCH_RECIPIENTS` declared %s; `setHeader(\'x-gateway-vouch\'` at %s; `createProxyRoutes` at %s' % (
            [(i + 1, l.strip()[:80]) for i, l in enumerate(ph) if re.search(r'\bVOUCH_RECIPIENTS\b[^=]*=\s*new Set', l)], [i + 1 for i, l in enumerate(ph) if "setHeader('x-gateway-vouch'" in l], [i + 1 for i, l in enumerate(ph) if 'export function createProxyRoutes' in l]))
    if n == '1306':
        paths_all = sorted(set().union(*OWN.values()))
        ab = {'merge-base': blob(cb, AUTH), 'head': blob(h, AUTH), 'develop': blob(REAL_DEV, AUTH), 'END': blob(END, AUTH) if END else None}
        hard(AUTH not in paths_all and ab['merge-base'] == ab['head'] and ab['develop'] == ab['END'],
             '#1306 NO AUTH PRODUCT BYTE CHANGES: middleware/auth.ts is in NO kit PR\'s paths, its blob at #1306\'s merge-base == at #1306\'s head (%s), and on END_TREE == develop\'s (%s)' % ((ab['head'] or '-')[:12], (ab['END'] or '-')[:12]))
        gwp = [p for p in P[n]['paths']]
        out.append('AUTH SURFACE (READ): #1306 paths %s — none under middleware/ or routes/; auth.ts blob merge-base %s / head %s / develop %s / END %s (%s since the merge-base: %s)' % (
            gwp, (ab['merge-base'] or '-')[:12], (ab['head'] or '-')[:12], (ab['develop'] or '-')[:12], (ab['END'] or '-')[:12],
            'UNCHANGED on develop' if ab['merge-base'] == ab['develop'] else 'CHANGED on develop', [l for l in g('log', '--format=%h %s', '%s..%s' % (cb, REAL_DEV), '--', AUTH).splitlines()] or 'no commit'))
        out.append('TITLE vs DIFF (READ): the PR title says %r; the cells pin that an API key\'s limiter bucket is NOT `api_key:` + the BARE sha256 of the key (the stored key_hash) — G-BUCKET-HASH — and read the bucket the real authenticateToken assigns; no cell sends a JWT claim. Wednesday\'s addendum keeps the title as the declared subject (lands at 84); the mismatch is put to her (README §6) and the gate rules on it' % AP[n]['title'])
        ah = show(h, AUTH).split('\n')
        out.append('rateLimitBucket in auth.ts (READ, head): lines %s — the brief said :300 (f8c7aaa39), its note predicted :304 after KS-1207, the seat measured :313 at 94c9c7aa9be7' % [i + 1 for i, l in enumerate(ah) if 'rateLimitBucket' in l])
    if n == '1307':
        ph = show(h, PROXY).split('\n')
        out.append('THE DOOR (READ, proxy.ts at head): `Router(` on lines %s; `erasureDoorCaseSensitive` at %s; the tamper swaps `erasureDoor` for the factory `router` (G-READOUTER); the READY predicts BOTH R1 and R2 red ("2 failed / 4", seat i4-RED.out)' % (
            [i + 1 for i, l in enumerate(ph) if 'Router(' in l], [i + 1 for i, l in enumerate(ph) if 'erasureDoorCaseSensitive' in l]))
    if n == '1308':
        gp = BRIEFS + 'KS-1108/KS-1108.recounted-at-94c9c7aa.diff'
        gb, gs = readbytes(gp); gsecs = sections(gb.decode('utf-8'))
        psec = [s for s in gsecs if sec_path(s)[1] == SEC]; tsec = [s for s in gsecs if sec_path(s)[1] == AKTO_T]
        hard(len(psec) == 1 and len(tsec) == 1, '#1308 golden %s (%d B, sha256 %s, read ONCE): exactly one product section (secrets.ts) and one test section' % (os.path.basename(gp), len(gb), gs[:16]))
        pbytes = ('\n'.join(psec[0]) + '\n').encode('utf-8'); ps = sha256b(pbytes)
        gpm, hpm = pm(psec[0][2:]), pm_diff(cb, h, SEC)
        ab_, am = git_apply_at(cb, pbytes, ps, [SEC], 'ks1108prod')
        prod_exact = gpm == hpm and ab_ is not None and ab_[SEC] == blob(h, SEC)
        hard(prod_exact, '#1308 PRODUCT HUNK byte-identical to the golden\'s product section: +/- lines golden %d vs head %d -> %s; the product section ALONE (%d B, sha256 %s — the bytes split, verified AND applied): %s -> secrets.ts blob %s == head %s' % (
            len(gpm), len(hpm), cmp_seq(gpm, hpm), len(pbytes), ps[:16], am, ((ab_ or {}).get(SEC) or '-')[:12], (blob(h, SEC) or '-')[:12]))
        gtest = [l[1:] for l in tsec[0][2:] if l and l[0] == '+']
        htest = show(h, AKTO_T).split('\n')
        if htest and htest[-1] == '': htest = htest[:-1]
        def classify(a, b):
            sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False); rows = []
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == 'equal': continue
                rem, add = a[i1:i2], b[j1:j2]
                jsdoc = all(re.match(r'^\s*(/\*\*|\*/|\*( |$))', x) for x in rem + add) and rem and all(re.match(r'^\s*/\*\*.*\*/\s*$', x) for x in rem)
                fmt = re.sub(r'\s+', '', ''.join(rem)) == re.sub(r'\s+|,$', '', ''.join(add)).rstrip(',') or re.sub(r'\s+', '', ''.join(rem)) == re.sub(r'\s+', '', ''.join(add))
                fmt2 = re.sub(r'[\s,]+', '', ''.join(rem)) == re.sub(r'[\s,]+', '', ''.join(add))
                rows.append({'old': [i1 + 1, i2], 'new': [j1 + 1, j2], 'removed': len(rem), 'added': len(add), 'kind': 'JSDOC' if jsdoc else ('FORMAT' if (fmt or fmt2) else 'OTHER')})
            return rows
        rows = classify(gtest, htest)
        nj = sum(r['removed'] + r['added'] for r in rows if r['kind'] == 'JSDOC'); nf = sum(r['removed'] + r['added'] for r in rows if r['kind'] == 'FORMAT'); no = sum(r['removed'] + r['added'] for r in rows if r['kind'] == 'OTHER')
        mutated = list(htest); i_code = next(i for i, l in enumerate(mutated) if 'const SENTINEL' in l); mutated[i_code] = mutated[i_code].replace("'ks1108-tag-Pw-4c2e91'", "'ks1108-tag-Pw-4c2e92'")
        crow = classify(gtest, mutated); c_other = sum(r['removed'] + r['added'] for r in crow if r['kind'] == 'OTHER')
        c_same = classify(gtest, gtest)
        ctl108 = c_other > 0 and not c_same
        hard(no == 0 and nj == 12 and nf == 4 and ctl108, '#1308 TEST FILE DEPARTURE from the golden (%d lines) to head (%d lines): JSDOC %d + FORMAT %d + OTHER %d changed lines (the ruled disclosure: 12 JSDoc + 4 formatting, ONLY) — hunks %s; controls: golden vs itself 0 hunks (%s), a ONE-TOKEN code mutation classified OTHER (%d)' % (
            len(gtest), len(htest), nj, nf, no, [(r['old'], r['new'], r['kind']) for r in rows], not c_same, c_other))
        MEAS[n] = {'golden': os.path.basename(gp), 'golden_sha256': gs, 'product_section_sha256': ps, 'product_exact': prod_exact, 'apply': am, 'departure': rows, 'jsdoc': nj, 'format': nf, 'other': no}
        out.append('GOLDEN PRODUCT HUNK (MEASURED by the drafter): %s; the golden\'s hunk header `%s` vs head `%s` (git apply locates by context without fuzz; the header line differs by the offset only)' % (
            'EXACT' if prod_exact else 'NOT EXACT', [l for l in psec[0] if l.startswith('@@')][0][:60], [l for l in g('diff', '-U3', cb, h, '--', SEC).splitlines() if l.startswith('@@')][:1]))
        out.append('RULED DEPARTURE (MEASURED): %d JSDoc lines + %d formatting lines, %d other — matches the seat\'s i5-disclosure.diff (16c16,20 · 26c30,34 · 48c56,58)' % (nj, nf, no))
        LJ = os.path.join(GS, 'aktolint_gate32.json')
        if os.path.exists(LJ):
            lj = json.load(open(LJ)); out.append('AKTO LINT (MEASURED by the drafter, aktolint_gate32.sh -> aktolint_1.out): %s' % lj.get('summary'))
        else: out.append('AKTO LINT: aktolint_gate32.json ABSENT — UNMEASURED by the drafter')
    if n == '1309':
        gp = BRIEFS + 'KS-1196/KS-1196.regenerated-at-94c9c7aa.diff'
        gb, gs = readbytes(gp); gsecs = sections(gb.decode('utf-8'))
        byp = {sec_path(s)[1]: s for s in gsecs}
        T1196 = GW + '__tests__/ks1196-admin-post-api-admin-document-types.test.ts'
        gpm = {p: pm(byp[p][2:]) for p in byp}; hpm = {p: pm_diff(cb, h, p) for p in P[n]['paths']}
        exact = sorted(gpm) == sorted(hpm) and all(gpm[p] == hpm[p] for p in hpm)
        mut = {p: list(v) for p, v in hpm.items()}; mut[ADMIN][-1] = mut[ADMIN][-1].replace('randomUUID', 'randomUUIDx')
        ctl = all(hpm[p] == hpm[p] for p in hpm) and mut[ADMIN] != hpm[ADMIN]
        hard(exact and ctl, '#1309 == the REGENERATED golden %s (%d B, sha256 %s, read once): the +/- line sequence per file %s vs head %s -> %s; controls (head vs itself IDENTICAL; a one-token mutation of the admin.ts `+` line DIFFER): %s' % (
            os.path.basename(gp), len(gb), gs[:16], {os.path.basename(p): len(v) for p, v in gpm.items()}, {os.path.basename(p): len(v) for p, v in hpm.items()}, 'EXACT' if exact else 'NOT EXACT', ctl))
        ab_, am = git_apply_at(cb, gb, gs, P[n]['paths'], 'ks1196')
        out.append('GOLDEN APPLY (MEASURED, `git apply --cached --check` then apply, strict, the WHOLE regenerated diff at the merge-base): %s%s — note its new-file section is headed `%s` / `%s` (not `/dev/null`)' % (
            am, (' -> blobs == head: %s' % all(ab_[p] == blob(h, p) for p in P[n]['paths'])) if ab_ else '', byp[T1196][0][:60] if T1196 in byp else '?', byp[T1196][2][:24] if T1196 in byp else '?'))
        rpth = ready_path(key); rs, rl, glued = ready_block(rpth) if rpth else ('', [], None)
        rsecs = sections('\n'.join(rl)); rpm = {sec_path(s)[1]: pm(s[2:]) for s in rsecs}
        out.append('READY vs REGENERATED (MEASURED): the READY %s (sha256 %s) +/- lines %s vs the regenerated %s -> %s (Wednesday: "its +/- lines are identical to the READY\'s")' % (
            os.path.basename(rpth or '-'), rs[:16], {os.path.basename(p): len(v) for p, v in rpm.items()}, {os.path.basename(p): len(v) for p, v in gpm.items()},
            'IDENTICAL' if rpm == gpm else 'DIFFER (%s)' % [os.path.basename(p) for p in set(rpm) | set(gpm) if rpm.get(p) != gpm.get(p)]))
        adh = show(h, ADMIN); adl = adh.split('\n')
        imps = [(i + 1, l.strip()[:90]) for i, l in enumerate(adl) if re.search(r"^\s*import\b.*\bcrypto\b|require\(['\"](node:)?crypto['\"]\)", l)]
        uses = [(i + 1, l.strip()[:100]) for i, l in enumerate(adl) if re.search(r'\bcrypto\.', l)]
        shadow = [(i + 1, l.strip()[:90]) for i, l in enumerate(adl) if re.search(r'\b(const|let|var|function)\s+crypto\b|\(\s*crypto\s*[,):]', l)]
        tsc = show(h, GW.replace('src/', '') + 'tsconfig.json')
        tdecl = ''
        for f in ('globals.d.ts', 'crypto.d.ts', 'web-globals/crypto.d.ts'):
            fp = CHECKOUT + '/Blockchain/Dev/node_modules/@types/node/' + f
            if os.path.exists(fp) and re.search(r'var crypto\b', open(fp, encoding='utf-8', errors='replace').read()): tdecl += f + ' '
        tver = json.load(open(CHECKOUT + '/Blockchain/Dev/node_modules/@types/node/package.json')).get('version') if os.path.exists(CHECKOUT + '/Blockchain/Dev/node_modules/@types/node/package.json') else 'ABSENT'
        nr = subprocess.run(['node', '-e', "const u = crypto.randomUUID(); process.stdout.write(typeof crypto + ' ' + typeof crypto.randomUUID + ' ' + /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(u) + ' ' + process.version)"], capture_output=True, text=True)
        nc = subprocess.run(['node', '-e', "process.stdout.write(typeof globalThis.cryptoNOPE)"], capture_output=True, text=True)
        MEAS[n] = {'golden': os.path.basename(gp), 'golden_sha256': gs, 'exact': exact, 'apply': am, 'crypto_imports': imps, 'crypto_uses': uses, 'crypto_shadow': shadow,
                   'types_node': tver, 'types_global_decl': tdecl.strip(), 'node_runtime': nr.stdout.strip(), 'node_rc': nr.returncode}
        out.append('CRYPTO IN SCOPE (READ + one node run): admin.ts at head imports crypto %s; `crypto.` used at %s; a local binding named crypto %s; api-gateway tsconfig `lib` %s `types` %s; @types/node %s declares a GLOBAL `var crypto` in [%s]; node (a CommonJS -e script, MEASURED): `%s` rc %d — control: an undefined global reads `%s`' % (
            imps or 'NOWHERE (no import/require)', [u[0] for u in uses], shadow or 'NONE', re.findall(r'"lib"\s*:\s*\[[^\]]*\]', tsc) or 'not set', re.findall(r'"types"\s*:\s*\[[^\]]*\]', tsc) or 'not set',
            tver, tdecl.strip() or 'NONE FOUND', nr.stdout.strip(), nr.returncode, nc.stdout.strip()))
        # SORT-BY-ID (Wednesday: MEASURE it): every reader of document-type ids in api-gateway src and the frontends, at develop, tests excluded
        RX = r'getAllDocumentTypes|getDocumentType\(|document-types|documentTypes?\b|docTypes?\b'
        rc_, o_, _ = gq('grep', '-l', '-I', '-E', RX, REAL_DEV, '--', GW, 'Blockchain/Dev/frontend/')
        files = sorted(x.split(':', 1)[1] for x in o_.strip().splitlines() if x and '__tests__' not in x and '.test.' not in x and '/tests/' not in x) if rc_ == 0 else []
        sorts, idparse = [], []
        for f in files:
            L = show(REAL_DEV, f).split('\n')
            for i, l in enumerate(L):
                if re.search(r'\.sort\(|localeCompare|\bsortBy\b|\borderBy\b|ORDER BY', l):
                    sorts.append('%s:%d: %s' % (f.replace('Blockchain/Dev/', ''), i + 1, l.strip()[:120]))
                if re.search(r'\.id\b[^;]*(\.slice\(|\.substring\(|\.split\(|\.replace\()|(parseInt|Number|new Date)\([^)]*\.id\b|[<>]=?\s*\w+\.id\b\s*[;)?]', l):
                    idparse.append('%s:%d: %s' % (f.replace('Blockchain/Dev/', ''), i + 1, l.strip()[:120]))
        rimpl = show(REAL_DEV, GW + 'services/redis.ts'); ri = rimpl.find('export async function getAllDocumentTypes')
        impl = [l.strip() for l in rimpl[ri:ri + 700].split('\n') if re.search(r'keys\(|Array\.from|\.sort\(', l)]
        CTL_SORT = bool(re.search(r'\.sort\(|localeCompare', "types.sort((a, b) => a.id.localeCompare(b.id))")) and bool(re.search(r'(parseInt|Number|new Date)\([^)]*\.id\b', "new Date(Number(t.id.slice(3)))"))
        sort_id = [s for s in sorts if re.search(r'\bid\b|\.id\b', s)]
        MEAS[n].update({'readers': files, 'sort_lines': sorts, 'sort_lines_naming_id': sort_id, 'id_parse_lines': idparse, 'store_impl': impl})
        out.append('SORT-BY-ID (MEASURED by the drafter: `git grep -l -E %r` at develop %s over api-gateway src + frontend/, tests excluded -> %d reader file(s) %s; then every sort/order line in those files): %d sort/order line(s), of which %d name an id: %s; lines that DERIVE anything from a document-type id (slice/split/parseInt/Number/new Date/compare on `.id`): %s; the store (services/redis.ts getAllDocumentTypes, READ): %s — Redis KEYS order is unspecified and the in-memory Map keeps insertion order, so no list order was ever an id order; control: both patterns fire on planted lines (`types.sort((a, b) => a.id.localeCompare(b.id))`, `new Date(Number(t.id.slice(3)))`): %s' % (
            RX, REAL_DEV[:12], len(files), [f.replace('Blockchain/Dev/', '') for f in files], len(sorts), len(sort_id), sort_id or 'NONE', idparse or 'NONE', impl, CTL_SORT))
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
