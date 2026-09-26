#!/usr/bin/env python3
"""predict_gate28.py — MEASURE one gate28 kit (the directory this script lives in; its PR set, tiers and commit counts are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json carries
NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and the
fetch into the scratch clone must agree with both.

Shape copied from gate27's predict_gate27.py and re-keyed for gate28: THREE rows (#1286 docs fix round, ROUND 2 OF 2 at the cap; #1288
KS-1341 part A, T1; #1289 KS-1318 J2 alone, T2), NO sibling kit (END_TREE_WITH_SIBLING == END_TREE by construction), a PER-PR merge-base
(#1286 on 00de57ba, #1288/#1289 on the current develop e080174c) and a DECLARED COMMIT COUNT per PR (#1286 is TWO commits: round 1 + the
fast-forward fix round). The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight`, read by the PULLS API): hard path-disjoint.
ONE open PR is a DECLARED overlap, not a census row: #1268 (NO GO at its cap, dead-open) carries #1289's one path — kit.json
`dead_open_declared` — at a DIFFERENT blob (gate27's #1268 x #1287 overlap was byte-identical; this one is not): #1289 is hunk 3 of #1268's
three-hunk diff of that file. The overlap is asserted as a HUNK SUBSET (every hunk body of #1289 byte-identical to one of #1268's, #1268 carrying
more), with the pre-image blob unchanged across #1268's merge-base, #1289's merge-base and develop — never absorbed.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g28_sp/clone.git — `git clone --bare --no-local` FROM the checkout (NO
alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never
printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over merge-base(develop, head), with NO merge
commit among them; (1) diff(develop, merged) == EXACTLY the PR's own paths (diff(merge-base, head)), each merged blob byte-equal to the head's blob
(kit.json `declared_overlap` would carry a 3-way target; BOTH gate28 kits declare NONE — measured); (2) numstat(develop -> merged) ==
numstat(merge-base -> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. NOT STACKED: for every pair in the kit (and
across a sibling kit, if any), neither head is an ancestor of the other and their merge-base is an ancestor of develop (no shared non-develop commit).
PAIRWISE the kit's path sets are DISJOINT (hard), disjoint from the SIBLING kit's (hard: the kits may merge in either order), and disjoint from
Seat B 30th's in-flight PRs and worktree(s) (hard: an overlap must be DECLARED by a re-draft, never absorbed). END_TREE = develop + every PR of
the kit, identical in ALL orders (N! orders, memoised on (tree, PR) so equal states are merged once), and END_TREE_WITH_SIBLING = develop + the
sibling kit + this kit, identical whichever kit lands first. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the kit) builds develop + a FOREIGN edit of that PR's first own
file and must REFUSE; --simulate moved builds develop + an UNRELATED synthetic commit (a new file no PR touches) and must PASS (the base-
invariance of a develop move; gate28 cannot use an OLDER develop: #1288 and #1289 sit on the current one). A simulation writes
pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate28.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate28.py <scratchpad> [--simulate …]'); sys.exit(9)
SIM = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--simulate' else 'none'
NS = sorted(K['prs']); SIB = K['sibling_batch']; INF = K['inflight']; DOS = K.get('dead_open_declared', {})
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
CL = os.path.join(SP, 'g28_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate28 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

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
AP = {n: api('pulls/' + n) for n in NS + SIB + INF + sorted(DOS)}
for n in NS: hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == 'develop', '#%s open, not draft, base develop (API)' % n)
for n in INF + sorted(DOS): print('  %s #%s (censused, never pinned; its head may move): state %s head %s branch %s' % ('DEAD-OPEN (declared overlap, hunk subset)' if n in DOS else 'open', n, AP[n]['state'], AP[n]['head']['sha'], AP[n]['head']['ref']))
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
    run(['git', 'clone', '-q', '--bare', '--no-local', CHECKOUT, CL]); run(['git', '--git-dir', CL, 'remote', 'set-url', 'origin', ORIGIN])
hard(not os.path.exists(os.path.join(CL, 'objects', 'info', 'alternates')), 'the scratch clone has NO alternates file (no borrowing from the shared object store)')
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g28/develop']
    + ['+refs/pull/%s/head:refs/g28/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g28/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g28/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g28/pull/' + n).strip() == g('rev-parse', 'refs/g28/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
if SIM == 'moved':
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input='gate28 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n').strip()
    idx = tempfile.mktemp(prefix='g28idx', dir=os.path.join(SP, 'g28_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, 'GATE28-SIMULATED-MOVE.txt')], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', DEV, '-m', 'gate28 SIMULATION moved'], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE28-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    mb0 = g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', mb0, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n# gate28 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g28idx', dir=os.path.join(SP, 'g28_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate28 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION %s: develop := %s (a foreign edit of %s)' % (SIM, DEV, path))
DT = g('rev-parse', DEV + '^{tree}').strip()
print('  develop %s tree %s | %s' % (DEV, DT, g('log', '-1', '--format=%s', DEV).strip()))

print('--- (b) per PR: shape (declared commit count over its merge-base, no merge commit), own paths, BASE-INVARIANT over develop')
P = {}
def blob(c, p):
    rc, o, _ = gq('rev-parse', '%s:%s' % (c, p)); return o.strip() if rc == 0 else None
def numstat(a, b): return sorted(g('diff', '--numstat', a, b).strip().splitlines())
for n in NS:
    h = H[n]; mb = g('merge-base', DEV, h).strip()
    cnt = int(g('rev-list', '--count', '%s..%s' % (mb, h)).strip()); merges = g('rev-list', '--merges', '%s..%s' % (mb, h)).split()
    chain = g('rev-list', '--reverse', '%s..%s' % (mb, h)).split()
    hard(cnt == K['prs'][n]['commits'] and not merges and g('rev-parse', chain[0] + '^').strip() == mb,
         '#%s is %d commit(s) (declared %d) on merge-base %s, no merge commit, the first commit\'s parent == the merge-base' % (n, cnt, K['prs'][n]['commits'], mb[:12]))
    own = sorted(g('diff', '--name-only', mb, h).split())
    move = sorted(g('diff', '--name-only', mb, DEV).split())
    ov = sorted(set(own) & set(move))
    res = {'head': h, 'branch': BR[n], 'merge_base': mb, 'commits': chain, 'paths': own, 'numstat': numstat(mb, h),
           'ahead': int(g('rev-list', '--count', '%s..%s' % (DEV, h)).strip()), 'behind': int(g('rev-list', '--count', '%s..%s' % (h, DEV)).strip()),
           'move_paths': len(move), 'overlap_with_move': ov,
           'msg_keys': sorted(set(re.findall(r'KS-\d+', g('log', '--format=%B', '%s..%s' % (mb, h))))),
           'subjects': [s for s in g('log', '--reverse', '--format=%s', '%s..%s' % (mb, h)).splitlines()]}
    rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + mb, DEV, h)
    hard(rc == 0, '#%s merges CLEAN over develop (merge-tree rc %d)' % (n, rc))
    mt = o.split()[0] if (o and rc == 0) else ''; res['merged_tree'] = mt
    if not mt:
        print('  (#%s: not a clean merge — its blob checks are not reachable; REFUSED above)' % n); P[n] = res; continue
    changed = sorted(g('diff', '--name-only', DEV, mt).split())
    hard(changed == own, '#%s (1) diff(develop, merged) == its own %d path(s) %s' % (n, len(own), own))
    res['merged_blobs'] = {}
    for p in own:
        mbl, hbl = blob(mt, p), blob(h, p)
        hard(mbl == hbl, '#%s (1) merged blob == head blob %s for %s' % (n, (hbl or 'DELETED')[:12], p))
        res['merged_blobs'][p] = {'merged': mbl, 'head': hbl, 'target': 'head blob'}
    hard(numstat(DEV, mt) == res['numstat'], '#%s (2) numstat(develop -> merged) == numstat(merge-base -> head) %s' % (n, res['numstat']))
    modes = g('diff', '--summary', DEV, mt).strip()
    hard('mode change' not in modes, '#%s no mode change (%s)' % (n, modes.replace('\n', ' | ') or 'none'))
    hard(not ov, '#%s (3) develop move since %s ∩ own paths == %s (no declared overlap in this kit)' % (n, mb[:12], ov or 'EMPTY'))
    P[n] = res

print('--- (c) NOT STACKED and PAIRWISE: the kit, the sibling kit (none), every other open PR, and the declared dead-open overlap (hunk subset)')
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g28/pull/' + n).strip()
def paths_of(n):
    h = head_of(n); mb = g('merge-base', REAL_DEV, h).strip(); return set(g('diff', '--name-only', mb, h).split())
OWN = {n: set(P[n]['paths']) for n in NS}
SIBP = {n: paths_of(n) for n in SIB}; INFP = {n: paths_of(n) for n in INF}
for a, b in itertools.combinations(NS + SIB, 2):
    if a not in NS and b not in NS: continue
    ha, hb = head_of(a), head_of(b)
    anc = gq('merge-base', '--is-ancestor', ha, hb)[0] == 0 or gq('merge-base', '--is-ancestor', hb, ha)[0] == 0
    mab = g('merge-base', ha, hb).strip()
    hard(not anc and gq('merge-base', '--is-ancestor', mab, REAL_DEV)[0] == 0, 'NOT STACKED #%s/#%s: neither head is the other\'s ancestor; their merge-base %s is on develop' % (a, b, mab[:12]))
for a, b in itertools.combinations(NS, 2): hard(not (OWN[a] & OWN[b]), 'kit pair #%s/#%s disjoint %s' % (a, b, sorted(OWN[a] & OWN[b]) or ''))
for a in NS:
    for b in SIB: hard(not (OWN[a] & SIBP[b]), '#%s vs sibling-kit #%s disjoint %s' % (a, b, sorted(OWN[a] & SIBP[b]) or ''))
    for b in INF: hard(not (OWN[a] & INFP[b]), '#%s vs open #%s (head %s) disjoint %s' % (a, b, head_of(b)[:12], sorted(OWN[a] & INFP[b]) or ''))
DOSR = {}
import hashlib
def hunks(x, y, pth):
    """the hunk BODIES of diff(x, y) on one path (each hunk's text without its @@ header line: position-free), sha256 each"""
    d = g('diff', '-U3', x, y, '--', pth).splitlines(); out, cur = [], None
    for l in d:
        if l.startswith('@@'):
            if cur is not None: out.append(hashlib.sha256('\n'.join(cur).encode()).hexdigest())
            cur = []; continue
        if cur is not None: cur.append(l)
    if cur is not None: out.append(hashlib.sha256('\n'.join(cur).encode()).hexdigest())
    return out
for b, decl in sorted(DOS.items()):
    hb = head_of(b); pb = paths_of(b); mbb = g('merge-base', REAL_DEV, hb).strip()
    for a in NS:
        ov = sorted(OWN[a] & pb)
        if not ov: continue
        hard(a == decl['pr'] and ov == sorted(decl['paths']), 'DECLARED overlap #%s x dead-open #%s (head %s): measured %s == declared (#%s, %s)' % (a, b, hb[:12], ov, decl['pr'], sorted(decl['paths'])))
        for pth in ov:
            ba, bb = blob(H[a], pth), blob(hb, pth)
            pa, pbb, pd = blob(P[a]['merge_base'], pth), blob(mbb, pth), blob(REAL_DEV, pth)
            hard(pa == pbb == pd and pa is not None, 'DECLARED overlap %s: the PRE-IMAGE is one blob at #%s\'s merge-base %s, #%s\'s merge-base %s and develop (%s %s %s)' % (pth.split('/')[-1], a, P[a]['merge_base'][:12], b, mbb[:12], (pa or '-')[:12], (pbb or '-')[:12], (pd or '-')[:12]))
            ha, hbk = hunks(P[a]['merge_base'], H[a], pth), hunks(mbb, hb, pth)
            idx = [hbk.index(x) + 1 if x in hbk else None for x in ha]
            if decl.get('mode') == 'same_blob':
                hard(ba == bb, 'DECLARED overlap %s: SAME blob %s == %s' % (pth, ba, bb))
            else:
                hard(ba != bb and ha and None not in idx and len(hbk) > len(ha),
                     'DECLARED overlap %s: HUNK SUBSET — #%s carries %d hunk(s), each body byte-identical to #%s\'s hunk(s) %s of %d; the blobs DIFFER (#%s %s, #%s %s), so a merge of #%s after #%s would land its OTHER %d hunk(s)' % (
                         pth.split('/')[-1], a, len(ha), b, idx, len(hbk), a, (ba or '-')[:12], b, (bb or '-')[:12], b, a, len(hbk) - len(ha)))
            DOSR.setdefault(b, []).append({'pr': a, 'path': pth, 'blob_kit': ba, 'blob_dead_open': bb, 'dead_open_head': hb, 'dead_open_merge_base': mbb,
                                           'pre_image': pd, 'kit_hunks': len(ha), 'dead_open_hunks': len(hbk), 'kit_hunk_index_in_dead_open': idx, 'mode': decl.get('mode')})
    undeclared = [pth for pth in decl['paths'] if not any(pth in OWN[a] for a in NS)]
    hard(not undeclared, 'every declared dead-open path is a kit path %s' % (undeclared or ''))
WT = {}
for lab, wt in K['inflight_worktrees'].items():
    if not os.path.isdir(wt): print('  worktree %s ABSENT at %s (REPORTED: nothing to census)' % (lab, wt)); WT[lab] = {'state': 'ABSENT'}; continue
    def rd(*a):
        r = subprocess.run(['git', '--no-optional-locks', '-C', wt] + list(a), capture_output=True, text=True); return r.stdout.strip() if r.returncode == 0 else ''
    wh = rd('rev-parse', 'HEAD'); wb = rd('rev-parse', '--abbrev-ref', 'HEAD'); wmb = rd('merge-base', 'HEAD', 'refs/remotes/origin/develop')
    wp = set(rd('diff', '--name-only', wmb, 'HEAD').split()) if wmb else set()
    dirty = set(l[3:].strip() for l in rd('status', '--porcelain=v1').splitlines() if len(l) > 3)
    WT[lab] = {'head': wh, 'branch': wb, 'merge_base': wmb, 'paths': sorted(wp), 'uncommitted': sorted(dirty)}
    print('  worktree %s: branch %s head %s over %s | committed paths %s | uncommitted %s (READ: rev-parse, merge-base, diff, --no-optional-locks status)' % (lab, wb, wh[:12], wmb[:12], sorted(wp), sorted(dirty) or 'none'))
    for a in NS: hard(not (OWN[a] & (wp | dirty)), '#%s vs %s disjoint %s' % (a, lab, sorted(OWN[a] & (wp | dirty)) or ''))

print('--- (d) END_TREE over develop, ALL orders (memoised); END_TREE_WITH_SIBLING (either kit first)')
MEMO = {}
def step(t, n, heads):
    k = (t, n)
    if k not in MEMO:
        h = heads[n]; mb = g('merge-base', DEV, h).strip()
        rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + mb, t, h)
        MEMO[k] = o.split()[0] if rc == 0 else None
    return MEMO[k]
