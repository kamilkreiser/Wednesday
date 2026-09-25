#!/usr/bin/env python3
"""predict_gate21T1b.py <scratchpad> — the drafter's MEASUREMENTS for the round-21 SECOND tier-1 batch gate over #1224 KS-1179, #1226 KS-872,
#1228 KS-1171, #1230 KS-1131 (widened by Wednesday 05:2xZ; FROZEN at four). Every git WRITE verb (clone, fetch, merge-tree --write-tree, commit-tree, read-tree/apply/write-tree in a temp index) lives in a
scratch FULL bare clone FROM ORIGIN under <scratchpad> (over the checkout's own ssh road, read with `config --get` and never printed; a blobless clone
was tried first and its lazy fetch failed on wide greps — see README); the Secuura checkout is read with `ls-remote` / `config --get` only.

BASE-INVARIANT by design (Wednesday's 04:35Z ANSWER to Seat B 25th, `answer_seatB25_movedbase`): the three heads were cut from the OLD develop
6ab9d5021 (BASE) and develop has since MOVED (the first tier-1 batch merged). A merged-tree sha is base-dependent, so every merge assertion here is
stated so it holds over ANY develop that descends from BASE without touching the PR's paths:
  (1) the diff between the develop just read and each PR's merged result == EXACTLY that PR's own paths, each blob byte-equal to the head's blob;
  (2) that diff's numstat == the PR's own BASE..head numstat (nothing else changes; the delta is the same delta over the new base);
  (3) the develop move (BASE..develop) intersected with EACH PR's own paths == EMPTY (the test is per PR, not against a batch-wide set).
Measures: (a) develop + the three pull heads + branches at origin, two reads (ls-remote, then the fetch) that must agree; (b) ancestry: each head is
ONE commit whose parent == BASE; develop descends from BASE; the move's commits and paths; (c) per-PR numstat == the pinned file set, blobs + modes;
(d) pairwise path disjointness; 0 bytes under services/auth/ with a control that sees bytes under packages/shared/; (e) per-PR merged tree over the
develop just read with the base-invariant checks (1)-(3), then the END_TREE of the three in THREE orders + an `apply --cached` second instrument, and
the END_TREE's diff vs develop == the union of the 8 paths at the head blobs; (f) #1224: `resolvePublicAddresses` byte-identical BASE -> head (control:
the instrument sees `safeOutboundRequest` change), the `finally` present, callers of safeOutboundRequest enumerated; (g) #1226: the ONLY non-comment
changed lines are the `interface JwkLike` block and the one cast; no package.json / lockfile / tsconfig anywhere in the PR; (h) #1228: the two
constants are the ruled values, the gate needs BOTH conditions, the production poll call is unchanged BASE -> head -> develop, the production
schedule's first attempt that can clear 60 s, the integration-config census, the importers of anchorSubmission / confirmation, the new file's cell
count; (i) the hyphenated-key scan on the three branch names. Writes pins_gate21T1b.txt (key=value) + devlog_gate21T1b.txt beside itself.
rc 0 only if every HARD assertion holds."""
import os, subprocess, sys, datetime, re, tempfile, random
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(SP)) and os.path.isdir(SP), 'argv[1] must be a scratchpad dir'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE = '6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7'   # the OLD develop every head was cut from (measured: parent of each head)
D = 'Blockchain/Dev/'
SH = D + 'packages/shared/src/'
AN = D + 'services/anchoring/src/'
PRS = [  # seat order: Seat L3 (wrap 04:20:54Z) #1224, #1226; Seat L2 READY FOR QA 4 (04:41:36Z) #1228
    dict(n='1224', key='KS-1179', head='d4862b3eee3566635c61cf9d0b810131140e4fa2',
         br='refs/heads/feature/ks-1179-ssrf-dns-timer-docs-l3-r1-1',
         files={SH + '__tests__/ks1179-dns-timer-cleared.test.ts': (121, 0), SH + 'security/ssrf-guard.ts': (45, 14)}),
    dict(n='1226', key='KS-872', head='fcda1a6ef7e4fde33215466a29b730025fcd6233',
         br='refs/heads/feature/ks-872-jwks-jsonwebkey-l3-r1-1',
         files={SH + 'crypto/jwks.ts': (41, 1)}),
    dict(n='1228', key='KS-1171', head='43279280f76ed9982782ad7652288d2c3d522b71',
         br='refs/heads/feature/ks-1171-lastansweredattempt-gates-absent-l2-lastans-1',
         files={AN + '__tests__/ks1171b-absent-needs-both-conditions.test.ts': (156, 0), AN + '__tests__/ks726-gate-f1-unreachable-chain.test.ts': (48, 11),
                AN + '__tests__/ks726-write-ahead-tx-hash.test.ts': (31, 3), AN + 'anchorSubmission.ts': (79, 7), AN + 'cardano/confirmation.ts': (26, 0)}),
    dict(n='1230', key='KS-1131', head='1116dab0466da48ce96c4811f8086b061a49aa70', ncommits=2,   # Seat B 25th PUSHED + READY 3/4/5 (05:15:44Z), its #1230 section
         br='refs/heads/feature/ks-1131-ks963-structural-cells-count-raw-text-a-comment-naming-r21-callshaped-fa-fb-1',
         files={D + 'services/auth/src/__tests__/ks963-preauth-rethrow.test.ts': (55, 1)}),
]
H = {p['n']: p['head'] for p in PRS}
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(a, env=None, inp=None):
    p = subprocess.run(a, capture_output=True, text=True, env=env, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
FAIL = []
def hard(ok, msg):
    print(('  OK   ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
print('predict_gate21T1b start', now())
url = sh(['git', '-C', REPO, 'config', '--get', 'remote.origin.url'])[1]
ssh = sh(['git', '-C', REPO, 'config', '--get', 'core.sshCommand'])[1]
ENV = dict(os.environ); ENV['GIT_SSH_COMMAND'] = ssh
print('checkout remote.origin.url:', url, '| core.sshCommand present:', bool(ssh), '(value not printed)')
CL = tempfile.mkdtemp(prefix='g21bclone_', dir=SP); os.rmdir(CL)
rc, o, e = sh(['git', 'clone', '--quiet', '--bare', '--single-branch', '--branch', 'develop', '--no-tags', url, CL], env=ENV)
print('FULL clone FROM ORIGIN rc=%d %s -> %s' % (rc, e[:200], CL)); assert rc == 0
def g(*a, env=None, inp=None): return sh(['git', '--git-dir', CL] + list(a), env=env or ENV, inp=inp)
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % p['n'] for p in PRS] + [p['br'] for p in PRS]
lsr = sh(['git', '-C', REPO, 'ls-remote', 'origin'] + refs)
LS = dict(l.split('\t')[::-1] for l in lsr[1].splitlines()); print('ls-remote rc %d at %s:' % (lsr[0], now())); [print('   ', v, k) for k, v in LS.items()]
spec = ['+refs/heads/develop:refs/heads/develop'] + ['+refs/pull/%s/head:refs/g21b/%s' % (p['n'], p['n']) for p in PRS] + ['+%s:refs/g21bbr/%s' % (p['br'], p['n']) for p in PRS]
rc, o, e = g('fetch', '--quiet', 'origin', *spec); print('fetch rc=%d %s at %s' % (rc, e[:200], now())); assert rc == 0
DEV = g('rev-parse', 'refs/heads/develop')[1]
print('--- (a) heads and develop (ls-remote, then the fetch)')
hard(DEV == LS.get('refs/heads/develop'), 'develop %s == ls-remote' % DEV)
for p in PRS:
    h = g('rev-parse', 'refs/g21b/' + p['n'])[1]; b = g('rev-parse', 'refs/g21bbr/' + p['n'])[1]
    hard(h == b == LS.get('refs/pull/%s/head' % p['n']) == LS.get(p['br']) == p['head'], '#%s head %s == pull head == branch (ls-remote AND fetch) == the pin' % (p['n'], h))
print('--- (b) ancestry and the develop move')
for p in PRS:
    nc = p.get('ncommits', 1); chain_ = g('rev-list', '--parents', BASE + '..' + p['head'])[1].splitlines()
    first_parents = [l.split()[1:] for l in chain_]
    hard(len(chain_) == nc and all(len(x) == 1 for x in first_parents) and first_parents[-1] == [BASE],
         '#%s: %d commit(s), linear, the first one\'s parent == BASE %s (%s)' % (p['n'], nc, BASE[:12], ' <- '.join(l.split()[0][:9] for l in chain_)))
ALL = sorted(set(f for p in PRS for f in p['files']))
MOVE = []
if DEV == BASE:
    BEHIND = 0; print('  develop == BASE %s (0 commits ahead)' % BASE)
else:
    anc = g('merge-base', '--is-ancestor', BASE, DEV)[0] == 0; hard(anc, 'develop %s is a DESCENDANT of BASE' % DEV[:12])
    BEHIND = int(g('rev-list', '--count', BASE + '..' + DEV)[1]); MOVE = g('diff', '--name-only', BASE, DEV)[1].splitlines()
    print('  develop moved %d commits; %d paths changed:' % (BEHIND, len(MOVE))); print('    ' + g('log', '--format=%H %s', BASE + '..' + DEV)[1].replace('\n', '\n    '))
    for f in MOVE: print('      moved path', f)
    for p in PRS:
        x = sorted(set(p['files']) & set(MOVE)); hard(not x, '(3) BASE-INVARIANT: the develop move ∩ #%s\'s OWN paths == EMPTY (%s)' % (p['n'], x))
with open(os.path.join(G, 'devlog_gate21T1b.txt'), 'w') as f: f.write(g('log', '--format=%H %s', BASE + '..' + DEV)[1] + '\n')
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
        print('    %s %s %s (BASE %s) %s' % (ls[0], ls[2], p['n'], BB[f][:12], f))
        hard(ls[0] == '100644', f + ' mode 100644 at head')
print('--- (d) disjointness, services/auth/, dependency files')
for i, a in enumerate(PRS):
    for b in PRS[i + 1:]:
        x = set(a['files']) & set(b['files']); hard(not x, '#%s ∩ #%s = EMPTY (%s)' % (a['n'], b['n'], sorted(x)))
for p in PRS:
    au = g('diff', '--numstat', BASE, p['head'], '--', D + 'services/auth/')[1]
    if p['n'] == '1230': hard(au != '', 'CONTROL: the services/auth/ instrument SEES #1230\'s auth test file')
    else: hard(au == '', '#%s: 0 bytes under services/auth/' % p['n'])
    dep = [f for f in p['files'] if re.search(r'(^|/)(package(-lock)?\.json|tsconfig[^/]*\.json|npm-shrinkwrap\.json)$', f)]
    hard(not dep, '#%s: NO package.json / lockfile / tsconfig in the PR (%s)' % (p['n'], dep))
hard(any(g('diff', '--numstat', BASE, p['head'], '--', D + 'packages/shared/')[1] for p in PRS), 'CONTROL: the same instrument SEES rows under packages/shared/ (#1224/#1226)')
hard(bool([f for f in MOVE if f.endswith('package-lock.json')]) or DEV == BASE, 'CONTROL: the dependency-file regex instrument has something to see — the develop move carries lockfiles (it is applied to the MOVE only as a control)')
print('--- (e) BASE-INVARIANT merged trees over the develop just read + END_TREE in three orders + a second instrument')
MT = {}
for p in PRS:
    r = g('merge-tree', '--write-tree', DEV, p['head']); t = r[1].splitlines()[0] if r[1] else ''; MT[p['n']] = t
    print('  #%s merge-tree rc %d -> %s' % (p['n'], r[0], t)); hard(r[0] == 0, '#%s merges clean over develop' % p['n'])
    dn = sorted(g('diff', '--name-only', DEV, t)[1].splitlines())
    hard(dn == sorted(p['files']), '(1) BASE-INVARIANT: diff(develop, #%s merged) == EXACTLY its own %d paths (got %d)' % (p['n'], len(p['files']), len(dn)))
    for f in p['files']: hard(g('rev-parse', t + ':' + f)[1] == BL[f][0], '(1) #%s merged blob == head blob: %s' % (p['n'], f[len(D):]))
    dns = {r_.split('\t')[2]: (int(r_.split('\t')[0]), int(r_.split('\t')[1])) for r_ in g('diff', '--numstat', DEV, t)[1].splitlines()}
    hard(dns == NS[p['n']], '(2) BASE-INVARIANT: numstat(develop -> merged) == numstat(BASE -> head) for #%s' % p['n'])
def chain(order):
    E = dict(ENV); E['GIT_AUTHOR_NAME'] = E['GIT_COMMITTER_NAME'] = 'x'; E['GIT_AUTHOR_EMAIL'] = E['GIT_COMMITTER_EMAIL'] = 'x@x'
    cur = DEV
    for n in order:
        r = g('merge-tree', '--write-tree', cur, H[n])
        if r[0] != 0: return 'CONFLICT@' + n
        t = r[1].splitlines()[0]; cur = g('commit-tree', t, '-p', cur, '-p', H[n], '-m', 'g21b chain (scratch only)', env=E)[1]
    return g('rev-parse', cur + '^{tree}')[1]
orders = [[p['n'] for p in PRS]]; orders.append(list(reversed(orders[0]))); sh_ = list(orders[0]); random.Random(21).shuffle(sh_)
if sh_ in orders: sh_ = [orders[0][1], orders[0][0], orders[0][2]]
orders.append(sh_)
ENDS = [chain(o) for o in orders]
for o, t in zip(orders, ENDS): print('  END_TREE order %s -> %s' % (','.join(o), t))
hard(len(set(ENDS)) == 1 and not ENDS[0].startswith('CONFLICT') and len(set(map(tuple, orders))) == 3, 'END_TREE identical in three DISTINCT orders')
END = ENDS[0]
idx = os.path.join(CL, 'g21b.index'); E2 = dict(ENV); E2['GIT_INDEX_FILE'] = idx
sh(['git', '--git-dir', CL, 'read-tree', DEVTREE], env=E2)
for p in PRS:
    patch = g('diff', '--binary', '--full-index', BASE, p['head'])[1] + '\n'
    ap = sh(['git', '--git-dir', CL, 'apply', '--cached', '-'], env=E2, inp=patch); print('  apply --cached #%s rc %d %s' % (p['n'], ap[0], ap[2][:120]))
    hard(ap[0] == 0, 'second instrument: apply --cached of #%s BASE..head onto develop\'s tree rc 0' % p['n'])
AT = sh(['git', '--git-dir', CL, 'write-tree'], env=E2)[1]
hard(AT == END, 'second instrument (apply --cached) == END_TREE: %s' % AT)
st = g('diff', '--shortstat', DEV, END)[1]; print('  develop -> END_TREE:', st)
hard(sorted(g('diff', '--name-only', DEV, END)[1].splitlines()) == ALL, 'END_TREE diff vs develop == the union of the %d batch paths' % len(ALL))
for f in ALL: hard(g('rev-parse', END + ':' + f)[1] == BL[f][0], 'END_TREE %s == head blob' % f[len(D):])
print('--- (f) #1224: ssrf-guard')
def fn_text(rev, path, name):
    t = g('cat-file', 'blob', rev + ':' + path)[1] + '\n'   # predict_1 FAILED 3 on this: sh() strips stdout, so a function closing the file lost its '\n}\n'
    m = re.search(r'(export\s+)?(async\s+)?function\s+' + name + r'\b[\s\S]*?\n}\n', t); return m.group(0) if m else None
SG = SH + 'security/ssrf-guard.ts'
rb, rh = fn_text(BASE, SG, 'resolvePublicAddresses'), fn_text(H['1224'], SG, 'resolvePublicAddresses')
hard(rb is not None and rb == rh, '#1224: resolvePublicAddresses function text byte-identical BASE -> head (found at both: %s/%s)' % (rb is not None, rh is not None))
sb, shd = fn_text(BASE, SG, 'safeOutboundRequest'), fn_text(H['1224'], SG, 'safeOutboundRequest')
hard(sb is not None and shd is not None and sb != shd, 'CONTROL: the same instrument sees safeOutboundRequest CHANGE')
hard('} finally {\n    if (dnsTimer) clearTimeout(dnsTimer);' in (shd or ''), '#1224: the clearTimeout sits in a `finally` at the head')
hard('if (dnsTimer) clearTimeout(dnsTimer);' in (sb or '') and 'finally' not in (sb or ''), 'CONTROL: at BASE the clearTimeout sits outside any finally (the defect the ticket names)')
code = lambda t: [l for l in t.splitlines() if l.strip() and not l.strip().startswith(('//', '*', '/*'))]
print('  #1224 code (non-comment) lines in safeOutboundRequest: BASE %d -> head %d' % (len(code(sb or '')), len(code(shd or ''))))
rets = lambda t: len(re.findall(r'\breturn\b', t or ''))
print('  #1224 `return` statements in safeOutboundRequest: BASE %d -> head %d (an ADDED return would be a new early exit)' % (rets(sb), rets(shd)))
hard(rets(sb) == rets(shd), '#1224: no return statement added to safeOutboundRequest (the early-return class, lesson 2026-09-20)')
for lab, spec_ in (('product callers', [D, ':!*__tests__*', ':!*.md']), ('test files', ['Blockchain/Dev/**/__tests__/**'])):
    r = g('grep', '-n' if lab == 'product callers' else '-l', 'safeOutboundRequest' + ('(' if lab == 'product callers' else ''), H['1224'], '--', *spec_)[1]
    print('  %s of safeOutboundRequest at #1224:' % lab); [print('    ' + l.split(':', 1)[1][:160]) for l in r.splitlines()]
print('--- (g) #1226: type-only')
JW = SH + 'crypto/jwks.ts'
d26 = g('diff', '-U0', BASE, H['1226'], '--', JW)[1]
add = [l[1:] for l in d26.splitlines() if l.startswith('+') and not l.startswith('+++')]; rem = [l[1:] for l in d26.splitlines() if l.startswith('-') and not l.startswith('---')]
addc, remc = code('\n'.join(add)), code('\n'.join(rem))
print('  added lines %d (non-comment %d) | removed %d (non-comment %d)' % (len(add), len(addc), len(rem), len(remc)))
for l in addc: print('    + ' + l.strip())
for l in remc: print('    - ' + l.strip())
want_add = ['interface JwkLike {', 'kty?: string;', 'use?: string;', 'key_ops?: string[];', 'alg?: string;', 'kid?: string;', '[parameter: string]: unknown;', '}',
            ".createPublicKey({ key: jwk as JwkLike, format: 'jwk' })"]
hard([l.strip() for l in addc] == want_add, '#1226: the ONLY non-comment added lines are the JwkLike interface block + the one cast (type-level constructs only)')
hard([l.strip() for l in remc] == [".createPublicKey({ key: jwk as crypto.JsonWebKey, format: 'jwk' })"], '#1226: the ONLY non-comment removed line is the old cast')
hard('export' not in ' '.join(addc), '#1226: JwkLike is NOT exported (so the emitted .d.ts surface should not change — the gate MEASURES that)')
print('--- (h) #1228: the ruling in code')
AS = AN + 'anchorSubmission.ts'; CF = AN + 'cardano/confirmation.ts'; IX = AN + 'index.ts'
ash = g('cat-file', 'blob', H['1228'] + ':' + AS)[1]
hard('export const ABSENT_MIN_ANSWERED_POLLS = 2;' in ash, '#1228: ABSENT_MIN_ANSWERED_POLLS = 2 (condition 1, the ruled value)')
hard('export const ABSENT_MIN_LAST_ANSWER_MS = 60_000;' in ash, '#1228: ABSENT_MIN_LAST_ANSWER_MS = 60_000 (condition 2, the ruled value)')
hard('const answeredTwice = answered >= ABSENT_MIN_ANSWERED_POLLS;' in ash and "typeof lastAnsweredElapsedMs === 'number' && lastAnsweredElapsedMs >= ABSENT_MIN_LAST_ANSWER_MS" in ash
     and 'if (!answeredTwice || !answeredLateEnough) {' in ash, '#1228: the rest-arm fires unless BOTH hold (`!answeredTwice || !answeredLateEnough` -> unknown) — the text; the gate proves the BEHAVIOUR')
hard('const answered = confirmation.polled ?? 0;' in ash, '#1228: a counter-less result reads answered 0 (no `polled === undefined` carve-out)')
asb = g('cat-file', 'blob', BASE + ':' + AS)[1]
hard('if (confirmation.polled === 0) {' in asb and 'if (confirmation.polled === 0) {' not in ash, 'CONTROL: BASE carries the old `polled === 0` gate; the head does not')
pc = [(lab, re.findall(r'confirm: \(txHash, onStatusUpdate\) => waitForConfirmation\([^)]*\)', g('cat-file', 'blob', rev + ':' + IX)[1])) for lab, rev in (('BASE', BASE), ('#1228', H['1228']), ('develop', DEV))]
for lab, m in pc: print('  production confirm wiring at %s: %s' % (lab, m))
hard(all(m == ["confirm: (txHash, onStatusUpdate) => waitForConfirmation(txHash, 30, 10_000, 60_000, onStatusUpdate)"] for _, m in pc), '#1228: production poll wiring (30 attempts, 10 s initial, 60 s cap) identical at BASE, head and develop')
cfh = g('cat-file', 'blob', H['1228'] + ':' + CF)[1]
hard('await sleep(delay + require(\'crypto\').randomInt(0, 2000));' in cfh and 'delay = Math.min(delay * 1.5, maxDelayMs);' in cfh, '#1228: the backoff the schedule below models is the head\'s (delay + 0..2 s jitter, x1.5, capped)')
t, d_, sched = 0.0, 10.0, []
for a in range(1, 31):
    sched.append((a, t, t + 2 * (a - 1))); t += d_; d_ = min(d_ * 1.5, 60.0)
first = next(a for a, lo, hi in sched if lo >= 60); maybe = [a for a, lo, hi in sched if hi >= 60 and lo < 60]
print('  production schedule, attempt: [earliest, latest] start s (sleep jitter 0..2 s each): ' + ' '.join('%d:[%.1f,%.1f]' % (a, lo, hi) for a, lo, hi in sched[:7]) + ' ...')
print('  first attempt ALWAYS >= 60 s after poll start: %d; attempts that MAY be (jitter): %s; total window lower bound %.0f s' % (first, maybe, sched[-1][1]))
hard(first <= 30, '#1228: condition 2 is REACHABLE in production (an answer at attempt %d starts >= 60 s after polling began) — the ABSENT arm is not dead code' % first)
ints = [f for f in g('ls-tree', '-r', '--name-only', H['1228'])[1].splitlines() if f.startswith(D + 'services/anchoring/') and re.search(r'jest\.integration|\.integration\.test\.ts$', f)]
allint = [f for f in g('ls-tree', '-r', '--name-only', H['1228'])[1].splitlines() if f.endswith('jest.integration.config.js')]
print('  integration configs anywhere at #1228: %s | integration files under services/anchoring: %s' % (allint, ints))
hard(bool(allint), 'CONTROL: the integration-config instrument FINDS one (%s)' % allint)
print('  => INTEGRATION CENSUS: %d integration configs/cells under services/anchoring (the KS-1171 service runs vitest: services/anchoring/vitest.config.ts)' % len(ints))
imp = g('grep', '-l', '-E', r"anchorSubmission|/confirmation['\"]", H['1228'], '--', D)[1]
print('  importers/readers of anchorSubmission or confirmation at #1228:'); [print('    ' + l.split(':', 1)[1]) for l in imp.splitlines()]
nb = g('cat-file', 'blob', H['1228'] + ':' + AN + '__tests__/ks1171b-absent-needs-both-conditions.test.ts')[1]
print('  ks1171b cells (it/test calls): %d' % len(re.findall(r'^\s*(it|test)(\.each\([^)]*\))?\(', nb, re.M)))
print('--- (j) #1230: the ks963 helper (a TEST file that is its own product)')
KT = D + 'services/auth/src/__tests__/ks963-preauth-rethrow.test.ts'
kb, kh = g('cat-file', 'blob', BASE + ':' + KT)[1], g('cat-file', 'blob', H['1230'] + ':' + KT)[1]
hard("expect(count(src.slice(expiryGuard, lookup), consumeFn)).toBe(1);" in kb and "expect(count(src.slice(expiryGuard, lookup), consumeFn + '(')).toBe(1);" in kh
     and "expect(count(src.slice(expiryGuard, lookup), consumeFn)).toBe(1);" not in kh, '#1230 F-A: property 2 counts consumeFn at BASE -> consumeFn + \'(\' at the head (the RELAXATION: a non-call-shaped hoisted consume is no longer counted)')
hard("expect(guardBody).toContain(consumeFn + '(');" in kh and "expect(guardBody).toContain(consumeFn + '(');" not in kb and "expect(guardBody).toContain(consumeFn);" in kh,
     '#1230 F-B: property 1 now also needs the call-shaped name; the raw-name line (:206) is KEPT')
hard("expect(count(expiryBody, consumeFn)).toBe(1);" in kb and "expect(count(expiryBody, consumeFn)).toBe(1);" in kh, '#1230: the expiry-body count (:218) is UNTOUCHED, as the body says')
stages = g('rev-list', '--reverse', BASE + '..' + H['1230'])[1].split()
for c in stages: print('  #1230 stage %s blob %s' % (c[:9], g('rev-parse', c + ':' + KT)[1][:12]))
print('  #1230 blob at BASE %s | the READY names F-A alone 560bb49c242f, stacked 041396c7fce5, tip(BASE) 9427c652ac2d' % g('rev-parse', BASE + ':' + KT)[1][:12])
hard([g('rev-parse', c + ':' + KT)[1][:12] for c in stages] == ['560bb49c242f', '041396c7fce5'] and g('rev-parse', BASE + ':' + KT)[1][:12] == '9427c652ac2d',
     '#1230: the per-stage blobs == the READY\'s (F-A 560bb49c242f, stacked 041396c7fce5, BASE 9427c652ac2d)')
prod = g('diff', '--name-only', BASE, H['1230'], '--', D + 'services/auth/src/routes/')[1]
hard(prod == '', '#1230: 0 bytes under services/auth/src/routes/ (auth.ts / wallet.ts read by the suite, unedited)')
mv_auth = [f for f in MOVE if f.startswith(D + 'services/auth/')]
hard(not mv_auth, 'the develop move touches 0 paths under services/auth/ (the files the ks963 suite reads are develop\'s == BASE\'s)')
print('--- (i) branch names through the hyphenated-key scanner (own key only)')
for p in PRS:
    ks = sorted(set(re.findall(r'(?i)\bks-(\d+)\b', p['br']))); hard(ks == [p['key'].split('-')[1]], '#%s branch keys %s == own %s' % (p['n'], ks, p['key']))
with open(os.path.join(G, 'pins_gate21T1b.txt'), 'w') as f:
    for k, v in [('MEASURED_AT', now()), ('BASE', BASE), ('BASE_TREE', BASETREE), ('DEVELOP', DEV), ('DEVELOP_TREE', DEVTREE), ('BEHIND', BEHIND), ('END_TREE', END),
                 ('END_SHORTSTAT', st), ('MOVE_PATHS', len(MOVE))] + [('HEAD_' + p['n'], p['head']) for p in PRS] + [('MERGED_' + n, t) for n, t in MT.items()] + \
                [('BLOB|' + f, '%s %s' % BL[f]) for f in ALL] + [('BASEBLOB|' + f, BB[f]) for f in ALL] + [('FIRST60', first), ('FAIL', len(FAIL))]:
        f.write('%s=%s\n' % (k, v))
print('scratch clone', CL); print('HARD FAILS:', len(FAIL), FAIL); print('done', now())
sys.exit(1 if FAIL else 0)
