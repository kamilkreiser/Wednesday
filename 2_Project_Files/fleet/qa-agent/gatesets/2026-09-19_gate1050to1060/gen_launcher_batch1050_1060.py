#!/usr/bin/env python3
"""gen_launcher_batch1050_1060.py — derive launchers/launch_qa_secuura_batch1050_1060.sh from launchers/launch_qa_secuura_batch1042_1045.sh (the
batch gate that ran clean on 2026-09-18, one gate / four verdicts) by ASSERTED block substitutions: every anchor must occur exactly as often as
stated, or the generator refuses and writes nothing.

ONE BATCHED gate, TIER 1 floor (set by #1059 and #1060), ELEVEN PRs #1050..#1060 (Seat B 2nd successor, READY 2026-09-18 21:56:17Z).
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb anywhere, not even in a scratch repo:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (git rev-parse / cat-file / diff --name-only / rev-list): ten PRs are ONE commit whose parent IS develop; #1059 is THREE commits
    (verbatim / titles / yaml) on a first-parent chain to develop, each commit single-parent, each commit's file set as pinned; every PR's file set
    and head tree as pinned; every judged develop blob and every landed head blob as pinned; the eleven pairwise file-disjoint (19 files);
  * CANONICAL-PATCH identity for ALL ELEVEN (every one is a local-model patch): develop's blobs are written as plain files into a fresh scratch dir
    (not a repo), `git apply` (patch mode, cwd = that dir) applies each run's sections with their own opts, and `git hash-object` (no -w) of each
    result must equal the TARGET blob — the head, except #1059 whose target is its first commit 8a1bdf1df (commits 2 and 3 are the seat's: titles,
    generator output; their shape is asserted separately). #1056's --recount is CONTROLLED: a strict apply must succeed and give a DIFFERENT blob;
  * the ALL-ELEVEN TREE is re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, CONTROLLED by re-deriving each of the
    eleven head trees from develop the same way; it must equal the builder's cb7860d61 and the tree of its local predict commit 23c379dcd.
Usage: gen_launcher_batch1050_1060.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1050_1060', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '59412d0575dff3243f5f0ccd1e50608ddb920d6c'   # develop at 21:59:10Z; every PR's merge-base
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; N = D + 'services/anchoring/'; T = 'Blockchain/Testing/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4699a68d-11eb-47c2-969d-81b79ab45768/scratchpad'
# n, ticket, branch, head, ahead, file count, head tree
PRS = [
 (1050, 'KS-1261', 'feature/ks-1261-preflight-failed_legs-fail_total-are-never-initialised-so-an', '6f6c6ed306f35aea0ca4f1e51fb785d8b1cf77b8', 1, 2, 'a84e8df579bae96c135a043b858c9492f4f54d85'),
 (1051, 'KS-1136', 'feature/ks-1136-audit-jobs-a-per-image-trivy-failure-reads-as-a-clean-image', '58e2fb66bd5ed5138f700cd58433e82e25ba9b82', 1, 2, '137cc4ff4f110f5004f9158f7cd1ddd855790aa5'),
 (1052, 'KS-1267', 'feature/ks-1267-ks-1228-two-row-placements-are-unpinned-versions-row-after', 'cd791b8214999427b645364e666ca215dc4e7c39', 1, 1, '454a870ee7fd50f7d869fad467cf2863ceb100a9'),
 (1053, 'KS-1258', 'feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n44-1', 'baf651460a46dff3c5bd52e19ab3f64e681ab6df', 1, 1, '5902a257a390adea80f756ab1649817d334513c0'),
 (1054, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n45-5', '1ea5c7b7eb955d146d935447572e28d8f48a12cf', 1, 1, '544f6dd76e68f2bf4b92e8d6613aea358b24bf9f'),
 (1055, 'KS-1202', 'feature/ks-1202-the-served-document-type-comes-from-datadocumenttype-which-n-b', '31d55923d35669959413aba8e533661282608e18', 1, 1, '08b3b219b4cb0819cd7ac6058d8b408c8ee70e7c'),
 (1056, 'KS-1153', 'feature/ks-1153-l7-gate-records-918924925-run-code-guardssh-check-unreached', '7eb4dbad51958c0c814a77e3263b54a84b1d0edc', 1, 1, 'd9a1c04a23546e44d6eae14f5e51cc76411d59e7'),
 (1057, 'KS-1209', 'feature/ks-1209-preflights-closing-verdict-says-a-run-failed-on-the-n41-3', 'b3b90db4d19818ed580cbc98a199a5f145e7f064', 1, 1, '72fcf4a478b706ef3acaf81fb9883dc212edad4d'),
 (1058, 'KS-1134', 'feature/ks-1134-orchestrate_jobs-cell-1415-cannot-tell-the-ks-922-fix-from-a', '2e212047d66d15ca8551e8fdd9d4ea772d5ab085', 1, 1, '7fabec16e7a1c4b92e135ec76fcc817263b0f35d'),
 (1059, 'KS-1172+KS-1173', 'feature/ks-1172-add-note-and-verified-to-the-lifecycle-vocabulary', 'f22ec785ea0dcc620e0e4bf53987a0da7a03e104', 3, 6, '93c05c6407dcbc11d4f789f9463b98189e044006'),
 (1060, 'KS-1264', 'feature/ks-1264-revoke-records-its-action_provenance-row-before', '3743e57eac6050056df87cbfc8724ae642d1ff6c', 1, 2, '841f00564a5aa1f5627d94496be17f7cf6604dfa'),
]
C1059 = ['8a1bdf1df4813dd49b9ea10f8775a196e530d1e8', '1a3e27ee583d1e8abe45a436e0bafe21f67bdf1d', 'f22ec785ea0dcc620e0e4bf53987a0da7a03e104']
COMBINED = 'cb7860d61b27cc41aa5865d850f2424884d1b8e0'   # builder's predicted all-eleven tree (READY 21:56:17Z); re-derived below
BUILDER_PREDICT_COMMIT = '23c379dcd'                    # builder's local-only predict commit; its tree must be COMBINED
# canonical patches: n -> (target commit, [(diff, opts, strict_control_must_differ)])
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
 1050: ('head', [('2026-09-18_ks1261-ornith35b-night', 'section_1.diff'), ('2026-09-18_ks1261-ornith35b-night', 'section_2.diff')]),
 1051: ('head', [('2026-09-18_ks1136-ornith35b-night2', 'section_1.diff'), ('2026-09-18_ks1136-ornith35b-night2', 'section_2.diff')]),
 1052: ('head', [('2026-09-18_ks1267-ornith35b-night', 'patch.diff')]),
 1053: ('head', [('2026-09-18_ks1258-ornith35b-night2', 'patch.diff')]),
 1054: ('head', [('2026-09-18_ks1230-ornith35b-night2', 'patch.diff')]),
 1055: ('head', [('2026-09-18_ks1202-ornith35b-night', 'patch.diff')]),
 1056: ('head', [('2026-09-18_ks1153-ornith35b-night2', 'patch.diff')]),
 1057: ('head', [('2026-09-18_ks1209-ornith35b-night2', 'patch.diff')]),
 1058: ('head', [('2026-09-18_ks1134-ornith35b-night', 'patch.diff')]),
 1059: (C1059[0], [('2026-09-15_ks1172-ornith35b-night9', 'section_1.diff'), ('2026-09-15_ks1172-ornith35b-night9', 'section_2.diff'),
                  ('2026-09-15_ks1172-ornith35b-night10', 'section_1.diff'), ('2026-09-15_ks1172-ornith35b-night10', 'section_2.diff'),
                  ('2026-09-15_ks1172-ornith35b-night11', 'patch.reanchored.diff')]),
 1060: ('head', [('2026-09-19_ks1264-ornith35b-night', 'section_1.diff'), ('2026-09-19_ks1264-ornith35b-night', 'section_2.diff')]),
}
FORCED_OPTS = {1056: ['--recount']}   # the READY header's rule; controlled below (strict must differ)

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 D + 'scripts/preflight/preflight.sh': 'f24fa96316b64f1b06b6a78835f4385fcd753e7b',
 T + 'jobs/04-container-trivy.sh': '4312a79f5292ed3a4cab07e0486dd2fd1dbe4763',
 O + 'src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts': '0b9be16318b97d1a214afcfdd5a1c0483c27904e',
 A + 'src/__tests__/ks1258-degraded-optional-service-advice.test.ts': '9143365cb4571906f6d0c2df13db430645447c72',
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': 'dd5ce85644dde844833989ad482288bf855e3d23',
 O + 'src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts': 'ada07f0536ad003754cb2a08f514fc04f8996b27',
 D + 'scripts/__tests__/run_code_guards.test.sh': '55a376f769e078ceeeadc25d026364c0e06961b1',
 D + 'scripts/__tests__/preflight_verdict_names_real_failures.test.sh': 'a3d5efe68e350710e2bde8b01c21b298dcca446f',
 D + 'scripts/__tests__/orchestrate_jobs.test.sh': 'a9abe5bcefd0969e79f07ba186f3f6647f88fadc',
 D + 'docs/VOCABULARY.md': '482544b9dc7dda652b5e7ac0452c35c8c035359f',
 D + 'docs/openapi/secuura-api.yaml': '16ac8aa78463849864fa6285e20c9946c027fb7b',
 N + 'src/__tests__/anchorSchema.test.ts': 'ff85c737628b8fc20e3b1faad6adfcc92c8dfd06',
 N + 'src/anchorSchema.ts': '67ae9d907f4e8a0ad405067af82c6b7308075f1b',
 O + 'src/__tests__/lifecycleEventRepo.test.ts': '4e53a82966d82da0b29eddd49eb101575c387347',
 O + 'src/lifecycleActions.ts': '4ac5ad58a22b565d267512b734b09b9bf1b1d844',
 O + 'src/routes/documents.ts': 'b5e76dc61ae5d4da8667b466b0a1dcf79d5a0498',
 '.githooks/pre-push': '1b22d4e146487aa25698310b353152a7d09986b5',
 D + 'scripts/run-shell-suites.sh': 'bf766bb54828cf6abad817f0f21a0c2f674d783f',
 D + 'scripts/run-code-guards.sh': '2f06e19d3d33d649d7229e44ade8a35c0df3a0db',
 T + 'jobs/09-aggregate-report.sh': '739ebab8c64e5f9195bc2280e38b4cc5fea0e023',
 T + 'ci/orchestrate.sh': '65247243f7585951ada3e5dfa8a9af88189ee5b1',
 T + 'ci/aggregate.ts': 'b841f02572247da7a1d0a29f69f9c3231636991c',
 D + 'scripts/generate-openapi.ts': 'e84acdc9e1be073751fcd6a8bb95504e23688019',
 O + 'src/originate.openapi.ts': '2d1b48a0c7ea93521d553cc28ccb53b4fe3fd19c',
 N + 'src/anchoring.openapi.ts': '29c089bb0abcd65d42fe8fca2d6beaff0368fa98',
 O + 'src/routes/certifications.ts': '02dcbe6294b497eab093f11a8fc6c9e275be91c5',
 O + 'src/services/provenance.ts': '483aa9eb331d2caa5af285e20d9668a9dbcd92a6',
 A + 'src/routes/system-status.ts': 'e911ce1fdaa4b755e9b7b6428f899cdbd63889cb',
 A + 'src/routes/admin.ts': '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 O + 'package.json': 'd4435238d3ece7f7da42f043f56ca7739a611132',
 O + 'jest.config.js': '735183662feea56d39f664eb6379cae1a2eec957',
 O + 'tsconfig.json': 'd1b46ece71ad5b2559ccad3648c23a5231e43b09',
 N + 'package.json': 'a7eed73550b40aa2d968872817fa22e933373831',
 N + 'package-lock.json': '7ef3f65a35b48bec2591df4b2859bab9aa237334',
 N + 'vitest.config.ts': '2e1d21f130f8aa80a1c71987f920181dafaf6b90',
 N + 'tsconfig.json': 'f593300cac7c9c3073f15a1287323cf5b9dd478d',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
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
    if n == 1059: ok = ok and chain == C1059[::-1]
    print('#%d %-16s head %s ahead %d parents %s base=develop %s files %d tree %s  %s' % (n, t, h[:9], len(chain), npars, base_ok, len(files), rp(h + '^{tree}')[:9], 'OK' if ok else 'BAD'))
    if not ok: bad.append(('PR shape', n, files, chain))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 19: bad.append(('eleven PRs not pairwise file-disjoint / not 19 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
# #1059 commits 2 and 3: titles only; yaml only
c2 = git('diff', '--numstat', C1059[0], C1059[1]).stdout.split('\n')
c2 = [l.split('\t') for l in c2 if l]
c2ok = sorted(x[2] for x in c2) == sorted([N + 'src/__tests__/anchorSchema.test.ts', O + 'src/__tests__/lifecycleEventRepo.test.ts']) and all(x[0] == x[1] == '1' for x in c2)
c2body = git('diff', '-U0', C1059[0], C1059[1]).stdout
c2plus = [l for l in c2body.splitlines() if l.startswith('+') and not l.startswith('+++')]
c2ok = c2ok and len(c2plus) == 2 and all("it('" in l and 'KS-1172/KS-1173' in l for l in c2plus)
c3 = [l.split('\t') for l in git('diff', '--numstat', C1059[1], C1059[2]).stdout.split('\n') if l]
c3plus = ['+' + l[1:].strip() for l in git('diff', '-U0', C1059[1], C1059[2]).stdout.splitlines() if l.startswith('+') and not l.startswith('+++')]
c3ok = [x[2] for x in c3] == [D + 'docs/openapi/secuura-api.yaml'] and c3[0][:2] == ['6', '0'] and sorted(c3plus) == sorted(['+- note', '+- certified', '+- verified'] * 2)
print('#1059 commit 2 (titles only, 2 x it() lines naming KS-1172/KS-1173):', c2ok, '| commit 3 (yaml only, +6: note/certified/verified x2):', c3ok)
if not (c2ok and c3ok): bad.append(('#1059 commit shape', c2ok, c3ok))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1050-', dir=SCRATCH)
def apply_into(W, n, target, force_opts=None):
    files = git('diff', '--name-only', DEV, target).stdout.splitlines()
    for f in files:
        if git('cat-file', '-e', DEV + ':' + f).returncode == 0:
            os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
            open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    for run, name in CANON[n][1]:
        o = opts_of(run, name)
        o = (o or []) if force_opts is None else force_opts
        r = subprocess.run(['git', 'apply', *o, sec(run, name)], cwd=W, capture_output=True, text=True)
        print('  #%d %s/%s git apply %s rc %d %s' % (n, run.split('_')[1], name, ' '.join(o) or '(strict)', r.returncode, r.stderr.strip()[:120]))
        if r.returncode: return None, files
    return {f: subprocess.run(['git', 'hash-object', os.path.join(W, f)], capture_output=True, text=True).stdout.strip() for f in files}, files
for n, t, br, h, *_ in PRS:
    target = h if CANON[n][0] == 'head' else CANON[n][0]
    W = os.path.join(X, 'p%d' % n); os.makedirs(W)
    got, files = apply_into(W, n, target, FORCED_OPTS.get(n))
    if got is None: bad.append(('canonical apply', n)); continue
    for f in files:
        want = rp(target + ':' + f)
        print('  #%d canonical %s -> %s == %s %s: %s' % (n, f.split('/')[-1], got[f][:9], 'head' if target == h else target[:9], want[:9], got[f] == want))
        if got[f] != want: bad.append(('canonical patch != PR', n, f))
    if n in FORCED_OPTS:   # control: the strict apply must succeed and give a DIFFERENT blob
        W2 = os.path.join(X, 'p%d-strict' % n); os.makedirs(W2)
        g2, _ = apply_into(W2, n, target, [])
        diff = g2 is not None and any(g2[f] != rp(target + ':' + f) for f in files)
        print('  #%d CONTROL strict apply succeeded and differs from the head: %s' % (n, diff))
        if not diff: bad.append(('recount control', n))
print('scratch (plain files, not a repo; left in place):', X)

# 4. the all-eleven tree by pure tree hashing (read-only cat-file), controlled by each single head tree
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
print('ALL ELEVEN over develop -> %s | builder predicted %s: %s | builder predict commit %s tree %s: %s' % (comb, COMBINED[:9], comb == COMBINED, BUILDER_PREDICT_COMMIT, bt[:9], bt == COMBINED))
if comb != COMBINED or bt != COMBINED: bad.append(('combined tree', comb, bt))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md'
PROMPT = WEDB + 'briefs/2026-09-19_secuura-batch1050-1060.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-batch1042-1045-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1050-#1060 (eleven PRs; tier 1 = #1059 KS-1172+KS-1173, #1060 KS-1264)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-2nd/'
assert os.path.isdir(PRIOR) and os.path.isdir(SEATHIST), 'prior report or seat history dir missing'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h[:9] in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head'
assert 'MESSAGE_ID: <010001a0b6853164-' in mt_ and 'TS: 2026-09-18T21:56:17' in mt_, 'mail capture is not the 21:56:17Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED[:9] in mt_ and COMBINED in pt_ and BUILDER_PREDICT_COMMIT in pt_, 'combined tree not named in mail AND prompt'

HEADER_OLD = cut('# launch_qa_secuura_batch1042_1045.sh', '# Exit: 0 launched (or guards passed under --check) · 2..30 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1050_1060.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over ELEVEN file-disjoint Secuura/Blockchain PRs
#   #1050 KS-1261 @ 6f6c6ed30  preflight.sh: FAILED_LEGS / fail_total initialised (the pre-push gate everyone runs) + new suite  — TIER 2 (runtime)
#   #1051 KS-1136 @ 58e2fb66b  Testing/jobs/04-container-trivy.sh: a failed per-image scan is scan-failed and exits 1 + suite  — TIER 2 (runtime)
#   #1052 KS-1267 @ cd791b821  ks1228 jest test: Q1, /version row after saveDocument                                         — TIER 2 (test-only)
#   #1053 KS-1258 @ baf651460  ks1258 vitest test: N44-1, no start command in any shape                                      — TIER 2 (test-only)
#   #1054 KS-1230 @ 1ea5c7b7e  ks1230 vitest test: N45-5, a null allow-list stores 200                                       — TIER 2 (test-only)
#   #1055 KS-1202 @ 31d55923d  ks1202 jest test: N-B, legacy matching shape + case-exact documentType                         — TIER 2 (test-only)
#   #1056 KS-1153 @ 7eb4dbad5  run_code_guards.test.sh: R-918-A, the advisory-skip arm (applied --recount)                   — TIER 2 (test-only)
#   #1057 KS-1209 @ b3b90db4d  preflight_verdict_names_real_failures.test.sh: N41-3, a real leg-1 failure is named           — TIER 2 (test-only)
#   #1058 KS-1134 @ 2e212047d  orchestrate_jobs.test.sh: zero Stage-1 jobs reach the JOIN                                    — TIER 2 (test-only)
#   #1059 KS-1172+KS-1173 @ f22ec785e  note / certified / verified in the anchored lifecycle vocabulary + yaml (3 commits)     — TIER 1 (sets the floor)
#   #1060 KS-1264 @ 3743e57ea  documents.ts /revoke: record the provenance row only after updateDocument                     — TIER 1
# Batched under Kam's 09:22 rule. ELEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 07:59:10 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: ten PRs are ONE commit
# whose parent IS develop 59412d057; #1059 is THREE (8a1bdf1df verbatim / 1a3e27ee5 titles / f22ec785e yaml); compare develop...head = merge_base
# 59412d057, ahead 1 (x10) / 3, files 2/2/1/1/1/1/1/1/1/6/2 (asserted per PR, exit 10). Pairwise file-disjoint (19 files). Each PR over develop is a
# fast-forward (merged tree = head tree). ALL ELEVEN = tree cb7860d61, re-derived by the generator by pure tree hashing (no git write), equal to the
# builder's prediction and to its local predict commit 23c379dcd's tree. All eleven are byte-identical to their CANONICAL local-model patches
# (#1059 at 8a1bdf1df), re-applied by the generator in a plain scratch dir; #1056's --recount controlled (a strict apply gives another blob).
#
# The develop pin is judged by CONTENT — FORTY-FIVE paths by blob at the CURRENT develop: the nineteen PR files (sixteen at develop blobs, three new
# files ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: the pre-push hook, run-shell-suites.sh,
# run-code-guards.sh, jobs/09 + ci/orchestrate.sh + ci/aggregate.ts, generate-openapi.ts, both openapi sources, certifications.ts, provenance.ts,
# system-status.ts, admin.ts, the originate / anchoring / api-gateway configs, the Dev package.json + lock, eslint.config.mjs and BACKLOG.md.
# GUARDED: scripts/, Testing/jobs/ + ci/, docs/, api-gateway / originate / anchoring src/ + config, the Dev package.json + lock, eslint.config.mjs,
# .githooks/, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md, the seat's READY mail (21:56:17Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the eleven heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all eleven heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and ELEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1042-#1045 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'Legs 3/4/8 were skipped', 'login_stub' and 'threadTokenMint'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-2nd history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's G1 / G2 / G3 (documents.ts:2327, :2051, 09-aggregate-report), and the prompt must
#          ask the gate to MEASURE, not conclude.
# exit 31: the prompt must name the all-eleven tree in full, the predict commit, the NOT-PINNED list, and pin preflight's GATEWAY_URL to loopback.
# QAB1050_CUR_DEV (test override, --check only): stands in for origin develop. QAB1050_HEAD_1060 (test override): stands in for #1060's pinned head.
# QAB1050_DOCS_FILE (test fixture, --check only): a local file stands in for develop services/originate/src/routes/documents.ts (its git blob).
# A launch with any QAB1050_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1050to1060/gen_launcher_batch1050_1060.py from launch_qa_secuura_batch1042_1045.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-eleven tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1050_1060.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..31 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != 1060 else '${QAB1050_HEAD_1060:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1042_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1042to1045/mail_batch1042_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1050_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1050_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (21:56:17Z) and re-read by the drafter (git ls-remote 07:59:10 AEST, branch AND refs/pull/N/head)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 07:59:10 AEST; every head's merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADCHK_OLD = cut('# The four heads, each pinned at its branch AND at refs/pull/N/head', 'HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"\ndone\n')
HEADCHK_NEW = HEADCHK_OLD.replace('# The four heads, each pinned', '# The eleven heads, each pinned', 1)
assert HEADCHK_NEW != HEADCHK_OLD
CMPC_OLD = cut('# develop...#1042 = 8b9c3f022', '(git diff --name-only, drafter 15:5x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = 59412d057 ahead 1 for ten PRs, ahead 3 for #1059; files #1050 2, #1051 2, #1052-#1058 1 each, #1059 6, #1060 2\n'
            '# (git diff --name-only + rev-list, drafter 07:5x AEST; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1042 $MERGE_BASE', '1045 $MERGE_BASE ahead=1 files=2"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): thirty-one paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): forty-five paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (O, 'O'), (N, 'N'), (T, 'T'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN) + NEWFILES
assert len(JPATHS) == 45, ('judged path count', len(JPATHS))
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p] if p in DEVPIN else '{"ABSENT": DV}'
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k = 'DOCSTS' if p == O + 'src/routes/documents.ts' else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k, ' ' * max(1, 80 - len(k)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\nO = D + "services/originate/"\nN = D + "services/anchoring/"\nT = "Blockchain/Testing/"\n'
              'DOCSTS = O + "src/routes/documents.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all eleven heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr[:9]) for n, _, _, _, _, _, tr in PRS) + '; all eleven together ' + COMBINED + ', drafter tree-hash = builder prediction; git ls-remote)"); sys.exit(0)\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = ('GUARDED = [A + "src/",\n'
             '           A + "package.json",\n'
             '           A + "vitest.config.ts",\n'
             '           O + "src/",\n'
             '           O + "package.json",\n'
             '           O + "jest.config.js",\n'
             '           O + "tsconfig.json",\n'
             '           N + "src/",\n'
             '           N + "package.json",\n'
             '           N + "package-lock.json",\n'
             '           N + "vitest.config.ts",\n'
             '           N + "tsconfig.json",\n'
             '           D + "scripts/",\n'
             '           D + "docs/",\n'
             '           T + "jobs/",\n'
             '           T + "ci/",\n'
             '           D + "package.json",\n'
             '           D + "package-lock.json",\n'
             '           D + "eslint.config.mjs",\n'
             '           ".githooks/",\n'
             '           "BACKLOG.md"]\n'
             '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a\n'
             '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.\n'
             '# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.\n'
             'DEV_CONTENT_ALLOWED = {}\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the four heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the eleven heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all eleven '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway, originate and anchoring src/ + config, scripts/, docs/, Testing jobs/ + ci/, '
               'the Dev package.json + lock, eslint.config.mjs, .githooks/, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, t, 1 if n in (1059, 1060) else 2) for n, t, *_ in PRS]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", '>&2; exit 30; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1050-#1058 T2, #1059 T1, #1060 T1)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'ELEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and ELEVEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'Legs 3/4/8 were skipped' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'threadTokenMint' "$PROMPT_FILE" \
  && grep -qF 'Legs 3/4/8 were skipped' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'threadTokenMint' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: Legs 3/4/8 were skipped / login_stub / threadTokenMint" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-2nd history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'documents.ts:2327' "$PROMPT_FILE" && grep -qF ':2051' "$PROMPT_FILE" && grep -qF '09-aggregate-report' "$PROMPT_FILE" && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" \
  && grep -qF 'documents.ts:2327' "$BRIEF" && grep -qF ':2051' "$BRIEF" && grep -qF '09-aggregate-report' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry G1 / G2 / G3, or the prompt does not say MEASURE, not conclude" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF '__PREDICT__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-eleven tree in full, the predict commit, the NOT-PINNED list, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED).replace('__PREDICT__', BUILDER_PREDICT_COMMIT)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  eleven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1050-#1058 T2, #1059 T1, #1060 T1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all eleven heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, ELEVEN verdict lines"
  echo "  prompt names the report directory, the #1042-#1045 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: Legs 3/4/8 were skipped / login_stub / threadTokenMint"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-2nd history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry G1 / G2 / G3; the prompt says MEASURE, not conclude"
  echo "  prompt names the all-eleven tree, the predict commit, the NOT-PINNED list and a loopback GATEWAY_URL for preflight"
  [ -n "${QAB1050_CUR_DEV:-}" ] && echo "  (develop read from the QAB1050_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1050_DOCS_FILE:-}" ] && echo "  (develop services/originate/src/routes/documents.ts read from the QAB1050_DOCS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('head check', HEADCHK_OLD, HEADCHK_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1042_CUR_DEV:-', 'CUR_DEV="${QAB1050_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1042_ADMIN_FILE", "") if f == ADMINTS else ""\n',
                 '    fixture = os.environ.get("QAB1050_DOCS_FILE", "") if f == DOCSTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1042_BRIEF:-}${QAB1042_PROMPT:-}${QAB1042_HEAD_1045:-}${QAB1042_CUR_DEV:-}${QAB1042_ADMIN_FILE:-}" ]',
            '[ -z "${QAB1050_BRIEF:-}${QAB1050_PROMPT:-}${QAB1050_HEAD_1060:-}${QAB1050_CUR_DEV:-}${QAB1050_DOCS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1042-1045 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1042-#1045 batch': 2, 'from launch_qa_secuura_batch1042_1045.sh': 1}   # exit 24 comment + --check line; the template
for k, v in INTENDED.items():
    assert BODY.count(k) == v, ('intended citation count', k, BODY.count(k), v)
    BODY = BODY.replace(k, '<CITED>')
RESID = ['QAB1042_', 'ADMINTS', 'ADMIN_FILE', 'mail_batch1042', 'gate1042to1045', 'batch1042', 'KS-1254', 'KS-1228 ', '2ad066ae2', '8d42bb016',
         'a21691fa4', '63ecb0930', '8b9c3f022', '816d53a2b', '93c99760a', 'seatA-11th', 'TS2708', 'checker.sh:921', 'NODE_ENV', 'FOUR', 'four heads',
         'all four', 'thirty-one', 'THIRTY-ONE', 'Settings.tsx', 's-a11', 'legs 3/4/8 skipped', 'packages/shared']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])104(2|3|4|5)(?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 2,   # OKPIN + the exit-31 guard
        REPORT_DIR: 1, PRIOR: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT": DV': 3, 'QAB1050_CUR_DEV': 5, 'QAB1050_DOCS_FILE': 5,
       'QAB1050_HEAD_1060': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-19_secuura-batch1050-1060.prompt.txt': 1, 'gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md': None,
       '"BACKLOG.md"]': 1, 'O + "src/",': 1, 'N + "src/",': 1, 'D + "scripts/",': 1, 'T + "jobs/",': 1, '".githooks/",': 1,
       'ahead=3 files=6': 1, 'ahead=1 files=': 10}
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
