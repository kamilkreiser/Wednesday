#!/usr/bin/env python3
"""predict_gate34.py — MEASURE the gate34 kit (the directory this script lives in; its PR set, tiers, classes, commit counts, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate34's predict (gate32 -> gate31 lineage) and re-keyed for gate34: the rows of Seat B 36th's round, all raised from local-model
READYs under Wednesday's briefs, NONE stacked, every one on develop ec32c40e2b1e — T1: #1316 KS-1346 C (originate routes/adminConfig.ts fail500
type-and-field-names + a NEW ks1346c cell), #1317 KS-1346 D (routes/webhooks.ts, the same line + a NEW ks1346d cell incl. the rotate-secret pin D7),
#1319 KS-908 (security index.ts returns connectorId from POST / GET /api/keys + a NEW ks908 cell), and #1320 KS-692 when it is in kit.json (vc-issuer
routes/status.ts drops ISSUER_ADMIN from STATUS_WRITE_ROLES + a NEW ks692 cell); T2 (spec): #1318 KS-747 (security security.openapi.ts declares
organizationId on GET /api/security/keys + the REGENERATED docs/openapi/secuura-api.yaml + a NEW ks747 cell). Each PR is measured over ITS OWN develop
merge-base and merged over the CURRENT develop (merge-tree with that merge-base). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin
(kit.json `inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles AND
`widen_branch_rx` on branches) is HARD: an open PR matching either outside this kit refuses.

TIER BY CLASS (kit.json `class`): `logging` / `api-response` / `authz` (T1) change EXACTLY ONE product file; `spec` (T2) changes NO runtime file — every
non-test path is the Zod OpenAPI source (`*.openapi.ts`) or the GENERATED docs/openapi/secuura-api.yaml, and the yaml hunk must equal the brief's
companion diff's +/- lines (the seat says it REGENERATED it; the drafter compares the bytes).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths: a merged blob DIFFERENT from the head's) and `noop_paths` (the
squash-stack NO-OP: head == merged == develop) are SEPARATE keys; gate34 declares neither, and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
VERIFIED BYTES == USED BYTES (STANDING_LINES 2026-09-27): every READY / golden / companion is read ONCE into memory, its sha256 printed, and those SAME
bytes are compared and applied (written to a scratch file whose sha256 is re-asserted equal at the point of use).
`git apply --check` (STANDING_LINES 2026-09-27, "`patch -F0` is not `git apply --check`"): every golden is verified with `git apply --cached` in a
scratch index seeded from the merge-base tree (strict: no --recount, no fuzz, no -C) — the tool the seat applies with — never with GNU patch.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate34 / Seat B 36th and is checked by rekey_check_gate34.py (which carries its own name in its own token map).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g34_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into
THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout.
The logging rows' WIDEN measurement is logprobe_gate34.py (run AFTER this script; its JSON is read here when present).

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate34.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate34.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g34_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate34 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g34/develop']
    + ['+refs/pull/%s/head:refs/g34/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g34/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g34/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g34/pull/' + n).strip() == g('rev-parse', 'refs/g34/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g34idx', dir=os.path.join(SP, 'g34_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE34-SIMULATED-MOVE.txt', 'gate34 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate34 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE34-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate34 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate34 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g34/pull/' + n).strip()
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
    W = os.path.join(SP, 'g34_sp'); fp = tempfile.mktemp(prefix='g34apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16])
    idx = tempfile.mktemp(prefix='g34gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
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
# the READY each PR was raised from, NAMED (never globbed: the 09-15 / 09-16 Ornith READYs for KS-747 / KS-908 / KS-692 and the 09-26 / 09-27 KS-1346
# A / B READYs sit in the same directory and are NOT this round's — READ at drafting)
READY = {
 '1316': NIGHT + 'READY_KS-1346-C-ADMINCONFIG-TYPEFIELDS_spark-dsv4flash_BRIEFED-CODEPATCH-TYPE-AND-FIELD-NAMES-ONLY-PASS-7of7_2026-09-28.diff.md',
 '1317': NIGHT + 'READY_KS-1346-D-WEBHOOKS-TYPEFIELDS_spark-dsv4flash_BRIEFED-CODEPATCH-TYPE-AND-FIELD-NAMES-ONLY-PASS-7of7_2026-09-28.diff.md',
 '1318': NIGHT + 'READY_KS-747-KS-747-R2_spark-dsv4flash_BRIEFED-CODEPATCH-KS747-SPEC-ORGID-PASS-7of7_2026-09-28.diff.md',
 '1319': NIGHT + 'READY_KS-908-KS-908-R2_spark-dsv4flash_BRIEFED-CODEPATCH-KS908-CONNECTORID-READBACK-PASS-7of7_2026-09-28.diff.md',
 '1320': NIGHT + 'READY_KS-692-KS-692-R2_spark-dsv4flash_BRIEFED-CODEPATCH-KS692-STATUS-WRITE-PLATFORM-ONLY-PASS-7of7_2026-09-28.diff.md',
}
# the canonical bytes each PR must equal — the brief-writer's golden (== the Spark checker's patch.diff, byte-identical, READ at drafting) — verified with
# `git apply --cached --check`; #1318 is the golden PLUS the brief's openapi-yaml COMPANION (the raising seat adds the regenerated yaml), applied in order
GOLDEN = {
 '1316': [BRIEFS + 'KS-1346-C-adminconfig/KS-1346.golden.diff'],
 '1317': [BRIEFS + 'KS-1346-D-webhooks/KS-1346.golden.diff'],
 '1318': [BRIEFS + 'KS-747/KS-747.golden.diff', BRIEFS + 'KS-747/KS-747.openapi-yaml.companion.diff'],
 '1319': [BRIEFS + 'KS-908/KS-908.golden.diff'],
 '1320': [BRIEFS + 'KS-692/KS-692.golden.diff'],
}
CHECKER = {'1316': 'spark_secuura_2026-09-28_KS-1346-C-adminconfig', '1317': 'spark_secuura_2026-09-28_KS-1346-D-webhooks', '1318': 'spark_secuura_2026-09-28_KS-747-R2',
           '1319': 'spark_secuura_2026-09-28_KS-908-R2', '1320': 'spark_secuura_2026-09-28_KS-692-R2'}
O = 'Blockchain/Dev/services/originate/src/'
SEC = 'Blockchain/Dev/services/security/src/'
VC = 'Blockchain/Dev/services/vc-issuer/src/'
YAML = 'Blockchain/Dev/docs/openapi/secuura-api.yaml'
ADMINCFG, WEBHOOKS, SYSERR, GDPR = O + 'routes/adminConfig.ts', O + 'routes/webhooks.ts', O + 'routes/systemErrors.ts', O + 'routes/gdpr.ts'
SECIDX, SECOAS, STATUS = SEC + 'index.ts', SEC + 'security.openapi.ts', VC + 'routes/status.ts'
F500 = "  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });"
# the line(s) each red arm is planted at — FROM the brief / the PR body (READ), re-located here by exact WHOLE-LINE match at head, develop and END_TREE
TAMPER = {
 '1316': [(ADMINCFG, F500, 104, 'ADD1: the fail500 log line at head (-> `inspect(err)`: the brief predicts C1 x4 AND C6 x4 red, 8 of 15; the seat measured 9 of 15 with C4 too, its tamper also quoting a string throw)')],
 '1317': [(WEBHOOKS, F500, 566, 'ADD1: the fail500 log line at head (-> `inspect(err)`: the brief predicts D1 x3 AND D6 x3 red, 6 of 13; the seat measured 7 of 13 with D4 too)')],
 '1318': [(SECOAS, "  request: { query: z.object({ organizationId: z.string().uuid() }) },", 810, 'the declaration at head (drop it: A1 + A2 red; `.uuid().optional()`: A1 only; `z.string()`: A2 only — the brief\'s arms)')],
 '1319': [(SECIDX, "        connectorId: apiKey.connectorId || null,", 1156, 'Edit 1, the 201 body (drop it: A1 red; feed it from apiKey.name: A1 + C1 red)'),
          (SECIDX, "      connectorId: k.connectorId || null,", 1218, 'Edit 2, the list row (drop it: A2 red; feed it from k.organizationId: A2 + C1 red); the keyHash plant in the 201 body reds C2 only (the seat)')],
 '1320': [(STATUS, "export const STATUS_WRITE_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin'] as const;", 44, 'the narrowed gate at head (re-add \'ISSUER_ADMIN\': A1 + A2 red; add \'ORG_ADMIN\': A1 only — the brief\'s arms)')],
}
def locate(c, p, line):
    if not c: return []
    L = show(c, p).split('\n'); return [i + 1 for i, l in enumerate(L) if l == line]
def its(s): return re.findall(r"^\s*it(?:\.each\([^)]*\))?\(\s*'([^']{0,120})", s, re.M)
PROBES = {}
MEAS = {}
# the comparator's own controls, once (STANDING_LINES 2026-09-27): identical pair IDENTICAL, one token DIFFER, and the empty-string trap caught
_x = ['+a', '-b', '+c']; _y = ['+a', '-b', '+C']
_trap = [l for l in ['+a', ''] if l[:1] in '+-']
CTL_PM = (cmp_seq(pm(_x + ['']), pm(_x)) == 'IDENTICAL' and cmp_seq(pm(_x), pm(_y)) == 'DIFFER' and len(_trap) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, 'CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in \'+-\'` would have counted the empty line (%d vs %d) — the kit uses `l and l[0] in \'+-\'`' % (len(_trap), len(pm(['+a', '']))))
LPJ = os.path.join(GS, 'logprobe_gate34.json'); LP = json.load(open(LPJ)) if os.path.exists(LPJ) else None
def f500_line(c, p):
    L = show(c, p).split('\n'); i = [k for k, l in enumerate(L) if l.startswith('function fail500(')]
    return (L[i[0] + 1].strip(), i[0] + 2) if len(i) == 1 else (None, None)
SPEC_OK = lambda p: p.endswith('.openapi.ts') or p == YAML
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []; cls = K['prs'][n].get('class', '?')
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    tests = [p for p in P[n]['paths'] if p not in prod]
    out.append(('PRODUCT files %s (changed +/- lines %s); TEST files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests])) if prod else 'NO product file changed (test-only): every changed path is a test file %s' % [os.path.basename(p) for p in tests])
    if cls == 'spec':
        hard(K['prs'][n]['tier'] == 'T2' and prod and all(SPEC_OK(p) for p in prod), '#%s is SPEC-ONLY as declared (T2, class spec): every non-test path is an OpenAPI source or the generated yaml %s — no runtime file' % (n, prod))
    else:
        hard(K['prs'][n]['tier'] == 'T1' and len(prod) == 1 and not any(SPEC_OK(p) for p in prod), '#%s (T1, class %s) changes exactly ONE runtime product file: %s' % (n, cls, prod))
    # --- the TAMPER / red-arm anchor(s), whole-line, at head, develop and END_TREE
    for tf, tl, tline, tsrc in TAMPER[n]:
        lh, ld, le = locate(h, tf, tl), locate(REAL_DEV, tf, tl), locate(END, tf, tl)
        bl = {'head': blob(h, tf), 'develop': blob(REAL_DEV, tf), 'END': blob(END, tf) if END else None}
        hard(len(lh) == 1 and len(le) == 1, '#%s RED-ARM ANCHOR (%s) is byte-unique as a whole line in %s at head %s AND on END_TREE %s%s' % (n, tsrc, tf.split('/src/')[1], lh, le, (' (the brief said :%d)' % tline) if tline else ''))
        out.append('RED-ARM ANCHOR (READ, whole-line match; %s): `%s` in %s — head %s | develop %s | END_TREE %s%s; blob of %s at head %s, develop %s, END %s (%s)' % (
            tsrc, tl.strip()[:110], tf.split('/src/')[1], lh, ld, le, (' | the brief said :%d' % tline) if tline else '', os.path.basename(tf), (bl['head'] or '-')[:12], (bl['develop'] or '-')[:12], (bl['END'] or '-')[:12],
            'the SAME file at head and on END_TREE' if bl['head'] == bl['END'] else 'the file DIFFERS between head and END_TREE — the gate plants at BOTH'))
    # --- READY identity: the READY's ```diff block (READ once) vs the head's +/- lines, per file, in order (the files the READY names)
    rp = READY[n]
    if not os.path.exists(rp): hard(False, '#%s READY %s ABSENT' % (n, rp)); PROBES[n] = out; continue
    rs, rl, glued = ready_block(rp)
    secs = sections('\n'.join(rl)); rpm = {os.path.basename(sec_path(s)[1]): pm(s[2:]) for s in secs}
    hpm_all = {os.path.basename(p): pm_diff(cb, h, p) for p in P[n]['paths']}
    hpm = {k: v for k, v in hpm_all.items() if k in rpm}
    outside = sorted(set(hpm_all) - set(rpm))
    same = rpm == hpm
    mut = {k: list(v) for k, v in hpm.items()}; k0 = sorted(mut)[0]; mut[k0][-1] = mut[k0][-1] + ' '
    ctl = (hpm == hpm and mut != hpm)
    rblock = ('\n'.join(rl).rstrip('\n') + '\n').encode('utf-8')
    gsame = sha256b(rblock) == sha256b(open(GOLDEN[n][0], 'rb').read())
    ck = os.path.join(RUNS, CHECKER[n], 'out.md.checker', 'patch.diff')
    csame = os.path.exists(ck) and sha256b(open(ck, 'rb').read()) == sha256b(open(GOLDEN[n][0], 'rb').read())
    hard(same and ctl and outside == ([os.path.basename(YAML)] if n == '1318' else []), '#%s == its READY (%s, bytes sha256 %s — read once, these bytes compared): +/- lines per file %s vs head %s -> %s; head files OUTSIDE the READY %s (the ONLY one allowed is #1318\'s generated yaml); controls (head vs itself IDENTICAL, a one-token mutation DIFFER): %s' % (
        n, os.path.basename(rp)[:70], rs[:16], {k: len(v) for k, v in rpm.items()}, {k: len(v) for k, v in hpm.items()}, cmp_seq(rpm, hpm), outside or 'NONE', ctl))
    out.append('READY IDENTITY (MEASURED, `git diff -U0` merge-base -> head vs the READY block, `l and l[0] in \'+-\'`): %s over %s%s — the READY block\'s bytes == the golden: %s; the Spark checker\'s patch.diff == the golden: %s — %s' % (
        cmp_seq(rpm, hpm), sorted(rpm), (' (outside the READY: %s — checked against the companion below)' % outside) if outside else '', gsame, csame, ('the READY\'s closing fence is GLUED to its last diff line %r: stripped as the seat stripped it' % glued[1]) if glued else 'no glued fence'))
    MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_identical': same, 'ready_bytes_eq_golden': gsame, 'checker_eq_golden': csame, 'glued_fence': bool(glued), 'outside_ready': outside}
    # --- GOLDEN (+ companion): `git apply --cached --check` then apply, STRICT, at the merge-base; the blobs must equal the head's
    gb = b''.join(open(x, 'rb').read() if x == GOLDEN[n][0] else (b'' if open(GOLDEN[n][0], 'rb').read().endswith(b'\n') else b'\n') + open(x, 'rb').read() for x in GOLDEN[n])
    gs = sha256b(gb)
    ab_, am = git_apply_at(cb, gb, gs, P[n]['paths'], 'g%s' % n)
    gexact = ab_ is not None and all(ab_[p] == blob(h, p) for p in P[n]['paths'])
    hard(gexact, '#%s == its canonical bytes %s (%d B, sha256 %s, read once): %s -> every blob == head: %s' % (n, ' + '.join(x.replace(BRIEFS, 'briefs/') for x in GOLDEN[n]), len(gb), gs[:16], am, gexact))
    out.append('GOLDEN APPLY (MEASURED, `git apply --cached --check` then apply, strict, at the merge-base %s; %s): %s -> blobs == head: %s' % (cb[:12], ' + '.join(os.path.basename(x) for x in GOLDEN[n]), am, gexact))
    MEAS[n].update({'golden': GOLDEN[n], 'golden_sha256': gs, 'golden_exact': gexact, 'apply': am})
    # --- cells (READ)
    for t in tests:
        tt = show(h, t)
        out.append('CELLS (READ, %s at head): %d `it(`/`it.each(` entries: %s' % (os.path.basename(t), len(its(tt)), [x[:70] for x in its(tt)]))
    pkg = show(REAL_DEV, P[n]['paths'][0].split('/src/')[0] + '/package.json') if '/services/' in P[n]['paths'][0] else ''
    svc = K['prs'][n]['service']
    pkg = show(REAL_DEV, 'Blockchain/Dev/' + svc + '/package.json')
    out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r; scripts.lint = %r' % (svc, (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1], (re.search(r'"lint"\s*:\s*"([^"]*)"', pkg) or [None, 'ABSENT'])[1]))
    # --- per-class READ probes
    if cls == 'logging':
        f = ADMINCFG if n == '1316' else WEBHOOKS
        fh = show(h, f).split('\n')
        calls = [(i + 1, l.strip()[:120]) for i, l in enumerate(fh) if re.search(r'\blogger\.(error|warn|info|debug)\(|console\.(log|error|warn)\(', l)]
        f5 = [i + 1 for i, l in enumerate(fh) if re.search(r'\bfail500\(res,', l)]
        other_string = [c for c in calls if 'String(err)' in c[1] or 'String(e)' in c[1] or 'String(error)' in c[1]]
        errobj = [c for c in calls if re.search(r'\{\s*(err|error|e)\s*[,}]|error:\s*(err|error|e)\s*[,}]', c[1])]
        out.append('LOG CALLS IN THE TOUCHED FILE (READ, %s at head): %d logger/console calls; fail500 call sites %d (the brief: %s); OTHER log calls still rendering `String(err)`: %s; log calls passing a raw error OBJECT as metadata: %s' % (
            os.path.basename(f), len(calls), len(f5), '50' if n == '1316' else '7', [c[0] for c in other_string] or 'NONE', [c for c in errobj] or 'NONE'))
        lines = {os.path.basename(p): f500_line(END or REAL_DEV, p) for p in (SYSERR, GDPR, ADMINCFG, WEBHOOKS)}
        out.append('THE FOUR LINES (READ, END_TREE): the fail500 log line of systemErrors.ts, gdpr.ts, adminConfig.ts and webhooks.ts identical modulo indentation: %s (lines %s)' % (
            len({v[0] for v in lines.values()}) == 1 and None not in {v[0] for v in lines.values()}, {k: v[1] for k, v in lines.items()}))
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r'^function fail500\(', END or REAL_DEV, '--', 'Blockchain/Dev/services')
        fam = [x.split(':', 2)[1] for x in o_.strip().splitlines() if x]
        famok = {os.path.basename(x): (f500_line(END or REAL_DEV, x)[0] == F500.strip()) for x in fam}
        out.append('THE FAIL500 FAMILY ON END_TREE (MEASURED, `git grep -E "^function fail500\\("` over Blockchain/Dev/services): %d helper(s) %s — each one\'s log line == the ruled line: %s (KS-1346\'s fail500 residue the prior round named as F-3 is CLOSED on END_TREE iff every value is True; the gate says whether that closes KS-1346\'s Definition of done)' % (len(fam), [os.path.basename(x) for x in fam], famok))
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r'logger\.(error|warn|info|debug)\(.*String\((err|error|e)\)', END or REAL_DEV, '--', 'Blockchain/Dev/services/originate/src')
        rest = [x.split(':', 1)[1] for x in o_.strip().splitlines() if x and '__tests__' not in x]
        out.append('OUTSIDE THE FAMILY (MEASURED, `git grep -E "logger\\.(error|warn|info|debug)\\(.*String\\((err|error|e)\\)"` over originate src, tests excluded, END_TREE): %d other log call(s) still render a non-Error through String() — NOT this PR\'s scope (KS-1346 names the fail500 helpers); by file %s' % (
            len(rest), dict(sorted({os.path.basename(x.split(':')[0]): sum(1 for y in rest if y.split(':')[0] == x.split(':')[0]) for x in rest}.items()))))
        if LP and 'END_TREE' in LP:
            out.append('WIDEN — FAIL500 THROUGH THE REAL LOGGER (MEASURED by the drafter, logprobe_gate34.py -> logprobe_1.out: the REAL logger.ts, NODE_ENV=production, the fail500 line of %s at each revision evaluated with it): VALUE probes reaching ANY sink at head %s / END_TREE %s / END_TREE under #1310\'s logger %s; ruled-residue probes reaching a FILE under #1310\'s logger %s; controls %s' % (
                os.path.basename(f), LP.get('_value_hits', {}).get('#%s head' % n), LP.get('_value_hits', {}).get('END_TREE'), LP.get('_value_hits', {}).get('END_TREE + #1310 logger'),
                LP.get('_residue_in_files', {}).get('END_TREE + #1310 logger'), LP.get('_controls')))
            MEAS[n]['logprobe'] = {'value_hits': LP.get('_value_hits'), 'controls': LP.get('_controls')}
        else: out.append('WIDEN — FAIL500 THROUGH THE REAL LOGGER: logprobe_gate34.json ABSENT — UNMEASURED by the drafter')
        if n == '1317':
            wh = show(h, WEBHOOKS).split('\n')
            rot = [i + 1 for i, l in enumerate(wh) if re.search(r"\.(post|put|patch)\(\s*'[^']*rotate-secret", l)]
            ns_ = [i + 1 for i, l in enumerate(wh) if 'newSecret' in l]
            out.append('ROTATE-SECRET (READ, webhooks.ts at head): route at %s; `newSecret` lines %s; D7 is a PIN (green at base and head, the brief), fail-able only by the planted `logger.debug(..., { newSecret })` arm' % (rot, ns_[:12]))
    if cls == 'spec':
        oa = show(h, SECOAS).split('\n')
        reg = [i + 1 for i, l in enumerate(oa) if "path: '/api/security/keys'" in l]
        idx = show(h, SECIDX).split('\n')
        get_ = [i + 1 for i, l in enumerate(idx) if l.startswith("app.get('/api/keys'")]
        req400 = [i + 1 for i, l in enumerate(idx) if "message: 'organizationId required'" in l]
        comp = open(GOLDEN[n][1], 'rb').read().decode('utf-8'); cpm = pm(comp.splitlines())
        ypm = pm_diff(cb, h, YAML)
        out.append('THE YAML (MEASURED): the head\'s `git diff -U0` +/- lines of %s == the brief\'s companion diff\'s: %s (%d vs %d lines, +%d/-%d)' % (
            os.path.basename(YAML), ypm == cpm, len(ypm), len(cpm), sum(1 for l in ypm if l[0] == '+'), sum(1 for l in ypm if l[0] == '-')))
        MEAS[n]['yaml_eq_companion'] = ypm == cpm
        hard(ypm == cpm, '#%s the generated yaml hunk == the brief\'s companion +/- lines (%d lines)' % (n, len(ypm)))
        out.append('THE HANDLER (READ, security index.ts at head): the published path /api/security/keys is registered at security.openapi.ts %s; the service route `app.get(\'/api/keys\'` at %s answers 400 `organizationId required` at %s — the runtime requirement PRE-EXISTS; this PR changes what the contract DECLARES, not what the endpoint enforces (the gate says whether uuid-format is ENFORCED at runtime: READ, the handler only checks presence)' % (reg, get_, req400))
    if cls == 'api-response':
        idx = show(h, SECIDX).split('\n')
        post = [i + 1 for i, l in enumerate(idx) if l.startswith("app.post('/api/keys'")]
        get_ = [i + 1 for i, l in enumerate(idx) if l.startswith("app.get('/api/keys'")]
        g0 = get_[0] if get_ else 0
        seg = idx[g0 - 1:g0 + 60] if g0 else []
        fil = [g0 + i for i, l in enumerate(seg) if '.filter(' in l]; mp = [g0 + i for i, l in enumerate(seg) if '.map(' in l]
        body = [l.strip() for l in idx[post[0]:post[0] + 120] if l.strip().endswith(',') and ':' in l][:0] if post else []
        # the 201 body's and the list row's KEYS (READ): every `name:` inside the two literals
        def lit_keys(start_rx, stop_rx):
            s = [i for i, l in enumerate(idx) if re.search(start_rx, l)]
            if not s: return []
            keys = []
            for l in idx[s[0] + 1:s[0] + 40]:
                if re.search(stop_rx, l): break
                m = re.match(r'^\s*([A-Za-z_]\w*)\s*:', l)
                if m: keys.append(m.group(1))
            return keys
        s201 = [i for i, l in enumerate(idx) if post and i > post[0] and re.search(r"^\s*res\.status\(201\)\.json\(\{", l)]
        d201 = [i for i in range(s201[0], s201[0] + 6) if re.match(r'^\s*data: \{\s*$', idx[i])] if s201 else []
        k201 = []
        for l in (idx[d201[0] + 1:d201[0] + 40] if d201 else []):
            if re.match(r'^\s*\},\s*$', l): break
            m = re.match(r'^\s*([A-Za-z_]\w*)\s*:', l)
            if m: k201.append(m.group(1))
        krow = lit_keys(r"^\s*\.map\(k => \(\{", r'^\s*\}\)\);')
        out.append('THE TWO RESPONSES (READ, security index.ts at head): POST /api/keys at %s, 201 body keys %s; GET /api/keys at %s, list-row keys %s; the tenant filter(s) at %s run BEFORE the map at %s (a caller only ever sees connectorIds of keys its own filter admits); `keyHash` in either literal: %s; the plaintext `key` in the 201 body only (by design, "Only returned once at creation"): %s' % (
            post, k201, get_, krow, fil, mp, 'keyHash' in k201 + krow, 'key' in k201 and 'key' not in krow))
        oa = show(h, SECOAS).split('\n')
        pt = [i + 1 for i, l in enumerate(oa) if '.passthrough()' in l]
        out.append('THE PUBLISHED SCHEMAS (READ, security.openapi.ts at head): `.passthrough()` at %s — connectorId is TOLERATED, not DECLARED (the brief: a KS 794-shaped follow-up); the gate says whether a generated client can see it' % pt[:8])
    if cls == 'authz':
        stx = show(h, STATUS).split('\n'); st0 = show(REAL_DEV, STATUS).split('\n')
        wr = [l.strip() for l in stx if l.startswith('export const STATUS_WRITE_ROLES')]; wr0 = [l.strip() for l in st0 if l.startswith('export const STATUS_WRITE_ROLES')]
        verbs = [(i + 1, l.split('(')[0].strip() + ' ' + (re.search(r"\('([^']*)'", l) or [None, '?'])[1]) for i, l in enumerate(stx) if re.match(r"^router\.(post|put|patch|delete)\(", l)]
        gate = [i + 1 for i, l in enumerate(stx) if "req.method === 'GET'" in l]
        out.append('THE GATE (READ, routes/status.ts): STATUS_WRITE_ROLES develop %s -> head %s; the router-level gate at %s admits every GET/HEAD/OPTIONS and puts EVERY other verb behind STATUS_WRITE_ROLES — the WRITE routes it covers at head: %s. So the NAMED CONSEQUENCE ("tenant ISSUER_ADMINs lose status-list revoke/unrevoke until lists get an owner") is WIDER as READ: an ISSUER_ADMIN also loses POST /api/status (create a list) and POST /:id/allocate — the gate must MEASURE each verb for ISSUER_ADMIN at the merge-base (past the gate) and at head (403) and REPORT it' % (wr0, wr, gate, verbs))
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r"api/status", END or REAL_DEV, '--', 'Blockchain/Dev', ':!*__tests__*', ':!*.md', ':!*.yaml', ':!Blockchain/Dev/docs', ':!*.openapi.ts', ':!Blockchain/Dev/services/vc-issuer/src/routes/status.ts')
        callers = [x.split(':', 1)[1][:170] for x in o_.strip().splitlines() if x]
        out.append('CALLERS (MEASURED, `git grep -E "api/status"` over Blockchain/Dev on END_TREE — tests, docs, yaml, *.openapi.ts and status.ts itself excluded): %d line(s) — the gateway PROXIES /api/status to vc-issuer, so the gate says which caller WRITES with a tenant ISSUER_ADMIN\'s token (a UI action, a connector, an issuance flow that allocates through HTTP) and what it now receives: %s' % (len(callers), callers))
        t586 = [p for p in ('Blockchain/Dev/services/vc-issuer/src/__tests__/ks586-status-write-authorization.test.ts',)]
        e586 = [l.strip()[:150] for l in show(h, t586[0]).split('\n') if 'STATUS_WRITE_ROLES' in l]
        out.append('KS586 (READ, ks586-status-write-authorization.test.ts, NOT in this PR): its STATUS_WRITE_ROLES uses %s — its it.each over the array shrinks by one role at head (the brief: 14 -> 13 cells, all green)' % e586[:6])
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
