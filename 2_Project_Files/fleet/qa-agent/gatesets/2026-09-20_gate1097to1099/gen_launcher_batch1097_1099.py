#!/usr/bin/env python3
"""gen_launcher_batch1097_1099.py — derive launchers/launch_qa_secuura_batch1097_1099.sh from launchers/launch_qa_secuura_batch1092_1096.sh (the
batch gate prepared 2026-09-20 01:1x AEST, one gate / five verdicts, which ran cleanly) by ASSERTED block substitutions: every anchor must occur
exactly as often as stated, or the generator refuses and writes nothing. Structure copied from gatesets/2026-09-20_gate1092to1096/
gen_launcher_batch1092_1096.py; the data changed, the by-name guard (exit 33) carries this batch's eleven items, the namespace guard (exit 32) reads
the READY's table rows, and the develop fixture now stands in for platform.ts (the tier-1 guards' file) instead of verification.ts.

ONE BATCHED gate, TIER 1 floor (set by #1099 KS-1238 + KS-1282, auth, test-only), THREE PRs #1097..#1099 (Seat B 8th, READY 2026-09-19T18:38:22Z).
ALL THREE ARE TEST-ONLY: every changed path sits under api-gateway src/__tests__/ (asserted from local objects here AND from the PR files API read
in gh_pr_reads.out beside this file). NAMESPACE TRAP: KS-1097..KS-1099 exist; PR #1097 is KS-1230, #1098 KS-1062 (archived: NO Refs, NO key), #1099
KS-1238 + KS-1282. The launcher refuses (exit 32) unless the prompt AND the READY both state which ticket(s) each PR is.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (rev-parse / cat-file / diff / rev-list / log): each PR is ONE commit whose parent IS develop; every file set, head tree, judged
    develop blob and landed head blob as pinned; pairwise file-disjoint (3 files, 0 new); zero product bytes and 0 deleted lines; each commit carries
    exactly its own Refs (#1097 KS-1230; #1099 KS-1238 + KS-1282) or NO KS key at all (#1098); no commit names KS-<its own PR number>; no commit
    carries ks1215 / ks-1215 (subject or body, any case);
  * CANONICAL-PATCH identity for all three (plain files in a scratch dir, `git apply` strict, `git hash-object` without -w): #1097 = N92-1, #1098 =
    N93-1, #1099 = N95-1 + N96-1a + N96-1b in ALL SIX orders; every non-empty subset of the three in every order = the READY's prefix; every patch
    reversed onto develop refuses; a crossed patch refuses;
  * the ALL-THREE TREE re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, controlled by re-deriving each head tree the
    same way; it must equal the builder's 706de8305 and its local octopus commit f893a92cf's tree. The drafter's two scratch-clone predictions
    (predict_all_three_scratch.out: merge-tree chains in THREE orders; predict_index_scratch.out: index composition), measure_scratch.out,
    step_trees_scratch.out, gh_pr_reads.out and linear_reads.out are asserted here.
Usage: gen_launcher_batch1097_1099.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, itertools, os, re, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1097_1099', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = 'c87458bdd8a9dd5ae3a082612e467cda5539aebc'   # develop at 18:39:34Z / 18:41:46Z (#1092-#1096 merged); every PR's merge-base; every run's tip
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd1ce61d-09bc-4b11-b5ed-43cb67420198/scratchpad'
# n, ticket (no spaces: the launcher's PRS_FLAT splits on whitespace), branch, head, ahead, file count, head tree
PRS = [
 (1097, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n92-1', 'f5364217952c1cb4d3755fbf8604b3edde124c42', 1, 1, 'dff1aafa3581c5707fd56d3d009d811180ba83e3'),
 (1098, 'KS-1062', 'feature/pin-startup-migrations-one-skipped-counted-and-all-failed-incomplete', 'efce14bed4a8adda15bca124fa60ae7d894fa6a6', 1, 1, '9da0c747cb375ab59fd5492298e55b892ff12a73'),
 (1099, 'KS-1238+KS-1282', 'feature/ks-1238-n95-1-n96-1-pin-admin-shadow-401-and-superadmin-guards', 'b68aaf9b4581e67369be33d8ebcf4d61886c039b', 1, 1, 'c65575ff98d0610b0c472521311d16478bb0e8e8'),
]
LABEL = {1097: 'KS-1230', 1098: 'KS-1062', 1099: 'KS-1238 + KS-1282'}   # the prompt's words
KEYS = {n: LABEL[n].split(' + ') for n in LABEL}
WANTREFS = {1097: ['KS-1230'], 1099: ['KS-1238', 'KS-1282']}
ARCHIVED = {1098}                                        # KS-1062: Done + archived; NO Refs, NO KS key in the commit
TIER1 = {1099}
OVERRIDE = 1099                                          # the head the launcher's test override stands in for (pushed LAST)
COMBINED = '706de83052728ddfe4c581e378f708fec2338b80'   # builder's predicted all-three tree (READY 18:38:22Z); re-derived below
BUILDER_PREDICT_COMMIT = 'f893a92cf105a4faaacb7c48b647efe3e8fedbec'   # builder's local-only octopus (1 + 4 parents); its tree must be COMBINED
N92_1 = ('2026-09-20_ks1230-ornith35b-night', 'patch.diff'); N93_1 = ('2026-09-20_ks1062-ornith35b-night2', 'patch.diff')
N95_1 = ('2026-09-20_ks1238-ornith35b-night3', 'patch.diff'); N96_1a = ('2026-09-20_ks1282-ornith35b-night2', 'patch.diff')
N96_1b = ('2026-09-20_ks1282-ornith35b-night3', 'patch.diff')
NAME = {N92_1: 'N92-1', N93_1: 'N93-1', N95_1: 'N95-1', N96_1a: 'N96-1a', N96_1b: 'N96-1b'}
CANON = {1097: [N92_1], 1098: [N93_1], 1099: [N95_1, N96_1a, N96_1b]}
# the READY's item-0 blob prefixes for every non-empty proper subset of #1099's three (each in every order)
SUBSET = {(N95_1,): 'f9bff1b332af', (N96_1a,): '63d5c6876d82', (N96_1b,): '7c56fdbdcfde',
          (N95_1, N96_1a): '86d7faeae0e3', (N95_1, N96_1b): 'f47c8eadf237', (N96_1a, N96_1b): '6292bafe5906'}
def sec(run, name): return RUNS + run + '/out.md.checker/' + name

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': '195a1453565d83f88072a293b26385c7f9772331',
 A + 'src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts': 'c363585f6404a9b53863d76fca0afc789c46e329',
 A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': '6adc2820514ee191df201c1cbfea2062c9b12f14',
 A + 'src/routes/platform.ts': 'b80a8cd8d4e1af5a944817227f5ee6612c793954',
 A + 'src/routes/admin.ts': '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 A + 'src/startup-migrations.ts': 'ed3e521426e75910c5bf2cf07e7251f2fd8ef538',
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
if len(LANDED) != 3 or NEWFILES: bad.append(('want 3 landed paths, 0 new', len(LANDED), NEWFILES))
for run in {r for v in CANON.values() for r, _ in v}:
    tip = re.search(r'"tip":\s*"([0-9a-f]{40})"', open(RUNS + run + '/input.json').read())
    ok = bool(tip) and tip.group(1) == DEV
    print('  run %s written at tip %s == develop pin: %s' % (run, tip.group(1)[:9] if tip else None, ok))
    if not ok: bad.append(('run tip != develop pin', run))
    ck = RUNS + run + '/out.md.checker/'
    extra = [f for f in os.listdir(ck) if f.endswith('.opts') or re.match(r'section_\d+\.diff$', f)]
    if extra: bad.append(('an opts / section file exists; this batch is strict patch.diff only', run, extra))

# 1. origin, read-only (git ls-remote): develop, every refs/pull/N/head and every branch
t0 = now()
refs = ['refs/heads/develop'] + [x for n, _, br, *_ in PRS for x in ('refs/pull/%d/head' % n, 'refs/heads/' + br)]
lsr = dict(reversed(l.split('\t')) for l in git('ls-remote', 'origin', *refs).stdout.strip().splitlines())
print('ls-remote', t0, '->', now(), '|', len(lsr), 'refs read')
if lsr.get('refs/heads/develop') != DEV: bad.append(('origin develop moved', lsr.get('refs/heads/develop')))
for n, t, br, h, *_ in PRS:
    a, b = lsr.get('refs/pull/%d/head' % n), lsr.get('refs/heads/' + br)
    print('  #%d %-16s pull/head %s branch %s  %s' % (n, t, (a or 'NONE')[:9], (b or 'NONE')[:9], 'OK' if a == b == h else 'MOVED'))
    if not (a == b == h): bad.append(('head moved', n, a, b))

# 2. PR shape against local objects
allfiles = []
for n, t, br, h, ahead, nf, tree in PRS:
    files = sorted(git('diff', '--name-only', DEV, h).stdout.splitlines()); allfiles += files
    chain = git('rev-list', '--first-parent', DEV + '..' + h).stdout.split()
    npars = [len(git('rev-list', '--parents', '-n', '1', c).stdout.split()) - 1 for c in chain]
    base_ok = git('merge-base', DEV, h).stdout.strip() == DEV and rp(chain[-1] + '^1') == DEV if chain else False
    ok = len(chain) == ahead and all(x == 1 for x in npars) and base_ok and len(files) == nf and rp(h + '^{tree}') == tree
    print('#%d %-16s head %s ahead %d parents %s base=develop %s files %d tree %s  %s' % (n, t, h[:9], len(chain), npars, base_ok, len(files), rp(h + '^{tree}')[:9], 'OK' if ok else 'BAD'))
    if not ok: bad.append(('PR shape', n, files, chain))
    prod = [f for f in files if '/src/__tests__/' not in f]
    dels = sum(int(l.split('\t')[1]) for l in git('diff', '--numstat', DEV, h).stdout.splitlines())
    print('    files outside src/__tests__/: %d %s (want 0) | deleted lines %d%s' % (len(prod), [f.split('/')[-1] for f in prod], dels, ' — TIER 1' if n in TIER1 else ''))
    if prod: bad.append(('product bytes', n, prod))
    if dels: bad.append(('deleted lines (the READY says 0)', n, dels))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 3: bad.append(('three PRs not pairwise file-disjoint / not 3 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
msg = {n: git('log', '-1', '--format=%s%n%b', h).stdout for n, _, _, h, *_ in PRS}
trap = all('KS-%d' % n not in msg[n] for n, *_ in PRS) \
       and all(sorted(re.findall(r'^Refs (KS-\d+)\s*$', msg[n], re.M)) == sorted(WANTREFS[n]) for n in WANTREFS) \
       and all(not re.search(r'KS-\d+', msg[n]) for n in ARCHIVED) \
       and all(not re.search(r'ks-?1215', msg[n], re.I) for n, *_ in PRS)
print('namespace trap (no commit names KS-<its own PR number>; Refs exactly #1097 KS-1230 / #1099 KS-1238 + KS-1282; #1098 carries NO KS key; no ks1215 / ks-1215 in any message):', trap)
if not trap: bad.append(('namespace trap / Refs', {n: msg[n][:60] for n in msg}))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1097-', dir=SCRATCH)
def seed(W, target):
    files = git('diff', '--name-only', DEV, target).stdout.splitlines()
    for f in files:
        os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
        open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    return files
def apply_into(W, n, target, sections, extra=()):
    files = seed(W, target)
    for run, name in sections:
        r = subprocess.run(['git', 'apply', *extra, sec(run, name)], cwd=W, capture_output=True, text=True)
        if r.returncode: print('  #%d %s git apply rc %d %s' % (n, run, r.returncode, r.stderr.strip()[:120])); return None, files
    return {f: subprocess.run(['git', 'hash-object', os.path.join(W, f)], capture_output=True, text=True).stdout.strip() for f in files}, files
k = 0
for n, t, br, h, *_ in PRS:
    orders = list(itertools.permutations(CANON[n]))
    for order in orders:
        k += 1; W = os.path.join(X, 'p%d-order%d' % (n, k)); os.makedirs(W)
        got, files = apply_into(W, n, h, order)
        lab = ' then '.join(NAME[o] for o in order)
        if got is None: bad.append(('canonical apply', n, lab)); continue
        for f in files:
            want = rp(h + ':' + f)
            print('  #%d canonical [%s] %s -> %s == head %s: %s' % (n, lab, f.split('/')[-1], got[f][:12], want[:12], got[f] == want))
            if got[f] != want: bad.append(('canonical patch != PR', n, lab, f))
    print('  #%d: %d application order(s) checked' % (n, len(orders)))
# controls: every proper subset of #1099's three, in every order, differs from the head and equals the READY's item-0 prefix
for sub, pre in SUBSET.items():
    for order in itertools.permutations(sub):
        k += 1; W = os.path.join(X, 'subset-%d' % k); os.makedirs(W)
        got, files = apply_into(W, 1099, headof[1099], list(order))
        f = files[0]
        ok = got is not None and got[f] != rp(headof[1099] + ':' + f) and got[f].startswith(pre)
        print('  CONTROL #1099 [%s] -> %s: differs from the head and = the READY item-0 %s: %s' % (' then '.join(NAME[o] for o in order), (got or {}).get(f, 'NONE')[:12], pre, ok))
        if not ok: bad.append(('subset control', order))
for n, t, br, h, *_ in PRS:
    for run, name in CANON[n]:
        k += 1; W = os.path.join(X, 'control-reverse-%d-%d' % (n, k)); os.makedirs(W); seed(W, h)
        r = subprocess.run(['git', 'apply', '--reverse', '--check', sec(run, name)], cwd=W, capture_output=True, text=True)
        print('  CONTROL #%d %s --reverse onto develop blobs refuses: rc %d (want non-zero)' % (n, NAME[(run, name)], r.returncode))
        if r.returncode == 0: bad.append(('reverse control applied', n, run))
W = os.path.join(X, 'control-crossed'); os.makedirs(W); seed(W, headof[1098])
r = subprocess.run(['git', 'apply', '--check', sec(*N92_1)], cwd=W, capture_output=True, text=True)
print('  CONTROL crossed: #1097 N92-1 patch into #1098 develop blobs refuses: rc %d (want non-zero)' % r.returncode)
if r.returncode == 0: bad.append(('crossed control applied',))
print('scratch (plain files, not a repo; left in place):', X)

# 4. the all-three tree by pure tree hashing (read-only cat-file), controlled by each single head tree
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
bt = rp(BUILDER_PREDICT_COMMIT + '^{tree}')
print('ALL THREE over develop -> %s | builder predicted %s: %s | builder octopus commit %s tree %s: %s' % (comb, COMBINED[:9], comb == COMBINED, BUILDER_PREDICT_COMMIT[:9], bt[:9], bt == COMBINED))
if comb != COMBINED or bt != COMBINED: bad.append(('combined tree', comb, bt))
GS = os.path.dirname(os.path.abspath(__file__))
rd = lambda nm: open(os.path.join(GS, nm)).read()
scr = rd('predict_all_three_scratch.out')
scr_ok = all(re.search(lab + r': 3 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None for lab in ('forward', 'reverse', 'tier1first')) \
         and 'PREDICTION OK' in scr and 'rc=0' in scr
idx = rd('predict_index_scratch.out')
idx_ok = ('ALL THREE by scratch-index composition: ' + COMBINED) in idx and 'PREDICTION OK' in idx and 'rc=0' in idx and idx.count(': True') == 4
stp = rd('step_trees_scratch.out')
stp_ok = 'STEPS OK' in stp and 'rc=0' in stp and ('after #1099: merged tree ' + COMBINED) in stp and 'after #1098: merged tree 752b889c63135a2c871d9ab08409e361d51213e5' in stp
mes = rd('measure_scratch.out')
mes_ok = 'ALL OK' in mes and 'rc=0' in mes and mes.count(': True |') == 17 and 'whole-line x13 at [222, 239, 284, 301, 320, 339, 362, 767, 782, 792, 806, 832, 859]' in mes
print('scratch-clone prediction (forward + reverse + tier1first merge-tree chains) names', COMBINED[:9], 'three times and PREDICTION OK:', scr_ok)
print('scratch-index composition names', COMBINED[:9], 'with three controls and PREDICTION OK:', idx_ok)
print('step trees in the suggested order #1097 -> #1098 -> #1099 end at', COMBINED[:9], ':', stp_ok)
print('measure_scratch: every subset / order, canonical identity, controls, 17 tamper plants = the checker, 13 guard lines:', mes_ok)
if not (scr_ok and idx_ok and stp_ok and mes_ok): bad.append(('scratch prediction', scr_ok, idx_ok, stp_ok, mes_ok))
ghr = rd('gh_pr_reads.out')
gh_ok = 'ZERO PRODUCT BYTES in all three (files API): True' in ghr and ghr.count('files outside src/__tests__/ (files API): 0 [] | deletions total 0') == 3 \
        and 'TIER 1 #1099: one file, zero product bytes (files API): True' in ghr and 'rc=0' in ghr and ghr.count('O-1 detector hits title/body/commit 0/0/0') == 3 \
        and 'Refs lines as wanted (#1097 KS-1230; #1098 none; #1099 KS-1238 + KS-1282): True' in ghr and ghr.count('ks1215/ks-1215 in branch/title/commit-subject []') == 3 \
        and "'require_extra_approval_for_unattributed_changes': True" in ghr and "'required_approving_review_count': 0" in ghr
print('PR files API (gh_pr_reads.out): zero product bytes x3, #1099 by name, Refs as wanted, O-1 detector 0 x3, no ks1215 in branch/title/subject, ruleset as read:', gh_ok)
lin = rd('linear_reads.out')
lin_ok = "attachmentsForURL pull/1097 -> [('KS-1230', 'contributes')]" in lin and 'attachmentsForURL pull/1098 -> []' in lin \
         and re.search(r"attachmentsForURL pull/1099 -> \[\('KS-12(38|82)', 'contributes'\), \('KS-12(38|82)', 'contributes'\)\]", lin) is not None \
         and 'KS-1238' in re.search(r'attachmentsForURL pull/1099 -> (.*)', lin).group(1) and 'KS-1282' in re.search(r'attachmentsForURL pull/1099 -> (.*)', lin).group(1) \
         and "archivedAt 2026-09-13T05:35:48.754Z" in lin and "attachments [('932', 'closes')]" in lin and "KS-1215 |" in lin and "[('1034', 'contributes')]" in lin \
         and '77f4ec90-d30c-4185-a8f6-815b2924d57e' in lin and 'rc=0' in lin
print('Linear (linear_reads.out): attachmentsForURL exactly {KS-1230} / {} / {KS-1238, KS-1282}, KS-1062 archived with #932 only, KS-1215 #1034, comment 77f4ec90 read:', lin_ok)
if not (gh_ok and lin_ok): bad.append(('files API / Linear reads', gh_ok, lin_ok))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md'
PROMPT = WEDB + 'briefs/2026-09-20_secuura-batch1097-1099.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1097-1099-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1092-1096-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1084-1091-tier1-r1/'
F1SRC = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1097-#1099 (three PRs; tier 1 = #1099 KS-1238 + KS-1282)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-8th/'
assert os.path.isdir(PRIOR) and os.path.isdir(EARLIER) and os.path.isdir(F1SRC) and os.path.isdir(SEATHIST), 'prior / earlier / F-1 report or seat history dir missing'
assert os.path.isfile(PRIOR + 'report.md'), 'PRIOR REPORT has no report.md'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head in full'
assert 'MESSAGE_ID: <010001a0baf65c8a-af774173-f73c-4a9f-a7fe-bde133faa3ec-000000@email.amazonses.com>' in mt_ and 'TS: 2026-09-19T18:38:22' in mt_, 'mail capture is not the 18:38:22Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED in mt_ and COMBINED in pt_ and BUILDER_PREDICT_COMMIT in pt_ and BUILDER_PREDICT_COMMIT[:9] in mt_, 'combined tree / octopus commit not named in mail AND prompt'
assert DEV in mt_ and DEV in pt_, 'develop pin not named in mail AND prompt'
assert F1SRC in pt_, 'prompt does not name the F-1 source report'
for n in LABEL:
    line = [l for l in mt_.splitlines() if l.startswith('| #%d | ' % n)]
    assert ('PR #%d is %s.' % (n, LABEL[n])) in pt_ and len(line) == 1 and all(k_ in line[0] for k_ in KEYS[n]), ('namespace trap not named for', n, LABEL[n])
assert not re.search(r"waits for Kam.s tap|on Kam.s tap only|signed GO alone", pt_ + mt_, re.I), 'a Kam-tap / not-alone condition in the prompt or READY'
assert not re.search(r'\b12 (requireSuperAdmin )?guards|\btwelve (requireSuperAdmin )?guards|other twelve', pt_, re.I), 'the prompt repeats a count of twelve guards (the GO says 11)'

HEADER_OLD = cut('# launch_qa_secuura_batch1092_1096.sh', '# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1097_1099.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over THREE file-disjoint Secuura/Blockchain PRs
#   #1097 KS-1230 @ f53642179  ks1230 vitest test: N92-1, a null allow-list FIRST of two (mixed) and FIRST of four, stored as null (admin.ts:1132) — TIER 2 (test-only)
#   #1098 KS-1062 @ efce14bed  ks1062 vitest test: N93-1, one tenant skipped counted; every tenant failed = INCOMPLETE (archived ticket, NO Refs, NO key) — TIER 2
#   #1099 KS-1238 + KS-1282 @ b68aaf9b4  ks1215 vitest test: N95-1 (the admin-shadow 401, admin.ts :1366 / :1428) + N96-1a + N96-1b (eleven
#         requireSuperAdmin guards, platform.ts) — TIER 1 (AUTH, test-only)
# ALL THREE ARE TEST-ONLY: every changed path is under api-gateway src/__tests__/ (generator: local objects AND the PR files API; 0 product bytes,
# 0 deleted lines; #1099 asserted by name).
# #1099's verdict carries the ruling KS-1238 COMPLETE or NOT-COMPLETE, by name, against the ticket's own ask, its F-1 source and the prior gate's
# comment 77f4ec90; a COMPLETE ruling moves KS-1238 to Done + archived after the last merge (the seat's D11). KS-1282's completeness is Kam's call.
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too (KS-1097..KS-1099 exist) and #1099 carries two tickets; the READY mail AND the prompt
# must BOTH state which ticket(s) each of the three PRs is, or the launch refuses (exit 32).
# Batched under Kam's 09:22 rule. THREE verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 04:41:46 AEST 2026-09-20 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop c87458bdd; compare develop...head = merge_base c87458bdd, ahead 1, files 1 each (asserted per PR, exit 10).
# Pairwise file-disjoint (3 files, all modified, 0 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL THREE = tree 706de8305,
# re-derived by the generator by pure tree hashing (no git write) AND by the drafter in --shared scratch clones (merge-tree chains in THREE orders:
# forward, reverse, tier-1-first; and a scratch-index composition), equal to the builder's prediction and to its local octopus commit f893a92cf's
# tree. All three are byte-identical to their CANONICAL local-model patch.diff, re-applied strict by the generator in a plain scratch dir (#1099 =
# three runs in ALL SIX orders; every proper subset in every order = the READY's item-0 blob), each reverse-applied control refusing.
#
# The develop pin is judged by CONTENT — TWENTY-ONE paths by blob at the CURRENT develop: the 3 PR files (all at develop blobs; any PR's head blob
# -> exit 19 LANDED, naming the PR), and what the gate runs or reads: platform.ts (the 13 requireSuperAdmin guards, SUPER_ROLES, the pg.Pool
# routes), admin.ts (:1132, :1366, :1428), startup-migrations.ts, proxy.ts (:472 / :504), verification.ts, auth.ts, index.ts (the mount order),
# preflight.sh, run-shell-suites.sh, the pre-push hook, the api-gateway configs incl. vitest.setup.ts, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md, the seat's READY mail (18:38:22Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the three heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all three heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and THREE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1092-#1096 batch), the EARLIER REPORT (the #1084-#1091 batch), the
#          KS-1238 F-1 source report and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state' and
#          'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-20_seatB-8th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (ruleset 18499832, the order-independence blobs, the 17 plant sha256s, the
#          tamper ids, the develop sha256s, the census words), and the prompt must ask the gate to MEASURE, not conclude, and to rule KS-1238
#          COMPLETE or NOT-COMPLETE.
# exit 31: the prompt must name the all-three tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the three, which ticket(s) the PR is (PR #1097 is KS-1230 ... PR #1099 is
#          KS-1238 + KS-1282).
# exit 33: the prompt must carry Wednesday's ELEVEN BY-NAME items: tier + round 1 of 2 + ZERO product bytes on #1099; ALL SIX orders; the WHOLE
#          api-gateway suite combined runs + the SHARED-LINE TAMPER PAIR; KS-1238 COMPLETE or NOT-COMPLETE BY NAME with comment 77f4ec90, its
#          one-cell-per-path sentence and the FACTS-COMMENT TEXT; the eleven guard lines + KS-1282 completeness as Kam's call; NOTHING ABOUT O-1 +
#          no /unrevoke pin; the real Postgres on 127.0.0.1:5432; attachmentsForURL + includeArchived; the NOT-PINNED row format; the MERGE ADDENDUM.
# QAB1097_CUR_DEV (test override, --check only): stands in for origin develop. QAB1097_HEAD_1099 (test override): stands in for #1099's pinned head.
# QAB1097_PLATFORMTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/platform.ts (its git blob).
# A launch with any QAB1097_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-20_gate1097to1099/gen_launcher_batch1097_1099.py from launch_qa_secuura_batch1092_1096.sh (asserted block
# substitutions + pins re-read + canonical-patch identity in every order + all-three tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1097_1099.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != OVERRIDE else '${QAB1097_HEAD_1099:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1092_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1092to1096/mail_batch1092_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1097_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1097_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (18:38:22Z) and re-read by the drafter (git ls-remote 04:41:46 AEST, branch AND refs/pull/N/head)\n'
            '# NAMESPACE TRAP: no PR here is its own-numbered ticket; #1098 is archived KS-1062 (no Refs); #1099 carries KS-1238 AND KS-1282; the ticket column is the truth (exit 32)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 04:41:46 AEST; every head's merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            "EARLIER_REPORT='" + EARLIER + "'\n"
            "F1_REPORT='" + F1SRC + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADSC_OLD = '# The five heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.\n'
HEADSC_NEW = '# The three heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.\n'
CMPC_OLD = cut('# develop...head = 4273adfac ahead 1 for all five PRs; files 1 each\n', '(git diff --name-only + rev-list, drafter 01:1x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = c87458bdd ahead 1 for all three PRs; files 1 each\n'
            '# (git diff --name-only + rev-list, drafter 04:4x AEST; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1092 $MERGE_BASE', '1096 $MERGE_BASE ahead=1 files=1"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): twenty-six paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): twenty-one paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN)
assert len(JPATHS) == 21, ('judged path count', len(JPATHS))
PLATP = A + 'src/routes/platform.ts'
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p]
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k_ = 'PLATFORMTS' if p == PLATP else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k_, ' ' * max(1, 80 - len(k_)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\n'
              'PLATFORMTS = A + "src/routes/platform.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all three heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr[:9]) for n, _, _, _, _, _, tr in PRS) + '; all three together ' + COMBINED + ', drafter tree-hash, three-order scratch-clone merges and scratch-index composition = builder prediction; git ls-remote)"); sys.exit(0)\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = ('GUARDED = [A + "src/",\n'
             '           A + "package.json",\n'
             '           A + "vitest.config.ts",\n'
             '           A + "vitest.setup.ts",\n'
             '           A + "tsconfig.json",\n'
             '           D + "packages/shared/src/",\n'
             '           D + "scripts/",\n'
             '           ".githooks/",\n'
             '           D + "package.json",\n'
             '           D + "package-lock.json",\n'
             '           D + "eslint.config.mjs",\n'
             '           "BACKLOG.md"]\n'
             '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a\n'
             '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.\n'
             '# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.\n'
             'DEV_CONTENT_ALLOWED = {}\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the five heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the three heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all three '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway src/ + config, packages/shared src/, scripts/, .githooks/, '
               'the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, LABEL[n], 1 if n in TIER1 else 2) for n in LABEL]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
SEATWORDS = ['PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state', 'zero product bytes']
GWORDS = ['18499832', 'fe235c8aa1d85d28d73a4853890c840bd59e0a7a', 'f9bff1b332af', '63d5c6876d82', '7c56fdbdcfde', '86d7faeae0e3', 'f47c8eadf237', '6292bafe5906',
          '6ca6003490e2', '7cbea3850ecc', 'caa3971a4e3a', 'c423a8f77ccc', '41234d5f1db7', '1a8800d9728e',
          'dec8abd6c60f', 'e091c63c14b6', '465234ebec8f', 'b31f6c613735', 'f1c507f33c70', 'b040c368c317', '75cd534254e4', 'b9010e9ee952', '4d76f733a198',
          'ad7aa5682a33', '8d871fb0274e', 'FIRSTOF2NULLMIXED', 'FIRSTOF4NULL', 'ONESKIPPED', 'ALLFAILED', 'ADMINSHADOW1366', 'ADMINSHADOW1428',
          '7d04a92ca724', '6a733afc58fd', '623a99b9531e', 'STOP-class 0', '76 runs', '127.0.0.1:1', ':5432', '667', '671']
for w in SEATWORDS + GWORDS: assert w in pt_ and w in mt_, ('READY mail and prompt must both carry', w)
BYNAME = ['round 1 of 2', 'ZERO product bytes on #1099', 'ALL SIX orders', 'WHOLE api-gateway suite', 'SHARED-LINE TAMPER PAIR',
          'KS-1238 COMPLETE or NOT-COMPLETE, BY NAME', '77f4ec90', 'One cell per path pinning that a connector key alone gets 401 there closes it',
          'FACTS-COMMENT TEXT', ':284 :301 :320 :339 :362 :767 :782 :792 :806 :832 :859', 'completeness is Kam', 'NOTHING ABOUT O-1',
          'must not recommend pinning either', 'a real Postgres listens on 127.0.0.1:5432', 'attachmentsForURL', 'includeArchived',
          'SAME ROW FORMAT as the PRIOR REPORT', 'ONE MERGE ADDENDUM line PER PR']
for w in BYNAME: assert "'" not in w, ('an apostrophe would break the single-quoted grep', w)
for w in BYNAME: assert w in pt_, ('prompt lacks the by-name item', w)
assert 'MEASURE, not conclude' in pt_ and 'COMPLETE or NOT-COMPLETE' in pt_ and 'three lines, one per pr' in pt_.lower() and 'proposed cell' in pt_ \
       and 'GATEWAY_URL=http://127.0.0.1:' in pt_, 'prompt phrasing'
TRAPGREP = ' && '.join("grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\" && " % (n, LABEL[n])
                       + ' && '.join("grep -F '| #%d | ' \"$BRIEF\" | grep -qF '%s'" % (n, k_) for k_ in KEYS[n]) for n in LABEL)
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", 'exit 33; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1099 T1, #1097 + #1098 T2)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat's READY mail capture path" >&2; exit 9; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'THREE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and THREE verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$F1_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the F-1 source $F1_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
''' + ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -qF '%s' \"$BRIEF\"" % (w, w) for w in SEATWORDS) + r''' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-20_seatB-8th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
''' + ''.join('grep -qF -- \'%s\' "$PROMPT_FILE" && grep -qF -- \'%s\' "$BRIEF" && ' % (w, w) for w in GWORDS) + r'''grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items, or the prompt does not say MEASURE, not conclude and rule KS-1238 COMPLETE or NOT-COMPLETE" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF '__PREDICT__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-three tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
''' + TRAPGREP + r''' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket(s) each PR is (PR #1097 is KS-1230, PR #1098 is KS-1062, PR #1099 is KS-1238 + KS-1282) — the PR numbers are other tickets' numbers too" >&2; exit 32; }
''' + ' && '.join('grep -qF -- \'%s\' "$PROMPT_FILE"' % w for w in BYNAME) + r''' \
  || { echo "REFUSING: the prompt does not carry Wednesday's eleven by-name items (tier + round 1 of 2 + zero product bytes on #1099, all six orders, whole-suite combined runs + the shared-line pair, KS-1238 by name with 77f4ec90 + its one-cell-per-path sentence + facts text, the eleven guards + KS-1282 as Kam's call, nothing about O-1 + no /unrevoke pin, the real Postgres on :5432, attachmentsForURL + includeArchived, the NOT-PINNED row format, the merge addendum)" >&2; exit 33; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED).replace('__PREDICT__', BUILDER_PREDICT_COMMIT)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  three heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1099 T1, #1097 + #1098 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all three heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, THREE verdict lines"
  echo "  prompt names the report directory, the #1092-#1096 batch PRIOR REPORT, the EARLIER REPORT, the F-1 source and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-20_seatB-8th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items; the prompt says MEASURE, not conclude, and rules KS-1238 COMPLETE or NOT-COMPLETE"
  echo "  prompt names the all-three tree, the octopus commit, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket(s) each of the three PRs is (namespace trap; #1098 archived KS-1062, #1099 KS-1238 + KS-1282)"
  echo "  prompt carries Wednesday's eleven by-name items: tier/round/zero bytes, six orders, whole-suite runs + shared-line pair, KS-1238 by name (77f4ec90), eleven guards + Kam's call, nothing about O-1, Postgres :5432 isolation, link hygiene, NOT-PINNED, addendum"
  [ -n "${QAB1097_CUR_DEV:-}" ] && echo "  (develop read from the QAB1097_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1097_PLATFORMTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/platform.ts read from the QAB1097_PLATFORMTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('heads comment', HEADSC_OLD, HEADSC_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1092_CUR_DEV:-', 'CUR_DEV="${QAB1097_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1092_VERIFTS_FILE", "") if f == VERIFTS else ""\n',
                 '    fixture = os.environ.get("QAB1097_PLATFORMTS_FILE", "") if f == PLATFORMTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1092_BRIEF:-}${QAB1092_PROMPT:-}${QAB1092_HEAD_1096:-}${QAB1092_CUR_DEV:-}${QAB1092_VERIFTS_FILE:-}" ]',
            '[ -z "${QAB1097_BRIEF:-}${QAB1097_PROMPT:-}${QAB1097_HEAD_1099:-}${QAB1097_CUR_DEV:-}${QAB1097_PLATFORMTS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1092-1096 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1092-#1096 batch': 2, 'from launch_qa_secuura_batch1092_1096.sh': 1}   # exit 24 comment + --check line; the template
for k_, v in INTENDED.items():
    assert BODY.count(k_) == v, ('intended citation count', k_, BODY.count(k_), v)
    BODY = BODY.replace(k_, '<CITED>')
RESID = ['QAB1092_', 'mail_batch1092', 'gate1092to1096', 'batch1092', '4273adfac', '458cff717', '4a1fa96a5', 'seatB-7th', 'five', 'FIVE',
         'twenty-six', 'TWENTY-SIX', 'VERIFTS', 'RAW598', 'RAW1297', 'REFRESHNOAUTH', 'TENANTSGETUNGUARDED', '60c1e1f7', 'originate', 'O + ',
         'jest', 'ks739', '01:17:23', '01:1x', 'PR #1092 is', 'twelve', '12 guards']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])(109[2-6])(?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 2,   # OKPIN + the exit-31 guard
       REPORT_DIR: 1, PRIOR: 1, EARLIER: 1, F1SRC: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT"': None, 'QAB1097_CUR_DEV': None, 'QAB1097_PLATFORMTS_FILE': None,
       'QAB1097_HEAD_1099': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 32': None, 'exit 33': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-20_secuura-batch1097-1099.prompt.txt': 1, 'gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md': None,
       '"BACKLOG.md"]': 1, 'A + "src/",': 1, 'D + "packages/shared/src/",': 1, 'D + "scripts/",': 1, '".githooks/",': 1,
       'ahead=1 files=': 3, 'PLATFORMTS': None, BUILDER_PREDICT_COMMIT: 1}
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
for p, b in DEVPIN.items():
    if s.count(b) != 1: print('CONTROL DISAGREED develop pin', p, s.count(b)); sys.exit(1)
for p, (b, n) in LANDED.items():   # #1099's head blob is ALSO a seat item in the exit-30 guard (prompt + READY): 1 + 2
    if s.count(b) != 1 + (2 if b in GWORDS else 0): print('CONTROL DISAGREED landed pin', n, p, s.count(b)); sys.exit(1)
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
