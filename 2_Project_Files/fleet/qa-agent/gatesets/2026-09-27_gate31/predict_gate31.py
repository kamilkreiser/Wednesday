#!/usr/bin/env python3
"""predict_gate31.py — MEASURE the gate31 kit (the directory this script lives in; its PR set, tiers, commit counts and the declared STACK are kit.json
beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json
carries NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and
the fetch into the scratch clone must agree with both.

Shape copied from gate30T1's predict_gate30T1.py (itself from gate29) and re-keyed for gate31: FOUR rows, MIXED tiers — #1300 KS-1334 part B (T1,
routes/adminConfig.ts + in-place ks730c edits), #1301 KS-1349 (T2, test-only, STACKED on #1300: its GitHub base is #1300's branch), #1302 KS-1348
(T1, utils/logger.ts: the production File transports get json() — a WIDENING of what reaches LOG STORAGE) and #1303 KS-1350 (T3, the WIDEN row: a
comment-only edit of webhooks.ts's fail500 docblock, graded by CODE-TOKEN EQUIVALENCE). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at
the pin (kit.json `inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx`:
KS-1350) is HARD: an open PR matching it outside this kit refuses.

THE STACK (kit.json `stacks`: child -> parent). A stacked child is measured over its PARENT'S HEAD, never over develop: its declared commit count is
over the parent head (the first commit's parent IS the parent head), its own paths are diff(parent head, child head), its API base.ref is the parent's
branch AND its API base.sha the parent's head, its develop merge-base equals the parent's, and its merged tree is merge-tree over the PARENT'S MERGED
TREE with the parent head as base. The pair is DECLARED stacked (asserted: the parent head is an ancestor of the child head); every other pair must be
NOT stacked. END_TREE is measured in every order in which each parent precedes its child. THE RETARGET PREDICTION: #1300 squash-merged as a new commit
S over develop (a squash never contains the parent head), then #1301 retargeted to develop and merged with GIT'S OWN merge-base (develop, not #1300's
head): the result must equal END over (#1300, #1301), and diff(S, result) must be EXACTLY #1301's own path(s) with the head blob(s).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g31_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates; git never writes through an
alternate), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed).
Nothing is written into the checkout. Node READS the checkout's typescript (#1303 token equivalence, tokeq_gate31.js) — require() only.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its chain base (develop merge-base, or the
parent head), NO merge commit; (1) diff(base side, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2)
numstat(base side -> merged) == numstat(chain base -> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the
kit's path sets are DISJOINT except the declared stack pair (whose overlap must lie inside the child's own paths), and disjoint from every other open
PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate31.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
TSDIR = CHECKOUT + '/Blockchain/Dev/node_modules/typescript'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate31.py <scratchpad> [--simulate …]'); sys.exit(9)
SIM = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--simulate' else 'none'
NS = sorted(K['prs']); SIB = K['sibling_batch']; INF = K['inflight']; DOS = K.get('dead_open_declared', {}); ST = K.get('stacks', {})
FAIL = 0
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def hard(ok, msg):
    global FAIL
    print('  %s %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: FAIL += 1
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0: print('  CMD FAILED rc %d: %s\n%s' % (r.returncode, ' '.join(cmd[:6]), r.stderr[-800:])); sys.exit(1)
    return r.stdout
CL = os.path.join(SP, 'g31_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate31 (%s) %s | simulation %s | scratchpad %s | stacks %s' % (K['kit'], now(), SIM, SP, ST or 'none'))

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
WRX = K.get('widen_rx', r'(?!x)x')
WID = [(str(x['number']), x['head']['sha'], x['title']) for x in OPEN if re.match(WRX, x['title'])]
hard(all(w[0] in NS + SIB for w in WID), 'WIDEN census (open PRs whose title matches %r): %s — every one is in this kit (a WIDEN PR outside it needs a re-draft that adds its cell)' % (WRX, WID or 'NONE'))
AP = {n: api('pulls/' + n) for n in NS + SIB + INF + sorted(DOS)}
for n in NS:
    if n in ST:
        par = ST[n]
        hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == AP[par]['head']['ref'] and AP[n]['base']['sha'] == AP[par]['head']['sha'],
             '#%s open, not draft, STACKED: API base.ref %s == #%s\'s branch %s AND base.sha %s == #%s\'s head' % (n, AP[n]['base']['ref'], par, AP[par]['head']['ref'], AP[n]['base']['sha'][:12], par))
    else:
        hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == 'develop', '#%s open, not draft, base develop (API)' % n)
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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g31/develop']
    + ['+refs/pull/%s/head:refs/g31/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g31/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g31/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g31/pull/' + n).strip() == g('rev-parse', 'refs/g31/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
def synth(parent, path, body, msg):
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body).strip()
    idx = tempfile.mktemp(prefix='g31idx', dir=os.path.join(SP, 'g31_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE31-SIMULATED-MOVE.txt', 'gate31 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate31 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE31-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate31 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate31 SIMULATION ' + SIM)
    print('  SIMULATION %s: develop := %s (a foreign edit of %s)' % (SIM, DEV, path))
DT = g('rev-parse', DEV + '^{tree}').strip()
print('  develop %s tree %s | %s' % (DEV, DT, g('log', '-1', '--format=%s', DEV).strip()))

print('--- (b) per PR: shape (declared commit count over its chain base, no merge commit), own paths, BASE-INVARIANT over develop (a stacked child over its parent)')
P = {}
def blob(c, p):
    rc, o, _ = gq('rev-parse', '%s:%s' % (c, p)); return o.strip() if rc == 0 else None
def numstat(a, b): return sorted(g('diff', '--numstat', a, b).strip().splitlines())
for n in NS:   # sorted: a parent (lower number) is measured before its child
    h = H[n]; dmb = g('merge-base', DEV, h).strip()
    par = ST.get(n)
    cb = H[par] if par else dmb                                    # the CHAIN BASE: the parent head for a stacked child, else the develop merge-base
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
    cmp_base = cb
    res = {'head': h, 'branch': BR[n], 'merge_base': cmp_base, 'develop_merge_base': dmb, 'stacked_on': par, 'commits': chain, 'paths': own, 'numstat': numstat(cb, h),
           'ahead': int(g('rev-list', '--count', '%s..%s' % (cmp_base if par else DEV, h)).strip()), 'behind': int(g('rev-list', '--count', '%s..%s' % (h, cmp_base if par else DEV)).strip()),
           'move_paths': len(move), 'overlap_with_move': ov,
           'msg_keys': sorted(set(re.findall(r'KS-\d+', g('log', '--format=%B', '%s..%s' % (cb, h))))),
           'subjects': [s for s in g('log', '--reverse', '--format=%s', '%s..%s' % (cb, h)).splitlines()]}
    side = P[par]['merged_tree'] if par else DEV                   # the tree the PR lands on: the parent's merged tree for a stacked child
    if par and not side:
        hard(False, '#%s cannot be measured: its parent #%s did not merge clean over develop (REFUSED above)' % (n, par)); res['merged_tree'] = ''; P[n] = res; continue
    rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + cb, side, h)
    hard(rc == 0, '#%s merges CLEAN over %s (merge-tree rc %d)' % (n, ('#%s merged over develop' % par) if par else 'develop', rc))
    mt = o.split()[0] if (o and rc == 0) else ''; res['merged_tree'] = mt
    if not mt:
        print('  (#%s: not a clean merge — its blob checks are not reachable; REFUSED above)' % n); P[n] = res; continue
    changed = sorted(g('diff', '--name-only', side, mt).split())
    hard(changed == own, '#%s (1) diff(%s, merged) == its own %d path(s) %s' % (n, 'parent-merged' if par else 'develop', len(own), own))
    res['merged_blobs'] = {}
    for p in own:
        mbl, hbl = blob(mt, p), blob(h, p)
        hard(mbl == hbl, '#%s (1) merged blob == head blob %s for %s' % (n, (hbl or 'DELETED')[:12], p))
        res['merged_blobs'][p] = {'merged': mbl, 'head': hbl, 'target': 'head blob'}
    hard(numstat(side, mt) == res['numstat'], '#%s (2) numstat(%s -> merged) == numstat(%s -> head) %s' % (n, 'parent-merged' if par else 'develop', 'parent head' if par else 'merge-base', res['numstat']))
    modes = g('diff', '--summary', side, mt).strip()
    hard('mode change' not in modes, '#%s no mode change (%s)' % (n, modes.replace('\n', ' | ') or 'none'))
    hard(not ov, '#%s (3) develop move since %s ∩ own paths == %s (no declared overlap in this kit)' % (n, dmb[:12], ov or 'EMPTY'))
    P[n] = res

print('--- (c) STACKED only where declared, and PAIRWISE: the kit (the declared stack pair excepted), every other open PR')
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g31/pull/' + n).strip()
def paths_of(n):
    h = head_of(n); mb = g('merge-base', REAL_DEV, h).strip(); return set(g('diff', '--name-only', mb, h).split())
OWN = {n: set(P[n]['paths']) for n in NS}
INFP = {n: paths_of(n) for n in INF}
def declared(a, b): return ST.get(b) == a or ST.get(a) == b
for a, b in itertools.combinations(NS, 2):
    ha, hb = head_of(a), head_of(b)
    anc_ab = gq('merge-base', '--is-ancestor', ha, hb)[0] == 0; anc_ba = gq('merge-base', '--is-ancestor', hb, ha)[0] == 0
    mab = g('merge-base', ha, hb).strip()
    if declared(a, b):
        par, ch = (a, b) if ST.get(b) == a else (b, a)
        hard(gq('merge-base', '--is-ancestor', H[par], H[ch])[0] == 0 and P[ch]['commits'] and g('rev-parse', P[ch]['commits'][0] + '^').strip() == H[par],
             'DECLARED STACK #%s on #%s: #%s\'s head is #%s\'s first commit\'s parent' % (ch, par, par, ch))
        ovp = sorted(OWN[a] & OWN[b])
        hard(set(ovp) <= OWN[ch], 'DECLARED STACK #%s/#%s path overlap %s lies inside the child #%s\'s own paths (its merged blob is the child\'s head blob, asserted in (b))' % (a, b, ovp, ch))
    else:
        hard(not anc_ab and not anc_ba and gq('merge-base', '--is-ancestor', mab, REAL_DEV)[0] == 0, 'NOT STACKED #%s/#%s: neither head is the other\'s ancestor; their merge-base %s is on develop' % (a, b, mab[:12]))
        hard(not (OWN[a] & OWN[b]), 'kit pair #%s/#%s disjoint %s' % (a, b, sorted(OWN[a] & OWN[b]) or ''))
for a in NS:
    for b in INF: hard(not (OWN[a] & INFP[b]), '#%s vs open #%s (head %s) disjoint %s' % (a, b, head_of(b)[:12], sorted(OWN[a] & INFP[b]) or ''))

print('--- (d) END_TREE over develop, every order in which each parent precedes its child (memoised); the RETARGET prediction')
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
hard(len(ends) == 1 and None not in ends, 'END_TREE identical in all %d valid orders (of %d; each parent before its child) (%d distinct merge-tree calls): %s' % (len(perms), len(list(itertools.permutations(NS))), len(MEMO), sorted(x or 'CONFLICT' for x in ends)))
END = ends.pop() if len(ends) == 1 else None
st = g('diff', '--shortstat', DT, END).strip() if END else ''
RT = {}
for ch, par in sorted(ST.items()):
    pair = seq(DT, [par, ch])
    tpar = P[par]['merged_tree']
    if not tpar or not P[ch].get('merged_tree'):
        hard(False, 'RETARGET #%s after #%s: not measurable (a merge in the stack is not clean — REFUSED above)' % (ch, par)); RT[ch] = {'parent': par, 'result_tree': None}; continue
    S = run(['git', '--git-dir', CL, 'commit-tree', tpar, '-p', DEV, '-m', 'gate31 SIMULATION: #%s squash-merged' % par], env=dict(os.environ, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    nat = g('merge-base', S, H[ch]).strip()
    rc, o, e = gq('merge-tree', '--write-tree', S, H[ch])
    rtree = o.split()[0] if rc == 0 and o else None
    rdiff = sorted(g('diff', '--name-only', S, rtree).split()) if rtree else None
    rbl = {p: blob(rtree, p) for p in P[ch]['paths']} if rtree else {}
    hard(rtree is not None and rtree == pair and rdiff == P[ch]['paths'] and all(rbl[p] == P[ch]['merged_blobs'][p]['head'] for p in P[ch]['paths']),
         'RETARGET #%s after #%s squashes: #%s squashed as %s over develop (tree %s); git\'s own merge-base for #%s is %s (%s); merge-tree rc %d -> %s == develop+#%s+#%s %s: %s; diff(squash, result) == #%s\'s own paths %s: %s; each blob == #%s\'s head blob: %s' % (
             ch, par, par, S[:12], tpar[:12], ch, nat[:12], 'develop' if nat == DEV else 'NOT develop', rc, rtree, par, ch, pair, rtree == pair, ch, rdiff, rdiff == P[ch]['paths'], ch, all(rbl.get(p) == P[ch]['merged_blobs'][p]['head'] for p in P[ch]['paths'])))
    RT[ch] = {'parent': par, 'squash_sim': S, 'natural_merge_base': nat, 'result_tree': rtree, 'pair_tree': pair, 'own_paths_after_retarget': rdiff, 'blobs': rbl}
print('  END_TREE %s (%s)' % (END, st))

print('--- (e) READ probes (PREDICTIONS for the gate; never evidence, unless the line says the drafter MEASURED it)')
def show(c, p):
    rc, o, _ = gq('show', '%s:%s' % (c, p)); return o if rc == 0 else ''
def ho(f):
    r = subprocess.run(['git', 'hash-object', '--no-filters', f], capture_output=True, text=True); return r.stdout.strip() if r.returncode == 0 else 'ABSENT'
def minus_plus(a, b, pth):
    d = g('diff', '-U0', a, b, '--', pth)
    return [l[1:] for l in d.splitlines() if l.startswith('-') and not l.startswith('---')], [l[1:] for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
def route_of(L, i, rx):
    for j in range(i, -1, -1):
        m = re.search(rx, L[j])
        if m: return '%s %s' % (m.group(1).upper(), m.group(2))
    return '?'
def golden_apply(base, gd, paths):
    """apply a golden diff with `git apply --cached` (strict: no recount, no fuzz) onto <base>'s tree in a scratch index; blob per path, or the refusal"""
    if not os.path.exists(gd): return None, 'golden diff ABSENT (%s)' % gd
    idx = tempfile.mktemp(prefix='g31gold', dir=os.path.join(SP, 'g31_sp')); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=e3)
    ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', gd], capture_output=True, text=True, env=e3)
    if ra.returncode != 0: return None, 'does NOT apply at %s: %s' % (base[:12], ra.stderr.strip()[:160].replace('\n', ' / '))
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
    return {p: blob(t_, p) for p in paths}, 'applies strictly at %s' % base[:12]
