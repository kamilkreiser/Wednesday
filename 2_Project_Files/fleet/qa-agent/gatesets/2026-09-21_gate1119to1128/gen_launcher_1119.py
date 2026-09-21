#!/usr/bin/env python3
"""gen_launcher_1119.py — write launchers/launch_qa_secuura_batch1119-1128.sh (ONE batched tier-1-floor round-1 gate over TEN file-disjoint PRs
#1119-#1128, Seat B 13th: thirteen TEST-ONLY patches + ONE bash_patch with a single product hunk on a CI job; READYs 2026-09-21T01:01:31Z-02:22:31Z)
in the SHAPE of gatesets/2026-09-21_gate1112to1118/gen_launcher_1112.py (pins re-read at generation, tree hashing, output controls, heredoc parity,
bash -n): exit 6 a head moved · 10 the compare per PR (merge_base + ahead + BEHIND + files — develop moving off the pin changes `behind` from 0 and
REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED detection · 7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 prompt + READY
greps · 16 overrides at launch · 21 TTY.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, the ten refs/pull/N/head AND the ten branches — all must equal the pins;
  * local objects (rev-list / rev-parse / diff --raw / diff --numstat / ls-tree): each head is ONE commit whose parent IS develop 7be81d5c9 (NO
    develop move this round: each PR is a fast-forward, merged tree = head tree); the 13 (path, develop blob | ABSENT, head blob) triples as
    pinned; the 13 paths pairwise disjoint, 12 under __tests__/ + the ONE job path on #1122 only, deletions 0 except the job's 1; every "unchanged
    read" path (config, locks, the eleven tamper files, the siblings) has the SAME blob at develop and at every head; the ten head trees; the
    all-ten tree re-derived by pure tree hashing from ls-tree reads (must equal predict_batch_scratch.out's real 3-way merges in six orders);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_1119.py <output launcher>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import hashlib, itertools, os, re, subprocess, sys, tempfile
OUT = sys.argv[1]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1119', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1119to1128'
DEV = '7be81d5c9b109959b559e03652fb092c12de58e8'    # origin develop at the pin = every head's parent (the #1112-#1118 batch landed; no move since)
DEV_TREE = '6aa9873f974019a92574d6db52e6356734573c8c'
ALL_OVER_DEV = '23d60cace7c37bc329ccc425e58659e950089a4d'   # the seat's s-b13-batch octopus tree = item 0; drafter predict_batch_scratch.out (6 orders)
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; S = D + 'services/security/'; T = D + 'services/timestamping/'
R = D + 'services/referral/'; M = D + 'services/mcp-server/'; SC = D + 'scripts/'; P = D + 'packages/shared/'; JOB = 'Blockchain/Testing/jobs/04-container-trivy.sh'
# n, ticket, item, branch, head, head tree (= tree over develop), file count, tier, additions, deletions
PRS = [
  ('1119', 'KS-753',  'VERIFIEDPERSISTED-1',                    'refs/heads/feature/ks-753-timestamping-fail-closed-a-mock-tsa-fallback-must-not-report-verifiedpersisted-1',        'e9e20196f2a91ca57ec6bc6d24087843e2611a08', 'c35d59b310b6b9d456a4f6b7b1eb8b26859b179d', 1, 2, 32, 0),
  ('1120', 'KS-1232', 'MCPINFORAWECHO-1 + HTTPSERVERINFOEMPTY-1', 'refs/heads/feature/ks-1232-get-apiconnectorinfo-tells-a-connector-all-types-permitted-mcp-info-doctypes-1',        '2a66cd17ec3bd5d91e2fc72c7e3f9102ce1eb839', 'e8b4659fab666a47c2e42c6fe1ec68d0945eb4dc', 2, 2, 87, 0),
  ('1121', 'KS-957',  'F4-TOOLINGTOKENS-1 (+ KS-930)',           'refs/heads/feature/ks-957-round-2-gate-residue-the-guard-and-its-suite-write-f4-toolingtokens-1',                '939de1ba519629cacd22031cbc42dbbb765b4040', 'c11e01c5e18b91705ebefec6e160b2c235f1daf6', 1, 2, 74, 0),
  ('1122', 'KS-1273', 'EXITCODEENV-1 (bash_patch)',              'refs/heads/feature/ks-1273-job-04-a-trivy_exit_code-or-trivyyaml-exit-code-in-the-exitcodeenv-1',                 '9aa5442aeef4d07a3d39e3c3e73e65ef9a42a350', '743126250635ef59c2421471712d90f3a4636449', 2, 2, 116, 1),
  ('1123', 'KS-1275', 'DESCRIPTIONVERBLIST-1',                   'refs/heads/feature/ks-1275-published-post-lifecycle-events-description-still-enumerates-descriptionverblist-1',    'c346999ad3956c02e56fca61f9ad30396ceee2ff', '85ddc802fe50371f051132a88c5141e9b133a0f0', 1, 2, 9, 0),
  ('1124', 'KS-880',  'LIVETENANTDEFAULT-1',                     'refs/heads/feature/ks-880-quarantine-or-reconcile-the-dead-converters-copy-a-second-livetenantdefault-1',          'bd907c5538286ee9333e2182d7b388c1007b7163', '192f34492e33c1b0e00b5fda33531b9cf2234afb', 1, 1, 9, 0),
  ('1125', 'KS-1223', 'WALLETFORWARD-1 + REFERRALFALLBACK-1',    'refs/heads/feature/ks-1223-a-client-x-wallet-address-is-forwarded-past-the-gateway-walletforward-referralfallback-1', 'c50c0a8d402cb6fc585b889c528802fba74c0e40', 'b058d498b3b6b86d8eb88df7b03e48d5426dab13', 2, 1, 124, 0),
  ('1126', 'KS-1283', 'PROVMOUNT-SUPERADMINROUTES-1',            'refs/heads/feature/ks-1283-platformts-a-widened-super_roles-would-admit-a-tenant-admin-provmount-superadminroutes-1', 'b23ad259a880ecb207b2ab3cf7e9a1b0b8368dad', '4b32a4d50b3758b2597f2a76e2aa84287a13aae8', 1, 1, 26, 0),
  ('1127', 'KS-1244', 'REFUSALMESSAGE-1',                        'refs/heads/feature/ks-1244-a-duplicated-x-api-key-header-defeats-key-authentication-via-refusalmessage-1',        'f0cc0aadc1a7856f76cbb69e925e23b94dd05a40', 'bf45a0ddb07a6154b394a70fcb583b44fe5c988f', 1, 1, 13, 0),
  ('1128', 'KS-1234', 'the KS-1234 trio',                        'refs/heads/feature/ks-1234-post-apiv1documents-with-applicationjson-never-answers-and-alias-trio-1',              'e35b5ddc27dffca5ad1a7cea17b4433484d460ac', '127d9d55be7796ca36449faa123be949f72dee50', 1, 1, 18, 0),
]
SECOND_KEY = {'1121': 'KS-930'}
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
# 1. origin
refs_wanted = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n, *_ in PRS] + [br for _, _, _, br, *_ in PRS]
lsr = out('ls-remote', 'origin', *refs_wanted)
print('ls-remote', now('+%Y-%m-%dT%H:%M:%SZ'), '|', len(lsr.strip().splitlines()), 'refs read (want 21)')
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
want = [('refs/heads/develop', DEV)] + [('refs/pull/%s/head' % n, h) for n, _, _, _, h, *_ in PRS] + [(br, h) for _, _, _, br, h, *_ in PRS]
for ref, w in want:
    print('  %-122s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
# 2. local objects
dt = out('rev-parse', DEV + '^{tree}').strip()
print('develop tree', dt[:9], '==', DEV_TREE[:9], dt == DEV_TREE)
if dt != DEV_TREE: sys.exit(1)
CHANGED = {}; PERPR = {}
for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS:
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    raw = out('diff', '--raw', '--abbrev=40', DEV, h).strip().splitlines()
    ns = {l.split('\t')[2]: (int(l.split('\t')[0]), int(l.split('\t')[1])) for l in out('diff', '--numstat', DEV, h).strip().splitlines()}
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split()
        files[path] = ('ABSENT' if b1 == '0' * 40 else b1, b2, st, m2, n)
    a_sum = sum(v[0] for v in ns.values()); d_sum = sum(v[1] for v in ns.values())
    non_test = [p_ for p_ in files if '__tests__/' not in p_]
    print('#%s %s head %s parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == pin %s | files %d (want %d) | +%d/-%d (want +%d/-%d) | modes %s | non-test paths %s' % (
        n, tk, h[:9], par == [DEV], lr, t[:9], t == ht, len(files), nf, a_sum, d_sum, adds, dels, sorted({v[3] for v in files.values()}), non_test or 'NONE'))
    ok_modes = all(v[3] == ('100755' if p_ == JOB else '100644') for p_, v in files.items())
    ok_nontest = (non_test == [JOB]) if n == '1122' else (non_test == [])
    if par != [DEV] or lr != ['0', '1'] or t != ht or len(files) != nf or a_sum != adds or d_sum != dels or not ok_modes or any(v[2] not in 'AM' for v in files.values()) or not ok_nontest: sys.exit(1)
    for p_, v in files.items():
        if p_ in CHANGED: print('REFUSING: path in two PRs', p_); sys.exit(1)
        CHANGED[p_] = v
    PERPR[n] = files
print('union paths', len(CHANGED), '(want 13) | added', sum(1 for v in CHANGED.values() if v[2] == 'A'), '(want 6) | pairwise overlaps', [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])] or 'NONE (45 pairs)')
if len(CHANGED) != 13: sys.exit(1)
PINNED = {  # the drafter's shape_1.out reads = the seat's GROUPING (develop-side blob, head blob), asserted against the live objects
  T + 'src/__tests__/ks740-bounded-fanout.test.ts': ('6fdf0e80a46c', 'd732631dc0c2adfa1cbf3345074f7c39ba41c2f5'),
  M + 'src/__tests__/ks1232-connector-info-relay.test.ts': ('ABSENT', 'e93bfae369f0ba940739c2a22ad25f9718ebda0a'),
  M + 'src/__tests__/ks1232-generate-package-doctypes-default.test.ts': ('ABSENT', '59bc927624043f1b5c3bccd03dc98cfec00ef400'),
  SC + '__tests__/check_shared_relink_tooling_tokens.test.sh': ('ABSENT', 'fdb125ca3e6ae4516836c4c12ac88e5b34b2ca46'),
  JOB: ('88444463f9d4', '6dfc5731e56ede5e5a6f420cccd92874b7566a87'),
  SC + '__tests__/container_trivy_exit_code_env_keeps_findings.test.sh': ('ABSENT', 'd119e64ba755e41e41d719d03ded24f79f297e04'),
  O + 'src/__tests__/ks978-published-contract-organizationuuid.test.ts': ('27366baf3251', '530fa32f8d886e70375e967304cf8881edf0e950'),
  S + 'src/__tests__/ks869-connector-id-persisted.test.ts': ('7a3fc7e16d0c', 'f452db039b9dceb34bebd5046525de1e42b1879e'),
  A + 'src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts': ('ABSENT', '82a92ea52407fba3cdeb755efab488854b3e5758'),
  R + 'src/__tests__/ks1223-wallet-header-fallback.test.ts': ('ABSENT', 'daf9f5c1a6bb586065fcf44559073c25624dcf48'),
  A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': ('50298953359e', '94d0813cc861333a2dc60457d7fac8af9ec6fd17'),
  A + 'src/__tests__/auth.test.ts': ('6d837e0aeeb8', '41f85fcb250ea6cd1b1e6bc33117dab2e7ee93ae'),
  A + 'src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts': ('3f85887f7268', 'e5cc79c5e29b0b657240feb2b8afc2b1d6073ba8'),
}
FULLDEV = {}
for p_, (b1, b2) in PINNED.items():
    if p_ not in CHANGED or not CHANGED[p_][0].startswith(b1) or CHANGED[p_][1] != b2: print('REFUSING: pinned blob disagrees for', p_, CHANGED.get(p_)); sys.exit(1)
    bd = git('rev-parse', '-q', '--verify', DEV + ':' + p_).stdout.strip() or 'ABSENT'
    if not bd.startswith(b1): print('REFUSING: develop-side blob of', p_, 'differs at', DEV[:9], bd, b1); sys.exit(1)
    FULLDEV[p_] = bd
print('the 13 pinned (develop blob, head blob) pairs agree with the live objects at 7be81d5c9: True')
# unchanged paths the gate reads or runs: same blob at develop and at EVERY head. The FIRST ELEVEN are the tamper files. The job is NOT here (PR F's target).
TAMPER = [S + 'src/index.ts', T + 'src/index.ts', A + 'src/index.ts', A + 'src/routes/verification.ts', A + 'src/routes/platform.ts', A + 'src/middleware/auth.ts',
          O + 'src/originate.openapi.ts', R + 'src/routes/referrals.ts', M + 'src/tools/info.ts', M + 'src/http-server.ts', SC + 'check-shared-relink.sh']
UNCHANGED = TAMPER + [SC + '__tests__/container_trivy_image_filter.test.sh', SC + '__tests__/container_trivy_failed_scan_is_loud.test.sh', SC + '__tests__/check_shared_relink.test.sh',
             SC + '__tests__/aggregate_report_trivy_artefact.test.sh', SC + '__tests__/orchestrate_jobs.test.sh', 'systemTest/__tests__/manifest_quarantine.test.sh',
             A + 'src/__tests__/ks480-org-provisioner-gate.test.ts', A + 'src/__tests__/db.retry.test.ts', A + 'src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts',
             A + 'vitest.setup.ts', A + 'package.json', A + 'vitest.config.ts', A + 'tsconfig.json', A + 'package-lock.json',
             O + 'package.json', O + 'jest.config.js', O + 'tsconfig.json', O + 'package-lock.json', O + 'src/index.ts',
             S + 'package.json', S + 'vitest.config.ts', S + 'tsconfig.json', S + 'package-lock.json',
             T + 'package.json', T + 'vitest.config.ts', T + 'tsconfig.json', T + 'package-lock.json',
             R + 'package.json', R + 'vitest.config.ts', R + 'tsconfig.json', R + 'package-lock.json', R + 'src/index.ts',
             M + 'package.json', M + 'vitest.config.ts', M + 'tsconfig.json', M + 'package-lock.json',
             P + 'package.json', P + 'vitest.config.ts', P + 'tsconfig.json',
             SC + 'run-shell-suites.sh', SC + 'preflight/preflight.sh', SC + 'fix-libsodium-symlink.js', '.githooks/pre-push', D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs']
UBLOB = {}
for p_ in UNCHANGED:
    b1 = out('rev-parse', DEV + ':' + p_).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', b1): print('REFUSING: missing', p_); sys.exit(1)
    for n, *_r in PRS:
        h = _r[3]
        if out('rev-parse', h + ':' + p_).strip() != b1: print('REFUSING: unchanged-read path differs at a head', p_, n); sys.exit(1)
    UBLOB[p_] = b1
print('unchanged-read paths', len(UNCHANGED), 'all same blob at develop and at every head: True (the first', len(TAMPER), 'are the tamper files)')
# the eleven tamper files + the targets held at 362e51fe0 byte-unchanged from the hold tip to DEV (auth.test.ts + ks978 were held AT DEV and DIFFER at 362e51fe0)
OLD = '362e51fe0db7e73d5557924902763fe3f10fd8c7'
for p_ in TAMPER:
    if out('rev-parse', OLD + ':' + p_).strip() != UBLOB[p_]: print('REFUSING: tamper file moved since 362e51fe0', p_); sys.exit(1)
for p_ in (T + 'src/__tests__/ks740-bounded-fanout.test.ts', JOB, S + 'src/__tests__/ks869-connector-id-persisted.test.ts', A + 'src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts', A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'):
    if out('rev-parse', OLD + ':' + p_).strip() != FULLDEV[p_]: print('REFUSING: target path moved since its hold tip', p_); sys.exit(1)
for p_ in (A + 'src/__tests__/auth.test.ts', O + 'src/__tests__/ks978-published-contract-organizationuuid.test.ts'):
    if out('rev-parse', OLD + ':' + p_).strip() == FULLDEV[p_]: print('REFUSING: expected #1114/#1115 to have changed this path between 362e51fe0 and 7be81d5c9', p_); sys.exit(1)
print('the 11 tamper files + 5 held-at-362e51fe0 targets identical at 362e51fe0 and 7be81d5c9; auth.test.ts + ks978 differ (held at 7be81d5c9): True')
# 2b. the trees re-derived WITHOUT any git write: pure tree hashing from ls-tree reads
def ls_tree(oid):
    ents = []
    for l in out('ls-tree', oid).strip().splitlines():
        meta, name = l.split('\t', 1); mode, typ, sha = meta.split()
        ents.append([mode, typ, sha, name])
    return ents
def hash_tree(ents):
    def key(e): return e[3] + ('/' if e[1] == 'tree' else '')
    body = b''.join((e[0].lstrip('0') + ' ' + e[3]).encode() + b'\0' + bytes.fromhex(e[2]) for e in sorted(ents, key=key))
    return hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
def compose(tree_oid, changes):
    ents = ls_tree(tree_oid)
    groups = {}
    for path, (mode, blob) in changes.items():
        top, rest = (path.split('/', 1) + [None])[:2]
        groups.setdefault(top, {})[rest] = (mode, blob)
    byname = {e[3]: e for e in ents}
    for top, sub in groups.items():
        if None in sub:
            mode, blob = sub[None]
            if top in byname: byname[top][0], byname[top][2] = mode, blob
            else: ents.append([mode, 'blob', blob, top]); byname[top] = ents[-1]
        else:
            byname[top][2] = compose(byname[top][2], sub)
    return hash_tree(ents)
ctrl = hash_tree(ls_tree(DEV_TREE)); print('tree-hash control: re-hashing develop root tree ->', ctrl[:9], ctrl == DEV_TREE)
if ctrl != DEV_TREE: sys.exit(1)
for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS:
    ch = {p_: (v[3], v[1]) for p_, v in PERPR[n].items()}
    mt = compose(DEV_TREE, ch)
    print('  #%s compose over develop -> %s == head tree %s (fast-forward)' % (n, mt[:9], mt == ht))
    if mt != ht: sys.exit(1)
thirteen = {p_: (v[3], v[1]) for p_, v in CHANGED.items()}
ad = compose(DEV_TREE, thirteen)
print('compose(the 13 into develop tree) ->', ad, '==', ALL_OVER_DEV[:9], ad == ALL_OVER_DEV)
if ad != ALL_OVER_DEV: sys.exit(1)
pm = open(os.path.join(GS, 'predict_batch_scratch.out')).read()
print('predict_batch_scratch.out: six orders name the tree:', pm.count(ALL_OVER_DEV) >= 7, '| read-tree control:', ('-> ' + DEV_TREE + ' == ' + DEV_TREE) in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm, '| 13 files +508/-1:', '13 files changed, 508 insertions(+), 1 deletion(-)' in pm)
if not (pm.count(ALL_OVER_DEV) >= 7 and ('-> ' + DEV_TREE + ' == ' + DEV_TREE) in pm and 'rc=128 (want 128)' in pm and '13 files changed, 508 insertions(+), 1 deletion(-)' in pm): sys.exit(1)

# 3. the launcher
BRIEF = GS + '/mail_batch1119_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1119-1128.prompt.txt'
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
OLDER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
for d_ in (PRIOR, EARLIER, OLDER):
    if not os.path.isdir(d_): print('REFUSING: report dir absent', d_); sys.exit(1)
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
if 'NOT YET ARRIVED' in brief_txt: print('REFUSING: the combined capture has a section NOT YET ARRIVED'); sys.exit(1)
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-118s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{"%s": "%s"}' % landed) if landed else '{}')
judged = [jline(p_, v[0], (v[1], '#%s own' % v[4])) for p_, v in CHANGED.items()] + [jline(p_, UBLOB[p_], None) for p_ in UNCHANGED]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, tk, br, ('${QAB1119_HEAD_1128:-%s}' % h) if n == '1128' else h, nf) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=0 files=%d' % (n, nf) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER %d' \"$PROMPT_FILE\"" % (n, tk, tier) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
def ns_sentence(n, tk): return 'PR #%s is %s.' % (n, tk) if n not in SECOND_KEY else 'PR #%s is %s + %s.' % (n, tk, SECOND_KEY[n])
NS_GREP = ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (ns_sentence(n, tk), n, tk) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
# exit 30: seat items that must sit in BOTH the READY capture and the prompt (the seat's own figures and words)
# (READY F prints its two head blobs as 12-hex prefixes — 6dfc5731e56e / d119e64ba755 — so those two enter the BOTH list by prefix; the other eleven in full)
BOTH = ['18499832', ALL_OVER_DEV, '6aa9873f9740', DEV, '855c77ac4db8', '84ef030470037ea14749365c6dbaf7895afc8624'] + [ht for *_a, ht, nf, tier, adds, dels in PRS] + [b2 if b2 not in ('6dfc5731e56ede5e5a6f420cccd92874b7566a87', 'd119e64ba755e41e41d719d03ded24f79f297e04') else b2[:12] for b1, b2 in PINNED.values()] + [
        '4a90382b7882', '7962b0e379ef', '9fa2a9e41619', '79d25bd522ff', 'c944a3e24782', 'd0333a7bb4ad', '947a3ec410ef', '8de000e899a9', '46784fc8ed79', 'ffc3162048bc',
        '75b4a70d1503', '53f09e6638f7', '4aa0c1b41466', '430f435447c5', '0acfe0d608fd', 'c135806c7c00', '3ac42d3bd247', '0c06f16a4a40', 'b8aa0b14a95f', 'd8b2e2654543',
        'VERIFIEDFALSE', 'VERIFIEDATDROPPED', 'RELAYDROPPED', 'RELAYWRONGFIELD', 'RAWDOCTYPES', 'TOOLINGTOKENSGONE', 'NPMGONE', 'YARNGONE', 'VERBLISTSTALE', 'VERBWITHOUTROUTE',
        'LIVETENANTRAW', 'WALLETNOTFORWARDED', 'HEADERFALLBACKREMOVED', 'PROVMOUNTUNGUARDED', 'WIDENROLES', 'REFUSALMESSAGECHANGED', 'ALIASNARROWED', 'SANITIZEEVERYWHERE', 'PARSERONNFTALIAS', 'NFTPARSERUNMOUNTED',
        '215', '44/44', '692', '690', '689', '697/697', '28/28', '5/5', '809/809', '907/907', '6 ok / 0 FAIL', '5 ok / 0 FAIL', '3 ok / 2 FAIL', '3 ok / 0 FAIL', '106 passed, 0 failed', '41 passed, 0 failed (of 41)', '42 passed, 0 failed (of 42)',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'login_stub', 'mergeable_state', 'stubs=4', 'INSTR-1', 'TS2339', 'TS2322', 'req.user', 'no-useless-assignment', 'LINT-1', 'LINT-2',
        'manifest_quarantine', 'KS-1135', 'reports nothing moved', 'drive.ts', 'SIBLING_ALLOW', 'prc_rows', 'quarantine-prc-run1', 'PROTOCOL-DIFF', 'PROTOCOL-CLEAN', 'GO: merge #1119-#1128 batch',
        'Deviation from verbatim: NONE', 'linear[bot]', 'attachmentsForURL', 'contributes', 'Refs KS-930', 'ks-930', 'KS-887', 'KS-958', 'KS-794', 'KS-1133',
        ':5432', 'anchoring:4005', 'localhost:6000', '203.0.113.7:443', 'unattributed', 'x-wallet-address', 'rowToApiKey', 'requireOrgProvisioner', 'requireSuperAdmin', 'sanitizeInput', 'shouldParseBody',
        'allowedDocumentTypes', 'LIFECYCLE_EVENT_ACTIONS', 'TRIVY_EXIT_CODE', '--exit-code 0', 'TRIVY_JOB_SH', 'shellcheck', 'jq', '/bin/bash', 'bash -n',
        'KS-1136', 'fullName', 'RED-FIRST', 'GREEN-AFTER', 'section_1', 'section_2', 'tolower(L)', 'T9 gap', 'em dash', '127.0.0.1:1',
        # (uploadBodyParser, generateCode, registerInfoTools, MCP_HTTP_PORT, PLATFORM_DATABASE_URL, tenantAdminJwt, KS-256, KS-1201 sit in the brief / PR bodies / prompt, NOT in the READY capture — by-name keywords, not BOTH tokens)
        'KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-869', 'KS-740', 'KS-444', 'KS-921', 'KS-490', 'KS-1072', 'KS-815', 'KS-1215',
        'KS-1203', 'KS-1198', 'KS-1284', 'KS-1175', 'KS-1006', 'KS-1236', 'KS-570', 'KS-719', 'KS-1194', 'KS-1279', 'KS-1272', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953',
        'Nothing failed', 'pairwise overlaps NONE', '<= 92 chars', 'six orders', 'both ways', '4ef6430c3d68e2bb', '0720a4bfa4a4', '7431262506', 'ALIASUPLOAD-1', 'ALIASOTHERROUTES-1', 'SECURITYMIDDLEWARESKIP-1',
        'VERIFIEDPERSISTED-1', 'MCPINFORAWECHO-1', 'HTTPSERVERINFOEMPTY-1', 'F4-TOOLINGTOKENS-1', 'EXITCODEENV-1', 'DESCRIPTIONVERBLIST-1', 'LIVETENANTDEFAULT-1', 'WALLETFORWARD-1', 'REFERRALFALLBACK-1', 'PROVMOUNT-SUPERADMINROUTES-1', 'REFUSALMESSAGE-1']
missing = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', [(t, online(t, brief_txt.splitlines()), online(t, prompt_txt.splitlines())) for t in missing]); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
# exit 33: Wednesday's eighteen by-name items, each by its own exact phrases (all must be in the prompt)
BYNAME = [
 ('1', ['round 1 of 2', 'ZERO product bytes on', 'EXACTLY ONE product path on #1122', 'files API union 13']),
 ('2', ['DISJOINTNESS AND THE TREES, RE-DERIVED', 'at least forward and exact reverse', 'read-tree back to develop', 'fast-forward = its head tree', 'every count from the RUNNER']),
 ('3', ['THE THREE SKIPPED LEGS AND THE LEG-14 RED', 'legs 3, 4, 8', 'skip_stack', 'GRADE the manifest_quarantine red', 'one class with INT-1']),
 ('4', ['RED-FIRST PER PR UNDER THE COVER RULE', 'DEVELOP COVER measured FIRST', 'reds == declared ∪ measured cover', 'ONE named sibling allowance on #1128', '20/20 by exact-line AND raw-substring', 'TWO-line block', 'THE NAMED SIBLING ALLOWANCE', 'expect EXACTLY those two cells red', 'RED-FIRST / GREEN-AFTER']),
 ('5', ['THE ROW MAPPER', 'OTHERMAPPERDEFAULT', 'KS-887 stays OUT']),
 ('6', ['THE WALLET HEADER, TWO LANES', 'GATEWAY_VOUCH_SECRET', 'LINT-1 (LEAD)']),
 ('7', ['THE MOUNTS', 'THIRTEENTHMOUNT', 'TWELVE method/path pairs', 'tenantAdminJwt()']),
 ('8', ['THE 401 BODY', 'INSTR-1 recurs by construction', 'two drives, one cell']),
 ('9', ['THE ALIAS TRIO AND THE ALLOWANCE', 'NOT the CONTROL']),
 ('10', ['vi.doMock', 'makes NO connection at all']),
 ('11', ['a NEW lane', 'MCP_HTTP_PORT=0', ':7890 never taken']),
 ('12', ['CONTROL install verb', 'TALLY line', 'ONLY product byte of the round graded on its own', 'which trivy', 'TRIVYYAMLEXITCODE', 'completeness detector fires']),
 ('13', ['REGISTERED schema', 'em dash planted as UTF-8', 'F3 (LEAD', 'testMatch']),
 ('14', ['THE db.retry INTERMITTENT, LOAD-2 AND THE LEG-14 RED', 're-run that suite SERIAL', 'RULE WHETHER IT BLOCKS', 'filed by nobody here']),
 ('15', ['THE CONNECTION CENSUS', 'four FIRST sets', 'multiplicity scales with']),
 ('16', ['LINEAR LINK HYGIENE', 'includeArchived', 'KS-1119', 'KS-1128', 'Completes KS-1244', 'recommend', 'archived-but-labelled-live']),
 ('17', ['SAME ROW FORMAT as the PRIOR REPORT', 'proposed cell', "local model's next round", 'BY DESIGN', 'THIRTEEN prior rows CLOSE here']),
 ('18', ['ONE MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', '#1120 TWO', '#1122 TWO', '#1125 TWO', 'COMMA-separated', '## MERGE ADDENDUM', 'MG-3 KEY-SET rule', 'merge14.py:58', 'THE LINE-NUMBER DISCIPLINE', 'NAME WHO INHERITED IT']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'must not recommend pinning either', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree', 'lsof -nP -iTCP:4005 -sTCP:LISTEN', 'lsof -nP -iTCP:4006 -sTCP:LISTEN', 'lsof -nP -iTCP:5432 -sTCP:LISTEN']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('## MERGE ADDENDUM',), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS:
    if not online(ns_sentence(n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt:', ns_sentence(n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk)); sys.exit(1)
    if not online('#%s %s: TIER %d' % (n, tk, tier), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER %d' % (n, tk, tier)); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 18 items + the closing, all present in the prompt')

L = r'''#!/bin/bash
# launch_qa_secuura_batch1119-1128.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over TEN file-disjoint
# Secuura/Blockchain PRs (Seat B 13th; fourteen local-model patches grouped by FILE SET into ten PRs across SEVEN lanes)
#   #1119 PR B KS-753 @ e9e20196f  timestamping VITEST test: VERIFIEDPERSISTED-1 (+32, one file) — TIER 2, pushed FIRST
#   #1120 PR E KS-1232 @ 2a66cd17e  mcp-server VITEST tests: MCPINFORAWECHO-1 + HTTPSERVERINFOEMPTY-1 (+87, two NEW files) — TIER 2 (a NEW lane)
#   #1121 PR G KS-957 + KS-930 @ 939de1ba5  BASH suite: F4-TOOLINGTOKENS-1 (+74, one NEW suite) — TIER 2
#   #1122 PR F KS-1273 @ 9aa5442ae  bash_patch: the round's ONE PRODUCT HUNK on Blockchain/Testing/jobs/04-container-trivy.sh (-1/+2) + one NEW suite (+114) — TIER 2 (a CI job)
#   #1123 PR H KS-1275 @ c346999ad  originate JEST test: DESCRIPTIONVERBLIST-1 (+9) — TIER 2
#   #1124 PR A KS-880 @ bd907c553  security VITEST test: LIVETENANTDEFAULT-1 (+9) — TIER 1 (rowToApiKey, a tenant-isolation surface)
#   #1125 PR D KS-1223 @ c50c0a8d4  api-gateway + referral VITEST tests: WALLETFORWARD-1 + REFERRALFALLBACK-1 (+124, two NEW files, TWO lanes) — TIER 1
#   #1126 PR I KS-1283 @ b23ad259a  api-gateway VITEST test: PROVMOUNT-SUPERADMINROUTES-1 (+26) — TIER 1 (routes/platform.ts)
#   #1127 PR J KS-1244 @ f0cc0aadc  api-gateway VITEST test: REFUSALMESSAGE-1 (+13) — TIER 1 (middleware/auth.ts)
#   #1128 PR C KS-1234 @ e35b5ddc2  api-gateway VITEST test: the KS-1234 trio (+18, one file, three READYs) — TIER 1 (the sanitizer mount), pushed LAST
# NINE are TEST-ONLY and #1122 carries EXACTLY ONE product path (files API + local diff --raw: 13 paths, 12 under __tests__/ + the job, +508/-1,
# 7 M + 6 A — generator-asserted by numstat; the job is mode 100755).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the ten heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the ten head trees (= the trees over develop: each head's parent IS develop, a fast-forward)
# and the all-ten tree by REAL 3-way merges in a --shared scratch clone in SIX orders (predict_batch_scratch.out) AND by pure tree hashing in the
# generator; every BOTH-list token asserted present in the READY capture and the prompt at generation.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets14.py wants exactly ONE equality target PER PR FILE (1/2/1/2/1/1/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` (targets14.py:28) — the #1120, #1122 and #1125 addendum lines carry TWO targets COMMA-separated (exit 25); merge14.py:54-:64
# asserts each squash body's key set == the PR's OWN Refs set (two keys on #1121 only).
# Batched under Kam 2026-09-18 standing rule. TEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All eleven tickets stay where they are (In Progress; bot-walked or already).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + ten refs/pull/N/head + ten branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS origin develop 7be81d5c9 (tree 6aa9873f974, the #1112-#1118 batch landed) — NO develop move under these
# heads, so each PR over develop is a fast-forward (merged tree = head tree); compare develop...head = merge_base 7be81d5c9, ahead 1, BEHIND 0,
# files 1/2/1/2/1/1/2/1/1/1 (exit 10 — a squash on develop changes `behind` and REFUSES: re-pin deliberately). Pairwise file-disjoint (13 paths:
# 6 modified tests + the job, 6 NEW tests; overlap 0 over 45 pairs). ALL TEN over 7be81d5c9 = 23d60cace7c37bc329ccc425e58659e950089a4d, identical
# in every order tried.
#
# The develop pin is judged by CONTENT — SIXTY-TWO paths by blob at the CURRENT develop: the 13 PR paths (7 at develop blobs, 6 ABSENT; any at its
# head blob -> exit 19 LANDED, naming the PR), the 11 tamper files (security index.ts, timestamping index.ts, api-gateway index.ts,
# verification.ts, platform.ts, middleware/auth.ts, originate.openapi.ts, referrals.ts, info.ts, http-server.ts, check-shared-relink.sh), and
# what the gate runs or reads: the five bash siblings + manifest_quarantine, the ks480 cover-cell file, db.retry (LOAD-1), the ks1207 control file,
# the six services' package.json / config / tsconfig / lock, the originate + referral index.ts, packages/shared's, run-shell-suites.sh,
# preflight.sh, fix-libsodium-symlink.js, the pre-push hook, the Dev package.json + lock, eslint.config.mjs.
# GUARDED: every service's src/ + config (security, timestamping, api-gateway, referral, mcp-server, originate, anchoring, auth), packages/shared,
# scripts/, systemTest/, .githooks/, Blockchain/Testing/jobs/, the Dev package.json + lock, eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate1119to1128/mail_batch1119_ready.md, the seat's TEN READY mails (01:01:31Z … 02:22:31Z) + the 00:58:10Z STATUS
# mail + the 00:13:13Z plan-confirmation mail + the 00:39:34Z PR C and 01:44:22Z PR D QUESTION mails, each captured verbatim by message id from
# wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1124 T1, #1125 T1, #1126 T1, #1127 T1, #1128 T1, #1119 T2, #1120 T2, #1121 T2, #1122 T2, #1123 T2).
# exit 10: the compare per PR (merge_base 7be81d5c9, ahead 1, behind 0, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all ten heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and TEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1112-#1118), the EARLIER REPORT (#1106-#1111), the OLDER REPORT
#          (#1102-#1104) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (TWO for #1120, #1122, #1125, comma-separated),
#          the `## MERGE ADDENDUM` heading targets14.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b13-*) and writing in the seat 2026-09-21_seatB-13th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4005 / :4006 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, develop and its tree, the ten head trees, the
#          all-ten tree, the thirteen head blobs, the 20 plant sha256s the READYs carry, the 20 tamper ids, the suite counts, the allowance's
#          words, LINT-1 / LINT-2 / INSTR-1, the leg-14 words, the :5432 and :4005 words, the archived and foreign keys, the GO subject), and
#          the prompt must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-ten tree in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the ten, which ticket(s) the PR is (PR #1119 is KS-753. … PR #1128 is KS-1234.).
# exit 33: the prompt must carry Wednesday EIGHTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1119_CUR_DEV (test override, --check only): stands in for origin develop. QAB1119_HEAD_1128 (test override): stands in for #1128 pinned head.
# QAB1119_BRIEF / QAB1119_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1119_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1119to1128/gen_launcher_1119.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1112.py.
#
# Usage: launch_qa_secuura_batch1119-1128.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1119_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1119_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation = every head's parent (no develop move this round)
MERGE_BASE='__DEV__'    # every head's parent = merge-base = develop itself
ALL_OVER_DEV='__ALLDEV__'     # all ten over the pin 7be81d5c9 (real 3-way, six orders; generator tree-hash) — the tree that matters for the merge
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
EARLIER_REPORT='__EARLIER__'
OLDER_REPORT='__OLDER__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The ten heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
HEADS_NOTE=""
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h _f <<< "$_pr"
  _lsr="$(git -C "$REPO" ls-remote origin "$_br" "refs/pull/$_n/head")"
  if ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]${_br}\$" || ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]refs/pull/${_n}/head\$"; then
    echo "REFUSING: #$_n $_t — $_h is not at $_br AND refs/pull/$_n/head on origin — that head moved; a verdict is valid ONLY at its head" >&2
    printf '%s\n' "$_lsr" >&2
    exit 6
  fi
  HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"
done

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 7be81d5c9, ahead 1, behind 0 (no develop
# move), files 1/2/1/2/1/1/2/1/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  PRS_FLAT="${PRS[*]}" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
for pr in os.environ["PRS_FLAT"].split():
    n, tk, br, h, nf = pr.split("|")
    r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + h, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
    c = json.load(r)
    print("%s %s ahead=%d behind=%d files=%d" % (n, c["merge_base_commit"]["sha"], c["ahead_by"], c["behind_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compares develop...head from the GitHub compare API" >&2; exit 13; }
WANT_COMPARE="__WANTCOMPARE__"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved —
# the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1119_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" ALL_OVER_DEV="$ALL_OVER_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]; all_over_dev = os.environ["ALL_OVER_DEV"]
D = "Blockchain/Dev/"
A = D + "services/api-gateway/"
O = D + "services/originate/"
S = D + "services/security/"
T = D + "services/timestamping/"
R = D + "services/referral/"
M = D + "services/mcp-server/"
SC = D + "scripts/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the six NEW tests)
JUDGED = {
__JUDGED__
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": HTTP " + str(e.code)); sys.exit(0)
        blob = "ABSENT"
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — that PR has landed; this gateset is stale for it"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (every head parent; every head a fast-forward over it; all ten together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/", A + "package.json", A + "vitest.config.ts", A + "vitest.setup.ts", A + "tsconfig.json", A + "package-lock.json",
           O + "src/", O + "package.json", O + "jest.config.js", O + "tsconfig.json", O + "package-lock.json",
           S + "src/", S + "package.json", S + "vitest.config.ts", S + "tsconfig.json", S + "package-lock.json",
           T + "src/", T + "package.json", T + "vitest.config.ts", T + "tsconfig.json", T + "package-lock.json",
           R + "src/", R + "package.json", R + "vitest.config.ts", R + "tsconfig.json", R + "package-lock.json",
           M + "src/", M + "package.json", M + "vitest.config.ts", M + "tsconfig.json", M + "package-lock.json",
           D + "services/anchoring/src/", D + "services/anchoring/package.json", D + "services/auth/src/", D + "services/auth/package.json",
           P + "src/", P + "package.json", P + "vitest.config.ts", P + "tsconfig.json",
           SC, "systemTest/", ".githooks/", "Blockchain/Testing/jobs/",
           D + "package.json", D + "package-lock.json", D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto EACH of the ten heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-ten tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1119.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && __TIERGREP__ \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1124 T1, #1125 T1, #1126 T1, #1127 T1, #1128 T1, #1119 T2, #1120 T2, #1121 T2, #1122 T2, #1123 T2)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat READY mail capture path" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h _f <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "$_h" "$BRIEF" \
    || { echo "REFUSING: the READY capture or the prompt does not name #$_n's head $_h — a gate about another SHA is another gate" >&2; exit 20; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1119-#1128 (ten PRs; tier 1 = #1124, #1125, #1126, #1127, #1128)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'TEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and TEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1120 TWO' "$PROMPT_FILE" && grep -qF '#1122 TWO' "$PROMPT_FILE" && grep -qF '#1125 TWO' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1120 TWO, #1122 TWO, #1125 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b13-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-13th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b13-*) and writing in the seat 2026-09-21_seatB-13th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4006 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4005 / :4006 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in __BOTHLOOP__; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-ten tree and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1119 is KS-753. … PR #1128 is KS-1234.)" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday eighteen by-name items (tier/round/product bytes; the trees and disjointness; the skipped legs + the leg-14 red; red-first under the cover rule with the allowance and the covers; #1124 the row mapper; #1125 the wallet header; #1126 the mounts; #1127 the 401 body; #1128 the alias trio; #1119; #1120; #1121+#1122 bash; #1123 jest; the intermittents; census; link hygiene incl. KS-1119..KS-1128; NOT-PINNED format incl. BY DESIGN; addendum per PR comma-separated under ## MERGE ADDENDUM + MG-3 + the line-number discipline) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  ten heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1124 T1, #1125 T1, #1126 T1, #1127 T1, #1128 T1, #1119 T2, #1120 T2, #1121 T2, #1122 T2, #1123 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all ten heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, TEN verdict lines"
  echo "  prompt names the report directory, the #1112-#1118 PRIOR REPORT, the #1106-#1111 EARLIER REPORT, the #1102-#1104 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1120 TWO, #1122 TWO, #1125 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b13-*) and the seat 2026-09-21_seatB-13th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4005 / :4006 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens: develop + tree, ten head trees, the all-ten tree, thirteen head blobs, 20 plant shas, 20 tamper ids, counts, the allowance, LINT-1/LINT-2/INSTR-1, the leg-14 words, :5432/:4005, archived + foreign keys, the GO subject); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names the all-ten tree and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each of the ten PRs is"
  echo "  prompt carries Wednesday eighteen by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1119_CUR_DEV:-}" ] && echo "  (develop read from the QAB1119_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1119_BRIEF:-}${QAB1119_PROMPT:-}${QAB1119_HEAD_1128:-}${QAB1119_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__ALLDEV__': ALL_OVER_DEV,
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__EARLIER__': EARLIER, '__OLDER__': OLDER, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME))}
for k, v in SUBS.items():
    n = s.count(k)
    if n == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z]+__', s)); sys.exit(2)
# 4. output controls: every carried value present as often as intended
want = {DEV: 3, ALL_OVER_DEV: 3, 'behind=0': 10, BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, EARLIER: 1, OLDER: 1,
        'exit 6': 2, 'exit 10': 4, 'exit 19': 3, 'exit 18': 4, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': 13 + len(UNCHANGED), '"ABSENT": DV': 6, ' own"': 13,
        'QAB1119_CUR_DEV': 5, 'QAB1119_HEAD_1128': 3, 'refs/pull/$_n/head': 2,
        '[QA -> Wednesday] BATCH GATE #1119-#1128 (ten PRs; tier 1 = #1124, #1125, #1126, #1127, #1128)': 1, 'PR #1119 is KS-753.': 3, 'PR #1121 is KS-957 + KS-930.': 1, 'PR #1128 is KS-1234.': 3}   # the two-key sentence sits only in the exit-32 grep (the header quotes #1119 and #1128 as the ends of the range)
for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS: want[h] = 1
got = {k: s.count(k) for k in want}
bad = {k: (got[k], want[k]) for k in want if got[k] != want[k]}
print('output controls', {(k[:28] + '…' if len(k) > 28 else k): v for k, v in got.items()})
if bad:
    for k in bad:
        for m in re.finditer(re.escape(k), s): print('   context for %r @ line %d: %r' % (k[:20], s.count('\n', 0, m.start()) + 1, s[max(0, m.start() - 70):m.end() + 15]))
    print('REFUSING: output control mismatch (got, want)', bad); sys.exit(1)
for kw in [kw for _, kws in BYNAME for kw in kws] + BOTH:
    if s.count(kw) < 1: print('REFUSING: ladder keyword missing from launcher', kw); sys.exit(1)
# heredoc parity (the PYJ block sits inside $( ) — apostrophes and parens must be even)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); end = s.index('\n' + tag[3:-2] + '\n', i)
    blk = s[i:end]
    print('heredoc', tag.strip(), '@', s.count('\n', 0, i) + 1, 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.sh', dir=os.path.dirname(OUT)); tmp.write(s); tmp.close()
p = subprocess.run(['bash', '-n', tmp.name], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp.name); sys.exit(3)
os.replace(tmp.name, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
