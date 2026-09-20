#!/usr/bin/env python3
"""gen_launcher_1106.py — write launchers/launch_qa_secuura_batch1106-1111.sh (ONE batched tier-1-floor round-1 gate over SIX file-disjoint PRs
#1106-#1111, Seat B 11th, READYs 2026-09-20T15:36:16Z-16:09:59Z) in the SHAPE of gatesets/2026-09-20_gate1105/gen_launcher_1105.py (pins re-read
at generation, tree hashing, output controls, heredoc parity, bash -n) crossed with launchers/launch_qa_secuura_batch1102_1104.sh (the multi-PR
guard ladder): exit 6 a head moved · 10 the compare per PR (merge_base + ahead + BEHIND + files — develop moving off the pin changes `behind`
and REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED detection · 7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33
prompt + READY greps · 16 overrides at launch · 21 TTY.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * origin: git ls-remote of refs/heads/develop, the six refs/pull/N/head AND the six branches — all must equal the pins;
  * local objects (rev-list / rev-parse / diff --raw / ls-tree): each head is ONE commit whose parent IS 778e6cfe2; develop cbae988db's parent IS
    778e6cfe2; the 8 (path, develop blob | ABSENT, head blob) triples as pinned; the 8 paths pairwise disjoint and disjoint from #1105's 12; every
    "unchanged read" path has the SAME blob at develop and at every head; the six head trees; the six per-PR trees over develop and the two
    all-six trees re-derived by pure tree hashing from ls-tree reads (must equal predict_batch_scratch.out's real 3-way merges);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_1106.py <output launcher>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import hashlib, itertools, os, re, subprocess, sys, tempfile
OUT = sys.argv[1]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1106', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1106to1111'
BASE = '778e6cfe2b6061d60ffcf3a57a951c84dc152b67'   # the six heads' parent = merge-base (the #1102-#1104 batch, landed)
DEV = 'cbae988dbe90ebe556459ada2cb437eaf80e2402'    # origin develop at the pin = BASE + the #1105 squash (anchoring only)
BASE_TREE = 'd0c8bfd095b65861efc1a4e8524017235b42e382'
DEV_TREE = '1f2bc512aee2a55d74142d9ba8206a795b0c975c'
ALL_OVER_BASE = 'a785e7cb93b46ac4253a13932aab0f10206cdc61'  # the seat's s-b11-batch octopus tree; drafter predict_batch_scratch.out (6 orders)
ALL_OVER_DEV = '2e981e7779dc9bcabecd099c6e93da21345a8ed0'   # the seat's item 0b; drafter predict_batch_scratch.out (6 orders)
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'; T = D + 'services/timestamping/'; S = D + 'services/security/'; P = D + 'packages/shared/'
# n, ticket, item, branch, head, head tree, tree over DEV, file count, tier
PRS = [
  ('1106', 'KS-1232', 'INFOEMPTY-1',        'refs/heads/feature/ks-1232-get-apiconnectorinfo-tells-a-connector-all-types-permitted-infoempty-1',        '2abc82d11014f00567b75a6b8fab5ec5e78f9df2', '50eb9b8683ec332b1d7caa4ee2b73552da6c6765', '4de60c4def27c21ceeb1c24843cdb8e0c0355b68', 1, 2),
  ('1107', 'KS-753',  'MOCKVERIFIED-1',     'refs/heads/feature/ks-753-timestamping-fail-closed-a-mock-tsa-fallback-must-not-report-mockverified-1',  '7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30', 'ceb6bdc7e2f101919ff81750ec6594f906680006', 'f6e218ea6fabee3fb4b78977b3fdc775dbcba0fa', 1, 2),
  ('1108', 'KS-1234', 'V1-ALIAS-BODYPARSE', 'refs/heads/feature/ks-1234-post-apiv1documents-with-applicationjson-never-answers-and-v1-alias-bodyparse-1', '4904c081c4f9be776acef78349bc10384f10de35', '83bd05b8033f2a8d15bf5af72b67d4afcd9004ff', '3d91c935f41ff9059a89a8456a713dcb42114f4f', 2, 1),
  ('1109', 'KS-1279', 'RATIO-ENVFAIL',      'refs/heads/feature/ks-1279-preflights-legs-ran-ratio-counts-leg-1-as-run-on-a-no-ratio-envfail-1',       'f592268af36b282029e50ff2fa1ebe2614304b81', 'a33bde818f2e790fd81610fa3abe9fe2f2a1c705', '44ba2d430d333130b218fe5a628e39f121b636d5', 2, 2),
  ('1110', 'KS-880',  'DEADCONV-1',         'refs/heads/feature/ks-880-quarantine-or-reconcile-the-dead-converters-copy-a-second-deadconv-1',          'a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c', '04659f893122a9b5c1edd5b98160eee90ef881db', '42641a11669e2890bc9d2baea0782b2388a8f521', 1, 1),
  ('1111', 'KS-1223', 'WALLET-1',           'refs/heads/feature/ks-1223-a-client-x-wallet-address-is-forwarded-past-the-gateway-wallet-1',             '3d1ea289a0c367af5cd0d060322e46fc900a1c76', '4a0792982a1bd8451b834d02cbe3013ee8fd2987', '1d877179f20c8a550b5ddca5599cf5f75e0895b1', 1, 1),
]
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
# 1. origin
refs_wanted = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n, *_ in PRS] + [br for _, _, _, br, *_ in PRS]
lsr = out('ls-remote', 'origin', *refs_wanted)
print('ls-remote', now('+%Y-%m-%dT%H:%M:%SZ'), '|', len(lsr.strip().splitlines()), 'refs read (want 13)')
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
want = [('refs/heads/develop', DEV)] + [('refs/pull/%s/head' % n, h) for n, _, _, _, h, *_ in PRS] + [(br, h) for _, _, _, br, h, *_ in PRS]
for ref, w in want:
    print('  %-110s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
# 2. local objects
if out('rev-list', '--parents', '-n1', DEV).split()[1:] != [BASE]: print('REFUSING: develop parent is not BASE'); sys.exit(1)
bt, dt = out('rev-parse', BASE + '^{tree}').strip(), out('rev-parse', DEV + '^{tree}').strip()
print('base tree', bt[:9], '==', BASE_TREE[:9], bt == BASE_TREE, '| develop tree', dt[:9], '==', DEV_TREE[:9], dt == DEV_TREE)
if bt != BASE_TREE or dt != DEV_TREE: sys.exit(1)
P1105 = [l for l in out('diff', '--name-only', BASE, DEV).splitlines() if l]
print('#1105 squash paths', len(P1105), '(want 12)')
if len(P1105) != 12: sys.exit(1)
CHANGED = {}   # path -> (develop blob|ABSENT, head blob, status, mode, pr)
PERPR = {}
for n, tk, item, br, h, ht, hd, nf, tier in PRS:
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    raw = out('diff', '--raw', '--abbrev=40', BASE, h).strip().splitlines()
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split()
        files[path] = ('ABSENT' if b1 == '0' * 40 else b1, b2, st, m2, n)
    print('#%s %s head %s parent==BASE %s | develop...head behind/ahead %s (want 1 1) | tree %s == pin %s | files %d (want %d) | modes %s' % (n, tk, h[:9], par == [BASE], lr, t[:9], t == ht, len(files), nf, sorted({v[3] for v in files.values()})))
    if par != [BASE] or lr != ['1', '1'] or t != ht or len(files) != nf or any(v[3] != '100644' for v in files.values()) or any(v[2] not in 'AM' for v in files.values()): sys.exit(1)
    for p_, v in files.items():
        if p_ in CHANGED: print('REFUSING: path in two PRs', p_); sys.exit(1)
        CHANGED[p_] = v
    PERPR[n] = files
print('union paths', len(CHANGED), '(want 8) | added', sum(1 for v in CHANGED.values() if v[2] == 'A'), '(want 2) | pairwise overlaps', [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])] or 'NONE (15 pairs)', '| ∩ #1105 paths', sorted(set(P1105) & set(CHANGED)) or 'NONE')
if len(CHANGED) != 8 or set(P1105) & set(CHANGED): sys.exit(1)
PINNED = {  # the drafter's shape_1.out / devpin_blobs.out reads, asserted against the live objects (develop-side blob, head blob)
  A + 'src/__tests__/ks480-connector-auth.test.ts': ('eca492723115531d8daa52d1d8b52b1b9b99970a', '16e88d9b7e00d816e6a93bfb4359e6bdc43fcb43'),
  T + 'src/__tests__/ks740-bounded-fanout.test.ts': ('a36eaa20ef8e96504a1844ba2eb16e3098f5ad0f', '6fdf0e80a46ce75c0e0f4c5540aea443779d944c'),
  A + 'src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts': ('ABSENT', '3f85887f7268a9a19fd61d73e6178bf7f6c892dc'),
  A + 'src/index.ts': ('db127dbfa5dd899b0a8e0d844690890d91e27f10', '4e7fc1174d5453f9d6f71e3a69f166fc6a08db49'),
  D + 'scripts/__tests__/preflight_ratio_excludes_leg1_no_install.test.sh': ('ABSENT', '42f43cd4393f57ece8d24ad122b5c02a438ebf17'),
  D + 'scripts/preflight/preflight.sh': ('712f895362e2c8d1ead6fd09ac257d7bce212948', 'fe29676b7073d4b6b9a71d492de962777cf5bdf8'),
  S + 'src/__tests__/row-converters.test.ts': ('17930b12b97344d23f7833dcc6de5705dde48be2', 'bde8ae21f66cdf34ae2342222cbfc6c281bec3fc'),
  A + 'src/__tests__/ks1041-vouch-header-strip.test.ts': ('a3e1631f4046288339898170bdaa1f2faff347d5', 'c92a7f85516b6b185e13ec14eec868d27f070244'),
}
for p_, (b1, b2) in PINNED.items():
    if p_ not in CHANGED or CHANGED[p_][0] != b1 or CHANGED[p_][1] != b2: print('REFUSING: pinned blob disagrees for', p_, CHANGED.get(p_)); sys.exit(1)
    bd = git('rev-parse', '-q', '--verify', DEV + ':' + p_).stdout.strip() or 'ABSENT'
    if bd != b1: print('REFUSING: develop-side blob of', p_, 'differs at', DEV[:9], bd, b1); sys.exit(1)
print('the 8 pinned (develop blob, head blob) pairs agree with the live objects at 778e6cfe2 AND at cbae988db: True')
# unchanged paths the gate reads or runs: same blob at develop and at EVERY head
UNCHANGED = [A + 'src/services/health.ts', T + 'src/index.ts', S + 'src/converters.ts', A + 'src/utils/trustHeaders.ts',
             A + 'src/routes/verification.ts', D + 'services/referral/src/routes/referrals.ts', A + 'src/__tests__/db.retry.test.ts', S + 'src/index.ts',
             S + 'src/__tests__/ks869-connector-id-persisted.test.ts', P + 'src/__tests__/ks781-p3-3-body-parser-order.test.ts',
             A + 'package.json', A + 'vitest.config.ts', A + 'vitest.setup.ts', A + 'tsconfig.json', T + 'package.json', T + 'vitest.config.ts', T + 'tsconfig.json',
             S + 'package.json', S + 'vitest.config.ts', S + 'tsconfig.json', P + 'package.json', P + 'vitest.config.ts', P + 'tsconfig.json',
             D + 'scripts/run-shell-suites.sh', '.githooks/pre-push', D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs', 'BACKLOG.md',
             D + 'services/mcp-server/src/tools/info.ts', D + 'services/mcp-server/src/http-server.ts']
DEVONLY = [D + 'docs/openapi/secuura-api.yaml']   # a #1105 path: differs at the heads by construction (they are behind develop by that squash); judged at develop only
UNCHANGED += [D + 'scripts/__tests__/%s.test.sh' % s for s in ('check_slot_credentials', 'no_tracked_credentials_root', 'pre_push_hook_base', 'pre_push_hook_current_develop', 'preflight_deps', 'preflight_failure_verdict_keeps_ratio', 'preflight_state_is_initialised', 'preflight_verdict_names_real_failures')]
UBLOB = {}
for p in UNCHANGED:
    b1 = out('rev-parse', DEV + ':' + p).strip()
    for n, *_r in PRS:
        h = _r[3]
        if out('rev-parse', h + ':' + p).strip() != b1: print('REFUSING: unchanged-read path differs at a head', p, n); sys.exit(1)
    if not re.fullmatch(r'[0-9a-f]{40}', b1): print('REFUSING: missing', p); sys.exit(1)
    UBLOB[p] = b1
print('unchanged-read paths', len(UNCHANGED), 'all same blob at develop and at every head: True')
for p in DEVONLY:
    UBLOB[p] = out('rev-parse', DEV + ':' + p).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', UBLOB[p]) or UBLOB[p] == out('rev-parse', BASE + ':' + p).strip(): print('REFUSING: DEVONLY path not a #1105-changed path', p); sys.exit(1)
print('develop-only judged paths', len(DEVONLY), '(the #1105 yaml; blob differs from BASE as expected): True')
# the four tamper files byte-unchanged from dc061f2bb (every input.json tip) through BASE to DEV
OLD = 'dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa'
for p in UNCHANGED[:4]:
    if out('rev-parse', OLD + ':' + p).strip() != UBLOB[p] or out('rev-parse', BASE + ':' + p).strip() != UBLOB[p]: print('REFUSING: tamper file moved since dc061f2bb', p); sys.exit(1)
print('the 4 tamper files identical at dc061f2bb, 778e6cfe2 and cbae988db: True')
# the #1108 product line and the #1109 script edit, by numstat
ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', BASE, PRS[2][4]).strip().splitlines()}
if ns.get(A + 'src/index.ts') != ('1', '1') or ns.get(A + 'src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts') != ('94', '0'): print('REFUSING: #1108 numstat', ns); sys.exit(1)
ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', BASE, PRS[3][4]).strip().splitlines()}
if ns.get(D + 'scripts/preflight/preflight.sh') != ('2', '1') or ns.get(D + 'scripts/__tests__/preflight_ratio_excludes_leg1_no_install.test.sh') != ('83', '0'): print('REFUSING: #1109 numstat', ns); sys.exit(1)
print('#1108 numstat 1 1 + 94 0, #1109 numstat 2 1 + 83 0: True')
# 2b. the trees re-derived WITHOUT any git write: pure tree hashing from ls-tree reads (the 1105 generator's compose)
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
for n, tk, item, br, h, ht, hd, nf, tier in PRS:
    ch = {p_: (v[3], v[1]) for p_, v in PERPR[n].items()}
    ff = compose(BASE_TREE, ch); mt = compose(DEV_TREE, ch)
    print('  #%s compose over BASE -> %s == head tree %s | over develop -> %s == pin %s' % (n, ff[:9], ff == ht, mt[:9], mt == hd))
    if ff != ht or mt != hd: sys.exit(1)
eight = {p_: (v[3], v[1]) for p_, v in CHANGED.items()}
ab = compose(BASE_TREE, eight); ad = compose(DEV_TREE, eight)
print('compose(the 8 into BASE tree) ->', ab, '==', ALL_OVER_BASE[:9], ab == ALL_OVER_BASE, '| compose(the 8 into develop tree) ->', ad, '==', ALL_OVER_DEV[:9], ad == ALL_OVER_DEV)
if ab != ALL_OVER_BASE or ad != ALL_OVER_DEV: sys.exit(1)
pm = open(os.path.join(GS, 'predict_batch_scratch.out')).read()
print('predict_batch_scratch.out: forward/reverse over both develops name the trees:', pm.count(ALL_OVER_BASE) >= 6 and pm.count(ALL_OVER_DEV) >= 6, '| read-tree controls:', ('-> ' + BASE_TREE + ' == ' + BASE_TREE) in pm and ('-> ' + DEV_TREE + ' == ' + DEV_TREE) in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm)
if not (pm.count(ALL_OVER_BASE) >= 6 and pm.count(ALL_OVER_DEV) >= 6 and 'rc=128 (want 128)' in pm): sys.exit(1)

# 3. the launcher
BRIEF = GS + '/mail_batch1106_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1106-1111.prompt.txt'
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
DEVMOVE = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-pr1105-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/'
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-90s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{"%s": "%s"}' % landed) if landed else '{}')
judged = [jline(p, v[0], (v[1], '#%s own' % v[4])) for p, v in CHANGED.items()] + [jline(p, UBLOB[p], None) for p in UNCHANGED + DEVONLY]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, tk, br, ('${QAB1106_HEAD_1111:-%s}' % h) if n == '1111' else h, nf) for n, tk, item, br, h, ht, hd, nf, tier in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=1 files=%d' % (n, nf) for n, tk, item, br, h, ht, hd, nf, tier in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER %d' \"$PROMPT_FILE\"" % (n, tk, tier) for n, tk, item, br, h, ht, hd, nf, tier in PRS)
NS_GREP = ' && '.join("grep -qF 'PR #%s is %s.' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (n, tk, n, tk) for n, tk, item, br, h, ht, hd, nf, tier in PRS)
# exit 30: seat items that must sit in BOTH the READY capture and the prompt (the seat's own figures and words)
BOTH = ['18499832', ALL_OVER_BASE, '2e981e7779dc', DEV, BASE, 'd0c8bfd095b6', '1f2bc512aee2'] + [ht for *_a, ht, hd, nf, tier in PRS] + [hd[:12] for *_a, hd, nf, tier in PRS] + [b2 for b1, b2 in PINNED.values()] + [
        'ffc1ee73959b', '518f4001c9db', '987e9d341057', '9811ba5fe34f', '734ef5eda655', '178c3b24f478', '793e0a42939a', '6e9106afb9a5',
        'NULLISHRAW', 'NOTALIST', 'VERIFIEDEQEIDAS', 'VERIFIEDNOTMOCK', 'TENANTMAPPED', 'CONNECTORMAPPED', 'WALLETINPATTERN', 'BAGDELETESWALLET',
        '678', '679', '681', '683', '42', '43', '213', '214', '907/907', '231/231', ':4006', 'INT-1', 'LINT-1', 'no-useless-assignment', 'preflight_deps', 'leg 14',
        ':5432', 'STOP-class 0', '127.0.0.1:1', 'anchoring:4005', 'localhost:6000', '203.0.113.7:443', 'shouldParseBody', 'referrals.ts:55', ':711', ':704', ':705',
        'REANCHOR', 'patch failed', '86 2', '`1 1`', '94 0', '`2 1`', '83 0', 'MG-2', 'MG-1', '1/1/2/2/1/1', 'section_1', 'section_2', 'converters.ts', 'rowToApiKey',
        'x-wallet-address', 'verified: true', 'stubs=4', 'skips are not a pass', 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub', 'mergeable_state',
        'linear[bot]', 'attachmentsForURL', 'contributes', 'Deviation from verbatim: NONE', 'bash -n', '/bin/bash', 'shellcheck', 'tools/info.ts:144', 'http-server.ts:258',
        'KS-1062', 'KS-1238', 'KS-1282', 'KS-501', 'KS-480', 'KS-740', 'KS-1041', 'KS-523', 'KS-1046', 'KS-781', 'KS-1260', 'KS-1209', 'KS-953', 'KS-741', '#995', 'TS2322', 'CAUGHT']
missing = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', missing); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
# exit 33: Wednesday's sixteen by-name items, each by its own exact phrases (all must be in the prompt)
BYNAME = [
 ('1', ['round 1 of 2', 'ZERO product bytes on #1106, #1107, #1110 and', 'ONE product line on #1108', 'ONE script edit on #1109']),
 ('2', ['DISJOINTNESS AND THE TREES, RE-DERIVED', 'at least forward and exact reverse', 'read-tree back to each develop', 'security develop baseline 213']),
 ('3', ['THE THREE SKIPPED LEGS', 'legs 3 4 8', 'skip_stack', 'would have EXERCISED these changes']),
 ('4', ['RED-FIRST PER TEST-ONLY PR', 'DEVELOP COVER measured', 'both tampers of a PR red', 'NOT routes/', 'FOUR lines :516 / :573 / :603 / :612']),
 ('5', ['THE FULL WEIGHT', 'ZERO bare `+` lines in the index.ts hunk', 'a 3 s timeout red', 'VALUE TABLE of `shouldParseBody(req)`', 'the four middlewares it now skips', ':561 runs AFTER :416-:459', 'THE TEST PINS THE ALIAS ONLY', 'ALIASWIDENINGOTHERROUTES', 'SECURITYMIDDLEWARESKIPUNPINNED', '231/231', 'develop\'s own', 'The 307: out of scope']),
 ('6', ['pins EXACTLY the strip and nothing else', 'verification.ts:1296', 'referrals.ts:55', 'WALLETFORWARDUNPINNED', 'REFERRALFALLBACKUNPINNED', 'NOT pinned BY DESIGN']),
 ('7', ['PROVE THE COPY IS DEAD', 'security/src/index.ts:418', 'LIVETENANTDEFAULT', 'fix-robust', 'MODULE ABSENCE']),
 ('8', ['DECIDES NOTHING on the 503-vs-verified:false question', 'FIX-ROBUST in that sense', '201 -> 503', "vi.doMock('../db')"]),
 ('9', ['MCPINFORAWECHO', 'HTTPSERVERINFOEMPTY', 'stale collision flag']),
 ('10', ['two-section strict apply', 'corrupt patch.diff rc 1 reproduced', 'reanchor disclosure', 'twin byte-unchanged at :712', '2 FAIL / 4 ok', '6 ok / 0 FAIL', 'INT-1: re-run preflight_deps', 'env_fail=1 now subtracts one', 'ENVFAILONLYSUBTRACTSONE']),
 ('11', ['PRE-EXISTING, CLOSED by the EARLIER REPORT', 're-run that suite SERIAL', 'report the ratio', 'RULE WHETHER IT BLOCKS']),
 ('12', ['THE CONNECTION CENSUS', 'CENSUS RULE v2', 'the baseline leg REPORTS only', 'a real Postgres listens on 127.0.0.1:5432', 'THE :4006 LISTENER']),
 ('13', ['LINEAR LINK HYGIENE', 'includeArchived', 'KS-1106', 'KS-1111', 'Completes KS-1234', 'recommend nothing']),
 ('14', ['SAME ROW FORMAT as the PRIOR REPORT', 'proposed cell', "local model's next round"]),
 ('15', ['ONE MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', '#1108 TWO, #1109', 'COMMA-separated', 'targets12.py:26', '## MERGE ADDENDUM', 'targets12.py reads report.md']),
 ('16', ["THE SEAT'S SLIPS S1 / S2 / S3 / S4 / S5 / S6", 'none reached a pushed byte']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'must not recommend pinning either', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('ZERO bare `+` lines in the index.ts hunk', 'VALUE TABLE of `shouldParseBody(req)`'), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
# every grep in the launcher is LINE-based: pre-check the namespace sentences, the tier lines and every by-name keyword as substrings of ONE line
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, item, br, h, ht, hd, nf, tier in PRS:
    if not online('PR #%s is %s.' % (n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt: PR #%s is %s.' % (n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk)); sys.exit(1)
    if not online('#%s %s: TIER %d' % (n, tk, tier), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER %d' % (n, tk, tier)); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 16 items + the closing, all present in the prompt')

L = r'''#!/bin/bash
# launch_qa_secuura_batch1106-1111.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SIX file-disjoint Secuura/Blockchain PRs
#   #1106 KS-1232 @ 2abc82d11  api-gateway VITEST test: INFOEMPTY-1, connector/info answers [] for a stored "", 0 or false — TIER 2 (test-only), pushed FIRST
#   #1107 KS-753  @ 7e7da2f88  timestamping VITEST test: MOCKVERIFIED-1, the mock TSA fallback is reported verified: true TODAY (decides nothing) — TIER 2
#   #1108 KS-1234 @ 4904c081c  api-gateway CODE PATCH: V1-ALIAS-BODYPARSE, ONE product line (index.ts:413 shouldParseBody judges the /api/v1 alias by its
#         rewritten path — a middleware-skip WIDENING on every /api/v1/<proxyPath> alias) + ONE new red-first test (94 lines) — TIER 1 (Wednesday's ruling)
#   #1109 KS-1279 @ f592268af  BASH PATCH: RATIO-ENVFAIL, ONE script line + ONE comment in scripts/preflight/preflight.sh (:704-:705, the :711 twin
#         unchanged) + ONE new bash test (83 lines) — TIER 2
#   #1110 KS-880  @ a2a7d7845  security VITEST test: DEADCONV-1, the dead converters.ts rowToApiKey maps neither tenantId nor connectorId — TIER 1 (security)
#   #1111 KS-1223 @ 3d1ea289a  api-gateway VITEST test: WALLET-1, x-wallet-address is OUTSIDE the trust-header strip — TIER 1 (the strip), pushed LAST
# #1106, #1107, #1110, #1111 are TEST-ONLY (files API + local diff-tree: 0 product bytes, 0 deleted lines); #1108 is exactly `1 1` on index.ts + `94 0`
# on the new test; #1109 exactly `2 1` on preflight.sh + `83 0` on the new test (generator-asserted by numstat).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the six heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR trees and blobs by diff --raw; the per-PR trees over develop and the two all-six trees by REAL 3-way merges in a
# --shared scratch clone in SIX orders each (predict_batch_scratch.out) AND by pure tree hashing in the generator; every BOTH-list token asserted
# present in the READY capture and the prompt at generation.
# MG-1 / MG-2 THIS ROUND: targets12.py wants exactly ONE equality target PER PR FILE (1/1/2/2/1/1) and parses the list non-greedily to the FIRST `;`
# (targets12.py:26) — the #1108 and #1109 addendum lines carry TWO targets COMMA-separated (exit 25).
# Batched under Kam 2026-09-18 standing rule. SIX verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All six tickets stay where they are (bot-walked In Progress).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + six refs/pull/N/head + six branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS 778e6cfe2 (tree d0c8bfd09, the #1102-#1104 batch tree, landed); origin develop = cbae988db (tree 1f2bc512a)
# = 778e6cfe2 + ONE squash (#1105, KS-1175 + KS-1284, anchoring only, 12 paths DISJOINT from the eight and from the four tamper files). So each PR
# over 778e6cfe2 is a fast-forward (merged tree = head tree) and over cbae988db a clean 3-way merge; compare develop...head = merge_base 778e6cfe2,
# ahead 1, BEHIND 1, files 1/1/2/2/1/1 (exit 10 — a second squash on develop changes `behind` and REFUSES: re-pin deliberately).
# Pairwise file-disjoint (8 paths: 4 modified tests, 1 product file, 1 script, 2 NEW tests; overlap 0 over 15 pairs). ALL SIX over 778e6cfe2 =
# a785e7cb93b46ac4253a13932aab0f10206cdc61 and over cbae988db = 2e981e7779dc9bcabecd099c6e93da21345a8ed0, identical in every order tried.
#
# The develop pin is judged by CONTENT — FORTY-EIGHT paths by blob at the CURRENT develop: the 8 PR paths (6 at develop blobs, 2 ABSENT; any at its
# head blob -> exit 19 LANDED, naming the PR), the 4 tamper files (health.ts, timestamping index.ts, converters.ts, trustHeaders.ts), and what the
# gate runs or reads: verification.ts + referrals.ts (the x-wallet-address readers), db.retry.test.ts (LOAD-1), security index.ts + the ks869 test
# (the LIVE rowToApiKey), the ks781 shared test, the four services' package.json / vitest.config.ts / tsconfig.json (+ api-gateway vitest.setup.ts),
# run-shell-suites.sh, the pre-push hook, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md, the spec yaml, the two MCP relay files, the
# 8 sibling bash suites.
# GUARDED: api-gateway src/ + config, timestamping src/ + config, security src/ + config, packages/shared src/ + config, referral src/routes/,
# mcp-server src/, scripts/, .githooks/, docs/openapi/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-21_gate1106to1111/mail_batch1106_ready.md, the seat's SIX READY mails (15:36:16Z … 16:09:59Z) + the 15:28:28Z STATUS
# mail, each captured verbatim by message id from wednesday-agent@ and combined in PR order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1108 T1, #1110 T1, #1111 T1, #1106 T2, #1107 T2, #1109 T2).
# exit 10: the compare per PR (merge_base 778e6cfe2, ahead 1, behind 1, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all six heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SIX verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1102-#1104), the DEVELOP-MOVE REPORT (#1105), the EARLIER REPORT
#          (#1100-#1101) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (two for #1108 and #1109, comma-separated), the
#          `## MERGE ADDENDUM` heading targets12.py parses from report.md, and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b11-*) and writing in the seat 2026-09-21_seatB-11th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4006 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, both develops and their trees, the six head trees, the
#          six per-PR trees over develop, the two all-six trees, the eight head blobs, the eight plant sha256s, the eight tamper ids, the suite
#          counts, INT-1 / LINT-1 / F2 words, the :4006 and :5432 words, the numstats, the reanchor, the archived and foreign keys), and the prompt
#          must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name BOTH all-six trees in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the six, which ticket the PR is (PR #1106 is KS-1232. … PR #1111 is KS-1223.).
# exit 33: the prompt must carry Wednesday SIXTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1106_CUR_DEV (test override, --check only): stands in for origin develop. QAB1106_HEAD_1111 (test override): stands in for #1111 pinned head.
# QAB1106_BRIEF / QAB1106_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1106_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1106to1111/gen_launcher_1106.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1105.py x launch_qa_secuura_batch1102_1104.sh.
#
# Usage: launch_qa_secuura_batch1106-1111.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1106_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1106_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation (778e6cfe2 + the #1105 squash)
MERGE_BASE='__BASE__'   # every head's parent = merge-base = the develop the seat built on
ALL_OVER_BASE='__ALLBASE__'   # all six over 778e6cfe2 (the seat's batch tree; fast-forward chain)
ALL_OVER_DEV='__ALLDEV__'     # all six over the pin cbae988db (real 3-way, six orders; generator tree-hash) — the tree that matters for the merge
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
DEVMOVE_REPORT='__DEVMOVE__'
EARLIER_REPORT='__EARLIER__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The six heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 778e6cfe2, ahead 1, behind 1 (the one
# #1105 squash), files 1/1/2/2/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
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
CUR_DEV="${QAB1106_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
T = D + "services/timestamping/"
S = D + "services/security/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the two NEW tests)
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
    print("OK " + state + " | origin develop still " + pinned + " (778e6cfe2 + the #1105 squash; every head merges clean over it; all six together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/", A + "package.json", A + "vitest.config.ts", A + "vitest.setup.ts", A + "tsconfig.json",
           T + "src/", T + "package.json", T + "vitest.config.ts", T + "tsconfig.json",
           S + "src/", S + "package.json", S + "vitest.config.ts", S + "tsconfig.json",
           P + "src/", P + "package.json", P + "vitest.config.ts", P + "tsconfig.json",
           D + "services/referral/src/routes/", D + "services/mcp-server/src/",
           D + "scripts/", ".githooks/", D + "docs/openapi/",
           D + "package.json", D + "package-lock.json", D + "eslint.config.mjs", "BACKLOG.md"]
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
tail = "the gate merges the then-current develop onto EACH of the six heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-six tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1106.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && __TIERGREP__ \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1108 T1, #1110 T1, #1111 T1, #1106 T2, #1107 T2, #1109 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1106-#1111 (six PRs; tier 1 = #1108, #1110, #1111)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SIX lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SIX verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$DEVMOVE_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the DEVELOP-MOVE REPORT $DEVMOVE_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1108 TWO, #1109' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1108 TWO, #1109 TWO, comma-separated), the ## MERGE ADDENDUM heading and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b11-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-11th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b11-*) and writing in the seat 2026-09-21_seatB-11th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4006 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4006 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in __BOTHLOOP__; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF "$ALL_OVER_BASE" "$PROMPT_FILE" && grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name both all-six trees and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #1106 is KS-1232. … PR #1111 is KS-1223.)" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday sixteen by-name items (tier/round/product bytes; the trees over both develops; the three skipped legs; red-first per test-only PR with the develop cover; #1108 the widening value table + the test pins the alias only; #1111 the strip and its two readers; #1110 the copy is dead + the live default; #1107 decides nothing + fix-robust; #1106 the MCP relays; #1109 two sections + the reanchor + INT-1 + env_fail; db.retry serial ratio + ruling; census v2 + :4006; link hygiene incl. KS-1106..KS-1111; NOT-PINNED format; addendum per PR comma-separated under ## MERGE ADDENDUM; the seat slips) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  six heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1108 T1, #1110 T1, #1111 T1, #1106 T2, #1107 T2, #1109 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all six heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SIX verdict lines"
  echo "  prompt names the report directory, the #1102-#1104 PRIOR REPORT, the #1105 DEVELOP-MOVE REPORT, the #1100-#1101 EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1108 TWO, #1109 TWO, comma-separated), the ## MERGE ADDENDUM heading and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b11-*) and the seat 2026-09-21_seatB-11th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4006 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens: both develops + trees, six head trees, six per-PR trees over develop, both all-six trees, eight head blobs, eight plant shas, eight tamper ids, counts, INT-1/LINT-1, :4006/:5432, numstats, reanchor, archived + foreign keys); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names both all-six trees and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each of the six PRs is"
  echo "  prompt carries Wednesday sixteen by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1106_CUR_DEV:-}" ] && echo "  (develop read from the QAB1106_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1106_BRIEF:-}${QAB1106_PROMPT:-}${QAB1106_HEAD_1111:-}${QAB1106_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__BASE__': BASE, '__ALLBASE__': ALL_OVER_BASE, '__ALLDEV__': ALL_OVER_DEV,
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__DEVMOVE__': DEVMOVE, '__EARLIER__': EARLIER, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME))}
for k, v in SUBS.items():
    n = s.count(k)
    if n == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z]+__', s)); sys.exit(2)
# 4. output controls: every carried value present as often as intended
# counts explained (run4 contexts): each head full ×1 (PRS only; #1111 via the override; the BOTH loop carries head BLOBS, not heads); DEV full ×2
# (DEVELOP_SHA + BOTH loop); BASE ×2 (MERGE_BASE + BOTH loop); ALL_OVER_BASE ×3 (the header's THE SHAPE line + assignment + BOTH loop); ALL_OVER_DEV
# ×2 (assignment + BOTH loop; the header carries it as 2e981e7779dc9…, the same string — counted); behind=1 ×6 (the six WANT_COMPARE lines; the
# comments say BEHIND 1); exit 10 ×4 (THE SHAPE header + the exit list + the compare comment + code); exit 19 ×3; exit 18 ×4 (exit list + empty
# CUR_DEV + PYJ comment + case); exit 30 ×4 (exit list + loop comment + loop refusal + the MEASURE refusal); exit 32 ×2; exit 33 ×2; exit 16 ×3;
# exit 21 ×3; ' own"' ×9 (8 JUDGED landed labels + the by-name keyword "develop's own"); 'PR #1106 is KS-1232.' ×3 (exit-32 header + grep + refusal).
want = {DEV: 2, BASE: 2, ALL_OVER_BASE: 3, ALL_OVER_DEV: 2, 'behind=1': 6, BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, DEVMOVE: 1, EARLIER: 1,
        'exit 6': 2, 'exit 10': 4, 'exit 19': 3, 'exit 18': 4, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': 8 + len(UNCHANGED) + len(DEVONLY), '"ABSENT": DV': 2, ' own"': 9,
        'QAB1106_CUR_DEV': 5, 'QAB1106_HEAD_1111': 3, 'refs/pull/$_n/head': 2,
        '[QA -> Wednesday] BATCH GATE #1106-#1111 (six PRs; tier 1 = #1108, #1110, #1111)': 1, 'PR #1106 is KS-1232.': 3, 'PR #1111 is KS-1223.': 3}
for n, tk, item, br, h, ht, hd, nf, tier in PRS: want[h] = 1
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
