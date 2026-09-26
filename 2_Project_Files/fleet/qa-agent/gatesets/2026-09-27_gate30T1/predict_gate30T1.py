#!/usr/bin/env python3
"""predict_gate30T1.py — MEASURE one gate30T1 kit (the directory this script lives in; its PR set, tiers and commit counts are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json carries
NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and the
fetch into the scratch clone must agree with both.

Shape copied from gate29's predict_gate29.py (the kit that worked on 2026-09-26) and re-keyed for gate30T1: FOUR rows, all T1 (#1292 KS-1341 part C
on services/originate routes/webhooks.ts; #1294 KS-1334 part A on routes/adminConfig.ts + in-place ks730c edits; #1296 KS-1346 part A on
routes/systemErrors.ts and #1297 KS-1346 part B on routes/gdpr.ts, the two WIDEN rows), a SIBLING kit gate30T2 (#1293, #1295 — END_TREE_WITH_SIBLING is measured both ways), a PER-PR merge-base
and a DECLARED COMMIT COUNT per PR (one each). The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since,
read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx`) is HARD: an open PR matching it outside this kit and its
sibling refuses. No dead-open overlap is declared (kit.json `dead_open_declared` is empty; the machinery asserts nothing when empty).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g30T1_sp/clone.git — `git clone --bare --no-local` FROM the checkout (NO
alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never
printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over merge-base(develop, head), with NO merge
commit among them; (1) diff(develop, merged) == EXACTLY the PR's own paths (diff(merge-base, head)), each merged blob byte-equal to the head's blob
(kit.json `declared_overlap` would carry a 3-way target; BOTH gate30 kits declare NONE — measured); (2) numstat(develop -> merged) ==
numstat(merge-base -> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. NOT STACKED: for every pair in the kit (and
across a sibling kit, if any), neither head is an ancestor of the other and their merge-base is an ancestor of develop (no shared non-develop commit).
PAIRWISE the kit's path sets are DISJOINT (hard), disjoint from the SIBLING kit's (hard: the kits may merge in either order), and disjoint from
every other open PR and any declared worktree (hard: an overlap must be DECLARED by a re-draft, never absorbed). END_TREE = develop + every PR of
the kit, identical in ALL orders (N! orders, memoised on (tree, PR) so equal states are merged once), and END_TREE_WITH_SIBLING = develop + the
sibling kit + this kit, identical whichever kit lands first. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the kit) builds develop + a FOREIGN edit of that PR's first own
file and must REFUSE; --simulate moved builds develop + an UNRELATED synthetic commit (a new file no PR touches) and must PASS (the base-
invariance of a develop move; gate30T1 cannot use an OLDER develop: #1292 needs part B, #1290, on the current one). A simulation writes
pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate30T1.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate30T1.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g30T1_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate30T1 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

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
hard(all(w[0] in NS + SIB for w in WID), 'WIDEN census (open PRs whose title matches %r): %s — every one is in this kit or its sibling (a WIDEN PR outside both needs a re-draft that adds its cell)' % (WRX, WID or 'NONE'))
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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g30T1/develop']
    + ['+refs/pull/%s/head:refs/g30T1/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g30T1/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g30T1/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g30T1/pull/' + n).strip() == g('rev-parse', 'refs/g30T1/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
if SIM == 'moved':
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input='gate30T1 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n').strip()
    idx = tempfile.mktemp(prefix='g30T1idx', dir=os.path.join(SP, 'g30T1_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, 'GATE30T1-SIMULATED-MOVE.txt')], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', DEV, '-m', 'gate30T1 SIMULATION moved'], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE30T1-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    mb0 = g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', mb0, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n# gate30T1 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g30T1idx', dir=os.path.join(SP, 'g30T1_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate30T1 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
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

print('--- (c) NOT STACKED and PAIRWISE: the kit, the sibling kit (%s), every other open PR, and the declared dead-open overlap (hunk subset)' % (K['sibling_kit'] + ' ' + ', '.join('#' + x for x in SIB) if SIB else 'none'))
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g30T1/pull/' + n).strip()
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
def golden_apply(mb, gd, paths):
    """apply a golden diff with `git apply --cached` (strict) onto the merge-base tree in a scratch index; blob per path, or the refusal"""
    if not os.path.exists(gd): return None, 'golden diff ABSENT (%s)' % gd
    idx = tempfile.mktemp(prefix='g30T1gold', dir=os.path.join(SP, 'g30T1_sp')); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', mb], env=e3)
    ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', gd], capture_output=True, text=True, env=e3)
    if ra.returncode != 0: return None, 'does NOT apply at the merge-base: %s' % ra.stderr.strip()[:200]
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
    return {p: blob(t_, p) for p in paths}, 'applies strictly'
SITE = "res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"
R3 = "  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
PROBES = {}
for n in NS:
    h = H[n]; mb = P[n]['merge_base']; out = []
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    d = g('diff', '-U0', mb, h, '--', *prod) if prod else ''
    ch = [l[1:] for l in d.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
    nc = [l for l in ch if not re.match(r'^\s*(//|\*|/\*)', l) and l.strip()]
    out.append('product files %s: changed lines %d, NON-comment changed lines %d (a line-prefix READ, NOT an emit)' % ([os.path.basename(p) for p in prod], len(ch), len(nc)))
    if n == '1292':
        W = 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'; T = 'Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts'
        sd, sh = show(mb, W), show(h, W); dl_, hl = sd.splitlines(), sh.splitlines(); RX = r"webhooksRouter\.(get|post|put|patch|delete)\('([^']*)'"
        out.append('LEAK SITES (READ, fixed-string `message: err.message` in webhooks.ts): merge-base %d -> head %d; `fail500(` merge-base %d -> head %d (1 declaration + %d calls at head)' % (
            sd.count('message: err.message'), sh.count('message: err.message'), sd.count('fail500('), sh.count('fail500('), sh.count('fail500(res,')))
        minus, plus = minus_plus(mb, h, W)
        out.append('CONVERTED-TWO (READ, `git diff -U0` merge-base -> head on webhooks.ts): %d `-` line(s), every one the SITE line: %s; %d `+` line(s), every one a `fail500(res, ...)` call: %s' % (
            len(minus), all(x.strip() == SITE for x in minus), len(plus), all(x.strip().startswith('fail500(res, ') for x in plus)))
        conv = [(route_of(hl, i, RX), i + 1, re.search(r"fail500\(res, '([^']*)'", l).group(1)) for i, l in enumerate(hl) if 'fail500(res,' in l]
        out.append('ALL SEVEN SITES (READ, at head): %d `fail500(res,` calls %s; distinct contexts %d; a context naming its own route\'s method: %s' % (
            len(conv), conv, len(set(c[2] for c in conv)), all(c[0].split(' ')[0] in c[2] for c in conv)))
        em = [(i + 1, l.strip()[:90]) for i, l in enumerate(hl) if 'err.message' in l]
        out.append('ERR.MESSAGE LEFT (READ, fixed-string `err.message` at head, every line): %s — the PR says both are server-side logs (:544 logger.warn, :563 the helper)' % em)
        def c3(src):   # the ks1341c C3 SOURCE cell's own rule, re-implemented line for line (a READ of the cell, not a run)
            L = [l for l in src.split('\n') if not l.strip().startswith('*') and not l.strip().startswith('//')]
            hc = [l for l in L if 'fail500(res,' in l]; cx = [(re.search(r"fail500\(res, '([^']+)'", l) or [None, None])[1] for l in hc]
            return {'leaks': sum(1 for l in L if re.search(r'message: *err\??\.?message', l)), 'helperCalls': len(hc), 'distinctContexts': len(set(cx)), 'definitions': sum(1 for l in L if l.startswith('function fail500('))}
        out.append('C3 SOURCE RULE (READ, the cell\'s filter re-implemented): merge-base %s | head %s | the cell expects {leaks: 0, helperCalls: 7, distinctContexts: 7, definitions: 1}. C3 pins a COUNT and DISTINCTNESS — not WHICH seven routes; a site moved or a context mislabelled onto another route keeps it green (the gate grades whether that matters)' % (c3(sd), c3(sh)))
        R3n = [i + 1 for i, l in enumerate(hl) if l == R3]
        out.append('ARM-R3 ANCHOR (READ, at head): the brief\'s R3 anchor `logger.error(context, { error: err instanceof Error ? err.message : String(err) });` (2 leading spaces) occurs %d time(s) at %s; brief-C\'s tamper is the un-braced `if (process.env.NODE_ENV === \'production\') logger.error(...)`' % (len(R3n), R3n))
        stale = ['the only place in this router that turns a caught error into a 500', 'Declared at the END of the file', 'Seven catch blocks above put the thrown error\'s own text']
        out.append('DOCBLOCK THREE SENTENCES (READ, at head; DECLARED NOT COVERED by the PR, a docs ticket follows): %s' % [(s[:48], [i + 1 for i, l in enumerate(hl) if s in l]) for s in stale])
        dc = [i + 1 for i, l in enumerate(hl) if '.catch(() => [])' in l]
        out.append('DELIVERIES TRAP (READ): `.catch(() => [])` at head line(s) %s — a REJECTED deliveries query is swallowed into a 200 before the catch; the cell arms GET /:id/deliveries with a SYNCHRONOUS throw (control C0 pins the swallow)' % dc)
        fns = {}
        def fb(L, nm):
            s = [i for i, l in enumerate(L) if l.startswith(('function ' + nm + '(', 'async function ' + nm + '(', 'export function ' + nm + '(', 'export async function ' + nm + '('))][:1]
            if not s: return []
            e = s[0]
            while e < len(L) and L[e] != '}': e += 1
            return L[s[0]:e + 1]
        for nm in ('encryptWebhookSecret', 'decryptWebhookSecret', 'deliverWebhook', 'dispatchEvent', 'fail500'):
            b0, b1 = fb(dl_, nm), fb(hl, nm)
            fns[nm] = ('IDENTICAL (%d lines)' % len(b0)) if b0 and b0 == b1 else ('ABSENT' if not b0 else 'DIFFERS')
        out.append('UNTOUCHED BODIES (READ, merge-base vs head, line-equal): %s' % fns)
        GB = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1341/golden/'
        gw, gt, ga = ho(GB + 'webhooks.ABC.ts'), ho(GB + 'ks1341c-webhooks-500-never-answers-err-message.test.ts'), ho(GB + 'webhooks.AB.ts')
        gb_, gm = golden_apply(mb, GB + 'C.golden.diff', [W, T])
        out.append('GOLDEN (READ, `git hash-object` of brief-C rev C\'s golden files vs the head blobs): webhooks.ABC.ts %s vs head %s -> %s; ks1341c test %s vs head %s -> %s; the merge-base webhooks.ts %s vs golden webhooks.AB.ts %s -> %s; C.golden.diff at the merge-base: %s%s' % (
            gw[:12], (blob(h, W) or '-')[:12], 'EXACT' if gw == blob(h, W) else 'DIFFERENT', gt[:12], (blob(h, T) or '-')[:12], 'EXACT' if gt == blob(h, T) else 'DIFFERENT',
            (blob(mb, W) or '-')[:12], ga[:12], 'EXACT' if ga == blob(mb, W) else 'DIFFERENT', gm, (' -> both blobs == head: %s' % (gb_[W] == blob(h, W) and gb_[T] == blob(h, T))) if gb_ else ''))
        ts = show(h, T); TL = ts.splitlines()
        loop = [i + 1 for i, l in enumerate(TL) if 'for (const nodeEnv of NODE_ENVS)' in l]; clr = [i + 1 for i, l in enumerate(TL) if 'mockLoggerError.mockClear()' in l]
        out.append('TEST FILE (READ): %d lines; RED titles %s; controls %d; the NODE_ENV loop at %s, `mockLoggerError.mockClear()` at %s (INSIDE the loop: %s); `.at(-1)` occurrences %d; listens on %s; NODE_ENVS %s' % (
            len(TL), sorted(set(re.findall(r"RED KS-1341 (C\d)", ts))), len(re.findall(r"^  it\('control KS-1341", ts, re.M)), loop, clr, bool(loop and clr and loop[0] < clr[0] < loop[0] + 5), ts.count('.at(-1)'),
            re.findall(r"app\.listen\(0, '([^']+)'", ts), re.findall(r'const NODE_ENVS = (\[[^\]]*\])', ts)))
    if n == '1294':
        A_ = 'Blockchain/Dev/services/originate/src/routes/adminConfig.ts'; T = 'Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts'
        sd, sh = show(mb, A_), show(h, A_); dl_, hl = sd.splitlines(), sh.splitlines(); RX = r"adminConfigRouter\.(get|post|put|patch|delete)\('([^']+)'"
        def c4(L): return [(route_of(L, i, RX), i + 1) for i, l in enumerate(L) if re.search(r'message: *err\??\.?message', l)]
        out.append('UNCONDITIONAL SITES (READ, the ks730c C4 regex `message: *err\\??\\.?message` per enclosing route): merge-base %s -> head %s' % (c4(dl_), c4(hl)))
        minus, plus = minus_plus(mb, h, A_)
        out.append('CONVERTED-TWO (READ, `git diff -U0` on adminConfig.ts): `-` %s | `+` %s' % ([x.strip()[:120] for x in minus], [x.strip()[:120] for x in plus]))
        hc = lambda L: [(re.search(r"fail500\(res, '([^']+)'", l) or [None, None])[1] for l in L if 'fail500(res,' in l]
        out.append('HELPER CALLS (READ): merge-base %d calls / %d distinct -> head %d / %d; `fail500` declared at head line(s) %s, body logs %s' % (
            len(hc(dl_)), len(set(hc(dl_))), len(hc(hl)), len(set(hc(hl))), [i + 1 for i, l in enumerate(hl) if l.startswith('function fail500(')], [l.strip()[:100] for l in hl if 'logger.error(context' in l][:1]))
        def catch_block(L, pat):
            s = [i for i, l in enumerate(L) if pat in l][:1]
            if not s: return []
            e = s[0]
            while e < len(L) and L[e] != '});': e += 1
            b = L[s[0]:e + 1]; c = [j for j, l in enumerate(b) if 'catch (' in l]
            return [x.strip()[:110] for x in b[c[-1]:]] if c else []
        for pat in ("adminConfigRouter.post('/refresh-tenants'", "adminConfigRouter.post('/backfill-certification-metadata'"):
            out.append('CATCH BODY at head (READ) for %s: %s — a benign `does not exist` / 42P01 branch in this catch: %s' % (pat.split("'")[1], catch_block(hl, pat), any('does not exist' in x for x in catch_block(hl, pat))))
        ts0, ts = show(mb, T), show(h, T)
        LK = re.findall(r"^const LEAK = '([^']*)';", ts, re.M); LK2 = re.findall(r"^const KS1334_LEAK = '([^']*)';", ts, re.M)
        out.append('LEAKED-CHECK (READ): the shared LEAK %r contains a double quote: %s -> JSON-escaped in the body, so `reply.text.includes(LEAK)` CAN NEVER be true (json.dumps carries it verbatim: %s); KS1334_LEAK %r survives JSON encoding: %s. What still catches a leak in C1: `expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY)` occurs %d time(s) in the file, at C1 line(s) %s' % (
            LK[0][:60] if LK else None, bool(LK and '"' in LK[0]), bool(LK and LK[0] in json.dumps({'message': LK[0]})), LK2[0][:60] if LK2 else None, bool(LK2 and LK2[0] in json.dumps({'message': LK2[0]})),
            ts.count('expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY)'), [i + 1 for i, l in enumerate(ts.splitlines()) if 'expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY)' in l]))
        out.append('IN-PLACE ks730c EDITS (READ, `git diff --numstat`): %s; C3 pin 46/46 -> %s; C4 KNOWN at head %s; the new block drives NODE_ENVs %s with `mockLoggerError.mockClear()` inside its loop: %s' % (
            g('diff', '--numstat', mb, h, '--', T).split('\t')[:2], re.findall(r'helperCalls: (\d+), distinctContexts: (\d+) \}\);', ts), re.findall(r"const KNOWN = \[\s*([^\]]*)\]", ts), re.findall(r'const KS1334_NODE_ENVS = (\[[^\]]*\])', ts),
            bool(re.search(r'for \(const nodeEnv of KS1334_NODE_ENVS\) \{\s*mockLoggerError\.mockClear\(\);', ts))))
        GB = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1334/golden/'
        ga, gt = ho(GB + 'adminConfig.A.ts'), ho(GB + 'ks730c.A.ts'); gb_, gm = golden_apply(mb, GB + 'KS-1334-A.golden.diff', [A_, T])
        out.append('GOLDEN (READ, brief-A\'s golden vs the head blobs): adminConfig.A.ts %s vs head %s -> %s; ks730c.A.ts %s vs head %s -> %s; KS-1334-A.golden.diff at the merge-base: %s%s — the Spark ran on an EXCERPTED input (3 regions of adminConfig.ts, briefs/KS-1334/README.md)' % (
            ga[:12], (blob(h, A_) or '-')[:12], 'EXACT' if ga == blob(h, A_) else 'DIFFERENT', gt[:12], (blob(h, T) or '-')[:12], 'EXACT' if gt == blob(h, T) else 'DIFFERENT', gm,
            (' -> both blobs == head: %s' % (gb_[A_] == blob(h, A_) and gb_[T] == blob(h, T))) if gb_ else ''))
    if n in ('1296', '1297'):
        S_, T, GB, GDN, TL_ = {'1296': ('Blockchain/Dev/services/originate/src/routes/systemErrors.ts', 'Blockchain/Dev/services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts', '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-A/golden/', 'KS-1346-A.golden.diff', 'A'),
                                '1297': ('Blockchain/Dev/services/originate/src/routes/gdpr.ts', 'Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts', '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-B/golden/', 'KS-1346-B.golden.diff', 'B')}[n]
        minus, plus = minus_plus(mb, h, S_)
        out.append('PRODUCT DIFF (READ, `git diff -U0` on %s): `-` %s | `+` %s' % (os.path.basename(S_), [x.strip()[:130] for x in minus], [x.strip()[:130] for x in plus]))
        sh = show(h, S_)
        out.append('LOG SINK (READ): %s imports the logger from %s; originate utils/logger.ts carries `redact` %d time(s), `SENSITIVE` %d, `password` %d (a winston logger with NO redaction format); packages/shared/src/logger/index.ts carries `SENSITIVE_KEYS` %d time(s) and is NOT the sink on this path' % (
            os.path.basename(S_), re.findall(r"import \{ logger \} from '([^']+)'", sh), *(show(REAL_DEV, 'Blockchain/Dev/services/originate/src/utils/logger.ts').lower().count(x) for x in ('redact', 'sensitive', 'password')),
            show(REAL_DEV, 'Blockchain/Dev/packages/shared/src/logger/index.ts').count('SENSITIVE_KEYS')))
        out.append('INSPECT WIDENING (READ, by construction — the gate MEASURES it): at head a thrown value that is neither an Error nor a string reaches `logger.error(context, { error: inspect(err) })` — util.inspect renders every own enumerable key and value to depth 2, so a thrown `{ password, token, email }` puts all three VALUES into the log line where the tip logged `[object Object]`; the PR body itself declares it (%s); the seat\'s s-inspect-probe.out (a node run of the two expressions, not of the router) is a claim. Wednesday\'s WIDEN rule: the gate proves inspect CANNOT put a secret/PII-looking field in the log line, or grades #%s NO GO' % ({'1296': '"It can, and nothing on this path redacts it."', '1297': '"it widens what reaches log storage on the one surface where that is most sensitive" — a SUBJECT-DATA surface'}[n], n))
        out.append('FAMILY (READ, `String(err)` fail500 bodies at develop): %s — parts A (systemErrors.ts) and B (gdpr.ts, a subject-data surface) are both in this kit; adminConfig.ts and webhooks.ts keep String(err)' % [x.split(':', 2)[1] + ':' + x.split(':', 2)[2].split(':')[0] for x in gq('grep', '-n', '-E', r'logger\.error\(context, \{ error: err instanceof Error \? err\.message : String\(err\) \}\);', REAL_DEV, '--', 'Blockchain/Dev/services/originate/src/routes/')[1].strip().splitlines()])
        ts = show(h, T)
        out.append('TEST FILE (READ): %d lines; RED rows %s x %d routes; controls %s; the object throw(s) the cell makes %s (no secret-looking key anywhere in the cell: %s); `inspect` imported by the cell %d time(s)' % (
            len(ts.splitlines()), sorted(set(re.findall(r"RED KS-1346 (%s\d)" % TL_, ts))), len(re.findall(r"^  \{ label: '", ts, re.M)), sorted(set(re.findall(r"control KS-1346 (%s\d)" % TL_, ts))),
            sorted(set(re.findall(r"callWithThrow\([^,]+, (\{[^}]*\})\)", ts))), not re.search(r'(?i)password|token|secret|email|apikey|ssn', ts), ts.count("from 'util'")))
        gt = ho(GB + os.path.basename(T)); gb_, gm = golden_apply(mb, GB + GDN, [S_, T])
        out.append('GOLDEN (READ, %s): test %s vs head %s -> %s; the golden diff at the merge-base: %s%s' % (GB.split('/briefs/')[1] + GDN,
            gt[:12], (blob(h, T) or '-')[:12], 'EXACT' if gt == blob(h, T) else 'DIFFERENT', gm, (' -> both blobs == head: %s' % (gb_[S_] == blob(h, S_) and gb_[T] == blob(h, T))) if gb_ else ''))
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
