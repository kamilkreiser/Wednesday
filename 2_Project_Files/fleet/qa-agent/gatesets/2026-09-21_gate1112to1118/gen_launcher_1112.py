#!/usr/bin/env python3
"""gen_launcher_1112.py — write launchers/launch_qa_secuura_batch1112-1118.sh (ONE batched tier-1-floor round-1 gate over SEVEN file-disjoint
TEST-ONLY PRs #1112-#1118, Seat B 12th, READYs 2026-09-20T19:53:20Z-20:29:59Z) in the SHAPE of gatesets/2026-09-21_gate1106to1111/gen_launcher_1106.py
(pins re-read at generation, tree hashing, output controls, heredoc parity, bash -n): exit 6 a head moved · 10 the compare per PR (merge_base +
ahead + BEHIND + files — develop moving off the pin changes `behind` from 0 and REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED
detection · 7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 prompt + READY greps · 16 overrides at launch · 21 TTY.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, the seven refs/pull/N/head AND the seven branches — all must equal the pins;
  * local objects (rev-list / rev-parse / diff --raw / diff --numstat / ls-tree): each head is ONE commit whose parent IS develop 362e51fe0 (NO
    develop move this round: each PR is a fast-forward, merged tree = head tree); the 11 (path, develop blob | ABSENT, head blob) triples as
    pinned; the 11 paths pairwise disjoint, every one under __tests__/, 0 deletions; every "unchanged read" path (config, locks, the ten tamper
    files, the cover-cell files) has the SAME blob at develop and at every head; the seven head trees; the all-seven tree re-derived by pure tree
    hashing from ls-tree reads (must equal predict_batch_scratch.out's real 3-way merges in six orders);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_1112.py <output launcher>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import hashlib, itertools, os, re, subprocess, sys, tempfile
OUT = sys.argv[1]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1112', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1112to1118'
DEV = '362e51fe0db7e73d5557924902763fe3f10fd8c7'    # origin develop at the pin = every head's parent (the #1106-#1111 batch landed; no move since)
DEV_TREE = '2e981e7779dc9bcabecd099c6e93da21345a8ed0'
ALL_OVER_DEV = '6aa9873f974019a92574d6db52e6356734573c8c'   # the seat's s-b12-batch octopus tree = item 0; drafter predict_batch_scratch.out (6 orders)
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; O = D + 'services/originate/'; N = D + 'services/anchoring/'; U = D + 'services/auth/'; P = D + 'packages/shared/'
# n, ticket(s), item, branch, head, head tree (= tree over develop), file count, tier, additions
PRS = [
  ('1112', 'KS-1203',           'NESTEDTYPE-1+WSTRIM-1',        'refs/heads/feature/ks-1203-a-connector-restricted-by-alloweddocumenttypes-can-still-nestedtype-wstrim-1',        '3a28d2a3c4d030cb73b7775bb19c5844ce190e56', '7b8734234ed58c55bf1ff427d6cd03fdfdc36e20', 1, 2, 8),
  ('1113', 'KS-1283',           'PROVADMIN-1',                  'refs/heads/feature/ks-1283-platformts-a-widened-super_roles-would-admit-a-tenant-admin-provadmin-1',           'abf8321a9ca426a1d623a54a41453824dce34def', '5c8e116814348c78207055424af12a43b93ab564', 1, 1, 4),
  ('1114', 'KS-1244',           'JOINEDKEY-1 + KS-1198 SKMETA-1', 'refs/heads/feature/ks-1244-a-duplicated-x-api-key-header-defeats-key-authentication-via-joinedkey-skmeta-1', '762a70117c6cf40545f8a4ac5f24708e7fcd91fe', 'c6a6a7380f1d4554de724f9a38257e0498e3a261', 1, 1, 24),
  ('1115', 'KS-1275',           'ORDERTHROUGHSPEC-1',           'refs/heads/feature/ks-1275-published-post-lifecycle-events-description-still-enumerates-orderthroughspec-1',  'b008489e4fbc72bb8b68cb3bb925557978399780', 'fea63ca447a2d2d54aada84575236780b03fa948', 1, 2, 6),
  ('1116', 'KS-1284',           'the anchoring six (+ KS-1175)', 'refs/heads/feature/ks-1284-cardanotransactionts-add_json_metadatum_with_schema-throws-anchoring-pins-1',   '9a485cfe77406f47103ed6ab65c14ec01144cb68', 'ea9fc7d7cefc2b88d7fec7b694fc1204b07f1777', 5, 2, 131),
  ('1117', 'KS-1137',           'F2-ESTATEIMAGE-1',             'refs/heads/feature/ks-1137-trivy-estate-image-1',                                                              'b3f94f14a0cf3e0236284481b85781417fd233f3', '8de2a19066c964a23b052e0db6395ea3f2bb74ec', 1, 2, 19),
  ('1118', 'KS-1006',           'WRONGCODE-1 + KS-1236 SUBMITLEVEL-1', 'refs/heads/feature/ks-1006-post-apiusersmemfadisable-skips-code-verification-when-wrongcode-submitlevel-1', 'f132c92147b5005c36e405d0116faa541d978a67', '7e75405911ec06a01839d4bcf86ccd747b4a3802', 1, 1, 24),
]
SECOND_KEY = {'1114': 'KS-1198', '1116': 'KS-1175', '1118': 'KS-1236'}
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
# 1. origin
refs_wanted = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n, *_ in PRS] + [br for _, _, _, br, *_ in PRS]
lsr = out('ls-remote', 'origin', *refs_wanted)
print('ls-remote', now('+%Y-%m-%dT%H:%M:%SZ'), '|', len(lsr.strip().splitlines()), 'refs read (want 15)')
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
want = [('refs/heads/develop', DEV)] + [('refs/pull/%s/head' % n, h) for n, _, _, _, h, *_ in PRS] + [(br, h) for _, _, _, br, h, *_ in PRS]
for ref, w in want:
    print('  %-118s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
# 2. local objects
dt = out('rev-parse', DEV + '^{tree}').strip()
print('develop tree', dt[:9], '==', DEV_TREE[:9], dt == DEV_TREE)
if dt != DEV_TREE: sys.exit(1)
CHANGED = {}   # path -> (develop blob|ABSENT, head blob, status, mode, pr)
PERPR = {}
for n, tk, item, br, h, ht, nf, tier, adds in PRS:
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
    print('#%s %s head %s parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == pin %s | files %d (want %d) | +%d/-%d (want +%d/-0) | modes %s | under __tests__/ %s' % (
        n, tk, h[:9], par == [DEV], lr, t[:9], t == ht, len(files), nf, a_sum, d_sum, adds, sorted({v[3] for v in files.values()}), all('__tests__/' in p_ for p_ in files)))
    if par != [DEV] or lr != ['0', '1'] or t != ht or len(files) != nf or a_sum != adds or d_sum != 0 or any(v[3] != '100644' for v in files.values()) or any(v[2] not in 'AM' for v in files.values()) or not all('__tests__/' in p_ for p_ in files): sys.exit(1)
    for p_, v in files.items():
        if p_ in CHANGED: print('REFUSING: path in two PRs', p_); sys.exit(1)
        CHANGED[p_] = v
    PERPR[n] = files
print('union paths', len(CHANGED), '(want 11) | added', sum(1 for v in CHANGED.values() if v[2] == 'A'), '(want 3) | pairwise overlaps', [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])] or 'NONE (21 pairs)')
if len(CHANGED) != 11: sys.exit(1)
PINNED = {  # the drafter's shape_1.out reads = the seat's GROUPING (develop-side blob, head blob), asserted against the live objects
  A + 'src/__tests__/ks501-enforcement-non-string-doctype.test.ts': ('e05c6bd21f64ad766083c72d0fc070ebeb478b7f', 'd68c6b2be95bf7c72b31903c27a0f26bbeee0332'),
  A + 'src/__tests__/ks480-org-provisioner-gate.test.ts': ('38787a194855ddb6931c81611c096cab8ec49c0d', '92966f9c1f6291e8190b139d117ce39148fc6752'),
  A + 'src/__tests__/auth.test.ts': ('72348995a66ea324ffe78dc64136f46e64985aad', '6d837e0aeeb8fdc7434033ae5d91fd018cfc5b66'),
  O + 'src/__tests__/ks978-published-contract-organizationuuid.test.ts': ('22485a7ab3c5022912bf5216e9207875bc530aa4', '27366baf325148d402822609f8ebe4d3c822724d'),
  N + 'src/__tests__/ks1175-anchor-readback.test.ts': ('05793d9254002f951e46d882510ec39e3d38dd37', 'd3d29533c9eeb962a6c1f7b3d4603b0a43658fd8'),
  N + 'src/__tests__/ks1175-identity-anchoring.test.ts': ('c3f430d783ba0d8594d962ceef13ad27325f402b', 'a6765883d409756eed8f7e73cca1dd05dd121d81'),
  N + 'src/__tests__/ks1175-getid-view-wired.test.ts': ('ABSENT', '57de9c9e24787dc33e3ec1006eae3f6640848b3f'),
  N + 'src/__tests__/ks1284-chain-read-order.test.ts': ('ABSENT', 'f461e832c5662bbe5258347654b0aa949008a1d3'),
  N + 'src/__tests__/ks1284-attach-point.test.ts': ('ABSENT', 'd42259343d79141948ff3e879f8a7b34187dcb95'),
  D + 'scripts/__tests__/container_trivy_image_filter.test.sh': ('dec2db8dee6326369ebc16cacb1f8d58287a7562', '35bbb4519950f77188ad30f3f1d46683ac63ddf5'),
  U + 'src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts': ('703c80dca84cde113b585788317f56cb5184f3d3', 'bfa8b1d3fc3611ad04266d9e520848958f2a4b55'),
}
for p_, (b1, b2) in PINNED.items():
    if p_ not in CHANGED or CHANGED[p_][0] != b1 or CHANGED[p_][1] != b2: print('REFUSING: pinned blob disagrees for', p_, CHANGED.get(p_)); sys.exit(1)
    bd = git('rev-parse', '-q', '--verify', DEV + ':' + p_).stdout.strip() or 'ABSENT'
    if bd != b1: print('REFUSING: develop-side blob of', p_, 'differs at', DEV[:9], bd, b1); sys.exit(1)
print('the 11 pinned (develop blob, head blob) pairs agree with the live objects at 362e51fe0: True')
# unchanged paths the gate reads or runs: same blob at develop and at EVERY head. The FIRST TEN are the tamper files.
TAMPER = [A + 'src/services/enforcement.ts', A + 'src/routes/platform.ts', A + 'src/middleware/auth.ts', O + 'src/originate.openapi.ts',
          N + 'src/anchorReadback.ts', N + 'src/cardano/cardanoMetadatum.ts', N + 'src/index.ts', N + 'src/cardano/transaction.ts',
          U + 'src/routes/users.ts', 'Blockchain/Testing/jobs/04-container-trivy.sh']
UNCHANGED = TAMPER + [A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts', A + 'src/__tests__/ks480-connector-auth.test.ts',
             N + 'src/__tests__/ks1284-cardano-metadatum.test.ts', N + 'src/__tests__/threadTokenMint.test.ts', A + 'src/__tests__/db.retry.test.ts',
             U + 'src/__tests__/auth.integration.test.ts', U + 'src/index.ts', O + 'src/index.ts',
             A + 'package.json', A + 'vitest.config.ts', A + 'vitest.setup.ts', A + 'tsconfig.json', A + 'package-lock.json',
             O + 'package.json', O + 'jest.config.js', O + 'tsconfig.json', O + 'package-lock.json',
             N + 'package.json', N + 'vitest.config.ts', N + 'tsconfig.json', N + 'package-lock.json',
             U + 'package.json', U + 'vitest.config.ts', U + 'tsconfig.json', U + 'package-lock.json',
             P + 'package.json', P + 'vitest.config.ts', P + 'tsconfig.json',
             D + 'scripts/run-shell-suites.sh', D + 'scripts/preflight/preflight.sh', '.githooks/pre-push', D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs',
             D + 'scripts/__tests__/aggregate_report_trivy_artefact.test.sh', D + 'scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh', D + 'scripts/__tests__/orchestrate_jobs.test.sh']
UBLOB = {}
for p in UNCHANGED:
    b1 = out('rev-parse', DEV + ':' + p).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', b1): print('REFUSING: missing', p); sys.exit(1)
    for n, *_r in PRS:
        h = _r[3]
        if out('rev-parse', h + ':' + p).strip() != b1: print('REFUSING: unchanged-read path differs at a head', p, n); sys.exit(1)
    UBLOB[p] = b1
print('unchanged-read paths', len(UNCHANGED), 'all same blob at develop and at every head: True (the first', len(TAMPER), 'are the tamper files)')
# the ten tamper files byte-unchanged from BOTH hold tips (778e6cfe2 for the five api-gateway READYs, cbae988db for the ten) to DEV
OLD1 = '778e6cfe2b6061d60ffcf3a57a951c84dc152b67'; OLD2 = 'cbae988dbe90ebe556459ada2cb437eaf80e2402'
for p in TAMPER:
    if out('rev-parse', OLD2 + ':' + p).strip() != UBLOB[p]: print('REFUSING: tamper file moved since cbae988db', p); sys.exit(1)
for p in TAMPER[:3]:
    if out('rev-parse', OLD1 + ':' + p).strip() != UBLOB[p]: print('REFUSING: api-gateway tamper file moved since 778e6cfe2', p); sys.exit(1)
print('the 10 tamper files identical at cbae988db and 362e51fe0; the 3 api-gateway ones also at 778e6cfe2: True')
# the 8 existing target paths byte-identical at their hold tips too
for p, (b1, b2) in PINNED.items():
    if b1 == 'ABSENT': continue
    hold = OLD1 if p.startswith(A) else OLD2
    if out('rev-parse', hold + ':' + p).strip() != b1: print('REFUSING: target path moved since its hold tip', p); sys.exit(1)
print('the 8 existing target paths identical at their hold tips and at 362e51fe0: True')
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
for n, tk, item, br, h, ht, nf, tier, adds in PRS:
    ch = {p_: (v[3], v[1]) for p_, v in PERPR[n].items()}
    mt = compose(DEV_TREE, ch)
    print('  #%s compose over develop -> %s == head tree %s (fast-forward)' % (n, mt[:9], mt == ht))
    if mt != ht: sys.exit(1)
eleven = {p_: (v[3], v[1]) for p_, v in CHANGED.items()}
ad = compose(DEV_TREE, eleven)
print('compose(the 11 into develop tree) ->', ad, '==', ALL_OVER_DEV[:9], ad == ALL_OVER_DEV)
if ad != ALL_OVER_DEV: sys.exit(1)
pm = open(os.path.join(GS, 'predict_batch_scratch.out')).read()
print('predict_batch_scratch.out: six orders name the tree:', pm.count(ALL_OVER_DEV) >= 7, '| read-tree control:', ('-> ' + DEV_TREE + ' == ' + DEV_TREE) in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm, '| 11 files +216:', '11 files changed, 216 insertions(+)' in pm)
if not (pm.count(ALL_OVER_DEV) >= 7 and ('-> ' + DEV_TREE + ' == ' + DEV_TREE) in pm and 'rc=128 (want 128)' in pm and '11 files changed, 216 insertions(+)' in pm): sys.exit(1)

# 3. the launcher
BRIEF = GS + '/mail_batch1112_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1112-1118.prompt.txt'
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
ANCHOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-pr1105-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-110s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{"%s": "%s"}' % landed) if landed else '{}')
judged = [jline(p, v[0], (v[1], '#%s own' % v[4])) for p, v in CHANGED.items()] + [jline(p, UBLOB[p], None) for p in UNCHANGED]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, tk, br, ('${QAB1112_HEAD_1118:-%s}' % h) if n == '1118' else h, nf) for n, tk, item, br, h, ht, nf, tier, adds in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=0 files=%d' % (n, nf) for n, tk, item, br, h, ht, nf, tier, adds in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER %d' \"$PROMPT_FILE\"" % (n, tk, tier) for n, tk, item, br, h, ht, nf, tier, adds in PRS)
def ns_sentence(n, tk): return 'PR #%s is %s.' % (n, tk) if n not in SECOND_KEY else 'PR #%s is %s + %s.' % (n, tk, SECOND_KEY[n])
NS_GREP = ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (ns_sentence(n, tk), n, tk) for n, tk, item, br, h, ht, nf, tier, adds in PRS)
# exit 30: seat items that must sit in BOTH the READY capture and the prompt (the seat's own figures and words)
BOTH = ['18499832', ALL_OVER_DEV, '2e981e7779dc', DEV, '9c8c7520b2cd'] + [ht for *_a, ht, nf, tier, adds in PRS] + [b2 for b1, b2 in PINNED.values()] + [
        '82085a23936d', '63e6537d84de', '0acfe0d608fd', '736c76413f61', 'b3757be6387c', 'df7bde2a7a39', 'f5c97a3d2437', 'e26f40eded94', 'b092b49304f4', 'eb792dee994c',
        '794830fdff2b', 'a31c8d005698', 'c0920d5a45ac', 'b23a4749fe9a', '542f8fad18b5', 'c525238074c4', '2186541ed00e', 'b59cb32248c7', 'ad1a74f801f3', '863ad55f9e69', 'fac3264f37b2', '13f6546e693a',
        'NESTEDTYPEHONOURED', 'WHITESPACETYPETRIMMED', 'WIDENROLES', 'ADMINBRANCH', 'SPLITFIRST', 'FALLTHROUGH', 'METADROPPED', 'METAWIDENED', 'REQREGREVERSED', 'RESREGREVERSED',
        'DOCIDFROMROWONLY', 'CERTIDFROMROWONLY', 'CODECJOINDROPPED', 'NETWORKINVERTED', 'MAINNETPREFIXED', 'EMPTYIDENTITYKEPT', 'GETIDVIEWDROPPED', 'GETIDVIEWWRONGSOURCE',
        'CHAINREADNODECODE', 'HASHCOMPARERAW', 'ATTACHPOINTRAW', 'TRAILINGDIGITONLY', 'KS867REVERTED', 'VERIFYINVERTED', 'PRESENCEINVERTED', 'EQUALADMITTED', 'GUARDNEVERFIRES',
        '683', '685', '684', '688', '807', '808', '328/329', '779', '782', '907/907', '5 ok / 0 FAIL', '4 ok / 0 FAIL', '18 ok', '41 passed, 0 failed (of 41)',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'login_stub', 'mergeable_state', 'stubs=4', 'INSTR-1', 'TS2339', 'TS2322', 'req.user',
        'threadTokenMint', 'per-seed policyId', 'ks1215', 'KS-1232', 'bools not allowed in metadata', 'TRIVY_JOB_SH', 'shellcheck', 'jq', '/bin/bash', 'bash -n',
        'Deviation from verbatim: NONE', 'linear[bot]', 'attachmentsForURL', 'contributes', 'GO: merge #1112-#1118 batch', 'ks-878867', 'KS-480', 'KS-721',
        ':5432', '"port":5432,', 'anchoring:4005', 'localhost:6000', '203.0.113.7:443', 'unattributed', 'x-api-key', 'connectorMeta', 'SUPER_ROLES', 'requireOrgProvisioner',
        'verifyTOTP', 'LIFECYCLE_EVENT_ACTIONS', 'anchorIdentityView', 'buildAnchorTransaction', 'handleAnchorVerifyByHash', 'dev-auth2',
        'Refs KS-1244', 'Refs KS-1198', 'Refs KS-1284', 'Refs KS-1175', 'Refs KS-1006', 'Refs KS-1236', 'F1', 'F2', 'F3', 'S1', 'S2', 'S3', 'S4', 'S5',
        'CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction',
        'KS-501', 'KS-978', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-1194', 'KS-1136', 'KS-753', 'KS-1205', 'KS-1171',
        'KS-1172', 'KS-1133', 'KS-794', 'KS-1215', 'KS-1273', 'KS-1274', 'KS-932', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953', '#995', 'cardano-serialization-lib', '<= 92 chars',
        'Nothing failed', 'quarantine', 'both orders', 'pairwise overlaps NONE']
# (the READYs TRUNCATE quoted cell titles at ~80 chars, so 'dev-m365-integration:latest', 'BAD_REQUEST', 'Invalid verification code', 'UNKNOWN_DOCUMENT_TYPE',
#  'provisionerKind' sit in the prompt and the PR bodies but not in the mail capture; 'app.listen' is the drafter's read, not the seat's — none is a BOTH token)
missing = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', missing); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
# exit 33: Wednesday's seventeen by-name items, each by its own exact phrases (all must be in the prompt)
BYNAME = [
 ('1', ['round 1 of 2', 'ZERO product bytes on ALL SEVEN', '0 files outside `__tests__/`', 'files API union 11']),
 ('2', ['DISJOINTNESS AND THE TREES, RE-DERIVED', 'at least forward and exact reverse', 'read-tree back to develop', 'fast-forward = its head tree', 'auth develop baseline 779']),
 ('3', ['THE THREE SKIPPED LEGS', 'legs 3, 4, 8', 'skip_stack', 'would have EXERCISED these changes']),
 ('4', ['RED-FIRST PER PR UNDER THE COVER RULE', 'DEVELOP COVER measured FIRST', 'reds == declared ∪ measured cover', 'ONE named sibling allowance', 'LEAD F1', 'LEAD F2', 'LEAD F3', 'GRADE F1', 'GRADE F2', 'GRADE F3', 'NEW = N - 1', '27/27 by exact-line count']),
 ('5', ['THE GUARD AND ITS MOUNT', 'PROVMOUNTUNPINNED', 'SUPERADMINROUTESWIDEN', 'fake req/res', ':489 -> :91 -> :97']),
 ('6', ['THE API-KEY PATH', 'OPTIONALMOUNTJOINEDKEY', 'INSTR-1 reproduced', 'Request augmentation', 'in either order']),
 ('7', ['THE TWO ROUTES', 'FALSYMFASECRETDOOR', 'STALEAPPROVALPATH', 'before any store read', ':4003 discipline']),
 ('8', ['THE RATIO, THE COVERS, THE THREE NEW FILES', 'a second red is a finding', 'GETIDROUTEBOOTLESS', 'source guard reds on text, not behaviour', 'prove CSL resolved in']),
 ('9', ["offset-4 apply after NESTEDTYPE", 'EARLIER rows it CLOSES']),
 ('10', ['reads the REGISTERED schemas', 'DESCRIPTIONVERBLIST', 'jest `fullName`']),
 ('11', ['TRIVY_JOB_SH copies', 'NONLATESTTAGEXCLUDED', 'jq absent rc 2']),
 ('12', ['THE db.retry INTERMITTENT AND LOAD-2', 're-run that suite SERIAL', 'RULE WHETHER IT BLOCKS', 'deterministic, develop\'s own']),
 ('13', ['THE CONNECTION CENSUS', 'CENSUS RULE v2', 'the baseline leg REPORTS only', 'a real Postgres listens on 127.0.0.1:5432', 'identical A/B totals']),
 ('14', ['LINEAR LINK HYGIENE', 'includeArchived', 'KS-1112', 'KS-1118', 'Completes KS-1244', 'recommend nothing', 'the seat elided']),
 ('15', ['SAME ROW FORMAT as the PRIOR REPORT', 'proposed cell', "local model's next round", 'BY DESIGN']),
 ('16', ['ONE MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', '#1116 FIVE', 'COMMA-separated', 'targets13.py:28', '## MERGE ADDENDUM', 'targets13.py reads', 'MG-3 KEY-SET rule', 'merge13.py:58']),
 ('17', ["THE SEAT'S SLIPS S1 / S2 / S3 / S4 / S5", 'none reached a pushed byte', 'THE LINE-NUMBER DISCIPLINE', 'NAME WHO INHERITED IT']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'must not recommend pinning either', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree', 'lsof -nP -iTCP:4003 -sTCP:LISTEN', 'lsof -nP -iTCP:4005 -sTCP:LISTEN']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('jest `fullName`', '0 files outside `__tests__/`', '## MERGE ADDENDUM'), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, item, br, h, ht, nf, tier, adds in PRS:
    if not online(ns_sentence(n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt:', ns_sentence(n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk)); sys.exit(1)
    if not online('#%s %s: TIER %d' % (n, tk, tier), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER %d' % (n, tk, tier)); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 17 items + the closing, all present in the prompt')

L = r'''#!/bin/bash
# launch_qa_secuura_batch1112-1118.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SEVEN file-disjoint TEST-ONLY
# Secuura/Blockchain PRs (Seat B 12th; fifteen local-model patches grouped by FILE into seven PRs across FIVE lanes)
#   #1112 PR A KS-1203 @ 3a28d2a3c  api-gateway VITEST test: NESTEDTYPE-1+WSTRIM-1 (+8, one file, two cells) — TIER 2, pushed FIRST
#   #1113 PR B KS-1283 @ abf8321a9  api-gateway VITEST test: PROVADMIN-1 (+4, the requireOrgProvisioner guard) — TIER 1 (Wednesday's ruling)
#   #1114 PR C KS-1244 + KS-1198 @ 762a70117  api-gateway VITEST test: JOINEDKEY-1 + SKMETA-1 (+24, auth.test.ts) — TIER 1 (authenticateToken)
#   #1115 PR D KS-1275 @ b008489e4  originate JEST test: ORDERTHROUGHSPEC-1 (+6) — TIER 2
#   #1116 PR E KS-1284 + KS-1175 @ 9a485cfe7  anchoring VITEST tests: the anchoring six (+131 over FIVE files, three NEW) — TIER 2
#   #1117 PR G KS-1137 @ b3f94f14a  BASH suite: F2-ESTATEIMAGE-1 (+19, container_trivy_image_filter.test.sh) — TIER 2
#   #1118 PR F KS-1006 + KS-1236 @ f132c9214  the AUTH service VITEST test: WRONGCODE-1 + SUBMITLEVEL-1 (+24) — TIER 1 (the auth service), pushed LAST
# ALL SEVEN are TEST-ONLY (files API + local diff --raw: 11 paths, every one under __tests__/, +216/-0, 8 M + 3 A — generator-asserted by numstat).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the seven heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the seven head trees (= the trees over develop: each head's parent IS develop, a
# fast-forward) and the all-seven tree by REAL 3-way merges in a --shared scratch clone in SIX orders (predict_batch_scratch.out) AND by pure tree
# hashing in the generator; every BOTH-list token asserted present in the READY capture and the prompt at generation.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets13.py wants exactly ONE equality target PER PR FILE (1/1/1/1/5/1/1) and parses the list non-greedily to the
# FIRST `;` (targets13.py:28) — the #1116 addendum line carries FIVE targets COMMA-separated (exit 25); merge13.py:58-:64 asserts each squash body's
# key set == the PR's OWN Refs set (two keys on #1114, #1116, #1118).
# Batched under Kam 2026-09-18 standing rule. SEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All ten tickets stay where they are (In Progress; bot-walked or already).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + seven refs/pull/N/head + seven branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS origin develop 362e51fe0 (tree 2e981e777, the #1106-#1111 batch landed) — NO develop move under these heads,
# so each PR over develop is a fast-forward (merged tree = head tree); compare develop...head = merge_base 362e51fe0, ahead 1, BEHIND 0, files
# 1/1/1/1/5/1/1 (exit 10 — a squash on develop changes `behind` and REFUSES: re-pin deliberately). Pairwise file-disjoint (11 paths: 8 modified
# tests, 3 NEW tests; overlap 0 over 21 pairs). ALL SEVEN over 362e51fe0 = 6aa9873f974019a92574d6db52e6356734573c8c, identical in every order tried.
#
# The develop pin is judged by CONTENT — FIFTY-TWO paths by blob at the CURRENT develop: the 11 PR paths (8 at develop blobs, 3 ABSENT; any at its
# head blob -> exit 19 LANDED, naming the PR), the 10 tamper files (enforcement.ts, platform.ts, middleware/auth.ts, originate.openapi.ts,
# anchorReadback.ts, cardanoMetadatum.ts, anchoring index.ts, transaction.ts, users.ts, 04-container-trivy.sh), and what the gate runs or reads:
# the three cover-cell files (ks1215, ks480-connector-auth, ks1284-cardano-metadatum), threadTokenMint.test.ts (the pre-existing red), db.retry
# (LOAD-1), auth.integration.test.ts + the auth / originate index.ts (the :4003 / :4000 listens), the five packages' package.json / config /
# tsconfig / lock, run-shell-suites.sh, preflight.sh, the pre-push hook, the Dev package.json + lock, eslint.config.mjs, the 3 sibling trivy suites.
# GUARDED: api-gateway src/ + config, originate src/ + config, anchoring src/ + config, auth src/ + config, packages/shared src/ + config,
# scripts/, .githooks/, Blockchain/Testing/jobs/, the Dev package.json + lock, eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate1112to1118/mail_batch1112_ready.md, the seat's SEVEN READY mails (19:53:20Z … 20:29:59Z) + the 19:34:31Z STATUS
# mail + the 18:45:57Z plan-confirmation mail, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1113 T1, #1114 T1, #1118 T1, #1112 T2, #1115 T2, #1116 T2, #1117 T2).
# exit 10: the compare per PR (merge_base 362e51fe0, ahead 1, behind 0, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all seven heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1106-#1111), the ANCHORING REPORT (#1105), the EARLIER REPORT
#          (#1102-#1104) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (FIVE for #1116, comma-separated), the
#          `## MERGE ADDENDUM` heading targets13.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b12-*) and writing in the seat 2026-09-21_seatB-12th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4005 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, develop and its tree, the seven head trees, the
#          all-seven tree, the eleven head blobs, the 22 plant sha256s the READYs carry, the 27 tamper ids, the suite counts, the three covers'
#          words F1 / F2 / F3 and INSTR-1, the :5432 and :4005 words, the archived and foreign keys, the GO subject), and the prompt must ask the
#          gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-seven tree in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the seven, which ticket(s) the PR is (PR #1112 is KS-1203. … PR #1118 is KS-1006 + KS-1236.).
# exit 33: the prompt must carry Wednesday SEVENTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1112_CUR_DEV (test override, --check only): stands in for origin develop. QAB1112_HEAD_1118 (test override): stands in for #1118 pinned head.
# QAB1112_BRIEF / QAB1112_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1112_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1112to1118/gen_launcher_1112.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1106.py.
#
# Usage: launch_qa_secuura_batch1112-1118.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1112_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1112_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation = every head's parent (no develop move this round)
MERGE_BASE='__DEV__'    # every head's parent = merge-base = develop itself
ALL_OVER_DEV='__ALLDEV__'     # all seven over the pin 362e51fe0 (real 3-way, six orders; generator tree-hash) — the tree that matters for the merge
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
ANCHOR_REPORT='__ANCHOR__'
EARLIER_REPORT='__EARLIER__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The seven heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 362e51fe0, ahead 1, behind 0 (no develop
# move), files 1/1/1/1/5/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
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
CUR_DEV="${QAB1112_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
N = D + "services/anchoring/"
U = D + "services/auth/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the three NEW tests)
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
    print("OK " + state + " | origin develop still " + pinned + " (every head parent; every head a fast-forward over it; all seven together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/", A + "package.json", A + "vitest.config.ts", A + "vitest.setup.ts", A + "tsconfig.json", A + "package-lock.json",
           O + "src/", O + "package.json", O + "jest.config.js", O + "tsconfig.json", O + "package-lock.json",
           N + "src/", N + "package.json", N + "vitest.config.ts", N + "tsconfig.json", N + "package-lock.json",
           U + "src/", U + "package.json", U + "vitest.config.ts", U + "tsconfig.json", U + "package-lock.json",
           P + "src/", P + "package.json", P + "vitest.config.ts", P + "tsconfig.json",
           D + "scripts/", ".githooks/", "Blockchain/Testing/jobs/",
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
tail = "the gate merges the then-current develop onto EACH of the seven heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-seven tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1112.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && __TIERGREP__ \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1113 T1, #1114 T1, #1118 T1, #1112 T2, #1115 T2, #1116 T2, #1117 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1112-#1118 (seven PRs; tier 1 = #1113, #1114, #1118)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SEVEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$ANCHOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the ANCHORING REPORT $ANCHOR_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1116 FIVE' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1116 FIVE, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b12-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-12th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b12-*) and writing in the seat 2026-09-21_seatB-12th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4005 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in __BOTHLOOP__; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-seven tree and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1112 is KS-1203. … PR #1118 is KS-1006 + KS-1236.)" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday seventeen by-name items (tier/round/product bytes; the trees and disjointness; the three skipped legs; red-first under the cover rule with F1 / F2 / F3 graded; #1113 the guard and its mount; #1114 the api-key path + INSTR-1; #1118 the two routes; #1116 the ratio, covers and three new files; #1112; #1115 jest; #1117 bash; db.retry + LOAD-2; census v2 + :4003/:4005; link hygiene incl. KS-1112..KS-1118; NOT-PINNED format incl. BY DESIGN; addendum per PR comma-separated under ## MERGE ADDENDUM + MG-3; the seat slips + the line-number discipline) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  seven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1113 T1, #1114 T1, #1118 T1, #1112 T2, #1115 T2, #1116 T2, #1117 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all seven heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SEVEN verdict lines"
  echo "  prompt names the report directory, the #1106-#1111 PRIOR REPORT, the #1105 ANCHORING REPORT, the #1102-#1104 EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1116 FIVE, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b12-*) and the seat 2026-09-21_seatB-12th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4005 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens: develop + tree, seven head trees, the all-seven tree, eleven head blobs, 22 plant shas, 27 tamper ids, counts, F1/F2/F3/INSTR-1, :5432/:4005, archived + foreign keys, the GO subject); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names the all-seven tree and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each of the seven PRs is"
  echo "  prompt carries Wednesday seventeen by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1112_CUR_DEV:-}" ] && echo "  (develop read from the QAB1112_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1112_BRIEF:-}${QAB1112_PROMPT:-}${QAB1112_HEAD_1118:-}${QAB1112_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__ALLDEV__': ALL_OVER_DEV,
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__ANCHOR__': ANCHOR, '__EARLIER__': EARLIER, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME))}
for k, v in SUBS.items():
    n = s.count(k)
    if n == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z]+__', s)); sys.exit(2)
# 4. output controls: every carried value present as often as intended
# counts explained: each head full x1 (PRS only; #1118 via the override; the BOTH loop carries head BLOBS + head TREES, not heads); DEV full x3
# (DEVELOP_SHA + MERGE_BASE + BOTH loop); ALL_OVER_DEV x3 (the header's THE SHAPE line + assignment + BOTH loop); behind=0 x7 (the seven
# WANT_COMPARE lines; the comments say BEHIND 0); exit 10 x4 (THE SHAPE header + the exit list + the compare comment + code); exit 19 x3; exit 18
# x4 (exit list + empty CUR_DEV + PYJ comment + case); exit 30 x4 (exit list + loop comment + loop refusal + the MEASURE refusal); exit 32 x2;
# exit 33 x2; exit 16 x3; exit 21 x3; ' own"' x12 (11 JUDGED landed labels + the by-name keyword "deterministic, develop's own"); 'PR #1112 is
# KS-1203.' x3 (exit-32 header + grep + refusal).
want = {DEV: 3, ALL_OVER_DEV: 3, 'behind=0': 7, BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, ANCHOR: 1, EARLIER: 1,
        'exit 6': 2, 'exit 10': 4, 'exit 19': 3, 'exit 18': 4, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': 11 + len(UNCHANGED), '"ABSENT": DV': 3, ' own"': 12,
        'QAB1112_CUR_DEV': 5, 'QAB1112_HEAD_1118': 3, 'refs/pull/$_n/head': 2,
        '[QA -> Wednesday] BATCH GATE #1112-#1118 (seven PRs; tier 1 = #1113, #1114, #1118)': 1, 'PR #1112 is KS-1203.': 3, 'PR #1118 is KS-1006 + KS-1236.': 3}
for n, tk, item, br, h, ht, nf, tier, adds in PRS: want[h] = 1
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
