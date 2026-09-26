#!/usr/bin/env python3
"""predict_gate30T2.py — MEASURE one gate30T2 kit (the directory this script lives in; its PR set, tiers and commit counts are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json carries
NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and the
fetch into the scratch clone must agree with both.

Shape copied from gate29's predict_gate29.py (the kit that worked on 2026-09-26) and re-keyed for gate30T2: FOUR rows, all T2 (#1293 KS-1344, a
TEST-ONLY edit of the ks1341a cell; #1295 KS-1337 akto site, systemTest/akto preSuiteSetup.ts + one vitest cell; #1298 KS-1347, the WIDEN row:
services/auth ks732 test paths + one vitest cell, TEST FILES ONLY; #1299 KS-1339, the second WIDEN row: ks1293's CONFIGPINNED
assertion order + one jest cell, TEST FILES ONLY), a SIBLING kit gate30T1 (#1292,
#1294, #1296, #1297 — END_TREE_WITH_SIBLING is measured both ways), a PER-PR merge-base and a DECLARED COMMIT COUNT per PR (one each). The in-flight census
is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN
census (kit.json `widen_rx`: KS-1347 / KS-1339) is HARD: an open PR matching it outside this kit and its sibling refuses. No dead-open overlap.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g30T2_sp/clone.git — `git clone --bare --no-local` FROM the checkout (NO
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
invariance of a develop move; gate30T2 cannot use an OLDER develop: #1292 needs part B, #1290, on the current one). A simulation writes
pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate30T2.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate30T2.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g30T2_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate30T2 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g30T2/develop']
    + ['+refs/pull/%s/head:refs/g30T2/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g30T2/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g30T2/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g30T2/pull/' + n).strip() == g('rev-parse', 'refs/g30T2/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
if SIM == 'moved':
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input='gate30T2 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n').strip()
    idx = tempfile.mktemp(prefix='g30T2idx', dir=os.path.join(SP, 'g30T2_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, 'GATE30T2-SIMULATED-MOVE.txt')], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', DEV, '-m', 'gate30T2 SIMULATION moved'], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE30T2-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    mb0 = g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', mb0, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n# gate30T2 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g30T2idx', dir=os.path.join(SP, 'g30T2_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate30T2 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g30T2/pull/' + n).strip()
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
def golden_apply(mb, gd, paths):
    """apply a golden diff with `git apply --cached` (strict) onto the merge-base tree in a scratch index; blob per path, or the refusal"""
    if not os.path.exists(gd): return None, 'golden diff ABSENT (%s)' % gd
    idx = tempfile.mktemp(prefix='g30T2gold', dir=os.path.join(SP, 'g30T2_sp')); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', mb], env=e3)
    ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', gd], capture_output=True, text=True, env=e3)
    if ra.returncode != 0: return None, 'does NOT apply at the merge-base: %s' % ra.stderr.strip()[:160].replace('\n', ' / ')
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
    return {p: blob(t_, p) for p in paths}, 'applies strictly'
R3 = "  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
PROBES = {}
for n in NS:
    h = H[n]; mb = P[n]['merge_base']; out = []
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/unit/' not in p]
    if prod:
        d = g('diff', '-U0', mb, h, '--', *prod)
        ch = [l[1:] for l in d.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
        nc = [l for l in ch if not re.match(r'^\s*(//|\*|/\*)', l) and l.strip()]
        out.append('product files %s: changed lines %d, NON-comment changed lines %d (a line-prefix READ, NOT an emit)' % ([os.path.basename(p) for p in prod], len(ch), len(nc)))
    else:
        out.append('NO product file: every path is a test path %s — TEST-ONLY (no product byte)' % [os.path.basename(p) for p in P[n]['paths']])
    if n == '1293':
        T = 'Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts'; W = 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'
        minus, plus = minus_plus(mb, h, T)
        out.append('TEST DIFF (READ, `git diff -U0` on ks1341a): `-` %s | `+` %s' % ([x.strip()[:110] for x in minus], [x.strip()[:110] for x in plus]))
        ts0, ts = show(mb, T), show(h, T); TL = ts.splitlines()
        loop = [i + 1 for i, l in enumerate(TL) if 'for (const nodeEnv of NODE_ENVS)' in l]; clr = [i + 1 for i, l in enumerate(TL) if 'mockLoggerError.mockClear()' in l]
        out.append('A1 SHAPE (READ): `.at(-1)` merge-base %d -> head %d; the NODE_ENV loop at %s, `mockLoggerError.mockClear()` at %s (INSIDE the loop: %s); NODE_ENVS %s; the A1 whole-list assertion carries `nodeEnv` in its expected value: %s (a red names its environment only through the loop order if not); A2 unchanged (production only): %s' % (
            ts0.count('.at(-1)'), ts.count('.at(-1)'), loop, clr, bool(loop and clr and loop[0] < clr[0] < loop[0] + 5), re.findall(r'const NODE_ENVS = (\[[^\]]*\])', ts),
            'nodeEnv, calls' in ts, [l for l in ts0.splitlines() if 'RED KS-1341 A2' in l] == [l for l in TL if 'RED KS-1341 A2' in l]))
        wd = show(REAL_DEV, W).splitlines()
        out.append('THE PRODUCT TAMPER TARGET (READ): the R3 anchor `%s` occurs %d time(s) in webhooks.ts at the launch develop, at %s — the red for a test-only PR comes from THIS product tamper (production-only logging): A1 rows red at #1293\'s head, GREEN at the tip (develop\'s ks1341a, `.at(-1)`) under the same tamper' % (R3.strip()[:60], sum(1 for l in wd if l == R3), [i + 1 for i, l in enumerate(wd) if l == R3]))
        out.append('A1 ROUTES (READ): %s — two rows, GET / (synchronous throw; control A0 pins the swallow) and POST / (rejected $executeRaw)' % re.findall(r"label: '([^']+)'", ts))
        GD = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1344.golden/KS-1344.golden.diff'
        gb_, gm = golden_apply(mb, GD, [T])
        out.append('GOLDEN (READ): KS-1344.golden.diff (%s, %d B) at the merge-base: %s%s; the pre-image blob at the merge-base %s (the PR says 3318cccbca3f at both 179a4f32 and 3f70224a: at gate29\'s develop %s)' % (
            ho(GD)[:12], os.path.getsize(GD) if os.path.exists(GD) else -1, gm, (' -> blob == head: %s' % (gb_[T] == blob(h, T))) if gb_ else '', (blob(mb, T) or '-')[:12], (blob(K['predev'], T) or '-')[:12]))
    if n == '1295':
        C = 'systemTest/akto/tests/preSuiteSetup.ts'; T = 'systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts'
        minus, plus = minus_plus(mb, h, C)
        out.append('PRODUCT DIFF (READ, `git diff -U0` on preSuiteSetup.ts): `-` %s | `+` %s' % ([x.strip()[:110] for x in minus], [x.strip()[:110] for x in plus]))
        cd, ch_ = show(mb, C), show(h, C)
        sp_ = lambda t: [l.strip() for l in t.splitlines() if "spawnSync('npx', ['tsx', step" in l]
        out.append('SPAWN UNCHANGED (READ): `spawnSync(\'npx\', [\'tsx\', step, label], ...)` merge-base %s | head %s | byte-identical: %s' % (sp_(cd), sp_(ch_), sp_(cd) == sp_(ch_) and len(sp_(ch_)) == 1))
        sweep = {}
        for c_, lab in ((REAL_DEV, 'develop'), (h, 'head')):
            rc, o, _ = gq('grep', '-n', '-E', r'import\.meta\.url\)\.pathname', c_, '--', 'systemTest/', 'Blockchain/Dev/')
            sweep[lab] = [':'.join(x.split(':')[1:3]) for x in o.strip().splitlines()] if rc == 0 else []
        rc2, o2, _ = gq('grep', '-n', '-E', r'new URL\([^)]*\)\.pathname', REAL_DEV, '--', 'systemTest/')
        out.append('SITE SWEEP (READ, `git grep -nE "import\\.meta\\.url\\)\\.pathname" -- systemTest/ Blockchain/Dev/`): develop %s | head %s; the wider `new URL(...).pathname` form in systemTest/ at develop: %s — KS-1337 site 2 of 3 (playwright global-setup.ts:42 left, KS-1337 stays open); KS1347 owns the Blockchain/Dev occurrences' % (
            sweep['develop'], sweep['head'], [':'.join(x.split(':')[1:3]) for x in o2.strip().splitlines()] if rc2 == 0 else 'NONE'))
        ts = show(h, T)
        out.append('CELL (READ, at head): %d lines; `spawn`/`spawnSync`/`execFile`/`execSync`/`fork` calls %d; reads preSuiteSetup.ts as TEXT (`readFileSync(`) %d; the statement filter `line.trim().startsWith(\'const step = \')` %d; `mkdtempSync` %d; `rmSync` %d (afterEach, inside its own tmpdir); the literal `Testing Agent MAIN` %d; `await import(` %d — the cell never runs the npx/tsx pre-suite step (the same DoD-2 boundary #1291 disclosed)' % (
            len(ts.splitlines()), len(re.findall(r'\b(spawn|spawnSync|execFile|execFileSync|execSync|fork)\(', ts)), ts.count('readFileSync('), ts.count("startsWith('const step = ')"), ts.count('mkdtempSync('), ts.count('rmSync('), ts.count('Testing Agent MAIN'), ts.count('await import(')))
        GB = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
        gb_, gm = golden_apply(mb, GB + 'KS-1337/golden/KS-1337-akto.golden.diff', [C, T])
        gw_, gmw = golden_apply(mb, GB + 'KS-1337.golden/KS-1337.golden.diff', [C, T])
        out.append('GOLDEN (READ): briefs/KS-1337/golden/KS-1337-akto.golden.diff at the merge-base: %s%s | the OTHER golden briefs/KS-1337.golden/KS-1337.golden.diff (the k6 site, #1291) at the merge-base: %s — the PR says the akto one is the match' % (
            gm, (' -> both blobs == head: %s' % (gb_[C] == blob(h, C) and gb_[T] == blob(h, T))) if gb_ else '', gmw))
        pk = show(REAL_DEV, 'systemTest/akto/package.json')
        try: pj = json.loads(pk); sc = pj.get('scripts', {}); eng = pj.get('engines')
        except Exception: sc, eng = {}, None
        out.append('PACKAGE SCRIPTS (READ, systemTest/akto/package.json at develop): lint `%s`; format:check `%s`; test:unit `%s`; engines %s' % (sc.get('lint'), sc.get('format:check'), sc.get('test:unit'), eng))
        tc = show(REAL_DEV, 'systemTest/akto/tsconfig.json'); vc = show(REAL_DEV, 'systemTest/akto/vitest.unit.config.ts')
        sq = lambda x: re.sub(r'\s+', ' ', x)
        out.append('PROGRAMS (READ): tsconfig.json include %s exclude %s (covers tests/**/*.ts: the lint script\'s ONE tsc stage sees both files); vitest.unit.config include %s' % (
            [sq(x) for x in re.findall(r'"include"\s*:\s*(\[[^\]]*\])', tc)], [sq(x) for x in re.findall(r'"exclude"\s*:\s*(\[[^\]]*\])', tc)], re.findall(r'include\s*:\s*(\[[^\]]*\])', vc)))
    if n == '1298':
        K7 = 'Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts'; T = 'Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts'
        out.append('TEST FILES ONLY (READ): paths NOT under services/auth/src/__tests__/: %s — no auth product file changes: %s' % ([p for p in P[n]['paths'] if '/src/__tests__/' not in p] or 'NONE', not [p for p in P[n]['paths'] if '/src/__tests__/' not in p]))
        minus, plus = minus_plus(mb, h, K7)
        out.append('ks732 DIFF (READ, `git diff -U0`): `-` %s | `+` %s' % ([x.strip()[:90] for x in minus], [x.strip()[:100] for x in plus]))
        sweep = {}
        for c_, lab in ((REAL_DEV, 'develop'), (h, 'head')):
            rc, o, _ = gq('grep', '-n', '-E', r'import\.meta\.url\)\.pathname', c_, '--', 'Blockchain/Dev/')
            sweep[lab] = [':'.join(x.split(':')[1:3]) for x in o.strip().splitlines()] if rc == 0 else []
        out.append('SITE SWEEP (READ, `git grep -nE "import\\.meta\\.url\\)\\.pathname" -- Blockchain/Dev/`): develop %s | head %s — KS-1347 site 1 of 2 (the proxy server.ts site left, the ticket stays open)' % (sweep['develop'], sweep['head']))
        GB = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1347/golden/'
        gb_, gm = golden_apply(mb, GB + 'KS-1347-ks732.golden.diff', [K7, T])
        dn = ''
        if gb_:
            idx = tempfile.mktemp(prefix='g30T2gold', dir=os.path.join(SP, 'g30T2_sp'))
            dn = g('diff', '--numstat', gb_[T], blob(h, T)).strip() if gb_[T] and blob(h, T) else ''
        out.append('GOLDEN (READ, briefs/KS-1347/golden/KS-1347-ks732.golden.diff at the merge-base: %s): ks732 golden %s vs head %s -> %s; the new cell golden %s vs head %s -> %s%s — the PR declares ONE token renamed on review (`(line, i)` -> `(_line, i)`, TS6133 under a test-inclusive compile)' % (
            gm, ((gb_ or {}).get(K7) or '-')[:12], (blob(h, K7) or '-')[:12], 'EXACT' if gb_ and gb_[K7] == blob(h, K7) else 'DIFFERENT', ((gb_ or {}).get(T) or '-')[:12], (blob(h, T) or '-')[:12],
            'EXACT' if gb_ and gb_[T] == blob(h, T) else 'DIFFERENT', (' (numstat golden -> head %s)' % dn.split('\t')[:2]) if dn else ''))
        ts = show(h, T)
        out.append('CELL (READ, at head): %d lines; `spawn`/`exec`/`fork` calls %d; reads ks732 as TEXT (`readFileSync(`) %d; TARGETS %s; `realpathSync` %d (the tmpdir symlink on macOS); `rmSync` %d; the literal `Testing Agent MAIN` %d; `await import(` %d; `_line` %d / `(line, i)` %d' % (
            len(ts.splitlines()), len(re.findall(r'\b(spawn|spawnSync|execFile|execFileSync|execSync|fork)\(', ts)), ts.count('readFileSync('), re.findall(r'const TARGETS = (\[[^\]]*\])', ts), ts.count('realpathSync('), ts.count('rmSync('), ts.count('Testing Agent MAIN'), ts.count('await import('), ts.count('_line'), ts.count('(line, i)')))
        pk = show(REAL_DEV, 'Blockchain/Dev/services/auth/package.json')
        try: sc = json.loads(pk).get('scripts', {})
        except Exception: sc = {}
        tc = show(REAL_DEV, 'Blockchain/Dev/services/auth/tsconfig.json')
        out.append('AUTH PACKAGE (READ, at develop): test `%s` (VITEST, not jest), lint `%s`, build `%s`; tsconfig.json exclude %s' % (sc.get('test'), sc.get('lint'), sc.get('build'), [re.sub(r'\s+', ' ', x) for x in re.findall(r'"exclude"\s*:\s*(\[[^\]]*\])', tc)]))
    if n == '1299':
        K3 = 'Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts'; T = 'Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts'
        out.append('TEST FILES ONLY (READ): paths NOT under services/originate/src/__tests__/: %s' % ([p for p in P[n]['paths'] if '/src/__tests__/' not in p] or 'NONE'))
        k0, k1 = show(mb, K3).splitlines(), show(h, K3).splitlines()
        def cell(L):
            s_ = [i for i, l in enumerate(L) if l.strip().startswith("it('CONFIGPINNED:")][:1]
            if not s_: return []
            e = s_[0]
            while e < len(L) and L[e] != '  });': e += 1
            return [l.strip() for l in L[s_[0]:e + 1]]
        c0, c1 = cell(k0), cell(k1)
        out.append('CONFIGPINNED CELL (READ, merge-base -> head): %d -> %d lines; the SAME multiset of lines: %s; order of the two assertions at merge-base %s -> head %s' % (
            len(c0), len(c1), sorted(c0) == sorted(c1), [x[:40] for x in c0 if x.startswith('expect(')], [x[:40] for x in c1 if x.startswith('expect(')]))
        out.append('FILE HEADER CLAIM (READ): ks1293 says an offender is NAMED BY FILE: %s' % [l.strip()[:120] for l in k1 if re.search(r'(?i)named by file|NAMED BY FILE', l)][:2])
        ts = show(h, T)
        out.append('CELL (READ, at head): %d lines; `new Function(` %d (it EXECUTES the CONFIGPINNED statements read as TEXT from ks1293); END anchor `line === \'  });\'` %d; RED titles %s; controls %s' % (
            len(ts.splitlines()), ts.count('new Function('), ts.count("line === '  });'"), sorted(set(re.findall(r'RED KS-1339 (A\d)', ts))), sorted(set(re.findall(r'control KS-1339 (A\d)', ts)))))
        GD = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1339/golden/KS-1339.golden.diff'
        gb_, gm = golden_apply(mb, GD, [K3, T])
        out.append('GOLDEN (READ, briefs/KS-1339/golden/KS-1339.golden.diff at the merge-base: %s)%s' % (gm, (' -> both blobs == head: %s' % (gb_[K3] == blob(h, K3) and gb_[T] == blob(h, T))) if gb_ else ''))
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
