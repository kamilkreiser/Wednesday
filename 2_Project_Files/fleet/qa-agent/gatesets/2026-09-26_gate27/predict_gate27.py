#!/usr/bin/env python3
"""predict_gate27.py — MEASURE one gate27 kit (the directory this script lives in; its PR set, tiers and commit counts are kit.json beside it)
over origin develop AS READ NOW, and write pins_<kit>.json beside this script. Never adopts a value from a mail or from kit.json (kit.json carries
NO head): every head is read from origin by TWO instruments — `git ls-remote` (READ, from the Secuura checkout) and the GitHub PULLS API — and the
fetch into the scratch clone must agree with both.

Shape copied from gate26's predict_gate26.py and re-keyed for gate27: FOUR rows (#1278 fix round, #1285, #1286, #1287), NO sibling kit (the
sibling set is empty, so END_TREE_WITH_SIBLING == END_TREE by construction), a PER-PR merge-base (#1278 on 4db87c3e, #1285/#1286 on 00de57ba,
#1287 on the current develop) and a DECLARED COMMIT COUNT per PR (#1278 is TWO commits: round 1 by Seat L7 + the fast-forward fix round by Seat
B 30th). The in-flight census is EVERY OTHER OPEN PR at the pin (kit.json `inflight`, read by the PULLS API): hard path-disjoint. ONE open PR is a
DECLARED overlap, not a census row: #1268 (NO GO at its cap, dead-open) carries #1287's one path — kit.json `dead_open_same_blob` — and the
overlap is asserted BYTE-IDENTICAL (the same blob at both heads), never absorbed.

Instruments: `git ls-remote` READ from the Secuura checkout (read verb only); every write verb (clone, fetch, merge-tree --write-tree, hash-object,
commit-tree for a simulation) runs in a scratch BARE clone <scratchpad>/g27_sp/clone.git — `git clone --bare --no-local` FROM the checkout (NO
alternates), then a fetch FROM ORIGIN into THAT clone (the checkout's core.sshCommand exported as GIT_SSH_COMMAND for that fetch only, never
printed). Nothing is written into the checkout.

BASE-INVARIANT per PR over the develop read now: (0) the PR is exactly kit.json's `commits` commits over merge-base(develop, head), with NO merge
commit among them; (1) diff(develop, merged) == EXACTLY the PR's own paths (diff(merge-base, head)), each merged blob byte-equal to the head's blob
(kit.json `declared_overlap` would carry a 3-way target; BOTH gate27 kits declare NONE — measured); (2) numstat(develop -> merged) ==
numstat(merge-base -> head); (3) the develop move since the merge-base ∩ the PR's own paths == EMPTY. NOT STACKED: for every pair in the kit (and
across a sibling kit, if any), neither head is an ancestor of the other and their merge-base is an ancestor of develop (no shared non-develop commit).
PAIRWISE the kit's path sets are DISJOINT (hard), disjoint from the SIBLING kit's (hard: the kits may merge in either order), and disjoint from
Seat B 30th's in-flight PRs and worktree(s) (hard: an overlap must be DECLARED by a re-draft, never absorbed). END_TREE = develop + every PR of
the kit, identical in ALL orders (N! orders, memoised on (tree, PR) so equal states are merged once), and END_TREE_WITH_SIBLING = develop + the
sibling kit + this kit, identical whichever kit lands first. READ probes (PREDICTIONS for the gate, never evidence) are printed per PR.
REFUSES (rc 1) unless every HARD assertion holds. --simulate foreign<n> (n in the kit) builds develop + a FOREIGN edit of that PR's first own
file and must REFUSE; --simulate moved builds develop + an UNRELATED synthetic commit (a new file no PR touches) and must PASS (the base-
invariance of a develop move; gate27 cannot use an OLDER develop: #1287 sits on the current one). A simulation writes
pins_<kit>.SIM-<mode>.json, never the pins.
Usage: predict_gate27.py <scratchpad dir under /private/tmp/claude-501/> [--simulate foreign<n>|moved]
"""
import itertools, json, os, re, subprocess, sys, datetime, tempfile, urllib.request, urllib.error, time

GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN = 'git@github.com:Secuura/Distributed_Secuura.git'
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: predict_gate27.py <scratchpad> [--simulate …]'); sys.exit(9)
SIM = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--simulate' else 'none'
NS = sorted(K['prs']); SIB = K['sibling_batch']; INF = K['inflight']; DOS = K.get('dead_open_same_blob', {})
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
CL = os.path.join(SP, 'g27_sp', 'clone.git')
def g(*a, **kw): return run(['git', '--git-dir', CL] + list(a), **kw)
def gq(*a):
    r = subprocess.run(['git', '--git-dir', CL] + list(a), capture_output=True, text=True); return r.returncode, r.stdout, r.stderr
