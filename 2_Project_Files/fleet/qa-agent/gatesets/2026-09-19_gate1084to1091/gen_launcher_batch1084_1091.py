#!/usr/bin/env python3
"""gen_launcher_batch1084_1091.py — derive launchers/launch_qa_secuura_batch1084_1091.sh from launchers/launch_qa_secuura_batch1077_1083.sh (the
batch gate prepared 2026-09-19 17:5x, one gate / seven verdicts, which ran cleanly) by ASSERTED block substitutions: every anchor must occur exactly
as often as stated, or the generator refuses and writes nothing. Structure copied from gatesets/2026-09-19_gate1077to1083/gen_launcher_batch1077_1083.py;
the data changed, plus one guard (exit 33).

ONE BATCHED gate, TIER 1 floor (set by #1090 + #1091, both KS-1238, auth, test-only), EIGHT PRs #1084..#1091 (Seat B 6th, READY 2026-09-19 11:53:21Z).
ALL EIGHT ARE TEST-ONLY: every changed path sits under a src/__tests__/ directory (asserted from local objects here; the launcher's prompt asks the
gate to prove it from the PR files API too — gh_pr_reads.out beside this file already did, and asserts #1090 / #1091 by name).
NAMESPACE TRAP: the PR numbers are also other tickets' numbers; PR #1084 is KS-1269 ... PR #1090 AND PR #1091 are KS-1238. The launcher refuses
(exit 32) unless the prompt AND the READY both state which ticket each of the eight PRs is.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (git rev-parse / cat-file / diff --name-only / rev-list): each PR is ONE commit whose parent IS develop; every PR's file set and
    head tree as pinned; every judged develop blob and every landed head blob as pinned; the eight pairwise file-disjoint (8 files, 0 new);
    zero product bytes in every PR; the commits carry Refs <own ticket> (six) or NO KS key at all (#1088, #1089); no commit carries ks1215 / ks-1215;
  * the two N71 items' blobs equal at f9c28a8b8 and ba1210afc (the seat's item 6);
  * CANONICAL-PATCH identity for ALL EIGHT (nine local-model patch.diff, strict; #1084 is two runs, applied in BOTH orders): develop's blobs are
    written as plain files into a fresh scratch dir (not a repo), `git apply` (patch mode, cwd = that dir) applies each run's patch.diff, and
    `git hash-object` (no -w) of each result must equal the head blob; controls: #1084 with EITHER run alone must differ; every patch applied
    --reverse onto develop's blobs must refuse; a crossed patch (#1089's into #1084's develop blobs) must refuse;
  * the ALL-EIGHT TREE is re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, CONTROLLED by re-deriving each of the
    eight head trees from develop the same way; it must equal the builder's f76901ed9 and the tree of its local octopus commit 1f11437af. (The
    drafter ALSO predicted it by merge-tree chains in THREE orders in a --shared scratch clone: predict_all_eight_scratch.sh / .out beside this file.)
Usage: gen_launcher_batch1084_1091.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1084_1091', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = 'ba1210afcab7ddf127cccb270b1c341360261cee'   # develop at 11:55:59Z (#1077-#1083 merged); every PR's merge-base
PREV = 'f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf'  # the tip the two N71 runs were written at
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; V = D + 'services/vc-issuer/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e756a2de-6a98-48d1-a280-ca95596a3651/scratchpad'
# n, ticket, branch, head, ahead, file count, head tree
PRS = [
 (1084, 'KS-1269', 'feature/ks-1269-post-apistatusidrevoke-accepts-index-object-where-integer-is-n71', '946cdfd7801e0994d7f5e8847397aaf1c0d13677', 1, 1, 'e9fc521fbfb72dab46b751ee215e76268efffab7'),
 (1085, 'KS-1258', 'feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n77-1', 'c3d9ca2e2ccd6402eeb8456a1b577b0609df019b', 1, 1, 'b904e7243737d1b13381b215a310f104a30acc38'),
 (1086, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n80-1', 'b0bcf733f316083fe661facab6a11d024600c497', 1, 1, '8f3df5a6417bf4108f3eaa7012456fd6829dc605'),
 (1087, 'KS-1206', 'feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an-n81-1', 'd4658c0211a214f476bcf79470957e0f50317275', 1, 1, '6c3dfead8367bb70466990367a3b16f0eb6c1325'),
 (1088, 'KS-1062', 'feature/pin-startup-migrations-skipped-tenants-counted-loop-continues', '734a8f0bd1b1cd420c09ee35a2e736b2a6fb832e', 1, 1, '56a40abab5b7ea84abe8f670874b67949be64902'),
 (1089, 'KS-739', 'feature/pin-transfer-custody-nonjson-400-503-lookup', 'a64390edf791e5c52a841cdb63397a33893af2f9', 1, 1, 'bab87a37e86d34746462c25ef4f7cc2ee35748ba'),
 (1090, 'KS-1238', 'feature/ks-1238-n83-3-pin-anchor-store-forward-sends-no-caller-bearer', 'bd45f3b4f02789a55f9d6f81d061ae4dd21f02d0', 1, 1, '95ecc81a825d5b4d0e75e298874918a5e66666ce'),
 (1091, 'KS-1238', 'feature/ks-1238-n83-5-pin-platform-tenants-refuses-a-connector-key', 'dad4786c8e3e0616cc8785c901997b4fbe1f7287', 1, 1, '4a4802bb7431314f2b1998db2162fcefc9a4f6b2'),
]
ARCHIVED = {1088, 1089}                                  # KS-1062 and KS-739: Done + archived; NO Refs, NO KS key in the commit
TIER1 = {1090, 1091}
OVERRIDE = 1091                                          # the head the launcher's test override stands in for (pushed LAST)
COMBINED = 'f76901ed9cfae15ce6580ff24ebcbbea22bd36fb'   # builder's predicted all-eight tree (READY 11:53:21Z); re-derived below
BUILDER_PREDICT_COMMIT = '1f11437afc21cad6a77fbf75030444fd845e17c4'   # builder's local-only octopus commit (9 parents); its tree must be COMBINED
def sec(run, name): return RUNS + run + '/out.md.checker/' + name
def opts_of(run, name):
    ck = RUNS + run + '/out.md.checker/'
    for cand in (ck + name + '.opts', ck + name[:-5] + '.opts'):
        if os.path.exists(cand):
            words = open(cand).read().split()
            named = [w for w in words if w.endswith('.diff')]
            assert named in ([], [ck + name]), ('opts names another diff', cand, named)
            return [w for w in words if w.startswith('--')]
    return None
CANON = {
 1084: [('2026-09-19_ks1269-ornith35b-night3', 'patch.diff'), ('2026-09-19_ks1269-ornith35b-night4', 'patch.diff')],   # N71-1, N71-2
 1085: [('2026-09-19_ks1258-ornith35b-night4', 'patch.diff')],
 1086: [('2026-09-19_ks1230-ornith35b-night4', 'patch.diff')],
 1087: [('2026-09-19_ks1206-ornith35b-night4', 'patch.diff')],
 1088: [('2026-09-19_ks1062-ornith35b-night3', 'patch.diff')],
 1089: [('2026-09-19_ks739-ornith35b-night6', 'patch.diff')],
 1090: [('2026-09-19_ks1238-ornith35b-night4', 'patch.diff')],
 1091: [('2026-09-19_ks1238-ornith35b-night5', 'patch.diff')],
}
# every section applies strict (no opts file in any of the nine checker dirs — asserted below); the READY: "Deviations from verbatim: none"

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 V + 'src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts': 'bb8801cfb463758b3765ad015382906e4191d627',
 A + 'src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts': '57b5fdc453bf1feb6a6af6c5a11dba2d477d08c5',
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': '069ad80eb125b52d94b475b9d8319c260016ef9f',
 O + 'src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts': '67edac0af3d9c491fcc5f0efc8e5eba225018005',
 A + 'src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts': 'c7046d12d2fa1229911e25cf8fdcb2f8a1d53773',
 O + 'src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts': '42e4af4860a54d0d87a5d2ec3f743606dc0c4b73',
 A + 'src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts': 'e3384324c6051ef70d6a16e3c15e08038f53a9d5',
 A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': '7d14580b0a2c0f7967e578345e13f534d0919987',
 A + 'src/routes/verification.ts': 'f888e8cd0bd10c98a508542d75902ab122595157',
 A + 'src/routes/platform.ts': 'b80a8cd8d4e1af5a944817227f5ee6612c793954',
 A + 'src/routes/system-status.ts': 'e911ce1fdaa4b755e9b7b6428f899cdbd63889cb',
 A + 'src/startup-migrations.ts': 'ed3e521426e75910c5bf2cf07e7251f2fd8ef538',
 A + 'src/routes/admin.ts': '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 A + 'src/routes/proxy.ts': '795ae7ca3bdc76be3e563e87fc34a8cc221e5632',
 A + 'src/middleware/auth.ts': 'bf09d315a64443b7f02bc27a74366b7a7f1dae81',
 A + 'src/index.ts': 'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 V + 'src/routes/status.ts': '394337283ec19e77a10d1b25b8c5cc2b978fb52e',
 O + 'src/routes/adminConfig.ts': '62af28d017069d38fa00e7915bfa65226db678c6',
 O + 'src/routes/documents.ts': '3f837fc6e656d5a10f9cc349b1cb2a876a2be09b',
 D + 'scripts/preflight/preflight.sh': '712f895362e2c8d1ead6fd09ac257d7bce212948',
 D + 'scripts/run-shell-suites.sh': 'bf766bb54828cf6abad817f0f21a0c2f674d783f',
 '.githooks/pre-push': '1b22d4e146487aa25698310b353152a7d09986b5',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 O + 'package.json': 'd4435238d3ece7f7da42f043f56ca7739a611132',
 O + 'jest.config.js': '735183662feea56d39f664eb6379cae1a2eec957',
 O + 'tsconfig.json': 'd1b46ece71ad5b2559ccad3648c23a5231e43b09',
 V + 'package.json': '27888b6eeb6c20b44af947d14eddb3bccf6293cf',
 V + 'package-lock.json': 'b0b66b5018e556731056875d4c1720945e3478e7',
 V + 'vitest.config.ts': 'ddacccfb518d23d24ecfb5ddcf60e8373166d8b5',
 V + 'tsconfig.json': 'b3546b85f68847a2cd62ad74f10f5f7347579bc5',
 D + 'package.json': '773443a9faa0a2eb7caf01c313b880fbe3251922',
 D + 'package-lock.json': '646c19f6f7f735ba32bfb20bef8b936835184949',
 D + 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
 'BACKLOG.md': '59a1928dc56d9921dbdf2e8d36667e2df6af4024',
}
bad = []
headof = {n: h for n, _, _, h, *_ in PRS}
# LANDED: every PR file -> (its head blob, PR); read from the repo, then shape-checked below
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
if len(LANDED) != 8 or NEWFILES: bad.append(('want 8 landed paths, 0 new', len(LANDED), NEWFILES))
# the seat's item 6: the two N71 items' blobs are equal at the tip the runs were written at and at the pin
for p in (V + 'src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts', V + 'src/routes/status.ts'):
    eq = rp(PREV + ':' + p) == rp(DEV + ':' + p) == DEVPIN[p]
    print('  N71 blob %s at f9c28a8b8 == at ba1210afc == pin %s: %s' % (p.split('/')[-1], DEVPIN[p][:12], eq))
    if not eq: bad.append(('N71 blob moved between the tips', p))

# 1. origin, read-only (git ls-remote): develop, every refs/pull/N/head and every branch
t0 = now()
refs = ['refs/heads/develop'] + [x for n, _, br, *_ in PRS for x in ('refs/pull/%d/head' % n, 'refs/heads/' + br)]
lsr = dict(reversed(l.split('\t')) for l in git('ls-remote', 'origin', *refs).stdout.strip().splitlines())
print('ls-remote', t0, '->', now(), '|', len(lsr), 'refs read')
if lsr.get('refs/heads/develop') != DEV: bad.append(('origin develop moved', lsr.get('refs/heads/develop')))
for n, t, br, h, *_ in PRS:
    a, b = lsr.get('refs/pull/%d/head' % n), lsr.get('refs/heads/' + br)
    print('  #%d %-8s pull/head %s branch %s  %s' % (n, t, (a or 'NONE')[:9], (b or 'NONE')[:9], 'OK' if a == b == h else 'MOVED'))
    if not (a == b == h): bad.append(('head moved', n, a, b))

# 2. PR shape against local objects
allfiles = []
for n, t, br, h, ahead, nf, tree in PRS:
    files = sorted(git('diff', '--name-only', DEV, h).stdout.splitlines()); allfiles += files
    chain = git('rev-list', '--first-parent', DEV + '..' + h).stdout.split()
    npars = [len(git('rev-list', '--parents', '-n', '1', c).stdout.split()) - 1 for c in chain]
    base_ok = git('merge-base', DEV, h).stdout.strip() == DEV and rp(chain[-1] + '^1') == DEV if chain else False
    ok = len(chain) == ahead and all(x == 1 for x in npars) and base_ok and len(files) == nf and rp(h + '^{tree}') == tree
    print('#%d %-8s head %s ahead %d parents %s base=develop %s files %d tree %s  %s' % (n, t, h[:9], len(chain), npars, base_ok, len(files), rp(h + '^{tree}')[:9], 'OK' if ok else 'BAD'))
    if not ok: bad.append(('PR shape', n, files, chain))
    # zero product bytes: every PR changes files under a src/__tests__/ directory ONLY
    prod = [f for f in files if '/src/__tests__/' not in f]
    print('    files outside src/__tests__/: %d %s (want 0)%s' % (len(prod), [f.split('/')[-1] for f in prod], ' — TIER 1' if n in TIER1 else ''))
    if prod: bad.append(('product bytes', n, prod))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 8: bad.append(('eight PRs not pairwise file-disjoint / not 8 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
# namespace trap, asserted from the commits: no commit names its own PR number as a ticket; each live PR carries Refs <its ticket>;
# the two archived-ticket PRs carry NO KS key at all in the commit (the seat's message lint); no commit carries ks1215 / ks-1215 (any case)
subj = {n: git('log', '-1', '--format=%s%n%b', h).stdout for n, _, _, h, *_ in PRS}
trap = all('KS-%d' % n not in subj[n] for n, *_ in PRS) \
       and all(re.search(r'^Refs ' + t + r'\b', subj[n], re.M) for n, t, *_ in PRS if n not in ARCHIVED) \
       and all(not re.search(r'KS-\d+', subj[n]) for n in ARCHIVED) \
       and all(not re.search(r'ks-?1215', subj[n], re.I) for n, *_ in PRS)
print('namespace trap (no commit names KS-<its own PR number>; six carry Refs <own ticket>; #1088 and #1089 carry NO KS key; no ks1215 / ks-1215):', trap)
if not trap: bad.append(('namespace trap / Refs', {n: subj[n][:60] for n in subj}))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1084-', dir=SCRATCH)
def seed(W, target):
    files = git('diff', '--name-only', DEV, target).stdout.splitlines()
    for f in files:
        os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
        open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    return files
def apply_into(W, n, target, sections=None, extra=()):
    files = seed(W, target)
    for run, name in (sections or CANON[n]):
        o = opts_of(run, name)
        if o is not None: bad.append(('an opts file exists; this batch is strict-only', n, run, o)); return None, files
        r = subprocess.run(['git', 'apply', *extra, sec(run, name)], cwd=W, capture_output=True, text=True)
        print('  #%d %s/%s git apply %s rc %d %s' % (n, run.split('_')[1], name, ' '.join(extra) or '(strict)', r.returncode, r.stderr.strip()[:120]))
        if r.returncode: return None, files
    return {f: subprocess.run(['git', 'hash-object', os.path.join(W, f)], capture_output=True, text=True).stdout.strip() for f in files}, files
for n, t, br, h, *_ in PRS:
    W = os.path.join(X, 'p%d' % n); os.makedirs(W)
    got, files = apply_into(W, n, h)
    if got is None: bad.append(('canonical apply', n)); continue
    for f in files:
        want = rp(h + ':' + f)
        print('  #%d canonical %s -> %s == head %s: %s' % (n, f.split('/')[-1], got[f][:9], want[:9], got[f] == want))
        if got[f] != want: bad.append(('canonical patch != PR', n, f))
# order independence: #1084's two runs in the REVERSE order (N71-2 then N71-1) must give the same head blob
W = os.path.join(X, 'order-1084-reversed'); os.makedirs(W)
got, files = apply_into(W, 1084, headof[1084], list(reversed(CANON[1084])))
ord_ok = got is not None and all(got[f] == rp(headof[1084] + ':' + f) for f in files)
print('  ORDER #1084 N71-2 THEN N71-1 -> equals the head blob: %s (want True)' % ord_ok)
if not ord_ok: bad.append(('#1084 reversed-order identity',))
# control: #1084 with EITHER run alone must NOT equal the head (both runs are load-bearing)
for i, lab in ((0, 'N71-1'), (1, 'N71-2')):
    W = os.path.join(X, 'control-1084-%s-alone' % lab); os.makedirs(W)
    got, files = apply_into(W, 1084, headof[1084], [CANON[1084][i]])
    diff_ok = got is not None and any(got[f] != rp(headof[1084] + ':' + f) for f in files)
    print('  CONTROL #1084 %s run ALONE -> differs from the head: %s (want True)' % (lab, diff_ok))
    if not diff_ok: bad.append(('#1084 one-run control', lab))
# control: every canonical patch applied --reverse onto develop's blobs must refuse (the patch is not already in develop)
for n, t, br, h, *_ in PRS:
    for run, name in CANON[n]:
        W = os.path.join(X, 'control-reverse-%d-%s' % (n, run.split('_')[1])); os.makedirs(W); seed(W, h)
        r = subprocess.run(['git', 'apply', '--reverse', '--check', sec(run, name)], cwd=W, capture_output=True, text=True)
        print('  CONTROL #%d %s --reverse onto develop blobs refuses: rc %d (want non-zero)' % (n, run.split('_')[1], r.returncode))
        if r.returncode == 0: bad.append(('reverse control applied', n, run))
# control: a canonical patch into the WRONG file set refuses — #1089's patch into #1084's develop blobs
W = os.path.join(X, 'control-crossed'); os.makedirs(W); seed(W, headof[1084])
r = subprocess.run(['git', 'apply', '--check', sec('2026-09-19_ks739-ornith35b-night6', 'patch.diff')], cwd=W, capture_output=True, text=True)
print('  CONTROL crossed: #1089 patch into #1084 develop blobs refuses: rc %d (want non-zero)' % r.returncode)
if r.returncode == 0: bad.append(('crossed control applied',))
print('scratch (plain files, not a repo; left in place):', X)

# 4. the all-eight tree by pure tree hashing (read-only cat-file), controlled by each single head tree
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
def compose(tree_oid, changes):  # changes: {path_parts tuple: (mode bytes, blob hex)}
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
print('ALL EIGHT over develop -> %s | builder predicted %s: %s | builder octopus commit %s tree %s: %s' % (comb, COMBINED[:9], comb == COMBINED, BUILDER_PREDICT_COMMIT[:9], bt[:9], bt == COMBINED))
if comb != COMBINED or bt != COMBINED: bad.append(('combined tree', comb, bt))
scr = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'predict_all_eight_scratch.out')).read()
scr_ok = all(re.search(lab + r': 8 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None for lab in ('forward', 'reverse', 'shuffled')) \
         and 'PREDICTION OK' in scr and 'rc=0' in scr
print('scratch-clone prediction (predict_all_eight_scratch.out, forward + reverse + shuffled merge-tree chains) names', COMBINED[:9], 'three times and PREDICTION OK:', scr_ok)
if not scr_ok: bad.append(('scratch prediction',))
ghr = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gh_pr_reads.out')).read()
gh_ok = 'ZERO PRODUCT BYTES in all eight (files API): True' in ghr and ghr.count('files outside __tests__/ (files API): 0 []') == 8 \
        and 'TIER 1 #1090 and #1091: one file each, zero product bytes (files API): True' in ghr and 'rc=0' in ghr
print('PR files API (gh_pr_reads.out): zero product bytes in all eight, and #1090 / #1091 by name:', gh_ok)
if not gh_ok: bad.append(('files API zero-product read',))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-19_gate1084to1091/mail_batch1084_ready.md'
PROMPT = WEDB + 'briefs/2026-09-19_secuura-batch1084-1091.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1084-1091-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1077-1083-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1070-1076-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1084-#1091 (eight PRs; tier 1 = #1090 + #1091 KS-1238)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-6th/'
assert os.path.isdir(PRIOR) and os.path.isdir(EARLIER) and os.path.isdir(SEATHIST), 'prior / earlier report or seat history dir missing'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head in full'
assert 'MESSAGE_ID: <010001a0b9838e9b-84e4303e-b752-479f-8ac7-423afbf7f515-000000@email.amazonses.com>' in mt_ and 'TS: 2026-09-19T11:53:21' in mt_, 'mail capture is not the 11:53:21Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED in mt_ and COMBINED in pt_ and BUILDER_PREDICT_COMMIT in pt_ and BUILDER_PREDICT_COMMIT in mt_, 'combined tree / octopus commit not named in mail AND prompt'
assert DEV in mt_ and DEV in pt_, 'develop pin not named in mail AND prompt'
for n, t, *_ in PRS:
    assert ('PR #%d is %s.' % (n, t)) in pt_ and ('| #%d | %s' % (n, t)) in mt_, ('namespace trap not named for', n, t)
assert not re.search(r"waits for Kam.s tap|on Kam.s tap only|signed GO alone", pt_ + mt_, re.I), 'a Kam-tap / not-alone condition in the prompt or READY'

HEADER_OLD = cut('# launch_qa_secuura_batch1077_1083.sh', '# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1084_1091.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over EIGHT file-disjoint Secuura/Blockchain PRs
#   #1084 KS-1269 @ 946cdfd78  vc-issuer ks1269 vitest test: N71-1 (index null refused, /revoke + /unrevoke) + N71-2 (/revoke guard order)  — TIER 2 (test-only)
#   #1085 KS-1258 @ c3d9ca2e2  ks1248 vitest test: N77-1, the :576 degraded REQUIRED advice is EXACTLY the comment + one curl (allow-list)  — TIER 2 (test-only)
#   #1086 KS-1230 @ b0bcf733f  ks1230 vitest test: N80-1, nulls at 2 and 3 of four, and null LAST of three, stored as null            — TIER 2 (test-only)
#   #1087 KS-1206 @ d4658c021  ks1206 jest test: N81-1, rateLimit Infinity / " 100" / -0 refused 400 before the INSERT                   — TIER 2 (test-only)
#   #1088 KS-1062 @ 734a8f0bd  ks1062 vitest test: N79-2, two skipped counted; skipped-first keeps the loop (archived, NO Refs, NO key)   — TIER 2 (test-only)
#   #1089 KS-739  @ a64390edf  ks739 jest test: N82-1, a non-JSON 400 / 503 lookup maps to 400 / 502 (archived ticket, NO Refs, NO key)  — TIER 2 (test-only)
#   #1090 KS-1238 @ bd45f3b4f  ks1238 vitest test: N83-3, the recorder also sees /api/anchors/ — pins verification.ts:521 (RAW521)      — TIER 1 (AUTH, test-only)
#   #1091 KS-1238 @ dad4786c8  ks1215 vitest test: N83-5, a connector key is refused 403 on POST /api/platform/tenants (platform.ts:239)  — TIER 1 (AUTH, test-only)
# ALL EIGHT ARE TEST-ONLY: every changed path is under a src/__tests__/ directory (generator: local objects AND the PR files API; 0 product bytes;
# ZERO product bytes in #1090 and #1091 asserted by name).
# #1090's and #1091's verdicts carry the same ruling, KS-1238 COMPLETE or NOT-COMPLETE; KS-1238 stays in Backlog regardless (this batch never moves
# it to Done) and the gate gives its corrected facts-comment text.
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too, and two PRs share KS-1238; the READY mail AND the prompt must BOTH state which ticket
# each of the eight PRs is, or the launch refuses (exit 32).
# Batched under Kam's 09:22 rule. EIGHT verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 21:55:59 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop ba1210afc; compare develop...head = merge_base ba1210afc, ahead 1, files 1 each (asserted per PR, exit 10).
# Pairwise file-disjoint (8 files, all modified, 0 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL EIGHT = tree f76901ed9,
# re-derived by the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains in THREE orders:
# forward, reverse, shuffled with the tier-1 heads first), equal to the builder's prediction and to its local octopus commit 1f11437af's tree. All
# eight are byte-identical to their CANONICAL local-model patch.diff, re-applied strict by the generator in a plain scratch dir (#1084 = two runs, in
# BOTH orders; each run alone differs), each reverse-applied control refusing.
#
# The develop pin is judged by CONTENT — THIRTY-SIX paths by blob at the CURRENT develop: the 8 PR files (all at develop blobs; any PR's head blob
# -> exit 19 LANDED, naming the PR), and what the gate runs or reads: verification.ts (RAW521 / :598 / :1297), platform.ts (:239 / :222 / :254),
# system-status.ts, startup-migrations.ts, admin.ts, proxy.ts, auth.ts, index.ts, vc-issuer status.ts, adminConfig.ts, documents.ts, preflight.sh,
# run-shell-suites.sh, the pre-push hook, the api-gateway / originate / vc-issuer configs, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway / originate / vc-issuer src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1084to1091/mail_batch1084_ready.md, the seat's READY mail (11:53:21Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the eight heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all eight heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and EIGHT verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1077-#1083 batch), the EARLIER REPORT (the #1070-#1076 batch) and
#          NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'The 3 skipped legs need a stack', 'login_stub',
#          'mergeable_state: unstable' and 'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-6th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (ruleset 18499832, the order-independence tree e9fc521fb, the six plant
#          sha256s of the line-pinned anchors, RAW521 and its sha 2c7f6a3dbdef, TENANTSORGPROV / TENANTSUNGUARDED, --listFilesOnly, the N71 blobs
#          bb8801cfb463 / 394337283ec1, db.retry.test.ts), and the prompt must ask the gate to MEASURE, not conclude, and to rule KS-1238
#          COMPLETE or NOT-COMPLETE.
# exit 31: the prompt must name the all-eight tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the eight, which ticket the PR is (PR #1084 is KS-1269 ... PR #1091 is KS-1238).
# exit 33: the prompt must carry Wednesday's BY-NAME items: KS-1238's comment 18580369, ZERO product bytes in #1090 and #1091, the NON-RULED
#          /unrevoke -1 rule (the gate must not recommend pinning -1 either way), the tsc --listFilesOnly finding, and the PRIOR REPORT's row format.
# QAB1084_CUR_DEV (test override, --check only): stands in for origin develop. QAB1084_HEAD_1091 (test override): stands in for #1091's pinned head.
# QAB1084_VERIFTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/verification.ts (its git blob).
# A launch with any QAB1084_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1084to1091/gen_launcher_batch1084_1091.py from launch_qa_secuura_batch1077_1083.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-eight tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1084_1091.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != OVERRIDE else '${QAB1084_HEAD_1091:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1077_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1077to1083/mail_batch1077_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1084_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1084_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (11:53:21Z) and re-read by the drafter (git ls-remote 21:55:59 AEST, branch AND refs/pull/N/head)\n'
            '# NAMESPACE TRAP: no PR here is its own-numbered ticket, and #1090 and #1091 share KS-1238; the ticket column is the truth (exit 32)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 21:55:59 AEST; every head's merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            "EARLIER_REPORT='" + EARLIER + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADSC_OLD = '# The seven heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.\n'
HEADSC_NEW = '# The eight heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.\n'
CMPC_OLD = cut('# develop...head = f9c28a8b8 ahead 1 for all seven PRs', '(git diff --name-only + rev-list, drafter 17:5x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = ba1210afc ahead 1 for all eight PRs; files 1 each\n'
            '# (git diff --name-only + rev-list, drafter 21:5x AEST; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1077 $MERGE_BASE', '1083 $MERGE_BASE ahead=1 files=1"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): thirty paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): thirty-six paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (O, 'O'), (V, 'V'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN)
assert len(JPATHS) == 36, ('judged path count', len(JPATHS))
VERIFP = A + 'src/routes/verification.ts'
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p]
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k = 'VERIFTS' if p == VERIFP else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k, ' ' * max(1, 80 - len(k)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\nO = D + "services/originate/"\nV = D + "services/vc-issuer/"\n'
              'VERIFTS = A + "src/routes/verification.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all eight heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr[:9]) for n, _, _, _, _, _, tr in PRS) + '; all eight together ' + COMBINED + ', drafter tree-hash and three-order scratch-clone merges = builder prediction; git ls-remote)"); sys.exit(0)\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = ('GUARDED = [A + "src/",\n'
             '           A + "package.json",\n'
             '           A + "vitest.config.ts",\n'
             '           A + "tsconfig.json",\n'
             '           O + "src/",\n'
             '           O + "package.json",\n'
             '           O + "jest.config.js",\n'
             '           O + "tsconfig.json",\n'
             '           V + "src/",\n'
             '           V + "package.json",\n'
             '           V + "package-lock.json",\n'
             '           V + "vitest.config.ts",\n'
             '           V + "tsconfig.json",\n'
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
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the seven heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the eight heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all eight '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway, originate and vc-issuer src/ + config, packages/shared src/, scripts/, .githooks/, '
               'the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, t, 1 if n in TIER1 else 2) for n, t, *_ in PRS]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
SEATWORDS = ['The 3 skipped legs need a stack', 'login_stub', 'mergeable_state: unstable', 'zero product bytes']
GWORDS = ['18499832', 'e9fc521fbfb72dab46b751ee215e76268efffab7', 'fa9573ff4f16', 'ab8cf42a9e96', '95c52eeb088d', 'aa66a0aa4555', 'c3a3e6140e5d',
          '1db9dd398a46', '2c7f6a3dbdef', 'RAW521', 'TENANTSORGPROV', 'TENANTSUNGUARDED', '--listFilesOnly', 'bb8801cfb463', '394337283ec1',
          'db.retry.test.ts']
for w in SEATWORDS + GWORDS: assert w in pt_ and w in mt_, ('READY mail and prompt must both carry', w)
BYNAME = ['18580369', 'ZERO product bytes in #1090 and #1091', 'NON-RULED', 'must not recommend pinning -1 either way', 'SAME ROW FORMAT as the PRIOR REPORT', 'CORRECTED FACTS-COMMENT TEXT']
for w in BYNAME: assert "'" not in w, ('an apostrophe would break the single-quoted grep', w)
for w in BYNAME: assert w in pt_, ('prompt lacks the by-name item', w)
assert 'MEASURE, not conclude' in pt_ and 'COMPLETE or NOT-COMPLETE' in pt_ and 'eight lines, one per pr' in pt_.lower() and 'proposed cell' in pt_ \
       and 'GATEWAY_URL=http://127.0.0.1:' in pt_, 'prompt phrasing'
TRAPGREP = ' && '.join("grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\" && grep -qF '| #%d | %s' \"$BRIEF\"" % (n, t, n, t) for n, t, *_ in PRS)
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", '>&2; exit 32; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1090 + #1091 T1, #1084-#1089 T2)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'EIGHT lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and EIGHT verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'The 3 skipped legs need a stack' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'mergeable_state: unstable' "$PROMPT_FILE" && grep -qF 'zero product bytes' "$PROMPT_FILE" \
  && grep -qF 'The 3 skipped legs need a stack' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state: unstable' "$BRIEF" && grep -qF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: The 3 skipped legs need a stack / login_stub / mergeable_state: unstable / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-6th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
''' + ''.join('grep -qF -- \'%s\' "$PROMPT_FILE" && grep -qF -- \'%s\' "$BRIEF" && ' % (w, w) for w in GWORDS) + r'''grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items 1-10, or the prompt does not say MEASURE, not conclude and rule KS-1238 COMPLETE or NOT-COMPLETE" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF '__PREDICT__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-eight tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
''' + TRAPGREP + r''' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket each PR is (PR #1084 is KS-1269 ... PR #1090 and PR #1091 are KS-1238) — the PR numbers are other tickets' numbers too" >&2; exit 32; }
''' + ' && '.join('grep -qF -- \'%s\' "$PROMPT_FILE"' % w for w in BYNAME) + r''' \
  || { echo "REFUSING: the prompt does not carry Wednesday's by-name items (KS-1238 comment 18580369 and the corrected facts text, ZERO product bytes in #1090 and #1091, the NON-RULED /unrevoke -1 rule, the PRIOR REPORT's row format)" >&2; exit 33; }
grep -qF -- '--listFilesOnly' "$PROMPT_FILE" && grep -qF -- '--listFilesOnly' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the tsc --listFilesOnly finding (by-name item 5)" >&2; exit 33; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED).replace('__PREDICT__', BUILDER_PREDICT_COMMIT)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  eight heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1090 + #1091 T1, #1084-#1089 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all eight heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, EIGHT verdict lines"
  echo "  prompt names the report directory, the #1077-#1083 batch PRIOR REPORT, the EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: The 3 skipped legs need a stack / login_stub / mergeable_state: unstable / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-6th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items; the prompt says MEASURE, not conclude, and rules KS-1238 COMPLETE or NOT-COMPLETE"
  echo "  prompt names the all-eight tree, the octopus commit, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket each of the eight PRs is (namespace trap; #1090 and #1091 both KS-1238)"
  echo "  prompt carries Wednesday's by-name items: 18580369 + corrected facts text, ZERO product bytes in #1090 and #1091, NON-RULED -1, --listFilesOnly, the row format"
  [ -n "${QAB1084_CUR_DEV:-}" ] && echo "  (develop read from the QAB1084_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1084_VERIFTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/verification.ts read from the QAB1084_VERIFTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('heads comment', HEADSC_OLD, HEADSC_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1077_CUR_DEV:-', 'CUR_DEV="${QAB1084_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1077_VERIFTS_FILE", "") if f == VERIFTS else ""\n',
                 '    fixture = os.environ.get("QAB1084_VERIFTS_FILE", "") if f == VERIFTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1077_BRIEF:-}${QAB1077_PROMPT:-}${QAB1077_HEAD_1083:-}${QAB1077_CUR_DEV:-}${QAB1077_VERIFTS_FILE:-}" ]',
            '[ -z "${QAB1084_BRIEF:-}${QAB1084_PROMPT:-}${QAB1084_HEAD_1091:-}${QAB1084_CUR_DEV:-}${QAB1084_VERIFTS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1077-1083 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1077-#1083 batch': 2, 'from launch_qa_secuura_batch1077_1083.sh': 1}   # exit 24 comment + --check line; the template
for k, v in INTENDED.items():
    assert BODY.count(k) == v, ('intended citation count', k, BODY.count(k), v)
    BODY = BODY.replace(k, '<CITED>')
RESID = ['QAB1077_', 'mail_batch1077', 'gate1077to1083', 'batch1077', '993718b84', '6780f7856', 'f9c28a8b8', 'seatB-5th', 'seven', 'SEVEN',
         'thirty paths', 'THIRTY paths', 'RAW516', '75b0024e', '0ef47512b728', 'ks1238-RAW516-whole.out', 'ks1258-D3-combined.json', 'CHECKER_NO_RESULT',
         'NONEDECLAREDEXIT0', '68e05caaed94', ':788', '17:51:24', '17:5x', '07:48:28', 'PR #1077 is', 'PR #1083 is', 'goes Done + archived ONLY', 'N76-1',
         'N68-1 (', 'N62', 'N67-1', 'N74-1', 'N72-1', 'N75-1', 'KS-1260', 'files 2/1/1']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])(107[7-9]|108[0-3])(?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 2,   # OKPIN + the exit-31 guard
       REPORT_DIR: 1, PRIOR: 1, EARLIER: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT"': None, 'QAB1084_CUR_DEV': None, 'QAB1084_VERIFTS_FILE': None,
       'QAB1084_HEAD_1091': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 32': None, 'exit 33': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-19_secuura-batch1084-1091.prompt.txt': 1, 'gatesets/2026-09-19_gate1084to1091/mail_batch1084_ready.md': None,
       '"BACKLOG.md"]': 1, 'O + "src/",': 1, 'A + "src/",': 1, 'V + "src/",': 1, 'D + "packages/shared/src/",': 1, 'D + "scripts/",': 1, '".githooks/",': 1,
       'ahead=1 files=': 8, 'VERIFTS': None, BUILDER_PREDICT_COMMIT: 1}
for n, t, *_ in PRS: CTL["grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\"" % (n, t)] = 1; CTL["grep -qF '| #%d | %s' \"$BRIEF\"" % (n, t)] = 1
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if k == '"ABSENT"':
        # the JUDGED comment carries ABSENT UNQUOTED, so only the 404 branch `blob = "ABSENT"` counts
        if got[k] != 1: print('CONTROL DISAGREED', k, got[k], 'want 1 (the 404 branch only; this batch has no new file)'); sys.exit(1)
        continue
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for p, b in DEVPIN.items():
    if s.count(b) != 1: print('CONTROL DISAGREED develop pin', p, s.count(b)); sys.exit(1)
for p, (b, n) in LANDED.items():
    if s.count(b) != 1: print('CONTROL DISAGREED landed pin', n, p, s.count(b)); sys.exit(1)
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
