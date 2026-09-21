#!/usr/bin/env python3
"""gen_launcher_1130.py — write launchers/launch_qa_secuura_batch1130-<last>.sh (ONE batched tier-1-floor round-1 gate over SIX Secuura/Blockchain
PRs #1130-#<last>, Seat B 14th: five TEST-ONLY patches + ONE bash_patch with two product lines on the re-link PUSH GUARD; READYs
2026-09-21T08:56:14Z-…) in the SHAPE of gatesets/2026-09-21_gate1119to1128/gen_launcher_1119.py (pins re-read at generation, tree hashing, output
controls, heredoc parity, bash -n): exit 6 a head moved · 10 the compare per PR (merge_base + ahead + BEHIND + files — develop moving off the pin
changes `behind` from 0 and REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED detection · 7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33
prompt + READY greps · 16 overrides at launch · 21 TTY.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * the six PR numbers and heads come from the captured READY mails (mail_seatB14_ready*_pr<N>_*.md) and are asserted against the pinned trees;
  * origin: git ls-remote of refs/heads/develop, the six refs/pull/N/head AND the six branches — all must equal the pins;
  * local objects (rev-list / rev-parse / diff --raw / diff --numstat / ls-tree): each head is ONE commit whose parent IS develop 9f0265eb0 (NO
    develop move this round: each PR is a fast-forward, merged tree = head tree); the 6 (path, develop blob | ABSENT, head blob) triples as
    pinned; the six paths pairwise disjoint EXCEPT the PR 3 / PR 5 pair on ONE file (asserted exactly that pair), five under __tests__/ + the ONE
    guard path on PR 6 only, deletions 1/1/2/0/1/0; every "unchanged read" path (config, locks, the four other tamper files, the siblings) has the
    SAME blob at develop and at every head; the six head trees; the all-six tree re-derived by pure tree hashing from ls-tree reads with the PAIR
    blob on the shared path (must equal predict_batch_scratch_*.out's real 3-way merges in six orders);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_1130.py <output launcher>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import glob, hashlib, itertools, os, re, subprocess, sys, tempfile
OUT = sys.argv[1]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1130', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135'
DEV = '9f0265eb06ecf24d4de18149ce862ad2330a61ee'    # origin develop at the pin = every head's parent (the #1119-#1128 batch landed; no move since)
DEV_TREE = '23d60cace7c37bc329ccc425e58659e950089a4d'
ALL_OVER_DEV = '60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b'   # the seat's s-b14-batch octopus tree = item 0; drafter predict_batch_scratch (6 orders)
PAIR_TREE = '9e5dec6aef2070de26d1450c961f531572ee8f57'; PAIR_BLOB = 'dcd3efaaf45a26bb4324b656ef62e79685462600'
D = 'Blockchain/Dev/'; S = D + 'services/security/'; AU = D + 'services/auth/'; SC = D + 'scripts/'; P = D + 'packages/shared/'
GUARD = SC + 'check-shared-relink.sh'; SHARED = S + 'src/__tests__/ks869-connector-id-persisted.test.ts'
# seat PR -> (ticket(s), item, branch, head tree (= tree over develop), file count, tier, additions, deletions); the PR NUMBER and HEAD come from the READYs
SEAT = {
  '1': (['KS-1273'], 'TRIVYYAMLEXITCODE-1', 'refs/heads/feature/ks-1273-job-04-a-trivy_exit_code-or-trivyyaml-exit-code-in-the-trivyyamlexitcode-1', 'ff4427e75a4dbc62943b23dd6e1e8560ccd13ce0', 1, 2, 8, 1),
  '2': (['KS-1135'], 'MANIFESTQUARANTINESTDERR-1', 'refs/heads/feature/ks-1135-run-shell-suitessh-fails-6-of-25-suites-under-a-long-tmpdir-manifestquarantinestderr-1', '2088fe31d9ffd6ee8b0693ca3c5d73fbc8d59233', 1, 2, 1, 1),
  '6': (['KS-958'], 'KS-958 (bash_patch)', 'refs/heads/feature/ks-958-the-re-link-guard-matches-the-js-runtime-name-case-1', 'c531a4e6bb680fd91b8b1795552aa8890759fb61', 2, 1, 86, 2),
  '3': (['KS-880'], 'OTHERMAPPERDEFAULT-1', 'refs/heads/feature/ks-880-quarantine-or-reconcile-the-dead-converters-copy-a-second-othermapperdefault-1', '2fba2bc1c6157476a3287de7d6cf061946b3c894', 1, 1, 8, 0),
  '5': (['KS-887'], 'KS-887 (modify-in-place)', 'refs/heads/feature/ks-887-test-defect-mine-the-write-half-column-list-pin-can-modifyinplace-1', '8af100d484836ea87081767b64299c4416e889c6', 1, 1, 5, 1),
  '4': (['KS-1236', 'KS-1006'], 'ALREADYPENDING-1 + MFANOTENABLED-1', 'refs/heads/feature/ks-1236-approving-a-stale-pending-verification-request-after-the-alreadypending-mfanotenabled-1', '009a8116db0d18dfb63d3357220a478d09c2b49e', 1, 1, 32, 0),
}
PUSH = ['1', '2', '6', '3', '5', '4']
READY = {}
for f in sorted(glob.glob(os.path.join(GS, 'mail_seatB14_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 14th\): PR (\d) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(4))
if any(p not in READY for p in PUSH): print('REFUSING: READY missing for seat PR', [p for p in PUSH if p not in READY]); sys.exit(1)
# n, ticket(s), item, branch, head, head tree, nfiles, tier, adds, dels — in push order
PRS = [(READY[p][0], SEAT[p][0], SEAT[p][1], SEAT[p][2], READY[p][1], SEAT[p][3], SEAT[p][4], SEAT[p][5], SEAT[p][6], SEAT[p][7]) for p in PUSH]
N = {p: READY[p][0] for p in PUSH}; LAST = N['4']
if int(LAST) != max(int(n) for n, *_ in PRS): print('REFUSING: PR 4 is not the highest number'); sys.exit(1)
print('PR numbers (push order 1 2 6 3 5 4):', [n for n, *_ in PRS], '| last', LAST)
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
    print('  %-122s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
# 2. local objects
dt = out('rev-parse', DEV + '^{tree}').strip()
print('develop tree', dt[:9], '==', DEV_TREE[:9], dt == DEV_TREE)
if dt != DEV_TREE: sys.exit(1)
CHANGED = {}; PERPR = {}; OWNERS = {}
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
        n, '+'.join(tk), h[:9], par == [DEV], lr, t[:9], t == ht, len(files), nf, a_sum, d_sum, adds, dels, sorted({v[3] for v in files.values()}), non_test or 'NONE'))
    ok_modes = all(v[3] == ('100755' if p_ in (GUARD, 'systemTest/__tests__/manifest_quarantine.test.sh') else '100644') for p_, v in files.items())
    ok_nontest = (non_test == [GUARD]) if n == N['6'] else (non_test == [])
    if par != [DEV] or lr != ['0', '1'] or t != ht or len(files) != nf or a_sum != adds or d_sum != dels or not ok_modes or any(v[2] not in 'AM' for v in files.values()) or not ok_nontest: sys.exit(1)
    for p_, v in files.items():
        OWNERS.setdefault(p_, []).append(n)
        if p_ in CHANGED and p_ != SHARED: print('REFUSING: path in two PRs', p_); sys.exit(1)
        CHANGED[p_] = v
    PERPR[n] = files
overl = [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])]
print('union paths', len(CHANGED), '(want 6) | added', sum(1 for v in CHANGED.values() if v[2] == 'A'), '(want 1) | pairwise overlaps', overl, '(want exactly the PR 3 / PR 5 pair on the ks869 file)')
if len(CHANGED) != 6 or overl != [(N['3'], N['5'])] or OWNERS[SHARED] != [N['3'], N['5']]: sys.exit(1)
PINNED = {  # the drafter's shape_2.out reads = the seat's GROUPING (develop-side blob, head blob per PR), asserted against the live objects
  SC + '__tests__/container_trivy_exit_code_env_keeps_findings.test.sh': ('d119e64ba755', 'fa63512f6fc234b061c2d7352fabd0124d9b6f89'),
  'systemTest/__tests__/manifest_quarantine.test.sh': ('2ae67f244ddd', '8d21c7e127bb97220df90997bb560bcf29dd89cf'),
  GUARD: ('d41c79538503', '4e0704b6c7b9f4db2ceebf0530015e3b2f469662'),
  SC + '__tests__/check_shared_relink_case.test.sh': ('ABSENT', '9a16088ca5e3c9043cf82ec54f26204e516e62f9'),
  SHARED: ('f452db039b9d', 'f796e9527537a786ed17ef12bdf433b96d1dda8a'),   # CHANGED holds PR 5's (the later in push order); PR 3's is 789dff0cde0b
  AU + 'src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts': ('bfa8b1d3fc36', '5273baafd36714a30403b1bdf55cd2318acc587c'),
}
PR3_BLOB = '789dff0cde0b54d4ecbdf83ead67cd897a5326ee'
if PERPR[N['3']][SHARED][1] != PR3_BLOB: print('REFUSING: PR 3 blob', PERPR[N['3']][SHARED][1]); sys.exit(1)
FULLDEV = {}
for p_, (b1, b2) in PINNED.items():
    if p_ not in CHANGED or not CHANGED[p_][0].startswith(b1) or CHANGED[p_][1] != b2: print('REFUSING: pinned blob disagrees for', p_, CHANGED.get(p_)); sys.exit(1)
    bd = git('rev-parse', '-q', '--verify', DEV + ':' + p_).stdout.strip() or 'ABSENT'
    if not bd.startswith(b1): print('REFUSING: develop-side blob of', p_, 'differs at', DEV[:9], bd, b1); sys.exit(1)
    FULLDEV[p_] = bd
print('the 6 pinned (develop blob, head blob) pairs (+ PR 3 blob 789dff0cde0b on the shared file) agree with the live objects at 9f0265eb0: True')
# unchanged paths the gate reads or runs: same blob at develop and at EVERY head. The FIRST FOUR are the tamper files (the guard is PR 6's TARGET, not here).
TAMPER = ['Blockchain/Testing/jobs/04-container-trivy.sh', 'systemTest/fixtures/manifest.ts', S + 'src/index.ts', AU + 'src/routes/users.ts']
UNCHANGED = TAMPER + [SC + '__tests__/container_trivy_image_filter.test.sh', SC + '__tests__/container_trivy_failed_scan_is_loud.test.sh', SC + '__tests__/check_shared_relink.test.sh',
             SC + '__tests__/check_shared_relink_tooling_tokens.test.sh', SC + '__tests__/ks949_main_seed_idempotence.test.sh', SC + '__tests__/preflight_deps.test.sh',
             SC + 'run-shell-suites.sh', SC + 'preflight/preflight.sh', SC + 'fix-libsodium-symlink.js', SC + 'run-code-guards.sh', '.githooks/pre-push',
             S + 'package.json', S + 'vitest.config.ts', S + 'tsconfig.json', S + 'package-lock.json',
             AU + 'package.json', AU + 'vitest.config.ts', AU + 'tsconfig.json', AU + 'package-lock.json', AU + 'src/index.ts',
             P + 'package.json', P + 'vitest.config.ts', P + 'tsconfig.json', D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs']
UBLOB = {}
for p_ in UNCHANGED:
    b1 = out('rev-parse', DEV + ':' + p_).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', b1): print('REFUSING: missing', p_); sys.exit(1)
    for n, *_r in PRS:
        h = _r[3]
        if out('rev-parse', h + ':' + p_).strip() != b1: print('REFUSING: unchanged-read path differs at a head', p_, n); sys.exit(1)
    UBLOB[p_] = b1
print('unchanged-read paths', len(UNCHANGED), 'all same blob at develop and at every head: True (the first', len(TAMPER), 'are the tamper files)')
# hold tips: the two ks1194 READYs were held at 7be81d5c9 (target + users.ts unchanged since); KS-887 / KS-958 at 48e65c435 (index.ts + the guard unchanged; the ks869 test CHANGED by #1124)
OLD = '7be81d5c9b109959b559e03652fb092c12de58e8'; OLDER = '48e65c435'
for p_ in (AU + 'src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts', AU + 'src/routes/users.ts'):
    if out('rev-parse', OLD + ':' + p_).strip() != (FULLDEV.get(p_) or UBLOB.get(p_)): print('REFUSING: ks1194 path moved since 7be81d5c9', p_); sys.exit(1)
for p_ in (S + 'src/index.ts', GUARD):
    if out('rev-parse', OLDER + ':' + p_).strip() != (FULLDEV.get(p_) or UBLOB.get(p_)): print('REFUSING: KS-887/KS-958 anchor moved since 48e65c435', p_); sys.exit(1)
if out('rev-parse', OLDER + ':' + SHARED).strip() == FULLDEV[SHARED]: print('REFUSING: expected #1124 to have changed the ks869 test since 48e65c435'); sys.exit(1)
print('the ks1194 pair identical at 7be81d5c9 and 9f0265eb0; index.ts + the guard identical at 48e65c435 and 9f0265eb0; the ks869 test differs at 48e65c435 (#1124): True')
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
pair = compose(DEV_TREE, {SHARED: ('100644', PAIR_BLOB)})
print('compose(the pair blob into develop tree) ->', pair[:9], '== PAIR_TREE', pair == PAIR_TREE)
if pair != PAIR_TREE: sys.exit(1)
six = {p_: (v[3], v[1]) for p_, v in CHANGED.items()}; six[SHARED] = ('100644', PAIR_BLOB)
ad = compose(DEV_TREE, six)
print('compose(the 6 into develop tree, the pair blob on the shared file) ->', ad, '==', ALL_OVER_DEV[:9], ad == ALL_OVER_DEV)
if ad != ALL_OVER_DEV: sys.exit(1)
pms = sorted(glob.glob(os.path.join(GS, 'predict_batch_scratch_*.out')))
pm = open(pms[-1]).read()
print('newest predict_batch_scratch out:', os.path.basename(pms[-1]), '| six orders name the tree:', pm.count(ALL_OVER_DEV) >= 7, '| all orders identical: True:', 'all orders identical: True' in pm, '| read-tree control:', ('-> ' + DEV_TREE + ' == ' + DEV_TREE + ' True') in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm, '| 6 files +140/-5:', '6 files changed, 140 insertions(+), 5 deletions(-)' in pm, '| pair:', ('== seat pair tree %s: True' % PAIR_TREE) in pm, '| byte-identical:', 'byte-identical to before: True' in pm)
if not (pm.count(ALL_OVER_DEV) >= 7 and 'all orders identical: True' in pm and ('-> ' + DEV_TREE + ' == ' + DEV_TREE + ' True') in pm and 'rc=128 (want 128)' in pm and '6 files changed, 140 insertions(+), 5 deletions(-)' in pm and ('== seat pair tree %s: True' % PAIR_TREE) in pm and 'byte-identical to before: True' in pm): sys.exit(1)

# 3. the launcher
BRIEF = GS + '/mail_batch1130_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1130-%s.prompt.txt' % LAST
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-%s-tier1-r1/' % LAST
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
OLDER_R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
for d_ in (PRIOR, EARLIER, OLDER_R):
    if not os.path.isdir(d_): print('REFUSING: report dir absent', d_); sys.exit(1)
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
if 'NOT YET ARRIVED' in brief_txt: print('REFUSING: the combined capture has a section NOT YET ARRIVED'); sys.exit(1)
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-118s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{' + ', '.join('"%s": "%s"' % x for x in landed) + '}') if landed else '{}')
judged = []
for p_, v in CHANGED.items():
    if p_ == SHARED: judged.append(jline(p_, v[0], [(PR3_BLOB, '#%s own' % N['3']), (v[1], '#%s own' % N['5']), (PAIR_BLOB, '#%s + #%s (the pair)' % (N['3'], N['5']))]))
    else: judged.append(jline(p_, v[0], [(v[1], '#%s own' % v[4])]))
judged += [jline(p_, UBLOB[p_], None) for p_ in UNCHANGED]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, '+'.join(tk), br, ('${QAB1130_HEAD_%s:-%s}' % (LAST, h)) if n == LAST else h, nf) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=0 files=%d' % (n, nf) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER %d' \"$PROMPT_FILE\"" % (n, ' + '.join(tk), tier) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
def ns_sentence(n, tk): return 'PR #%s is %s.' % (n, ' + '.join(tk))
NS_GREP = ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (ns_sentence(n, tk), n, tk[0]) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
TIER_LIST = ', '.join('#%s T%d' % (n, tier) for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS)
SUBJECT = '[QA -> Wednesday] BATCH GATE #1130-#%s (six PRs; tier 1 = #%s, #%s, #%s, #%s)' % (LAST, N['6'], N['3'], N['5'], N['4'])
# exit 30: seat items that must sit in BOTH the READY capture and the prompt (the seat's own figures and words)
# (the three auth cell bodies — 'A verification request is already pending' etc. — sit in the brief + prompt, NOT in the READY capture: by-name words, not BOTH tokens)
# (the READYs print the pair tree / blob as 12-hex prefixes — those two enter the BOTH list by prefix)
BOTH = ['18499832', ALL_OVER_DEV, '23d60cace7c3', DEV, 'cecbb9a62653', PAIR_TREE[:12], PAIR_BLOB[:12], '6eeef3623e8a'] + [ht for *_a, ht, nf, tier, adds, dels in PRS] + [
        'fa63512f6fc2', '8d21c7e127bb', '4e0704b6c7b9', '9a16088ca5e3', '789dff0cde0b', 'f796e9527537', '5273baafd367',
        '0720a4bfa4a4', 'f38ad737419a', 'e461d3795550', 'cbc37764f051', 'e2b088f924d6', '67e4f8b38833', 'e417c05bf5d0', 'c97ddc96b6ab',
        'EXITCODEFLAGGONE', 'DRIVERTHROWS', 'AUDITTENANTRAW', 'GUARDTOLOG', 'SAMETARGETONLY', 'MFAOFFIDEMPOTENT', 'LENGTHDROPPED', 'CONNECTORIDDROPPED',
        '216/216', '786/786', '215/215', '782/782', '6 ok / 0 FAIL', '5 ok / 0 FAIL', '3 ok / 0 FAIL', '14 ok / 0 FAIL', '3 ok / 2 FAIL', '3 ok / 3 FAIL', '7 ok / 7 FAIL',
        '2 passed, 4 failed, 0 skipped', '6 passed, 0 failed, 0 skipped', '106 passed, 0 failed', '56 passed, 0 failed', '27 passed, 0 failed (of 27 cells)',
        '43 passed, 0 failed (of 43)', '44 passed, 0 failed (of 44)', '42 passed, 1 failed (of 43)',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'login_stub', 'mergeable_state', 'stubs=4', 'NO PREFLIGHT VERDICT', 'ran NO legs',
        'PROTOCOL-DIFF', 'PROTOCOL-CLEAN', 'packages/shared is not built', 'ks949_main_seed_idempotence', 'deps15b', 'S6',
        '--recount', 'corrupt patch at line 7', 'golden', '85a7a98230b4', '87bb65f6f302', 'driver stderr (tail -40 of driver.err',
        'wrapModuleLoad', 'KS-1135 tamper: the quarantine aborted for a September stamp', 'npm_config_offline=true', 'tsx v4.23.15',
        'section_1', 'section_2', 'patch failed', 'tolower(L)', 'expected exit 1, got 0', 'NODE_ENV=production', 'latent, closed', 'push guard',
        '--directory=Blockchain/Dev', 'does not exist in index', 'connector_id)', 'WRITE half', 'COALESCE', 'ks-869',
        'flag > env > config', 'TRIVY_EXIT_CODE', '--exit-code 0', 'trivy.yaml', 'CRITICAL=1 HIGH=1', 'could not scan',
        'rowToAuditLog', 'rowToApiKey', 'DEFAULT_TENANT',
        'TS2322', 'typecheck15', 'eslint', 'linear[bot]', 'attachmentsForURL', 'contributes', 'Refs KS-1006', 'Refs KS-1236',
        ':5432', '127.0.0.1', 'netlog.cjs', 'STOP-class 0', 'jq', '/bin/bash', 'bash -n', 'shellcheck',
        'KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
        'KS-869', 'KS-1194', 'KS-1136', 'KS-1137', 'KS-957', 'KS-930', 'KS-969', 'KS-973', 'KS-1203', 'KS-1198', 'KS-1284', 'KS-1175', 'KS-1215', 'KS-753', 'KS-1232', 'KS-1223', 'KS-1234', 'KS-1283', 'KS-1244', 'KS-1275', 'KS-1279', 'KS-1272', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953',
        'Nothing failed', '<= 92 chars', 'Deviation from verbatim', 'GO: merge #1130-#%s batch' % LAST, 'unrendered', 'CORRECTION',
        'TRIVYYAMLEXITCODE-1', 'MANIFESTQUARANTINESTDERR-1', 'OTHERMAPPERDEFAULT-1', 'ALREADYPENDING-1', 'MFANOTENABLED-1', 'KS-958', 'KS-887']
missing = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', [(t, online(t, brief_txt.splitlines()), online(t, prompt_txt.splitlines())) for t in missing]); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
# exit 33: Wednesday's seventeen by-name items, each by its own exact phrases (all must be in the prompt)
BYNAME = [
 ('1', ['round 1 of 2', 'ZERO product bytes on FIVE', 'EXACTLY the two paths on #%s' % N['6'], 'files API union 6']),
 ('2', ['DISJOINTNESS AND THE TREES, RE-DERIVED', 'at least forward and exact reverse', 'read-tree back to develop', 'fast-forward = its head tree', 'every count from the RUNNER', 'the PAIR needs its own proof']),
 ('3', ['CANONICAL-PATCH IDENTITY', 'both roads, both rcs quoted', 'the two recheck sections in both orders', 'Name any byte that differs']),
 ('4', ['RED-FIRST PER PR UNDER THE COVER RULE', 'DEVELOP COVER measured FIRST', 'reds == declared ∪ measured cover', '7/7 by exact-line-block AND raw-substring', 'TWO-line blocks', 'THE TWO-READY FRAME', 'RED-FIRST / GREEN-AFTER', 'THE PRODUCT BYTES GRADED ON THEIR OWN']),
 ('5', ['THE PRODUCT BYTES:', 'preflight LEG 13', 'SHARED_RELINK_STRICT=1', 'mode 100644 vs the 15 executable siblings', 'completeness detector fires 0/1/0']),
 ('6', ['THE OTHER MAPPER', 'THIRDMAPPERDEFAULT', 'rowToAuditLog(` at :374']),
 ('7', ['THE WRITE-HALF CELL, MODIFY-IN-PLACE', 'A2 needed --recount', 'SAME-FILE\n    PAIR'.replace('\n    ', ' '), "Kam's own ticket"]),
 ('8', ['THE AUTH GUARDS', 'two drives, one cell', 'STALEAPPROVALPATH / FALSYMFASECRETDOOR', "auth's FIRST census set"]),
 ('9', ["THE STUB'S trivy.yaml ARM", 'which trivy', 'the `jq` FATAL control', 'REALTRIVYCONFIGARM']),
 ('10', ['THE DIAGNOSTIC AND THE UNGATED PUSH', 'NO PREFLIGHT VERDICT on its push', 'design or a gap', 'SYSTEMTESTPUSHUNGATED']),
 ('11', ['THE INTERMITTENTS', 're-run it standalone 3× serial', 'RULE WHETHER IT BLOCKS', 'one finding, two or three']),
 ('12', ['THE CONNECTION CENSUS', '30 vs 10', ':4003 / :4004 / :4005 / :4006']),
 ('13', ['LINEAR LINK HYGIENE', 'includeArchived', 'KS-1129', 'KS-1137', 'Completes KS-1273', 'recommend nothing', 'PR #887 is OPEN and is KS-961']),
 ('14', ['SAME ROW FORMAT as the PRIOR REPORT', 'proposed cell', "local model's next round", 'BY DESIGN', 'FOUR prior rows CLOSE here']),
 ('15', ['ONE MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', '#%s TWO' % N['6'], 'COMMA-separated', '## MERGE ADDENDUM', 'MG-3 KEY-SET', 'merge15.py:58', "THE PAIR'S ADDENDUM", 'THE LINE-NUMBER DISCIPLINE', 'NAME WHO INHERITED IT']),
 ('16', ['"FOR THE GATE TO MEASURE" ITEMS map onto the above', 'the commit subjects <= 92 chars']),
 ('17', ['THE CENSUS RULE, THE NAMESPACE GUARD AND report.md BEFORE THE MAIL', '"port":5432,', 'KS-1135 = PR 2']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'must not recommend pinning either', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree', 'lsof -nP -iTCP:4003 -sTCP:LISTEN', 'lsof -nP -iTCP:4004 -sTCP:LISTEN', 'lsof -nP -iTCP:5432 -sTCP:LISTEN', 'GATEWAY_URL=http://127.0.0.1:']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('## MERGE ADDENDUM', 'rowToAuditLog(` at :374', 'the `jq` FATAL control'), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, item, br, h, ht, nf, tier, adds, dels in PRS:
    if not online(ns_sentence(n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt:', ns_sentence(n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk[0] in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk[0])); sys.exit(1)
    if not online('#%s %s: TIER %d' % (n, ' + '.join(tk), tier), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER %d' % (n, ' + '.join(tk), tier)); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 17 items + the closing, all present in the prompt')

HEADER_LINES = '\n'.join('#   #%s PR %s %s @ %s  %s — TIER %d%s' % (n, p, ' + '.join(SEAT[p][0]), READY[p][1][:9], {
    '1': 'scripts BASH suite (MODIFY): TRIVYYAMLEXITCODE-1 (+8/-1, the suite\'s own trivy stub + one cell)', '2': 'systemTest BASH suite (MODIFY): MANIFESTQUARANTINESTDERR-1 (+1/-1, cleanup() diagnostic, NO cell)',
    '6': 'bash_patch: the round\'s ONLY PRODUCT bytes on Blockchain/Dev/scripts/check-shared-relink.sh (-2/+2, a PUSH GUARD) + one NEW suite (+84)', '3': 'security VITEST test: OTHERMAPPERDEFAULT-1 (+8, rowToAuditLog)',
    '5': 'security VITEST test: KS-887 modify-in-place of PR 3\'s OWN file (+5/-1, the WRITE-half cell)', '4': 'auth VITEST test: ALREADYPENDING-1 + MFANOTENABLED-1 (+32, one file, two READYs, two tickets)'}[p], SEAT[p][5],
    {'1': ', pushed FIRST', '4': ', pushed LAST', '6': ' (pushed THIRD)', '3': '', '5': ' (after PR 3, same file)', '2': ''}[p]) for p, n in ((p, N[p]) for p in PUSH))

L = r'''#!/bin/bash
# launch_qa_secuura_batch1130-__LAST__.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SIX Secuura/Blockchain PRs
# (Seat B 14th; seven local-model patches grouped by FILE SET into six PRs across THREE lanes — five file-disjoint plus ONE same-file pair)
__HEADERLINES__
# FIVE are TEST-ONLY and #__N6__ carries EXACTLY the two paths (files API + local diff --raw: 6 paths, 5 under __tests__/ + the guard, +140/-5,
# 5 M + 1 A — generator-asserted by numstat; the guard and the manifest suite are mode 100755).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the six heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the six head trees (= the trees over develop: each head's parent IS develop, a fast-forward)
# and the all-six tree by REAL 3-way merges in a --shared scratch clone in SIX orders (predict_batch_scratch_*.out) AND by pure tree hashing in the
# generator (the PAIR blob dcd3efaaf45a on the shared ks869 file); every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets15.py wants exactly ONE equality target PER PR FILE (1/1/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` (targets15.py:28) — the #__N6__ addendum line carries TWO targets COMMA-separated (exit 25); merge15.py:54-:65
# asserts each squash body's key set == the PR's OWN Refs set (two keys on #__N4__ only).
# Batched under Kam 2026-09-18 standing rule. SIX verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All seven tickets stay where they are (In Progress; bot-walked or already).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + six refs/pull/N/head + six branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS origin develop 9f0265eb0 (tree 23d60cace7c3, the #1119-#1128 batch landed) — NO develop move under these
# heads, so each PR over develop is a fast-forward (merged tree = head tree); compare develop...head = merge_base 9f0265eb0, ahead 1, BEHIND 0,
# files 1/1/2/1/1/1 (exit 10 — a squash on develop changes `behind` and REFUSES: re-pin deliberately). Pairwise file-disjoint EXCEPT the PR 3 / PR 5
# pair on ks869-connector-id-persisted.test.ts (disjoint hunks; both orders one blob dcd3efaaf45a). ALL SIX over 9f0265eb0 =
# __ALLDEV__, identical in every order tried; the PAIR alone __PAIRTREE__.
#
# The develop pin is judged by CONTENT — THIRTY-THREE paths by blob at the CURRENT develop: the 6 PR paths (5 at develop blobs, 1 ABSENT; any at
# a head blob or at the PAIR blob -> exit 19 LANDED, naming the PR), the 4 other tamper files (the trivy job, manifest.ts, security index.ts,
# users.ts), and what the gate runs or reads: the six bash siblings, run-shell-suites.sh, preflight.sh, run-code-guards.sh, fix-libsodium-symlink.js,
# the pre-push hook, security's and auth's package.json / config / tsconfig / lock, auth index.ts, packages/shared's, the Dev package.json + lock,
# eslint.config.mjs.
# GUARDED: security/ + auth/ src + config, packages/shared, scripts/, systemTest/, .githooks/, Blockchain/Testing/jobs/, the Dev package.json + lock,
# eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate1130to1135/mail_batch1130_ready.md, the seat's SIX READY mails (08:56:14Z … ) + the 09:24:08Z CORRECTION to
# READY 5 + the 08:33:52Z STATUS mail + the 08:00:58Z plan-confirmation mail + the 08:43:18Z PR 1 leg-14 QUESTION mail, each captured verbatim by
# message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (__TIERLIST__).
# exit 10: the compare per PR (merge_base 9f0265eb0, ahead 1, behind 0, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all six heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SIX verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1119-#1128), the EARLIER REPORT (#1112-#1118), the OLDER REPORT
#          (#1106-#1111) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (TWO for #__N6__, comma-separated),
#          the `## MERGE ADDENDUM` heading targets15.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b14-*) and writing in the seat 2026-09-21_seatB-14th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, develop and its tree, the six head trees, the
#          all-six tree, the pair tree + blob, the seven head blobs, the 8 plant sha256s, the 8 tamper ids, the suite counts, the S6 words, the
#          --recount / golden words, the NO PREFLIGHT VERDICT words, the :5432 words, the archived and foreign keys, the GO subject, the
#          CORRECTION), and the prompt must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-six tree in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the six, which ticket(s) the PR is (PR #1130 is KS-1273. … PR #__N4__ is KS-1236 + KS-1006.).
# exit 33: the prompt must carry Wednesday SEVENTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1130_CUR_DEV (test override, --check only): stands in for origin develop. QAB1130_HEAD___LAST__ (test override): stands in for #__LAST__ pinned head.
# QAB1130_BRIEF / QAB1130_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1130_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1130to1135/gen_launcher_1130.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1119.py.
#
# Usage: launch_qa_secuura_batch1130-__LAST__.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1130_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1130_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket(s)|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation = every head's parent (no develop move this round)
MERGE_BASE='__DEV__'    # every head's parent = merge-base = develop itself
ALL_OVER_DEV='__ALLDEV__'     # all six over the pin 9f0265eb0 (real 3-way, six orders; generator tree-hash with the pair blob) — the tree that matters for the merge
PAIR_TREE='__PAIRTREE__'      # PR 3 + PR 5 both orders over the pin
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
EARLIER_REPORT='__EARLIER__'
OLDER_REPORT='__OLDER__'
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 9f0265eb0, ahead 1, behind 0 (no develop
# move), files 1/1/2/1/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
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
CUR_DEV="${QAB1130_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
S = D + "services/security/"
AU = D + "services/auth/"
SC = D + "scripts/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the one NEW suite)
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
    print("OK " + state + " | origin develop still " + pinned + " (every head parent; every head a fast-forward over it; all six together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [S + "src/", S + "package.json", S + "vitest.config.ts", S + "tsconfig.json", S + "package-lock.json",
           AU + "src/", AU + "package.json", AU + "vitest.config.ts", AU + "tsconfig.json", AU + "package-lock.json",
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
tail = "the gate merges the then-current develop onto EACH of the six heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-six tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1130.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && __TIERGREP__ \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (__TIERLIST__)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SIX lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SIX verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#__N6__ TWO' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 KEY-SET' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#__N6__ TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b14-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-14th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b14-*) and writing in the seat 2026-09-21_seatB-14th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in __BOTHLOOP__; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$PAIR_TREE" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-six tree, the pair tree and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1130 is KS-1273. … PR #__N4__ is KS-1236 + KS-1006.)" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday seventeen by-name items (tier/round/product bytes; the trees, the pair and disjointness; canonical-patch identity; red-first under the cover rule with the two declared covers and PR 4 frame; #__N6__ the product bytes; #__N3__ the other mapper; #__N5__ the write-half cell; #__N4__ the auth guards; #1130 the stub; #1131 the diagnostic + the ungated push; the intermittents; census; link hygiene incl. KS-1129..KS-1137; NOT-PINNED format incl. BY DESIGN; addendum per PR comma-separated under ## MERGE ADDENDUM + MG-3 + the pair + the line-number discipline; the seat items; the census/namespace/report.md restatement) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  six heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (__TIERLIST__); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all six heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SIX verdict lines"
  echo "  prompt names the report directory, the #1119-#1128 PRIOR REPORT, the #1112-#1118 EARLIER REPORT, the #1106-#1111 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#__N6__ TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b14-*) and the seat 2026-09-21_seatB-14th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens: develop + tree, six head trees, the all-six tree, the pair tree + blob, seven head blobs, 8 plant shas, 8 tamper ids, counts, S6, --recount/golden, NO PREFLIGHT VERDICT, :5432, archived + foreign keys, the GO subject, the CORRECTION); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the all-six tree, the pair tree and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each of the six PRs is"
  echo "  prompt carries Wednesday seventeen by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1130_CUR_DEV:-}" ] && echo "  (develop read from the QAB1130_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1130_BRIEF:-}${QAB1130_PROMPT:-}${QAB1130_HEAD___LAST__:-}${QAB1130_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
__ENTERQA__ || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__HEADERLINES__': HEADER_LINES, '__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__ALLDEV__': ALL_OVER_DEV, '__PAIRTREE__': PAIR_TREE,
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__EARLIER__': EARLIER, '__OLDER__': OLDER_R, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME)),
        '__TIERLIST__': TIER_LIST, '__SUBJECT__': SUBJECT, '__LAST__': LAST, '__N6__': N['6'], '__N3__': N['3'], '__N5__': N['5'], '__N4__': N['4'],
        '__ENTERQA__': 'c' + 'd' + ' "$QA_DIR"'}
for k, v in SUBS.items():
    n_ = s.count(k)
    if n_ == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z0-9]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z0-9]+__', s)); sys.exit(2)
# 4. output controls: every carried value present as often as intended
want = {DEV: 3, ALL_OVER_DEV: 3, PAIR_TREE: 2, 'behind=0': 6, BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, EARLIER: 1, OLDER_R: 1,
        'exit 6': 2, 'exit 10': 4, 'exit 19': 3, 'exit 18': 4, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': 6 + len(UNCHANGED), '"ABSENT": DV': 1, ' own"': 7, '(the pair)"': 1,
        'QAB1130_CUR_DEV': 5, 'QAB1130_HEAD_' + LAST: 3, 'refs/pull/$_n/head': 2,
        SUBJECT: 1, 'PR #1130 is KS-1273.': 3, 'PR #%s is KS-1236 + KS-1006.' % N['4']: 3, 'PR #%s is KS-887.' % N['5']: 1}
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
