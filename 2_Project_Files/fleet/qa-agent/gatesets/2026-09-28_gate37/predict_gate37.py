#!/usr/bin/env python3
"""predict_gate37.py — MEASURE the gate37 kit (the directory this script lives in; its PR set, tiers, classes, commit counts, declared stacks (NONE),
declared overlaps (NONE) and declared no-op paths (NONE) are kit.json beside it) over origin develop AS READ NOW, and write pins_<kit>.json beside this
script. Never adopts a value from a mail or from kit.json (kit.json carries NO head): every head is read from origin by TWO instruments — `git ls-remote`
(READ, from the Secuura checkout) and the GitHub PULLS API — and the fetch into the scratch clone must agree with both.

Shape copied from gate36's predict (gate35 -> gate34 lineage) and re-keyed for gate37: the two rows of Seat B 39th's round, NONE stacked, both on develop
63db8a38354c — T1 x2: #1327 KS-888 REVOKE (security index.ts: DELETE /api/keys/:id opts into dbSaveApiKey's rethrow inside its own try; a failed save
answers 503 (infrastructure, the mint's classifier) or 500 (other) and KEEPS the in-memory revoke; mint and validate unchanged; a Spark golden, applied
by section, plus TWO HAND-WRITTEN rewordings in the existing ks888 cell file — header :5-7 and describe :98 — so every fullName in that file changes)
and #1328 KS-1335 (m365-integration: the notify window rotates on a NEW nullable `last_attempted_at`, added at all three DDL sites — docker init 06, the
CORE_MIGRATIONS CREATE, the guarded information_schema add-column block — stamped ONCE after the deadline guard and before safeOutboundRequest; the
DEADLINE-SKIPPED row is NOT stamped; seat-written). Each PR is measured over ITS OWN develop merge-base and merged over the CURRENT develop (merge-tree
with that merge-base). No sibling kit. The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight` PLUS any PR opened since, read by the
PULLS API every run): hard path-disjoint. The WIDEN census (kit.json `widen_rx` on titles AND `widen_branch_rx` on branches) is HARD: an open PR
matching either outside this kit refuses.

TIER BY CLASS (kit.json `class`): `key-revocation` (T1) changes EXACTLY ONE runtime product file (security index.ts) and one test file;
`schema-migration` (T1) changes EXACTLY the three declared product files (docker init 06, api-gateway startup-migrations.ts, m365-integration
index.ts) and one test file. #1328's real-Postgres behaviour is MEASURED by pgprobe_gate37.py (run AFTER this script; its JSON is read here when present).
DECLARATIONS (STANDING_LINES 2026-09-27): kit.json `declared_overlap` (merged_blob_paths: a merged blob DIFFERENT from the head's) and `noop_paths` (the
squash-stack NO-OP: head == merged == develop) are SEPARATE keys; gate37 declares neither, and (c) asserts that no pair needs one.
UNFETCHED OBJECTS (STANDING_LINES 2026-09-27): blob() asserts `cat-file -e <commit-or-tree>^{tree}` FIRST (a missing commit is a hard FAIL, never "a
different blob") and accepts only a 40-hex answer whose `cat-file -t` is `blob`; a control in (a) proves the guard fires on a sha the clone does not hold.
VERIFIED BYTES == USED BYTES (STANDING_LINES 2026-09-27): every READY / golden is read ONCE into memory, its sha256 printed, and those SAME bytes are
compared and applied (written to a scratch file whose sha256 is re-asserted equal at the point of use).
`git apply --check` (STANDING_LINES 2026-09-27, "`patch -F0` is not `git apply --check`"): the golden is verified with `git apply --cached` in a
scratch index seeded from the merge-base tree (strict: no --recount, no fuzz, no -C) — the tool the seat applies with — never with GNU patch.
Every +/- comparator tests `l and l[0] in '+-'` (never `l[:1] in '+-'`) and carries a control pair (identical -> IDENTICAL, one token -> DIFFER).
COPIED TOOLS ARE KEYED TO THEIR AUTHOR (STANDING_LINES 2026-09-28): every seat-, pane-, generation-, folder- and path-keyed constant here was re-derived
for gate37 / Seat B 39th and is checked by rekey_check_gate37.py (which carries its own name in its own token map).
ONE ROW HAS A READY (#1327: the Spark's KS-888-REVOKE READY == the brief's golden == the checker's patch.diff); the head carries the golden PLUS a
DECLARED hand-written set (HANDWRITTEN below: the header :5-7 and the describe :98) — the golden's strict apply must give the head's blob for the
product file EXACTLY, and diff(golden-applied, head) must be EXACTLY the declared hand-written lines, nothing more. #1328 has NO READY (seat-written).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
read-tree/update-index/write-tree/commit-tree for a simulation, apply --cached for a golden) runs in a scratch BARE clone <scratchpad>/g37_sp/clone.git —
`git clone --bare --shared --no-checkout` FROM the checkout (objects BORROWED read-only through objects/info/alternates), then a fetch FROM ORIGIN into
THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over its develop merge-base, NO merge commit; (1)
diff(develop, merged) == EXACTLY the PR's own paths, each merged blob byte-equal to the head's blob; (2) numstat(develop -> merged) == numstat(merge-base
-> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. PAIRWISE the kit's path sets are DISJOINT and NOT stacked, and disjoint
from every other open PR. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR. REFUSES (rc 1) unless every HARD assertion holds.
--simulate foreign<n> builds develop + a FOREIGN edit of that PR's first own file and must REFUSE; --simulate moved builds develop + an UNRELATED
synthetic commit and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate37.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time, hashlib, difflib

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate37.py <scratchpad> [--simulate …]'); sys.exit(9)
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
CL = os.path.join(SP, 'g37_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
def sha256b(b): return hashlib.sha256(b).hexdigest()
print('predict_gate37 (%s) %s | simulation %s | scratchpad %s | stacks %s | declared_overlap %s | noop_paths %s' % (K['kit'], now(), SIM, SP, ST or 'NONE', DOV or 'NONE', NOOP or 'NONE'))

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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g37/develop']
    + ['+refs/pull/%s/head:refs/g37/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g37/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g37/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g37/pull/' + n).strip() == g('rev-parse', 'refs/g37/branch/' + n).strip(),
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
    idx = tempfile.mktemp(prefix='g37idx', dir=os.path.join(SP, 'g37_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', parent], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    return run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', parent, '-m', msg], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
if SIM == 'moved':
    DEV = synth(DEV, 'GATE37-SIMULATED-MOVE.txt', 'gate37 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n', 'gate37 SIMULATION moved')
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE37-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    base0 = H[ST[tn]] if tn in ST else g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', base0, H[tn]).split())[0]
    rc, blb, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blb.strip()) if rc == 0 else ''
    DEV = synth(DEV, path, body + '\n# gate37 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM, 'gate37 SIMULATION ' + SIM)
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
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g37/pull/' + n).strip()
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
    """split a unified diff into [[header lines + body]] by '--- ' / '+++ ' header pairs"""
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
    written are the bytes verified (sha256 at the point of use). Returns ({path: blob} or None, message, tree or None)."""
    W = os.path.join(SP, 'g37_sp'); fp = tempfile.mktemp(prefix='g37apply_%s_' % tag, suffix='.diff', dir=W)
    open(fp, 'wb').write(diffbytes)
    used = sha256b(open(fp, 'rb').read())
    if used != sha_expected: return None, 'USED-BYTES MISMATCH: wrote %s, verified %s' % (used[:16], sha_expected[:16]), None
    idx = tempfile.mktemp(prefix='g37gold', dir=W); e3 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', base], env=e3)
    rchk = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', '--check', fp], capture_output=True, text=True, env=e3)
    if rchk.returncode != 0: return None, '`git apply --cached --check` REFUSES at %s (rc %d): %s [bytes used sha256 %s == verified]' % (base[:12], rchk.returncode, rchk.stderr.strip()[:220].replace('\n', ' / '), used[:16]), None
    ra = subprocess.run(['git', '--git-dir', CL, 'apply', '--cached', fp], capture_output=True, text=True, env=e3)
    if ra.returncode != 0: return None, 'apply rc %d after a passing --check: %s' % (ra.returncode, ra.stderr.strip()[:160]), None
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e3).strip()
    return {p: blob(t_, p) for p in paths}, '`git apply --cached --check` rc 0 and apply rc 0 at %s (strict) [bytes used sha256 %s == verified]' % (base[:12], used[:16]), t_
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
def net(ls):
    """cancel identical -x/+x pairs (a golden may carry an unchanged line as a -/+ pair that `git diff -U0` never shows: the brief's +29/-4 vs git's +28/-3)"""
    ls = list(ls); out_ = []
    for l in ls:
        if l[0] == '-' and ('+' + l[1:]) in ls[ls.index(l):]: continue
        out_.append(l)
    for l in [x for x in ls if x[0] == '-' and ('+' + x[1:]) in ls[ls.index(x):]]:
        out_.remove('+' + l[1:])
    return out_
