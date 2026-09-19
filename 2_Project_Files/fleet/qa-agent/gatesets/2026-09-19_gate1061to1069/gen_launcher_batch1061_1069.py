#!/usr/bin/env python3
"""gen_launcher_batch1061_1069.py — derive launchers/launch_qa_secuura_batch1061_1069.sh from launchers/launch_qa_secuura_batch1050_1060.sh (the
batch gate that ran clean on 2026-09-19 08:18, one gate / eleven verdicts) by ASSERTED block substitutions: every anchor must occur exactly as often
as stated, or the generator refuses and writes nothing. Structure copied from gatesets/2026-09-19_gate1050to1060/gen_launcher_batch1050_1060.py;
the data changed.

ONE BATCHED gate, TIER 1 floor (set by #1061 KS-1206 and #1062 KS-1260), NINE PRs #1061..#1069 (Seat B 3rd, READY 2026-09-19 01:39:55Z).
NAMESPACE TRAP: PR #1062 is KS-1260 and PR #1067 is KS-1062.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (git rev-parse / cat-file / diff --name-only / rev-list): each PR is ONE commit whose parent IS develop; every PR's file set and
    head tree as pinned; every judged develop blob and every landed head blob as pinned; the nine pairwise file-disjoint (11 files, 5 new);
  * CANONICAL-PATCH identity for ALL NINE (every one is a local-model patch): develop's blobs are written as plain files into a fresh scratch dir
    (not a repo), `git apply` (patch mode, cwd = that dir) applies each run's sections with their own opts, and `git hash-object` (no -w) of each
    result must equal the head blob;
  * the ALL-NINE TREE is re-derived by pure tree-object hashing in Python from `git cat-file tree` reads, CONTROLLED by re-deriving each of the
    nine head trees from develop the same way; it must equal the builder's 275cff9ff and the tree of its local octopus commit 77b7af584. (The
    drafter ALSO predicted it by merge-tree chains in a --shared scratch clone: predict_all_nine_scratch.sh / .out beside this file.)
Usage: gen_launcher_batch1061_1069.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1061_1069', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '3c447abc7714e98fbba596aa1045b7bb47a6d215'   # develop at 01:42:47Z (#1050-#1060 merged); every PR's merge-base
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; S = D + 'services/security/'; ST = 'systemTest/schemathesis/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad'
# n, ticket, branch, head, ahead, file count, head tree
PRS = [
 (1061, 'KS-1206', 'feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an', '413cc5e80c8aab94c9b3058fbe0d49fbcfdaa540', 1, 2, '40cce41acc30f46ce9ddd4d124f181feb1747042'),
 (1062, 'KS-1260', 'feature/ks-1260-preflight-failure-verdict-keeps-the-ratio', 'b9497c69837d33d3c56562abfb9f9ac5c0dafa2b', 1, 2, 'b8571562e14c43e78ed383036d8ec5b9d368d0ca'),
 (1063, 'KS-1101', 'feature/ks-1101-gateway-health-aggregates-read-anchorings-http-status-only-n-3', 'cd0a88e41ada8ddd927c3dc85f8270b52142f834', 1, 1, '9b842f84cbeb27219b33ea8f8f439d1bb373bc98'),
 (1064, 'KS-864', 'feature/ks-864-dead-estate-pointers-in-runtime-source-outside-r-1', '7fd0f7d1e560d85c789872eac96067b428215ed5', 1, 1, 'd03d08e1abf5c41266820c7b84a03a65acdc66dc'),
 (1065, 'KS-991', 'feature/pin-pre-push-hook-current-develop-not-stale', '3b46e2e14a2783bfe03df8919ca79d2dea21c043', 1, 1, 'edfd6317a7b3695b91dda23960b4079dbe1173fd'),
 (1066, 'KS-739', 'feature/pin-transfer-custody-nonjson-403-stays-403', '0c649c09bca81ccb41ba791bb2a85ba29476c052', 1, 1, '3608b08d150dde0c8e25ecd2bb45c926892c8dd2'),
 (1067, 'KS-1062', 'feature/pin-startup-migrations-tenant-summary-first-error', '48a8e12bbb6b01d34bea55ab29936b033f8304b3', 1, 1, '2930849c59e0402d488adc061ed76e8456f201e7'),
 (1068, 'KS-1258', 'feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n53-1', '9af88d99dbc0203a69cb765c67dee10df900e737', 1, 1, '9a10fc667c8f288ea460c234241c3aadfc20b10e'),
 (1069, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors-n54-1', '34406a29babe355a7ea8ecd916062da5b2fa8f85', 1, 1, 'ed4f0411a2b545aba4b22d22702d993a3a69adde'),
]
COMBINED = '275cff9ffcb1a8204db499506f08db54ee39f4eb'   # builder's predicted all-nine tree (READY 01:39:55Z); re-derived below
BUILDER_PREDICT_COMMIT = '77b7af584'                    # builder's local-only octopus commit; its tree must be COMBINED
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
CANON = {
 1061: ('head', [('2026-09-19_ks1206-ornith35b-night', 'section_1.diff'), ('2026-09-19_ks1206-ornith35b-night', 'section_2.diff')]),
 1062: ('head', [('2026-09-19_ks1260-ornith35b-night', 'section_1.diff'), ('2026-09-19_ks1260-ornith35b-night', 'section_2.diff')]),
 1063: ('head', [('2026-09-19_ks1101-ornith35b-night', 'patch.diff')]),
 1064: ('head', [('2026-09-19_ks864-ornith35b-night', 'patch.diff')]),
 1065: ('head', [('2026-09-19_ks991-ornith35b-night', 'patch.diff')]),
 1066: ('head', [('2026-09-19_ks739-ornith35b-night2', 'patch.diff')]),
 1067: ('head', [('2026-09-19_ks1062-ornith35b-night', 'patch.diff')]),
 1068: ('head', [('2026-09-19_ks1258-ornith35b-night', 'patch.diff')]),
 1069: ('head', [('2026-09-19_ks1230-ornith35b-night', 'patch.diff')]),
}
WANT_OPTS = {1061: ['--directory=Blockchain/Dev']}   # the READY header's rule; every other section applies strict (asserted below)
FORCED_OPTS = {}

def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 O + 'src/routes/adminConfig.ts': '26cec03de665ef75a8f6e4f2532dfc42a59a25b8',
 D + 'scripts/preflight/preflight.sh': '539493d9d94942189e85953512d6f3981bd9c5d4',
 A + 'src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts': 'e03f600d51d441ca42aff15d92e8391bcc66e2cb',
 O + 'src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts': '1b0eb5dd81839dd6e402ff4e6fa87b0b24877885',
 A + 'src/__tests__/ks1258-degraded-optional-service-advice.test.ts': 'fe456997603256f1036499a8a8f33949f43631bf',
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': '26af52344bcdbc5de5ba592e97fabc2608718738',
 '.githooks/pre-push': '1b22d4e146487aa25698310b353152a7d09986b5',
 D + 'scripts/run-shell-suites.sh': 'bf766bb54828cf6abad817f0f21a0c2f674d783f',
 D + 'scripts/__tests__/preflight_state_is_initialised.test.sh': 'ee31ee5f5bc3f0e4939df9587e346296b8ea494c',
 D + 'scripts/__tests__/preflight_verdict_names_real_failures.test.sh': 'fb762f6389a0700afcab456fc275062cace05520',
 D + 'scripts/__tests__/pre_push_hook_base.test.sh': 'affdf027bff11e3690d374e902e3e93274788c62',
 D + 'scripts/__tests__/preflight_deps.test.sh': '5ad0541313589635c6c100677cf14fb02d00be78',
 D + 'scripts/__tests__/check_slot_credentials.test.sh': '5ea337e2c7b92bcc92bb99cea4d229fb354d0358',
 D + 'scripts/__tests__/no_tracked_credentials_root.test.sh': 'b4e622e3a7c605ff050cec14e40d9f1fccd030cc',
 A + 'src/routes/system-status.ts': 'e911ce1fdaa4b755e9b7b6428f899cdbd63889cb',
 A + 'src/routes/admin.ts': '20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3',
 A + 'src/startup-migrations.ts': 'ed3e521426e75910c5bf2cf07e7251f2fd8ef538',
 O + 'src/routes/documents.ts': '3f837fc6e656d5a10f9cc349b1cb2a876a2be09b',
 S + 'src/index.ts': '0903ce4380f219765ac63f5f9399d1bf0b4f230a',
 ST + 'scripts/setup_api_key.py': '8779ff2210d6c2e04aea09e9b66144aa26130309',
 ST + 'tests/test_tenant_isolation_writes.py': '0365de3858588226930092aa5eae64444f86ecbe',
 O + 'package.json': 'd4435238d3ece7f7da42f043f56ca7739a611132',
 O + 'jest.config.js': '735183662feea56d39f664eb6379cae1a2eec957',
 O + 'tsconfig.json': 'd1b46ece71ad5b2559ccad3648c23a5231e43b09',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
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
if len(NEWFILES) != 5: bad.append(('want 5 new files', NEWFILES))

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
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 11: bad.append(('nine PRs not pairwise file-disjoint / not 11 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
# namespace trap, asserted from the commit subjects: PR #1062 carries KS-1260, PR #1067 carries KS-1062
subj = {n: git('log', '-1', '--format=%s%n%b', h).stdout for n, _, _, h, *_ in PRS}
trap = 'KS-1260' in subj[1062] and 'KS-1062' not in subj[1062] and 'KS-1260' not in subj[1067]
print('namespace trap (#1062 commit names KS-1260 and not KS-1062; #1067 commit does not name KS-1260):', trap)
if not trap: bad.append(('namespace trap', subj[1062][:80], subj[1067][:80]))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1061-', dir=SCRATCH)
def apply_into(W, n, target, force_opts=None):
    files = git('diff', '--name-only', DEV, target).stdout.splitlines()
    for f in files:
        if git('cat-file', '-e', DEV + ':' + f).returncode == 0:
            os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
            open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    for run, name in CANON[n][1]:
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
        print('  #%d canonical %s -> %s == head %s: %s' % (n, f.split('/')[-1], got[f][:9], want[:9], got[f] == want))
        if got[f] != want: bad.append(('canonical patch != PR', n, f))
# control: #1061's --directory is load-bearing — section_1 applied WITHOUT it onto the same develop blobs must refuse (its paths are service-relative)
Wc = os.path.join(X, 'control-1061-nodir'); os.makedirs(Wc)
for f in git('diff', '--name-only', DEV, headof[1061]).stdout.splitlines():
    if git('cat-file', '-e', DEV + ':' + f).returncode == 0:
        os.makedirs(os.path.dirname(os.path.join(Wc, f)), exist_ok=True); open(os.path.join(Wc, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
r = subprocess.run(['git', 'apply', sec('2026-09-19_ks1206-ornith35b-night', 'section_1.diff')], cwd=Wc, capture_output=True, text=True)
print('  CONTROL #1061 section_1 WITHOUT --directory onto develop blobs refuses: rc %d (want non-zero) %s' % (r.returncode, r.stderr.strip()[:100]))
if r.returncode == 0: bad.append(('#1061 no-directory control applied',))
# control: a canonical patch into the WRONG file set refuses — #1068's patch into #1061's develop blobs
r = subprocess.run(['git', 'apply', sec('2026-09-19_ks1258-ornith35b-night', 'patch.diff')], cwd=Wc, capture_output=True, text=True)
print('  CONTROL crossed: #1068 patch into #1061 develop blobs refuses: rc %d (want non-zero)' % r.returncode)
if r.returncode == 0: bad.append(('crossed control applied',))
print('scratch (plain files, not a repo; left in place):', X)

# 4. the all-nine tree by pure tree hashing (read-only cat-file), controlled by each single head tree
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
print('ALL NINE over develop -> %s | builder predicted %s: %s | builder octopus commit %s tree %s: %s' % (comb, COMBINED[:9], comb == COMBINED, BUILDER_PREDICT_COMMIT, bt[:9], bt == COMBINED))
if comb != COMBINED or bt != COMBINED: bad.append(('combined tree', comb, bt))
scr = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'predict_all_nine_scratch.out')).read()
scr_ok = (re.search(r'forward: 9 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None
          and re.search(r'reverse: 9 merges -> commit \w+ tree ' + COMBINED + r'\n', scr) is not None and 'PREDICTION OK' in scr and 'rc=0' in scr)
print('scratch-clone prediction (predict_all_nine_scratch.out, forward + reverse merge-tree chains) names', COMBINED[:9], 'twice and PREDICTION OK:', scr_ok)
if not scr_ok: bad.append(('scratch prediction',))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md'
PROMPT = WEDB + 'briefs/2026-09-19_secuura-batch1061-1069.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1061-1069-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1061-#1069 (nine PRs; tier 1 = #1061 KS-1206, #1062 KS-1260)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-3rd/'
assert os.path.isdir(PRIOR) and os.path.isdir(SEATHIST), 'prior report or seat history dir missing'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h[:9] in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head'
assert 'MESSAGE_ID: <010001a0b751f095-' in mt_ and 'TS: 2026-09-19T01:39:55' in mt_, 'mail capture is not the 01:39:55Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'
assert COMBINED[:9] in mt_ and COMBINED in pt_ and BUILDER_PREDICT_COMMIT in pt_ and BUILDER_PREDICT_COMMIT in mt_, 'combined tree / octopus commit not named in mail AND prompt'
assert 'PR #1062 is KS-1260' in pt_ and 'PR #1067 is KS-1062' in pt_ and 'PR #1062 is KS-1260' in mt_ and 'PR #1067 is KS-1062' in mt_, 'namespace trap not named'

HEADER_OLD = cut('# launch_qa_secuura_batch1050_1060.sh', '# Exit: 0 launched (or guards passed under --check) · 2..31 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1061_1069.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over NINE file-disjoint Secuura/Blockchain PRs
#   #1061 KS-1206 @ 413cc5e80  adminConfig.ts: POST /api/admin/api-keys refuses rateLimit outside integer 1..10000 (null/0 -> 400) + test — TIER 1 (runtime)
#   #1062 KS-1260 @ b9497c698  preflight.sh: the early FAILED verdict keeps the legs-ran ratio (the pre-push gate) + new suite       — TIER 1 (runtime)
#   #1063 KS-1101 @ cd0a88e41  ks1101 vitest test: N-3, a degraded OPTIONAL service leaves /system/status operational          — TIER 2 (test-only)
#   #1064 KS-864  @ 7fd0f7d1e  NEW ks864d vitest test: R-1 row 17, an EMPTY portal env var falls back                           — TIER 2 (test-only)
#   #1065 KS-991  @ 3b46e2e14  NEW pre_push_hook_current_develop.test.sh: R-1, a CURRENT local develop is not called stale      — TIER 2 (test-only)
#   #1066 KS-739  @ 0c649c09b  ks739 jest test: F1, a non-JSON 403 still answers 403                                           — TIER 2 (test-only)
#   #1067 KS-1062 @ 48a8e12bb  NEW ks1062 vitest test: F-1, the tenant migration summary and the FIRST error                    — TIER 2 (test-only)
#   #1068 KS-1258 @ 9af88d99d  ks1258 vitest test: N53-1, no yarn / node start shape in the degraded optional advice             — TIER 2 (test-only)
#   #1069 KS-1230 @ 34406a29b  ks1230 vitest test: N54-1, a NULL allow-list is stored as null                                   — TIER 2 (test-only)
# NAMESPACE TRAP: PR #1062 is KS-1260 and PR #1067 is KS-1062 (exit 32).
# Batched under Kam's 09:22 rule. NINE verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 11:42:47 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop 3c447abc7; compare develop...head = merge_base 3c447abc7, ahead 1, files 2/2/1/1/1/1/1/1/1 (asserted per PR, exit 10).
# Pairwise file-disjoint (11 files, 5 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL NINE = tree 275cff9ff, re-derived by
# the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains, forward and reverse), equal to
# the builder's prediction and to its local octopus commit 77b7af584's tree. All nine are byte-identical to their CANONICAL local-model patches,
# re-applied by the generator in a plain scratch dir (#1061's sections with --directory=Blockchain/Dev, the rest strict).
#
# The develop pin is judged by CONTENT — THIRTY-SIX paths by blob at the CURRENT develop: the 11 PR files (six at develop blobs, five new files
# ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: the pre-push hook, run-shell-suites.sh, the six
# preflight sibling suites, system-status.ts, admin.ts, startup-migrations.ts, documents.ts, the security service index.ts, the two systemTest
# callers of the mint route, the originate / api-gateway configs, the Dev package.json + lock, eslint.config.mjs and BACKLOG.md.
# GUARDED: api-gateway / originate src/ + config, security src/, scripts/, systemTest/schemathesis/, the Dev package.json + lock, eslint.config.mjs,
# .githooks/, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md, the seat's READY mail (01:39:55Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the nine heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all nine heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and NINE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1050-#1060 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'Legs 3/4/8 need a stack', 'login_stub' and 'mergeable_state: unstable'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-3rd history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's G-1 / G-2 / G-3 / G-4 (security/src/index.ts:569, Nothing failed, NOJSONCATCH at
#          1695, matches at 576), and the prompt must ask the gate to MEASURE, not conclude, and to execute the FAILED path itself.
# exit 31: the prompt must name the all-nine tree in full, the octopus commit, the NOT-PINNED list, and pin preflight's GATEWAY_URL to loopback.
# exit 32: the READY mail AND the prompt must BOTH name the namespace trap: 'PR #1062 is KS-1260' and 'PR #1067 is KS-1062'.
# QAB1061_CUR_DEV (test override, --check only): stands in for origin develop. QAB1061_HEAD_1069 (test override): stands in for #1069's pinned head.
# QAB1061_ADMINCFG_FILE (test fixture, --check only): a local file stands in for develop services/originate/src/routes/adminConfig.ts (its git blob).
# A launch with any QAB1061_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1061to1069/gen_launcher_batch1061_1069.py from launch_qa_secuura_batch1050_1060.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-nine tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1061_1069.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != 1069 else '${QAB1061_HEAD_1069:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB1050_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1061_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1061_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (01:39:55Z) and re-read by the drafter (git ls-remote 11:42:47 AEST, branch AND refs/pull/N/head)\n'
            '# NAMESPACE TRAP: PR #1062 is KS-1260 and PR #1067 is KS-1062\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 11:42:47 AEST; every head's merge-base\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADCHK_OLD = cut('# The eleven heads, each pinned at its branch AND at refs/pull/N/head', 'HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"\ndone\n')
HEADCHK_NEW = HEADCHK_OLD.replace('# The eleven heads, each pinned', '# The nine heads, each pinned', 1)
assert HEADCHK_NEW != HEADCHK_OLD
CMPC_OLD = cut('# develop...head = 59412d057 ahead 1 for ten PRs', '(git diff --name-only + rev-list, drafter 07:5x AEST; the launcher reads the compare API).\n')
CMPC_NEW = ('# develop...head = 3c447abc7 ahead 1 for all nine PRs; files #1061 2, #1062 2, #1063-#1069 1 each\n'
            '# (git diff --name-only + rev-list, drafter 11:4x AEST; the launcher reads the compare API).\n')
WANT_OLD = cut('WANT_COMPARE="1050 $MERGE_BASE', '1060 $MERGE_BASE ahead=1 files=2"\n')
WANT_NEW = 'WANT_COMPARE="' + '\n'.join('%d $MERGE_BASE ahead=%d files=%d' % (n, ahead, nf) for n, t, br, h, ahead, nf, tree in PRS) + '"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): forty-five paths', 'with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): thirty-six paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (O, 'O'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    if p.startswith(ST): return 'ST + "' + p[len(ST):] + '"'
    return '"' + p + '"'
rows = []
JPATHS = list(DEVPIN) + NEWFILES
assert len(JPATHS) == 36, ('judged path count', len(JPATHS))
for p in JPATHS:
    ok = '{"%s": DV}' % DEVPIN[p] if p in DEVPIN else '{"ABSENT": DV}'
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k = 'ADMINCFG' if p == O + 'src/routes/adminConfig.ts' else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k, ' ' * max(1, 80 - len(k)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\nO = D + "services/originate/"\nST = "systemTest/schemathesis/"\n'
              'ADMINCFG = O + "src/routes/adminConfig.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all nine heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr[:9]) for n, _, _, _, _, _, tr in PRS) + '; all nine together ' + COMBINED + ', drafter tree-hash and scratch-clone merges = builder prediction; git ls-remote)"); sys.exit(0)\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = ('GUARDED = [A + "src/",\n'
             '           A + "package.json",\n'
             '           A + "vitest.config.ts",\n'
             '           A + "tsconfig.json",\n'
             '           O + "src/",\n'
             '           O + "package.json",\n'
             '           O + "jest.config.js",\n'
             '           O + "tsconfig.json",\n'
             '           D + "services/security/src/",\n'
             '           D + "scripts/",\n'
             '           ST,\n'
             '           D + "package.json",\n'
             '           D + "package-lock.json",\n'
             '           D + "eslint.config.mjs",\n'
             '           ".githooks/",\n'
             '           "BACKLOG.md"]\n'
             '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a\n'
             '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.\n'
             '# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.\n'
             'DEV_CONTENT_ALLOWED = {}\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the eleven heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the nine heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all nine '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway and originate src/ + config, security src/, scripts/, systemTest/schemathesis/, '
               'the Dev package.json + lock, eslint.config.mjs, .githooks/, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#%d %s: TIER %d' % (n, t, 1 if n in (1061, 1062) else 2) for n, t, *_ in PRS]
for tl in TIERLINES: assert tl in pt_, ('prompt lacks tier line', tl)
SEATWORDS = ['Legs 3/4/8 need a stack', 'login_stub', 'mergeable_state: unstable']
GWORDS = ['security/src/index.ts:569', 'Nothing failed', 'NOJSONCATCH', '1695', 'matches at 576']
for w in SEATWORDS + GWORDS: assert w in pt_ and w in mt_, ('READY mail and prompt must both carry', w)
assert 'MEASURE, not conclude' in pt_ and 'execute the failed path' in pt_.lower() and 'nine lines, one per pr' in pt_.lower(), 'prompt phrasing'
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", '>&2; exit 31; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1061 T1, #1062 T1, #1063-#1069 T2)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'NINE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and NINE verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'Legs 3/4/8 need a stack' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'mergeable_state: unstable' "$PROMPT_FILE" \
  && grep -qF 'Legs 3/4/8 need a stack' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state: unstable' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: Legs 3/4/8 need a stack / login_stub / mergeable_state: unstable" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-3rd history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'security/src/index.ts:569' "$PROMPT_FILE" && grep -qF 'Nothing failed' "$PROMPT_FILE" && grep -qF 'NOJSONCATCH' "$PROMPT_FILE" && grep -qF '1695' "$PROMPT_FILE" && grep -qF 'matches at 576' "$PROMPT_FILE" \
  && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qiF 'execute the FAILED path' "$PROMPT_FILE" \
  && grep -qF 'security/src/index.ts:569' "$BRIEF" && grep -qF 'Nothing failed' "$BRIEF" && grep -qF 'NOJSONCATCH' "$BRIEF" && grep -qF '1695' "$BRIEF" && grep -qF 'matches at 576' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry G-1 / G-2 / G-3 / G-4, or the prompt does not say MEASURE, not conclude and execute the FAILED path" >&2; exit 30; }
grep -qF '__COMBINED__' "$PROMPT_FILE" && grep -qF '__PREDICT__' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-nine tree in full, the octopus commit, the NOT-PINNED list, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1062 is KS-1260' "$PROMPT_FILE" && grep -qF 'PR #1067 is KS-1062' "$PROMPT_FILE" && grep -qF 'PR #1062 is KS-1260' "$BRIEF" && grep -qF 'PR #1067 is KS-1062' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH name the namespace trap: PR #1062 is KS-1260 / PR #1067 is KS-1062" >&2; exit 32; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST).replace('__COMBINED__', COMBINED).replace('__PREDICT__', BUILDER_PREDICT_COMMIT)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  nine heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1061 T1, #1062 T1, #1063-#1069 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all nine heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, NINE verdict lines"
  echo "  prompt names the report directory, the #1050-#1060 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: Legs 3/4/8 need a stack / login_stub / mergeable_state: unstable"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-3rd history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry G-1 / G-2 / G-3 / G-4; the prompt says MEASURE, not conclude, and execute the FAILED path"
  echo "  prompt names the all-nine tree, the octopus commit, the NOT-PINNED list and a loopback GATEWAY_URL for preflight"
  echo "  READY mail and prompt BOTH name the namespace trap: PR #1062 is KS-1260, PR #1067 is KS-1062"
  [ -n "${QAB1061_CUR_DEV:-}" ] && echo "  (develop read from the QAB1061_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1061_ADMINCFG_FILE:-}" ] && echo "  (develop services/originate/src/routes/adminConfig.ts read from the QAB1061_ADMINCFG_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('head check', HEADCHK_OLD, HEADCHK_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB1050_CUR_DEV:-', 'CUR_DEV="${QAB1061_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB1050_DOCS_FILE", "") if f == DOCSTS else ""\n',
                 '    fixture = os.environ.get("QAB1061_ADMINCFG_FILE", "") if f == ADMINCFG else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB1050_BRIEF:-}${QAB1050_PROMPT:-}${QAB1050_HEAD_1060:-}${QAB1050_CUR_DEV:-}${QAB1050_DOCS_FILE:-}" ]',
            '[ -z "${QAB1061_BRIEF:-}${QAB1061_PROMPT:-}${QAB1061_HEAD_1069:-}${QAB1061_CUR_DEV:-}${QAB1061_ADMINCFG_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n_ = s.count(old)
    if n_ != want: print('ANCHOR COUNT', label, n_, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n_)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1050-1060 gate survives except the PRIOR REPORT path (cited on purpose) and the template name
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'#1050-#1060 batch': 2, 'from launch_qa_secuura_batch1050_1060.sh': 1}   # exit 24 comment + --check line; the template
for k, v in INTENDED.items():
    assert BODY.count(k) == v, ('intended citation count', k, BODY.count(k), v)
    BODY = BODY.replace(k, '<CITED>')
RESID = ['QAB1050_', 'DOCS_FILE', 'DOCSTS', 'mail_batch1050', 'gate1050to1060', 'batch1050', 'cb7860d61', '23c379dcd', '59412d057', 'seatB-2nd',
         'eleven', 'ELEVEN', 'forty-five', 'FORTY-FIVE', 'nineteen', 'sixteen', 'threadTokenMint', 'Legs 3/4/8 were skipped', 'documents.ts:2327', ':2051',
         '09-aggregate-report', 'KS-1261', 'KS-1136', 'KS-1172', 'KS-1264', 'KS-1267', 'KS-1202', 'KS-1153', 'KS-1209', 'KS-1134', 'Testing/', 'services/anchoring',
         'N + "', '  T + "', ' T + "jobs', '21:56:17', '07:59:10', '07:5x', 'certifications.ts', 'provenance.ts', 'generate-openapi', 'orchestrate.sh']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])10(5[0-9]|60)(?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 2,   # OKPIN + the exit-31 guard
        REPORT_DIR: 1, PRIOR: 1, SUBJECT: 1, ': DV}': len(JPATHS), '"ABSENT": DV': 5, 'QAB1061_CUR_DEV': 5, 'QAB1061_ADMINCFG_FILE': 5,
       'QAB1061_HEAD_1069': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 31': None, 'exit 32': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-19_secuura-batch1061-1069.prompt.txt': 1, 'gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md': None,
       '"BACKLOG.md"]': 1, 'O + "src/",': 1, 'A + "src/",': 1, 'D + "scripts/",': 1, 'D + "services/security/src/",': 1, '".githooks/",': 1, '           ST,': 1,
       'ahead=1 files=': 9, 'PR #1062 is KS-1260': None, 'PR #1067 is KS-1062': None}
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
