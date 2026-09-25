#!/usr/bin/env python3
"""predict_gate21T2c.py <scratchpad> [--simulate-develop 1221|foreign] — the drafter's MEASUREMENTS for the round-21 THIRD tier-2 batch gate over
#1218 KS-897+KS-896 (ROUND 2), #1219 KS-1277 (T3), #1223 KS-1118 (ROUND 2 — widened in by Wednesday 06:3xZ), #1233 KS-1133 (+KS-1229 R-a),
#1235 KS-1140 GF-1, #1236 KS-1110 A+B, #1237 KS-1229, #1238 KS-1158 (T3) — FROZEN at eight by Wednesday. Every git WRITE verb (clone, fetch, merge-tree --write-tree, commit-tree, read-tree/apply/write-tree in a temp index)
lives in a scratch FULL bare clone FROM ORIGIN under <scratchpad> (over the checkout's own ssh road, read with `config --get` and never printed); the
Secuura checkout is read with `ls-remote` / `config --get` only. Derived from gate21T1b's predict_gate21T1b.py (same base-invariant shape), re-keyed.

BASE-INVARIANT (Wednesday's 04:35Z ANSWER to Seat B 25th, `answer_seatB25_movedbase`): every head was cut from the OLD develop 6ab9d5021 (BASE) and
develop has MOVED. Per PR: (1) diff(develop, merged) == EXACTLY the PR's own paths, each blob byte-equal to the head's blob; (2) numstat(develop ->
merged) == numstat(BASE -> head); (3) the develop move ∩ the PR's OWN paths == EMPTY.
DECLARED OVERLAP (NEW here, measured): #1221 KS-1266 is GO'd (Wednesday 05:36Z) but NOT merged at drafting, and it edits
services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — the one file #1237 edits. If #1221 lands first, (1) and (3) cannot
hold for #1237 by construction. The overlap is accepted ONLY in this exact shape: develop's blob at that path == #1221's head blob d0e886e9 (the move's
change there IS #1221's change and nothing else), the merge is clean, numstat (2) holds, and the +/- lines of diff(develop, merged) on the path equal
the +/- lines of diff(BASE, #1237 head) byte for byte. Anything else on an own path refuses.
--simulate-develop 1221 builds develop+#1221 in the scratch clone and measures over it (a CONTROL of the overlap mode: must pass); --simulate-develop
foreign builds develop + a foreign edit of that file (a NEGATIVE CONTROL: must FAIL on #1237). A simulation writes pins_gate21T2c.SIM-<mode>.txt and
never the real pins. rc 0 only if every HARD assertion holds.

SECOND DECLARED OVERLAP (added 2026-09-25 ~07:5xZ by the finishing drafter, measured): #1225 KS-1291 DEADGUARD squashed as 1ded2f817 (07:32:47Z)
edits services/originate/src/routes/documents.ts — the ONE file #1219 edits (#1225: the create handler's unreachable issuerName '@' guard, hunks at
:610-611 and :841-849, 8+/11-, -3 net lines; #1219: the KS-480 docblock :61-67 and the /revoke PLACEMENT comment :2332-2345 — textually disjoint). Accepted ONLY in the
same exact shape: develop's blob at that path == #1225's squash blob 8331f626 (the move's change there IS #1225's change and nothing else), the merge
clean, numstat (2), +/- lines byte-identical. --simulate-develop foreign1219 builds develop + a foreign edit of documents.ts (a NEGATIVE CONTROL: must
FAIL on #1219)."""
import os, subprocess, sys, datetime, re, tempfile, random, hashlib
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(SP)) and os.path.isdir(SP), 'argv[1] must be a scratchpad dir'
SIM = sys.argv[sys.argv.index('--simulate-develop') + 1] if '--simulate-develop' in sys.argv else ''
assert SIM in ('', '1221', 'foreign', 'foreign1219'), 'unknown simulation ' + SIM
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
D = 'Blockchain/Dev/'
SH = D + 'packages/shared/src/'
OR = D + 'services/originate/src/'
PT = 'systemTest/performance/tests/unit/'
KS1213 = OR + '__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts'
H1221 = '0a561a5db393e8f0ced82b86af572c7231330d64'   # #1221 KS-1266, GO'd 05:36Z, not merged at drafting
H1221_KS1213_BLOB = 'd0e886e959258bc0fa962c03727453eb422196b3'
DOCS_TS = OR + 'routes/documents.ts'
H1225_DOCS_BLOB = '8331f626cd82b977204da3c5193c64df91908ce7'   # #1225 KS-1291's squash 1ded2f817's blob at documents.ts
PRS = [  # seat order: L4 round 2, then L1 (A, D, E, F), then Seat B 25th (6, 7)
    dict(n='1218', key='KS-897', keys=('KS-897', 'KS-896'), tier='T2', head='d971aa4f24665bb192765a0c6e82f719996efb92', ncommits=3,
         br='refs/heads/feature/ks-897-build-fixture-swallows-its-own-failure-l4-fixtureabort-1',
         files={D + 'scripts/__tests__/pre_push_hook_base.test.sh': (50, 7), D + 'scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh': (190, 0)}),
    dict(n='1219', key='KS-1277', tier='T3', head='5d5129a03af0bf1586c26403a453ce283ae0be2f',
         br='refs/heads/feature/ks-1277-stale-obo-comments-l1-a-1',
         files={OR + 'routes/documents.ts': (11, 7)}),
    dict(n='1223', key='KS-1118', tier='T2', head='2892e528630d93a5b1b1482efa6978edce4211f1', ncommits=2,   # ROUND 2: 759726d8d + the P3 drop
         br='refs/heads/feature/ks-1118-verify-hash-precedence-l1-c-1',
         files={OR + 'routes/verification.ts': (8, 3)}),
    dict(n='1233', key='KS-1133', keys=('KS-1133', 'KS-1229'), tier='T2', head='6892124d9304ae014c52f7ea08a17e9468d411bf',
         br='refs/heads/feature/ks-1133-verify-alias-order-spec-l1-d-1',
         files={D + 'docs/openapi/secuura-api.yaml': (20, 6), OR + 'originate.openapi.ts': (19, 5)}),
    dict(n='1235', key='KS-1140', tier='T2', head='1c899947ea31e7a6628f5256174c1c353e6587af',
         br='refs/heads/feature/ks-1140-ks879-guard-the-cell-walks-the-tree-on-its-own-r21-handedlist-1',
         files={SH + '__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts': (33, 3)}),
    dict(n='1236', key='KS-1110', tier='T2', head='4296ba6d090c212d0849f488f882d00a2985245e', ncommits=2,
         br='refs/heads/feature/ks-1110-two-k6-unit-tests-parse-configscenariosyml-with-js-yaml-r21-readyaml-1',
         files={PT + 'config/sheddingCeiling.test.ts': (14, 3), PT + 'package_scripts.test.ts': (13, 3)}),
    dict(n='1237', key='KS-1229', tier='T2', head='cfa16eb70ba28c5833101e39e4e1cb1680b8dd6c',
         br='refs/heads/feature/ks-1229-version-truthy-cell-l1-e-1',
         files={KS1213: (28, 0)}),
    dict(n='1238', key='KS-1158', tier='T3', head='0f3ffbb0947a82b7ec1c2866fd1a82ff4c94b2c1',
         br='refs/heads/feature/ks-1158-stale-header-lines-l1-f-1',
         files={OR + '__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts': (10, 7)}),
]
OVERLAP = {'1237': {KS1213: ('#1221', H1221_KS1213_BLOB)}, '1219': {DOCS_TS: ('#1225', H1225_DOCS_BLOB)}}   # the ONLY accepted own-path overlaps, each only in this exact shape
H = {p['n']: p['head'] for p in PRS}
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(a, env=None, inp=None):
    p = subprocess.run(a, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
print('predict_gate21T2c start', now(), '| SIMULATION: ' + (SIM or 'none (the real read)'))
url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]
ssh = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
ENV = dict(os.environ); ENV['GIT_SSH_COMMAND'] = ssh
print('checkout remote.origin.url:', url, '| core.sshCommand present:', bool(ssh), '(value not printed)')
CL = tempfile.mkdtemp(prefix='g21cclone_', dir=SP); os.rmdir(CL)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('FULL clone FROM ORIGIN rc=%d %s -> %s' % (rc, e[:200], CL)); assert rc == 0
def g(*a, env=None, inp=None): return sh(['git', '--git-dir', CL] + list(a), env=env or ENV, inp=inp)
CE = dict(ENV); CE['GIT_AUTHOR_NAME'] = CE['GIT_COMMITTER_NAME'] = 'x'; CE['GIT_AUTHOR_EMAIL'] = CE['GIT_COMMITTER_EMAIL'] = 'x@x'
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % p['n'] for p in PRS] + [p['br'] for p in PRS] + ['refs/pull/1221/head']
lsr = sh(['git', '-C', REPO, 'ls-remote', 'origin'] + refs)
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s:' % (lsr[0], now())); [print('   ', v, k) for k, v in LS.items()]
spec = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/g21c/%s' % (p['n'], p['n']) for p in PRS] + \
       ['+%s:refs/g21cbr/%s' % (p['br'], p['n']) for p in PRS] + ['+refs/pull/1221/head:refs/g21c/1221']
