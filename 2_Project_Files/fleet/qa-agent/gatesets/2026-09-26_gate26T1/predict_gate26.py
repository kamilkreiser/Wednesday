#!/usr/bin/env python3
"""predict_gate26.py — MEASURE one gate26 kit (the directory this script lives in; its PR set, tiers and commit counts are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json carries
NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and the
fetch into the scratch clone must agree with both.

Shape copied from gate25's predict_gate25.py and re-keyed: N rows (4 in T1, 6 in T2), a PER-PR merge-base (the ten PRs sit on THREE different
develop commits: 6e2a00bf (#1245), 4db87c3e (#1275 #1277 #1278), d7cdecf1 (the rest)), and a DECLARED COMMIT COUNT per PR (#1245 is THREE commits
— rounds 1-3 — the rest ONE). There is no Seat-M1 merge set in flight at drafting (M1 merged gate25's six before this kit was pinned); instead the
LIVE build seat (Seat B 30th) is censused: its in-flight PRs (kit.json `inflight`: heads that WILL move) and its unpushed worktree(s)
(kit.json `inflight_worktrees`, READ with read verbs only: rev-parse, merge-base, diff, `--no-optional-locks status`).

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g26_sp/clone.git — `git clone --bare --no-local` FROM the checkout (NO
alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never
printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over merge-base(develop, head), with NO merge
commit among them; (1) diff(develop, merged) == EXACTLY the PR's own paths (diff(merge-base, head)), each merged blob byte-equal to the head's blob
(kit.json `declared_overlap` would carry a 3-way target; BOTH gate26 kits declare NONE — measured); (2) numstat(develop -> merged) ==
numstat(merge-base -> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. NOT STACKED: for every pair in the kit and
across the sibling kit, neither head is an ancestor of the other and their merge-base is an ancestor of develop (no shared non-develop commit).
PAIRWISE the kit's path sets are DISJOINT (hard), disjoint from the SIBLING kit's (hard: the kits may merge in either order), and disjoint from
Seat B 30th's in-flight PRs and worktree(s) (hard: an overlap must be DECLARED by a re-draft, never absorbed). END_TREE = develop + every PR of
the kit, identical in ALL orders (N! orders, memoised on (tree, PR) so equal states are merged once), and END_TREE_WITH_SIBLING = develop + the
sibling kit + this kit, identical whichever kit lands first. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the kit) builds develop + a FOREIGN edit of that PR's first own
file and must REFUSE; --simulate predev measures over kit.json's `predev` (develop before gate25's six squashes) and must PASS. A simulation
writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate26.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|predev]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate26.py <scratchpad> [--simulate …]'); sys.exit(9)
SIM = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--simulate' else 'none'
NS = sorted(K['prs']); SIB = K['sibling_batch']; INF = K['inflight']
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
CL = os.path.join(SP, 'g26_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate26 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

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
AP = {n: api('pulls/' + n) for n in NS + SIB + INF}
for n in NS: hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == 'develop', '#%s open, not draft, base develop (API)' % n)
for n in INF: print('  in-flight #%s (Seat B 30th; its head WILL move — censused, never pinned): state %s head %s' % (n, AP[n]['state'], AP[n]['head']['sha']))
BR = {n: 'refs/heads/' + AP[n]['head']['ref'] for n in NS}
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in NS + SIB + INF] + [BR[n] for n in NS]
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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g26/develop']
    + ['+refs/pull/%s/head:refs/g26/pull/%s' % (n, n) for n in NS + SIB + INF] + ['+%s:refs/g26/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g26/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g26/pull/' + n).strip() == g('rev-parse', 'refs/g26/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
if SIM == 'predev':
    DEV = K['predev']; print('  SIMULATION predev: develop := %s (%s)' % (DEV, K['predev_note']))
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    mb0 = g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', mb0, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n// gate26 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g26idx', dir=os.path.join(SP, 'g26_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate26 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
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

print('--- (c) NOT STACKED and PAIRWISE: the kit, the sibling kit, Seat B 30th\'s in-flight PRs and worktree(s)')
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g26/pull/' + n).strip()
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
    for b in INF: hard(not (OWN[a] & INFP[b]), '#%s vs Seat B 30th in-flight #%s (head %s) disjoint %s' % (a, b, head_of(b)[:12], sorted(OWN[a] & INFP[b]) or ''))
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
        nc = [l for l in ch if not re.match(r'^\s*(//|\*|/\*)', l) and l.strip()]
        out.append('product files %s: changed lines %d, NON-comment changed lines %d (a line-prefix READ, NOT an emit)' % ([os.path.basename(p) for p in prod], len(ch), len(nc)))
    else:
        out.append('NO product file: every path is a test / tooling path %s' % [os.path.basename(p) for p in P[n]['paths']])
    OR = 'Blockchain/Dev/services/originate/src'
    if n == '1280':
        out.append('RAW-HEIGHT-SITES at head (non-test originate/src): `blockNumber ??` %d, `blockNumber ||` %d — #1281\'s rebuild writers persist `blockHeight: anchor.blockNumber || 0` UNcoerced (outside KS-1129\'s heal scope; READ)' % (
            grepc(h, r'blockNumber \?\?', OR + '/routes') + grepc(h, r'blockNumber \?\?', OR + '/services'), grepc(h, r'blockNumber \|\|', OR + '/routes') + grepc(h, r'blockNumber \|\|', OR + '/services')))
        out.append('DOCBLOCK-DISPLACED: the new toBlockHeight docblock sits between confirmStalePendingAnchor\'s own docblock and its function (READ; cosmetic)')
    if n == '1281':
        src = show(h, OR + '/services/anchorStateSync.ts')
        out.append('WRITERS in anchorStateSync.ts at head: `updateDocument(` %d, `blockchain: {` %d, `...carriedForward(` %d (READ)' % (src.count('updateDocument('), src.count('blockchain: {'), src.count('...carriedForward(')))
        out.append('READ-PER-WRITE: the poller adds a getDocument() before each updateDocument — the window between that read and the write is still a read-modify-write race (READ; the gate measures a token minted between the two)')
    if n in ('1282', '1283', '1284'):
        f = OR + {'1282': '/routes/systemErrors.ts', '1283': '/routes/gdpr.ts', '1284': '/routes/adminConfig.ts'}[n]
        src = show(h, f)
        out.append('%s at head: live `NODE_ENV === \'production\' ? \'Internal server error\' : err.message` ternaries %d; fail500( call sites %d (READ)' % (
            os.path.basename(f), len(re.findall(r"NODE_ENV === 'production' \? 'Internal server error' : err\.message", src)), src.count('fail500(res,')))
        rest = gq('grep', '-l', '-E', r"NODE_ENV === 'production' \? 'Internal server error' : err\.message", h, '--', OR)[1].split()
        out.append('KS-730 REMAINDER at this head (files still carrying the ternary): %s — each of the three KS-730 PRs clears ONE file; only develop + all three clears the class (the gate measures the three together on END_TREE)' % sorted(x.split(':', 1)[1] for x in rest))
        out.append('LOG-CONTENT: fail500 now logs err.message (pg / service error text; %s) through the winston logger — the gate reads where it lands (Console always; logs/*.log in production) and whether any sink forwards it (READ)' % {'1282': 'system-error admin routes', '1283': 'GDPR routes: a message can carry a user id or DSR text', '1284': 'admin-configuration routes'}[n])
        if n == '1283':
            ln = [i + 1 for i, l in enumerate(src.splitlines()) if 'Deliberately no logger import in this file' in l]
            out.append('STALE-COMMENT: the head still carries "Deliberately no logger import in this file" at line(s) %s, while the head commit message says "The comment is corrected in place" and the file now imports the logger (READ)' % (ln or 'NONE'))
        out.append('DOCBLOCK-DISPLACED: fail500\'s docblock sits between the first route\'s own one-line docblock and that route (READ; cosmetic)')
        if n == '1284':
            unc = [i + 1 for i, l in enumerate(src.splitlines()) if 'err.message' in l and not re.match(r'^\s*(//|\*|/\*)', l) and not re.search(r'logger\.|NODE_ENV|instanceof Error', l)]
            out.append('UNCONDITIONAL-LEAK (KS1334): non-comment lines putting err.message in a RESPONSE with NO NODE_ENV guard at this head: %d at lines %s (three `message: err.message` 500 bodies + one per-tenant `error: err.message?.substring(0, 60)` result row) — the seat says 4 at base and 4 here, pinned by cell C4 and ticketed; the gate grades them as DECLARED SCOPE and says what each returns (READ)' % (len(unc), unc))
            out.append('FIXTURE-TRAP: every driven route opens its catch with a benign `does not exist` -> 200 branch; a LEAK message containing that text never reaches fail500 — C1 (the logger REACHED with [route context, {error: LEAK}]) is load-bearing, C0 and C4 are its controls (Wednesday 09:5x; READ)')
    if n == '1274':
        src = show(h, 'Blockchain/Dev/services/m365-integration/src/index.ts')
        q = re.search(r'SELECT \* FROM svc_teams_webhooks WHERE is_active = true AND events[^`]*`', src)
        out.append('ROUND 2 query at head (READ): %s | param %s' % (' '.join(q.group(0).split()) if q else 'NOT FOUND', re.findall(r'\[event, TEAMS_NOTIFY_MAX_ROWS[^\]]*\]', src)))
        for sp in ('Blockchain/Dev/docker/init/06-m365-tables.sql', 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts'):
            lines = show(h, sp).splitlines()
            out.append('LAST-SENT-AT-SOURCES %s: `last_sent_at` on line(s) %s (READ at the head; the seat says 06-m365-tables.sql:63, startup-migrations.ts:361 + backfill :526-527)' % (os.path.basename(sp), [i + 1 for i, l in enumerate(lines) if 'last_sent_at' in l]))
        mig = gq('grep', '-l', 'svc_teams_webhooks', h, '--', 'Blockchain/Dev/migrations')[1].split()
        out.append('migrations/ naming svc_teams_webhooks: %s' % (mig or 'NONE'))
        out.append('ENV x ROUND 2 (arithmetic, READ): MAX_ROWS="abc" -> LIMIT NaN+1 = NaN and `fetched.length > NaN` is false, so truncated can never be true; MAX_ROWS="0" -> LIMIT 1, the probe row makes truncated TRUE while slice(0, 0) notifies NOTHING — every call answers total 0, truncated true (F-1274-2 is still unfixed; now loud rather than silent)')
        out.append('KS1335 (DECLARED): last_sent_at is written only after a SUCCESSFUL send, so >= MAX_ROWS permanently failing rows hold the head of every call and starve the rest again; cell R3 PINS that as a known limit — the healthy-row rotation cells do not cover it')
    if n == '1261':
        f = 'Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts'
        src = show(h, f)
        out.append('MANIFEST (READ at head): %d `.test.ts` string literals in the file; RS1/RS2/RS3a named %s; MANIFEST-DRIFT named %s; the dns spy answers non-loopback itself (N-1261-a): a `lookup` stub present %s' % (
            len(set(re.findall(r"'([\w.-]+\.test\.ts)'", src))), [x for x in ('RS1', 'RS2', 'RS3a') if x in src], 'MANIFEST-DRIFT' in src, 'lookup' in src))
        out.append('RS FIXTURES are COPIES in a temp directory (the seat) — the gate still reverts the REAL lines in its own worktree (gate24T2c\'s RS1/RS2/RS3a method) and checks the cell reds by NAME')
    if n == '1268':
        r1 = g('rev-parse', h + '^').strip()
        ec = 'Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts'
        out.append('ROUND-1 WORK BY BLOB: entrypoint-corpus.test.ts round 1 (%s) %s | round 2 head %s -> %s (READ)' % (r1[:12], blob(r1, ec), blob(h, ec), 'BYTE-IDENTICAL' if blob(r1, ec) == blob(h, ec) else 'DIFFERENT'))
        d2 = g('diff', '--name-only', r1, h).split()
        out.append('round 2 (%s) touches only %s (READ)' % (h[:12], d2))
        out.append('THIRD RULE (returned escape) — the gate grades it as a SHAPE: can a function returned from an invoked one be used to make an UNGUARDED path read guarded:true (an over-report that hides nothing) or to hide a guarded one (under-report)? W19 (stored, never called -> false) is its boundary')
    if n == '1245':
        out.append('LIVE-SHAPE (drafter_liveshape_g26.sh, liveshape_1.out): round 3\'s readChildOutput, extracted from the head blob and run under node, reads all 42 REAL stdout captures of gate24T2c correctly (H1/H1b/H1c NULL); SYN-H4s (an exit-hook lookalike INCLUDING `Start at` after the real block, status 1) reads {7,0} — the gate captures it LIVE and rules')
    if n == '1275':
        out.append('EMIT: the only non-comment product change is `(res) =>` -> `(res: http.IncomingMessage) =>` (READ) — the gate owes the EMIT PROOF (transpile parent vs head, removeComments, byte-equal, with a control that reads DIFFERENT)')
    if n == '1279':
        out.append('DB-SUITE: an integration suite that INSERTs rows over two DSNs; the new guard refuses a non-loopback host and the shared-stack ports BEFORE connecting (READ) — measurable without a database')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT,
       'end_tree': END, 'end_tree_with_sibling': sib_first, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES,
       'sibling_paths': {n: sorted(SIBP[n]) for n in SIB}, 'sibling_heads': {n: head_of(n) for n in SIB},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': WT}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | END_TREE_WITH_SIBLING %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, sib_first))
sys.exit(1 if FAIL else 0)
