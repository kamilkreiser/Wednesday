#!/usr/bin/env python3
"""predict_gate21T2.py <scratchpad> — the drafter's MEASUREMENTS for the round-21 TIER-2 batch gate over #1215 KS-1288, #1218 KS-897+KS-896,
#1220 KS-1129, #1221 KS-1266, #1222 KS-1181 F2, #1223 KS-1118 (#1222/#1223 added by Wednesday mid-draft; FROZEN at six). Every git WRITE verb (clone, fetch, merge-tree --write-tree, commit-tree, read-tree/apply/write-tree in a temp index)
lives in a scratch bare clone FROM ORIGIN under <scratchpad> (blob:none, over the checkout's own ssh road, read with `config --get` and never
printed); the Secuura checkout is read with `ls-remote` / `config --get` only. Derived from gate21T1's predict_gate21T1.py, re-keyed.
Measures: (a) develop + the four pull heads + branches, ls-remote then the fetch, must agree; (b) ancestry: #1215/#1220/#1221 ONE commit on BASE,
#1218 TWO commits (ebbdb3df6 on BASE, then 999623d28); (c) per-PR numstat == the pinned file set, blobs + modes; product-vs-test classification;
(d) pairwise disjointness; (e) merged trees + END_TREE in three orders + an `apply --cached` second instrument; (f) #1220: the BASE line
`anchorReadback.ts` raw block_number pass, the head's toBlockNumber + call site, the route that serves it; (g) #1221: `127.0.0.1:1` / `127.0.0.1:2` /
ANCHORING_SERVICE_URL counts per file at BASE vs head; (h) #1215: api-gateway index.ts untouched, the LEG D line-pins at BASE vs head;
(i) #1218: build_fixture call count, the /dev/null redirect at BASE, the `fx` CONTROL at head; (k) #1222: the ks727 canary cells' `forwarded` pins, the entity.too.large filter pin, error-handler.ts untouched; (l) #1223: verification.ts non-comment changed lines (must be 0) with a control on the test file; (j) the hyphenated-key scan on the six branch names.
Writes pins_gate21T2.txt (key=value) beside itself. rc 0 only if every HARD assertion holds."""
import os, subprocess, sys, datetime, re, tempfile, random
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) and os.path.isdir(SP), 'argv[1] must be a scratchpad dir'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'
D = 'Blockchain/Dev/'
OT = D + 'services/originate/src/__tests__/'
PRS = [
    dict(n='1215', key='KS-1288', head='5e3419a46db5a1a4e7e640aee2e60dd89db3912a', commits=1,
         br='refs/heads/feature/ks-1288-legd-text-pins-l3-r1-1',
         files={D + 'packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts': (178, 79)}),
    dict(n='1218', key='KS-897', head='999623d28f7cc3f11140cf379cfd3169e6530b57', commits=2, mid='ebbdb3df66673b5ec2ded18641e3fd73a2404825',
         br='refs/heads/feature/ks-897-build-fixture-swallows-its-own-failure-l4-fixtureabort-1',
         files={D + 'scripts/__tests__/pre_push_hook_base.test.sh': (28, 6)}),
    dict(n='1220', key='KS-1129', head='9c2021ba3e770abc9ad464b62fdc245a920389cb', commits=1,
         br='refs/heads/feature/ks-1129-anchoring-blocknumber-number-l2-bignum-1',
         files={D + 'services/anchoring/src/__tests__/ks1129-blocknumber-is-a-number.test.ts': (96, 0), D + 'services/anchoring/src/anchorReadback.ts': (32, 1)}),
    dict(n='1221', key='KS-1266', head='0a561a5db393e8f0ced82b86af572c7231330d64', commits=1,
         br='refs/heads/feature/ks-1266-anchoring-url-hermetic-l1-b-1',
         files={OT + 'ks1213-a-derived-writer-relabel-is-refused.test.ts': (10, 2), OT + 'ks1228-a-refused-request-writes-no-provenance-row.test.ts': (3, 1),
                OT + 'ks444-certifications-issue-body-types.test.ts': (7, 0), OT + 'ks444-documents-create-title-guard.test.ts': (7, 0),
                OT + 'ks445-certifications-issue-unstorable-payload.test.ts': (7, 0), OT + 'ks520-anchor-fail-closed.test.ts': (3, 1),
                OT + 'ks543-certify-boundary-strip.test.ts': (7, 0)}),
    dict(n='1222', key='KS-1181', head='9bce90229ad60b4ab988248648530b3b9a0d951d', commits=1,
         br='refs/heads/feature/ks-1181-errorhandler-canary-hit-l3-r1-1',
         files={D + 'packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts': (60, 4)}),
    dict(n='1223', key='KS-1118', head='759726d8d046e6098e720d4768c87e114d0c363c', commits=1,
         br='refs/heads/feature/ks-1118-verify-hash-precedence-l1-c-1',
         files={OT + 'ks1103-verify-hash-field.test.ts': (12, 0), D + 'services/originate/src/routes/verification.ts': (8, 3)}),
]
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(a, env=None, inp=None):
    p = subprocess.run(a, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
print('predict_gate21T2 start', now())
url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]
ssh = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
ENV = dict(os.environ); ENV['GIT_SSH_COMMAND'] = ssh
print('checkout remote.origin.url:', url, '| core.sshCommand present:', bool(ssh), '(value not printed)')
CL = tempfile.mkdtemp(prefix='g21T2clone_', dir=SP); os.rmdir(CL)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--filter=blob:none', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('clone FROM ORIGIN rc=%d %s -> %s' % (rc, e[:200], CL)); assert rc == 0
def g(*a, env=None, inp=None): return sh(['git', '-C', CL] + list(a), env=env or ENV, inp=inp)
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % p['n'] for p in PRS] + [p['br'] for p in PRS]
lsr = sh(['git', '-C', REPO, 'ls-remote', 'origin'] + refs)
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s:' % (lsr[0], now())); [print('   ', v, k) for k, v in LS.items()]
spec = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/g21/%s' % (p['n'], p['n']) for p in PRS] + ['+%s:refs/g21br/%s' % (p['br'], p['n']) for p in PRS]
rc, o, e = g('fetch', '--quiet', 'origin', *spec); print('fetch rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEV = g('rev-parse', 'refs/heads/develop')[1]
print('--- (a) heads and develop (ls-remote, then the fetch)')
hard(DEV == LS.get('refs/heads/develop'), 'develop %s == ls-remote' % DEV)
for p in PRS:
    h = g('rev-parse', 'refs/g21/' + p['n'])[1]; b = g('rev-parse', 'refs/g21br/' + p['n'])[1]
    hard(h == b == LS.get('refs/pull/%s/head' % p['n']) == LS.get(p['br']) == p['head'], '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (p['n'], h))
print('--- (b) ancestry and the develop reading')
for p in PRS:
    revs = g('rev-list', '--parents', BASE + '..' + p['head'])[1].splitlines()
    hard(len(revs) == p['commits'], '#%s: %d commit(s) over BASE (measured %d)' % (p['n'], p['commits'], len(revs)))
    if p['commits'] == 1: hard(revs[0].split()[1:] == [BASE], '#%s: parent == BASE' % p['n'])
    else:
        hard(revs[0].split() == [p['head'], p['mid']] and revs[1].split() == [p['mid'], BASE], '#%s: head %s -> %s -> BASE (linear, no merge commit)' % (p['n'], p['head'][:9], p['mid'][:9]))
ALL = sorted(set(f for p in PRS for f in p['files']))
if DEV == BASE:
    BEHIND = 0; print('  develop == BASE %s (0 commits ahead)' % BASE)
else:
    anc = g('merge-base', '--is-ancestor', BASE, DEV)[0] == 0; hard(anc, 'develop moved to a DESCENDANT of BASE')
    BEHIND = int(g('rev-list', '--count', BASE + '..' + DEV)[1]); mv = g('diff', '--name-only', BASE, DEV)[1].splitlines()
    print('  develop moved %d commits; %d paths changed' % (BEHIND, len(mv))); print('    ' + g('log', '--format=%H %s', BASE + '..' + DEV)[1].replace('\n', '\n    '))
    hard(not (set(ALL) & set(mv)), 'the develop move touches NONE of the batch paths (else re-predict BY HAND): %s' % sorted(set(ALL) & set(mv)))
with open(os.path.join(G, 'devlog_gate21T2.txt'), 'w') as f: f.write(g('log', '--format=%H %s', BASE + '..' + DEV)[1] + '\n')
DEVTREE = g('rev-parse', DEV + '^{tree}')[1]; BASETREE = g('rev-parse', BASE + '^{tree}')[1]
print('  develop tree', DEVTREE, '| BASE tree', BASETREE)
print('--- (c) per-PR numstat, blobs, modes, product-vs-test')
BL = {}; BB = {}
for p in PRS:
    ns = g('diff', '--numstat', BASE, p['head'])[1]; rows = {r.split('\t')[2]: (int(r.split('\t')[0]), int(r.split('\t')[1])) for r in ns.splitlines()}
    print('  #%s %s: %d files +%d/-%d' % (p['n'], p['key'], len(rows), sum(a for a, _ in rows.values()), sum(d for _, d in rows.values())))
    hard(rows == p['files'], '#%s numstat == the pinned file set and counts' % p['n'])
    for f in sorted(p['files']):
        ls = g('ls-tree', p['head'], '--', f)[1].split(); BL[f] = (ls[2], ls[0])
        lb = g('ls-tree', BASE, '--', f)[1].split(); BB[f] = lb[2] if lb else 'ABSENT'
        cls = 'TEST' if '/__tests__/' in f else 'PRODUCT'
        print('    %s %s %s %-7s (BASE %s) %s' % (ls[0], ls[2], p['n'], cls, BB[f][:12], f))
        want = '100755' if f.endswith('.test.sh') and BB[f] != 'ABSENT' and g('ls-tree', BASE, '--', f)[1].split()[0] == '100755' else (g('ls-tree', BASE, '--', f)[1].split()[0] if BB[f] != 'ABSENT' else '100644')
        hard(ls[0] == want, '%s mode %s at head == BASE mode (or 100644 if new)' % (f[len(D):], ls[0]))
prod = [f for f in ALL if '/__tests__/' not in f]
print('  PRODUCT paths in the batch: %s' % prod)
hard(prod == [D + 'services/anchoring/src/anchorReadback.ts', D + 'services/originate/src/routes/verification.ts'], 'the product paths are exactly #1220 anchorReadback.ts (behaviour) and #1223 verification.ts (comment-only, see (l)); the other four PRs are test-only')
print('--- (d) disjointness')
for i, a in enumerate(PRS):
    for b in PRS[i + 1:]:
        x = set(a['files']) & set(b['files']); hard(not x, '#%s ∩ #%s = EMPTY (%s)' % (a['n'], b['n'], sorted(x)))
print('  distinct paths:', len(ALL))
print('--- (e) merged trees over the develop just read + END_TREE in three orders + a second instrument')
MT = {}
for p in PRS:
    r = g('merge-tree', '--write-tree', DEV, p['head']); t = r[1].splitlines()[0] if r[1] else ''
    ht = g('rev-parse', p['head'] + '^{tree}')[1]; MT[p['n']] = t
    print('  #%s merge-tree rc %d -> %s | head tree %s | equal %s' % (p['n'], r[0], t, ht, t == ht)); hard(r[0] == 0, '#%s merges clean over develop' % p['n'])
    if DEV == BASE: hard(t == ht, '#%s merged tree == head tree (develop == BASE)' % p['n'])
def chain(order):
    E = dict(ENV); E['GIT_AUTHOR_NAME'] = E['GIT_COMMITTER_NAME'] = 'x'; E['GIT_AUTHOR_EMAIL'] = E['GIT_COMMITTER_EMAIL'] = 'x@x'
    cur = DEV
    for n in order:
        h = [p['head'] for p in PRS if p['n'] == n][0]
        r = g('merge-tree', '--write-tree', cur, h)
        if r[0] != 0: return 'CONFLICT@' + n
        t = r[1].splitlines()[0]; cur = g('commit-tree', t, '-p', cur, '-p', h, '-m', 'g21T2 chain (scratch only)', env=E)[1]
    return g('rev-parse', cur + '^{tree}')[1]
orders = [[p['n'] for p in PRS]]; orders.append(list(reversed(orders[0]))); sh_ = list(orders[0]); random.Random(21).shuffle(sh_); orders.append(sh_)
ENDS = [chain(o) for o in orders]
for o, t in zip(orders, ENDS): print('  END_TREE order %s -> %s' % (','.join(o), t))
hard(len(set(ENDS)) == 1 and not ENDS[0].startswith('CONFLICT'), 'END_TREE identical in three orders')
END = ENDS[0]
idx = os.path.join(CL, 'g21T2.index'); E2 = dict(ENV); E2['GIT_INDEX_FILE'] = idx
sh(['git', '-C', CL, 'read-tree', DEVTREE], env=E2)
for p in PRS:
    # RAW stdout (never .strip()): a trailing blank context line is ' ' and stripping it corrupts the patch (run 1: #1215 'corrupt patch at line 304')
    patch = subprocess.run(['git', '-C', CL, 'diff', '--binary', '--full-index', BASE, p['head']], capture_output=True, text=True, env=ENV).stdout
    ap = sh(['git', '-C', CL, 'apply', '--cached', '-'], env=E2, inp=patch); print('  apply --cached #%s rc %d %s' % (p['n'], ap[0], ap[2][:120]))
AT = sh(['git', '-C', CL, 'write-tree'], env=E2)[1]
hard(AT == END, 'second instrument (apply --cached of each BASE..head onto develop tree) == END_TREE: %s' % AT)
st = g('diff', '--shortstat', DEV, END)[1]; print('  develop -> END_TREE:', st)
for p in PRS:
    for f in p['files']: hard(g('rev-parse', END + ':' + f)[1] == BL[f][0], 'END_TREE %s == #%s head blob' % (f.split('/')[-1], p['n']))
def blob(rev, f):
    r = g('cat-file', 'blob', rev + ':' + f); return r[1] if r[0] == 0 else None
print('--- (f) #1220 anchorReadback.ts: the raw pass at BASE, the fix at head, the route')
AR = D + 'services/anchoring/src/anchorReadback.ts'
b0 = blob(BASE, AR).splitlines(); b1 = blob('9c2021ba3e770abc9ad464b62fdc245a920389cb', AR).splitlines()
bn0 = [(i + 1, l.strip()) for i, l in enumerate(b0) if 'block_number' in l]; bn1 = [(i + 1, l.strip()) for i, l in enumerate(b1) if 'block_number' in l or 'toBlockNumber' in l]
print('  BASE block_number lines:', bn0); print('  head block_number / toBlockNumber lines:', bn1)
hard(any(n == 103 for n, _ in bn0), 'BASE anchorReadback.ts:103 names block_number (the seat\'s site)')
IX = D + 'services/anchoring/src/index.ts'
ix0 = blob(BASE, IX).splitlines()
print('  BASE anchoring index.ts `row?.block_number` hits:', sum('row?.block_number' in l for l in ix0), '| `Number(row.block_number)` lines:', [i + 1 for i, l in enumerate(ix0) if 'Number(row.block_number)' in l])
print('  BASE anchoring index.ts verify routes:', [(i + 1, l.strip()[:110]) for i, l in enumerate(ix0) if '/api/anchors/verify' in l][:6])
print('  BASE anchoring index.ts anchorReadback imports:', [(i + 1, l.strip()[:120]) for i, l in enumerate(ix0) if 'anchorReadback' in l][:6])
print('  #1220 diff of anchorReadback.ts:'); print('    ' + g('diff', BASE, '9c2021ba3e770abc9ad464b62fdc245a920389cb', '--', AR)[1].replace('\n', '\n    '))
T1129 = D + 'services/anchoring/src/__tests__/ks1129-blocknumber-is-a-number.test.ts'
tt = blob('9c2021ba3e770abc9ad464b62fdc245a920389cb', T1129)
print('  ks1129 test: it( count %d, test( count %d, RED-labelled lines %d, CONTROL-labelled lines %d' % (len(re.findall(r'\bit\(', tt)), len(re.findall(r'\btest\(', tt)), len(re.findall(r'RED', tt)), len(re.findall(r'CONTROL', tt))))
print('  anchoring package.json test script:', [l.strip() for l in blob(BASE, D + 'services/anchoring/package.json').splitlines() if '"test' in l])
TM = [l for l in g('ls-tree', '-r', '--name-only', BASE, '--', D + 'services/anchoring/src/')[1].splitlines() if 'threadTokenMint' in l]
print('  threadTokenMint files at BASE:', TM)
if TM:
    tmb = blob(BASE, TM[0]); print('  its "deterministic per-seed policyId" titles:', [l.strip()[:140] for l in tmb.splitlines() if 'per-seed' in l])
print('--- (g) #1221: port / URL counts per file, BASE -> head')
for f in sorted(PRS[3]['files']):
    a = blob(BASE, f) or ''; b = blob(PRS[3]['head'], f) or ''
    c = lambda s, t: len(re.findall(re.escape(t) + r'(?!\d)', s))
    print('  %-62s 127.0.0.1:1 %d->%d | 127.0.0.1:2 %d->%d | ANCHORING_SERVICE_URL %d->%d | delete-env %d->%d' % (f.split('/')[-1], c(a, '127.0.0.1:1'), c(b, '127.0.0.1:1'), c(a, '127.0.0.1:2'), c(b, '127.0.0.1:2'),
          a.count('ANCHORING_SERVICE_URL'), b.count('ANCHORING_SERVICE_URL'), a.count('delete process.env.ANCHORING_SERVICE_URL'), b.count('delete process.env.ANCHORING_SERVICE_URL')))
gp = g('grep', '-n', '-E', r"127\.0\.0\.1:1([^0-9]|$)", PRS[3]['head'], '--', D + 'services/originate/')[1]
print('  `127.0.0.1:1` (not :1x) left under services/originate/ at #1221 head: %d' % ((gp.count('\n') + 1) if gp else 0))
for l in gp.splitlines(): print('    ' + l.split(':', 1)[1][len(D):][:220])
g0 = g('grep', '-n', '-E', r"127\.0\.0\.1:1([^0-9]|$)", BASE, '--', D + 'services/originate/')[1]
print('  the same grep at BASE under services/originate/: %d' % ((g0.count('\n') + 1) if g0 else 0))
for l in g0.splitlines(): print('    ' + l.split(':', 1)[1][len(D):][:220])
gp0 = g('grep', '-n', '-E', r"127\.0\.0\.1:1([^0-9]|$)", BASE, '--', D)[1]
print('  CONTROL, the same grep at BASE over Blockchain/Dev:', (gp0.count('\n') + 1) if gp0 else 0); print('    ' + gp0.replace('\n', '\n    ')[:1500])
dflt = g('grep', '-n', 'anchoring:4005', BASE, '--', D + 'services/originate/src/')[1]
print('  default `anchoring:4005` in originate src at BASE:', dflt[:600])
print('  originate package.json test scripts:', [l.strip() for l in blob(BASE, D + 'services/originate/package.json').splitlines() if '"test' in l])
print('--- (h) #1215: the LEG D pins BASE vs head; api-gateway index.ts untouched')
F15 = list(PRS[0]['files'])[0]
x0 = blob(BASE, F15); x1 = blob(PRS[0]['head'], F15)
print('  LEG D mentions BASE %d head %d | `anchor` BASE %d head %d | `siteAnchor` head %d | `(top level)` head %d' % (x0.count('LEG D'), x1.count('LEG D'), x0.count('anchor'), x1.count('anchor'), x1.count('siteAnchor'), x1.count('(top level)')))
print('  BASE numeric line pins in LEG D region:', sorted(set(re.findall(r'\b(8\d\d)\b', x0)))[:20])
print('  head numeric 8xx literals:', sorted(set(re.findall(r'\b(8\d\d)\b', x1)))[:20])
print('  it( count BASE %d head %d' % (len(re.findall(r'\bit\(', x0)), len(re.findall(r'\bit\(', x1))))
hard(g('diff', '--quiet', BASE, PRS[0]['head'], '--', D + 'services/api-gateway/')[0] == 0, '#1215: 0 bytes under services/api-gateway/ (the file the suite READS is untouched)')
print('  api-gateway/src/index.ts blob at BASE:', g('rev-parse', BASE + ':' + D + 'services/api-gateway/src/index.ts')[1])
print('--- (i) #1218: build_fixture calls, the /dev/null redirect, the fx CONTROL')
F18 = list(PRS[1]['files'])[0]
y0 = blob(BASE, F18); y1 = blob(PRS[1]['head'], F18)
print('  build_fixture CALL lines at col 0 (definition excluded): BASE %d head %d | definition lines %d' % (len(re.findall(r'(?m)^build_fixture (?!\()', y0)), len(re.findall(r'(?m)^build_fixture (?!\()', y1)), len(re.findall(r'(?m)^build_fixture\(\)', y1))))
print('  `/dev/null 2>&1` BASE %d head %d | FIXTURE BUILD FAILED head %d | build.log head %d | `fx` head %d | `exit 2` BASE %d head %d' % (y0.count('/dev/null 2>&1'), y1.count('/dev/null 2>&1'), y1.count('FIXTURE BUILD FAILED'), y1.count('build.log'), len(re.findall(r'\bfx\b', y1)), y0.count('exit 2'), y1.count('exit 2')))
print('  the trap line(s):', [(i + 1, l.strip()) for i, l in enumerate(y1.splitlines()) if l.startswith('trap ')])
print('  #1218 diff:'); print('    ' + g('diff', BASE, PRS[1]['head'], '--', F18)[1].replace('\n', '\n    '))
print('--- (k) #1222: the ks727 canary pins; error-handler.ts untouched')
F22 = D + 'packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts'
z0 = blob(BASE, F22); z1 = blob(PRS[4]['head'], F22)
for k in ('forwarded', 'shouldForward', 'entity.too.large', 'payloadTooLargeErrorHandler', 'driveThroughRoute', 'CONTROL', '0-hit'):
    print('  %-28s BASE %3d head %3d' % (k, z0.count(k), z1.count(k)))
print('  it( count BASE %d head %d' % (len(re.findall(r'\bit\(', z0)), len(re.findall(r'\bit\(', z1))))
print('  `const shouldForward` declarations at head: %d (the seat: ONE after its T-1 fix)' % len(re.findall(r'\bconst shouldForward\b', z1)))
EH = D + 'packages/shared/src/errors/error-handler.ts'
print('  error-handler.ts at BASE:', g('ls-tree', BASE, '--', EH)[1])
hard(g('diff', '--quiet', BASE, PRS[4]['head'], '--', D + 'packages/shared/src/errors/')[0] == 0, '#1222: 0 bytes under packages/shared/src/errors/ (the tampered file is restored; only the test moved)')
print('  #1222 diff:'); print('    ' + g('diff', BASE, PRS[4]['head'], '--', F22)[1].replace('\n', '\n    '))
print('--- (l) #1223: verification.ts comment-only; the control sees code lines in the test file')
def noncomment(rev_a, rev_b, f):
    out = []
    for l in g('diff', '-U0', rev_a, rev_b, '--', f)[1].splitlines():
        if l[:1] in '+-' and not l.startswith(('+++', '---')):
            s = l[1:].strip()
            if s and not s.startswith(('//', '*', '/*', '*/')): out.append(l)
    return out
H23 = PRS[5]['head']; VF = D + 'services/originate/src/routes/verification.ts'
nc = noncomment(BASE, H23, VF); ct = noncomment(BASE, H23, OT + 'ks1103-verify-hash-field.test.ts')
print('  verification.ts non-comment +/- lines: %d %s | CONTROL ks1103 test non-comment +/- lines: %d' % (len(nc), nc, len(ct)))
hard(len(nc) == 0 and len(ct) > 0, '#1223: 0 executable lines changed in verification.ts, and the same instrument SEES code lines in the test file')
print('  #1223 diff of verification.ts:'); print('    ' + g('diff', BASE, H23, '--', VF)[1].replace('\n', '\n    '))
print('  #1223 diff of the test:'); print('    ' + g('diff', BASE, H23, '--', OT + 'ks1103-verify-hash-field.test.ts')[1].replace('\n', '\n    '))
print('  the alias chain at BASE:', [(i + 1, l.strip()[:150]) for i, l in enumerate(blob(BASE, VF).splitlines()) if 'providedHash' in l and '||' in l][:4])
print('  history of the test file at BASE (the seat: #965 / #931 / #1170, no #1136):'); print('    ' + g('log', '--format=%h %s', BASE, '--', OT + 'ks1103-verify-hash-field.test.ts')[1].replace('\n', '\n    '))
print('--- (j) hyphenated-key scan on the branch names (own key only)')
for p in PRS:
    ks = sorted(set(m.upper() for m in re.findall(r'(?i)\bks-\d+', p['br'])))
    own = {p['key']}
    print('  #%s %s -> %s' % (p['n'], p['br'], ks)); hard(set(ks) <= own | ({'KS-896'} if p['n'] == '1218' else set()) and p['key'] in ks, '#%s branch carries its own key only' % p['n'])
print('--- summary')
PINS = dict(MEASURED_AT=now(), BASE=BASE, BASE_TREE=BASETREE, DEVELOP=DEV, DEVELOP_TREE=DEVTREE, BEHIND=str(BEHIND), END_TREE=END, END_SHORTSTAT=st)
for p in PRS: PINS['HEAD_' + p['n']] = p['head']; PINS['MERGED_' + p['n']] = MT[p['n']]
for f in ALL: PINS['BLOB|' + f] = '%s %s' % BL[f]
for f in ALL: PINS['BASEBLOB|' + f] = BB[f]
PINS['FAIL'] = str(len(FAIL))
with open(os.path.join(G, 'pins_gate21T2.txt'), 'w') as f:
    for k, v in PINS.items(): f.write('%s=%s\n' % (k, v))
print('pins written; FAIL', len(FAIL), FAIL); print('scratch clone (kept, never deleted):', CL)
sys.exit(1 if FAIL else 0)
