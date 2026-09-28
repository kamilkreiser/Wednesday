#!/usr/bin/env python3
"""predict_gate35.py — MEASURE the gate35 kit (the directory this script lives in; its PR set, tiers, classes, commit counts, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate34's predict (gate33 -> gate32 lineage) and re-keyed for gate35: the two rows of Seat B 37th's round, both raised from local-model
READYs under Wednesday's briefs, NEITHER stacked, both on develop 54f37d6399bd — T1: #1321 KS-1348 r3 (originate utils/logger.ts keeps r2's Console
redaction and adds a keepFileFields allow-list on both production File transports + a NEW ks1348 allow-list cell; replaces the CLOSED #1310) and
#1322 KS-888 mint (security index.ts: dbSaveApiKey gets an opt-in { rethrow }; POST /api/keys drops the unsaved key and answers 503 / 500 with no key
material + a NEW ks888 cell; revoke and validate UNCHANGED). Each PR is measured over ITS OWN develop merge-base and merged over the CURRENT develop
(merge-tree with that merge-base). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since,
read by the PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles AND `widen_branch_rx` on branches) is HARD: an
open PR matching either outside this kit refuses.

TIER BY CLASS (kit.json `class`): `logging` / `security` (T1) change EXACTLY ONE product file (no spec row this round).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths: a merged blob DIFFERENT from the head's) and `noop_paths` (the
squash-stack NO-OP: head == merged == develop) are SEPARATE keys; gate35 declares neither, and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
VERIFIED BYTES == USED BYTES (STANDING_LINES 2026-09-27): every READY / golden is read ONCE into memory, its sha256 printed, and those SAME bytes are
compared and applied (written to a scratch file whose sha256 is re-asserted equal at the point of use).
`git apply --check` (STANDING_LINES 2026-09-27, "`patch -F0` is not `git apply --check`"): every golden is verified with `git apply --cached` in a
scratch index seeded from the merge-base tree (strict: no --recount, no fuzz, no -C) — the tool the seat applies with — never with GNU patch.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate35 / Seat B 37th and is checked by rekey_check_gate35.py (which carries its own name in its own token map).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g35_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into
THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout.
The logging row's WIDEN measurement is logprobe_gate35.py (run AFTER this script; its JSON is read here when present).

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate35.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate35.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g35_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate35 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g35/develop']
    + ['+refs/pull/%s/head:refs/g35/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g35/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g35/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g35/pull/' + n).strip() == g('rev-parse', 'refs/g35/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g35idx', dir=os.path.join(SP, 'g35_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE35-SIMULATED-MOVE.txt', 'gate35 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate35 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE35-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate35 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate35 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g35/pull/' + n).strip()
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
    W = os.path.join(SP, 'g35_sp'); fp = tempfile.mktemp(prefix='g35apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16])
    idx = tempfile.mktemp(prefix='g35gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
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
# the READY each PR was raised from, NAMED (never globbed: the 09-27 KS-1348 PRODLOGGERJSON-A / R2-REDACT READYs and the 09-15 Ornith KS-888 READY
# sit in the same directory and are NOT this round's — READ at drafting)
READY = {
 '1321': NIGHT + 'READY_KS-1348-KS-1348-R3_spark-dsv4flash_BRIEFED-CODEPATCH-KS1348-FILE-ALLOWLIST-PASS-7of7_2026-09-28.diff.md',
 '1322': NIGHT + 'READY_KS-888-KS-888-MINT_spark-dsv4flash_BRIEFED-CODEPATCH-KS888-MINT-NO-UNSAVED-KEY-PASS-7of7_2026-09-28.diff.md',
}
# the canonical bytes each PR must equal — the brief-writer's golden (== the Spark checker's patch.diff, byte-identical, READ at drafting) — verified with
# `git apply --cached --check` at the merge-base
GOLDEN = {
 '1321': [BRIEFS + 'KS-1348-r3/KS-1348.golden.diff'],
 '1322': [BRIEFS + 'KS-888-mint/KS-888.golden.diff'],
}
CHECKER = {'1321': 'spark_secuura_2026-09-28_KS-1348-R3', '1322': 'spark_secuura_2026-09-28_KS-888-MINT'}
O = 'Blockchain/Dev/services/originate/src/'
SEC = 'Blockchain/Dev/services/security/src/'
LOGGER, SYSERR, ERRH = O + 'utils/logger.ts', O + 'routes/systemErrors.ts', O + 'middleware/errorHandler.ts'
SECIDX, SECOAS = SEC + 'index.ts', SEC + 'security.openapi.ts'
# the line(s) each red arm is planted at — FROM the brief / the PR body (READ), re-located here by exact WHOLE-LINE match at head, develop and END_TREE
TAMPER = {
 '1321': [(LOGGER, "const FILE_LOG_FIELDS = ['timestamp', 'level', 'service', 'message', 'requestId', 'method', 'path', 'statusCode'];", 69, 'the allow-list (the brief\'s arm: add \'ip\' -> A1 x2 + A3 x2 red, 4 of 11)'),
          (LOGGER, "  if (typeof info.error === 'string') kept.error = info.error;", 76, 'the string-error clause (a gate arm: drop the typeof guard -> a nested Error object reaches the files)'),
          (LOGGER, "    if (key !== 'level' && key !== 'message') copy[key] = redactLogValue(key, copy[key], 0);", 60, 'the Console redaction (the brief\'s arm: `key === \'ks1348-never\'` -> B1 only, 1 of 11)')],
 '1322': [(SECIDX, "      await dbSaveApiKey(apiKey, { rethrow: true });", 1140, 'the mint opts in (the brief\'s arm: drop `{ rethrow: true }` -> A1, A2 x3, A3 red, 5 of 9)'),
          (SECIDX, "      return res.status(infra ? 503 : 500).json({", 1145, 'the status choice (the brief\'s arm: `res.status(500)` -> A2 x3 red, 3 of 9)'),
          (SECIDX, "    if (opts.rethrow) throw err;", 335, 'the opt-in guard (the seat\'s / brief\'s CANDIDATE arm: an unconditional re-throw -> A2 x3, A3, C2 + C3 red, 2 unhandled rejections)'),
          (SECIDX, "      memApiKeys.delete(apiKey.id);", 1142, 'the in-memory drop (a gate arm: remove it -> A3 red, and the unsaved key stays listed / valid in memory)')],
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
LPJ = os.path.join(GS, 'logprobe_gate35.json'); LP = json.load(open(LPJ)) if os.path.exists(LPJ) else None
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []; cls = K['prs'][n].get('class', '?')
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    tests = [p for p in P[n]['paths'] if p not in prod]
    out.append(('PRODUCT files %s (changed +/- lines %s); TEST files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests])) if prod else 'NO product file changed (test-only): every changed path is a test file %s' % [os.path.basename(p) for p in tests])
    hard(K['prs'][n]['tier'] == 'T1' and len(prod) == 1 and not prod[0].endswith('.openapi.ts'), '#%s (T1, class %s) changes exactly ONE runtime product file: %s' % (n, cls, prod))
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
    # NET +/- identity: a golden may re-write an unchanged line as a -/+ pair (KS-888's brief: blank lines as -/+ pairs, which `git diff -U0` of the
    # resulting blobs never shows); cancel identical -X/+X pairs per file before comparing, and print the raw counts beside the net ones
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
    same = rpm == hpm
    mut = {k: list(v) for k, v in hpm.items()}; k0 = sorted(mut)[0]; mut[k0][-1] = mut[k0][-1] + ' '
    ctl = (hpm == hpm and mut != hpm)
    rblock = ('\n'.join(rl).rstrip('\n') + '\n').encode('utf-8')
    gsame = sha256b(rblock) == sha256b(open(GOLDEN[n][0], 'rb').read())
    ck = os.path.join(RUNS, CHECKER[n], 'out.md.checker', 'patch.diff')
    csame = os.path.exists(ck) and sha256b(open(ck, 'rb').read()) == sha256b(open(GOLDEN[n][0], 'rb').read())
    hard(same and ctl and not outside, '#%s == its READY (%s, bytes sha256 %s — read once, these bytes compared): NET +/- lines per file %s (raw %s) vs head %s -> %s; head files OUTSIDE the READY %s (none allowed this round); controls (head vs itself IDENTICAL, a one-token mutation DIFFER): %s' % (
        n, os.path.basename(rp)[:70], rs[:16], {k: len(v) for k, v in rpm.items()}, {k: len(v) for k, v in rpm_raw.items()}, {k: len(v) for k, v in hpm.items()}, cmp_seq(rpm, hpm), outside or 'NONE', ctl))
    out.append('READY IDENTITY (MEASURED, `git diff -U0` merge-base -> head vs the READY block NETTED of identical -/+ pairs (%d cancelled), `l and l[0] in \'+-\'`): %s over %s — the READY block\'s bytes == the golden: %s; the Spark checker\'s patch.diff == the golden: %s — %s' % (
        sum(len(rpm_raw[k]) - len(rpm[k]) for k in rpm), cmp_seq(rpm, hpm), sorted(rpm), gsame, csame, ('the READY\'s closing fence is GLUED to its last diff line %r: stripped as the seat stripped it' % glued[1]) if glued else 'no glued fence'))
    MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_identical': same, 'ready_bytes_eq_golden': gsame, 'checker_eq_golden': csame, 'glued_fence': bool(glued), 'outside_ready': outside}
    # --- GOLDEN: `git apply --cached --check` then apply, STRICT, at the merge-base; the blobs must equal the head's
    gb = open(GOLDEN[n][0], 'rb').read()
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
    svc = K['prs'][n]['service']
    pkg = show(REAL_DEV, 'Blockchain/Dev/' + svc + '/package.json')
    out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r; scripts.lint = %r' % (svc, (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1], (re.search(r'"lint"\s*:\s*"([^"]*)"', pkg) or [None, 'ABSENT'])[1]))
    # --- per-class READ probes
    if cls == 'logging':
        lg = show(h, LOGGER).split('\n')
        fl = [l.strip() for l in lg if l.startswith('const FILE_LOG_FIELDS')]
        fts = [i + 1 for i, l in enumerate(lg) if 'new winston.transports.File(' in l]
        ftf = [i + 1 for i, l in enumerate(lg) if 'new winston.transports.File(' in l and 'format: combine(keepFileFields(), json())' in l]
        cons = [l.strip()[:120] for l in lg if 'new winston.transports.Console(' in l]
        out.append('THE FILE FORMAT (READ, logger.ts at head): %s; File transports at %s, of which carry `format: combine(keepFileFields(), json())`: %s; the Console transport keeps its own format and receives the logger-level `redactSecrets()` output (its suffix matcher is r2\'s, UNCHANGED) %s' % (fl, fts, ftf, cons))
        hard(len(fts) == 2 and ftf == fts, '#%s BOTH production File transports carry the allow-list format (READ: %d File transports, %d with keepFileFields)' % (n, len(fts), len(ftf)))
        # what the files LOSE: metadata keys outside the allow-list in originate's logger calls (single-line grep; READ, a lower bound)
        lost = {}
        for key in ('userId', 'documentId', 'ip', 'stack', 'tenantId', 'organizationId', 'id', 'anchorId', 'pgCode', 'code'):
            rc_, o_, _ = gq('grep', '-n', '-I', '-E', r'logger\.(error|warn|info|debug)\(.*[{,][[:space:]]*%s[[:space:]]*[:,}]' % key, END or REAL_DEV, '--', O, ':!*__tests__*')
            rc2, o2, _ = gq('grep', '-n', '-I', '-E', r'^[[:space:]]*%s[[:space:]]*[:,]' % key, END or REAL_DEV, '--', O, ':!*__tests__*')
            lost[key] = (len([x for x in o_.strip().splitlines() if x]), len([x for x in o2.strip().splitlines() if x]))
        # POSIX classes only: this git's ERE does NOT support \s (MEASURED at drafting: `\s` gave 0 for documentId where [[:space:]] gave 27 — a false zero); the control below must be > 0
        hard(lost['documentId'][0] > 0, 'CONTROL (the grep can find a dropped key): documentId single-line logger-call hits %d > 0 (the brief READ 27)' % lost['documentId'][0])
        out.append('WHAT THE FILES NOW LOSE (READ, `git grep -E` with POSIX classes over originate src on END_TREE, tests excluded; per key (single-line logger calls carrying it, any source line OPENING with it as an object key — the latter over-counts non-log objects)): %s; errorHandler.ts logs `message, statusCode, path, method, userId, ip (+ stack outside production)` — the files keep message / statusCode / path / method, drop userId and ip (the body says so)' % lost)
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r'logger\.(error|warn|info|debug)\(.*error:[[:space:]]*[^,}]*String\((err|error|e)\)', END or REAL_DEV, '--', O, ':!*__tests__*')
        w3 = [x.split(':')[1].split('/')[-1] + ':' + x.split(':')[2] for x in o_.strip().splitlines() if x]
        out.append('W-3 RESIDUE (READ, `git grep` over originate src on END_TREE): %d log call(s) put `error: … String(err)` — a STRING, so it reaches the FILES through the allow-list\'s string-`error` clause (gate33 W-3: an Array\'s elements / a toString value), e.g. %s — the ruled residue (the error text is kept) or a finding for the KS-1346 remainder: the gate rules' % (len(w3), w3[:8]))
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r'(^|[^A-Za-z])(path|requestId)[[:space:]]*:[[:space:]]*req\.(originalUrl|url)([^A-Za-z]|$)', END or REAL_DEV, '--', O, ':!*__tests__*')
        pq = [x.split(':', 1)[1][:150] for x in o_.strip().splitlines() if x]
        rc_, o_, _ = gq('grep', '-n', '-I', '-E', r'(^|[^A-Za-z])path[[:space:]]*:[[:space:]]*req\.path([^A-Za-z]|$)', END or REAL_DEV, '--', O, ':!*__tests__*')
        hard(len([x for x in o_.strip().splitlines() if x]) > 0, 'CONTROL (the carrier grep can find a logged path): `path: req.path` hits %d > 0 (errorHandler.ts, READ)' % len([x for x in o_.strip().splitlines() if x]))
        out.append('ALLOWED-FIELD-AS-CARRIER (READ, `git grep` over originate src on END_TREE): log metadata that sets an allow-listed `path` / `requestId` from `req.originalUrl` / `req.url` (a query string can carry a token): %s' % (pq or 'NONE found'))
        if LP and '_widen' in LP:
            out.append('WIDEN — THE REAL LOGGER, NODE_ENV=production (MEASURED by the drafter, logprobe_gate35.py -> logprobe_1.out): VALUE sentinels reaching a FILE at #%s head %s / END_TREE %s; reaching stdout at the head %s; the message / error text in both files at the head %s; the disclosed loss (userId / documentId / ip / stack absent from the files) %s; controls %s' % (
                n, LP['_widen'].get('head_files'), LP['_widen'].get('end_files'), LP['_widen'].get('head_stdout'), LP['_widen'].get('head_text_kept'), LP['_widen'].get('head_loss'), LP.get('_controls')))
            MEAS[n]['logprobe'] = {'widen': LP.get('_widen'), 'controls': LP.get('_controls')}
        else: out.append('WIDEN — THE REAL LOGGER: logprobe_gate35.json ABSENT — UNMEASURED by the drafter')
    if cls == 'security':
        ix = show(h, SECIDX).split('\n'); ix0 = show(REAL_DEV, SECIDX).split('\n')
        saves = [(i + 1, l.strip()) for i, l in enumerate(ix) if 'dbSaveApiKey(' in l and not l.lstrip().startswith(('async function', '//', '*'))]
        routes = {i + 1: l.split(',')[0] for i, l in enumerate(ix) if re.match(r"^app\.(get|post|put|patch|delete)\('/api/keys", l)}
        def route_of(ln): return [v for k, v in sorted(routes.items()) if k <= ln][-1:] or ['?']
        out.append('dbSaveApiKey CALL SITES (READ, security index.ts at head): %s — ONLY the mint opts in; revoke (app.delete) and validate keep the log-only swallow (the handlers take no `next`)' % [(ln, route_of(ln)[0], 'rethrow' in s) for ln, s in saves])
        hard(sum(1 for ln, s in saves if 'rethrow: true' in s) == 1 and all(route_of(ln)[0].startswith("app.post('/api/keys'") for ln, s in saves if 'rethrow: true' in s), '#%s exactly ONE dbSaveApiKey call opts in to rethrow, inside POST /api/keys (READ)' % n)
        mint = [i + 1 for i, l in enumerate(ix) if l.startswith("app.post('/api/keys',")]
        sv = [ln for ln, s in saves if 'rethrow: true' in s]; rv = [i + 1 for i, l in enumerate(ix) if 'await revokePriorConnectorKeys(' in l]
        dl = [i + 1 for i, l in enumerate(ix) if 'memApiKeys.delete(apiKey.id)' in l]
        out.append('THE KS-577 ORDER (READ, index.ts at head): the mint at %s saves (with rethrow) at %s, drops the in-memory copy at %s and RETURNS 503/500 before the rotate revoke at %s — a failed save never revokes the prior key (mint first, then revoke, preserved: %s)' % (mint, sv, dl, rv, bool(sv and rv and dl and sv[0] < dl[0] < rv[0])))
        mem = [i + 1 for i, l in enumerate(ix) if l.strip() == 'if (!isDbAvailable()) return;']
        out.append('THE MEMORY-ONLY MINT (READ): dbSaveApiKey sets memApiKeys FIRST (:%s) and returns before the INSERT when `!isDbAvailable()` (%s) — no throw, so the no-database mint still answers 201 from memory (C4)' % (
            [i + 1 for i, l in enumerate(ix) if l.strip() == 'memApiKeys.set(k.id, k);'], mem[:4]))
        rx = [l.strip()[:230] for l in ix if l.strip().startswith('const infra =')]
        out.append('THE INFRA CLASSIFIER (READ, index.ts at head): %s — codes by PREFIX 08 / 53 / 57 (SQLSTATE classes), socket codes by whole value, five message phrases; the gate drives each class and a non-infra code (42703 -> 500), and says whether `String(saveErr?.code)` for a numeric or absent code behaves' % rx)
        oa = show(h, SECOAS).split('\n')
        reg = [i for i, l in enumerate(oa) if "path: '/api/security/keys'" in l]
        post_reg = [i for i in reg if i >= 1 and "method: 'post'" in oa[i - 1]]
        d503 = [j + 1 for j in range(post_reg[0], post_reg[0] + 30) if post_reg and '503: commonErrorResponses[503]' in oa[j]][:1] if post_reg else []
        out.append('SPEC-503-DECLARED (READ, security.openapi.ts at head): POST /api/security/keys registered at %s; a 503 response is ALREADY declared at %s (commonErrorResponses) — the PR body\'s NOT-COVERED line "the newly reachable 503 is not declared in the spec" is a PREDICTION SLIP as READ; the gate runs `npm run check:openapi` to settle it' % ([i + 1 for i in post_reg], d503 or 'NOT FOUND'))
        MEAS[n]['spec_503_declared_line'] = d503
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
