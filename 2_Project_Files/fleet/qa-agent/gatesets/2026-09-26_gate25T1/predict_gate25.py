#!/usr/bin/env python3
"""predict_gate25.py — MEASURE one gate25 kit (the directory this script lives in; its PR set, tiers and declared overlap are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json's heads (kit.json
carries none): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and
the fetch into the scratch clone must agree with both.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, merge-file,
hash-object, commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g25_sp/clone.git — `git clone --bare --no-local` FROM the
checkout (NO alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for the clone only,
never printed). Nothing is written into the checkout.

DEVELOP IS MOVING: Seat M1 is squashing #1262-#1266 onto d7cdecf1 (expected END tree 6942101caa7b). The pin is the develop READ NOW, whatever
subset of M1's five has landed. BASE-INVARIANT per PR over that develop: (1) diff(develop, merged) == EXACTLY the PR's own paths, each merged blob
byte-equal to the head's blob — EXCEPT a DECLARED OVERLAP (kit.json `declared_overlap`: #1267's credentialRepo.ts, which #1264 also edits, in a
DIFFERENT hunk): there the merged blob must equal the clean 3-way `git merge-file` of (develop blob, parent blob, head blob), and develop's blob must
be EITHER the parent's (M1's #1264 not landed) OR #1264's head blob (landed) — anything else REFUSES; (2) numstat(develop -> merged) ==
numstat(parent -> head); (3) the develop move since the PR's parent ∩ the PR's OWN paths == EMPTY, the declared overlap excepted under (1)'s rule.
PAIRWISE the kit's path sets are DISJOINT (hard), and disjoint from the SIBLING kit's four (hard: the two kits may merge in either order); M1's five
are censused (overlap reported; only the declared one is allowed). END_TREE = develop + every PR of the kit, identical in ALL orders (4! = 24,
measured), and END_TREE_AFTER_M1 = the same over develop + whichever of M1's five are still OPEN (the tree the kit lands on once M1 finishes),
with M1's own expected END tree checked when all five are in. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the kit) builds develop + a FOREIGN edit of that PR's first own file
and must REFUSE; --simulate overlapbad (T1 only) builds develop + a foreign edit of the declared-overlap path and must REFUSE; --simulate m1base
measures over M1's base d7cdecf1 (the declared overlap UNMOVED) and must PASS. A simulation writes pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate25.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|overlapbad|m1base]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate25.py <scratchpad> [--simulate …]'); sys.exit(9)
SIM = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--simulate' else 'none'
NS = sorted(K['prs']); SIB = K['sibling_batch']; M1 = K['m1']
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
CL = os.path.join(SP, 'g25_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate25 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

print('--- (a) heads and develop: the PULLS API, then ls-remote (the checkout, READ), then a fetch FROM ORIGIN into the scratch clone')
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
def api(u):
    for i in range(4):   # a 5xx from GitHub is retried (3 x 10 s), never read as an answer
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            print('  (GitHub %d on %s — retry %d)' % (e.code, u, i + 1)); import time; time.sleep(10)
AP = {n: api('pulls/' + n) for n in NS + SIB + M1}
for n in NS: hard(AP[n]['state'] == 'open' and not AP[n]['draft'] and AP[n]['base']['ref'] == 'develop', '#%s open, not draft, base develop (API)' % n)
BR = {n: 'refs/heads/' + AP[n]['head']['ref'] for n in NS}
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in NS + SIB + M1] + [BR[n] for n in NS]
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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g25/develop']
    + ['+refs/pull/%s/head:refs/g25/pull/%s' % (n, n) for n in NS + SIB + M1] + ['+%s:refs/g25/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g25/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g25/pull/' + n).strip() == g('rev-parse', 'refs/g25/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
if SIM == 'm1base':
    DEV = K['m1_base']; print('  SIMULATION m1base: develop := M1\'s base %s (the declared overlap UNMOVED)' % DEV)
elif SIM.startswith('foreign') or SIM == 'overlapbad':
    tn = SIM[7:] if SIM.startswith('foreign') else list(K['declared_overlap'])[0]
    par = g('rev-parse', H[tn] + '^').strip()
    path = K['declared_overlap'][tn]['path'] if SIM == 'overlapbad' else sorted(g('diff', '--name-only', par, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n// gate25 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g25idx', dir=os.path.join(SP, 'g25_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate25 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION %s: develop := %s (a foreign edit of %s)' % (SIM, DEV, path))
DT = g('rev-parse', DEV + '^{tree}').strip()
print('  develop %s tree %s | %s' % (DEV, DT, g('log', '-1', '--format=%s', DEV).strip()))

print('--- (b) Seat M1\'s merge set on develop (API state + ancestry); the expected M1 END tree %s' % K['m1_end_tree'])
m1open = []
for n in M1:
    p = AP[n]; mc = p.get('merge_commit_sha') if p['merged'] else None
    anc = (gq('merge-base', '--is-ancestor', mc, DEV)[0] == 0) if mc else False
    print('  #%s state %s merged %s merge_commit %s on develop %s' % (n, p['state'], p['merged'], (mc or '-')[:12], anc))
    if not p['merged']: m1open.append(n)
    elif SIM != 'm1base': hard(anc, '#%s merged AND its squash is an ancestor of the pinned develop' % n)
if SIM == 'm1base': m1open = list(M1)
if not m1open: print('  all five of M1 are in: develop tree %s %s M1\'s expected END tree' % (DT, '==' if DT == K['m1_end_tree'] else '!= (REPORTED)'))

print('--- (c) per PR: shape, own paths, BASE-INVARIANT over develop')
P = {}
def blob(c, p):
    rc, o, _ = gq('rev-parse', '%s:%s' % (c, p)); return o.strip() if rc == 0 else None
def numstat(a, b): return sorted(g('diff', '--numstat', a, b).strip().splitlines())
for n in NS:
    h = H[n]; par = g('rev-parse', h + '^').strip()
    mb = g('merge-base', DEV, h).strip()
    hard(g('rev-list', '--count', '%s..%s' % (par, h)).strip() == '1' and mb == par, '#%s is ONE commit on %s, and that parent is develop\'s merge-base' % (n, par[:12]))
    own = sorted(g('diff', '--name-only', par, h).split())
    move = sorted(g('diff', '--name-only', par, DEV).split())
    ov = sorted(set(own) & set(move)); dec = K['declared_overlap'].get(n)
    res = {'head': h, 'branch': BR[n], 'parent': par, 'paths': own, 'numstat': numstat(par, h), 'merge_base': mb,
           'ahead': int(g('rev-list', '--count', '%s..%s' % (DEV, h)).strip()), 'behind': int(g('rev-list', '--count', '%s..%s' % (h, DEV)).strip()),
           'move_paths': len(move), 'overlap_with_move': ov}
    rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + par, DEV, h)
    hard(rc == 0, '#%s merges CLEAN over develop (merge-tree rc %d)' % (n, rc))
    mt = o.split()[0] if (o and rc == 0) else ''; res['merged_tree'] = mt
    if not mt:
        print('  (#%s: not a clean merge — its blob checks are not reachable; REFUSED above)' % n); P[n] = res; continue
    changed = sorted(g('diff', '--name-only', DEV, mt).split()) if mt else []
    hard(changed == own, '#%s (1) diff(develop, merged) == its own %d path(s) %s' % (n, len(own), own))
    res['merged_blobs'] = {}
    for p in own:
        mbl, hbl, pbl, dbl = blob(mt, p), blob(h, p), blob(par, p), blob(DEV, p)
        if p in ov:
            ok_dec = bool(dec) and dec['path'] == p
            by = dec['by'] if ok_dec else None
            byb = blob(H.get(by) or g('rev-parse', 'refs/g25/pull/%s' % by).strip(), p) if by else None
            hard(ok_dec and dbl in (pbl, byb), ('#%s (3) develop moved its own path %s: DECLARED overlap with #%s — develop blob %s must be the parent\'s %s or #%s\'s head blob %s' % (n, p, by, (dbl or '-')[:12], (pbl or '-')[:12], by, (byb or '-')[:12])) if ok_dec else '#%s (3) develop moved its own path %s: an UNDECLARED overlap' % (n, p))
            if not ok_dec or dbl is None or pbl is None:
                res['merged_blobs'][p] = {'merged': mbl, 'head': hbl, 'target': 'UNDECLARED OVERLAP — no target'}; continue
            d = tempfile.mkdtemp(prefix='g25mf', dir=os.path.join(SP, 'g25_sp'))
            for nm, b in (('cur', dbl), ('base', pbl), ('other', hbl)): open(os.path.join(d, nm), 'w', encoding='utf-8').write(g('cat-file', '-p', b))
            r = subprocess.run(['git', 'merge-file', '-p', os.path.join(d, 'cur'), os.path.join(d, 'base'), os.path.join(d, 'other')], capture_output=True, text=True)
            tgt = run(['git', '--git-dir', CL, 'hash-object', '--stdin'], input=r.stdout).strip()
            hard(r.returncode == 0 and tgt == mbl, '#%s (1) DECLARED-OVERLAP merged blob %s == the clean 3-way merge-file(develop, parent, head) (rc %d); != head blob %s: %s' % (n, (mbl or '-')[:12], r.returncode, hbl[:12], mbl != hbl))
            res['merged_blobs'][p] = {'merged': mbl, 'head': hbl, 'target': 'merge-file(develop %s, parent %s, head %s)' % ((dbl or '-')[:12], (pbl or '-')[:12], hbl[:12])}
        else:
            hard(mbl == hbl, '#%s (1) merged blob == head blob %s for %s' % (n, (hbl or 'DELETED')[:12], p))
            res['merged_blobs'][p] = {'merged': mbl, 'head': hbl, 'target': 'head blob'}
    hard(numstat(DEV, mt) == res['numstat'], '#%s (2) numstat(develop -> merged) == numstat(parent -> head) %s' % (n, res['numstat']))
    modes = g('diff', '--summary', DEV, mt).strip()
    hard('mode change' not in modes, '#%s no mode change (%s)' % (n, modes.replace('\n', ' | ') or 'none'))
    hard(not [p for p in ov if not (dec and dec['path'] == p)], '#%s (3) develop move since %s ∩ own paths == %s (declared: %s)' % (n, par[:12], ov or 'EMPTY', dec['path'] if dec else 'none'))
    P[n] = res

print('--- (d) PAIRWISE: the kit, the sibling kit, and Seat M1\'s five')
OWN = {n: set(P[n]['paths']) for n in NS}
def paths_of(n):
    h = g('rev-parse', 'refs/g25/pull/' + n).strip(); return set(g('diff', '--name-only', h + '^', h).split())
SIBP = {n: paths_of(n) for n in SIB}; M1P = {n: paths_of(n) for n in M1}
for a, b in itertools.combinations(NS, 2): hard(not (OWN[a] & OWN[b]), 'kit pair #%s/#%s disjoint %s' % (a, b, sorted(OWN[a] & OWN[b]) or ''))
for a in NS:
    for b in SIB: hard(not (OWN[a] & SIBP[b]), '#%s vs sibling-kit #%s disjoint %s' % (a, b, sorted(OWN[a] & SIBP[b]) or ''))
M1OV = {}
for a in NS:
    for b in M1:
        x = sorted(OWN[a] & M1P[b])
        if x:
            M1OV['%s/%s' % (a, b)] = x
            dec = K['declared_overlap'].get(a)
            hard(bool(dec) and dec['by'] == b and x == [dec['path']], 'OVERLAP #%s ∩ M1 #%s = %s — %s' % (a, b, x, 'DECLARED' if dec and dec['by'] == b else 'UNDECLARED'))
print('  M1 overlap census: %s' % (M1OV or 'EMPTY'))

print('--- (e) END_TREE over develop, ALL orders; END_TREE_AFTER_M1 over develop + M1\'s still-open PRs')
def seq(base_tree, order, heads):
    t = base_tree
    for n in order:
        h = heads[n]; par = g('rev-parse', h + '^').strip()
        rc, o, e = gq('merge-tree', '--write-tree', '--merge-base=' + par, t, h)
        if rc != 0: return None
        t = o.split()[0]
    return t
ends = {seq(DT, o, H) for o in itertools.permutations(NS)}
hard(len(ends) == 1 and None not in ends, 'END_TREE identical in all %d orders: %s' % (len(list(itertools.permutations(NS))), sorted(x or 'CONFLICT' for x in ends)))
END = ends.pop() if len(ends) == 1 else None
MH = {n: g('rev-parse', 'refs/g25/pull/' + n).strip() for n in M1}
m1t = seq(DT, m1open, MH) if m1open else DT
hard(m1t is not None, 'develop + M1\'s still-open %s merges clean: tree %s%s' % (m1open or 'none', m1t, (' (== M1\'s expected END tree)' if m1t == K['m1_end_tree'] else ' (!= M1\'s expected END tree %s — REPORTED)' % K['m1_end_tree'][:12])))
ends2 = {seq(m1t, o, H) for o in itertools.permutations(NS)} if m1t else {None}
hard(len(ends2) == 1 and None not in ends2, 'END_TREE_AFTER_M1 identical in all orders: %s' % sorted(x or 'CONFLICT' for x in ends2))
END2 = ends2.pop() if len(ends2) == 1 else None
st = g('diff', '--shortstat', DT, END).strip() if END else ''
print('  END_TREE %s (%s)' % (END, st))

print('--- (f) READ probes (PREDICTIONS for the gate; never evidence)')
def show(c, p): return g('show', '%s:%s' % (c, p))
PROBES = {}
for n in NS:
    h = H[n]; par = P[n]['parent']; out = []
    diff = g('diff', '-U0', par, h)
    if K['prs'][n]['tier'] == 'T3':
        ch = [l[1:] for l in diff.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
        nc = [l for l in ch if not re.match(r'^\s*(//|\*|/\*)', l) and l.strip()]
        out.append('changed lines %d; NON-comment changed lines %d %s (port: a line/prefix read, NOT the emit — the gate owes the emit proof)' % (len(ch), len(nc), nc[:3]))
    if n == '1274':
        f = P[n]['paths']; src = show(h, [p for p in f if p.endswith('index.ts')][0])
        out.append('env bounds: %s' % re.findall(r'const TEAMS_NOTIFY_\w+ = Number\([^;]+\);', src))
        out.append('ENV-NAN: Number("abc") -> NaN; `NaN <= 0` is false so the deadline never trips; Math.min(2000, NaN) = NaN reaches safeOutboundRequest, whose `init.timeoutMs ?? 10_000` keeps NaN and hands it to setTimeout (node treats NaN as 1 ms); LIMIT $2 = NaN reaches Postgres (READ; the gate measures)')
        for sp in ('Blockchain/Dev/docker/init/06-m365-tables.sql', 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts'):
            t = show(h, sp); i = t.find('svc_teams_webhooks ('); out.append('%s: svc_teams_webhooks created_at present %s' % (sp, 'created_at' in t[i:i + 900]))
        mig = gq('grep', '-l', 'svc_teams_webhooks', h, '--', 'Blockchain/Dev/migrations')[1].split()
        out.append('migrations/ naming svc_teams_webhooks: %s (the THIRD schema source, if any — BUILD THE SCHEMA THE PRODUCT DEPLOYS)' % (mig or 'NONE'))
    if n == '1272':
        src = show(h, 'Blockchain/Dev/services/kyc/src/index.ts')
        m = re.search(r'ON CONFLICT[^`]*?DO UPDATE SET([^`]*?)(`|RETURNING)', src, re.S)
        cols = sorted(set(re.findall(r'(\w+)\s*=\s*EXCLUDED\.', m.group(1)))) if m else []
        out.append('dbSaveVerification DO UPDATE SET columns (READ): %s' % (cols or 'NOT PARSED'))
        tst = show(h, [p for p in P[n]['paths'] if '__tests__' in p][0])
        mc = sorted(set(re.findall(r"'(\w+_\w+|status|documents|checks)'", tst)) & set(cols)) if cols else []
        out.append('the test mock names %d of those columns as quoted strings (READ port; the gate compares the mock\'s column list with the SQL itself)' % len(mc))
        out.append('KS-1327 (Backlog): cell S3 pins that status/currentLevel ARE still overwritten at the 3 s timer — a declared limit, NOT a defect of #1272')
    if n == '1269':
        out.append('HDR-THROW: res.setHeader(name, value) throws ERR_INVALID_HTTP_TOKEN / ERR_INVALID_CHAR for a name with a space or a value with CR/LF — inside the error handler (READ; node\'s own validation). Express catches a throw in error middleware and hands it to finalhandler (READ); the gate measures what the client receives')
        out.append('HDR-ON-500: err.headers is applied even when the status was COERCED to 500 (finalhandler applies err.headers only for a 4xx/5xx err.status) — READ')
    if n == '1273':
        out.append('BACKTICK-SPAN: the back-quote branch `[^`]*/?<verb>` matches any back-quoted span that ENDS in the verb (`subversion`, `a new version`) and can pair a CLOSING back-quote with the next opening one — over-reports (the safe direction); READ, the gate measures through the real cell')
    if n == '1271':
        out.append('k6LogMountFor compares RAW strings (no path.resolve) — correct for its derivation (the replace either changes the string or does not); writeGateReport resolves both sides; a SYMLINK to the summary is NOT caught by path.resolve (READ)')
    if n == '1267':
        out.append('the WARN names credentialId (an identifier, not the credential): LOG-CONTENT — the gate reads what else the logger serialises; loadFromDb()\'s silent early return is untouched by design (bare silent returns 2 -> 1)')
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT, 'parent': K['parent'],
       'behind_parent': int(g('rev-list', '--count', '%s..%s' % (K['parent'], DEV)).strip()), 'm1_open': m1open, 'm1_overlap': M1OV,
       'end_tree': END, 'end_tree_after_m1': END2, 'end_shortstat': st, 'orders': len(list(itertools.permutations(NS))), 'prs': P, 'probes': PROBES,
       'sibling_paths': {n: sorted(SIBP[n]) for n in SIB}, 'm1_paths': {n: sorted(M1P[n]) for n in M1}}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | END_TREE_AFTER_M1 %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, END2))
sys.exit(1 if FAIL else 0)