def ex(tag): return 'EXACT' if tag else 'DIFFERENT'
BRIEFS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
ADM = 'Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
T730 = 'Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts'
LOGT = 'Blockchain/Dev/services/originate/src/utils/logger.ts'
T1348 = 'Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-log-lines-are-json.test.ts'
WEB = 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'
HELPER_LOG = "  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
PROBES = {}
TOKEQ = {}
for n in NS:
    h = H[n]; cb = H[ST[n]] if n in ST else P[n]['develop_merge_base']; out = []
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    d = g('diff', '-U0', cb, h, '--', *prod) if prod else ''
    ch_ = [l[1:] for l in d.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
    nc = [l for l in ch_ if not re.match(r'^\s*(//|\*|/\*)', l) and l.strip()]
    out.append(('product files %s: changed lines %d, NON-comment-shaped changed lines %d (a line-prefix READ, NOT an emit)' % ([os.path.basename(p) for p in prod], len(ch_), len(nc))) if prod else 'NO product file changed (test-only): every changed path is under __tests__')
    if n == '1300':
        sd, sh = show(cb, ADM), show(h, ADM); dl_, hl = sd.splitlines(), sh.splitlines(); RX = r"adminConfigRouter\.(get|post|put|patch|delete)\('([^']+)'"
        def c4(L): return [(route_of(L, i, RX), i + 1) for i, l in enumerate(L) if re.search(r'message: *err\??\.?message', l)]
        out.append('UNCONDITIONAL SITES (READ, the ks730c C4 regex `message: *err\\??\\.?message` per enclosing route): merge-base %s -> head %s' % (c4(dl_), c4(hl)))
        minus, plus = minus_plus(cb, h, ADM)
        out.append('CONVERTED-TWO (READ, `git diff -U0` on adminConfig.ts): `-` %s | `+` %s' % ([x.strip()[:120] for x in minus], [x.strip()[:120] for x in plus]))
        hc = lambda L: [(re.search(r"fail500\(res, '([^']+)'", l) or [None, None])[1] for l in L if 'fail500(res,' in l]
        out.append('HELPER CALLS (READ): merge-base %d calls / %d distinct -> head %d / %d; `fail500` declared at head line(s) %s; its log line (the tamper anchor) occurs %d time(s) at %s' % (
            len(hc(dl_)), len(set(hc(dl_))), len(hc(hl)), len(set(hc(hl))), [i + 1 for i, l in enumerate(hl) if l.startswith('function fail500(')], sum(1 for l in hl if l == HELPER_LOG), [i + 1 for i, l in enumerate(hl) if l == HELPER_LOG]))
        em = [(i + 1, l.strip()[:110]) for i, l in enumerate(hl) if ('err.message' in l or 'err?.message' in l) and '.includes(' not in l and not l.strip().startswith('*')]
        ng = sum(1 for l in hl if ('err.message' in l or 'err?.message' in l) and '.includes(' in l)
        out.append('ERR.MESSAGE LEFT at head (READ, every line naming err.message / err?.message that is not a `.includes(` guard; %d guard line(s) not listed): %s — KS-1334 also owns a FIFTH site, the per-tenant `err.message?.substring(0, 60)` in a 200 body (no fix-shape ruled; briefs/KS-1334-B/README.md), so part B does NOT close KS-1334' % (ng, em))
        def catch_block(L, pat):
            s = [i for i, l in enumerate(L) if pat in l][:1]
            if not s: return []
            e = s[0]
            while e < len(L) and L[e] != '});': e += 1
            b = L[s[0]:e + 1]; c = [j for j, l in enumerate(b) if 'catch (' in l]
            return [x.strip()[:110] for x in b[c[-1]:]] if c else []
        for pat in ("adminConfigRouter.post('/seed-demo-users'", "adminConfigRouter.post('/migrate-tenant-data'"):
            cbk = catch_block(hl, pat)
            out.append('CATCH BODY at head (READ) for %s: %s — a benign `does not exist` / 42P01 branch in this catch: %s' % (pat.split("'")[1], cbk, any('does not exist' in x for x in cbk)))
        ts0, ts = show(cb, T730), show(h, T730)
        out.append('IN-PLACE ks730c EDITS (READ, `git diff --numstat`): %s; C3 pin %s -> %s; C4 KNOWN at head %s; the new part-B block drives NODE_ENVs %s with `mockLoggerError.mockClear()` inside its loop: %s; `.at(-1)` in the file at head %d (C1, KS-1349\'s subject, #1301)' % (
            g('diff', '--numstat', cb, h, '--', T730).split('\t')[:2], re.findall(r'helperCalls: (\d+), distinctContexts: (\d+) \}\);', ts0), re.findall(r'helperCalls: (\d+), distinctContexts: (\d+) \}\);', ts),
            re.findall(r"const KNOWN(?:: string\[\])? = \[\s*([^\]]*)\]", ts), re.findall(r'const KS1334_NODE_ENVS = (\[[^\]]*\])', ts),
            bool(re.search(r'for \(const nodeEnv of KS1334_NODE_ENVS\) \{\s*mockLoggerError\.mockClear\(\);', ts[ts.find('part B'):] if 'part B' in ts else '')), ts.count('.at(-1)')))
        rows = re.findall(r"RED KS-1334 B1|control KS-1334 B0", ts)
        out.append('PART-B CELLS (READ): `RED KS-1334 B1` it.each block(s) %d, `control KS-1334 B0` it.each block(s) %d, over KS1334B routes %s; the driving seams (READ, brief README): seed-demo-users through its closed demo-seed gate\'s refusal `logger.warn` throwing, migrate-tenant-data through `getPlatformPool()` throwing on the mocked tenant manager — the gate says whether each reaches the OUTER catch and nothing else' % (
            ts.count('RED KS-1334 B1'), ts.count('control KS-1334 B0'), re.findall(r"label: '(POST /[^']+)'", ts[ts.find('KS1334B_ROUTES'):]) [:4]))
        GB = BRIEFS + 'KS-1334-B/golden/'
        ga, gt = ho(GB + 'adminConfig.B.ts'), ho(GB + 'ks730c.B.ts'); gb_, gm = golden_apply(cb, GB + 'KS-1334-B.golden.diff', [ADM, T730])
        out.append('GOLDEN (READ, briefs/KS-1334-B/golden, `git hash-object`): adminConfig.B.ts %s vs head %s -> %s; ks730c.B.ts %s vs head %s -> %s; KS-1334-B.golden.diff at the merge-base: %s%s — the Spark ran on an EXCERPTED input (2 regions of adminConfig.ts, briefs/KS-1334-B/README.md)' % (
            ga[:12], (blob(h, ADM) or '-')[:12], ex(ga == blob(h, ADM)), gt[:12], (blob(h, T730) or '-')[:12], ex(gt == blob(h, T730)), gm,
            (' -> both blobs == head: %s' % (gb_[ADM] == blob(h, ADM) and gb_[T730] == blob(h, T730))) if gb_ else ''))
    if n == '1301':
        minus, plus = minus_plus(cb, h, T730)
        ts = show(h, T730); tsp = show(cb, T730)
        out.append('THE HUNK (READ, `git diff -U0` #1300 head -> #1301 head on ks730c): `-` %s | `+` %s' % ([x.strip()[:120] for x in minus], [x.strip()[:120] for x in plus]))
        c1 = ts[ts.find("RED KS-730 C1"):ts.find("RED KS-730 C2")]
        out.append('C1 AT HEAD (READ): `mockLoggerError.mockClear()` inside the C1 loop: %s; `.at(-1)` in the file: #1300 head %d -> #1301 head %d; C1 NODE_ENVS %s (production row present: %s); C1 is `it.each(ROUTES)` over %d route(s) %s; `beforeEach(() => jest.clearAllMocks())` present: %s (cleared per TEST, not per environment)' % (
            bool(re.search(r'for \(const nodeEnv of NODE_ENVS\) \{\s*(//[^\n]*\n\s*)*mockLoggerError\.mockClear\(\);', c1)), tsp.count('.at(-1)'), ts.count('.at(-1)'),
            re.findall(r"^const NODE_ENVS = (\[[^\]]*\])", ts, re.M), "'production'" in (re.findall(r"^const NODE_ENVS = (\[[^\]]*\])", ts, re.M) or [''])[0],
            len(re.findall(r"^  \{ label: 'GET /", ts, re.M)), re.findall(r"^  \{ label: '(GET /[^']+)'", ts, re.M), 'beforeEach(() => jest.clearAllMocks());' in ts))
        adm_h = show(h, ADM).splitlines()
        out.append('THE TAMPER ANCHOR (READ, adminConfig.ts at #1301 head == #1300 head: %s): fail500\'s log line `%s` occurs %d time(s) at %s. PREDICTION (READ, by construction): the COMMISSION\'s tamper (log only under NODE_ENV=production) does NOT discriminate for C1 — C1\'s NODE_ENVS has no production row, so C1 logs nothing and reds under the OLD `.at(-1)` form too (the brief\'s own measurement, briefs/KS-1349/README.md); the DISCRIMINATING tamper is DEVELOPMENT-only (C1\'s first environment): old form C1 x4 GREEN (blind), fixed form C1 x4 RED' % (
            blob(h, ADM) == blob(cb, ADM), HELPER_LOG.strip(), sum(1 for l in adm_h if l == HELPER_LOG), [i + 1 for i, l in enumerate(adm_h) if l == HELPER_LOG]))
        GB = BRIEFS + 'KS-1349/golden/'
        gb_, gm = golden_apply(cb, GB + 'KS-1349.golden.diff', [T730]); gbd, gmd = golden_apply(P[n]['develop_merge_base'], GB + 'KS-1349.golden.diff', [T730])
        gt = ho(GB + 'ks730c.1349.ts')
        out.append('GOLDEN (READ, briefs/KS-1349/golden): KS-1349.golden.diff at #1300\'s head: %s%s; at develop: %s%s (ks730c.1349.ts %s == that develop-applied blob: %s — the golden FILE was cut at develop; the stacked head carries #1300\'s part-B block too)' % (
            gm, (' -> blob == #1301 head: %s' % (gb_[T730] == blob(h, T730))) if gb_ else '', gmd, (' -> %s' % (gbd[T730] or '-')[:12]) if gbd else '', gt[:12], bool(gbd and gt == gbd[T730])))
        out.append('RETARGET (MEASURED by the drafter over simulated commits, (d)): %s' % ({k: (v['result_tree'], v.get('own_paths_after_retarget'), 'natural merge-base ' + (v.get('natural_merge_base') or '-')[:12]) for k, v in RT.items()} or 'n/a'))
    if n == '1302':
        minus, plus = minus_plus(cb, h, LOGT)
        out.append('PRODUCT DIFF (READ, `git diff -U0` on logger.ts): `-` %s | `+` %s' % ([x.strip()[:150] for x in minus], [x.strip()[:150] for x in plus]))
        lg = show(h, LOGT)
        out.append('LOGGER SHAPE (READ, at head): redaction format of any kind %d (`redact` occurrences); logger-level format %s; Console format in production `combine(json())`: %s; File transports %s; logger level in production %s' % (
            lg.lower().count('redact'), re.findall(r'format: combine\(\s*errors\(\{ stack: true \}\),\s*timestamp', lg) and 'combine(errors({stack:true}), timestamp(...)) — no json(), no printf()', "? combine(json())" in lg,
            re.findall(r"filename: '([^']+)'(?:, level: '(\w+)')?", lg), re.findall(r"level: process\.env\.LOG_LEVEL \|\| \(nodeEnv === 'production' \? '(\w+)'", lg)))
        LP = os.path.join(GS, 'logprobe_gate31.json')
        if os.path.exists(LP):
            lp = json.load(open(LP))
            dv, hv = lp.get('develop (merge-base)', {}), lp.get('#1302 head', {})
            out.append('LOG-FILE WIDENING (MEASURED by the drafter, logprobe_gate31.py -> logprobe_1.out: the REAL logger.ts at each commit, transpiled by the checkout\'s typescript, the checkout\'s winston %s, NODE_ENV=production, one logged metadata object carrying six sentinel fields): develop (logger blob %s) logs/error.log sentinels %s, first line %r; #1302 head (logger blob %s) logs/error.log sentinels %s, logs/combined.log sentinels %s; stdout (Console) carried all six at BOTH commits. So at head a secret/PII-looking field on a logged metadata object (password, token, apiKey, email, subject.ssn, headers.authorization) NOW LANDS IN THE FILE LINE where develop wrote the literal `undefined` — no redaction on the path. Whether the stdout stream is already "log storage" decides whether this is the KS-1346 class (Wednesday\'s call; the gate MEASURES it again)' % (
                '(json)', (dv.get('logger_blob') or '-')[:12], dv.get('files', {}).get('logs/error.log', {}).get('sentinels'), dv.get('files', {}).get('logs/error.log', {}).get('first_line'),
                (hv.get('logger_blob') or '-')[:12], hv.get('files', {}).get('logs/error.log', {}).get('sentinels'), hv.get('files', {}).get('logs/combined.log', {}).get('sentinels')))
        else:
            out.append('LOG-FILE WIDENING: logprobe_gate31.json ABSENT — UNMEASURED by the drafter')
        rcg, gout, _ = gq('grep', '-n', '-I', '-E', r'logger\.(error|warn|info|debug|http|verbose)\(', REAL_DEV, '--', 'Blockchain/Dev/services/originate/src/')
        allc = [x for x in gout.strip().splitlines() if '__tests__' not in x]
        hits = [x for x in allc if re.search(r'(?i)\b(password|passwd|token|secret|apikey|api_key|authorization|email|ssn)\b\s*:', x.split(':', 3)[-1])]
        out.append('CALLERS (READ, `git grep -E` of logger calls at develop over originate src, tests excluded, then a Python key filter; the positive control is the logger-call count itself, %d): %d line(s) whose metadata names a secret/PII-looking KEY %s — a single-line READ; multi-line metadata objects and `err.message` text (the fail500 family logs the thrown text) are NOT seen by it; the gate measures reachability as CONTEXT, never as a mitigation' % (
            len(allc), len(hits), [re.sub(r'^[^:]+:Blockchain/Dev/services/originate/src/', '', x)[:140] for x in hits[:8]]))
        tt = show(h, T1348)
        out.append('TEST FILE (READ): %d lines; `it(` %d; RED titles %s; asserts a secret/PII sentinel ABSENT from the file line: %s (the cell logs %s); isolates the module per NODE_ENV (`jest.isolateModules`): %s; cwd moved to a temp dir: %s' % (
            len(tt.splitlines()), len(re.findall(r"^\s*it\(", tt, re.M)), re.findall(r"it\('(RED [^']{0,60})", tt), bool(re.search(r'(?i)password|token|secret|apikey|ssn', tt)),
            re.findall(r"logger\.error\(([^;]{0,120})\);", tt)[:2], 'isolateModules' in tt, 'chdir' in tt))
        GB = BRIEFS + 'KS-1348/golden/'
        gl, gt = ho(GB + 'logger.fixed.ts'), ho(GB + 'ks1348-production-file-log-lines-are-json.test.ts'); gb_, gm = golden_apply(cb, GB + 'KS-1348.golden.diff', [LOGT, T1348])
        out.append('GOLDEN (READ, briefs/KS-1348/golden): logger.fixed.ts %s vs head %s -> %s; test %s vs head %s -> %s; KS-1348.golden.diff at the merge-base: %s%s — the PR says the golden, not the model\'s own block, is canonical (one trailing context line differs)' % (
            gl[:12], (blob(h, LOGT) or '-')[:12], ex(gl == blob(h, LOGT)), gt[:12], (blob(h, T1348) or '-')[:12], ex(gt == blob(h, T1348)), gm,
            (' -> both blobs == head: %s' % (gb_[LOGT] == blob(h, LOGT) and gb_[T1348] == blob(h, T1348))) if gb_ else ''))
    if n == '1303':
        W = os.path.join(SP, 'g31_sp', 'tokeq_%s' % datetime.datetime.now().strftime('%H%M%S%f')); os.makedirs(W, exist_ok=True)
        sb, sh = show(cb, WEB), show(h, WEB)
        fa, fb = os.path.join(W, 'base.ts'), os.path.join(W, 'head.ts')
        open(fa, 'w').write(sb); open(fb, 'w').write(sh)
        def teq(a, b):
            r = subprocess.run(['node', os.path.join(GS, 'tokeq_gate31.js'), TSDIR, a, b], capture_output=True, text=True); return r.returncode, (r.stdout.strip() or r.stderr.strip()[-200:])
        def mut(src, old, new, name):
            assert src.count(old) >= 1, 'mutation anchor absent: %r' % old
            p = os.path.join(W, name); open(p, 'w').write(src.replace(old, new, 1)); return p
        rc0, o0 = teq(fa, fb)
        ctl = [('C0 identical pair (merge-base vs itself)', teq(fa, fa), 0),
               ('CA one CODE token (`function fail500(` -> `function fail501(`)', teq(fb, mut(sh, 'function fail500(', 'function fail501(', 'ca.ts')), 1),
               ('CB a JSDoc comment edit (`the only place` -> `the ONLY place`)', teq(fb, mut(sh, 'the only place in this router', 'the ONLY place in this router', 'cb.ts')), 0),
               ('CC a string literal (`Internal server error` -> `Internal server ERROR`)', teq(fb, mut(sh, "'Internal server error'", "'Internal server ERROR'", 'cc.ts')), 1),
               ('CD a line comment edit (the first `// ` comment, one word appended)', teq(fb, mut(sh, '// ', '// gate31 ', 'cd.ts')), 0)]
        ctl_ok = all(r[0] == want for _, r, want in ctl)
        TOKEQ = {'base_vs_head': {'rc': rc0, 'out': o0}, 'controls': [{'label': l, 'rc': r[0], 'out': r[1], 'want_rc': w} for l, r, w in ctl], 'controls_ok': ctl_ok}
        out.append('CODE-TOKEN EQUIVALENCE (MEASURED by the drafter, tokeq_gate31.js: the checkout\'s TypeScript PARSER, leaves minus the JSDoc kind range) merge-base vs head webhooks.ts: rc %d | %s' % (rc0, o0))
        out.append('TOKEN-EQUIVALENCE CONTROLS (MEASURED, each must behave: rc 0 = preserves, rc 1 = breaks): %s -> all behaved: %s' % ('; '.join('%s rc %d (want %d)' % (l, r[0], w) for l, r, w in ctl), ctl_ok))
        dd = g('diff', '-U0', cb, h, '--', WEB)
        hunks = [(int(m.group(1)), int(m.group(2)) if m.group(2) is not None else 1) for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+', dd, re.M)]
        rng = [((a, a + c - 1) if c else ('insert after', a)) for a, c in hunks]
        out.append('WINDOW (READ, `git diff -U0` hunk headers, merge-base line numbers): old-side ranges %s; every one inside the declared :549-:561: %s' % (rng, all(549 <= (r[0] if c else a) and (r[1] if c else a) <= 561 for (a, c), r in zip(hunks, rng))))
        hl = sh.splitlines()
        fd = [i for i, l in enumerate(hl) if l.startswith('function fail500(')]
        e = fd[0] if fd else 0
        while fd and e < len(hl) and hl[e] != '}': e += 1
        nxt = next((hl[j] for j in range(e + 1, len(hl)) if hl[j].strip()), None) if fd else None
        above = sum(1 for l in hl[:fd[0]] if 'fail500(res,' in l) if fd else -1
        out.append('THE NEW SENTENCES, READ against the file at head: "Declared after every route, immediately above the default export" — the first non-blank line after fail500\'s closing brace is %r; "All seven route catch blocks above now call it" — `fail500(res,` calls above the declaration: %d; `message: err.message` in the file: %d' % (nxt, above, sh.count('message: err.message')))
        GB = BRIEFS + 'KS-1350/golden/'
        gw = ho(GB + 'webhooks.fixed.ts'); gb_, gm = golden_apply(cb, GB + 'KS-1350.golden.diff', [WEB])
        out.append('GOLDEN (READ, briefs/KS-1350/golden): webhooks.fixed.ts %s vs head %s -> %s; KS-1350.golden.diff at the merge-base: %s%s' % (
            gw[:12], (blob(h, WEB) or '-')[:12], ex(gw == blob(h, WEB)), gm, (' -> blob == head: %s' % (gb_[WEB] == blob(h, WEB))) if gb_ else ''))
        hard(rc0 == 0 and ctl_ok, '#1303 T3 CODE-TOKEN EQUIVALENCE holds at the pin (merge-base vs head IDENTICAL) and all five instrument controls behaved')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT,
       'end_tree': END, 'end_tree_with_sibling': None, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES,
       'stacks': ST, 'retarget': RT, 'tokeq_1303': TOKEQ, 'sibling_paths': {}, 'sibling_heads': {},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': {}, 'dead_open_declared': {}}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | retarget %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, {k: v['result_tree'] for k, v in RT.items()}))
sys.exit(1 if FAIL else 0)
