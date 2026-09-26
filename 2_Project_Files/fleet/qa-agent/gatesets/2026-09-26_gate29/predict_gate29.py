#!/usr/bin/env python3
"""predict_gate29.py — MEASURE one gate29 kit (the directory this script lives in; its PR set, tiers and commit counts are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json carries
NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and the
fetch into the scratch clone must agree with both.

Shape copied from gate28's predict_gate28.py and re-keyed for gate29: TWO rows (#1290 KS-1341 part B, T1, a local-model patch on
services/originate routes/webhooks.ts; #1291 KS-1337, T2, systemTest/performance runner/cli.ts + one vitest cell), NO sibling kit
(END_TREE_WITH_SIBLING == END_TREE by construction), a PER-PR merge-base and a DECLARED COMMIT COUNT per PR (one each). The in-flight census is
EVERY OTHER OPEN PR at the pin (kit.json `inflight`, read by the PULLS API): hard path-disjoint. No dead-open overlap is declared
(kit.json `dead_open_declared` is empty; the machinery is kept from gate28 and asserts nothing when empty).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g29_sp/clone.git — `git clone --bare --no-local` FROM the checkout (NO
alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never
printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over merge-base(develop, head), with NO merge
commit among them; (1) diff(develop, merged) == EXACTLY the PR's own paths (diff(merge-base, head)), each merged blob byte-equal to the head's blob
(kit.json `declared_overlap` would carry a 3-way target; BOTH gate29 kits declare NONE — measured); (2) numstat(develop -> merged) ==
numstat(merge-base -> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. NOT STACKED: for every pair in the kit (and
across a sibling kit, if any), neither head is an ancestor of the other and their merge-base is an ancestor of develop (no shared non-develop commit).
PAIRWISE the kit's path sets are DISJOINT (hard), disjoint from the SIBLING kit's (hard: the kits may merge in either order), and disjoint from
Seat B 30th's in-flight PRs and worktree(s) (hard: an overlap must be DECLARED by a re-draft, never absorbed). END_TREE = develop + every PR of
the kit, identical in ALL orders (N! orders, memoised on (tree, PR) so equal states are merged once), and END_TREE_WITH_SIBLING = develop + the
sibling kit + this kit, identical whichever kit lands first. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the kit) builds develop + a FOREIGN edit of that PR's first own
file and must REFUSE; --simulate moved builds develop + an UNRELATED synthetic commit (a new file no PR touches) and must PASS (the base-
invariance of a develop move; gate29 cannot use an OLDER develop: #1288 and #1289 sit on the current one). A simulation writes
pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate29.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate29.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g29_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate29 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g29/develop']
    + ['+refs/pull/%s/head:refs/g29/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g29/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g29/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g29/pull/' + n).strip() == g('rev-parse', 'refs/g29/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
if SIM == 'moved':
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input='gate29 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n').strip()
    idx = tempfile.mktemp(prefix='g29idx', dir=os.path.join(SP, 'g29_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, 'GATE29-SIMULATED-MOVE.txt')], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', DEV, '-m', 'gate29 SIMULATION moved'], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE29-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    mb0 = g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', mb0, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n# gate29 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g29idx', dir=os.path.join(SP, 'g29_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate29 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g29/pull/' + n).strip()
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
    if n == '1290':
        W = 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'; T = 'Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts'
        SITE = "res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"
        sd, sh = show(mb, W), show(h, W); dl_, hl = sd.splitlines(), sh.splitlines()
        def route_of(L, i):
            for j in range(i, -1, -1):
                m = re.search(r"webhooksRouter\.(get|post|put|patch|delete)\('([^']*)'", L[j])
                if m: return '%s %s' % (m.group(1).upper(), m.group(2))
            return '?'
        out.append('LEAK SITES (READ, fixed-string `message: err.message` in webhooks.ts): merge-base %d -> head %d; `fail500(` merge-base %d -> head %d (1 declaration + %d calls at head)' % (
            sd.count('message: err.message'), sh.count('message: err.message'), sd.count('fail500('), sh.count('fail500('), sh.count('fail500(res,')))
        d = g('diff', '-U0', mb, h, '--', W)
        minus = [l[1:] for l in d.splitlines() if l.startswith('-') and not l.startswith('---')]
        plus = [l[1:] for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
        conv = [(route_of(hl, i), i + 1, re.search(r"fail500\(res, '([^']*)'", l).group(1)) for i, l in enumerate(hl) if 'fail500(res,' in l and i + 1 < len(hl)]
        out.append('CONVERTED-THREE (READ, `git diff -U0` merge-base -> head on webhooks.ts): %d `-` line(s), every one the SITE line: %s; %d `+` line(s), every one a `fail500(res, ...)` call: %s; the fail500 calls at head (route, line, context): %s' % (
            len(minus), all(x.strip() == SITE for x in minus), len(plus), all(x.strip().startswith('fail500(res, ') for x in plus), conv))
        left = [(route_of(hl, i), i + 1) for i, l in enumerate(hl) if 'message: err.message' in l]
        out.append('UNCONVERTED-TWO (READ): `message: err.message` 500 lines left at head %s; each line byte-identical to its merge-base line: %s (declared scope — part C)' % (
            left, all(hl[i - 1] == dl_[i - 1] for _, i in left) if len(hl) == len(dl_) else 'LINE COUNT MOVED %d -> %d' % (len(dl_), len(hl))))
        def block(L, pat):
            s = [i for i, l in enumerate(L) if pat in l][:1]
            if not s: return []
            e = s[0]
            while e < len(L) and L[e] != '});': e += 1
            return L[s[0]:e + 1]
        rb0, rb1 = block(dl_, "webhooksRouter.post('/:id/rotate-secret'"), block(hl, "webhooksRouter.post('/:id/rotate-secret'")
        diffl = [(a, b) for a, b in zip(rb0, rb1) if a != b]
        sec = [(i + 1, l.strip()[:90]) for i, l in enumerate(hl) if any(k in l for k in ('newSecret', 'encryptWebhookSecret(', 'secret_v2'))]
        out.append('SECRET-PATH (READ, the rotate-secret handler block merge-base vs head): %d line(s) -> %d line(s); lines that differ %d: %s; every OTHER line of the block byte-identical: %s; the secret-path lines at head %s' % (
            len(rb0), len(rb1), len(diffl), [(a.strip()[:60], b.strip()[:90]) for a, b in diffl], len(rb0) == len(rb1) and len(diffl) == 1, sec))
        fns = {}
        def fb(L, nm):   # a top-level function body: from its declaration line to the first line that is exactly `}`
            s = [i for i, l in enumerate(L) if l.startswith(('function ' + nm + '(', 'async function ' + nm + '(', 'export function ' + nm + '(', 'export async function ' + nm + '('))][:1]
            if not s: return []
            e = s[0]
            while e < len(L) and L[e] != '}': e += 1
            return L[s[0]:e + 1]
        for nm in ('encryptWebhookSecret', 'decryptWebhookSecret', 'deliverWebhook', 'dispatchEvent', 'fail500'):
            b0, b1 = fb(dl_, nm), fb(hl, nm)
            fns[nm] = ('IDENTICAL (%d lines)' % len(b0)) if b0 and b0 == b1 else ('ABSENT' if not b0 else 'DIFFERS')
        out.append('UNTOUCHED BODIES (READ, merge-base vs head, line-equal): %s' % fns)
        R3 = "  logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
        out.append('ARM-R3 ANCHOR (READ, at head): the brief\'s R3 anchor `logger.error(context, { error: err instanceof Error ? err.message : String(err) });` (2 leading spaces) occurs %d time(s) at %s; the brief\'s tamper is the un-braced `if (process.env.NODE_ENV === \'production\') logger.error(...)`, the seat\'s armR3.py planted a BRACED variant — same behaviour, different bytes' % (
            sh.count(R3 + '\n'), [i + 1 for i, l in enumerate(hl) if l == R3]))
        out.append('DOCBLOCK-STILL-FALSE (READ): the docblock opens %s — at head %d `message: err.message` 500 lines remain, so "the only place" is still FALSE at part B (declared by the PR body; true only at part C)' % (
            [l.strip() for l in hl if 'KS-1341:' in l][:1], sh.count('message: err.message')))
        pi = [i + 1 for i, l in enumerate(hl) if "webhooksRouter.patch('/:id'" in l]
        pe = [i + 1 for i, l in enumerate(hl) if 'extractPgCode' in l]
        out.append('PATCH-400-BRANCH (READ): PATCH /:id opens at %s; `extractPgCode` referenced at %s (import + the catch\'s SQLSTATE->400 branch ABOVE the converted line); utils/pgErrors.ts at develop reads err.message: %s — a LEAK carrying a known SQLSTATE token is answered 400 and never reaches fail500 (control B0)' % (
            pi, pe, 'message' in show(REAL_DEV, 'Blockchain/Dev/services/originate/src/utils/pgErrors.ts')))
        GB = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1341/golden/'
        def ho(f):
            r = subprocess.run(['git', 'hash-object', '--no-filters', f], capture_output=True, text=True); return r.stdout.strip() if r.returncode == 0 else 'ABSENT'
        gw, gt = ho(GB + 'webhooks.AB.ts'), ho(GB + 'ks1341b-webhooks-500-never-answers-err-message.test.ts')
        out.append('GOLDEN (READ, `git hash-object` of the brief\'s golden files vs the head blobs): webhooks.AB.ts %s vs head %s -> %s; ks1341b test %s vs head %s -> %s; the merge-base webhooks.ts blob %s vs golden webhooks.A.ts %s -> %s' % (
            gw[:12], (blob(h, W) or '-')[:12], 'EXACT' if gw == blob(h, W) else 'DIFFERENT', gt[:12], (blob(h, T) or '-')[:12], 'EXACT' if gt == blob(h, T) else 'DIFFERENT',
            (blob(mb, W) or '-')[:12], ho(GB + 'webhooks.A.ts')[:12], 'EXACT' if ho(GB + 'webhooks.A.ts') == blob(mb, W) else 'DIFFERENT'))
        ts = show(h, T); TL = ts.splitlines()
        loop = [i + 1 for i, l in enumerate(TL) if 'for (const nodeEnv of NODE_ENVS)' in l]; clr = [i + 1 for i, l in enumerate(TL) if 'mockLoggerError.mockClear()' in l]
        out.append('TEST FILE (READ): %d lines; it.each RED families %d x %d routes = %d cells + controls %d; the NODE_ENV loop at %s, `mockLoggerError.mockClear()` at %s (INSIDE the loop: %s); `.at(-1)` occurrences %d; listens on %s; NODE_ENVS %s' % (
            len(TL), len(re.findall(r"it\.each\(ROUTES\)\('RED KS-1341", ts)), len(re.findall(r"^    label: '", ts, re.M)), len(re.findall(r"it\.each\(ROUTES\)\('RED KS-1341", ts)) * len(re.findall(r"^    label: '", ts, re.M)),
            len(re.findall(r"^  it\('control KS-1341", ts, re.M)), loop, clr, bool(loop and clr and loop[0] < clr[0] < loop[0] + 5), ts.count('.at(-1)'), re.findall(r"app\.listen\(0, '([^']+)'", ts), re.findall(r'const NODE_ENVS = (\[[^\]]*\])', ts)))
    if n == '1291':
        C = 'systemTest/performance/runner/cli.ts'; T = 'systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts'
        cd, ch = show(mb, C), show(h, C)
        d = g('diff', '-U0', mb, h, '--', C)
        minus = [l[1:] for l in d.splitlines() if l.startswith('-') and not l.startswith('---')]
        plus = [l[1:] for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
        out.append('PRODUCT DIFF (READ, `git diff -U0` merge-base -> head on cli.ts): `-` %s | `+` %s' % ([x.strip()[:100] for x in minus], [x.strip()[:110] for x in plus]))
        sp = [l.strip() for l in ch.splitlines() if "['tsx', preSuiteStep" in l]
        out.append('SPAWN UNCHANGED (READ): the spawn argv line `[\'tsx\', preSuiteStep, ...]` occurs %d time(s) at merge-base, %d at head, at head line(s) %s, byte-identical: %s' % (
            sum(1 for l in cd.splitlines() if "['tsx', preSuiteStep" in l), len(sp), [i + 1 for i, l in enumerate(ch.splitlines()) if "['tsx', preSuiteStep" in l], [l.strip() for l in cd.splitlines() if "['tsx', preSuiteStep" in l] == sp))
        sweep = {}
        for c_, lab in ((REAL_DEV, 'develop'), (h, 'head')):
            rc, o, _ = gq('grep', '-n', '-E', r'import\.meta\.url\)\.pathname', c_, '--', 'systemTest/')
            sweep[lab] = [':'.join(x.split(':')[1:3]) for x in o.strip().splitlines()] if rc == 0 else []
        rc2, o2, _ = gq('grep', '-n', '-E', r'\.pathname', REAL_DEV, '--', 'systemTest/akto/tests/preSuiteSetup.ts', 'systemTest/playwright/global-setup.ts')
        out.append('NOT-COVERED SWEEP (READ, `git grep -nE "import\\.meta\\.url\\)\\.pathname" -- systemTest/`): develop %s | head %s; `.pathname` in the two named files at develop: %s — the gate grades whether the PR\'s "the other two occurrences … preSuiteSetup.ts:36 and global-setup.ts:42" is TRUE (the ticket\'s DoD 3 says "Measured today: **1** occurrence" — a disagreement to rule on)' % (
            sweep['develop'], sweep['head'], [':'.join(x.split(':')[1:3]) + ' ' + ':'.join(x.split(':')[3:]).strip()[:110] for x in o2.strip().splitlines()] if rc2 == 0 else 'NONE'))
        ts = show(h, T)
        out.append('DOD2-BOUNDARY (READ, the new cell at head): %d lines; `spawn`/`spawnSync`/`execFile`/`execSync`/`fork` occurrences %d; reads cli.ts as TEXT (`readFileSync(`) %d; writes a probe module (`writeFileSync(`) %d; `mkdtemp` %d; the literal `Testing Agent MAIN` %d; imports the probe (`await import(`) %d — the cell never starts the CLI process: the PR\'s "approximated, not met" for DoD 2 is consistent with the READ' % (
            len(ts.splitlines()), len(re.findall(r'\b(spawn|spawnSync|execFile|execFileSync|execSync|exec|fork)\(', ts)), ts.count('readFileSync('), ts.count('writeFileSync('), ts.count('mkdtemp'), ts.count('Testing Agent MAIN'), ts.count('await import(')))
        GD = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1337.golden/KS-1337.golden.diff'
        gres = 'golden diff ABSENT'
        if os.path.exists(GD):
            idx = tempfile.mktemp(prefix='g29gold', dir=os.path.join(SP, 'g29_sp')); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
            run(['git', '--git-dir', CL, 'read-tree', mb], env=e3)
            ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', GD], capture_output=True, text=True, env=e3)
            if ra.returncode == 0:
                gt_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
                gc, gtst = blob(gt_, C), blob(gt_, T)
                ns = g('diff', '--numstat', gt_, h, '--', T).strip()
                gres = 'golden applied (`git apply --cached`, strict) at the merge-base: cli.ts golden %s vs head %s -> %s; test golden %s vs head %s -> %s, golden -> head numstat %s' % (
                    (gc or '-')[:12], (blob(h, C) or '-')[:12], 'EXACT' if gc == blob(h, C) else 'DIFFERENT', (gtst or '-')[:12], (blob(h, T) or '-')[:12], 'EXACT' if gtst == blob(h, T) else 'DIFFERENT', ns.split('\t')[:2] if ns else 'none')
            else: gres = 'golden diff does NOT apply at the merge-base: %s' % ra.stderr.strip()[:200]
        out.append('GOLDEN + FORMATTER DELTA (READ): %s — the PR discloses ONE eslint --fix hunk re-wrapping the writeFileSync call (+9/-6 by its fmt.diff)' % gres)
        pk = show(REAL_DEV, 'systemTest/performance/package.json')
        try: sc = json.loads(pk).get('scripts', {})
        except Exception: sc = {}
        out.append('PACKAGE SCRIPTS (READ, systemTest/performance/package.json at develop): lint `%s`; test:unit `%s`; format:check `%s`' % (sc.get('lint'), sc.get('test:unit'), sc.get('format:check')))
        tc = show(REAL_DEV, 'systemTest/performance/tsconfig.json'); tn = show(REAL_DEV, 'systemTest/performance/tsconfig.node.json'); vc = show(REAL_DEV, 'systemTest/performance/vitest.unit.config.ts')
        sq = lambda x: re.sub(r'\s+', ' ', x)
        out.append('PROGRAMS (READ): tsconfig.json include/exclude %s / %s (EXCLUDES runner and tests); tsconfig.node.json include %s (covers runner/**/*.ts AND tests/**/*.ts — the lint script runs both tsc stages); vitest.unit.config include %s — the gate proves the new cell is in the tsconfig.node.json program (`--listFilesOnly`)' % (
            [sq(x) for x in re.findall(r'"include"\s*:\s*(\[[^\]]*\])', tc)], [sq(x) for x in re.findall(r'"exclude"\s*:\s*(\[[^\]]*\])', tc)], [sq(x) for x in re.findall(r'"include"\s*:\s*(\[[^\]]*\])', tn)], re.findall(r'include\s*:\s*(\[[^\]]*\])', vc)))
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