print('predict_gate27 (%s) %s | simulation %s | scratchpad %s' % (K['kit'], now(), SIM, SP))

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
for n in INF + sorted(DOS): print('  %s #%s (censused, never pinned; its head may move): state %s head %s branch %s' % ('DEAD-OPEN (declared same-blob overlap)' if n in DOS else 'open', n, AP[n]['state'], AP[n]['head']['sha'], AP[n]['head']['ref']))
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
run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/heads/develop:refs/g27/develop']
    + ['+refs/pull/%s/head:refs/g27/pull/%s' % (n, n) for n in NS + SIB + INF + sorted(DOS)] + ['+%s:refs/g27/branch/%s' % (BR[n], n) for n in NS], env=env)
DEV = g('rev-parse', 'refs/g27/develop').strip()
hard(DEV == LS.get('refs/heads/develop'), 'develop %s: fetch == ls-remote' % DEV)
H = {}
for n in NS:
    h = AP[n]['head']['sha']; H[n] = h
    hard(h == LS.get('refs/pull/%s/head' % n) == LS.get(BR[n]) == g('rev-parse', 'refs/g27/pull/' + n).strip() == g('rev-parse', 'refs/g27/branch/' + n).strip(),
         '#%s head %s == API == ls-remote pull/head == ls-remote branch == fetched pull == fetched branch' % (n, h))
REAL_DEV = DEV
if SIM == 'moved':
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input='gate27 SIMULATION: an UNRELATED develop move (a new file no PR touches)\n').strip()
    idx = tempfile.mktemp(prefix='g27idx', dir=os.path.join(SP, 'g27_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, 'GATE27-SIMULATED-MOVE.txt')], env=e2)
    t_ = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t_, '-p', DEV, '-m', 'gate27 SIMULATION moved'], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
    print('  SIMULATION moved: develop := %s (the real develop + one unrelated file GATE27-SIMULATED-MOVE.txt)' % DEV)
elif SIM.startswith('foreign'):
    tn = SIM[7:]
    mb0 = g('merge-base', DEV, H[tn]).strip()
    path = sorted(g('diff', '--name-only', mb0, H[tn]).split())[0]
    rc, blob, _ = gq('rev-parse', '%s:%s' % (DEV, path))
    body = g('cat-file', '-p', blob.strip()) if rc == 0 else ''
    nb = run(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], input=body + '\n# gate27 SIMULATION: a FOREIGN edit on develop (%s)\n' % SIM).strip()
    idx = tempfile.mktemp(prefix='g27idx', dir=os.path.join(SP, 'g27_sp')); e2 = dict(os.environ, GIT_INDEX_FILE=idx)
    run(['git', '--git-dir', CL, 'read-tree', DEV], env=e2); run(['git', '--git-dir', CL, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (nb, path)], env=e2)
    t = run(['git', '--git-dir', CL, 'write-tree'], env=e2).strip()
    DEV = run(['git', '--git-dir', CL, 'commit-tree', t, '-p', DEV, '-m', 'gate27 SIMULATION ' + SIM], env=dict(e2, GIT_AUTHOR_NAME='sim', GIT_AUTHOR_EMAIL='sim@x', GIT_COMMITTER_NAME='sim', GIT_COMMITTER_EMAIL='sim@x')).strip()
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