def seq(base_tree, order, heads):
    t = base_tree
    for n in order:
        t = step(t, n, heads)
        if t is None: return None
    return t
ALLH = dict(H); ALLH.update({n: head_of(n) for n in SIB})
perms = list(itertools.permutations(NS))
ends = {seq(DT, o, ALLH) for o in perms}
hard(len(ends) == 1 and None not in ends, 'END_TREE identical in all %d orders (%d distinct merge-tree calls): %s' % (len(perms), len(MEMO), sorted(x or 'CONFLICT' for x in ends)))
END = ends.pop() if len(ends) == 1 else None
sib_first = seq(DT, SIB, ALLH); sib_first = seq(sib_first, NS, ALLH) if sib_first else None
kit_first = seq(END, SIB, ALLH) if END else None
hard(sib_first is not None and sib_first == kit_first, 'END_TREE_WITH_SIBLING: develop + sibling kit + this kit %s == develop + this kit + sibling kit %s' % (sib_first, kit_first))
st = g('diff', '--shortstat', DT, END).strip() if END else ''
print('  END_TREE %s (%s) | END_TREE_WITH_SIBLING %s' % (END, st, sib_first))

print('--- (e) READ probes (PREDICTIONS for the gate; never evidence)')
def show(c, p):
    rc, o, _ = gq('show', '%s:%s' % (c, p)); return o if rc == 0 else ''
