#!/usr/bin/env python3
"""predict_gate33.py — MEASURE the gate33 kit (the directory this script lives in; its PR set, tiers, commit counts, declared stacks (NONE), declared
overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this script.
Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate32's predict (gate31 -> gate30T1 -> gate29 lineage) and re-keyed for gate33: SIX rows of MIXED tier, all raised by Seat B 35th from
local-model READYs, NONE stacked — T1: #1310 KS-1348 r2 (originate utils/logger.ts redact-then-JSON + a NEW ks1348 cell; replaces the closed #1302),
#1311 KS-1346 A (originate routes/systemErrors.ts fail500 type-and-field-names + a NEW cell; replaces the closed #1296), #1312 KS-1346 B (routes/gdpr.ts,
the same line + a NEW cell; replaces the closed #1297), #1313 KS-1121 (vc-issuer repositories/credentialRepo.ts exact-id-only + its test in place);
T2 (test-only): #1314 KS-1221 (the api-gateway ks744 cells in place) and #1315 KS-1220 (the auth ks839 cells in place). #1310 branches from a24db57e65c9;
the other five from the OLDER 94c9c7aa9be7: each is measured over ITS OWN develop merge-base and merged over the CURRENT develop (merge-tree with that
merge-base). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since, read by the PULLS API
every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles AND `widen_branch_rx` on branches) is HARD: an open PR matching either
outside this kit refuses.

DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths: a merged blob DIFFERENT from the head's) and `noop_paths` (the
squash-stack NO-OP: head == merged == develop) are SEPARATE keys; gate33 declares neither, and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
VERIFIED BYTES == USED BYTES (STANDING_LINES 2026-09-27): every READY / golden / patch.diff is read ONCE into memory, its sha256 printed, and those SAME
bytes are compared and applied (written to a scratch file whose sha256 is re-asserted equal at the point of use).
`git apply --check` (STANDING_LINES 2026-09-27, "`patch -F0` is not `git apply --check`"): every golden is verified with `git apply --cached` in a
scratch index seeded from the merge-base tree (strict: no --recount, no fuzz, no -C) — the tool the seat applies with — never with GNU patch.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate33 / Seat B 35th and is checked by rekey_check_gate33.py (which carries its own name in its own token map).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g33_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into
THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout.
The logging rows' WIDEN measurement is logprobe_gate33.py (run AFTER this script; its JSON is read here when present).

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate33.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate33.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g33_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate33 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g33/develop']
    + ['+refs/pull/%s/head:refs/g33/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g33/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g33/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g33/pull/' + n).strip() == g('rev-parse', 'refs/g33/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g33idx', dir=os.path.join(SP, 'g33_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE33-SIMULATED-MOVE.txt', 'gate33 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate33 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE33-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate33 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate33 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g33/pull/' + n).strip()
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
    W = os.path.join(SP, 'g33_sp'); fp = tempfile.mktemp(prefix='g33apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16])
    idx = tempfile.mktemp(prefix='g33gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
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
# the READY each PR was raised from, NAMED (never globbed: two KS-1220 READYs and three rejected 09-26/27 shapes sit in the same directory — Seat B 35th's
# ready_inventory.txt lists which are live and which MUST NOT be used; READ at drafting)
READY = {
 '1310': NIGHT + 'READY_KS-1348-R2-REDACT_spark-dsv4flash_BRIEFED-CODEPATCH-REDACT-THEN-JSON-PASS-7of7_2026-09-27.diff.md',
 '1311': NIGHT + 'READY_KS-1346-A-R2-TYPEFIELDS_spark-dsv4flash_BRIEFED-CODEPATCH-TYPE-AND-FIELD-NAMES-ONLY-PASS-7of7_2026-09-27.diff.md',
 '1312': NIGHT + 'READY_KS-1346-B-R2-TYPEFIELDS_spark-dsv4flash_BRIEFED-CODEPATCH-TYPE-AND-FIELD-NAMES-ONLY-PASS-7of7_2026-09-27.diff.md',
 '1313': NIGHT + 'READY_KS-1121-EXACTID_spark-dsv4flash_BRIEFED-CODEPATCH-EXACT-ID-ONLY-PASS-7of7_2026-09-27.diff.md',
 '1314': NIGHT + 'READY_KS-1221_ornith35b-q4_TEST-CELLS-FALSY-LEVEL-CLAIM-PASS-7of7_2026-09-17.diff.md',
 '1315': NIGHT + 'READY_KS-1220-R5UNICODECARRIERS_spark-dsv4flash_TESTONLY-INPLACE-PASS-7of7_2026-09-27.diff.md',
}
# the canonical bytes each PR must equal (a golden, a checker's patch.diff, or a coordinator's regeneration) — verified with `git apply --cached --check`
GOLDEN = {
 '1310': BRIEFS + 'KS-1348-r2/KS-1348.golden.diff',
 '1311': BRIEFS + 'KS-1346-A-r2/KS-1346.golden.diff',
 '1312': BRIEFS + 'KS-1346-B-r2/KS-1346.golden.diff',
 '1313': '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1121-r2/out.md.checker/patch.diff',
 '1314': BRIEFS + 'KS-1221/KS-1221.regenerated-at-94c9c7aa.diff',
 '1315': None,   # no golden: the READY block itself is the source (the seat's raise; its +/- identity is measured below)
}
O = 'Blockchain/Dev/services/originate/src/'
GW = 'Blockchain/Dev/services/api-gateway/src/'
AU = 'Blockchain/Dev/services/auth/src/'
VC = 'Blockchain/Dev/services/vc-issuer/src/'
LOGGER, SYSERR, GDPR = O + 'utils/logger.ts', O + 'routes/systemErrors.ts', O + 'routes/gdpr.ts'
REPO, CREDR = VC + 'repositories/credentialRepo.ts', VC + 'routes/credentials.ts'
F500 = "  logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });"
# the line each red arm is planted at — FROM the brief / the PR body (READ), re-located here by exact WHOLE-LINE match at head, develop and END_TREE
TAMPER = {
 '1310': (LOGGER, '    redactSecrets(),', None, 'the logger-level format list at head (drop it: B1 + A3 red; the seat\'s EXTRA arm swaps #1302\'s whole logger blob instead)'),
 '1311': (SYSERR, '    ' + F500.strip(), None, 'ADD1: the fail500 log line at head (-> `inspect(err)`: the four A1 AND the four A6 rows red, 8 of 15)'),
 '1312': (GDPR, F500, None, 'ADD1: the fail500 log line at head (-> `inspect(err)`: the four B1 AND the four B6 rows red, 8 of 15)'),
 '1313': (REPO, '  if (exact) return exact;', None, 'the memory fallback\'s exact return at head (re-insert the deleted includes() scan after it: A and B red)'),
 '1314': (GW + 'middleware/auth.ts', "      if (decoded.verificationLevel) req.headers['x-verification-level'] = decoded.verificationLevel;", 398, 'briefs/KS-1221.md ## Tamper (line 398; the PR body: :407 at 94c9c7aa9be7)'),
 '1315': (AU + 'services/oauth.ts', "  if (allowed.some(entry => parseScopeString(entry).includes('*'))) return []; // KS-839: a wildcard grants nothing, padded or not (' *', 'openid,*' split to '*' on the way to the token)", 353, 'briefs/KS-1220-r2/KS-1220.md ## Tamper (line 353)'),
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
LPJ = os.path.join(GS, 'logprobe_gate33.json'); LP = json.load(open(LPJ)) if os.path.exists(LPJ) else None
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    tests = [p for p in P[n]['paths'] if p not in prod]
    out.append(('PRODUCT files %s (changed +/- lines %s); TEST files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests])) if prod else 'NO product file changed (test-only): every changed path is a test file %s' % [os.path.basename(p) for p in tests])
    if K['prs'][n]['tier'] == 'T2': hard(not prod, '#%s is TEST-ONLY as declared (T2): no product path in %s' % (n, P[n]['paths']))
    else: hard(len(prod) == 1, '#%s (T1) changes exactly ONE product file: %s' % (n, prod))
    # --- the TAMPER / red-arm anchor, whole-line, at head, develop and END_TREE
    tf, tl, tline, tsrc = TAMPER[n]
    lh, ld, le = locate(h, tf, tl), locate(REAL_DEV, tf, tl), locate(END, tf, tl)
    bl = {'head': blob(h, tf), 'develop': blob(REAL_DEV, tf), 'END': blob(END, tf) if END else None}
    hard(len(lh) == 1 and len(le) == 1, '#%s RED-ARM ANCHOR (%s) is byte-unique as a whole line in %s at head %s AND on END_TREE %s%s' % (n, tsrc, tf.split('/src/')[1], lh, le, (' (the brief said :%d)' % tline) if tline else ''))
    out.append('RED-ARM ANCHOR (READ, whole-line match; %s): `%s` in %s — head %s | develop %s | END_TREE %s%s; blob of %s at head %s, develop %s, END %s (%s)' % (
        tsrc, tl.strip()[:110], tf.split('/src/')[1], lh, ld, le, (' | the brief said :%d' % tline) if tline else '', os.path.basename(tf), (bl['head'] or '-')[:12], (bl['develop'] or '-')[:12], (bl['END'] or '-')[:12],
        'the SAME file at head and on END_TREE' if bl['head'] == bl['END'] else 'the file DIFFERS between head and END_TREE — the gate plants at BOTH'))
    # --- READY identity: the READY's ```diff block (READ once) vs the head's +/- lines, per file, in order
    rp = READY[n]
    if not os.path.exists(rp): hard(False, '#%s READY %s ABSENT' % (n, rp)); PROBES[n] = out; continue
    rs, rl, glued = ready_block(rp)
    secs = sections('\n'.join(rl)); rpm = {os.path.basename(sec_path(s)[1]): pm(s[2:]) for s in secs}
    hpm = {os.path.basename(p): pm_diff(cb, h, p) for p in P[n]['paths']}
    same = rpm == hpm
    mut = {k: list(v) for k, v in hpm.items()}; k0 = sorted(mut)[0]; mut[k0][-1] = mut[k0][-1] + ' '
    ctl = (hpm == hpm and mut != hpm)
    # a READY whose +/- lines differ from `git diff`'s only by a REMOVED-and-RE-ADDED identical line (a non-minimal diff: git re-reads the pair as
    # context) is judged by BLOBS instead: its bytes must be the golden's bytes, and the golden must apply strict to the head's blobs (checked below)
    def _nomin(a, b):
        from collections import Counter
        extra = Counter(a) - Counter(b); miss = Counter(b) - Counter(a)
        return not miss and all(extra[x] == extra[('+' if x[0] == '-' else '-') + x[1:]] for x in extra)
    nonmin = (not same) and all(_nomin(rpm.get(k, []), hpm.get(k, [])) for k in set(rpm) | set(hpm))
    rblock = ('\n'.join(rl).rstrip('\n') + '\n').encode('utf-8')
    gsame = bool(GOLDEN[n]) and sha256b(rblock) == sha256b(open(GOLDEN[n], 'rb').read())
    hard((same or (nonmin and gsame)) and ctl, '#%s == its READY (%s, bytes sha256 %s — read once, these bytes compared): +/- lines per file %s vs head %s -> %s%s; controls (head vs itself IDENTICAL, a one-token mutation DIFFER): %s' % (
        n, os.path.basename(rp)[:70], rs[:16], {k: len(v) for k, v in rpm.items()}, {k: len(v) for k, v in hpm.items()}, cmp_seq(rpm, hpm),
        (' — NON-MINIMAL ONLY: every extra line is a removed-and-re-added identical line (git reads the pair as context); the READY block\'s bytes == the canonical %s: %s, so it is judged by BLOBS (GOLDEN APPLY below)' % (os.path.basename(GOLDEN[n] or '-'), gsame)) if not same else '', ctl))
    out.append('READY IDENTITY (MEASURED, `git diff -U0` merge-base -> head vs the READY block, `l and l[0] in \'+-\'`): %s%s — %s' % (cmp_seq(rpm, hpm), (' (NON-MINIMAL: %s; the READY block\'s bytes == %s: %s; judged by blobs)' % ({k: len(rpm.get(k, [])) - len(hpm.get(k, [])) for k in set(rpm) | set(hpm) if rpm.get(k) != hpm.get(k)}, os.path.basename(GOLDEN[n] or '-'), gsame)) if not same else '', ('the READY\'s closing fence is GLUED to its last diff line %r: stripped as the seat stripped it' % glued[1]) if glued else 'no glued fence'))
    MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_identical': same, 'ready_nonminimal_only': nonmin, 'ready_bytes_eq_golden': gsame, 'glued_fence': bool(glued)}
    # --- GOLDEN / canonical bytes: `git apply --cached --check` then apply, STRICT, at the merge-base; the blobs must equal the head's
    gp = GOLDEN[n]
    if gp:
        gb, gs = readbytes(gp)
        ab_, am = git_apply_at(cb, gb, gs, P[n]['paths'], 'g%s' % n)
        gexact = ab_ is not None and all(ab_[p] == blob(h, p) for p in P[n]['paths'])
        hard(gexact, '#%s == its canonical bytes %s (%d B, sha256 %s, read once): %s -> every blob == head: %s' % (n, gp.replace(NIGHT, 'night/'), len(gb), gs[:16], am, gexact))
        out.append('GOLDEN APPLY (MEASURED, `git apply --cached --check` then apply, strict, at the merge-base %s): %s -> blobs == head: %s' % (cb[:12], am, gexact))
        MEAS[n].update({'golden': gp, 'golden_sha256': gs, 'golden_exact': gexact, 'apply': am})
    else:
        out.append('GOLDEN: NONE for this row (the READY block is the source; its +/- identity above is the check)')
    # --- per-row READ probes
    if n in ('1314', '1315'):
        tt, t0 = show(h, tests[0]), show(cb, tests[0])
        ec = re.findall(r'^const EXPECTED_CELLS = (\d+);', tt, re.M); ec0 = re.findall(r'^const EXPECTED_CELLS = (\d+);', t0, re.M)
        new = [x for x in its(tt) if x not in its(t0)]
        out.append('CELLS (READ): merge-base %d `it(` -> head %d; EXPECTED_CELLS %s -> %s; new titles %s' % (len(its(t0)), len(its(tt)), ec0, ec, new))
        pkg = show(REAL_DEV, tf.split('/src/')[0] + '/package.json')
        out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r' % (tf.split('/src/')[0].split('/')[-1], (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1]))
        if n == '1315':
            add = [l for l in pm_diff(cb, h, tests[0]) if l.startswith('+')]
            nonascii = [l[:60] for l in add if any(ord(c) > 127 for c in l)]
            out.append('ASCII (READ): %d added line(s), %d carry a non-ASCII byte %s — the PR body says every carrier is built with String.fromCharCode; fromCharCode codes in the diff: %s' % (
                len(add), len(nonascii), nonascii or '', sorted(set(re.findall(r'fromCharCode\((0x[0-9a-fA-F]+|\d+)\)', '\n'.join(add))))))
    if n == '1310':
        lh_ = show(h, LOGGER)
        rx = re.findall(r'^const SENSITIVE_LOG_KEY = (/.*/i);', lh_, re.M)
        comb = re.search(r'format: combine\(([\s\S]*?)\),\n  transports', lh_[lh_.find('winston.createLogger('):])
        files_json = len(re.findall(r"new winston\.transports\.File\(\{[^}]*format: combine\(json\(\)\)", lh_))
        errpass = 'value instanceof Error' in lh_
        out.append('LOGGER SHAPE (READ, head): SENSITIVE_LOG_KEY %s (suffix-anchored `$`, case-insensitive); the logger-level combine(...) is %s — redactSecrets() LAST: %s; File transports with format combine(json()) %d of 2; `value instanceof Error` returns the value UNWALKED: %s; `message` and `level` are never redacted: %s' % (
            rx, [x.strip() for x in comb.group(1).split('\n') if x.strip()] if comb else '?', bool(comb and comb.group(1).strip().rstrip(',').endswith('redactSecrets()')), files_json, errpass, "key !== 'level' && key !== 'message'" in lh_))
        if LP and all(k in LP for k in ('develop (the pin)', '#1310 head', 'END_TREE')):
            H0, E0 = LP['#1310 head'], LP['END_TREE']
            out.append('WIDEN — PRODUCTION LOG FILES (MEASURED by the drafter, logprobe_gate33.py -> logprobe_1.out: the REAL logger.ts at each revision, the checkout\'s typescript + winston, NODE_ENV=production, eight probes each with its own sentinels): P1 (the six ruled top-level keys) in the files at #1310 head %s; sentinels that reach a FILE at #1310 head and did NOT at develop %s; at END_TREE %s; controls %s' % (
                {f: H0['hits'][f]['P1'] for f in ('logs/error.log', 'logs/combined.log')}, H0.get('new_in_files_vs_develop'), E0.get('new_in_files_vs_develop'), LP.get('_controls')))
            MEAS[n]['logprobe'] = {'head_new': H0.get('new_in_files_vs_develop'), 'end_new': E0.get('new_in_files_vs_develop'), 'controls': LP.get('_controls')}
        else: out.append('WIDEN — PRODUCTION LOG FILES: logprobe_gate33.json ABSENT — UNMEASURED by the drafter')
        c02 = gq('rev-parse', '--verify', '-q', 'refs/g33/closed/1302:' + LOGGER)
        out.append('#1302 (CLOSED predecessor; the seat\'s EXTRA arm swaps its logger blob in): refs/g33/closed/1302 logger.ts blob %s (fetched by logprobe_gate33.py; READ)' % ((c02[1].strip()[:12]) if c02[0] == 0 else 'NOT FETCHED'))
    if n in ('1311', '1312'):
        f = SYSERR if n == '1311' else GDPR
        fh = show(h, f).split('\n')
        calls = [(i + 1, l.strip()[:150]) for i, l in enumerate(fh) if re.search(r'\blogger\.(error|warn|info|debug)\(|console\.(log|error|warn)\(', l)]
        f5 = [i + 1 for i, l in enumerate(fh) if 'fail500(res,' in l]
        other_string = [c for c in calls if 'String(err)' in c[1]]
        out.append('LOG CALLS IN THE TOUCHED FILE (READ, %s at head): %s; fail500 call sites %d; OTHER catch paths still logging `String(err)` for a non-Error: %s' % (os.path.basename(f), calls, len(f5), [c[0] for c in other_string] or 'NONE'))
        out.append('THE TWO LINES (READ): systemErrors.ts fail500 line on END_TREE == gdpr.ts fail500 line on END_TREE modulo indentation: %s' % (
            bool(END) and [l.strip() for l in show(END, SYSERR).split('\n') if l.strip().startswith('logger.error(context,')] == [l.strip() for l in show(END, GDPR).split('\n') if l.strip().startswith('logger.error(context,')]))
        out.append('WIDEN (READ, by construction of the ruled line): an Error logs its MESSAGE (unchanged, by the ruling); a plain object logs its constructor name and Object.keys() — so a thrown object whose KEYS are data (an email-keyed map) puts those keys in the line; a null-prototype object logs `object`; a Proxy whose ownKeys trap throws makes fail500 itself throw before res.status(500) (READ, not run). With #1310 merged the `error` key is NOT redacted (its name matches no SENSITIVE_LOG_KEY suffix), so the line reaches the files verbatim — logprobe P6/P7 measures it: %s' % (
            ({k: (LP['END_TREE']['hits'][k]['P6'] if n == '1311' else LP['END_TREE']['hits'][k]['P7']) for k in ('logs/error.log', 'logs/combined.log', 'stdout')}) if LP and 'END_TREE' in LP else 'logprobe ABSENT'))
    if n == '1313':
        rr = show(h, REPO).split('\n'); cr = show(h, CREDR).split('\n')
        out.append('THE ROUTE (READ, routes/credentials.ts at head): GET /:id -> credentialRepo.getById at %s (404 `Credential not found` on undefined: %s); POST /:id/revoke -> credentialRepo.revoke at %s; revoke() resolves through getById at %s' % (
            [i + 1 for i, l in enumerate(cr) if 'credentialRepo.getById(' in l], any("AppError('Credential not found', 404)" in l for l in cr), [i + 1 for i, l in enumerate(cr) if 'credentialRepo.revoke(' in l],
            [i + 1 for i, l in enumerate(rr) if 'const credential = await getById(id);' in l]))
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r' LIKE |\.includes\(id\)|value\.id\.includes', END or REAL_DEV, '--', VC)
        hits_ = [x.split(':', 1)[1] for x in o_.strip().splitlines() if x and '__tests__' not in x]
        out.append('THE CLASS ON END_TREE (MEASURED, `git grep -E " LIKE |\\.includes\\(id\\)|value\\.id\\.includes"` over vc-issuer src, tests excluded): %s' % (hits_ or 'NONE'))
        out.append('DISCLOSED (READ, head): `let result` at %s is now assigned once (prefer-const, the seat: 0 -> 1 warning); the TS2339 `revoked` read in the new revoke cell at %s (the seat: +1 of the pre-existing class; follow-up KS-1351; Wednesday ruled raise-as-is)' % (
            [i + 1 for i, l in enumerate(rr) if re.search(r'^\s*let result = await query', l)], [i + 1 for i, l in enumerate(show(h, tests[0]).split('\n')) if 'credentialStatus?.revoked' in l]))
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