NIGHT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
BRIEFS = NIGHT + 'briefs/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
# the READY each PR was raised from, NAMED (never globbed: the 09-15 Ornith KS-888 READY and the 09-28 KS-888-MINT READY sit in the same directory and are
# NOT this round's); None = no READY (#1328 was written by the seat)
READY = {
 '1327': NIGHT + 'READY_KS-888-REVOKE_spark-dsv4flash_BRIEFED-CODEPATCH-KS888-REVOKE-FAILED-SAVE-503-PASS-7of7_2026-09-28.diff.md',
 '1328': None,
}
GOLDEN = {'1327': [BRIEFS + 'KS-888-revoke/KS-888.golden.diff']}
CHECKER = {'1327': 'spark_secuura_2026-09-28_KS-888-REVOKE'}
SEC = 'Blockchain/Dev/services/security/src/'
IDX, KT = SEC + 'index.ts', SEC + '__tests__/ks888-failed-mint-save-issues-no-key.test.ts'
M3 = 'Blockchain/Dev/services/m365-integration/src/'
MIDX, NT = M3 + 'index.ts', M3 + '__tests__/ks934-teams-notify-request-path-bound.test.ts'
SMIG, INIT = 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts', 'Blockchain/Dev/docker/init/06-m365-tables.sql'
# THE DECLARED HAND-WRITTEN LINES of #1327 (the PR body's "The two hand-written edits", READ): the head's ks888 test file carries them ON TOP of the golden.
# diff(golden applied at the merge-base, head) must be EXACTLY these four `+` lines (and their four `-` predecessors, each a merge-base line)
HANDWRITTEN = {'1327': {KT: [
 "+// 500, and neither carries a key. This file covers the MINT and REVOKE routes. Validate keeps the swallow:",
 "+// its handler takes no next, so a throw from dbSaveApiKey there is an unhandled rejection (measured by the",
 "+// KS-888 r2 brief-writer). Control C3 pins that it still answers 200 while the same INSERT fails.",
 "+describe('KS-888: a mint whose save fails issues no key; validate is unchanged', () => {"]}}