rc, o, e = g('fetch', '--quiet', 'origin', *spec); print('fetch rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEV = g('rev-parse', 'refs/heads/develop')[1]
print('--- (a) heads and develop (ls-remote, then the fetch)')
hard(DEV == LS.get('refs/heads/develop'), 'develop %s == ls-remote' % DEV)
for p in PRS:
    h = g('rev-parse', 'refs/g21c/' + p['n'])[1]; b = g('rev-parse', 'refs/g21cbr/' + p['n'])[1]
    hard(h == b == LS.get('refs/pull/%s/head' % p['n']) == LS.get(p['br']) == p['head'], '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (p['n'], h))
print('  #1221 (NOT in the batch; the declared overlap) pull head at origin: %s (pinned %s)' % (LS.get('refs/pull/1221/head'), H1221))
REAL_DEV = DEV
if SIM:
    if SIM == '1221':
        t = g('merge-tree', '--write-tree', DEV, H1221)[1].splitlines()[0]
        DEV = g('commit-tree', t, '-p', DEV, '-p', H1221, '-m', 'SIMULATED develop + #1221 (scratch only, never pushed)', env=CE)[1]
    else:
        FP = DOCS_TS if SIM == 'foreign1219' else KS1213
        idx = os.path.join(CL, 'sim.index'); E2 = dict(CE); E2['GIT_INDEX_FILE'] = idx
        sh(['git', '--git-dir', CL, 'read-tree', DEV], env=E2)
        blob = g('cat-file', 'blob', DEV + ':' + FP)[1] + '\n// a FOREIGN edit, not #1221 / #1225\n'
        bo = sh(['git', '--git-dir', CL, 'hash-object', '-w', '--stdin'], env=E2, inp=blob)[1]
        sh(['git', '--git-dir', CL, 'update-index', '--cacheinfo', '100644,%s,%s' % (bo, FP)], env=E2)
        t = sh(['git', '--git-dir', CL, 'write-tree'], env=E2)[1]
        DEV = g('commit-tree', t, '-p', DEV, '-m', 'SIMULATED foreign edit of ' + FP.rsplit('/', 1)[1] + ' (scratch only, never pushed)', env=CE)[1]
    print('  SIMULATED develop (%s): %s over the real develop %s — every check below is over the SIMULATION' % (SIM, DEV, REAL_DEV))
print('--- (b) ancestry and the develop move')
for p in PRS:
    nc = p.get('ncommits', 1); chain_ = g('rev-list', '--parents', BASE + '..' + p['head'])[1].splitlines()
    fp = [l.split()[1:] for l in chain_]
    hard(len(chain_) == nc and all(len(x) == 1 for x in fp) and fp[-1] == [BASE],
         '#%s: %d commit(s), linear, the first one\'s parent == BASE %s (%s)' % (p['n'], nc, BASE[:12], ' <- '.join(l.split()[0][:9] for l in chain_)))
ALL = sorted(set(f for p in PRS for f in p['files']))
anc = g('merge-base', '--is-ancestor', BASE, DEV)[0] == 0; hard(anc, 'develop %s is a DESCENDANT of BASE' % DEV[:12])
BEHIND = int(g('rev-list', '--count', BASE + '..' + DEV)[1]); MOVE = g('diff', '--name-only', BASE, DEV)[1].splitlines()
print('  develop is %d commits ahead of BASE; %d paths changed:' % (BEHIND, len(MOVE))); print('    ' + g('log', '--format=%H %s', BASE + '..' + DEV)[1].replace('\n', '\n    '))
for f in MOVE: print('      moved path', f)
OVL = {}
for p in PRS:
    x = sorted(set(p['files']) & set(MOVE)); allowed = OVERLAP.get(p['n'], {})
    ok_ovl = bool(x) and all(f in allowed and g('rev-parse', DEV + ':' + f)[1] == allowed[f][1] for f in x)
    if ok_ovl: OVL[p['n']] = x
    hard(not x or ok_ovl, '(3) BASE-INVARIANT: the develop move ∩ #%s\'s OWN paths == EMPTY%s (%s)' % (
        p['n'], (' — or ONLY the declared %s overlap with develop\'s blob == %s\'s blob %s' % (list(allowed.values())[0][0], list(allowed.values())[0][0], list(allowed.values())[0][1][:12])) if allowed else '', x))
if OVL: print('  DECLARED OVERLAP(S) ACTIVE:', OVL, '(', '; '.join('#%s x %s blob %s' % (n, OVERLAP[n][f][0], OVERLAP[n][f][1][:12]) for n in OVL for f in OVL[n]), ')')
if not SIM:
    with open(os.path.join(G, 'devlog_gate21T2c.txt'), 'w') as f: f.write(g('log', '--format=%H %s', BASE + '..' + DEV)[1] + '\n')
DEVTREE = g('rev-parse', DEV + '^{tree}')[1]; BASETREE = g('rev-parse', BASE + '^{tree}')[1]
print('  develop tree', DEVTREE, '| BASE tree', BASETREE)
print('--- (c) per-PR numstat, blobs, modes')
BL = {}; BB = {}; NS = {}
for p in PRS:
    ns = g('diff', '--numstat', BASE, p['head'])[1]; rows = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in ns.splitlines()}; NS[p['n']] = rows
    print('  #%s %s: %d files +%d/-%d' % (p['n'], p['key'], len(rows), sum(a for a, _ in rows.values()), sum(d for _, d in rows.values())))
    hard(rows == p['files'], '#%s numstat == the pinned file set and counts' % p['n'])
    for f in sorted(p['files']):
        ls = g('ls-tree', p['head'], '--', f)[1].split(); BL[f] = (ls[2], ls[0])
        lb = g('ls-tree', BASE, '--', f)[1].split(); BB[f] = lb[2] if lb else 'ABSENT'
        print('    %s %s #%s (BASE %s%s) %s' % (ls[0], ls[2], p['n'], BB[f][:12], (' mode ' + lb[0]) if lb else '', f))
        hard(ls[0] == '100644' and (not lb or lb[0] == ls[0]), f + ' mode 100644 at head, unchanged from BASE (the .sh files are run as `bash <file>`, not exec)')
print('--- (d) disjointness, surfaces, dependency files, raw control bytes')
for i, a in enumerate(PRS):
    for b in PRS[i + 1:]:
        x = set(a['files']) & set(b['files']); hard(not x, '#%s ∩ #%s = EMPTY (%s)' % (a['n'], b['n'], sorted(x)))
for p in PRS:
    dep = [f for f in p['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json)$', f)]
    hard(not dep, '#%s: NO package.json / lockfile / tsconfig in the PR (%s)' % (p['n'], dep))
hard(bool([f for f in MOVE if f.endswith('package-lock.json')]), 'CONTROL: the dependency-file regex instrument has something to see — the develop move carries lockfiles (applied to the MOVE only as a control)')
SURF = re.compile(r'(\.openapi\.ts$|/docs/openapi/|/routes/|docker-compose|/Dockerfile$|/index\.ts$)')
for p in PRS:
    s = [f for f in p['files'] if SURF.search(f)]
    print('  #%s surface-shaped paths (route / spec / served-spec / entrypoint): %s' % (p['n'], s or 'none'))
hard([f for p in PRS for f in p['files'] if SURF.search(f)] == [OR + 'routes/documents.ts', OR + 'routes/verification.ts', D + 'docs/openapi/secuura-api.yaml', OR + 'originate.openapi.ts'],
     'surface census: ONLY #1219\'s documents.ts and #1223\'s verification.ts (both comment-only claims) and #1233\'s yaml + originate.openapi.ts carry surface-shaped paths')
CTRL = re.compile(rb'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
def blob_bytes(sha): return subprocess.run(['git', '--git-dir', CL, 'cat-file', 'blob', sha], capture_output=True, env=ENV).stdout
hits = {f: len(CTRL.findall(blob_bytes(BL[f][0]))) for f in ALL}
print('  raw C0/DEL bytes (not \\t \\n \\r) per batch blob at its head:', {f.rsplit('/', 1)[1]: n for f, n in hits.items()})
hard(all(n == 0 for n in hits.values()), 'no batch blob adds a raw control byte (so #1235\'s ks879 walk over the END_TREE should see no NEW offender — a prediction)')
hard(len(CTRL.findall(b'a\x00b\tc\n')) == 1, 'CONTROL: the same control-byte instrument counts a planted NUL (1) and ignores \\t \\n')
print('--- (e) BASE-INVARIANT merged trees over the develop just read + END_TREE in three orders + a second instrument')
MT = {}; MB = {}
def pm(a, b, f):   # the +/- lines of diff(a, b) on f, headers dropped
    d = g('diff', '-U0', a, b, '--', f)[1].splitlines()
    return [l for l in d if l[:1] in '+-' and not l.startswith(('+++', '---'))]
for p in PRS:
    r = g('merge-tree', '--write-tree', DEV, p['head']); t = r[1].splitlines()[0] if r[1] else ''; MT[p['n']] = t
    print('  #%s merge-tree rc %d -> %s' % (p['n'], r[0], t)); hard(r[0] == 0, '#%s merges clean over develop' % p['n'])
    dn = sorted(g('diff', '--name-only', DEV, t)[1].splitlines())
    hard(dn == sorted(p['files']), '(1) BASE-INVARIANT: diff(develop, #%s merged) == EXACTLY its own %d paths (got %d)' % (p['n'], len(p['files']), len(dn)))
    for f in p['files']:
        mb = g('rev-parse', t + ':' + f)[1]; MB[f] = mb
        if f in OVL.get(p['n'], []):
            hard(pm(DEV, t, f) == pm(BASE, p['head'], f), '(1\') DECLARED OVERLAP #%s: the +/- lines of diff(develop, merged) == those of diff(BASE, head), byte for byte (%d lines): %s' % (p['n'], len(pm(BASE, p['head'], f)), f[len(D):]))
            print('       merged blob %s (head blob %s — differs by %s\'s hunks, as declared)' % (mb, BL[f][0], OVERLAP[p['n']][f][0]))
        else:
            hard(mb == BL[f][0], '(1) #%s merged blob == head blob: %s' % (p['n'], f.replace(D, '')))
    dns = {r_.split('\t')[2]: (int(r_.split('\t')[0]), int(r_.split('\t')[1])) for r_ in g('diff', '--numstat', DEV, t)[1].splitlines()}
    hard(dns == NS[p['n']], '(2) BASE-INVARIANT: numstat(develop -> merged) == numstat(BASE -> head) for #%s' % p['n'])
def chain(order):
    cur = DEV
    for n in order:
        r = g('merge-tree', '--write-tree', cur, H[n])
        if r[0] != 0: return 'CONFLICT@' + n
        t = r[1].splitlines()[0]; cur = g('commit-tree', t, '-p', cur, '-p', H[n], '-m', 'g21c chain (scratch only)', env=CE)[1]
    return g('rev-parse', cur + '^{tree}')[1]
orders = [[p['n'] for p in PRS]]; orders.append(list(reversed(orders[0]))); sh_ = list(orders[0]); random.Random(21).shuffle(sh_)
if sh_ in orders: sh_ = orders[0][1:] + orders[0][:1]
orders.append(sh_)
ENDS = [chain(o) for o in orders]
for o, t in zip(orders, ENDS): print('  END_TREE order %s -> %s' % (','.join(o), t))
hard(len(set(ENDS)) == 1 and not ENDS[0].startswith('CONFLICT') and len(set(map(tuple, orders))) == 3, 'END_TREE identical in three DISTINCT orders')
END = ENDS[0]
idx = os.path.join(CL, 'g21c.index'); E2 = dict(ENV); E2['GIT_INDEX_FILE'] = idx
sh(['git', '--git-dir', CL, 'read-tree', DEVTREE], env=E2)
for p in PRS:
    patch = g('diff', '--binary', '--full-index', BASE, p['head'])[1] + '\n'
    ap = sh(['git', '--git-dir', CL, 'apply', '--cached', '-'], env=E2, inp=patch)   # a declared-overlap patch applies at an OFFSET (#1221's lines above it)
    print('  apply --cached #%s rc %d %s' % (p['n'], ap[0], ap[2][:120]))
    hard(ap[0] == 0, 'second instrument: apply --cached of #%s BASE..head onto develop\'s tree rc 0' % p['n'])
AT = sh(['git', '--git-dir', CL, 'write-tree'], env=E2)[1]
hard(AT == END, 'second instrument (apply --cached) == END_TREE: %s' % AT)
st = g('diff', '--shortstat', DEV, END)[1]; print('  develop -> END_TREE:', st)
hard(sorted(g('diff', '--name-only', DEV, END)[1].splitlines()) == ALL, 'END_TREE diff vs develop == the union of the %d batch paths' % len(ALL))
for f in ALL: hard(g('rev-parse', END + ':' + f)[1] == MB[f], 'END_TREE %s == its PR\'s merged blob%s' % (f.replace(D, ''), '' if MB[f] == BL[f][0] else ' (the declared overlap)'))
print('--- (f) #1218 ROUND 2: build_fixture under errexit, the status on its own line, the cd guard; the new guard suite')
PH = D + 'scripts/__tests__/pre_push_hook_base.test.sh'; FG = D + 'scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh'
R1 = g('rev-parse', H['1218'] + '~1')[1]
hard(R1 == '999623d28f7cc3f11140cf379cfd3169e6530b57', '#1218: the round-2 commit sits on the round-1 head 999623d28 (the gated round-1 bytes are its parent)')
sub = g('cat-file', 'blob', H['1218'] + ':' + PH)[1] + '\n'; sub1 = g('cat-file', 'blob', R1 + ':' + PH)[1] + '\n'
m = re.search(r'\nbuild_fixture\(\) \{\n([\s\S]*?)\n\}\n', sub); bf = m.group(1) if m else ''
body = re.search(r'\n  \(\n([\s\S]*?)\n  \) >"\$WORK/build\.log" 2>&1\n', '\n' + bf + '\n')
raw_ = (body.group(1) if body else '').splitlines(); code = []; inhd = False
for l in raw_:   # drop comments AND the heredoc stub's lines (they are the stub file's CONTENT, not commands of the subshell)
    if inhd:
        if l.strip() == 'GATE_STUB': inhd = False
        continue
    if "<<'GATE_STUB'" in l: inhd = True
    if l.strip() and not l.strip().startswith('#'): code.append(l)
hard(bool(body), '#1218: the fixture subshell `( … ) >"$WORK/build.log" 2>&1` found at the head')
hard(code[:4] == ['    set -e', '    rm -rf "$root"', '    mkdir -p "$root"', '    cd "$root" || exit 2'],
     '#1218: the subshell OPENS with `set -e`, then rm -rf / mkdir -p "$root", then `cd "$root" || exit 2` — before any git verb (%s)' % code[:4])
hard('\n  _bf_rc=$?\n' in bf and ') >"$WORK/build.log" 2>&1 || {' not in sub, '#1218: the status is read on its OWN line (`_bf_rc=$?`) and `) … || {` is gone')
hard('    echo "FIXTURE BUILD FAILED for $root (mode=$mode, rc=$_bf_rc) — build log follows:" >&2' in bf, '#1218: the abort line STARTS with `FIXTURE BUILD FAILED` and goes to stderr')
git_before_cd = [l for l in code[:code.index('    cd "$root" || exit 2')] if re.search(r'\bgit\b', l)] if '    cd "$root" || exit 2' in code else ['NO CD']
hard(git_before_cd == [], '#1218: no git verb precedes the cd guard inside the subshell')
exempt = [l.strip() for l in code if re.search(r'&&|\|\||(?<![|])\|(?![|])|^\s*!\s', l) and l.strip() != 'cd "$root" || exit 2']
print('  subshell body: %d command lines (heredoc content excluded); errexit-EXEMPT shapes (&&, ||, |, !) other than the cd guard: %s' % (len(code), exempt or 'none'))
hard(exempt == [] and len(code) > 20, '#1218: no &&/||/pipeline/! command inside the errexit body could swallow a mid-build failure')
hard(bool(re.search(r'&&|\|\|', "[ -f x ] && { echo y; }")), 'CONTROL: the exempt-shape instrument sees an && list')
calls = re.findall(r'^.*\bbuild_fixture\b.*$', sub, re.M)
bare = [c for c in calls if re.fullmatch(r'build_fixture "\$WORK/c\d+" (with|no)-develop', c)]
print('  build_fixture mentions %d; bare column-0 calls %d; definition 1; comment lines %d' % (len(calls), len(bare), len([c for c in calls if c.lstrip().startswith('#')])))
hard(len(bare) == 12 and all(c in bare or c.lstrip().startswith('#') or c.startswith('build_fixture() {') for c in calls),
     '#1218: all 12 calls are BARE statements (none inside if/||/&&/$( ) — errexit is not suspended at any call site)')
hard(sub.count('git init -q -b main "$root/seed"') == 1 == sub1.count('git init -q -b main "$root/seed"') and
     sub.count('build_fixture "$WORK/c0" with-develop') == 1 == sub1.count('build_fixture "$WORK/c0" with-develop'),
     '#1218: the guard\'s two sed anchors (CELL 1 mid-build `false`, CELL 2 `/dev/null/nope` root) each match ONCE at the head AND at the round-1 head (so SUBJ_SH can point at either)')
fg = g('cat-file', 'blob', H['1218'] + ':' + FG)[1] + '\n'
nok = len(re.findall(r'^  ok "', fg, re.M)); nbad = len(re.findall(r'^  bad "', fg, re.M))
print('  guard suite: ok-cells %d, bad-arms %d; `cd "$SR"` runs %d; unanchored grep of the abort string %d; lines STARTING with it %d' % (
    nok, nbad, fg.count('cd "$SR'), fg.count("grep -c 'FIXTURE BUILD FAILED'"), len(re.findall(r'^FIXTURE BUILD FAILED', fg, re.M))))
hard(nok == 6 and nbad == 6, '#1218: the guard suite has 6 cells, each with its fail arm')
hard(len(re.findall(r'^FIXTURE BUILD FAILED', fg, re.M)) == 0 and 'echo "FIXTURE BUILD FAILED' not in fg, '#1218: the guard suite never PRINTS the abort string itself (L4\'s label fix; the 05:48Z line-start predicate)')
hard('git init -q --bare -b main "$b/origin.git"' in fg and 'git -C "$r" remote add origin "$b/origin.git"' in fg, '#1218: the guard\'s scratch repos push only to a LOCAL bare origin under $WORK')
hard('cat "$1/.git/config"' in fg and 'for-each-ref' in fg and 'status' not in re.search(r'repo_state\(\) \{[\s\S]*?\n\}', fg).group(0),
     '#1218: the guard\'s repo_state hashes HEAD + refs + config ONLY (not the worktree, index or hooks — a NOT-PINNED lead for the gate)')
roots = ['Blockchain/Dev/scripts/__tests__', 'systemTest/__tests__']
def nsuites(rev): return sum(1 for f in g('ls-tree', '-r', '--name-only', rev, '--', *roots)[1].splitlines() if re.fullmatch(r'[^/]+\.test\.sh', f.rsplit('/', 1)[1]) and f.rsplit('/', 1)[0] in roots)
SD, SE = nsuites(DEV), nsuites(END)
print('  run-shell-suites.sh discovery (its ROOTS glob `*.test.sh`, read statically): develop %d suites -> END_TREE %d' % (SD, SE))
hard(SE == SD + 1, '#1218: the runner will discover exactly ONE more suite after the merge (the guard) — 57 -> 58 expected')
print('--- (g) comment-only instrument for the two tier-3 PRs (#1219 product file, #1238 test header) — the GATE owes the AST equivalence')
def comment_like(l): s = l[1:].strip(); return s == '' or s.startswith(('//', '*', '/*', '*/'))
for n, f in (('1219', OR + 'routes/documents.ts'), ('1223', OR + 'routes/verification.ts'), ('1238', OR + '__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts')):
    ch = pm(BASE, H[n], f); nc = [l for l in ch if not comment_like(l)]
    b0, h0 = g('cat-file', 'blob', BASE + ':' + f)[1], g('cat-file', 'blob', H[n] + ':' + f)[1]
    print('  #%s changed lines %d, NON-comment-looking %d %s | block-comment tokens /* %d->%d, */ %d->%d' % (n, len(ch), len(nc), nc[:3], b0.count('/*'), h0.count('/*'), b0.count('*/'), h0.count('*/')))
    hard(not nc and b0.count('/*') == h0.count('/*') and b0.count('*/') == h0.count('*/'), '#%s: every changed line is comment-shaped and the block-comment token counts are unchanged (a LINE instrument; the AST equivalence is the gate\'s)' % n)
ctl = [l for l in pm(BASE, H['1237'], KS1213) if not comment_like(l)]
hard(len(ctl) > 0, 'CONTROL: the same instrument scores %d non-comment lines on #1237\'s code-bearing diff' % len(ctl))
print('--- (h) #1219: the claims its new comments make')
DOC = OR + 'routes/documents.ts'
for lab, rev in (('BASE', BASE), ('#1219', H['1219']), ('#1219 MERGED over develop', MT['1219'])):
    t = g('cat-file', 'blob', rev + ':' + DOC)[1]; L = t.splitlines()
    cs = [i + 1 for i, l in enumerate(L) if 'await checkOnBehalfOf(' in l]; rs = [i + 1 for i, l in enumerate(L) if re.search(r'^\s*recordOnBehalfOf\(', l)]
    print('  %s: checkOnBehalfOf call lines %s | recordOnBehalfOf call lines %s' % (lab, cs, rs))
    hard(len(cs) == 4 and len(rs) == 4, '%s: checkOnBehalfOf has exactly FOUR call sites and recordOnBehalfOf four (the comment\'s "those four routes and no others")' % lab)
    routes = [(i + 1, re.search(r"'(/[^']*)'", L[i + 1] if i + 1 < len(L) else '') or re.search(r"'(/[^']*)'", l)) for i, l in enumerate(L) if re.match(r'^documentsRouter\.(post|get|put|patch|delete)\(', l)]
    def route_of(ln):
        prev = [(a, m_.group(1) if m_ else '?') for a, m_ in routes if a <= ln]; return prev[-1][1] if prev else '?'
    print('  %s: the four call sites\' routes: %s' % (lab, [route_of(c) for c in cs]))
    hard(sorted(route_of(c).rsplit('/', 1)[-1] for c in cs) == ['revoke', 'share', 'transfer-custody', 'version'], '%s: the four callers are /transfer-custody, /version, /share, /revoke — NOT /lifecycle-events' % lab)
h19 = g('cat-file', 'blob', H['1219'] + ':' + DOC)[1]
cob = re.search(r'\nasync function checkOnBehalfOf\([\s\S]*?\n\}\n', h19) or re.search(r'\n(export )?(async )?function checkOnBehalfOf\b[\s\S]*?\n\}\n', h19)
hard(bool(cob) and 'action_provenance' not in re.sub(r'//.*|/\*[\s\S]*?\*/', '', cob.group(0)) and 'recordOnBehalfOf(' not in cob.group(0),
     '#1219: checkOnBehalfOf\'s code writes NOTHING (no action_provenance, no recordOnBehalfOf call) — the comment\'s "Since KS-1228 it appends NOTHING"')
kp = re.search(r'KS-564: also RETURNS[\s\S]*?\*/', h19)
print('  #1219 lead: the KS-564 paragraph at the head STILL names `/lifecycle-events`: %s — read against the new "does not call the hook" sentence (the gate rules)' % (bool(kp) and '/lifecycle-events' in kp.group(0)))
print('--- (h2) #1223 ROUND 2: P3 dropped; the net diff is the one product comment; the T5 anchor; #1149\'s pin; v1/v2 chains vs #1233\'s text')
VF = OR + 'routes/verification.ts'; K1103 = OR + '__tests__/ks1103-verify-hash-field.test.ts'; K1149 = OR + '__tests__/ks1118-verify-documenthash-over-hash.test.ts'
r1_23 = g('rev-parse', H['1223'] + '~1')[1]
hard(r1_23 == '759726d8d046e6098e720d4768c87e114d0c363c', '#1223: the round-2 commit sits on the round-1 head 759726d8d (a fast-forward, no force)')
hard(g('rev-parse', H['1223'] + ':' + K1103)[1] == g('rev-parse', BASE + ':' + K1103)[1] != g('rev-parse', r1_23 + ':' + K1103)[1],
     '#1223: ks1103 at the head == its BASE blob (P3 DROPPED, net zero) and != the round-1 blob (control: round 1 did change it)')
hard(g('rev-parse', H['1223'] + ':' + VF)[1] == g('rev-parse', r1_23 + ':' + VF)[1], '#1223: verification.ts at the head == its round-1 blob (F-3a unchanged since the round-1 gate confirmed it AST-equivalent)')
CHAIN1 = 'const hashToVerify = providedHash || contentHash || documentHash || hash;'
for lab, rev in (('BASE', BASE), ('#1223', H['1223']), ('develop', DEV)):
    L_ = g('cat-file', 'blob', rev + ':' + VF)[1].splitlines(); at = [i + 1 for i, l in enumerate(L_) if l.strip() == CHAIN1]
    print('  v1 alias chain (the T5 plant site) at %s: line %s' % (lab, at)); hard(len(at) == 1, '%s: the v1 chain `%s` appears exactly once' % (lab, CHAIN1))
hard(bool(g('ls-tree', DEV, '--', K1149)[1]) and bool(g('ls-tree', BASE, '--', K1149)[1]), '#1149\'s pin ks1118-verify-documenthash-over-hash.test.ts is present at BASE and at develop (the reds T5 must produce)')
k49 = g('cat-file', 'blob', BASE + ':' + K1149)[1]
print('  #1149 file: it/test cells %d' % len(re.findall(r'^\s*(it|test)(\.each\([^)]*\))?\(', k49, re.M)))
v2 = g('cat-file', 'blob', DEV + ':' + OR + 'routes/verificationV2.ts')[1]
v2c = re.findall(r'hash\s*\|\|\s*providedHash\s*\|\|\s*contentHash\s*\|\|\s*documentHash', v2)
hard(len(v2c) >= 1, 'v2 reads `hash || providedHash || contentHash || documentHash` at develop (#1233\'s "hash FIRST on v2" text is consistent; control: the v1 chain above reads hash LAST)')
print('--- (i) #1238: the corrected citations against anchorStateSync.ts')
AS = OR + 'services/anchorStateSync.ts'
ab = g('cat-file', 'blob', BASE + ':' + AS)[1].splitlines()
CITE = {329: "const inFlight = bc.status !== 'anchor_failed' && bc.status !== 'confirmed';", 331: 'if (!inFlight && !failed) return document;',
        342: 'if (confirmed && txHash) {', 358: "if (inFlight && anchor.status === 'failed') {", 378: 'if (inFlight && !bc.txHash && simFields.simulated) {'}
for ln, want in CITE.items(): hard(ab[ln - 1].strip() == want, '#1238: anchorStateSync.ts:%d at BASE reads `%s`' % (ln, want))
hard(AS not in MOVE and g('rev-parse', DEV + ':' + AS)[1] == g('rev-parse', BASE + ':' + AS)[1], '#1238: anchorStateSync.ts is byte-identical BASE -> develop (the citations hold on the merged tree too)')
t38 = g('cat-file', 'blob', H['1238'] + ':' + OR + '__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts')[1]
old = [c for c in (':283', ':285', ':296', ':~315', ':325') if c in t38]
print('  #1238 head: stale citations still present %s; `d4cf7e3cf` occurrences %d' % (old, t38.count('d4cf7e3cf')))
hard(old == [] and t38.count('d4cf7e3cf') == 2, '#1238: all five stale citations read 0 and `d4cf7e3cf` reads 2 (the READY\'s residual check)')
old_at = g('cat-file', 'blob', 'd4cf7e3cf:' + AS)[1].splitlines()
for ln, what in ((283, 'const inFlight ='), (285, 'if (!inFlight && !failed)'), (296, 'if (confirmed && txHash)'), (325, 'if (inFlight && simFields.simulated)')):
    at = [i + 1 for i, l in enumerate(old_at) if what in l]
    print('  record correction at d4cf7e3cf: the old header said :%d for `%s` — the file there has it at %s' % (ln, what, at))
print('--- (j) #1233: the four descriptions; yaml == its source; the sign-wallet BAD_REQUEST is real')
Y = D + 'docs/openapi/secuura-api.yaml'; OT = OR + 'originate.openapi.ts'
yh, yb = g('cat-file', 'blob', H['1233'] + ':' + Y)[1], g('cat-file', 'blob', BASE + ':' + Y)[1]
# predict_1 FAILED here on the drafter's own instrument: the yaml FOLDS long descriptions across lines ("HASH ALIAS\n        ORDER"), so a raw
# substring count read 1 for 2. Counts are now taken over whitespace-normalised text (the folded scalar's own semantics).
yh, yb = re.sub(r'\s+', ' ', yh), re.sub(r'\s+', ' ', yb)
hard(yh.count('HASH ALIAS ORDER') == 2 and yh.count('HASH ALIAS order') == 1 and yb.count('HASH ALIAS') == 0, '#1233: the yaml carries the alias-order text on both verify routes + VerifyRequest (2 + 1); BASE 0 (control)')
hard(not [f for f in MOVE if f.endswith('.openapi.ts') or '/docs/openapi/' in f], 'the develop move touches NO *.openapi.ts and NO docs/openapi/ path (check:openapi on the merged tree should equal the head\'s — the gate MEASURES it)')
ot = g('cat-file', 'blob', H['1233'] + ':' + OT)[1].splitlines()
i400 = [i for i, l in enumerate(ot) if 'or BAD_REQUEST (KS-1213' in l]
pth = [re.search(r"path: '([^']+)'", ot[j]).group(1) for j in range(i400[0], 0, -1) if re.search(r"path: '([^']+)'", ot[j])][:1] if i400 else []
print('  #1233: the BAD_REQUEST 400 sits in the registerPath whose path is', pth)
hard(pth and pth[0].endswith('/sign-wallet'), '#1233: the new BAD_REQUEST 400 description is on the sign-wallet operation (KS-1229 R-a)')
dl = g('cat-file', 'blob', BASE + ':' + DOC)[1].splitlines()
gs = [i + 1 for i, l in enumerate(dl) if 'if (metadata.documentType !== undefined && metadata.documentType !== source.type) {' in l]
def route_at(lines, ln):
    for j in range(ln - 1, 0, -1):
        if re.match(r'^documentsRouter\.(post|get|put|patch|delete)\(', lines[j - 1]):
            m_ = re.search(r"'(/[^']*)'", lines[j]) or re.search(r"'(/[^']*)'", lines[j - 1]); return m_.group(1) if m_ else '?'
    return '?'
groutes = [(ln, route_at(dl, ln)) for ln in gs]
print('  the documentType PRESENCE guard at BASE (documents.ts): %s' % groutes)
hard(len(gs) == 3 and any(r_.endswith('/sign-wallet') for _, r_ in groutes) and any(r_.endswith('/version') for _, r_ in groutes),
     'the guard shape sits at THREE sites incl. /version and /sign-wallet (so #1233\'s BAD_REQUEST is a real answer, and #1237\'s tamper must touch /version ONLY)')
print('--- (k) #1235 / #1236: the PR bytes == the local-model checker\'s canonical patches (PASS 7/7, held READYs)')
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
def apply_at(rev, patch_path, opts, f):
    idx2 = os.path.join(CL, 'lm.index'); E3 = dict(ENV); E3['GIT_INDEX_FILE'] = idx2
    sh(['git', '--git-dir', CL, 'read-tree', rev], env=E3)
    a = sh(['git', '--git-dir', CL, 'apply', '--cached', '-p1'] + opts + [patch_path], env=E3)
    t = sh(['git', '--git-dir', CL, 'write-tree'], env=E3)[1]
    return a[0], g('rev-parse', t + ':' + f)[1], a[2][:160]
K79 = SH + '__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts'
rc_, b_, e_ = apply_at(BASE, LM + '2026-09-25_ks1140-ornith35b-night/out.md.checker/patch.diff', ['--recount', '--ignore-whitespace'], K79)
print('  KS-1140 canonical patch at BASE (--recount --ignore-whitespace, the checker\'s recorded mode) rc %d -> %s %s' % (rc_, b_, e_))
hard(rc_ == 0 and b_ == BL[K79][0], '#1235: the head blob == the checker-passed canonical patch applied at BASE (the PR is the local model\'s bytes, no hand edit)')
C1236A = g('rev-list', '--reverse', BASE + '..' + H['1236'])[1].split()[0]
SC = PT + 'config/sheddingCeiling.test.ts'; PS = PT + 'package_scripts.test.ts'
rc_, b_, e_ = apply_at(BASE, LM + '2026-09-25_ks1110-ornith35b-night/out.md.checker/patch.diff', [], SC)
hard(rc_ == 0 and b_ == BL[SC][0] == g('rev-parse', C1236A + ':' + SC)[1], '#1236 A: sheddingCeiling blob == the canonical patch (strict) at BASE == commit %s\'s blob' % C1236A[:9])
rc_, b_, e_ = apply_at(C1236A, LM + '2026-09-25_ks1110-ornith35b-night2/out.md.checker/patch.diff', [], PS)
hard(rc_ == 0 and b_ == BL[PS][0], '#1236 B: package_scripts blob == the canonical patch (strict) applied on commit A')
yb2 = g('cat-file', 'blob', H['1236'] + ':systemTest/performance/utils/yaml.ts')[1]
hard('export function readYaml(filepath: string): unknown {' in yb2 and 'systemTest/performance/utils/yaml.ts' not in MOVE, '#1236: readYaml exists and the develop move leaves utils/yaml.ts untouched')
tc = g('cat-file', 'blob', H['1236'] + ':systemTest/performance/tsconfig.json')[1]
print('  #1236: tsconfig `exclude` names `tests` (so `npm run lint`\'s tsc does NOT typecheck these files):', '"tests"' in tc, '| allowImportingTsExtensions true:', '"allowImportingTsExtensions": true' in tc)
jy = [f for f in g('grep', '-l', 'js-yaml', H['1236'], '--', 'systemTest/performance/tests')[1].splitlines()]
print('  #1236: test files still importing js-yaml directly at the head:', [f.split(':', 1)[1] for f in jy], '(KS-1110 names TWO files; the third is out of its scope — the gate says whether it is a sibling)')
print('--- (l) #1237 against #1221 (the declared overlap, measured both ways)')
gh_ = g('rev-parse', DEV + ':' + KS1213)[1]
print('  develop\'s ks1213 blob %s (BASE %s, #1221 head %s)' % (gh_, BB[KS1213], H1221_KS1213_BLOB))
t21 = g('merge-tree', '--write-tree', REAL_DEV, H1221)[1].splitlines()[0]; d21 = g('commit-tree', t21, '-p', REAL_DEV, '-p', H1221, '-m', 'g21c: real develop + #1221 (scratch only)', env=CE)[1]
r = g('merge-tree', '--write-tree', d21, H['1237']); t = r[1].splitlines()[0] if r[1] else ''
print('  #1237 over (the real develop + #1221) rc %d -> tree %s; ks1213 blob %s; numstat %s' % (r[0], t, g('rev-parse', t + ':' + KS1213)[1], g('diff', '--numstat', d21, t)[1].replace('\t', ' ')))
hard(r[0] == 0 and pm(d21, t, KS1213) == pm(BASE, H['1237'], KS1213), '#1237 merges CLEAN over develop+#1221 with its own hunk byte-identical (the order #1221-then-#1237 is safe)')
KS1213_OVER_1221 = g('rev-parse', t + ':' + KS1213)[1]
print('--- (m) branch names through the hyphenated-key scanner (own key only)')
for p in PRS:
    ks = sorted(set(re.findall(r'(?i)\bks-(\d+)\b', p['br']))); hard(ks == [p['key'].split('-')[1]], '#%s branch keys %s == own %s' % (p['n'], ks, p['key']))
out = 'pins_gate21T2c.txt' if not SIM else 'pins_gate21T2c.SIM-%s.txt' % SIM
with open(os.path.join(G, out), 'w') as f:
    for k, v in [('MEASURED_AT', now()), ('SIMULATION', SIM or 'none'), ('BASE', BASE), ('BASE_TREE', BASETREE), ('DEVELOP', DEV), ('DEVELOP_TREE', DEVTREE),
                 ('BEHIND', BEHIND), ('END_TREE', END), ('END_SHORTSTAT', st), ('MOVE_PATHS', len(MOVE)), ('OVERLAP', ','.join(sorted(OVL)) or 'none'),
                 ('SUITES_DEV', SD), ('SUITES_END', SE), ('KS1213_OVER_1221', KS1213_OVER_1221)] + \
                [('HEAD_' + p['n'], p['head']) for p in PRS] + [('MERGED_' + n, t_) for n, t_ in MT.items()] + \
                [('BLOB|' + f_, '%s %s' % BL[f_]) for f_ in ALL] + [('BASEBLOB|' + f_, BB[f_]) for f_ in ALL] + [('MERGEDBLOB|' + f_, MB[f_]) for f_ in ALL] + [('FAIL', len(FAIL))]:
        f.write('%s=%s\n' % (k, v))
print('wrote', out); print('scratch clone', CL); print('HARD FAILS:', len(FAIL), FAIL); print('done', now())
sys.exit(1 if FAIL else 0)
