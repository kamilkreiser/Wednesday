#!/usr/bin/env python3
"""gen_launcher_batch1070_1076.py — derive launchers/launch_qa_secuura_batch1070_1076.sh from launchers/launch_qa_secuura_batch1061_1069.sh (the
batch gate that ran clean on 2026-09-19 11:59, one gate / nine verdicts) by ASSERTED block substitutions: every anchor must occur exactly as often
as stated, or the generator refuses and writes nothing. Structure copied from gatesets/2026-09-19_gate1061to1069/gen_launcher_batch1061_1069.py;
the data changed.

ONE BATCHED gate, TIER 1 floor (set by #1071 KS-1269), SEVEN PRs #1070..#1076 (Seat B 4th, READY 2026-09-19 04:30:27Z).
NAMESPACE TRAP: the PR numbers are also other tickets' numbers (KS-1070..KS-1075 exist); PR #1070 is KS-1276 and PR #1071 is KS-1269.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (git rev-parse / cat-file / diff --name-only / rev-list): each PR is ONE commit whose parent IS develop; every PR's file set and
    head tree as pinned; every judged develop blob and every landed head blob as pinned; the seven pairwise file-disjoint (10 files, 3 new);
    #1076 and the five test-only PRs change files under __tests__/ ONLY (zero product bytes); #1070 changes docs/VOCABULARY.md only;
  * CANONICAL-PATCH identity for ALL SEVEN (every one is a local-model patch; #1071 is two, #1076 is two): develop's blobs are written as plain
    files into a fresh scratch dir (not a repo), `git apply` (patch mode, cwd = that dir) applies each run's sections with their own opts, and
    `git hash-object` (no -w) of each result must equal the head blob; #1071 is ALSO applied in the REVERSE run order (KS-1269-U first) and must
    give the same blobs, and a ONE-run control must differ; #1076's ks1215 file = its canonical patch + EXACTLY the seat's two declared D5 lines
    (and the bare canonical must differ from the head) — run 1 (gen_launcher.out) refused on that file before D5 was modelled;
  * the ALL-SEVEN TREE is re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, CONTROLLED by re-deriving each of the
    seven head trees from develop the same way; it must equal the builder's bc4d0ed7f and the tree of its local octopus commit 29bc11a08. (The
    drafter ALSO predicted it by merge-tree chains in a --shared scratch clone: predict_all_seven_scratch.sh / .out beside this file.)
Usage: gen_launcher_batch1070_1076.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1070_1076', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '51dbedd39ade43cc511278502b2e1e190de641c7'   # develop at 04:33:37Z (#1061-#1069 merged); every PR's merge-base
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; V = D + 'services/vc-issuer/'; ST = 'systemTest/schemathesis/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad'
# n, ticket, branch, head, ahead, file count, head tree
PRS = [
 (1070, 'KS-1276', 'feature/ks-1276-docsvocabularymd165-166-says-lifecycle-payloads-are-stored', '59af03cbab07bfcd151206d732d3aa989ac0256c', 1, 1, '2c1ffc1b08d63f0d8639aaec5e0feb8199d8ac90'),
 (1071, 'KS-1269', 'feature/ks-1269-post-apistatusidrevoke-accepts-index-object-where-integer-is', 'dc0bf93159a981d695d4fcdff9329003e1c26d99', 1, 3, '0ff438faa339f5a214babf4455e5ad51641832cd'),
 (1072, 'KS-1206', 'feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an-n61-1', 'cb8c0b18616b29eea77ef6efac0e3fac90178671', 1, 1, '48eb671540a06ee91a3ee3e1043935908319c686'),
 (1073, 'KS-864', 'feature/ks-864-dead-estate-pointers-in-runtime-source-outside-n64-1', '085205d444f6045c5ccc1c45f741aa252beae764', 1, 1, '35d782a03c23de687e2ec4dfaa63f624ee5a4fda'),
 (1074, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n69-1', '6be54e11b263f9881c7b410ae17613134c577fb7', 1, 1, '7a67ef6a3587d2974dc21e4d1a94918585929db9'),
 (1075, 'KS-739', 'feature/pin-transfer-custody-nonjson-401-429-lookup-failed', '3ec034083716f104eccfc50e2734ab16082e1e72', 1, 1, '0eb2d8cec7d9879a43e35613493e4a07f21f2334'),
 (1076, 'KS-1238', 'feature/ks-1238-f-1-pin-bearer-scheme-and-hand-forwarded-routes', 'aff1568f387b5073f31dcb99519cafeda7cc66bc', 1, 2, '8e11427ef99706f809537a1bd6f86ceefe25b031'),
]
COMBINED = 'bc4d0ed7fccc3bb9f594bd18565c9a5e47ab9db4'   # builder's predicted all-seven tree (READY 04:30:27Z); re-derived below
BUILDER_PREDICT_COMMIT = '29bc11a08'                    # builder's local-only octopus commit (8 parents); its tree must be COMBINED
# canonical patches: n -> (target, [(run, section)])
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
R69, R69U = '2026-09-19_ks1269-ornith35b-night', '2026-09-19_ks1269-ornith35b-night2'
CANON = {
 1070: ('head', [('2026-09-19_ks1276-ornith35b-night', 'patch.diff')]),
 1071: ('head', [(R69, 'section_1.diff'), (R69, 'section_2.diff'), (R69U, 'section_1.diff'), (R69U, 'section_2.diff')]),
 1072: ('head', [('2026-09-19_ks1206-ornith35b-night2', 'patch.diff')]),
 1073: ('head', [('2026-09-19_ks864-ornith35b-night2', 'patch.diff')]),
 1074: ('head', [('2026-09-19_ks1230-ornith35b-night2', 'patch.diff')]),
 1075: ('head', [('2026-09-19_ks739-ornith35b-night4', 'patch.diff')]),
 1076: ('head', [('2026-09-19_ks1238-ornith35b-night', 'patch.diff'), ('2026-09-19_ks1238-ornith35b-night2', 'patch.diff')]),
}
# #1071 in the REVERSE run order (KS-1269-U first): READY item 2, blob level
CANON_1071_REV = [(R69U, 'section_1.diff'), (R69U, 'section_2.diff'), (R69, 'section_1.diff'), (R69, 'section_2.diff')]
WANT_OPTS = {1071: ['--directory=Blockchain/Dev']}   # the READY_KS-1269 / -U headers' rule; every other section applies strict (asserted below)
FORCED_OPTS = {}
# D5 (READY item 6 / item 8): the seat ADDED two ledger lines to the F1i canonical patch, declared in #1076's body and commit. The ONLY bytes in
# any head that are not a checker's canonical patch. (after canonical line N, inserted line) — measured by the drafter with diff(1), 14:4x AEST.
DEVIATION = {
 (1076, 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'):
   [(288, "    RAN.add('KS-1238 (i) bearer scheme case');"), (403, "      'KS-1238 (i) bearer scheme case',")],
}

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 D + 'docs/VOCABULARY.md': 'cc4093b0b992621a651c21ac9a4cb6cee9425515',
 V + 'src/routes/status.ts': 'c44d69275a28f51dc26e41c66f382208a7962f03',
 O + 'src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts': '02339f9b0e00048b07c521c75d66239878e87158',
 A + 'src/__tests__/ks864d-empty-portal-env-var-falls-back.test.ts': '95f5fd995353d24ae1c641c4f78b53aeb1ff1a25',
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': '7fcedac7602a22f202f3ef6257db940d52f98010',
 O + 'src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts': '234858bb1f2661bb82d4f7aa40f360d320448dee',
 A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': '75006b5cf50fb8b42a5e7588a1d622b9168c1b07',
 O + 'src/repositories/lifecycleEventRepo.ts': '0aec7a3265ee91eeb430ad02b2445d9d89a9f7f2',
 O + 'src/utils/lifecyclePayloadCodec.ts': 'ff48ac114a60d450e9d477d748d48562ba50502e',
 A + 'src/routes/proxy.ts': '795ae7ca3bdc76be3e563e87fc34a8cc221e5632',
 A + 'src/middleware/auth.ts': 'bf09d315a64443b7f02bc27a74366b7a7f1dae81',
 A + 'src/routes/platform.ts': 'b80a8cd8d4e1af5a944817227f5ee6612c793954',
 O + 'src/routes/adminConfig.ts': '62af28d017069d38fa00e7915bfa65226db678c6',
 A + 'src/routes/system-status.ts': 'e911ce1fdaa4b755e9b7b6428f899cdbd63889cb',
 A + 'src/routes/admin.ts': '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 O + 'src/routes/documents.ts': '3f837fc6e656d5a10f9cc349b1cb2a876a2be09b',
 V + 'src/vc-issuer.openapi.ts': '6ab97ceb863a2d0a3725259670307d165918e9ba',
 V + 'package.json': '27888b6eeb6c20b44af947d14eddb3bccf6293cf',
 V + 'vitest.config.ts': 'ddacccfb518d23d24ecfb5ddcf60e8373166d8b5',
 V + 'tsconfig.json': 'b3546b85f68847a2cd62ad74f10f5f7347579bc5',
 O + 'package.json': 'd4435238d3ece7f7da42f043f56ca7739a611132',
 O + 'jest.config.js': '735183662feea56d39f664eb6379cae1a2eec957',
 O + 'tsconfig.json': 'd1b46ece71ad5b2559ccad3648c23a5231e43b09',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 D + 'package.json': '773443a9faa0a2eb7caf01c313b880fbe3251922',
 D + 'package-lock.json': '646c19f6f7f735ba32bfb20bef8b936835184949',
 D + 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
 ST + 'tests/test_by_design_permissive.py': 'c96967cfce7022e625ca92f66c8224f7defbaba5',
 ST + 'config/schemathesis-baseline.json': 'e94ee422eca3eb80554cf8a4d65f78ed65658f44',
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
    if p not in DEVPIN and git('cat-file', '-e', DEV + ':' + p).returncode == 0: bad.append(('new file already at develop', p))
    if p in DEVPIN and DEVPIN[p] == b: bad.append(('head blob == develop blob', n, p))
for p, b in DEVPIN.items():
    if rp(DEV + ':' + p) != b: bad.append(('develop blob', p, b, rp(DEV + ':' + p)))
NEWFILES = sorted(p for p in LANDED if p not in DEVPIN)
print('landed paths', len(LANDED), '| new files (ABSENT at develop):', len(NEWFILES))
if len(NEWFILES) != 3: bad.append(('want 3 new files', NEWFILES))

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
    # zero product bytes: #1076 and the five test-only PRs touch __tests__/ only; #1070 the doc only; #1071 status.ts + __tests__/ only
    prod = [f for f in files if '/src/__tests__/' not in f]
    want_prod = {1070: [D + 'docs/VOCABULARY.md'], 1071: [V + 'src/routes/status.ts']}.get(n, [])
    print('    files outside src/__tests__/: %d %s (want %s)' % (len(prod), [f.split('/')[-1] for f in prod], [f.split('/')[-1] for f in want_prod]))
    if prod != want_prod: bad.append(('product bytes', n, prod))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 10: bad.append(('seven PRs not pairwise file-disjoint / not 10 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
# namespace trap, asserted from the commits: no commit names its own PR number as a ticket; each live PR carries Refs <its ticket>; #1075 no Refs
subj = {n: git('log', '-1', '--format=%s%n%b', h).stdout for n, _, _, h, *_ in PRS}
trap = all('KS-%d' % n not in subj[n] for n, *_ in PRS) and all(re.search(r'^Refs ' + t + r'\b', subj[n], re.M) for n, t, *_ in PRS if n != 1075) \
       and not re.search(r'^Refs ', subj[1075], re.M | re.I)
print('namespace trap (no commit names KS-<its own PR number>; six carry Refs <own ticket>; #1075 carries no Refs line):', trap)
if not trap: bad.append(('namespace trap / Refs', {n: subj[n][:60] for n in subj}))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1070-', dir=SCRATCH)
def apply_into(W, n, target, force_opts=None, sections=None):
    files = git('diff', '--name-only', DEV, target).stdout.splitlines()
    for f in files:
        if git('cat-file', '-e', DEV + ':' + f).returncode == 0:
            os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
            open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    for run, name in (sections or CANON[n][1]):
        o = opts_of(run, name)
        o = (o or []) if force_opts is None else force_opts
        if o != WANT_OPTS.get(n, []): bad.append(('opts differ from the READY header', n, name, o)); return None, files
        r = subprocess.run(['git', 'apply', *o, sec(run, name)], cwd=W, capture_output=True, text=True)
        print('  #%d %s/%s git apply %s rc %d %s' % (n, run.split('_')[1], name, ' '.join(o) or '(strict)', r.returncode, r.stderr.strip()[:120]))
        if r.returncode: return None, files
    return {f: subprocess.run(['git', 'hash-object', os.path.join(W, f)], capture_output=True, text=True).stdout.strip() for f in files}, files
for n, t, br, h, *_ in PRS:
    target = h
    W = os.path.join(X, 'p%d' % n); os.makedirs(W)
    got, files = apply_into(W, n, target, FORCED_OPTS.get(n))
    if got is None: bad.append(('canonical apply', n)); continue
    for f in files:
        want = rp(target + ':' + f)
        if (n, f) in DEVIATION:
            # the seat's DECLARED deviation from verbatim: canonical + exactly these inserted lines (after the given canonical line numbers) == head;
            # the bare canonical must NOT equal the head (else the deviation is not load-bearing)
            lines = open(os.path.join(W, f), 'rb').read().split(b'\n')
            for after, ins in sorted(DEVIATION[(n, f)], reverse=True): lines.insert(after, ins.encode())
            data = b'\n'.join(lines); dev_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            print('  #%d canonical %s -> %s != head %s: %s | + the %d DECLARED D5 lines -> %s == head: %s'
                  % (n, f.split('/')[-1], got[f][:9], want[:9], got[f] != want, len(DEVIATION[(n, f)]), dev_blob[:9], dev_blob == want))
            if got[f] == want or dev_blob != want: bad.append(('declared deviation does not account for the head', n, f))
            continue
        print('  #%d canonical %s -> %s == head %s: %s' % (n, f.split('/')[-1], got[f][:9], want[:9], got[f] == want))
        if got[f] != want: bad.append(('canonical patch != PR', n, f))
# #1071 order independence (READY item 2, blob level): KS-1269-U's sections FIRST must give the same blobs; one run alone must NOT
W = os.path.join(X, 'p1071-reverse'); os.makedirs(W)
got, files = apply_into(W, 1071, headof[1071], None, CANON_1071_REV)
rev_ok = got is not None and all(got[f] == rp(headof[1071] + ':' + f) for f in files)
print('  #1071 REVERSE order (KS-1269-U first) -> status.ts %s == head %s: %s' % ((got or {}).get(V + 'src/routes/status.ts', 'NONE')[:12], rp(headof[1071] + ':' + V + 'src/routes/status.ts')[:12], rev_ok))
if not rev_ok: bad.append(('#1071 reverse order',))
W = os.path.join(X, 'control-1071-onerun'); os.makedirs(W)
got, files = apply_into(W, 1071, headof[1071], None, CANON[1071][1][:2])
one = (got or {}).get(V + 'src/routes/status.ts', '')
print('  CONTROL #1071 KS-1269 run ALONE -> status.ts %s differs from the head: %s (want True)' % (one[:12], bool(one) and one != rp(headof[1071] + ':' + V + 'src/routes/status.ts')))
if not one or one == rp(headof[1071] + ':' + V + 'src/routes/status.ts'): bad.append(('#1071 one-run control',))
# control: #1071's --directory is load-bearing — section_1 applied WITHOUT it onto the same develop blobs must refuse (its paths are service-relative)
Wc = os.path.join(X, 'control-1071-nodir'); os.makedirs(Wc)
for f in git('diff', '--name-only', DEV, headof[1071]).stdout.splitlines():
    if git('cat-file', '-e', DEV + ':' + f).returncode == 0:
        os.makedirs(os.path.dirname(os.path.join(Wc, f)), exist_ok=True); open(os.path.join(Wc, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
r = subprocess.run(['git', 'apply', sec(R69, 'section_1.diff')], cwd=Wc, capture_output=True, text=True)
print('  CONTROL #1071 section_1 WITHOUT --directory onto develop blobs refuses: rc %d (want non-zero) %s' % (r.returncode, r.stderr.strip()[:100]))
if r.returncode == 0: bad.append(('#1071 no-directory control applied',))
# control: a canonical patch into the WRONG file set refuses — #1075's patch into #1071's develop blobs
r = subprocess.run(['git', 'apply', sec('2026-09-19_ks739-ornith35b-night4', 'patch.diff')], cwd=Wc, capture_output=True, text=True)
print('  CONTROL crossed: #1075 patch into #1071 develop blobs refuses: rc %d (want non-zero)' % r.returncode)
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
        assert f[4] in ('M', 'A'), ('only M/A expected', l)
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
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md'
PROMPT = WEDB + 'briefs/2026-09-19_secuura-batch1070-1076.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1070-1076-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1061-1069-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1070-#1076 (seven PRs; tier 1 = #1071 KS-1269)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-4th/'
assert os.path.isdir(PRIOR) and os.path.isdir(SEATHIST), 'prior report or seat history dir missing'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h[:9] in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head'
assert 'MESSAGE_ID: <010001a0b7ee0fd1-' in mt_ and 'TS: 2026-09-19T04:30:27' in mt_, 'mail capture is not the 04:30:27Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED[:9] in mt_ and COMBINED in pt_ and BUILDER_PREDICT_COMMIT in pt_ and BUILDER_PREDICT_COMMIT in mt_, 'combined tree / octopus commit not named in mail AND prompt'
assert 'PR #1070 is KS-1276' in pt_ and 'PR #1071 is KS-1269' in pt_ and '| #1070 | KS-1276 |' in mt_ and '| #1071 | KS-1269' in mt_, 'namespace trap not named'

HEADER_OLD = cut('# launch_qa_secuura_batch1061_1069.sh', '# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1070_1076.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SEVEN file-disjoint Secuura/Blockchain PRs
#   #1070 KS-1276 @ 59af03cba  docs/VOCABULARY.md: the PII caveat opens "payload is encrypted at rest" — the gate GRADES it MEETS or PARTIAL — TIER 2 (docs)
#   #1071 KS-1269 @ dc0bf9315  vc-issuer status.ts: /revoke and /unrevoke refuse a present non-integer index (400) + 2 new suites  — TIER 1 (runtime)
#   #1072 KS-1206 @ cb8c0b186  ks1206 jest test: N61-1, rateLimit null / 0 / 1.5 / "100" refused, lower bound 1 mints            — TIER 2 (test-only)
#   #1073 KS-864  @ 085205d44  ks864d vitest test: N64-1, an EMPTY NODE_ENV is reported as development                           — TIER 2 (test-only)
#   #1074 KS-1230 @ 6be54e11b  ks1230 vitest test: N69-1, a null allow-list on the SECOND integration is stored as null           — TIER 2 (test-only)
#   #1075 KS-739  @ 3ec034083  ks739 jest test: N66-1, a non-JSON 401 / 429 lookup answers that 4xx (archived ticket, NO Refs)     — TIER 2 (test-only)
#   #1076 KS-1238 @ aff1568f3  ks1215 test +1 cell (F1i) and NEW ks1238 test (F1ii): AUTH surface, test files only, 0 product bytes  — TIER 2 (test-only)
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too; PR #1070 is KS-1276 and PR #1071 is KS-1269 (exit 32).
# Batched under Kam's 09:22 rule. SEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 14:33:37 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop 51dbedd39; compare develop...head = merge_base 51dbedd39, ahead 1, files 1/3/1/1/1/1/2 (asserted per PR, exit 10).
# Pairwise file-disjoint (10 files, 3 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL SEVEN = tree bc4d0ed7f, re-derived by
# the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains, forward and reverse), equal to
# the builder's prediction and to its local octopus commit 29bc11a08's tree. All seven are byte-identical to their CANONICAL local-model patches,
# re-applied by the generator in a plain scratch dir (#1071's four sections with --directory=Blockchain/Dev, in both run orders; the rest strict).
#
# The develop pin is judged by CONTENT — THIRTY-FIVE paths by blob at the CURRENT develop: the 10 PR files (seven at develop blobs, three new files
# ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: the lifecycle repo + payload codec (KS-1276's
# premise), proxy.ts / auth.ts / platform.ts (the auth tampers and F-1 (iii)), adminConfig.ts, system-status.ts, admin.ts, documents.ts, the
# vc-issuer OpenAPI source, the vc-issuer / originate / api-gateway configs, the Dev package.json + lock, eslint.config.mjs, the two systemTest reads
# (test_by_design_permissive.py, schemathesis-baseline.json) and BACKLOG.md.
# GUARDED: vc-issuer / api-gateway / originate src/ + config, packages/shared src/, docs/VOCABULARY.md, systemTest/schemathesis/, the Dev
# package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md, the seat's READY mail (04:30:27Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the seven heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all seven heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1061-#1069 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'Legs 3/4/8 need a stack', 'mergeable_state: unstable' and 'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-4th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (status.ts:300, :231, merge-msg-1071.txt, 2026-08-27T15:22:07Z, platform.ts:254,
#          BEARERONLY, COMPLETENESS), and the prompt must ask the gate to MEASURE, not conclude, and to grade KS-1276 MEETS or PARTIAL.
# exit 31: the prompt must name the all-seven tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row.
# exit 32: the READY mail AND the prompt must BOTH name the namespace trap: PR #1070 is KS-1276, PR #1071 is KS-1269.
# QAB1070_CUR_DEV (test override, --check only): stands in for origin develop. QAB1070_HEAD_1076 (test override): stands in for #1076's pinned head.
# QAB1070_STATUSTS_FILE (test fixture, --check only): a local file stands in for develop services/vc-issuer/src/routes/status.ts (its git blob).
# A launch with any QAB1070_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1070to1076/gen_launcher_batch1070_1076.py from launch_qa_secuura_batch1061_1069.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-seven tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1070_1076.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != 1076 else '${QAB1070_HEAD_1076:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1061_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1070_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1070_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (04:30:27Z) and re-read by the drafter (git ls-remote 14:33:37 AEST, branch AND refs/pull/N/head)\n'
            '# NAMESPACE TRAP: PR #1070 is KS-1276 and PR #1071 is KS-1269 (no PR here is its own-numbered ticket)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 14:33:37 AEST; every head's merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADCHK_OLD = cut('# The nine heads, each pinned at its branch AND at refs/pull/N/head', 'HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"\ndone\n')
HEADCHK_NEW = HEADCHK_OLD.replace('# The nine heads, each pinned', '# The seven heads, each pinned', 1)
assert HEADCHK_NEW != HEADCHK_OLD
CMPC_OLD = cut('# develop...head = 3c447abc7 ahead 1 for all nine PRs', '(git diff --name-only + rev-list, drafter 11:4x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = 51dbedd39 ahead 1 for all seven PRs; files #1070 1, #1071 3, #1072-#1075 1 each, #1076 2\n'
            '# (git diff --name-only + rev-list, drafter 14:3x AEST; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1061 $MERGE_BASE', '1069 $MERGE_BASE ahead=1 files=1"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): thirty-six paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): thirty-five paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (O, 'O'), (V, 'V'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    if p.startswith(ST): return 'ST + "' + p[len(ST):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN) + NEWFILES
assert len(JPATHS) == 35, ('judged path count', len(JPATHS))
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p] if p in DEVPIN else '{"ABSENT": DV}'
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k = 'STATUSTS' if p == V + 'src/routes/status.ts' else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k, ' ' * max(1, 80 - len(k)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\nO = D + "services/originate/"\nV = D + "services/vc-issuer/"\nST = "systemTest/schemathesis/"\n'
              'STATUSTS = V + "src/routes/status.ts"\nDV = "develop"\n'
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
             '           V + "src/",\n'
             '           V + "package.json",\n'
             '           V + "vitest.config.ts",\n'
             '           V + "tsconfig.json",\n'
             '           D + "packages/shared/src/",\n'
             '           D + "docs/VOCABULARY.md",\n'
             '           ST,\n'
             '           D + "package.json",\n'
             '           D + "package-lock.json",\n'
             '           D + "eslint.config.mjs",\n'
             '           "BACKLOG.md"]\n'
             '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a\n'
             '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.\n'
             '# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.\n'
             'DEV_CONTENT_ALLOWED = {}\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the nine heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the seven heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all seven '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (vc-issuer, api-gateway and originate src/ + config, packages/shared src/, docs/VOCABULARY.md, '
               'systemTest/schemathesis/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, t, 1 if n == 1071 else 2) for n, t, *_ in PRS]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
SEATWORDS = ['Legs 3/4/8 need a stack', 'mergeable_state: unstable', 'zero product bytes']
GWORDS = ['status.ts:300', ':231', 'merge-msg-1071.txt', '2026-08-27T15:22:07Z', 'platform.ts:254', 'BEARERONLY', 'COMPLETENESS']
for w in SEATWORDS + GWORDS: assert w in pt_ and w in mt_, ('READY mail and prompt must both carry', w)
assert 'MEASURE, not conclude' in pt_ and 'MEETS or PARTIAL' in pt_ and 'seven lines, one per pr' in pt_.lower() and 'proposed cell' in pt_, 'prompt phrasing'
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", '>&2; exit 32; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1071 T1, #1070 and #1072-#1076 T2)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat's READY mail capture path" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "${_h:0:9}" "$BRIEF" \
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
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'Legs 3/4/8 need a stack' "$PROMPT_FILE" && grep -qF 'mergeable_state: unstable' "$PROMPT_FILE" && grep -qF 'zero product bytes' "$PROMPT_FILE" \
  && grep -qF 'Legs 3/4/8 need a stack' "$BRIEF" && grep -qF 'mergeable_state: unstable' "$BRIEF" && grep -qF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: Legs 3/4/8 need a stack / mergeable_state: unstable / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-4th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'status.ts:300' "$PROMPT_FILE" && grep -qF ':231' "$PROMPT_FILE" && grep -qF 'merge-msg-1071.txt' "$PROMPT_FILE" && grep -qF '2026-08-27T15:22:07Z' "$PROMPT_FILE" && grep -qF 'platform.ts:254' "$PROMPT_FILE" && grep -qF 'BEARERONLY' "$PROMPT_FILE" && grep -qF 'COMPLETENESS' "$PROMPT_FILE" \
  && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'MEETS or PARTIAL' "$PROMPT_FILE" \
  && grep -qF 'status.ts:300' "$BRIEF" && grep -qF ':231' "$BRIEF" && grep -qF 'merge-msg-1071.txt' "$BRIEF" && grep -qF '2026-08-27T15:22:07Z' "$BRIEF" && grep -qF 'platform.ts:254' "$BRIEF" && grep -qF 'BEARERONLY' "$BRIEF" && grep -qF 'COMPLETENESS' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items 2-10, or the prompt does not say MEASURE, not conclude and grade KS-1276 MEETS or PARTIAL" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF '__PREDICT__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-seven tree in full, the octopus commit, or the NOT-PINNED list with a proposed cell per row" >&2; exit 31; }
grep -qF 'PR #1070 is KS-1276' "$PROMPT_FILE" && grep -qF 'PR #1071 is KS-1269' "$PROMPT_FILE" && grep -qF '| #1070 | KS-1276 |' "$BRIEF" && grep -qF '| #1071 | KS-1269' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH name the namespace trap: PR #1070 is KS-1276 / PR #1071 is KS-1269" >&2; exit 32; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED).replace('__PREDICT__', BUILDER_PREDICT_COMMIT)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  seven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1071 T1, #1070 and #1072-#1076 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all seven heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SEVEN verdict lines"
  echo "  prompt names the report directory, the #1061-#1069 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: Legs 3/4/8 need a stack / mergeable_state: unstable / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-4th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items 2-10; the prompt says MEASURE, not conclude, and grades KS-1276 MEETS or PARTIAL"
  echo "  prompt names the all-seven tree, the octopus commit and the NOT-PINNED list with a proposed cell per row"
  echo "  READY mail and prompt BOTH name the namespace trap: PR #1070 is KS-1276, PR #1071 is KS-1269"
  [ -n "${QAB1070_CUR_DEV:-}" ] && echo "  (develop read from the QAB1070_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1070_STATUSTS_FILE:-}" ] && echo "  (develop services/vc-issuer/src/routes/status.ts read from the QAB1070_STATUSTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('head check', HEADCHK_OLD, HEADCHK_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1061_CUR_DEV:-', 'CUR_DEV="${QAB1070_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1061_ADMINCFG_FILE", "") if f == ADMINCFG else ""\n',
                 '    fixture = os.environ.get("QAB1070_STATUSTS_FILE", "") if f == STATUSTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1061_BRIEF:-}${QAB1061_PROMPT:-}${QAB1061_HEAD_1069:-}${QAB1061_CUR_DEV:-}${QAB1061_ADMINCFG_FILE:-}" ]',
            '[ -z "${QAB1070_BRIEF:-}${QAB1070_PROMPT:-}${QAB1070_HEAD_1076:-}${QAB1070_CUR_DEV:-}${QAB1070_STATUSTS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1061-1069 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1061-#1069 batch': 2, 'from launch_qa_secuura_batch1061_1069.sh': 1}   # exit 24 comment + --check line; the template
for k, v in INTENDED.items():
    assert BODY.count(k) == v, ('intended citation count', k, BODY.count(k), v)
    BODY = BODY.replace(k, '<CITED>')
RESID = ['QAB1061_', 'ADMINCFG', 'mail_batch1061', 'gate1061to1069', 'batch1061', '275cff9ff', '77b7af584', '3c447abc7', 'seatB-3rd',
         'nine', 'NINE', 'thirty-six', 'THIRTY-SIX', 'login_stub', 'security/src/index.ts:569', 'NOJSONCATCH', 'matches at 576', 'Nothing failed',
         'GATEWAY_URL', 'PR #1062 is KS-1260', 'PR #1067 is KS-1062', 'KS-1260', 'KS-1101', 'KS-991', 'KS-1062', 'KS-1258', 'execute the FAILED path',
         '11:42:47', '11:4x', '01:39:55', 'preflight_', 'run-shell-suites', 'startup-migrations', 'services/security', '.githooks/', 'D + "scripts/"',
         'setup_api_key', 'test_tenant_isolation_writes']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])106[1-9](?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 2,   # OKPIN + the exit-31 guard
        REPORT_DIR: 1, PRIOR: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT": DV': 3, 'QAB1070_CUR_DEV': 5, 'QAB1070_STATUSTS_FILE': 5,
       'QAB1070_HEAD_1076': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 32': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-19_secuura-batch1070-1076.prompt.txt': 1, 'gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md': None,
       '"BACKLOG.md"]': 1, 'O + "src/",': 1, 'A + "src/",': 1, 'V + "src/",': 1, 'D + "packages/shared/src/",': 1, 'D + "docs/VOCABULARY.md",': 1,
       '           ST,': 1, 'ahead=1 files=': 7, 'PR #1070 is KS-1276': None, 'PR #1071 is KS-1269': None}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
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
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp); sys.exit(3)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
