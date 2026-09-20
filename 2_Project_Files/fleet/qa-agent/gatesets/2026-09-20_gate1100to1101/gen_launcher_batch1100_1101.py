#!/usr/bin/env python3
"""gen_launcher_batch1100_1101.py — derive launchers/launch_qa_secuura_batch1100_1101.sh from launchers/launch_qa_secuura_batch1097_1099.sh (the
batch gate prepared 2026-09-20 04:4x AEST, one gate / three verdicts, which ran cleanly) by ASSERTED block substitutions: every anchor must occur
exactly as often as stated, or the generator refuses and writes nothing. Structure copied from gatesets/2026-09-20_gate1097to1099/
gen_launcher_batch1097_1099.py; the data changed, the by-name guard (exit 33) carries this batch's items, the namespace guard (exit 32) reads the
READY's table rows, and the develop fixture still stands in for platform.ts (the tier-1 guard's file).

ONE BATCHED gate, TIER 1 floor (set by #1101 KS-1282 N99-1, an AUTH guard, test-only), TWO PRs #1100 + #1101 (Seat B 9th, READY 2026-09-20T06:37:50Z).
BOTH ARE TEST-ONLY: every changed path sits under api-gateway src/__tests__/ (asserted from local objects here AND from the PR files API read in
gh_pr_reads.out beside this file). NAMESPACE TRAP: KS-1100 and KS-1101 exist (KS-1100 Backlog, no attachment; KS-1101 In Progress, #1063 + #1037);
PR #1100 is KS-1230 and PR #1101 is KS-1282. The launcher refuses (exit 32) unless the prompt AND the READY both state which ticket each PR is.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, both refs/pull/N/head AND both branches — all must equal the pins;
  * local objects (rev-parse / cat-file / diff / rev-list / log): each PR is ONE commit whose parent IS develop; every file set, head tree, judged
    develop blob and landed head blob as pinned; pairwise file-disjoint (2 files, 0 new); zero product bytes and 0 deleted lines; each commit carries
    exactly its own Refs (#1100 KS-1230; #1101 KS-1282); no commit names KS-<its own PR number>; no commit carries ks1215 / ks-1215;
  * CANONICAL-PATCH identity for both (plain files in a scratch dir, `git apply` strict, `git hash-object` without -w): #1100 = N97-1, #1101 = N99-1;
    each patch reversed onto develop refuses; a crossed patch refuses;
  * the FOUR TAMPER PLANTS re-planted by TEXT from the develop blob, each `from` whole-line x1 AND raw-substring x1, each landed line and plant
    sha256 as the READY states, each planted ALONE (pre-plant bytes = develop's every time);
  * the BOTH-PRS TREE re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, controlled by re-deriving each head tree the
    same way; it must equal the READY's 1ccb80e0d. The drafter's scratch-clone prediction (predict_both_scratch.out: merge-tree chains in BOTH
    orders + an index composition + a read-tree-back control), measure_scratch.out, shape_scratch.out, gh_pr_reads.out and linear_reads.out are
    asserted here.
Usage: gen_launcher_batch1100_1101.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, json, os, re, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1100_1101', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = 'e470198783bcb1ef0eac94780f87579974051423'   # develop at READY time and re-read at 06:41Z; every PR's merge-base
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
# n, ticket (no spaces: the launcher's PRS_FLAT splits on whitespace), branch, head, ahead, file count, head tree
PRS = [
 (1100, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n97-1', '99ce89e741e6c3cad7457af7c91fb6fea86acdff', 1, 1, '68dc2d63123d48cc2f3473d05aa16013eba1d7c3'),
 (1101, 'KS-1282', 'feature/ks-1282-get-apiplatformtenants-the-requiresuperadmin-guard-n99-1', 'dc40087e756c598ca8b2957da7fbf1ec01945df8', 1, 1, '6d62805ccc009b7dca16041653bea89c46a33700'),
]
LABEL = {1100: 'KS-1230', 1101: 'KS-1282'}     # the prompt's words
KEYS = {n: LABEL[n].split(' + ') for n in LABEL}
WANTREFS = {1100: ['KS-1230'], 1101: ['KS-1282']}
TIER1 = {1101}
OVERRIDE = 1101                                # the head the launcher's test override stands in for (pushed LAST)
COMBINED = '1ccb80e0d66ab0ff12d5dbb61753b8c0c274e923'   # the READY's both-PRs tree; re-derived below
N97_1 = ('2026-09-20_ks1230-ornith35b-night2', 'patch.diff')
N99_1 = ('2026-09-20_ks1282-ornith35b-night4', 'patch.diff')
NAME = {N97_1: 'N97-1', N99_1: 'N99-1'}
CANON = {1100: N97_1, 1101: N99_1}
ADMINTS = A + 'src/routes/admin.ts'; PLATTS = A + 'src/routes/platform.ts'
# the READY's four plants: id, file, line, run, plant sha256 prefix, post-plant byte count
TAMPERS = [('LASTOF2NULLMIXED', ADMINTS, 1132, N97_1, '47724925d360', 74229),
           ('LASTOF4NULL', ADMINTS, 1132, N97_1, '3e08ce6b879e', 74179),
           ('SUPERROLESWIDEN', PLATTS, 64, N99_1, '0acfe0d608fd', 44906),
           ('SUPERADMITSANYUSER', PLATTS, 68, N99_1, 'b83e48fdbe83', 44881)]
PREBYTES = {ADMINTS: 74087, PLATTS: 44888}
def sec(run, name): return RUNS + run + '/out.md.checker/' + name

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': '026197fbaeff433b2b92d9fad9d9527a2e7ac212',
 A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': 'fe235c8aa1d85d28d73a4853890c840bd59e0a7a',
 A + 'src/__tests__/db.retry.test.ts': '5933da41ed3dcf37f415000c4da4a717ea8d7eba',
 PLATTS: 'b80a8cd8d4e1af5a944817227f5ee6612c793954',
 ADMINTS: '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 A + 'src/routes/proxy.ts': '795ae7ca3bdc76be3e563e87fc34a8cc221e5632',
 A + 'src/routes/verification.ts': 'f888e8cd0bd10c98a508542d75902ab122595157',
 A + 'src/middleware/auth.ts': 'bf09d315a64443b7f02bc27a74366b7a7f1dae81',
 A + 'src/index.ts': 'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'vitest.setup.ts': '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 D + 'scripts/preflight/preflight.sh': '712f895362e2c8d1ead6fd09ac257d7bce212948',
 D + 'scripts/run-shell-suites.sh': 'bf766bb54828cf6abad817f0f21a0c2f674d783f',
 '.githooks/pre-push': '1b22d4e146487aa25698310b353152a7d09986b5',
 D + 'package.json': '773443a9faa0a2eb7caf01c313b880fbe3251922',
 D + 'package-lock.json': '646c19f6f7f735ba32bfb20bef8b936835184949',
 D + 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
 'BACKLOG.md': '59a1928dc56d9921dbdf2e8d36667e2df6af4024',
}
bad = []
headof = {n: h for n, _, _, h, *_ in PRS}
LANDED = {}
for n, t, br, h, ahead, nf, tree in PRS:
    for f in git('diff', '--name-only', DEV, h).stdout.splitlines():
        LANDED[f] = (rp(h + ':' + f), n)
for p, (b, n) in LANDED.items():
    if len(b) != 40: bad.append(('landed blob unreadable', n, p))
    if p not in DEVPIN: bad.append(('PR file not pinned at develop (a new file?)', n, p))
    if p in DEVPIN and DEVPIN[p] == b: bad.append(('head blob == develop blob', n, p))
for p, b in DEVPIN.items():
    if rp(DEV + ':' + p) != b: bad.append(('develop blob', p, b, rp(DEV + ':' + p)))
NEWFILES = sorted(p for p in LANDED if p not in DEVPIN)
print('landed paths', len(LANDED), '| new files (ABSENT at develop):', len(NEWFILES), '| judged develop paths', len(DEVPIN))
if len(LANDED) != 2 or NEWFILES: bad.append(('want 2 landed paths, 0 new', len(LANDED), NEWFILES))
for run, _ in CANON.values():
    tip = re.search(r'"tip":\s*"([0-9a-f]{40})"', open(RUNS + run + '/input.json').read())
    ok = bool(tip) and tip.group(1) == DEV
    print('  run %s written at tip %s == develop pin: %s' % (run, tip.group(1)[:9] if tip else None, ok))
    if not ok: bad.append(('run tip != develop pin', run))
    ck = RUNS + run + '/out.md.checker/'
    extra = [f for f in os.listdir(ck) if f.endswith('.opts') or re.match(r'section_\d+\.diff$', f)]
    if extra: bad.append(('an opts / section file exists; this batch is strict patch.diff only', run, extra))

# 1. origin, read-only (git ls-remote): develop, both refs/pull/N/head and both branches
t0 = now()
refs = ['refs/heads/develop'] + [x for n, _, br, *_ in PRS for x in ('refs/pull/%d/head' % n, 'refs/heads/' + br)]
lsr = dict(reversed(l.split('\t')) for l in git('ls-remote', 'origin', *refs).stdout.strip().splitlines())
print('ls-remote', t0, '->', now(), '|', len(lsr), 'refs read')
if lsr.get('refs/heads/develop') != DEV: bad.append(('origin develop moved', lsr.get('refs/heads/develop')))
for n, t, br, h, *_ in PRS:
    a, b = lsr.get('refs/pull/%d/head' % n), lsr.get('refs/heads/' + br)
    print('  #%d %-10s pull/head %s branch %s  %s' % (n, t, (a or 'NONE')[:9], (b or 'NONE')[:9], 'OK' if a == b == h else 'MOVED'))
    if not (a == b == h): bad.append(('head moved', n, a, b))

# 2. PR shape against local objects
allfiles = []
for n, t, br, h, ahead, nf, tree in PRS:
    files = sorted(git('diff', '--name-only', DEV, h).stdout.splitlines()); allfiles += files
    chain = git('rev-list', '--first-parent', DEV + '..' + h).stdout.split()
    npars = [len(git('rev-list', '--parents', '-n', '1', c).stdout.split()) - 1 for c in chain]
    base_ok = git('merge-base', DEV, h).stdout.strip() == DEV and rp(chain[-1] + '^1') == DEV if chain else False
    ok = len(chain) == ahead and all(x == 1 for x in npars) and base_ok and len(files) == nf and rp(h + '^{tree}') == tree
    print('#%d %-10s head %s ahead %d parents %s base=develop %s files %d tree %s  %s' % (n, t, h[:9], len(chain), npars, base_ok, len(files), rp(h + '^{tree}')[:9], 'OK' if ok else 'BAD'))
    if not ok: bad.append(('PR shape', n, files, chain))
    prod = [f for f in files if '/src/__tests__/' not in f]
    dels = sum(int(l.split('\t')[1]) for l in git('diff', '--numstat', DEV, h).stdout.splitlines())
    print('    files outside src/__tests__/: %d %s (want 0) | deleted lines %d%s' % (len(prod), [f.split('/')[-1] for f in prod], dels, ' — TIER 1' if n in TIER1 else ''))
    if prod: bad.append(('product bytes', n, prod))
    if dels: bad.append(('deleted lines (the READY says 0)', n, dels))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 2: bad.append(('two PRs not pairwise file-disjoint / not 2 files', allfiles))
print('pairwise disjoint: %d files, %d distinct (overlap %d)' % (len(allfiles), len(set(allfiles)), len(allfiles) - len(set(allfiles))))
msg = {n: git('log', '-1', '--format=%s%n%b', h).stdout for n, _, _, h, *_ in PRS}
trap = all('KS-%d' % n not in msg[n] for n, *_ in PRS) \
       and all(sorted(re.findall(r'^Refs (KS-\d+)\s*$', msg[n], re.M)) == sorted(WANTREFS[n]) for n in WANTREFS) \
       and all(not re.search(r'ks-?1215', msg[n], re.I) for n, *_ in PRS)
print('namespace trap (no commit names KS-<its own PR number>; Refs exactly #1100 KS-1230 / #1101 KS-1282; no ks1215 / ks-1215 in either message):', trap)
if not trap: bad.append(('namespace trap / Refs', {n: msg[n][:60] for n in msg}))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
SCRATCH = os.environ.get('GEN_SCRATCH') or tempfile.gettempdir()
X = tempfile.mkdtemp(prefix='genb1100-', dir=SCRATCH)
def seed(W, target):
    files = git('diff', '--name-only', DEV, target).stdout.splitlines()
    for f in files:
        os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
        open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    return files
for n, t, br, h, *_ in PRS:
    W = os.path.join(X, 'canon-%d' % n); os.makedirs(W)
    files = seed(W, h)
    run, nm = CANON[n]
    r = subprocess.run(['git', 'apply', sec(run, nm)], cwd=W, capture_output=True, text=True)
    if r.returncode: print('  #%d %s git apply rc %d %s' % (n, NAME[CANON[n]], r.returncode, r.stderr.strip()[:120])); bad.append(('canonical apply', n)); continue
    for f in files:
        got = subprocess.run(['git', 'hash-object', os.path.join(W, f)], capture_output=True, text=True).stdout.strip()
        want = rp(h + ':' + f)
        print('  #%d canonical [%s] %s -> %s == head %s: %s' % (n, NAME[CANON[n]], f.split('/')[-1], got[:12], want[:12], got == want))
        if got != want: bad.append(('canonical patch != PR', n, f))
for n, t, br, h, *_ in PRS:
    run, nm = CANON[n]
    W = os.path.join(X, 'control-reverse-%d' % n); os.makedirs(W); seed(W, h)
    r = subprocess.run(['git', 'apply', '--reverse', '--check', sec(run, nm)], cwd=W, capture_output=True, text=True)
    print('  CONTROL #%d %s --reverse onto develop blobs refuses: rc %d (want non-zero)' % (n, NAME[CANON[n]], r.returncode))
    if r.returncode == 0: bad.append(('reverse control applied', n))
W = os.path.join(X, 'control-crossed'); os.makedirs(W); seed(W, headof[1100])
r = subprocess.run(['git', 'apply', '--check', sec(*N99_1)], cwd=W, capture_output=True, text=True)
print('  CONTROL crossed: #1101 N99-1 patch into #1100 develop blobs refuses: rc %d (want non-zero)' % r.returncode)
if r.returncode == 0: bad.append(('crossed control applied',))
print('scratch (plain files, not a repo; left in place):', X)

# 3b. the four tamper plants, re-planted by TEXT from the develop blob, each ALONE
srcs = {p: gitb('cat-file', 'blob', DEV + ':' + p) for p in (ADMINTS, PLATTS)}
for p, raw in srcs.items():
    print('  %s at develop: blob %s sha256 %s bytes %d (pre-plant want %d)' % (p.split('/')[-1], rp(DEV + ':' + p)[:12], hashlib.sha256(raw).hexdigest()[:12], len(raw), PREBYTES[p]))
    if len(raw) != PREBYTES[p]: bad.append(('pre-plant bytes', p, len(raw)))
for tid, path, line, run, psha, post in TAMPERS:
    inp = json.load(open(RUNS + run[0] + '/input.json'))
    t = [x for x in inp['tampers'] if x['id'] == tid][0]
    txt = srcs[path].decode('utf-8'); lines = txt.split('\n')
    whole = sum(1 for l in lines if l == t['from']); subs = txt.count(t['from'])
    landed = [i + 1 for i, l in enumerate(lines) if l == t['from']]
    out = None
    if whole == 1:
        l2 = list(lines); l2[landed[0] - 1] = t['to']; out = '\n'.join(l2)
    got = hashlib.sha256(out.encode()).hexdigest()[:12] if out else None
    nb = len(out.encode()) if out else -1
    okt = whole == 1 and subs == 1 and landed == [line] and got == psha and nb == post
    print('  %-18s %s:%-5d whole-line x%d raw x%d landed %s | plant sha256 %s == %s | bytes %d -> %d == %d : %s'
          % (tid, path.split('/')[-1], line, whole, subs, landed, got, psha, len(srcs[path]), nb, post, okt))
    if not okt: bad.append(('tamper plant', tid, whole, subs, landed, got, nb))
# the shared line: LASTOF2NULLMIXED and LASTOF4NULL share ONE `from` and have two DIFFERENT `to`s
fr = {}; to = {}
for tid, path, line, run, psha, post in TAMPERS:
    t = [x for x in json.load(open(RUNS + run[0] + '/input.json'))['tampers'] if x['id'] == tid][0]
    fr[tid] = t['from']; to[tid] = t['to']
shared = fr['LASTOF2NULLMIXED'] == fr['LASTOF4NULL'] and to['LASTOF2NULLMIXED'] != to['LASTOF4NULL']
print('  SHARED LINE admin.ts:1132 — one from, two different tos:', shared)
if not shared: bad.append(('shared line',))
# the :67 -> :68 correction (Wednesday brief and the PRIOR REPORT row said :67)
pl = srcs[PLATTS].decode('utf-8').split('\n')
corr = pl[66] == '  const user = req.user;' and pl[67] == '  if (!user || !SUPER_ROLES.includes(user.role)) {' \
       and pl[63] == "const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];"
print('  platform.ts:64 SUPER_ROLES / :67 const user / :68 the guard condition (the seat CORRECTED Wednesday:67 -> :68):', corr)
print('    :67 %r\n    :68 %r' % (pl[66], pl[67]))
if not corr: bad.append((':67 -> :68 correction',))
nguard = sum(1 for l in pl if l == '    requireSuperAdmin,')
print('  bare "    requireSuperAdmin," whole-line count in platform.ts: %d (a plant on the FIRST is VOID)' % nguard)
if nguard != 13: bad.append(('requireSuperAdmin line count', nguard))
# the FINDING's file is untouched by both patches and byte-identical at develop and both heads
DBR = A + 'src/__tests__/db.retry.test.ts'
b0 = rp(DEV + ':' + DBR)
same = all(rp(h + ':' + DBR) == b0 for _, _, _, h, *_ in PRS) and b0 == DEVPIN[DBR]
npat = sum(open(sec(*CANON[n])).read().count('db.retry') for n in CANON)
print('  FINDING file db.retry.test.ts blob %s identical at develop and both heads: %s | "db.retry" in the canonical patches: %d (want 0)' % (b0[:12], same, npat))
if not same or npat: bad.append(('finding file', b0, same, npat))
if bad: print('REFUSING:', bad); sys.exit(1)

# 4. the both-PRs tree by pure tree hashing (read-only cat-file), controlled by each single head tree
def read_tree(oid):
    raw = gitb('cat-file', 'tree', oid); ents = []; i = 0
    while i < len(raw):
        sp = raw.index(b' ', i); nul = raw.index(b'\0', sp)
        ents.append((raw[i:sp], raw[sp + 1:nul], raw[nul + 1:nul + 21])); i = nul + 21
    return ents
def hash_tree(ents):
    key = lambda e: e[1] + (b'/' if e[0] == b'40000' else b'')
    body = b''.join(m + b' ' + nm + b'\0' + sha for m, nm, sha in sorted(ents, key=key))
    return hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest(), body
def compose(tree_oid, changes):
    ents = {e[1]: e for e in read_tree(tree_oid)}
    sub = {}
    for parts, v in changes.items():
        if len(parts) == 1: ents[parts[0]] = (v[0], parts[0], bytes.fromhex(v[1]))
        else: sub.setdefault(parts[0], {})[parts[1:]] = v
    for d, ch in sub.items():
        if d not in ents: raise SystemExit('new directory not supported: %r' % d)
        ents[d] = (b'40000', d, bytes.fromhex(compose(ents[d][2].hex(), ch)))
    oid, _ = hash_tree(list(ents.values())); return oid
def pr_changes(h):
    ch = {}
    for l in git('diff', '--raw', '--no-abbrev', DEV, h).stdout.splitlines():
        meta, path = l.split('\t', 1); f = meta.split()
        assert f[4] == 'M', ('only M expected in this batch', l)
        ch[tuple(x.encode() for x in path.split('/'))] = (f[1].encode().lstrip(b'0') or b'0', f[3])
    return ch
devtree = rp(DEV + '^{tree}'); allch = {}
for n, t, br, h, ahead, nf, tree in PRS:
    ch = pr_changes(h); allch.update(ch)
    got = compose(devtree, ch)
    print('  control #%d: develop tree + its delta -> %s == head tree %s' % (n, got[:9], got == tree))
    if got != tree: bad.append(('tree-hash control', n, got))
comb = compose(devtree, allch)
print('BOTH over develop (tree-object hashing, no git write) -> %s | READY %s: %s' % (comb, COMBINED[:9], comb == COMBINED))
if comb != COMBINED: bad.append(('combined tree', comb))
GS = os.path.dirname(os.path.abspath(__file__))
rd = lambda nm: open(os.path.join(GS, nm)).read()
scr = rd('predict_both_scratch.out')
scr_ok = all(re.search(lab + r': 2 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None for lab in ('1230then1282', '1282then1230')) \
         and ('scratch-index ' + COMBINED) in scr and 'PREDICTION OK' in scr and 'rc=0' in scr and scr.count(': True') >= 6
mes = rd('measure_scratch.out')
mes_ok = 'ALL OK' in mes and 'rc=0' in mes and all(k in mes for k in ('47724925d360', '3e08ce6b879e', '0acfe0d608fd', 'b83e48fdbe83')) \
         and 'is the guard line' in mes and mes.count('rc 1 (want non-zero)') == 3
shp = rd('shape_scratch.out')
shp_ok = 'overlap 0' in shp and 'rc=0' in shp and shp.count('(==develop True)') == 2
print('scratch-clone prediction (both merge orders + index composition + read-tree-back control) names', COMBINED[:9], 'and PREDICTION OK:', scr_ok)
print('measure_scratch: canonical identity, three refusing controls, the four plants, the :67 -> :68 correction, the finding file:', mes_ok)
print('shape_scratch: both PRs one commit on develop, overlap 0:', shp_ok)
if not (scr_ok and mes_ok and shp_ok): bad.append(('drafter measurements', scr_ok, mes_ok, shp_ok))
ghr = rd('gh_pr_reads.out')
gh_ok = 'ZERO PRODUCT BYTES in both (files API): True' in ghr and ghr.count('files outside src/__tests__/ (files API): 0 [] | deletions total 0') == 2 \
        and 'TIER 1 #1101: one file, zero product bytes (files API): True' in ghr and 'rc=0' in ghr and ghr.count('O-1 detector hits title/body/commit 0/0/0') == 2 \
        and 'Refs lines as wanted (#1100 KS-1230; #1101 KS-1282): True' in ghr and ghr.count('ks1215/ks-1215 in branch/title/commit-subject []') == 2 \
        and '#1101 carries NO completeness claim and NO guard count in title/body/commit: True' in ghr \
        and ghr.count('completeness-claim detector hits title/body/commit (0, 0, 0) | guard-count detector hits (0, 0, 0)') == 2 \
        and "'require_extra_approval_for_unattributed_changes': True" in ghr and "'required_approving_review_count': 0" in ghr
print('PR files API (gh_pr_reads.out): zero product bytes x2, #1101 by name, Refs as wanted, O-1 0 x2, NO completeness claim / NO guard count, ruleset as read:', gh_ok)
lin = rd('linear_reads.out')
lin_ok = "attachmentsForURL pull/1100 -> [('KS-1230', 'contributes')]" in lin and "attachmentsForURL pull/1101 -> [('KS-1282', 'contributes')]" in lin \
         and 'namespace KS-1100: state Backlog archivedAt None attachments []' in lin and "namespace KS-1101:" in lin \
         and "archivedAt 2026-09-13T05:35:48.754Z" in lin and "attachments [('932', 'closes')]" in lin and 'archivedAt 2026-09-19T19:55:22' in lin \
         and "[('1034', 'contributes')]" in lin and 'rc=0' in lin
print('Linear (linear_reads.out): attachmentsForURL exactly {KS-1230} / {KS-1282}, the namespace tickets read, KS-1062 + KS-1238 archived, KS-1215 #1034:', lin_ok)
if not (gh_ok and lin_ok): bad.append(('files API / Linear reads', gh_ok, lin_ok))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-20_gate1100to1101/mail_batch1100_ready.md'
PROMPT = WEDB + 'briefs/2026-09-20_secuura-batch1100-1101.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1097-1099-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1092-1096-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1100-#1101 (two PRs; tier 1 = #1101 KS-1282)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-9th/'
assert os.path.isdir(PRIOR) and os.path.isdir(EARLIER) and os.path.isdir(SEATHIST), 'prior / earlier report or seat history dir missing'
assert os.path.isfile(PRIOR + 'report.md'), 'PRIOR REPORT has no report.md'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head in full'
assert 'MESSAGE_ID: <010001a0bd890a6f-286e9774-1ebe-4e80-b76b-55e4cc7831a0-000000@email.amazonses.com>' in mt_ and 'TS: 2026-09-20T06:37:50' in mt_, 'mail capture is not the 06:37:50Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED in mt_ and COMBINED in pt_, 'both-PRs tree not named in mail AND prompt'
assert DEV in mt_ and DEV in pt_, 'develop pin not named in mail AND prompt'
for n in LABEL:
    line = [l for l in mt_.splitlines() if l.startswith('| #%d | ' % n)]
    assert ('PR #%d is %s.' % (n, LABEL[n])) in pt_ and len(line) == 1 and all(k_ in line[0] for k_ in KEYS[n]), ('namespace trap not named for', n, LABEL[n])
assert not re.search(r"waits for Kam.s tap|on Kam.s tap only|signed GO alone", pt_ + mt_, re.I), 'a Kam-tap / not-alone condition in the prompt or READY'
assert not re.search(r'\brule (KS-1282|it) COMPLETE\b(?! or NOT-COMPLETE)', pt_), 'the prompt asks for a KS-1282 completeness ruling'

HEADER_OLD = cut('# launch_qa_secuura_batch1097_1099.sh', '# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1100_1101.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over TWO file-disjoint Secuura/Blockchain PRs
#   #1100 KS-1230 @ 99ce89e74  ks1230 vitest test: N97-1, a null allow-list LAST of two (mixed) and LAST of four (admin.ts:1132) — TIER 2 (test-only)
#   #1101 KS-1282 @ dc40087e7  ks1215 vitest test: N99-1, a tenant ADMIN JWT is refused 403 on GET /api/platform/tenants with nothing forwarded
#         (platform.ts:64 SUPER_ROLES and :68 the requireSuperAdmin condition) — TIER 1 (AUTH, test-only), pushed LAST
# BOTH ARE TEST-ONLY: every changed path is under api-gateway src/__tests__/ (generator: local objects AND the PR files API; 0 product bytes, 0
# deleted lines; #1101 asserted by name).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the both-PRs tree by pure tree hashing and by scratch-clone
# merges in BOTH orders; the four plant sha256s re-planted by text; the :67 -> :68 correction re-read at develop.
# KS-1282 completeness is KAM ruling, already given — the gate rules nothing about it and only grades the seat facts-comment bytes.
# NAMESPACE TRAP: the PR numbers are other tickets numbers too (KS-1100 Backlog, KS-1101 In Progress with #1063 + #1037); the READY mail AND the
# prompt must BOTH state which ticket each of the two PRs is, or the launch refuses (exit 32).
# Batched under Kam 2026-09-18 standing rule. TWO verdicts, one per head; one PR failing does not block the other. Merge authority for each:
# WEDNESDAY'S signed GO naming its head, under Kam TESTED grant (exit 26).
#
# THE SHAPE, re-read live 2026-09-20T06:41Z (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop e47019878; compare develop...head = merge_base e47019878, ahead 1, files 1 each (asserted per PR, exit 10).
# Pairwise file-disjoint (2 files, all modified, 0 new, overlap 0). Each PR over develop is a fast-forward (merged tree = head tree). BOTH = tree
# 1ccb80e0d, re-derived by the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains in
# BOTH orders, an index composition, and a read-tree back to develop as a control). Both are byte-identical to their CANONICAL local-model
# patch.diff, re-applied strict by the generator in a plain scratch dir, each reverse-applied control refusing and a crossed patch refusing.
#
# The develop pin is judged by CONTENT — TWENTY paths by blob at the CURRENT develop: the 2 PR files (both at develop blobs; either PR head blob
# -> exit 19 LANDED, naming the PR), and what the gate runs or reads: platform.ts (SUPER_ROLES :64, the guard :68, the 13 requireSuperAdmin
# registrations, the pg.Pool routes), admin.ts (:1132), db.retry.test.ts (the FINDING file, which must stay byte-identical for the seat
# measurement to mean anything), proxy.ts, verification.ts, auth.ts, index.ts (the mount order), preflight.sh, run-shell-suites.sh, the pre-push
# hook, the api-gateway configs incl. vitest.setup.ts, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-20_gate1100to1101/mail_batch1100_ready.md, the seat READY mail (06:37:50Z) captured verbatim by message id from
# wednesday-agent@.
#
# exit 6:  either head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line.
# exit 20: the READY mail AND the prompt must name both heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and TWO verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1097-#1099 batch), the EARLIER REPORT (the #1092-#1096 batch) and
#          NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state' and
#          'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat 2026-09-20_seatB-9th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat items (ruleset 18499832, the per-PR and both-PRs trees, the four plant sha256s,
#          the tamper ids, the develop byte counts, the FINDING numbers and blob, the census words), and the prompt must ask the gate to MEASURE,
#          not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the both-PRs tree in full, the NOT-PINNED list with a proposed cell per row, and a loopback GATEWAY_URL for any
#          preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the two, which ticket the PR is (PR #1100 is KS-1230, PR #1101 is KS-1282).
# exit 33: the prompt must carry Wednesday BY-NAME items: tier + round 1 of 2 + ZERO product bytes on #1101; BOTH MERGE ORDERS; the SHARED LINE
#          admin.ts:1132 with each plant ALONE; the :67 -> :68 correction; the FINDING with RULE WHETHER IT BLOCKS; NO completeness claim and NO
#          guard count; the KS-1282 FACTS-COMMENT BYTES with completeness as Kam call; the real Postgres on 127.0.0.1:5432; attachmentsForURL +
#          includeArchived; the NOT-PINNED row format; the MERGE ADDENDUM; NOTHING ABOUT O-1.
# QAB1100_CUR_DEV (test override, --check only): stands in for origin develop. QAB1100_HEAD_1101 (test override): stands in for #1101 pinned head.
# QAB1100_PLATFORMTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/platform.ts (its git blob).
# A launch with any QAB1100_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-20_gate1100to1101/gen_launcher_batch1100_1101.py from launch_qa_secuura_batch1097_1099.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + the four plants re-planted + both-PRs tree re-derived + residual guard + output controls
# + bash -n).
#
# Usage: launch_qa_secuura_batch1100_1101.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != OVERRIDE else '${QAB1100_HEAD_1101:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1097_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1100_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1100_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (06:37:50Z) and re-read by the drafter (git ls-remote 06:41Z, branch AND refs/pull/N/head)\n'
            '# NAMESPACE TRAP: neither PR is its own-numbered ticket (KS-1100 and KS-1101 are other tickets); the ticket column is the truth (exit 32)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 06:41Z; both heads merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            "EARLIER_REPORT='" + EARLIER + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADSC_OLD = '# The three heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.\n'
HEADSC_NEW = '# The two heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.\n'
CMPC_OLD = cut('# develop...head = c87458bdd ahead 1 for all three PRs; files 1 each\n', '(git diff --name-only + rev-list, drafter 04:4x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = e47019878 ahead 1 for both PRs; files 1 each\n'
            '# (git diff --name-only + rev-list, drafter 06:4x Z; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1097 $MERGE_BASE', '1099 $MERGE_BASE ahead=1 files=1"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): twenty-one paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): twenty paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN)
assert len(JPATHS) == 20, ('judged path count', len(JPATHS))
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p]
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k_ = 'PLATFORMTS' if p == PLATTS else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k_, ' ' * max(1, 80 - len(k_)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\n'
              'PLATFORMTS = A + "src/routes/platform.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; either PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of both heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr) for n, _, _, _, _, _, tr in PRS) + '; both together ' + COMBINED + ', drafter tree-hash, two-order scratch-clone merges and scratch-index composition; git ls-remote)"); sys.exit(0)\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the three heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the two heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; both together '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway src/ + config, packages/shared src/, scripts/, .githooks/, '
               'the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, LABEL[n], 1 if n in TIER1 else 2) for n in LABEL]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
SEATWORDS = ['PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state', 'zero product bytes']
GWORDS = ['18499832', COMBINED, '68dc2d63123d48cc2f3473d05aa16013eba1d7c3', '6d62805ccc009b7dca16041653bea89c46a33700',
          '893879a1995031a13d4a1969d24f3aa0c60e5d21', '50298953359ead9f947ac9f20f455a529dd2543a',
          '47724925d360', '3e08ce6b879e', '0acfe0d608fd', 'b83e48fdbe83',
          'LASTOF2NULLMIXED', 'LASTOF4NULL', 'SUPERROLESWIDEN', 'SUPERADMITSANYUSER',
          '7d04a92ca724', '44888', '74087', '5933da41ed3dcf37f415000c4da4a717ea8d7eba', 'KS-1155', '8655', '7483',
          'STOP-class 0', ':5432', '127.0.0.1:1', '674', '671', '706de83052728ddfe4c581e378f708fec2338b80', DEV]
for w in SEATWORDS + GWORDS: assert w in pt_ and w in mt_, ('READY mail and prompt must both carry', w)
BYNAME = ['round 1 of 2', 'ZERO product bytes on #1101', 'BOTH MERGE ORDERS', 'SHARED LINE admin.ts:1132',
          'each planted ALONE and never stacked', 'the :67 -> :68 correction', 'RULE WHETHER IT BLOCKS',
          'NO completeness claim and NO guard count', 'THE KS-1282 FACTS-COMMENT BYTES', 'completeness is Kam',
          'a real Postgres listens on 127.0.0.1:5432', 'attachmentsForURL', 'includeArchived',
          'SAME ROW FORMAT as the PRIOR REPORT', 'ONE MERGE ADDENDUM line PER PR', 'NOTHING ABOUT O-1',
          'must not recommend pinning either']
for w in BYNAME: assert "'" not in w, ('an apostrophe would break the single-quoted grep', w)
for w in BYNAME: assert w in pt_, ('prompt lacks the by-name item', w)
assert 'MEASURE, not conclude' in pt_ and 'two lines, one per pr' in pt_.lower() and 'proposed cell' in pt_ \
       and 'GATEWAY_URL=http://127.0.0.1:' in pt_, 'prompt phrasing'
TRAPGREP = ' && '.join("grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\" && " % (n, LABEL[n])
                       + ' && '.join("grep -F '| #%d | ' \"$BRIEF\" | grep -qF '%s'" % (n, k_) for k_ in KEYS[n]) for n in LABEL)
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", 'exit 33; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1101 T1, #1100 T2)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat READY mail capture path" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "$_h" "$BRIEF" \
    || { echo "REFUSING: the READY mail or the prompt does not name #$_n's head $_h — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'TWO lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and TWO verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
''' + ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -qF '%s' \"$BRIEF\"" % (w, w) for w in SEATWORDS) + r''' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat 2026-09-20_seatB-9th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
''' + ''.join('grep -qF -- \'%s\' "$PROMPT_FILE" && grep -qF -- \'%s\' "$BRIEF" && ' % (w, w) for w in GWORDS) + r'''grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat items, or the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the both-PRs tree in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
''' + TRAPGREP + r''' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket each PR is (PR #1100 is KS-1230, PR #1101 is KS-1282) — the PR numbers are other tickets numbers too" >&2; exit 32; }
''' + ' && '.join('grep -qF -- \'%s\' "$PROMPT_FILE"' % w for w in BYNAME) + r''' \
  || { echo "REFUSING: the prompt does not carry Wednesday by-name items (tier + round 1 of 2 + zero product bytes on #1101, both merge orders, the shared line with each plant alone, the :67 -> :68 correction, the finding with RULE WHETHER IT BLOCKS, no completeness claim and no guard count, the KS-1282 facts-comment bytes with completeness as Kam call, the real Postgres on :5432, attachmentsForURL + includeArchived, the NOT-PINNED row format, the merge addendum, nothing about O-1)" >&2; exit 33; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  two heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1101 T1, #1100 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name both heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, TWO verdict lines"
  echo "  prompt names the report directory, the #1097-#1099 batch PRIOR REPORT, the EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat 2026-09-20_seatB-9th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat items; the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names the both-PRs tree, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket each of the two PRs is (namespace trap; KS-1100 and KS-1101 are other tickets)"
  echo "  prompt carries Wednesday by-name items: tier/round/zero bytes, both merge orders, the shared line, the :67 -> :68 correction, the finding ruling, no completeness claim or guard count, the facts-comment bytes, Postgres :5432 isolation, link hygiene, NOT-PINNED, addendum, nothing about O-1"
  [ -n "${QAB1100_CUR_DEV:-}" ] && echo "  (develop read from the QAB1100_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1100_PLATFORMTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/platform.ts read from the QAB1100_PLATFORMTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('heads comment', HEADSC_OLD, HEADSC_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1097_CUR_DEV:-', 'CUR_DEV="${QAB1100_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1097_PLATFORMTS_FILE", "") if f == PLATFORMTS else ""\n',
                 '    fixture = os.environ.get("QAB1100_PLATFORMTS_FILE", "") if f == PLATFORMTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1097_BRIEF:-}${QAB1097_PROMPT:-}${QAB1097_HEAD_1099:-}${QAB1097_CUR_DEV:-}${QAB1097_PLATFORMTS_FILE:-}" ]',
            '[ -z "${QAB1100_BRIEF:-}${QAB1100_PROMPT:-}${QAB1100_HEAD_1101:-}${QAB1100_CUR_DEV:-}${QAB1100_PLATFORMTS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1097-1099 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1097-#1099 batch': 2, 'from launch_qa_secuura_batch1097_1099.sh': 1}   # exit 24 comment + --check line; the template
for k_, v in INTENDED.items():
    assert BODY.count(k_) == v, ('intended citation count', k_, BODY.count(k_), v)
    BODY = BODY.replace(k_, '<CITED>')
RESID = ['QAB1097_', 'mail_batch1097', 'gate1097to1099', 'batch1097', 'c87458bdd', '458cff717', 'f893a92cf', 'seatB-8th', 'three', 'THREE',
         'twenty-one', 'TWENTY-ONE', 'startup-migrations', 'VERIFTS', 'N92-1', 'N93-1', 'N95-1', 'N96-1', 'KS-1238', 'KS-1062',
         'ADMINSHADOW', 'FIRSTOF', 'ONESKIPPED', 'ALLFAILED', 'GUARD284', '77f4ec90', 'COMPLETE or NOT-COMPLETE', 'octopus', 'eleven',
         'seatB-8', '04:41:46', '04:4x AEST', 'PR #1097 is', '18:38:22', 'F1_REPORT', 'twelve']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])(109[7-9])(?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {REPORT_DIR: 1, PRIOR: 1, EARLIER: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT"': None,
       'QAB1100_CUR_DEV': None, 'QAB1100_PLATFORMTS_FILE': None, 'QAB1100_HEAD_1101': None, 'refs/pull/$_n/head': 2,
       'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None, 'exit 27': None, 'exit 28': None,
       'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 32': None, 'exit 33': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-20_secuura-batch1100-1101.prompt.txt': 1, 'gatesets/2026-09-20_gate1100to1101/mail_batch1100_ready.md': None,
       '"BACKLOG.md"]': 1, 'A + "src/",': 1, 'D + "packages/shared/src/",': 1, 'D + "scripts/",': 1, '".githooks/",': 1,
       'ahead=1 files=': 2, 'PLATFORMTS': None}
for n in LABEL:
    CTL["grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\"" % (n, LABEL[n])] = 1
    for k_ in KEYS[n]: CTL["grep -F '| #%d | ' \"$BRIEF\" | grep -qF '%s'" % (n, k_)] = 1
got = {k_: s.count(k_) for k_ in CTL}
print('output controls', {(k_[:24] + '…' if len(k_) > 24 else k_): v for k_, v in got.items()})
for k_, v in CTL.items():
    if k_ == '"ABSENT"':
        if got[k_] != 1: print('CONTROL DISAGREED', k_, got[k_], 'want 1 (the 404 branch only; this batch has no new file)'); sys.exit(1)
        continue
    if (v is not None and got[k_] != v) or got[k_] == 0: print('CONTROL DISAGREED', k_, got[k_], v); sys.exit(1)
# every pinned sha appears exactly once for its own use, plus twice per GWORDS grep pair (prompt + brief)
def want_count(tok, base): return base + (2 if tok in GWORDS else 0)
for p, b in DEVPIN.items():
    w = want_count(b, 1)
    if s.count(b) != w: print('CONTROL DISAGREED develop pin', p, s.count(b), w); sys.exit(1)
for p, (b, n) in LANDED.items():
    w = want_count(b, 1)
    if s.count(b) != w: print('CONTROL DISAGREED landed pin', n, p, s.count(b), w); sys.exit(1)
for tok, base in ((DEV, 1), (COMBINED, 2)) + tuple((tr, 1) for *_x, tr in PRS):
    w = want_count(tok, base)
    if s.count(tok) != w: print('CONTROL DISAGREED token', tok[:12], s.count(tok), w); sys.exit(1)
    print('  token control %s count %d (want %d)' % (tok[:12], s.count(tok), w))
for n, t, br, h, *_ in PRS:
    if s.count(h) != 1 or s.count('refs/heads/' + br + '|') != 1: print('CONTROL DISAGREED head/branch', n, s.count(h), s.count(br)); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    for i in [m.start() for m in re.finditer(re.escape(tag), s)]:
        end = '\nPY' + ('J' if 'PYJ' in tag else '') + '\n'; j = s.index(end, i); blk = s[i:j]
        print('heredoc', tag.strip(), '@', s.count('\n', 0, i) + 1, 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
        if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull|merge-tree)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
if os.path.exists(OUT): print('REFUSING: output exists; never overwrite from this generator', OUT); sys.exit(1)
tmp = OUT + '.gen-tmp'
if os.path.exists(tmp): print('REFUSING: a previous tmp output exists; never overwrite it', tmp); sys.exit(1)
open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp); sys.exit(3)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