# the line(s) each red arm is planted at — FROM the PR body's arms (READ), re-located here by exact WHOLE-LINE match at head, develop and END_TREE. A 4th
# field, when present, is the PREDECESSOR line (a two-line anchor). #1327's anchors occur TWICE as substrings (the mint's and the revoke's): whole-line with
# indentation they are unique — MEASURED here, and the mint's twin is located too so the gate proves it untouched
TAMPER = {
 '1327': [(IDX, "    await dbSaveApiKey(apiKey, { rethrow: true });", 1293, 'the revoke\'s opt-in (the seat\'s arm a: `{ rethrow: true }` removed -> R1 x3 + R4 red, 4 of 14; the mint\'s twin at :1141 is indented 6 and must stay untouched)'),
          (IDX, "    const infra = /^(08|53|57)|^(ECONNREFUSED|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|EPIPE)$/.test(String(saveErr?.code)) || /connection terminated|timeout exceeded when trying to connect|connection timeout|pool is draining|client has encountered a connection error/i.test(String(saveErr?.message));", 1295, 'the revoke\'s classifier (arms b / c / d / e: forced false -> 3 of 14, forced true -> 1 of 14, message half dropped -> 1 of 14, code half dropped -> 2 of 14)'),
          (IDX, "  apiKey.isActive = false;", 1286, 'the IN-MEMORY revoke, before the try (a gate arm: restore `apiKey.isActive = true` in the catch -> R2 reds: the kept revoke is what R2 pins)')],
 '1328': [(MIDX, "       ORDER BY last_attempted_at ASC NULLS FIRST, created_at ASC", 1255, 'the rotation key (the seat\'s arm f: the OLD `ORDER BY last_sent_at` put back -> R3 red, 1 of 9)'),
          (MIDX, "        await query('UPDATE svc_teams_webhooks SET last_attempted_at = NOW() WHERE id = $1', [wh.id]);", 1312, 'the ONE stamp (arm g: removed -> R2 + R3 + R5 red, 3 of 9 — the seat predicted 2 and measured 3)'),
          (MIDX, "        skipped.push(wh.id);", 1301, 'the deadline-SKIPPED branch (arm h: stamp it too -> R5 red, and only R5, 1 of 9)'),
          (SMIG, "      ALTER TABLE svc_teams_webhooks ADD COLUMN last_attempted_at TIMESTAMPTZ;", 532, 'the guarded add-column (a gate arm on a REAL Postgres: drop it -> an upgraded database has no column and the head route answers 42703)')],
}
def locate(c, p, line, prev=None):
    if not c: return []
    L = show(c, p).split('\n'); return [i + 1 for i, l in enumerate(L) if l == line and (prev is None or (i > 0 and L[i - 1] == prev))]
def its(s): return re.findall(r"^\s*it(?:\.each\([^)]*\))?\(\s*'([^']{0,140})", s, re.M)
def describes(s): return re.findall(r"^\s*describe\(\s*'([^']{0,200})'", s, re.M)
def grep_rev(rev, rx, *paths):
    rc_, o_, _ = gq('grep', '-n', '-I', '-E', rx, rev, '--', *paths); return [x for x in o_.strip().splitlines() if x]
def region(text, start, stop_rx=r'^(app\.(get|post|put|delete|patch)\(|/\*\*)'):
    """the lines from the one that STARTS WITH <start> up to (not including) the next line matching <stop_rx>; None if <start> is not exactly once"""
    L = text.split('\n'); st = [i for i, l in enumerate(L) if l.startswith(start)]
    if len(st) != 1: return None
    e = next((j for j in range(st[0] + 1, len(L)) if re.match(stop_rx, L[j])), len(L))
    return '\n'.join(L[st[0]:e])