print('--- (c) NOT STACKED and PAIRWISE: the kit, the sibling kit (none), every other open PR, and the declared dead-open same-blob overlap')
def head_of(n): return H.get(n) or g('rev-parse', 'refs/g27/pull/' + n).strip()
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
for b, decl in sorted(DOS.items()):
    hb = head_of(b); pb = paths_of(b)
    for a in NS:
        ov = sorted(OWN[a] & pb)
        if not ov: continue
        hard(ov == sorted(decl), 'DECLARED overlap #%s x dead-open #%s (head %s): measured %s == declared %s' % (a, b, hb[:12], ov, sorted(decl)))
        for pth in ov:
            ba, bb = blob(H[a], pth), blob(hb, pth)
            hard(ba == bb and ba is not None, 'DECLARED overlap %s: #%s head blob %s == #%s head blob %s (BYTE-IDENTICAL, so the overlap cannot change what lands)' % (pth, a, ba, b, bb))
            DOSR.setdefault(b, []).append({'pr': a, 'path': pth, 'blob_kit': ba, 'blob_dead_open': bb, 'dead_open_head': hb})
    undeclared = [pth for pth in decl if not any(pth in OWN[a] for a in NS)]
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
    if n == '1278':
        r1 = g('rev-parse', h + '^').strip(); rr = 'systemTest/performance/tests/unit/support/readYamlRouting.ts'
        src = show(h, rr)
        out.append('FIX ROUND (READ): round 1 %s + fix %s; the fix touches %s; `collapseImportStatements` left in the head reader: %s; `ts.createSourceFile` calls: %d; `callsReadYaml` exported: %s' % (
            r1[:12], h[:12], g('diff', '--name-only', r1, h).split(), 'collapseImportStatements' in src, src.count('ts.createSourceFile('), 'export function callsReadYaml' in src))
        out.append('AST NODE SHAPES the reader visits (READ): ImportDeclaration, ExportDeclaration, CallExpression(require), CallExpression(import) — NOT ImportEqualsDeclaration (`import y = require(...)`), NOT a require ALIAS (createRequire(import.meta.url)(...)); the gate measures each through the REAL function and says whether each is REAL in this ESM package (type %s)' % (
            'module' if '"type": "module"' in show(h, 'systemTest/performance/package.json') else 'NOT module'))
        out.append('callsReadYaml (READ): Identifier `readYaml` or PropertyAccess `.readYaml` as a CALLEE only — an ALIAS (`const r = readYaml; r(p)`), `readYaml.call(...)` and a call inside a never-invoked function are the shapes to grade (a false red, a false red, an over-report)')
        out.append('typescript in systemTest/performance/package.json at head: %s (READ)' % re.findall(r'"typescript":\s*"[^"]+"', show(h, 'systemTest/performance/package.json')))
        out.append('the refused intermediate push 824edb4882af (format gate FAILED, "the ref did not move") never reached origin — the gate verifies by ls-remote that only %s is on the branch' % h[:12])
    if n == '1285':
        f = 'Blockchain/Dev/scripts/base-image-watch.sh'; src = show(h, f)
        out.append('SELF-TEST CASES (READ, a count of LITERAL `echo "  PASS` lines in %s — run_case rows print theirs from a helper, so this is the DELTA, not the total): base %d, head %d (+2, matching the seat\'s runtime 20 -> 22; drafter_probe1285.sh MEASURED 20 -> 22 under a docker shim, probe1285_1.out); the self-test runs no docker (header :32)' % (
            os.path.basename(f), show(mb, f).count('echo "  PASS'), src.count('echo "  PASS')))
        out.append('FLEET-SUITE MEMBERSHIP (READ): run-shell-suites.sh globs *.test.sh under Blockchain/Dev/scripts/__tests__ and systemTest/__tests__ only; base-image-watch.sh is neither, and `git grep base-image-watch` outside *.md finds it named only by .github/workflows/base-image-refresh.yml comments — so the fleet quadruple is UNCHANGED by path class and its own self-test count (20 -> 22) is a SEPARATE count')
        out.append('mode at head %s (READ: `ls-tree`), at the merge-base %s' % (g('ls-tree', h, '--', f).split()[0], g('ls-tree', mb, '--', f).split()[0]))
        out.append('PRODUCER CALL SITE (READ): the live run pipes `docker run … version --format json | db_age_from_version_json || true`; the function is defined before the self-test and before the call site: %s' % (
            src.index('db_age_from_version_json() {') < src.index('| db_age_from_version_json || true') if 'db_age_from_version_json() {' in src and '| db_age_from_version_json || true' in src else 'NOT FOUND'))
    if n == '1286':
        D = REAL_DEV
        fl = gq('grep', '-n', 'PROVISION_PER_TENANT_DB', D)[1].strip().splitlines()
        mt = gq('grep', '-l', 'MULTI_TENANCY_ENABLED', D, '--', '*.json', '*.bicep', '*.yml', '*.yaml')[1].split()
        out.append('FLAG CENSUS at develop %s (READ, `git grep`): PROVISION_PER_TENANT_DB appears on %d line(s), all in code (%s) — set in NO config file; MULTI_TENANCY_ENABLED appears in config files %s' % (
            D[:12], len(fl), sorted(set(x.split(':')[1] for x in fl)), sorted(x.split(':', 1)[1] for x in mt)))
        out.append('DOC-CLAIM-TWO-FLAGS (a PREDICTION): the PR writes that MULTI_TENANCY_ENABLED and PROVISION_PER_TENANT_DB are "set in NO configuration file" (MULTI-TENANCY.md key points; RLS-FAIL-CLOSED-PLAN.md) — MULTI_TENANCY_ENABLED is "true" in deployment/azure/env.dev.json, env.demo.json and services.bicep (READ above); the gate measures and rules')
        sm = show(D, 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts').splitlines()
        a = [i + 1 for i, l in enumerate(sm) if 'Ensure all tenants have a tenant_config entry' in l]; z = [i + 1 for i, l in enumerate(sm) if 'Platform tenant seed complete' in l]
        out.append('startup-migrations.ts at develop: the tenant_config block opens at line %s and the seed log line is %s — the PR cites :1116-1144 (READ); the block seeds a FIXED list of %d tenant ids at boot' % (a, z, sum(1 for l in sm[(a[0] if a else 0):(z[0] if z else 0)] if re.search(r"^\s*'[0-9a-f-]{36}',", l))))
        tp = show(D, 'Blockchain/Dev/services/tenant-provisioning/src/index.ts').splitlines()
        out.append('ONBOARDING-CITE (a PREDICTION): a NEW tenant\'s tenant_config row is written by tenant-provisioning/src/index.ts (`provisionPerTenantDb` at line(s) %s, the INSERT at line(s) %s), not by startup-migrations.ts, which the corrected onboarding step cites (READ)' % (
            [i + 1 for i, l in enumerate(tp) if 'const provisionPerTenantDb' in l], [i + 1 for i, l in enumerate(tp) if 'INSERT INTO tenant_config' in l]))
        out.append('039_rls_fail_closed.sql present at develop: %s; tenant-pool-manager.ts:151-152 read `%s` (READ)' % (
            gq('cat-file', '-e', '%s:Blockchain/Dev/migrations/039_rls_fail_closed.sql' % D)[0] == 0, ' | '.join(x.strip()[:60] for x in show(D, 'Blockchain/Dev/packages/shared/src/db/tenant-pool-manager.ts').splitlines()[150:152])))
        out.append('head commit message Refs line: %s (unhyphenated own key); PR body Refs: KS-1336 + a foreign KS-1055 (READ)' % re.findall(r'(?m)^Refs .*$', g('log', '-1', '--format=%B', h)))
    if n == '1287':
        ec = 'Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts'; k7 = 'Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'
        out.append('BLOB (READ): head %s | expected 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa -> %s | develop %s | #1268 head %s' % (
            blob(h, ec), 'EXACT' if blob(h, ec) == '8a4ce36a3a96d2e511faf9b19eba14593d8e99fa' else 'DIFFERENT', blob(REAL_DEV, ec), blob(head_of('1268'), ec) if '1268' in DOS else 'n/a'))
        def corpus(c):
            s_ = show(c, k7); o_ = s_.find('const CORPUS = ['); z_ = s_.find('];', o_)
            return re.findall(r"'([^']+)'", s_[o_:z_]) if o_ > -1 else None
        cd, c68 = corpus(REAL_DEV), corpus(head_of('1268')) if '1268' in DOS else None
        out.append('K1b CONTENT COUPLING (READ): K1b reads ks781\'s `const CORPUS = [` from SOURCE TEXT — at develop ks781 is blob %s with %s CORPUS entries; at #1268\'s head (what rounds 1-2 graded against) %s entries; the two literals are %s' % (
            blob(REAL_DEV, k7)[:12], len(cd) if cd else 'NO', len(c68) if c68 else 'NO', 'IDENTICAL' if cd == c68 else 'DIFFERENT'))
    PROBES[n] = out
    for o in out: print('  #%s %s' % (n, o))

res = {'kit': K['kit'], 'measured_at': now(), 'simulation': SIM, 'fail': FAIL, 'develop': DEV, 'develop_tree': DT,
       'end_tree': END, 'end_tree_with_sibling': sib_first, 'end_shortstat': st, 'orders': len(perms), 'merge_tree_calls': len(MEMO), 'prs': P, 'probes': PROBES,
       'sibling_paths': {n: sorted(SIBP[n]) for n in SIB}, 'sibling_heads': {n: head_of(n) for n in SIB},
       'inflight': {n: {'head': head_of(n), 'state': AP[n]['state'], 'paths': sorted(INFP[n])} for n in INF}, 'inflight_worktrees': WT, 'dead_open_same_blob': DOSR}
name = 'pins_%s.json' % K['kit'] if SIM == 'none' else 'pins_%s.SIM-%s.json' % (K['kit'], SIM)
json.dump(res, open(os.path.join(GS, name), 'w'), indent=1)
print('%s: FAIL=%d -> %s | develop %s | END_TREE %s | END_TREE_WITH_SIBLING %s' % ('REFUSED' if FAIL else 'PASS', FAIL, name, DEV[:12], END, sib_first))
sys.exit(1 if FAIL else 0)
