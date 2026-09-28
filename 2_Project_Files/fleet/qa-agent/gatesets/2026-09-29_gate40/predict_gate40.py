#!/usr/bin/env python3
"""predict_gate40.py — MEASURE the gate40 kit (the directory this script lives in; its PR set, tier, class, commit count, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate39's predict (gate38 -> gate37 lineage) and re-keyed for gate40: ONE row of Seat B 42nd's queue, T1 — #1338 KS-1370 both halves
(security-validate: services/security validate answers on the STORED revoke through the SECURITY DEFINER carve-out security_find_api_key_by_hash on a
cache HIT, sticky both ways, a vanished row evicted, a failed stored read with a database configured answers 503, memory-only mode answers from memory;
the usage write becomes the usage-only dbRecordApiKeyUsage UPDATE; #1334's KS 888 validate cells re-pinned). Measured over ITS develop merge-base
(develop 0de108577e61 itself at drafting) and merged over the CURRENT develop. No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin
(kit.json `inflight` PLUS any PR opened since, read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles
AND `widen_branch_rx` on branches — Seat B 42nd's `-b42-<n>`) is HARD: an open PR matching either outside this kit refuses.
TIER BY CLASS (kit.json `class`): `security-validate` (T1) changes EXACTLY services/security/src/index.ts and two test files (ks1370 new, ks888 re-pinned).
STANDING REQUIREMENTS: the CROSS-PACKAGE CENSUS — for every changed file, `git grep -l` of its file name and `<parent>/<stem>` over every *.test.ts /
*.test.js / *.test.sh / __tests__/*.sh in Blockchain/Dev at the head (the KS 764 revoke call-site guard in packages/shared READS security index.ts:
it is named here) — the gate runs EVERY suite so named. #1338's real-Postgres behaviour AS A NON-SUPERUSER APPLICATION ROLE is MEASURED by
pgprobe_gate40.py (run AFTER this script; its JSON is read here when present).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths) and `noop_paths` are SEPARATE keys; gate40 declares neither,
and (c) asserts that none is needed.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate40 / Seat B 42nd and is checked by rekey_check_gate40.py (which carries its own name in its own token map, and gate39's namespace too).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g40_sp/clone.git — `git clone --bare --shared
--no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's
core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout. The scratchpad MUST be on the
Data volume (/private/tmp/...): /Volumes/DevMASTER is full.

BASE-INVARIANT over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY; disjoint from every other open PR. READ probes (PREDICTIONS for the
gate, never evidence) are printed. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate40.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib, http.client

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate40.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g40_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate40 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g40/develop']
    + ['+refs/pull/%s/head:refs/g40/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g40/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g40/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g40/pull/' + n).strip() == g('rev-parse', 'refs/g40/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g40idx', dir=os.path.join(SP, 'g40_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE40-SIMULATED-MOVE.txt', 'gate40 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate40 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE40-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate40 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate40 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g40/pull/' + n).strip()
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
SECIDX = 'Blockchain/Dev/services/security/src/index.ts'
T1370 = 'Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts'
T888 = 'Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts'
KS764 = 'Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts'
GWAUTH = 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
M039 = 'Blockchain/Dev/migrations/039_rls_fail_closed.sql'
SMIG = 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts'
TIER_OF = {'security-validate': 'T1'}
DECL = {'security-validate': {'prod': [SECIDX], 'doc': [], 'tests': sorted([T1370, T888])}}
# the lines each red arm is planted at (WHOLE-LINE match, located at head; a 5th field is the PREDECESSOR line for a two-line anchor)
TAMPER = {'1338': [
 (SECIDX, '      if (revokedInMemory) apiKey.isActive = false;', 'design call (a) STICKY REVOKE: delete it -> the cached-revoked / stored-active arm (KS-888 R2) must answer valid (the arm the gate owes)'),
 (SECIDX, '        memApiKeys.delete(apiKey.id);', 'design call (b) EVICTION of a vanished row: delete it -> the entry survives the Key not found answer', '      if (storedResult.rows.length === 0) {'),
 (SECIDX, '  if (apiKey && isDbAvailable()) {', "half (ii)'s guard: `false &&` neutralises half (ii) (the seat's W arm: half (i) alone must still keep the row revoked)"),
 (SECIDX, '  await dbRecordApiKeyUsage(apiKey);', "half (i)'s call site: put `dbSaveApiKey(apiKey)` back with half (ii) off -> the revoke is REVIVED (the seat's W4)"),
 (SECIDX, '      return res.status(503).json({', "Kam's split, limb 1: the 503 on a failed stored read"),
 (SECIDX, '      `UPDATE svc_api_keys SET last_used_at = $2, usage_count = $3 WHERE id = $1`,', 'the usage-only statement (names neither is_active nor INSERT)'),
 (SECIDX, '         is_active = EXCLUDED.is_active,', 'the SHARED upsert KEEPS is_active (revoke persists through it; the KS 764 guard pins that shape)'),
 (SECIDX, '  apiKey.isActive = false;', 'the revoke flip (UNCHANGED by this PR — the KS 764 guard reads it)'),
]}
BASE_ANCHOR = (SECIDX, '  await dbSaveApiKey(apiKey);', "validate's usage write at the BASE (the shared upsert: the revive)")
def locate(c, p, line, prev=None):
    if not c: return []
    L = show(c, p).split('\n'); return [i + 1 for i, l in enumerate(L) if l == line and (prev is None or (i > 0 and L[i - 1] == prev))]
def its(s): return re.findall(r"^\s*it(?:\.each\([^)]*\))?\(\s*'([^']{0,140})", s, re.M)
def grep_l(rev, frag, *globs):
    rc_, o_, _ = gq('grep', '-l', '-F', frag, rev, '--', *globs); return sorted(x.split(':', 1)[1] for x in o_.strip().splitlines() if x)
def census(h, own):
    rows = {}
    for p in own:
        b = os.path.basename(p); stem = b.rsplit('.', 1)[0]; par = os.path.basename(os.path.dirname(p)) or '.'
        hits = set()
        frags = (b, par + '/' + stem) if b != 'index.ts' else ('security/src/index', "'security', 'src', 'index.ts'", '"security", "src", "index.ts"', 'services/security/src/index.ts')
        for frag in frags:
            for f in grep_l(h, frag, 'Blockchain/Dev/*.test.ts', 'Blockchain/Dev/*.test.js', 'Blockchain/Dev/*.test.sh', 'Blockchain/Dev/*/__tests__/*.sh'):
                if f != p: hits.add(f)
        rows[p] = sorted(hits)
    return rows
def pkg_of(f):
    m = re.match(r'Blockchain/Dev/((services|packages)/[^/]+)/', f)
    return m.group(1) if m else ('/'.join(f.split('/')[:3]) if f.startswith('Blockchain/Dev/') else f.split('/')[0])
def func_text(src, start_rx):
    m = re.search(start_rx, src, re.M)
    if not m: return None
    i = m.start(); j = src.find('\n}\n', i); return src[i:j + 3] if j > 0 else None
CTL_PM = (cmp_seq(pm(['+a', '-b', '+c', '']), pm(['+a', '-b', '+c'])) == 'IDENTICAL' and cmp_seq(pm(['+a', '-b', '+c']), pm(['+a', '-b', '+C'])) == 'DIFFER' and len([l for l in ['+a', ''] if l[:1] in '+-']) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, "CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in '+-'` would have counted the empty line — the kit uses `l and l[0] in '+-'`")
PGJ = os.path.join(GS, 'pgprobe_gate40.json'); PG = json.load(open(PGJ)) if os.path.exists(PGJ) else None
PROBES, MEAS = {}, {}
for n in NS:
    h = H[n]; cb = P[n]['merge_base']; cls = K['prs'][n]['class']; out = []; MEAS[n] = {}
    d = DECL[cls]
    hard(sorted(P[n]['paths']) == sorted(d['prod'] + d['doc'] + d['tests']) and TIER_OF[cls] == K['prs'][n]['tier'],
         '#%s TIER BY CLASS %s (%s): changes EXACTLY %s' % (n, cls, TIER_OF[cls], [os.path.basename(x) for x in sorted(d['prod'] + d['tests'])]))
    sb, sh_ = show(cb, SECIDX), show(h, SECIDX)
    for t in TAMPER[n]:
        at_h = locate(h, t[0], t[1], t[3] if len(t) > 3 else None); at_b = locate(cb, t[0], t[1], t[3] if len(t) > 3 else None)
        hard(len(at_h) == 1 or t[1] in ('  apiKey.isActive = false;', '         is_active = EXCLUDED.is_active,'), '#%s ANCHOR %r at head %s (base %s) — %s' % (n, t[1].strip()[:70], at_h, at_b, t[2]))
        out.append('ANCHOR %s :%s (base :%s) `%s` — %s' % (os.path.basename(t[0]), at_h, at_b, t[1].strip()[:90], t[2]))
    bb = locate(cb, BASE_ANCHOR[0], BASE_ANCHOR[1]); bh = locate(h, BASE_ANCHOR[0], BASE_ANCHOR[1])
    out.append('BASE ANCHOR `%s` at base :%s, at head :%s — %s (the RED arm at base; at head the call site is dbRecordApiKeyUsage)' % (BASE_ANCHOR[1].strip(), bb, bh, BASE_ANCHOR[2]))
    # the revoke path is UNCHANGED: dbSaveApiKey's whole body and the revoke route are byte-identical base -> head
    fb, fh = func_text(sb, r'^async function dbSaveApiKey\('), func_text(sh_, r'^async function dbSaveApiKey\(')
    hard(fb is not None and fb == fh and 'is_active = EXCLUDED.is_active' in (fh or ''), '#%s dbSaveApiKey is BYTE-IDENTICAL base -> head (%d bytes) and still carries `is_active = EXCLUDED.is_active` (revoke persists through it)' % (n, len(fh or '')))
    rb = re.search(r"app\.delete\('/api/keys/:id'.*?\n\}\);\n", sb, re.S); rh = re.search(r"app\.delete\('/api/keys/:id'.*?\n\}\);\n", sh_, re.S)
    hard(bool(rb) and bool(rh) and rb.group(0) == rh.group(0), '#%s the REVOKE route (DELETE /api/keys/:id) is BYTE-IDENTICAL base -> head (%s bytes)' % (n, len(rh.group(0)) if rh else None))
    hunks = [l for l in g('diff', '-U0', cb, h, '--', SECIDX).splitlines() if l.startswith('@@')]
    out.append('index.ts HUNKS (READ, `git diff -U0`): %s' % hunks)
    # the new validate body, READ: the stored read, the sticky combine, the eviction, the 503, the isDbAvailable() split
    vb = re.search(r"app\.post\('/api/keys/validate'.*?\n\}\);\n", sh_, re.S); v = vb.group(0) if vb else ''
    facts = {'stored read on a cache hit via the carve-out': "if (apiKey && isDbAvailable()) {" in v and v.count("security_find_api_key_by_hash($1)") == 2,
             'sticky: revokedInMemory captured BEFORE the refresh and re-applied': v.find('const revokedInMemory = apiKey.isActive === false;') < v.find('apiKey = rowToApiKey(storedResult.rows[0]);') < v.find('if (revokedInMemory) apiKey.isActive = false;'),
             'vanished row: evict + Key not found': "memApiKeys.delete(apiKey.id);\n        return res.json({ success: true, data: { valid: false, reason: 'Key not found' } });" in v,
             "failed read: 503 SERVICE_UNAVAILABLE 'Unable to verify key'": "res.status(503)" in v and "'Unable to verify key'" in v and "SERVICE_UNAVAILABLE" in v,
             'usage write: dbRecordApiKeyUsage, never dbSaveApiKey, in validate': 'await dbRecordApiKeyUsage(apiKey);' in v and 'dbSaveApiKey(' not in v.replace('dbSaveApiKey would', ''),
             'the cache-MISS branch unchanged (warn, then Key not found on a failed read)': "logger.warn('DB fallback for api-key validation failed'" in v}
    hard(all(facts.values()), '#%s THE NEW VALIDATE (READ): %s' % (n, facts))
    ru = func_text(sh_, r'^async function dbRecordApiKeyUsage\(') or ''
    ufacts = {'UPDATE only (no INSERT, no is_active in SQL)': 'UPDATE svc_api_keys SET last_used_at = $2, usage_count = $3 WHERE id = $1' in ru and 'INSERT' not in ru.split('async function')[1] and 'is_active' not in re.sub(r'//.*', '', ru),
              'tenant GUC pinned (runWithTenantId(k.tenantId, …))': 'runWithTenantId(k.tenantId' in ru,
              "logged, never rethrown, message byte-identical to dbSaveApiKey's": "logger.error('DB save API key failed', { error: err?.message });" in ru and 'throw' not in re.sub(r'//.*', '', ru),
              'memApiKeys.set first; memory-only returns before SQL': ru.find('memApiKeys.set(k.id, k);') < ru.find('if (!isDbAvailable()) return;') < ru.find('UPDATE svc_api_keys')}
    hard(all(ufacts.values()), '#%s dbRecordApiKeyUsage (READ): %s' % (n, ufacts))
    out.append('NOTE (READ, for the gate to MEASURE): an UPDATE that the tenant_isolation policy filters to ZERO rows does NOT throw — a GUC mismatch would lose the usage count SILENTLY (rowCount is never read); the drafter measured the usage count moving 0 -> 1 as secuura_app (pgprobe U2 / R1). The stale-copy LOST UPDATE (usage_count written from a stale value) is the seat\'s own candidate, not fixed, not filed')
    # the KS 764 guard, EMULATED on head's index.ts (its revoke patterns READ from the guard file at the pinned develop, never typed)
    gsrc = show(DEV, KS764); pats = re.findall(r'revokeWrite: /(.*)/([a-z]*),\s*$', gsrc, re.M)
    em = {}
    for src_, fl in pats:
        rx = re.compile(src_, re.M if 'm' in fl else 0)
        em[src_[:40]] = (len(rx.findall(sb)), len(rx.findall(sh_)))
    hard(bool(pats) and all(b_ >= 1 and h_ == b_ for b_, h_ in em.values()), '#%s KS 764 guard revoke patterns over security index.ts (EMULATED, READ; base, head): %s — the revoke shape the guard pins is unchanged' % (n, em))
    # #1334's re-pin in ks888: which declarations' TEXT changed (READ) — the gate owes the RED set (5 declarations / 7 cases per the seat) by RUNNING
    t888h = show(h, T888).split('\n'); ch = []
    for l in g('diff', '-U0', cb, h, '--', T888).splitlines():
        m = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', l)
        if m:
            s0 = int(m.group(1)); decl = 'TOP-LEVEL (the mock / state)'
            for i in range(s0 - 1, -1, -1):
                mm = re.match(r"^\s*it(?:\.each\(\w+\))?\(\s*'([^']{0,70})", t888h[i]) if i < len(t888h) else None
                if mm: decl = mm.group(1); break
                if re.match(r'^describe\(|^const |^vi\.mock', t888h[i] if i < len(t888h) else ''): break
            ch.append('+%s: %s' % (s0, decl))
    pmd = pm_diff(cb, h, T888)
    out.append("#1334's RE-PIN in ks888 (READ): %d `-` / %d `+` lines; hunks by declaration %s; declarations at base %d, at head %d (it.each over INFRA = %d cases each). The seat: 5 declarations = 7 executed cases went red on the fix — only the ones listed here had TEXT edits; the rest went green by the MOCK change alone: the gate runs the BASE ks888 file against the HEAD product to name the red set, and reads each changed line: fixture more faithful, or a pin weakened" % (
        len([l for l in pmd if l[0] == '-']), len([l for l in pmd if l[0] == '+']), ch, len(its(show(cb, T888))), len(its(show(h, T888))), len(re.findall(r"^  \['", show(h, T888), re.M))))
    out.append('ks1370 CELLS (READ, head): %s' % its(show(h, T1370)))
    # the cross-package census
    cz = census(h, P[n]['paths'])
    out.append('CROSS-PACKAGE CENSUS (READ, `git grep -l -F` over Blockchain/Dev at head; fragments = file name and <parent>/<stem>, for index.ts the path spellings; globs *.test.ts *.test.js *.test.sh __tests__/*.sh): %s — the suites the gate RUNS: %s' % (
        {os.path.basename(k): v for k, v in cz.items()}, sorted({pkg_of(f) for v in cz.values() for f in v} | {'services/security'})))
    hard(KS764 in cz.get(SECIDX, []), '#%s the census finds the packages/shared KS 764 revoke call-site guard as a reader of security index.ts' % n)
    # the gateway's refusal cache (READ at the pinned develop; api-gateway is not changed by this PR)
    ga = show(DEV, GWAUTH).split('\n')
    c30 = [i + 1 for i, l in enumerate(ga) if 'expiresAt: Date.now() + 30_000' in l]; c60 = [i + 1 for i, l in enumerate(ga) if 'expiresAt: Date.now() + 60_000' in l]
    nok = [i + 1 for i, l in enumerate(ga) if 'if (!resp.ok) {' in l]; cb8 = [i + 1 for i, l in enumerate(ga) if l.startswith('const CONNECTOR_BEARER_CACHE_MS')]
    out.append('GATEWAY REFUSAL CACHE (READ, api-gateway middleware/auth.ts at develop): `if (!resp.ok)` :%s and `!data?.valid` both cache null for 30 s at :%s; a VALID answer is cached 60 s at :%s; the connector bearer is cached up to 8 min at :%s. So END TO END (a PREDICTION): a security-DB fault on a cache-HIT key now answers 503 -> the gateway caches a refusal 30 s -> the caller gets 401 Invalid API key for the fault + up to 30 s; a key whose VALID answer the gateway cached in the last 60 s keeps working until that entry expires (a revoke also takes up to 60 s + 8 min of bearer cache to bite through the gateway, unchanged by this PR); a cache-MISS key answered Key not found (valid:false, also cached 30 s) BEFORE and AFTER this PR; memory-only security never 503s' % (nok, c30, c60, cb8))
    # the premise, READ: 039's carve-out and the provisioning grant
    m39 = show(DEV, M039).split('\n'); sm = show(DEV, SMIG).split('\n')
    out.append('THE PREMISE (READ, develop): 039 creates security_find_api_key_by_hash SECURITY DEFINER at :%s, the permissive svc_api_keys_auth_lookup policy FOR SELECT TO secuura_auth_lookup at :%s, owner -> secuura_auth_lookup and GRANT EXECUTE to secuura_app ONLY IF the role exists at :%s; the gateway provisions secuura_app (NOSUPERUSER NOINHERIT NOBYPASSRLS) AFTER the migrations and grants EXECUTE ON ALL FUNCTIONS at startup-migrations.ts :%s — so on a fresh database the function EXECUTE for secuura_app comes from the gateway grant, not from 039 (measured by pgprobe P rows)' % (
        [i + 1 for i, l in enumerate(m39) if l.startswith('CREATE OR REPLACE FUNCTION security_find_api_key_by_hash')], [i + 1 for i, l in enumerate(m39) if 'CREATE POLICY svc_api_keys_auth_lookup' in l],
        [i + 1 for i, l in enumerate(m39) if 'GRANT EXECUTE ON FUNCTION %s TO secuura_app' in l], [i + 1 for i, l in enumerate(sm) if 'GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO secuura_app' in l]))
    # Kam's two cards (READ only)
    try:
        dj = json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json', encoding='utf-8')); found = {}
        def walk(x):
            if isinstance(x, dict):
                if x.get('id') in ('secuura-ks1370-revoke-undone-by-stale-process', 'secuura-ks1370-validate-when-the-revoke-check-cannot-read', 'secuura-ks888-validate-usage-write-failure'):
                    found[x['id']] = '%s %s at %s' % (x.get('status'), x.get('ruled_choice'), x.get('ruled_ts'))
                for vv in x.values(): walk(vv)
            elif isinstance(x, list):
                for vv in x: walk(vv)
        walk(dj)
    except Exception as e: found = {'READ FAILED': str(e)[:80]}
    hard(found.get('secuura-ks1370-revoke-undone-by-stale-process', '').startswith('ruled a') and found.get('secuura-ks1370-validate-when-the-revoke-check-cannot-read', '').startswith('ruled a'),
         "#%s Kam's cards (READ, decisions.json): %s" % (n, found))
    if PG and '_summary' in PG:
        out.append('THE POSTGRES (MEASURED by the drafter AS secuura_app, pgprobe_gate40.py -> pgprobe_1.out / pgprobe_gate40.json, %s): %s — the gate re-measures and RULES' % (PG.get('engine', '?')[:40], PG['_summary']))
        MEAS[n]['pgprobe'] = {'summary': PG['_summary']}
    else: out.append('THE POSTGRES: pgprobe_gate40.json ABSENT — UNMEASURED by the drafter')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))
ORDER_PROOF = {}
res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT, 'merge_bases': MB,
       'end_tree': END, 'end_tree_with_sibling': None, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES, 'measured': MEAS,
       'stacks': ST, 'retarget': RT, 'declared_overlap': DOV, 'noop_paths': NOOP, 'sibling_paths': {}, 'sibling_heads': {},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': {}, 'dead_open_declared': {},
       'titles': {n: AP[n]['title'] for n in NS}, 'merge_order': K['merge_order'], 'order_proof': ORDER_PROOF}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | merge-bases %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, [m[:12] for m in MB]))
sys.exit(1 if FAIL else 0)