PROBES = {}
MEAS = {}
# the comparator's own controls, once (STANDING_LINES 2026-09-27): identical pair IDENTICAL, one token DIFFER, and the empty-string trap caught
_x = ['+a', '-b', '+c']; _y = ['+a', '-b', '+C']
_trap = [l for l in ['+a', ''] if l[:1] in '+-']
CTL_PM = (cmp_seq(pm(_x + ['']), pm(_x)) == 'IDENTICAL' and cmp_seq(pm(_x), pm(_y)) == 'DIFFER' and len(_trap) == 2 and len(pm(['+a', ''])) == 1)
hard(CTL_PM, 'CONTROL (the +/- comparator): an identical pair (one with a trailing empty line) reads IDENTICAL, a one-token mutation reads DIFFER, and the SHORT form `l[:1] in \'+-\'` would have counted the empty line (%d vs %d) — the kit uses `l and l[0] in \'+-\'`' % (len(_trap), len(pm(['+a', '']))))
hard(net(['+a', '-b', '+b', '+c']) == ['+a', '+c'] and net(['-b', '+c']) == ['-b', '+c'], 'CONTROL (the net comparator): an identical -b/+b pair cancels, a real -b/+c edit does not')
_r0 = 'app.post(\'/x\', a)\n  body\n/**\n */\napp.get(\'/y\')'
hard(region(_r0, "app.post('/x'") == "app.post('/x', a)\n  body" and region(_r0, "app.put('/z'") is None, 'CONTROL (the handler-region cutter): a region stops at the next `/**` or `app.<verb>(`, and a start that does not occur reads None')
PGJ = os.path.join(GS, 'pgprobe_gate37.json'); PG = json.load(open(PGJ)) if os.path.exists(PGJ) else None
TIER_OF = {'key-revocation': 'T1', 'schema-migration': 'T1'}
for n in NS:
    h = H[n]; cb = P[n]['develop_merge_base']; out = []; cls = K['prs'][n].get('class', '?')
    prod = [p for p in P[n]['paths'] if '__tests__' not in p and '/tests/' not in p]
    tests = [p for p in P[n]['paths'] if p not in prod]
    out.append(('PRODUCT files %s (changed +/- lines %s); TEST files %s' % ([os.path.basename(p) for p in prod], [len(pm_diff(cb, h, p)) for p in prod], [os.path.basename(p) for p in tests])) if prod else 'NO product file changed (test-only): every changed path is a test file %s' % [os.path.basename(p) for p in tests])
    hard(K['prs'][n]['tier'] == TIER_OF.get(cls), '#%s tier %s == the tier its class %s carries (%s)' % (n, K['prs'][n]['tier'], cls, TIER_OF.get(cls)))
    if cls == 'key-revocation':
        hard(prod == [IDX] and tests == [KT], '#%s (T1, class %s) changes EXACTLY ONE runtime product file %s and ONE test file %s' % (n, cls, [os.path.basename(p) for p in prod], [os.path.basename(t) for t in tests]))
    elif cls == 'schema-migration':
        hard(sorted(prod) == sorted([INIT, SMIG, MIDX]) and tests == [NT], '#%s (T1, class %s) changes EXACTLY the three declared product files %s and ONE test file %s' % (n, cls, [os.path.basename(p) for p in prod], [os.path.basename(t) for t in tests]))
    # --- the TAMPER / red-arm anchor(s), whole-line (two-line where declared), at head, develop and END_TREE
    for tt_ in TAMPER[n]:
        tf, tl, tline, tsrc = tt_[:4]; prev = tt_[4] if len(tt_) > 4 else None
        lh, ld, le = locate(h, tf, tl, prev), locate(REAL_DEV, tf, tl, prev), locate(END, tf, tl, prev)
        sub_h = [i + 1 for i, l in enumerate(show(h, tf).split('\n')) if l.strip() == tl.strip()]
        bl = {'head': blob(h, tf), 'develop': blob(REAL_DEV, tf), 'END': blob(END, tf) if END else None}
        hard(len(lh) == 1 and len(le) == 1, '#%s RED-ARM ANCHOR (%s) is byte-unique as a whole line (indentation included) in %s at head %s AND on END_TREE %s (the brief / seat said :%d)' % (n, tsrc[:90], tf.split('/Dev/')[1], lh, le, tline))
        out.append('RED-ARM ANCHOR (READ; %s): `%s` in %s — head %s | develop %s | END_TREE %s | the seat said :%d; the SAME text with ANY indentation occurs at %s at head%s; blob of %s at head %s, develop %s, END %s (%s)' % (
            tsrc, tl.strip()[:110], tf.split('/Dev/')[1], lh, ld, le, tline, sub_h, ' — the other occurrence is the MINT\'s twin: plant by WHOLE LINE, never by substring (the seat\'s first arm runner selected both and refused on its own count)' if len(sub_h) > 1 else '',
            os.path.basename(tf), (bl['head'] or '-')[:12], (bl['develop'] or '-')[:12], (bl['END'] or '-')[:12], 'the SAME file at head and on END_TREE' if bl['head'] == bl['END'] else 'the file DIFFERS between head and END_TREE — the gate plants at BOTH'))
    # --- READY identity + the golden's strict apply + the DECLARED hand-written residue
    rp = READY[n]
    if rp is None:
        out.append('READY IDENTITY: NONE — #%s was written by Seat B 39th itself (ITEM 2), not from a local-model READY; there is no golden and no checker patch to compare. Its figures are claims in its PR body, graded by the gate like any seat claim' % n)
        MEAS[n] = {'ready': None}
    elif not os.path.exists(rp):
        hard(False, '#%s READY %s ABSENT' % (n, rp)); PROBES[n] = out; continue
    else:
        rs, rl, glued = ready_block(rp)
        rblock = ('\n'.join(rl).rstrip('\n') + '\n').encode('utf-8')
        gb = open(GOLDEN[n][0], 'rb').read(); gs = sha256b(gb)
        ck = os.path.join(RUNS, CHECKER[n], 'out.md.checker', 'patch.diff')
        gsame = sha256b(rblock) == gs
        csame = os.path.exists(ck) and sha256b(open(ck, 'rb').read()) == gs
        hard(gsame and csame, '#%s the READY block\'s bytes == the golden %s (sha256 %s, %d B) == the Spark checker\'s patch.diff: %s / %s' % (n, GOLDEN[n][0].replace(BRIEFS, 'briefs/'), gs[:16], len(gb), gsame, csame))
        secs = sections('\n'.join(rl)); rpm = {sec_path(s)[1]: net(pm(s[2:])) for s in secs}
        hw = HANDWRITTEN.get(n, {})
        ab_, am, gtree = git_apply_at(cb, gb, gs, P[n]['paths'], 'g%s' % n)
        exact = {p: (ab_ is not None and ab_[p] == blob(h, p)) for p in P[n]['paths']}
        # the residue: diff(golden-applied tree, head) per path — must be EXACTLY the declared hand-written `+` lines, each `-` a merge-base line
        resid = {p: pm(g('diff', '-U0', gtree, h, '--', p).splitlines()) if gtree else None for p in P[n]['paths']}
        base_lines = {p: set(show(cb, p).split('\n')) for p in P[n]['paths']}
        want_ok = all((resid[p] == [] and p not in hw) or (p in hw and sorted(l for l in resid[p] if l[0] == '+') == sorted(hw[p]) and all(l[1:] in base_lines[p] for l in resid[p] if l[0] == '-') and len([l for l in resid[p] if l[0] == '-']) == len(hw[p])) for p in P[n]['paths']) if gtree else False
        _mut = {p: list(v) for p, v in hw.items()}; k0 = sorted(_mut)[0]; _mut[k0][0] = _mut[k0][0] + ' '
        ctl_hw = gtree is not None and sorted(l for l in resid[k0] if l[0] == '+') != sorted(_mut[k0])
        hard(ab_ is not None and all(exact[p] for p in P[n]['paths'] if p not in hw) and want_ok and ctl_hw,
             '#%s == its golden + the DECLARED hand-written lines: %s; blob == head for %s; diff(golden-applied, head) == EXACTLY the %d declared hand-written `+` line(s) in %s (each `-` a merge-base line), nothing in any other path: %s; control (a one-space mutation of a declared line reads DIFFERENT): %s' % (
                 n, am, [os.path.basename(p) for p in P[n]['paths'] if exact[p]], sum(len(v) for v in hw.values()), [os.path.basename(p) for p in hw], want_ok, ctl_hw))
        # READY +/- identity per file (NET of identical -/+ pairs): product file vs head; test file vs head MINUS the hand-written residue
        hpm = {p: pm_diff(cb, h, p) for p in P[n]['paths']}
        ident = {}
        for p in P[n]['paths']:
            if rpm.get(p, []) == hpm[p]: ident[p] = 'IDENTICAL'
            elif sorted(rpm.get(p, []) + (resid[p] or [])) == sorted(hpm[p]) and p in hw: ident[p] = 'EQUAL AS A MULTISET once the %d declared hand-written line pairs are added' % len(hw[p])
            elif sorted(rpm.get(p, [])) == sorted(hpm[p]): ident[p] = 'SLIDE-EQUAL (same lines, another order)'
            else: ident[p] = 'DIFFER'
        hard(all(v != 'DIFFER' for v in ident.values()), '#%s READY +/- identity per file (net of identical -/+ pairs; the hand-written residue added for the declared file only): %s' % (n, {os.path.basename(p): v for p, v in ident.items()}))
        out.append('READY IDENTITY (MEASURED, `git diff -U0` merge-base -> head vs the READY block netted of identical -/+ pairs, `l and l[0] in \'+-\'`): %s — the READY block\'s bytes == the golden: %s; the Spark checker\'s patch.diff == the golden: %s; %s' % (
            {os.path.basename(p): v for p, v in ident.items()}, gsame, csame, ('the READY\'s closing fence is GLUED to its last diff line %r: stripped' % glued[1]) if glued else 'no glued fence'))
        out.append('GOLDEN APPLY (MEASURED, `git apply --cached --check` then apply, strict, at the merge-base %s; %s): %s -> product blob == head: %s; the test file == head AFTER the %d DECLARED hand-written lines (the header :5-7 and the describe :98, the PR body\'s "The two hand-written edits"): %s. The brief predicted +29/-4 on the test file, git counts +28/-3 (one empty -/+ pair the golden carries and git collapses; the body says so) — the NET comparator cancels it' % (
            cb[:12], ' + '.join(os.path.basename(x) for x in GOLDEN[n]), am, exact.get(IDX), sum(len(v) for v in hw.values()), want_ok))
        MEAS[n] = {'ready': os.path.basename(rp), 'ready_sha256': rs, 'ready_bytes_eq_golden': gsame, 'checker_eq_golden': csame, 'golden': GOLDEN[n], 'golden_sha256': gs,
                   'apply': am, 'product_blob_eq_head': exact.get(IDX), 'handwritten_residue_exact': want_ok, 'handwritten': hw, 'identity': ident}
    # --- cells (READ): every test file the PR touches, at the merge-base and at head; describe titles too (a describe rename changes every fullName)
    for t in tests:
        tt, t0 = show(h, t), show(cb, t)
        d0, d1 = describes(t0), describes(tt)
        out.append('CELLS (READ, %s): %d `it(`/`it.each(` entries at the merge-base, %d at head%s; NEW at head: %s; GONE at head: %s; describe %s -> %s%s' % (
            os.path.basename(t), len(its(t0)), len(its(tt)), ' (an it.each over INFRA expands to one cell per row: 3 rows)' if 'it.each(INFRA)' in tt else '', [x[:90] for x in its(tt) if x not in its(t0)] or 'NONE', [x[:90] for x in its(t0) if x not in its(tt)] or 'NONE', d0, d1,
            ' — THE DESCRIBE WAS RENAMED, so EVERY fullName in this file changes (`<describe> <it>`): the gate greps the repo and every fleet list it can READ (baselines, intermittents, manifests, the preflight) for the OLD describe string and for each old fullName, and says whether anything pinned one' if d0 != d1 else ''))
        MEAS.setdefault(n, {})['describe_renamed'] = d0 != d1
    svc = K['prs'][n]['service']
    pkg = show(REAL_DEV, 'Blockchain/Dev/' + svc + '/package.json')
    out.append('TEST RUNNER (READ, %s package.json at develop): scripts.test = %r; scripts.lint = %r' % (svc, (re.search(r'"test"\s*:\s*"([^"]*)"', pkg) or [None, '?'])[1], (re.search(r'"lint"\s*:\s*"([^"]*)"', pkg) or [None, 'ABSENT'])[1]))
    # --- per-class probes
    if cls == 'key-revocation':
        i0, i1 = show(cb, IDX), show(h, IDX)
        regs = {}
        for lab, start, stop in (('MINT (POST /api/keys)', "app.post('/api/keys', ", None), ('VALIDATE (POST /api/keys/validate)', "app.post('/api/keys/validate'", None),
                                 ('revokePriorConnectorKeys (the KS-577 rotate revoke)', 'export async function revokePriorConnectorKeys(', r'^}'), ('LIST (GET /api/keys)', "app.get('/api/keys', ", None)):
            a_, b_ = region(i0, start, stop or r'^(app\.(get|post|put|delete|patch)\(|/\*\*)'), region(i1, start, stop or r'^(app\.(get|post|put|delete|patch)\(|/\*\*)')
            regs[lab] = (a_ is not None and a_ == b_, len((b_ or '').split('\n')))
        _pl = region(i1, "app.post('/api/keys', "); _plm = _pl.replace('memApiKeys.delete(apiKey.id);', 'memApiKeys.delete(apiKey.id); ', 1) if _pl else None
        hard(all(v[0] for v in regs.values()) and _pl is not None and _plm != _pl, '#%s MINT-UNCHANGED / VALIDATE-UNCHANGED / ROTATE-UNCHANGED (MEASURED, byte-equal handler regions merge-base vs head): %s; control (a one-space plant in the mint region reads DIFFERENT): %s' % (
            n, {k: 'BYTE-EQUAL (%d lines)' % v[1] if v[0] else 'DIFFERS' for k, v in regs.items()}, _plm != _pl if _pl else 'NO REGION'))
        MEAS[n]['handler_regions_byte_equal'] = {k: v[0] for k, v in regs.items()}
        cls_lines = [l.strip() for l in i1.split('\n') if l.strip().startswith('const infra = /^(08|53|57)')]
        hard(len(cls_lines) == 2 and cls_lines[0] == cls_lines[1], '#%s CLASSIFIER-TWIN (MEASURED): the infra classifier occurs %d time(s) at head (the mint\'s and the revoke\'s), and the two are byte-identical once de-indented: %s' % (n, len(cls_lines), len(set(cls_lines)) == 1))
        out.append('CLASSIFIER-TWIN (MEASURED): the revoke copies the mint\'s classifier INLINE (not a shared function) — byte-identical today; two copies can drift (a fix-shape, not a defect: one exported `isInfraSaveFault`). It reads `^(08|53|57)` on String(code) — so 57P01 (admin shutdown), 53300 (too many connections) and 08006 are 503; a code-less error reaches 503 only through the five message phrases; `ETIMEDOUT` etc. only as an EXACT code')
        dl = i1.split('\n')
        rv = [i + 1 for i, l in enumerate(dl) if l.startswith("app.delete('/api/keys/:id'")][0]
        order = {k: next((i + 1 for i in range(rv - 1, len(dl)) if dl[i].strip().startswith(k)), None) for k in ('const apiKey = await dbGetApiKey(', 'apiKey.isActive = false;', 'try {', 'await dbSaveApiKey(apiKey, { rethrow: true });', "log('info', 'API key revoked'")}
        out.append('THE REVOKE, IN ORDER (READ, index.ts at head from :%d): %s — `dbGetApiKey` swallows its own DB error and falls back to memApiKeys (READ :340-:355), so the handler\'s only await OUTSIDE a try cannot reject from the DB; with the DB available it returns a FRESH object from rowToApiKey, and `dbSaveApiKey` puts THAT object into memApiKeys BEFORE its INSERT (:293) — so the kept revoke reaches the cache on the production path too (FRESH-OBJECT PATH: the PR body says it is "reasoned, not driven" — the gate DRIVES it: a key the process did not mint, revoked under a failing save, then validated by hash)' % (rv, order))
        out.append('WHAT THE KEPT REVOKE DOES NOT COVER (READ, disclosed in the PR body): memApiKeys is re-warmed ONLY by loadFromDb at boot (:1585) — a restart re-reads the row as ACTIVE; another replica never saw the revoke; nothing retries; the api-gateway caches a validate answer for 30 s (middleware/auth.ts, per card secuura-ks888-validate-usage-write-failure) — so a key revoked AFTER a cached "valid" still passes the gateway for up to 30 s whether or not the save landed (pre-existing; say so once)')
        out.append('VALIDATE IS UNCHANGED (READ): its usage write `await dbSaveApiKey(apiKey);` (:1369) still takes the swallow; Kam RULED card secuura-ks888-validate-usage-write-failure option a at 2026-09-28 20:24 (decisions.json; the commission says 20:22:15): validate never refuses because of a failed usage write — a SEPARATE PR, not this one. The gate proves validate answers exactly as at develop, including under a failing INSERT (C3)')
        sp = grep_rev(REAL_DEV, r'/api/security/keys/\{id\}', SEC)
        out.append('THE PUBLISHED SPEC (READ, security.openapi.ts at develop): the revoke is published as `DELETE /api/security/keys/{id}` (%s) — the PR body: "no 503/500 is declared for revoke in the published spec"; the gate reads the operation\'s declared responses at END_TREE, runs `npm run check:openapi`, and says whether an undeclared 503/500 is a finding (SPEC-503-UNDECLARED)' % [x.split(':')[1].split('/src/')[1] + ':' + x.split(':')[2] for x in sp if '__tests__' not in x][:3])
    if cls == 'schema-migration':
        m1, sm1, in1 = show(h, MIDX), show(h, SMIG), show(h, INIT)
        sites = {'init 06 CREATE': in1.count('last_attempted_at TIMESTAMPTZ'), 'CORE CREATE': len(re.findall(r'CREATE TABLE IF NOT EXISTS svc_teams_webhooks \([^`]*last_attempted_at TIMESTAMPTZ', sm1)),
                 'guarded add-column': len(re.findall(r"column_name='last_attempted_at'\) THEN\s*\n\s*ALTER TABLE svc_teams_webhooks ADD COLUMN last_attempted_at TIMESTAMPTZ;", sm1))}
        hard(all(v == 1 for v in sites.values()), '#%s THREE DDL SITES (READ, at head): %s — each exactly once' % (n, sites))
        filemig = grep_rev(h, r'svc_teams_webhooks', 'Blockchain/Dev/services/api-gateway/migrations', 'Blockchain/Dev/migrations', 'Blockchain/Dev/database')
        out.append('THE MIGRATION\'S HOME (READ): the column lands in the LEGACY CORE_MIGRATIONS array (stage 2), beside `last_sent_at` — the file header says "Each new migration should go into a file under `migrations/`"; no stage-1 file names svc_teams_webhooks (%s). Wednesday RULED the guarded add-column shape (the commission: startup-migrations.ts:522-528); graded as ruled scope, never a defect. CORE_MIGRATIONS runs against the main DB, the platform DB AND every tenant DB (:1002, :1191 READ) — the gate says which of those hold svc_teams_webhooks' % (filemig or 'NONE'))
        L1 = m1.split('\n')
        def at(pfx, after=0): return next((i + 1 for i in range(after, len(L1)) if L1[i].strip().startswith(pfx)), None)
        a_g = at('if (remainingMs <= 0) {', 1250); a_s = at('skipped.push(wh.id);', a_g or 0); a_t = at('try {', a_s or 0)
        a_u = at("await query('UPDATE svc_teams_webhooks SET last_attempted_at = NOW() WHERE id = $1', [wh.id]);", a_t or 0); a_o = at('const result = await safeOutboundRequest(', a_u or 0)
        a_c = at('} catch { failed.push(wh.id); }', a_o or 0)
        n_st = m1.count('SET last_attempted_at = NOW()')
        hard(None not in (a_g, a_s, a_t, a_u, a_o, a_c) and a_g < a_s < a_t < a_u < a_o < a_c and n_st == 1, '#%s STAMP PLACEMENT A (READ, index.ts at head): deadline guard :%s < skipped.push :%s < try :%s < the ONE stamp :%s < safeOutboundRequest :%s < the per-row catch :%s; stamps in the file: %d' % (n, a_g, a_s, a_t, a_u, a_o, a_c, n_st))
        out.append('STAMP-INSIDE-THE-TRY (READ): the stamp is the first statement of the per-row `try` (:%s), so a stamp that THROWS (the column absent, a DB fault) lands in `catch { failed.push(wh.id) }` (:%s) — the row is reported FAILED with NO outbound request made, and stays unstamped; the gate drives a failing stamp and says whether "failed" then misreports a delivery that was never tried (a finding with its fix-shape, or not)' % (a_u, a_c))
        out.append('DEADLINE-STALE (READ): `remainingMs` is computed BEFORE the stamp and `timeoutMs: Math.min(TEAMS_NOTIFY_PER_ROW_TIMEOUT_MS, remainingMs)` is passed AFTER it — the stamp\'s latency is not subtracted, so the aggregate bound can overshoot by one stamp round-trip (plus the per-row ceiling) on the LAST attempted row; the gate measures the overshoot against N2 / N3\'s bounds')
        out.append('THE COST (READ + the seat\'s COUNT): writes per row 0 -> 0 (skipped), 0 -> 1 (blocked / non-ok / throws), 1 -> 2 (success); MAX_ROWS default 50, the aggregate deadline default 10000 ms, the per-row ceiling 2000 ms (index.ts :79-:81); the test env 25 / 1500 / 600 (ks934 :47-:49). The seat did NOT measure wall-clock ("there is no real Postgres in this environment") — the gate measures it on a REAL Postgres (THE POSTGRES below)')
        out.append('THE DEPLOY ORDER (READ): the head\'s SELECT orders by a column only the api-gateway\'s STARTUP migration adds — an m365-integration that starts on a database the gateway has not yet migrated (or a tenant DB the stage-2 run failed on: failures are a log line today, card secuura-ks1054-f9282-migration-failure-visibility ruled a at 20:24 — flag it on /health, not yet built) answers the WHOLE notify route with 42703, not one row; the body says `run-migrations.sh` exits 0 on a failed migration. The gate says whether that is a finding for this PR or for KS-1054')
        out.append('THE PUBLISHED FIELD (READ): GET /api/teams/webhook-config maps `lastSentAt: r.last_sent_at` (index.ts ~:1172) and NOT the new column — `last_attempted_at` reaches no response (the body says so; the gate confirms by the route at head)')
        if PG and '_summary' in PG:
            R = PG['runs']
            out.append('THE POSTGRES (MEASURED by the drafter, pgprobe_gate37.py -> pgprobe_1.out / pgprobe_gate37.json: every SQL text extracted from the clone at the merge-base and the head, run on PGlite — %s, IN-PROCESS: no socket, no port, never :5432): %s; the stamp UPDATE in-process median %s ms / p95 %s ms over %d (a LOWER BOUND: no network round-trip); E (the head\'s route SQL on an UNMIGRATED schema): select %s | update %s; controls %s' % (
                PG['engine'][:40], PG['_summary'], R['F_update_cost_inprocess']['median_ms'], R['F_update_cost_inprocess']['p95_ms'], R['F_update_cost_inprocess']['updates'],
                R['E_head_route_sql_on_unmigrated_schema']['select'][:70], R['E_head_route_sql_on_unmigrated_schema']['update'][:50], PG['controls']))
            MEAS[n]['pgprobe'] = {'summary': PG['_summary'], 'controls': PG['controls'], 'update_cost_ms': R['F_update_cost_inprocess']}
        else: out.append('THE POSTGRES: pgprobe_gate37.json ABSENT — UNMEASURED by the drafter')
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
