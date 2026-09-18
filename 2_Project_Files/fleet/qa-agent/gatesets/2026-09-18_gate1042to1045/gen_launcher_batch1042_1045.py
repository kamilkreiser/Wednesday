#!/usr/bin/env python3
"""gen_launcher_batch1042_1045.py — derive launchers/launch_qa_secuura_batch1042_1045.sh from launchers/launch_qa_secuura_batch1038_1041.sh (the
batch gate that ran clean earlier on 2026-09-18) by ASSERTED block substitutions: every anchor must occur exactly as often as stated, or the generator
refuses and writes nothing.

ONE BATCHED gate, TIER 1 floor (set by #1043), FOUR PRs: #1042 KS-1254, #1043 KS-1228, #1044 KS-1258, #1045 KS-1230.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb anywhere, not even in a scratch repo:
  * origin: git ls-remote of refs/heads/develop, every refs/pull/N/head AND every branch — all must equal the pins;
  * local objects (git rev-parse / cat-file / diff --name-only): each PR is ONE commit whose parent IS develop, its file set and head tree are as
    pinned, every judged develop blob and every landed head blob is as pinned, the four are pairwise file-disjoint;
  * CANONICAL-PATCH identity for the two local-model PRs (#1044, #1045): develop's blobs are written as plain files into a fresh scratch dir (not a
    repo), `git apply` (patch mode, cwd = that dir) applies each section with its own .opts, and `git hash-object` (no -w) of each result must equal the
    head blob. #1042 / #1043 are the seat's own code: no canonical patch exists, none is claimed;
  * the ALL-FOUR TREE is re-derived by pure tree-object hashing in Python from `git cat-file tree` reads (git's tree serialisation + sha1), CONTROLLED by
    re-deriving each single head tree from develop the same way; it must equal the builder's 816d53a2b and the tree of the builder's predict commit
    93c99760a (read with cat-file). This replaces merge-tree: with every parent == develop and 0 shared files a 3-way merge is exactly this composition.
Usage: gen_launcher_batch1042_1045.py <template launcher> <output launcher>
Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_batch1042_1045', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV = '8b9c3f022bee76b79a47f1b8c5de8ad3ddb4a0ae'   # develop = the #1041 KS-1209 squash; every PR's parent and merge-base
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; S = D + 'packages/shared/'
RUNS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/'
PRS = [  # n, ticket, branch, head, canonical run dir (None = seat code), file count, head tree
 (1042, 'KS-1254', 'feature/ks-1254-ks256-cells-pin-the-upper-case-rfc-variant-nibble-and-the', '2ad066ae213631e05a6f0d67d5d57b73cdb23dac',
  None, 1, '5e38b665c3d87ecfb619a963dc294f7e19175ba9'),
 (1043, 'KS-1228', 'feature/ks-1228-a-refused-request-still-writes-an-action_provenance-row', '8d42bb01627ba46354d58b5b07c8d1c5c274deb9',
  None, 4, '5487055f3ca340994314464e74adc00c935cdeb6'),
 (1044, 'KS-1258', 'feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally', 'a21691fa474632e340d36378213d53d9aaa01915',
  '2026-09-18_ks1258-ornith35b-night', 2, '615ffd6c491a349978292bcdc61a0e2b04c8e946'),
 (1045, 'KS-1230', 'feature/ks-1230-put-apiadminsettings-stores-a-connectors', '63ecb0930a2fc6ababa7e2fd2c189392f67b4269',
  '2026-09-18_ks1230-ornith35b-night', 2, '849cc11bf86afb4da2a95b37e82000090a2b9943'),
]
COMBINED = '816d53a2b5189482aab2f763b2b5940ddcd45389'   # builder's predicted all-four tree (READY 05:50:47Z); re-derived below
BUILDER_PREDICT_COMMIT = '93c99760a'                    # builder's s-a11-batch4 predict commit; its tree must be COMBINED
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def gitb(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True).stdout
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# develop-side pins: path (repo-relative) -> blob at develop. The gate runs or reads every one of these.
DEVPIN = {
 S + 'src/__tests__/ks256-spec-example-contract.test.ts': '4ef040f6f2fbbe6d73a76ff860caf71ac0bbe619',
 'BACKLOG.md': 'dca47caa1',
 O + 'src/routes/certifications.ts': '20934ee94',
 O + 'src/routes/documents.ts': 'e3eeb5a68',
 A + 'src/routes/system-status.ts': '0b0a4af82d5bdc9ddda96aabc86dda9fb6de98aa',
 A + 'src/routes/admin.ts': 'f47dd6a655702ffbfc402ca920a33c4619d62c4b',
 D + 'scripts/spec-examples/check/contract.mjs': '07d4e9ab6b2879e08acfd587c4575bfaac1d1071',
 S + 'package.json': '3957692311221fbe87c4ab19447de8cec44aa19a',
 S + 'vitest.config.ts': '2a226c0068faa65538cda8d43d03bb9bee2944f1',
 O + 'src/services/provenance.ts': '483aa9eb331d2caa5af285e20d9668a9dbcd92a6',
 O + 'src/repositories/shareRepo.ts': '55494e94957560e8415d567ed53560183eb98873',
 O + 'package.json': 'd4435238d3ece7f7da42f043f56ca7739a611132',
 O + 'package-lock.json': '4c1800aee48392e6ca2efa80526b1b2627cec34d',
 O + 'jest.config.js': '735183662feea56d39f664eb6379cae1a2eec957',
 O + 'tsconfig.json': 'd1b46ece71ad5b2559ccad3648c23a5231e43b09',
 A + 'src/routes/verification.ts': 'f888e8cd0bd10c98a508542d75902ab122595157',
 A + 'src/services/health.ts': '7bedc074583d816d997bd6d679043db010804aed',
 A + 'src/services/redis.ts': 'fbb74be7ccc3f3068b243af527f8dfff7cd63fbb',
 A + 'src/index.ts': 'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'vitest.setup.ts': '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 D + 'frontend/admin/src/pages/Settings.tsx': 'e414630f25c49a954a41d75794a37da781804b3b',
 D + 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
 D + 'package-lock.json': '646c19f6f7f735ba32bfb20bef8b936835184949',
}
# expand the three short pins to full OIDs from the repo, then assert the prefix held
for p, b in list(DEVPIN.items()):
    if len(b) < 40:
        full = rp(DEV + ':' + p)
        assert full.startswith(b), ('short develop pin disagrees', p, b, full)
        DEVPIN[p] = full
LANDED = {  # path -> (blob at that PR's head, PR number); a develop reading one of these means that PR landed (exit 19)
 S + 'src/__tests__/ks256-spec-example-contract.test.ts': ('c083367c6', 1042),
 'BACKLOG.md': ('59a1928dc', 1043),
 O + 'src/routes/certifications.ts': ('02dcbe629', 1043),
 O + 'src/routes/documents.ts': ('b5e76dc61', 1043),
 O + 'src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts': ('0b9be1631', 1043),
 A + 'src/routes/system-status.ts': ('e911ce1fd', 1044),
 A + 'src/__tests__/ks1258-degraded-optional-service-advice.test.ts': ('9143365cb', 1044),
 A + 'src/routes/admin.ts': ('20c8a088f', 1045),
 A + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts': ('dd5ce8564', 1045),
}
bad = []
headof = {n: h for n, _, _, h, *_ in PRS}
for p, (b, n) in list(LANDED.items()):
    full = rp(headof[n] + ':' + p)
    if not full.startswith(b): bad.append(('head blob', n, p, b, full))
    LANDED[p] = (full, n)
    if p not in DEVPIN and git('cat-file', '-e', DEV + ':' + p).returncode == 0: bad.append(('new test already at develop', p))
for p, b in DEVPIN.items():
    if rp(DEV + ':' + p) != b: bad.append(('develop blob', p, b, rp(DEV + ':' + p)))

# 1. origin, read-only (git ls-remote): develop, every refs/pull/N/head and every branch
t0 = now()
refs = ['refs/heads/develop'] + [x for n, _, br, *_ in PRS for x in ('refs/pull/%d/head' % n, 'refs/heads/' + br)]
lsr = dict(reversed(l.split('\t')) for l in git('ls-remote', 'origin', *refs).stdout.strip().splitlines())
print('ls-remote', t0, '->', now(), '|', len(lsr), 'refs read')
if lsr.get('refs/heads/develop') != DEV: bad.append(('origin develop moved', lsr.get('refs/heads/develop')))
for n, t, br, h, *_ in PRS:
    a, b = lsr.get('refs/pull/%d/head' % n), lsr.get('refs/heads/' + br)
    print('  #%d %s pull/head %s branch %s  %s' % (n, t, (a or 'NONE')[:9], (b or 'NONE')[:9], 'OK' if a == b == h else 'MOVED'))
    if not (a == b == h): bad.append(('head moved', n, a, b))

# 2. PR shape against local objects
allfiles = []
for n, t, br, h, run, nf, tree in PRS:
    files = sorted(git('diff', '--name-only', DEV, h).stdout.splitlines()); allfiles += files
    par = rp(h + '^1'); npar = len(git('rev-list', '--parents', '-n', '1', h).stdout.split()) - 1
    ok = par == DEV and npar == 1 and len(files) == nf and rp(h + '^{tree}') == tree and all(f in LANDED and LANDED[f][1] == n for f in files)
    print('#%d %s head %s parent %s (=develop %s) parents %d files %d tree %s  %s' % (n, t, h[:9], par[:9], par == DEV, npar, len(files), rp(h + '^{tree}')[:9], 'OK' if ok else 'BAD'))
    if not ok: bad.append(('PR shape', n, files))
if len(allfiles) != len(set(allfiles)) or len(allfiles) != 9: bad.append(('four PRs not pairwise file-disjoint / not 9 files', allfiles))
print('pairwise disjoint: %d files, %d distinct' % (len(allfiles), len(set(allfiles))))
if bad: print('REFUSING: pins disagree with the repo; nothing written', bad); sys.exit(1)

# 3. canonical-patch identity for the local-model PRs — plain files in a scratch dir, git apply in patch mode, hash-object without -w
X = tempfile.mkdtemp(prefix='genb1042-', dir='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9b05af00-d7be-4a1b-951b-52959709cae5/scratchpad')
for n, t, br, h, run, nf, tree in PRS:
    if run is None: continue
    W = os.path.join(X, 'p%d' % n); os.makedirs(W)
    files = git('diff', '--name-only', DEV, h).stdout.splitlines()
    for f in files:
        if git('cat-file', '-e', DEV + ':' + f).returncode == 0:
            os.makedirs(os.path.dirname(os.path.join(W, f)), exist_ok=True)
            open(os.path.join(W, f), 'wb').write(gitb('cat-file', 'blob', DEV + ':' + f))
    ck = RUNS + run + '/out.md.checker/'
    for sec in ('section_1', 'section_2'):
        lines = open(ck + sec + '.opts').read().split()
        named = [w for w in lines if w.endswith('.diff')]; opts = [w for w in lines if w.startswith('--')]
        assert named == [ck + sec + '.diff'], ('opts names another diff', n, sec, named)
        r = subprocess.run(['git', 'apply', *opts, ck + sec + '.diff'], cwd=W, capture_output=True, text=True)
        print('  #%d %s git apply %s rc %d %s' % (n, sec, ' '.join(opts), r.returncode, r.stderr.strip()[:120]))
        if r.returncode: bad.append(('canonical apply', n, sec))
    for f in files:
        got = subprocess.run(['git', 'hash-object', os.path.join(W, f)], capture_output=True, text=True).stdout.strip()
        want = LANDED[f][0]
        print('  #%d canonical %s -> %s == head %s' % (n, f.split('/')[-1], got[:9], got == want))
        if got != want: bad.append(('canonical patch != PR', n, f))
print('scratch (plain files, not a repo; left in place):', X)

# 4. the all-four tree by pure tree hashing (read-only cat-file), controlled by each single head tree
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
MEMO = {}
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
def pr_changes(n, h):
    ch = {}
    for l in git('diff', '--raw', '--no-abbrev', DEV, h).stdout.splitlines():
        meta, path = l.split('\t', 1); f = meta.split()
        assert f[4] in ('M', 'A'), ('only M/A expected', l)
        ch[tuple(x.encode() for x in path.split('/'))] = (f[1].encode().lstrip(b'0') or b'0', f[3])
    return ch
devtree = rp(DEV + '^{tree}'); allch = {}
for n, t, br, h, run, nf, tree in PRS:
    ch = pr_changes(n, h); allch.update(ch)
    got = compose(devtree, ch)
    print('  control #%d: develop tree + its delta -> %s == head tree %s' % (n, got[:9], got == tree))
    if got != tree: bad.append(('tree-hash control', n, got))
comb = compose(devtree, allch)
bt = rp(BUILDER_PREDICT_COMMIT + '^{tree}')
print('ALL FOUR over develop -> %s | builder predicted %s: %s | builder predict commit %s tree %s: %s' % (comb, COMBINED[:9], comb == COMBINED, BUILDER_PREDICT_COMMIT, bt[:9], bt == COMBINED))
if comb != COMBINED or bt != COMBINED: bad.append(('combined tree', comb, bt))
if bad: print('REFUSING:', bad); sys.exit(1)

# 5. substitutions
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-18_gate1042to1045/mail_batch1042_ready.md'
PROMPT = WEDB + 'briefs/2026-09-18_secuura-batch1042-1045.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-batch1042-1045-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-batch1038-1041-tier1-r1/'
SUBJECT = '[QA -> Wednesday] BATCH GATE #1042 #1043 #1044 #1045 (KS-1254 KS-1228 KS-1258 KS-1230)'
SEATHIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-11th/'
assert os.path.isdir(PRIOR) and os.path.isdir(SEATHIST), 'prior report or seat history dir missing'
assert not os.path.exists(REPORT_DIR), 'report dir already exists — a second gate into the same dir'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and os.path.isfile(promptf), 'mail capture or prompt missing'
mt_ = open(mailf).read(); pt_ = open(promptf).read()
assert all(h[:9] in mt_ for _, _, _, h, *_ in PRS) and all(h in pt_ for _, _, _, h, *_ in PRS), 'READY mail / prompt do not name every head'
assert 'MESSAGE_ID: <010001a0b311401b-' in mt_ and 'TS: 2026-09-18T05:50:47' in mt_, 'mail capture is not the 05:50:47Z READY'
assert hashlib.sha256(mt_.split('\n', 7)[7].encode()).hexdigest() == re.search(r'TEXT_SHA256: (\w+)', mt_).group(1), 'mail capture text sha256 disagrees'

HEADER_OLD = cut('# launch_qa_secuura_batch1038_1041.sh', '# Exit: 0 launched (or guards passed under --check) · 2..29 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_batch1042_1045.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over FOUR file-disjoint Secuura/Blockchain PRs
#   #1042 KS-1254 @ 2ad066ae2  ks256 BOUNDARY_ROWS: 3 rows pin the upper-case variant nibble + the credit_ decision, TEST-ONLY  — TIER 2
#   #1043 KS-1228 @ 8d42bb016  originate documents.ts + certifications.ts: a refused request writes no action_provenance row  — TIER 1 (sets the floor)
#   #1044 KS-1258 @ a21691fa4  system-status.ts: a DEGRADED optional service gets read-only advice, never start/restart     — TIER 2
#   #1045 KS-1230 @ 63ecb0930  admin.ts PUT /api/admin/settings: 400 + store nothing on a malformed allowedDocumentTypes     — TIER 1 (allow-list write)
# Batched under Kam's 09:22 rule. FOUR verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 15:53:06 AEST 2026-09-18 (git ls-remote develop + refs/pull/N/head) and again by the generator: each PR is ONE commit whose
# parent IS develop 8b9c3f022; compare develop...head = merge_base 8b9c3f022, ahead 1, files 1/4/2/2 (asserted per PR, exit 10). Pairwise file-disjoint
# (9 files). Each PR over develop is a fast-forward (merged tree = head tree). ALL FOUR = tree 816d53a2b, re-derived by the generator by pure tree
# hashing (no git write), equal to the builder's prediction and to its predict commit 93c99760a's tree. #1044 and #1045 are byte-identical to their
# CANONICAL local-model patches (re-applied by the generator in a plain scratch dir); #1042 and #1043 are the seat's own code.
#
# The develop pin is judged by CONTENT — THIRTY-ONE paths by blob at the CURRENT develop: the nine PR files (six at develop blobs, three new tests
# ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: contract.mjs (the #1042 tamper target), shared
# package.json / vitest.config.ts, originate provenance.ts / shareRepo.ts / package.json / package-lock.json / jest.config.js / tsconfig.json,
# api-gateway verification.ts / health.ts / redis.ts (the platform-settings readers), index.ts, package.json / vitest.config.ts / vitest.setup.ts /
# tsconfig.json, the admin Settings page, eslint.config.mjs and the root package-lock.json. GUARDED: api-gateway src/ + config, originate src/ +
# config, packages/shared src/ + config, scripts/spec-examples/, the Settings page, eslint.config.mjs, the root lock, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-18_gate1042to1045/mail_batch1042_ready.md, the seat's READY mail (05:50:47Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the four heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all four heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and FOUR verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1038-#1041 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'legs 3/4/8 skipped', 'login_stub' and 'TS2708'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-18_seatA-11th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the prompt must carry the checker note (checker.sh:921, NOT a PR finding) and the #1043 NODE_ENV restore question.
# QAB1042_CUR_DEV (test override, --check only): stands in for origin develop. QAB1042_HEAD_1045 (test override): stands in for #1045's pinned head.
# QAB1042_ADMIN_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/admin.ts (its git blob).
# A launch with any QAB1042_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-18_gate1042to1045/gen_launcher_batch1042_1045.py from launch_qa_secuura_batch1038_1041.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-four tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1042_1045.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..30 a guard refused
"""
PRLIST = '\n'.join('  "%d|%s|refs/heads/%s|%s"' % (n, t, br, (h if n != 1045 else '${QAB1042_HEAD_1045:-' + h + '}')) for n, t, br, h, *_ in PRS)
VARS_OLD = cut('BRIEF="${QAB4_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1038to1041/mail_batch4_ready.md"\n')
VARS_NEW = ('BRIEF="${QAB1042_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QAB1042_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            '# n|ticket|branch|head — pinned from the seat READY (05:50:47Z) and re-read by the drafter (git ls-remote 15:53:06 AEST, branch AND refs/pull/N/head)\n'
            'PRS=(\n' + PRLIST + '\n)\n'
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop at 15:53:06 AEST: the #1041 KS-1209 squash, every head's parent\n"
            'MERGE_BASE="$DEVELOP_SHA"    # every PR is one commit on the pin itself — the compare is asserted against it\n'
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')
HEADCHK_OLD = cut('# The four heads, each pinned at its branch on origin', 'HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"\ndone\n')
HEADCHK_NEW = '''# The four heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
HEADS_NOTE=""
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  _lsr="$(git -C "$REPO" ls-remote origin "$_br" "refs/pull/$_n/head")"
  if ! printf '%s\\n' "$_lsr" | grep -q "^${_h}[[:space:]]${_br}\\$" || ! printf '%s\\n' "$_lsr" | grep -q "^${_h}[[:space:]]refs/pull/${_n}/head\\$"; then
    echo "REFUSING: #$_n $_t — $_h is not at $_br AND refs/pull/$_n/head on origin — that head moved; a verdict is valid ONLY at its head" >&2
    printf '%s\\n' "$_lsr" >&2
    exit 6
  fi
  HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"
done
'''
CMPC_OLD = cut('# develop...#1038 / #1039 / #1041 = 207716440', '2026-09-18.\n')
CMPC_NEW = '# develop...#1042 = 8b9c3f022 ahead 1 files 1; #1043 files 4; #1044 files 2; #1045 files 2 (git diff --name-only, drafter 15:5x AEST; the launcher reads the compare API).\n'
WANT_OLD = cut('WANT_COMPARE="1038 $MERGE_BASE', '1041 $MERGE_BASE ahead=1 files=2"\n')
WANT_NEW = 'WANT_COMPARE="1042 $MERGE_BASE ahead=1 files=1\n1043 $MERGE_BASE ahead=1 files=4\n1044 $MERGE_BASE ahead=1 files=2\n1045 $MERGE_BASE ahead=1 files=2"\n'
DEVCOMMENT_OLD = cut('# The develop pin, judged by CONTENT (see the header): twenty-two paths', 'cleared (DEV_CONTENT_ALLOWED).\n')
DEVCOMMENT_NEW = ('# The develop pin, judged by CONTENT (see the header): thirty-one paths by PATH BLOB at the CURRENT develop (no region judgement), then — if\n'
                  '# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).\n')
def jkey(p):
    for pre, nm in ((A, 'A'), (O, 'O'), (S, 'S'), (D, 'D')):
        if p.startswith(pre): return nm + ' + "' + p[len(pre):] + '"'
    return '"' + p + '"'
rows = []
for p in list(DEVPIN) + [x for x in LANDED if x not in DEVPIN]:
    ok = '{"%s": DV}' % DEVPIN[p] if p in DEVPIN else '{"ABSENT": DV}'
    ld = '{"%s": "#%d own"}' % LANDED[p] if p in LANDED else '{}'
    k = 'ADMINTS' if p == A + 'src/routes/admin.ts' else jkey(p)
    rows.append('  %s:%s(%s, %s),' % (k, ' ' * max(1, 78 - len(k)), ok, ld))
JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
JUDGED_NEW = ('A = D + "services/api-gateway/"\nO = D + "services/originate/"\nS = D + "packages/shared/"\nADMINTS = A + "src/routes/admin.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) + '\n}\n'
              '# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).\n'
              'content_cleared = set()\n')
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (the parent of all four heads: each merged tree = its head tree, a fast-forward: '
             + ', '.join('#%d %s' % (n, tr) for n, _, _, _, _, _, tr in PRS) + '; all four together ' + COMBINED + ', drafter tree-hash = builder prediction; git ls-remote)"); sys.exit(0)\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = ('GUARDED = [A + "src/",\n'
             '           A + "package.json",\n'
             '           A + "vitest.config.ts",\n'
             '           A + "vitest.setup.ts",\n'
             '           A + "tsconfig.json",\n'
             '           O + "src/",\n'
             '           O + "package.json",\n'
             '           O + "package-lock.json",\n'
             '           O + "jest.config.js",\n'
             '           O + "tsconfig.json",\n'
             '           S + "src/",\n'
             '           S + "package.json",\n'
             '           S + "vitest.config.ts",\n'
             '           D + "scripts/spec-examples/",\n'
             '           D + "frontend/admin/src/pages/Settings.tsx",\n'
             '           D + "eslint.config.mjs",\n'
             '           D + "package-lock.json",\n'
             '           "BACKLOG.md"]\n'
             '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a\n'
             '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.\n'
             '# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.\n'
             'DEV_CONTENT_ALLOWED = {}\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto EACH of the four heads', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto EACH of the four heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all four '
            + COMBINED[:9] + ') and re-runs each PR items and suites on it"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — '
               'the rest disjoint from the GUARDED list (api-gateway, originate and packages/shared src/ + config, scripts/spec-examples/, the admin Settings page, '
               'eslint.config.mjs, the root lock, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)\n')
TIERLINES = ['#1042 KS-1254: TIER 2', '#1043 KS-1228: TIER 1', '#1044 KS-1258: TIER 2', '#1045 KS-1230: TIER 1']
GUARDS_OLD = cut("grep -q 'at the TIER 1 floor' \"$PROMPT_FILE\"", '>&2; exit 29; }\n')
GUARDS_NEW = (r'''grep -q 'at the TIER 1 floor' "$PROMPT_FILE" ''' + ''.join("&& grep -qF '%s' \"$PROMPT_FILE\" " % tl for tl in TIERLINES) + r'''\
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1042 T2, #1043 T1, #1044 T2, #1045 T1)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'FOUR lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and FOUR verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'legs 3/4/8 skipped' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'TS2708' "$PROMPT_FILE" \
  && grep -qF 'legs 3/4/8 skipped' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'TS2708' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: legs 3/4/8 skipped / login_stub / TS2708" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '__SEATHIST__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-18_seatA-11th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'checker.sh:921' "$PROMPT_FILE" && grep -qF 'NOT a PR finding' "$PROMPT_FILE" && grep -qF 'NODE_ENV' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the checker note (checker.sh:921, NOT a PR finding) and the #1043 NODE_ENV restore question" >&2; exit 30; }
''').replace('__SUBJECT__', SUBJECT).replace('__SEATHIST__', SEATHIST)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  four heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1042 T2, #1043 T1, #1044 T2, #1045 T1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all four heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, FOUR verdict lines"
  echo "  prompt names the report directory, the #1038-#1041 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: legs 3/4/8 skipped / login_stub / TS2708"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-18_seatA-11th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  prompt carries the checker note (checker.sh:921, not a PR finding) and the #1043 NODE_ENV restore question"
  [ -n "${QAB1042_CUR_DEV:-}" ] && echo "  (develop read from the QAB1042_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1042_ADMIN_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/admin.ts read from the QAB1042_ADMIN_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('head check', HEADCHK_OLD, HEADCHK_NEW, 1),
 ('compare comment', CMPC_OLD, CMPC_NEW, 1),
 ('want compare', WANT_OLD, WANT_NEW, 1),
 ('develop comment', DEVCOMMENT_OLD, DEVCOMMENT_NEW, 1),
 ('cur dev', 'CUR_DEV="${QAB4_CUR_DEV:-', 'CUR_DEV="${QAB1042_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QAB4_PREFLIGHT_FILE", "") if f == PREFLIGHT else ""\n',
                 '    fixture = os.environ.get("QAB1042_ADMIN_FILE", "") if f == ADMINTS else ""\n', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QAB4_BRIEF:-}${QAB4_PROMPT:-}${QAB4_HEAD_1041:-}${QAB4_CUR_DEV:-}${QAB4_PREFLIGHT_FILE:-}" ]',
            '[ -z "${QAB1042_BRIEF:-}${QAB1042_PROMPT:-}${QAB1042_HEAD_1045:-}${QAB1042_CUR_DEV:-}${QAB1042_ADMIN_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

# 6. residual guard: nothing of the 1038-1041 gate survives except the PRIOR REPORT path (cited on purpose)
BODY = s.replace(PRIOR, '<PRIOR>')
INTENDED = {'the #1041 KS-1209 squash': 1, '#1038-#1041 batch': 2, 'from launch_qa_secuura_batch1038_1041.sh': 1}   # pin origin; prior batch (exit 24 + --check); the template
for k, v in INTENDED.items():
    assert BODY.count(k) == v, ('intended citation count', k, BODY.count(k), v)
    BODY = BODY.replace(k, '<CITED>')
RESID = ['QAB4_', 'PREFLIGHT', 'preflight_', 'mail_batch4', 'gate1038to1041', 'batch1038', 'KS-1233', 'KS-1248', 'KS-1125', 'KS-1209',
         '2122b4af7', '6faaacf62', 'b01ffba0a', '900344f39', '570ea002d', '207716440', 'a1b4b6536', 'd69d10e35', 'dd54cab00', '#922', 'seatA-10th',
         '12/15, legs 3/4/8 SKIPPED', 'deploy caveat', 'twenty-two', 'TWENTY-TWO', 'startup-migrations']
res = {t: BODY.count(t) for t in RESID if t in BODY}
for m in re.finditer(r'(?<![0-9a-fA-F])10(38|39|40|41)(?![0-9a-fA-F])', BODY): res[m.group(0)] = res.get(m.group(0), 0) + 1
if res: print('REFUSING: residual tokens in the body', res, [l[:130] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

# 7. output controls
CTL = {DEV: 1, COMBINED: 1, REPORT_DIR: 1, PRIOR: 1, SUBJECT: 1, ': DV}': 26 + 3, '"ABSENT": DV': 3, 'QAB1042_CUR_DEV': 5, 'QAB1042_ADMIN_FILE': 5,
       'QAB1042_HEAD_1045': None, 'refs/pull/$_n/head': 2, 'exit 6': None, 'exit 10': None, 'exit 19': None, 'exit 20': None, 'exit 26': None,
       'exit 27': None, 'exit 28': None, 'exit 29': None, 'exit 30': None, 'exit 16': None, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'DEV_CONTENT_ALLOWED = {}': 1,
       'briefs/2026-09-18_secuura-batch1042-1045.prompt.txt': 1, 'gatesets/2026-09-18_gate1042to1045/mail_batch1042_ready.md': None,
       '"BACKLOG.md"]': 1, 'O + "src/",': 1, 'S + "src/",': 1, 'D + "scripts/spec-examples/",': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for p, b in DEVPIN.items():
    if s.count(b) != 1: print('CONTROL DISAGREED develop pin', p, s.count(b)); sys.exit(1)
for p, (b, n) in LANDED.items():
    if s.count(b) != 1: print('CONTROL DISAGREED landed pin', n, p, s.count(b)); sys.exit(1)
for n, t, br, h, *_ in PRS:
    if s.count(h) != 1 or s.count(br) != 1: print('CONTROL DISAGREED head/branch', n, s.count(h), s.count(br)); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    for i in [m.start() for m in re.finditer(re.escape(tag), s)]:
        end = '\nPY' + ('J' if 'PYJ' in tag else '') + '\n'; j = s.index(end, i); blk = s[i:j]
        print('heredoc', tag.strip(), '@', s.count('\n', 0, i) + 1, 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
        if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull|merge-tree)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp); sys.exit(3)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
