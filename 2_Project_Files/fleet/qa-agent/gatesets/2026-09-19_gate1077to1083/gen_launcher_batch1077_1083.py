#!/usr/bin/env python3
"""gen_launcher_batch1077_1083.py — derive launchers/launch_qa_secuura_batch1077_1083.sh from launchers/launch_qa_secuura_batch1070_1076.sh (the
batch gate prepared 2026-09-19 14:44, one gate / seven verdicts) by ASSERTED block substitutions: every anchor must occur exactly as often as
stated, or the generator refuses and writes nothing. Structure copied from gatesets/2026-09-19_gate1070to1076/gen_launcher_batch1070_1076.py;
the data changed.

ONE BATCHED gate, TIER 1 floor (set by #1083 KS-1238, auth, test-only), SEVEN PRs #1077..#1083 (Seat B 5th, READY 2026-09-19 07:48:28Z).
ALL SEVEN ARE TEST-ONLY: every changed path sits under a __tests__/ directory (asserted from local objects here; the launcher's prompt asks the gate
to prove it from the PR files API too — gh_pr_reads.out beside this file already did).
NAMESPACE TRAP: the PR numbers are also other tickets' numbers (KS-1077 and KS-1078 were gated 2026-09-14); PR #1077 is KS-1258 ... PR #1083 is
KS-1238. The launcher refuses (exit 32) unless the prompt AND the READY both state which ticket each of the seven PRs is.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (git rev-parse / cat-file / diff --name-only / rev-list): each PR is ONE commit whose parent IS develop; every PR's file set and
    head tree as pinned; every judged develop blob and every landed head blob as pinned; the seven pairwise file-disjoint (8 files, 0 new);
    zero product bytes in every PR; the commits carry Refs <own ticket> (five) or NO KS key at all (#1079, #1082);
  * CANONICAL-PATCH identity for ALL SEVEN (every one is a local-model patch.diff, strict; #1077 is two runs): develop's blobs are written as plain
    files into a fresh scratch dir (not a repo), `git apply` (patch mode, cwd = that dir) applies each run's patch.diff, and `git hash-object` (no
    -w) of each result must equal the head blob; controls: #1077 with ONE run must differ; every patch applied --reverse onto develop's blobs must
    refuse; a crossed patch (#1082's into #1077's develop blobs) must refuse;
  * the ALL-SEVEN TREE is re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, CONTROLLED by re-deriving each of the
    seven head trees from develop the same way; it must equal the builder's 993718b84 and the tree of its local octopus commit 6780f7856. (The
    drafter ALSO predicted it by merge-tree chains in a --shared scratch clone: predict_all_seven_scratch.sh / .out beside this file.)
Usage: gen_launcher_batch1077_1083.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1077_1083', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = 'f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf'   # develop at 07:51:24Z (#1070-#1076 merged); every PR's merge-base
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad'
# n, ticket, branch, head, ahead, file count, head tree
PRS = [
 (1077, 'KS-1258', 'feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n68', '3a549bcf821f0f2e41e6188cf8384ff16329179f', 1, 2, '1cecf7d3db546f52fb95f0f8362db98277d6e5a1'),
 (1078, 'KS-1260', 'feature/ks-1260-preflight-verdict-pins-ratio-leg1-note-none-declared-n62', 'c204a830848447ed6571f5c6547991fbe7b89402', 1, 1, '01d7b90adf704c4e0a32eb40bd537bc89ca6278f'),
 (1079, 'KS-1062', 'feature/pin-startup-migrations-skipped-tenant-summary-meta', 'de823dcdead32334444024774f6dd8dae8b9726a', 1, 1, '08d8262af7f35e28d265e407173fa4d5378953dc'),
 (1080, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n74-1', 'cdff7905d55756ff4d30acaf3cf14e0080d3d209', 1, 1, 'bd54a2249e8364c7e7b14935938b781b2babaff4'),
 (1081, 'KS-1206', 'feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an-n72-1', '2f0dfbcbb78f8ba1d99ab2f64c81b1b0334a92b3', 1, 1, '192e74a09408eb8c56f3ec40968920cb1a9ce6b1'),
 (1082, 'KS-739', 'feature/pin-transfer-custody-nonjson-404-500-lookup', 'c72e3f594f381175c5b4f917ee8b1665517e5f0d', 1, 1, '11a6bdc16b022cb34e6bc8568bccccbf7a43a996'),
 (1083, 'KS-1238', 'feature/ks-1238-n76-1-pin-documents-verify-sends-no-caller-bearer', '5f3280e9c09a5315968a48cb57f7166d361a2161', 1, 1, 'd98e0d35ba8491cfee73b7e5814dfdd77931a23c'),
]
ARCHIVED = {1079, 1082}                                  # KS-1062 and KS-739: Done + archived; NO Refs, NO KS key in the commit
TIER1 = 1083
COMBINED = '993718b84caa4478989a301331d53740991e6b79'   # builder's predicted all-seven tree (READY 07:48:28Z); re-derived below
BUILDER_PREDICT_COMMIT = '6780f7856'                    # builder's local-only octopus commit (8 parents); its tree must be COMBINED
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
 1077: [('2026-09-19_ks1258-ornith35b-night2', 'patch.diff'), ('2026-09-19_ks1258-ornith35b-night3', 'patch.diff')],   # N68-1, N68-2
 1078: [('2026-09-19_ks1260-ornith35b-night2', 'patch.diff')],
 1079: [('2026-09-19_ks1062-ornith35b-night2', 'patch.diff')],
 1080: [('2026-09-19_ks1230-ornith35b-night3', 'patch.diff')],
 1081: [('2026-09-19_ks1206-ornith35b-night3', 'patch.diff')],
 1082: [('2026-09-19_ks739-ornith35b-night5', 'patch.diff')],
 1083: [('2026-09-19_ks1238-ornith35b-night3', 'patch.diff')],
}
# every section applies strict (no opts file in any of the eight checker dirs — asserted below); the READY: "no D1 or D5-style change this round"

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 A + 'src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts': '6dbf8f1e0de1a03af6957748040e85190807f19a',
 A + 'src/__tests__/ks1258-degraded-optional-service-advice.test.ts': 'b8abdea46d68f745724fa7b36b3b852ddb38118b',
 D + 'scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh': '23a19ae6ddb532dc604a681a1e51eece1409e951',
 A + 'src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts': 'a30b777a017febbef378ad0772c4841ae12efa9f',
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': 'd7adefe7b6fad5135d3a934ec58119dd6aa13ea6',
 O + 'src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts': '97e3e28822556e6c85a2e6d5653538a11b952bbc',
 O + 'src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts': 'fcb46e6aa547fd51d8273b9336bae0dc87ad0dca',
 A + 'src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts': 'ee10e191c8497948720ccc3e9df705601c4a67b1',
 A + 'src/routes/verification.ts': 'f888e8cd0bd10c98a508542d75902ab122595157',
 A + 'src/routes/system-status.ts': 'e911ce1fdaa4b755e9b7b6428f899cdbd63889cb',
 A + 'src/startup-migrations.ts': 'ed3e521426e75910c5bf2cf07e7251f2fd8ef538',
 A + 'src/routes/admin.ts': '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 A + 'src/routes/proxy.ts': '795ae7ca3bdc76be3e563e87fc34a8cc221e5632',
 A + 'src/routes/platform.ts': 'b80a8cd8d4e1af5a944817227f5ee6612c793954',
 A + 'src/middleware/auth.ts': 'bf09d315a64443b7f02bc27a74366b7a7f1dae81',
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
    # zero product bytes: every PR changes files under a __tests__/ directory ONLY (#1078 under scripts/__tests__/, the rest under src/__tests__/)
    prod = [f for f in files if '/__tests__/' not in f]
    print('    files outside __tests__/: %d %s (want 0)' % (len(prod), [f.split('/')[-1] for f in prod]))
    if prod: bad.append(('product bytes', n, prod))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 8: bad.append(('seven PRs not pairwise file-disjoint / not 8 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
# namespace trap, asserted from the commits: no commit names its own PR number as a ticket; each live PR carries Refs <its ticket>;
# the two archived-ticket PRs carry NO KS key at all in the commit (the seat's message lint)
subj = {n: git('log', '-1', '--format=%s%n%b', h).stdout for n, _, _, h, *_ in PRS}
trap = all('KS-%d' % n not in subj[n] for n, *_ in PRS) \
       and all(re.search(r'^Refs ' + t + r'\b', subj[n], re.M) for n, t, *_ in PRS if n not in ARCHIVED) \
       and all(not re.search(r'KS-\d+', subj[n]) for n in ARCHIVED)
print('namespace trap (no commit names KS-<its own PR number>; five carry Refs <own ticket>; #1079 and #1082 carry NO KS key):', trap)
if not trap: bad.append(('namespace trap / Refs', {n: subj[n][:60] for n in subj}))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1077-', dir=SCRATCH)
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
# control: #1077 with ONE run (N68-1 only) must NOT equal the head (both runs are load-bearing)
W = os.path.join(X, 'control-1077-onerun'); os.makedirs(W)
got, files = apply_into(W, 1077, headof[1077], CANON[1077][:1])
diff_ok = got is not None and any(got[f] != rp(headof[1077] + ':' + f) for f in files)
print('  CONTROL #1077 N68-1 run ALONE -> differs from the head in some file: %s (want True)' % diff_ok)
if not diff_ok: bad.append(('#1077 one-run control',))
# control: every canonical patch applied --reverse onto develop's blobs must refuse (the patch is not already in develop)
for n, t, br, h, *_ in PRS:
    for run, name in CANON[n]:
        W = os.path.join(X, 'control-reverse-%d-%s' % (n, run.split('_')[1])); os.makedirs(W); seed(W, h)
        r = subprocess.run(['git', 'apply', '--reverse', '--check', sec(run, name)], cwd=W, capture_output=True, text=True)
        print('  CONTROL #%d %s --reverse onto develop blobs refuses: rc %d (want non-zero)' % (n, run.split('_')[1], r.returncode))
        if r.returncode == 0: bad.append(('reverse control applied', n, run))
# control: a canonical patch into the WRONG file set refuses — #1082's patch into #1077's develop blobs
W = os.path.join(X, 'control-crossed'); os.makedirs(W); seed(W, headof[1077])
r = subprocess.run(['git', 'apply', '--check', sec('2026-09-19_ks739-ornith35b-night5', 'patch.diff')], cwd=W, capture_output=True, text=True)
print('  CONTROL crossed: #1082 patch into #1077 develop blobs refuses: rc %d (want non-zero)' % r.returncode)
if r.returncode == 0: bad.append(('crossed control applied',))
print('scratch (plain files, not a repo; left in place):', X)

# 4. the all-seven tree by pure tree hashing (read-only cat-file), controlled by each single head tree
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
print('ALL SEVEN over develop -> %s | builder predicted %s: %s | builder octopus commit %s tree %s: %s' % (comb, COMBINED[:9], comb == COMBINED, BUILDER_PREDICT_COMMIT, bt[:9], bt == COMBINED))
if comb != COMBINED or bt != COMBINED: bad.append(('combined tree', comb, bt))
scr = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'predict_all_seven_scratch.out')).read()
scr_ok = (re.search(r'forward: 7 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None
          and re.search(r'reverse: 7 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None and 'PREDICTION OK' in scr and 'rc=0' in scr)
print('scratch-clone prediction (predict_all_seven_scratch.out, forward + reverse merge-tree chains) names', COMBINED[:9], 'twice and PREDICTION OK:', scr_ok)
if not scr_ok: bad.append(('scratch prediction',))
ghr = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gh_pr_reads.out')).read()
gh_ok = 'ZERO PRODUCT BYTES in all seven (files API): True' in ghr and ghr.count('files outside __tests__/ (files API): 0 []') == 7 and 'rc=0' in ghr
print('PR files API (gh_pr_reads.out): zero product bytes in all seven:', gh_ok)
if not gh_ok: bad.append(('files API zero-product read',))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-19_gate1077to1083/mail_batch1077_ready.md'
PROMPT = WEDB + 'briefs/2026-09-19_secuura-batch1077-1083.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1077-1083-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1070-1076-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1061-1069-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1077-#1083 (seven PRs; tier 1 = #1083 KS-1238)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-5th/'
assert os.path.isdir(PRIOR) and os.path.isdir(EARLIER) and os.path.isdir(SEATHIST), 'prior / earlier report or seat history dir missing'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head in full'
assert 'MESSAGE_ID: <010001a0b8a359a9-66f50e63-7ccd-47e1-855f-f3cf3b0ba896-000000@email.amazonses.com>' in mt_ and 'TS: 2026-09-19T07:48:28' in mt_, 'mail capture is not the 07:48:28Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED[:9] in mt_ and COMBINED in pt_ and BUILDER_PREDICT_COMMIT in pt_ and BUILDER_PREDICT_COMMIT in mt_, 'combined tree / octopus commit not named in mail AND prompt'
for n, t, *_ in PRS:
    assert ('PR #%d is %s.' % (n, t)) in pt_ and ('| #%d | %s' % (n, t)) in mt_, ('namespace trap not named for', n, t)

HEADER_OLD = cut('# launch_qa_secuura_batch1070_1076.sh', '# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1077_1083.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SEVEN file-disjoint Secuura/Blockchain PRs
#   #1077 KS-1258 @ 3a549bcf8  ks1248 + ks1258 vitest tests: N68-1 (:576 required advice, no start command) + N68-2 (:592 allow-list)  — TIER 2 (test-only)
#   #1078 KS-1260 @ c204a8308  preflight_failure_verdict_keeps_ratio.test.sh (BASH): N62, +3 cells, run_legs gains two optional args — TIER 2 (test-only)
#   #1079 KS-1062 @ de823dcde  ks1062 vitest test: N67-1, a SKIPPED tenant counted as skipped (archived ticket, NO Refs, NO key)     — TIER 2 (test-only)
#   #1080 KS-1230 @ cdff7905d  ks1230 vitest test: N74-1, a null allow-list in the MIDDLE of three integrations is stored as null     — TIER 2 (test-only)
#   #1081 KS-1206 @ 2f0dfbcbb  ks1206 jest test: N72-1, rateLimit false / "" / true / [] / {} refused 400 before the INSERT          — TIER 2 (test-only)
#   #1082 KS-739  @ c72e3f594  ks739 jest test: N75-1, a non-JSON 404 / 500 lookup maps to 404 / 502 (archived ticket, NO Refs)    — TIER 2 (test-only)
#   #1083 KS-1238 @ 5f3280e9c  ks1238 vitest test: N76-1, POST documents/:id/verify sends no caller Bearer (verification.ts:516)  — TIER 1 (AUTH, test-only)
# ALL SEVEN ARE TEST-ONLY: every changed path is under a __tests__/ directory (generator: local objects AND the PR files API; 0 product bytes).
# #1083's verdict carries the ruling KS-1238 COMPLETE or NOT-COMPLETE; KS-1238 goes Done + archived ONLY on COMPLETE.
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too (KS-1077 / KS-1078 were gated 2026-09-14); the READY mail AND the prompt must BOTH
# state which ticket each of the seven PRs is, or the launch refuses (exit 32).
# Batched under Kam's 09:22 rule. SEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 17:51:24 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop f9c28a8b8; compare develop...head = merge_base f9c28a8b8, ahead 1, files 2/1/1/1/1/1/1 (asserted per PR, exit 10).
# Pairwise file-disjoint (8 files, all modified, 0 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL SEVEN = tree 993718b84,
# re-derived by the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains, forward and
# reverse), equal to the builder's prediction and to its local octopus commit 6780f7856's tree. All seven are byte-identical to their CANONICAL
# local-model patch.diff, re-applied strict by the generator in a plain scratch dir (#1077 = two runs), each reverse-applied control refusing.
#
# The develop pin is judged by CONTENT — THIRTY paths by blob at the CURRENT develop: the 8 PR files (all at develop blobs; any PR's head blob ->
# exit 19 LANDED, naming the PR), and what the gate runs or reads: verification.ts (RAW516 / :788), system-status.ts, startup-migrations.ts, admin.ts,
# proxy.ts / platform.ts / auth.ts (the KS-1238 completeness census), adminConfig.ts, documents.ts, preflight.sh, run-shell-suites.sh, the pre-push
# hook, the api-gateway / originate configs, the Dev package.json + lock, eslint.config.mjs and BACKLOG.md.
# GUARDED: api-gateway / originate src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs,
# BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1077to1083/mail_batch1077_ready.md, the seat's READY mail (07:48:28Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the seven heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all seven heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1070-#1076 batch), the EARLIER REPORT (the #1061-#1069 batch) and
#          NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'The 3 skipped legs need a stack', 'login_stub',
#          'mergeable_state: unstable' and 'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-5th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (verification.ts:516, :788, 75b0024e, RAW516, ks1238-RAW516-whole.out,
#          0ef47512b728, ks1258-D3-combined.json, CHECKER_NO_RESULT, NONEDECLAREDEXIT0, 68e05caaed94), and the prompt must ask the gate to
#          MEASURE, not conclude, and to rule KS-1238 COMPLETE or NOT-COMPLETE.
# exit 31: the prompt must name the all-seven tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the seven, which ticket the PR is (PR #1077 is KS-1258 ... PR #1083 is KS-1238).
# QAB1077_CUR_DEV (test override, --check only): stands in for origin develop. QAB1077_HEAD_1083 (test override): stands in for #1083's pinned head.
# QAB1077_VERIFTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/verification.ts (its git blob).
# A launch with any QAB1077_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1077to1083/gen_launcher_batch1077_1083.py from launch_qa_secuura_batch1070_1076.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-seven tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1077_1083.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != TIER1 else '${QAB1077_HEAD_1083:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1070_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1077_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1077_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (07:48:28Z) and re-read by the drafter (git ls-remote 17:51:24 AEST, branch AND refs/pull/N/head)\n'
            '# NAMESPACE TRAP: no PR here is its own-numbered ticket; the ticket column is the truth (exit 32)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 17:51:24 AEST; every head's merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            "EARLIER_REPORT='" + EARLIER + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
CMPC_OLD = cut('# develop...head = 51dbedd39 ahead 1 for all seven PRs', '(git diff --name-only + rev-list, drafter 14:3x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = f9c28a8b8 ahead 1 for all seven PRs; files #1077 2, #1078-#1083 1 each\n'
            '# (git diff --name-only + rev-list, drafter 17:5x AEST; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1070 $MERGE_BASE', '1076 $MERGE_BASE ahead=1 files=2"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): thirty-five paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): thirty paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (O, 'O'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN)
assert len(JPATHS) == 30, ('judged path count', len(JPATHS))
VERIFP = A + 'src/routes/verification.ts'
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p]
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k = 'VERIFTS' if p == VERIFP else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k, ' ' * max(1, 80 - len(k)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\nO = D + "services/originate/"\n'
              'VERIFTS = A + "src/routes/verification.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all seven heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr[:9]) for n, _, _, _, _, _, tr in PRS) + '; all seven together ' + COMBINED + ', drafter tree-hash and scratch-clone merges = builder prediction; git ls-remote)"); sys.exit(0)\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = ('GUARDED = [A + "src/",\n'
             '           A + "package.json",\n'
             '           A + "vitest.config.ts",\n'
             '           A + "tsconfig.json",\n'
             '           O + "src/",\n'
             '           O + "package.json",\n'
             '           O + "jest.config.js",\n'
             '           O + "tsconfig.json",\n'
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
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the seven heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all seven '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway and originate src/ + config, packages/shared src/, scripts/, .githooks/, '
               'the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, t, 1 if n == TIER1 else 2) for n, t, *_ in PRS]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
SEATWORDS = ['The 3 skipped legs need a stack', 'login_stub', 'mergeable_state: unstable', 'zero product bytes']
GWORDS = ['verification.ts:516', ':788', '75b0024e', 'RAW516', 'ks1238-RAW516-whole.out', '0ef47512b728', 'ks1258-D3-combined.json',
          'CHECKER_NO_RESULT', 'NONEDECLAREDEXIT0', '68e05caaed94']
for w in SEATWORDS + GWORDS: assert w in pt_ and w in mt_, ('READY mail and prompt must both carry', w)
assert 'MEASURE, not conclude' in pt_ and 'COMPLETE or NOT-COMPLETE' in pt_ and 'seven lines, one per pr' in pt_.lower() and 'proposed cell' in pt_ \
       and 'GATEWAY_URL=http://127.0.0.1:' in pt_, 'prompt phrasing'
TRAPGREP = ' && '.join("grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\" && grep -qF '| #%d | %s' \"$BRIEF\"" % (n, t, n, t) for n, t, *_ in PRS)
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", '>&2; exit 32; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1083 T1, #1077-#1082 T2)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SEVEN verdict lines one per PR" >&2; exit 23; }
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
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-5th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
''' + ''.join('grep -qF \'%s\' "$PROMPT_FILE" && grep -qF \'%s\' "$BRIEF" && ' % (w, w) for w in GWORDS) + r'''grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items 1-5, or the prompt does not say MEASURE, not conclude and rule KS-1238 COMPLETE or NOT-COMPLETE" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF '__PREDICT__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-seven tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
''' + TRAPGREP + r''' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket each PR is (PR #1077 is KS-1258 ... PR #1083 is KS-1238) — the PR numbers are other tickets' numbers too" >&2; exit 32; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED).replace('__PREDICT__', BUILDER_PREDICT_COMMIT)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  seven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1083 T1, #1077-#1082 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all seven heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SEVEN verdict lines"
  echo "  prompt names the report directory, the #1070-#1076 batch PRIOR REPORT, the EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: The 3 skipped legs need a stack / login_stub / mergeable_state: unstable / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-5th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items; the prompt says MEASURE, not conclude, and rules KS-1238 COMPLETE or NOT-COMPLETE"
  echo "  prompt names the all-seven tree, the octopus commit, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket each of the seven PRs is (namespace trap)"
  [ -n "${QAB1077_CUR_DEV:-}" ] && echo "  (develop read from the QAB1077_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1077_VERIFTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/verification.ts read from the QAB1077_VERIFTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1070_CUR_DEV:-', 'CUR_DEV="${QAB1077_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1070_STATUSTS_FILE", "") if f == STATUSTS else ""\n',
                 '    fixture = os.environ.get("QAB1077_VERIFTS_FILE", "") if f == VERIFTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1070_BRIEF:-}${QAB1070_PROMPT:-}${QAB1070_HEAD_1076:-}${QAB1070_CUR_DEV:-}${QAB1070_STATUSTS_FILE:-}" ]',
            '[ -z "${QAB1077_BRIEF:-}${QAB1077_PROMPT:-}${QAB1077_HEAD_1083:-}${QAB1077_CUR_DEV:-}${QAB1077_VERIFTS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1070-1076 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1070-#1076 batch': 2, 'from launch_qa_secuura_batch1070_1076.sh': 1}   # exit 24 comment + --check line; the template
for k, v in INTENDED.items():
    assert BODY.count(k) == v, ('intended citation count', k, BODY.count(k), v)
    BODY = BODY.replace(k, '<CITED>')
RESID = ['QAB1070_', 'STATUSTS', 'mail_batch1070', 'gate1070to1076', 'batch1070', 'bc4d0ed7f', '29bc11a08', '51dbedd39', 'seatB-4th',
         'thirty-five', 'THIRTY-FIVE', 'VOCABULARY', 'vc-issuer', 'KS-1276', 'KS-1269', 'KS-864', 'MEETS or PARTIAL', 'status.ts:300', 'merge-msg-1071',
         '15:22:07', 'BEARERONLY', 'COMPLETENESS', 'Legs 3/4/8', '14:33:37', '14:3x', '04:30:27', 'lifecycle', 'test_by_design', 'schemathesis',
         'platform.ts:254', 'PR #1070 is', 'PR #1071 is', '           ST,', 'ST = ', 'V = D', '3 new', '10 files', "items 2-10"]
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])107[0-6](?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 2,   # OKPIN + the exit-31 guard
       REPORT_DIR: 1, PRIOR: 1, EARLIER: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT"': None, 'QAB1077_CUR_DEV': None, 'QAB1077_VERIFTS_FILE': None,
       'QAB1077_HEAD_1083': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 32': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-19_secuura-batch1077-1083.prompt.txt': 1, 'gatesets/2026-09-19_gate1077to1083/mail_batch1077_ready.md': None,
       '"BACKLOG.md"]': 1, 'O + "src/",': 1, 'A + "src/",': 1, 'D + "packages/shared/src/",': 1, 'D + "scripts/",': 1, '".githooks/",': 1,
       'ahead=1 files=': 7, 'VERIFTS': None}
for n, t, *_ in PRS: CTL["grep -qF 'PR #%d is %s.' \"$PROMPT_FILE\"" % (n, t)] = 1; CTL["grep -qF '| #%d | %s' \"$BRIEF\"" % (n, t)] = 1
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if k == '"ABSENT"':
        # run 1 (gen_launcher.out) wanted 2: the JUDGED comment carries ABSENT UNQUOTED, so only the 404 branch `blob = "ABSENT"` counts
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