def grepc(c, pat, path):
    rc, o, _ = gq('grep', '-c', '-E', pat, c, '--', path); return sum(int(x.rsplit(':', 1)[1]) for x in o.split()) if rc == 0 else 0
PROBES = {}
for n in NS:
    h = H[n]; mb = P[n]['merge_base']; out = []
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    if prod:
        d = g('diff', '-U0', mb, h, '--', *prod)
        ch = [l[1:] for l in d.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
        nc = [l for l in ch if not re.match(r'^\s*(//|\*|/\*|#)' if any(p.endswith('.sh') for p in prod) else r'^\s*(//|\*|/\*)', l) and l.strip()]
        out.append('product files %s: changed lines %d, NON-comment changed lines %d (a line-prefix READ, NOT an emit)' % ([os.path.basename(p) for p in prod], len(ch), len(nc)))
    else:
        out.append('NO product file: every path is a test / tooling path %s' % [os.path.basename(p) for p in P[n]['paths']])
    if n == '1286':
        D = REAL_DEV; B = 'Blockchain/Dev/'; MT = B + 'docs/MULTI-TENANCY.md'; RP = B + 'docs/RLS-FAIL-CLOSED-PLAN.md'
        r1 = P[n]['commits'][0]
        out.append('FIX ROUND (READ): round 1 %s + fix %s; the fix touches %s; numstat round1 -> head %s' % (
            r1[:12], h[:12], g('diff', '--name-only', r1, h).split(), sorted(g('diff', '--numstat', r1, h).strip().splitlines())))
        cited = [B + x for x in ('services/api-gateway/src/startup-migrations.ts', 'packages/shared/src/db/tenant-pool-manager.ts', 'services/tenant-provisioning/src/index.ts',
                                 'deployment/azure/env.dev.json', 'deployment/azure/env.demo.json', 'deployment/azure/services.bicep', 'migrations/039_rls_fail_closed.sql')]
        mv = g('diff', '--name-only', mb, D, '--', *cited).split()
        out.append('CITES-AT-LAUNCH-DEVELOP (READ): the develop move %s..%s touches %d of the %d cited code/config files %s — the round-1 sentence table reads the same bytes' % (mb[:12], D[:12], len(mv), len(cited), mv or ''))
        fl = gq('grep', '-n', 'PROVISION_PER_TENANT_DB', D)[1].strip().splitlines()
        mtc = gq('grep', '-n', 'MULTI_TENANCY_ENABLED', D, '--', '*.json', '*.bicep')[1].strip().splitlines()
        out.append('FLAG CENSUS at develop %s (READ, `git grep`): PROVISION_PER_TENANT_DB on %d line(s) in %s (no config file); MULTI_TENANCY_ENABLED in .json/.bicep at %s' % (
            D[:12], len(fl), sorted(set(x.split(':')[1] for x in fl)), [':'.join(x.split(':')[1:3]).replace(B, '') for x in mtc]))
        hm, hr = show(h, MT), show(h, RP)
        two = len(re.findall(r'two flags[^.]{0,40}set in \*\*no\*\*', hm + hr))
        out.append('TWO-FLAGS-FIXED (READ): the round-1 wording "two flags … set in **no**" occurs %d time(s) in the two head docs (round 1: %d); `ON in dev and demo` occurs %d time(s); the head docs cite env.dev.json:7 %d, env.demo.json:7 %d, services.bicep:798 %d time(s)' % (
            two, len(re.findall(r'two flags[^.]{0,40}set in \*\*no\*\*', show(r1, MT) + show(r1, RP))), (hm + hr).count('ON in dev and demo'), (hm + hr).count('env.dev.json:7'), (hm + hr).count('env.demo.json:7'), (hm + hr).count('services.bicep:798')))
        tp = show(D, B + 'services/tenant-provisioning/src/index.ts').splitlines()
        tpm = show(D, B + 'packages/shared/src/db/tenant-pool-manager.ts').splitlines()
        ins = [i + 1 for i, l in enumerate(tp) if 'INSERT INTO tenant_config' in l]
        call = [i + 1 for i in range(len(tp)) if i + 1 < len(tp) and 'platformQuery(' in tp[i] and 'INSERT INTO tenant_config' in tp[i + 1]]
        close = [j + 1 for j in range((ins or [0])[0], min(len(tp), (ins or [0])[0] + 6)) if tp[j].strip() == ');'][:1]
        out.append('ONBOARDING-CITE-R2 (READ): the corrected cite is `tenant-provisioning/src/index.ts:245-274, the INSERT at :271`; at develop :245 is `%s`; the `platformQuery(` call opens at %s, the `INSERT INTO tenant_config` text is at %s, the statement closes at %s — so ":271" names the call line, not the INSERT line (off by one), and the range ends one line before the close' % (
            tp[244].strip()[:70] if len(tp) > 244 else '?', call, ins, close))
        out.append('FLAG ROLES (READ, tenant-pool-manager.ts at develop): :151 `%s`; :152 `%s`; MULTI_TENANCY_ENABLED (this.enabled) is read at %s; PROVISION_PER_TENANT_DB (perTenantDbEnabled) at %s — "It enables tenant routing" and "every tenant still routes to the shared database" are graded against :203 and :233' % (
            tpm[150].strip()[:90], tpm[151].strip()[:90], [i + 1 for i, l in enumerate(tpm) if 'this.enabled' in l], [i + 1 for i, l in enumerate(tpm) if 'this.perTenantDbEnabled' in l]))
        az = g('ls-tree', '--name-only', D, B + 'deployment/azure/').split()
        out.append('BICEP-SCOPE (READ): the doc says MULTI_TENANCY_ENABLED is "ON in dev and demo" and cites services.bicep:798; services.bicep is a template deploy.sh applies for any `-e <env>` and .github/workflows/deploy-demo.yml applies for demo; env files in deployment/azure: %s — the gate rules whether "dev and demo" is the whole set' % (
            [os.path.basename(x) for x in az if os.path.basename(x).startswith('env.')]))
        nn = {'N-1286-3 "writes every `tenant_config` row"': len(re.findall(r'writes every `tenant_config` row', hm + hr)),
              'N-1286-4 "the only tenant isolation that exists"': (hm + hr).count('the only tenant isolation that exists'),
              'N-1286-5 RP "not split per-tenant-DB"': hr.count('not split per-tenant-DB'),
              'N-1286-6 "The deliberate exception"': (hm + hr).count('The deliberate exception') + (hm + hr).count('The deliberate escape')}
        out.append('ROUND-1 NON-BLOCKING NOTES still present at head (READ, fixed-string counts; the fix round declared them NOT done): %s' % nn)
        gb = open(os.path.join(GS, 'gh_body_1286.md'), encoding='utf-8').read()
        out.append('PR-BODY-STALE (READ, gh_body_1286.md): the PR BODY still says "dormant behind two flags set in no config file": %s — the round-1 false sentence survives in the body (not in the docs); the squash body is the MANDATED block, never the PR body' % (
            'dormant behind two flags set in no config file' in re.sub(r'\s+', ' ', gb)))
        out.append('head commit message Refs lines: %s (READ; round 1 said `Refs KS1336`, un-hyphenated)' % re.findall(r'(?m)^Refs .*$', g('log', '--format=%B', '%s..%s' % (mb, h))))
    if n == '1288':
        W = 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'; T = 'Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts'
        sd, sh = show(mb, W), show(h, W)
        out.append('LEAK SITES (READ, fixed-string `message: err.message` in webhooks.ts): merge-base %d -> head %d; `fail500(` at head %d (1 declaration + %d calls)' % (
            sd.count('message: err.message'), sh.count('message: err.message'), sh.count('fail500('), sh.count('fail500(res,')))
        def sites(src):
            L = src.splitlines(); res = []
            for i, l in enumerate(L):
                if 'message: err.message' in l:
                    r = [re.search(r"webhooksRouter\.(get|post|put|patch|delete)\('([^']*)'", L[j]) for j in range(i, -1, -1)]
                    r = [x for x in r if x][:1]
                    res.append(('%s %s' % (r[0].group(1).upper(), r[0].group(2)) if r else '?', i + 1, l.strip()))
            return res
        sdl, shl = sites(sd), sites(sh)
        out.append('UNCONVERTED-FIVE (READ): at head %s; the five lines are byte-identical to their merge-base lines: %s (declared scope — parts B and C)' % (
            ['%s :%d' % (r, ln) for r, ln, _ in shl], sorted(t for _, _, t in shl) == sorted(t for r, _, t in sdl if r not in ('GET /', 'POST /'))))
        hl = sh.splitlines(); dl = [i + 1 for i, l in enumerate(hl) if l.startswith('function fail500(')]; cl = [i + 1 for i, l in enumerate(hl) if 'fail500(res,' in l]
        out.append('HELPER-PLACEMENT (READ): `function fail500` declared at line %s of %d (a function DECLARATION — hoisted); its calls at %s (all above it); the last line is `%s`; deliverWebhook declared at %s, first called at %s' % (
            dl, len(hl), cl, hl[-1].strip() if hl else '?', [i + 1 for i, l in enumerate(hl) if re.match(r'^(export )?(async )?function deliverWebhook', l)], [i + 1 for i, l in enumerate(hl) if 'deliverWebhook(' in l and 'function' not in l][:1]))
        out.append('DOCBLOCK-FALSE-AT-A (READ): the docblock opens "%s" — at head %d `message: err.message` 500 lines remain, so "the only place" is FALSE at part A (declared by the PR body)' % (
            [l.strip() for l in hl if 'KS-1341:' in l][:1], sh.count('message: err.message')))
        G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1341/golden/'
        def ho(f):
            r = subprocess.run(['git', 'hash-object', '--no-filters', f], capture_output=True, text=True); return r.stdout.strip() if r.returncode == 0 else 'ABSENT'
        out.append('GOLDEN (READ, `git hash-object` of the brief\'s golden files vs the head blobs): webhooks.A.ts %s vs head %s -> %s; ks1341a test %s vs head %s -> %s; A.golden.diff is a plain unified diff (no `diff --git`/`index` header), so its sha256 is NOT the sha256 of `git diff` output — the identity is at BLOB level' % (
            ho(G + 'webhooks.A.ts')[:12], (blob(h, W) or '-')[:12], 'EXACT' if ho(G + 'webhooks.A.ts') == blob(h, W) else 'DIFFERENT',
            ho(G + 'ks1341a-webhooks-500-never-answers-err-message.test.ts')[:12], (blob(h, T) or '-')[:12], 'EXACT' if ho(G + 'ks1341a-webhooks-500-never-answers-err-message.test.ts') == blob(h, T) else 'DIFFERENT'))
        fam = {}
        for f in ('gdpr.ts', 'systemErrors.ts', 'adminConfig.ts'):
            src = show(REAL_DEV, 'Blockchain/Dev/services/originate/src/routes/' + f)
            m = re.search(r'function fail500\([^)]*\)[^{]*\{([^}]*)\}', src)
            fam[f] = re.sub(r'\s+', ' ', m.group(1)).strip()[:160] if m else ('NO fail500 in originate/src/routes/%s' % f if src else 'FILE ABSENT in originate/src/routes')
        out.append('KS-730 FAMILY (READ, fail500 bodies at develop in originate/src/routes/): %s; #1288\'s body: %s' % (fam, re.sub(r'\s+', ' ', re.search(r'function fail500\([^)]*\)[^{]*\{([^}]*)\}', sh).group(1)).strip()[:160] if 'function fail500(' in sh else 'NONE'))
        pe = show(REAL_DEV, 'Blockchain/Dev/services/originate/src/utils/pgErrors.ts')
        out.append('BENIGN-BRANCH (READ): catch blocks in webhooks.ts that test error TEXT (`.includes(` / `does not exist`) at head: %d / %d; the POST / and GET / catches call only fail500; utils/pgErrors.ts reads err.message: %s (the LEAK fixture carries no SQLSTATE token and no "does not exist")' % (
            len(re.findall(r'catch \(err[^)]*\) \{\s*(?:[^}]*?)\.includes\(', sh)), sh.count('does not exist'), 'message' in pe))
        out.append('GET / TRAP (READ): the list query chains `.catch(... return [])` at line(s) %s, so only a SYNCHRONOUS throw reaches the GET / catch — the cell arms mockImplementationOnce(() => { throw }) (control A0 pins the swallow)' % (
            [i + 1 for i, l in enumerate(hl) if "logger.warn('webhooks list query failed'" in l]))
        ts = show(h, T)
        out.append('TEST FILE (READ): it.each RED cells %d (A1 x2 routes, A2 x2 routes) + controls %d; listens on %s; NODE_ENVS %s' % (
            len(re.findall(r"it\.each\(ROUTES\)\('RED KS-1341", ts)) * 2, len(re.findall(r"^  it\('control KS-1341", ts, re.M)), re.findall(r"app\.listen\(0, '([^']+)'", ts), re.findall(r'const NODE_ENVS = (\[[^\]]*\])', ts)))
    if n == '1289':
        F = 'Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'
        b68 = head_of('1268') if '1268' in DOS else None
        out.append('BLOBS (READ): develop %s | #1289 merge-base %s | #1289 head %s | #1268 head %s | #1268 merge-base %s' % (
            (blob(REAL_DEV, F) or '-')[:12], (blob(mb, F) or '-')[:12], (blob(h, F) or '-')[:12], (blob(b68, F) or '-')[:12] if b68 else 'n/a', (blob(g('merge-base', REAL_DEV, b68).strip(), F) or '-')[:12] if b68 else 'n/a'))
        dd = g('diff', mb, h, '--', F); d68 = g('diff', g('merge-base', REAL_DEV, b68).strip(), b68, '--', F) if b68 else ''
        out.append('KS1316-FREE (READ): hunks #1289 %d vs #1268 %d on this file; KS1316-only token `W9` in #1289\'s diff %d vs #1268\'s %d (the instrument fires); numstat %s' % (
            dd.count('\n@@'), d68.count('\n@@'), dd.count('W9'), d68.count('W9'), g('diff', '--numstat', mb, h, '--', F).strip().split('\t')[:2]))
        sd, shh = show(mb, F), show(h, F); L = shh.splitlines()
        tags = re.findall(r"shapes\.push\('([^']+)'\)", shh) + [re.sub(r'\$\{[^}]*\}', 'Identifier', t) for t in re.findall(r"shapes\.push\(`([^`]+)`\)", shh)]
        m = re.search(r"expect\(defaultShapesOf\(src\)\)\.toEqual\(\[\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*\]\)", shh)
        out.append('J2 ASSERTION (READ): `expect(defaultShapesOf(src)).toHaveLength(3)` merge-base %d -> head %d; the head toEqual list %s; the push labels in defaultShapesOf %s (the template label `export default <${ts.SyntaxKind[...]}>` read as <Identifier> for the `export default f;` fixture line); every asserted tag is a push label: %s' % (
            sd.count('expect(defaultShapesOf(src)).toHaveLength(3)'), shh.count('expect(defaultShapesOf(src)).toHaveLength(3)'), list(m.groups()) if m else 'NOT FOUND', tags, bool(m) and all(t in tags for t in m.groups())))
        out.append('RED-ARM ANCHORS (READ, at head): `return shapes;` occurs %d time(s) at %s (arm A: -> `return shapes.reverse();`); `shapes.push(\'export default function\')` %d, `shapes.push(\'export { x as default }\')` %d (arm B swaps these two labels); the seat\'s arms1318j2.py predicted A: tip 0 red / head 1; B: tip 2 / head 3' % (
            shh.count('return shapes;'), [i + 1 for i, l in enumerate(L) if l.strip() == 'return shapes;'], shh.count("shapes.push('export default function')"), shh.count("shapes.push('export { x as default }')")))
        out.append('KS-1318 DoD (READ, linear_KS-1318.md): ONE checkbox — "the combined cell asserts the set of tags, not the count — e.g. toEqual([...]) against the three expected strings in source order"; this PR is exactly that; Linear link kind `contributes` (linear_reads_1.out) — merged, the ticket does NOT auto-close')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT,
       'end_tree': END, 'end_tree_with_sibling': sib_first, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES,
       'sibling_paths': {n: sorted(SIBP[n]) for n in SIB}, 'sibling_heads': {n: head_of(n) for n in SIB},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': WT, 'dead_open_declared': DOSR}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | END_TREE_WITH_SIBLING %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, sib_first))
sys.exit(1 if FAIL else 0)
