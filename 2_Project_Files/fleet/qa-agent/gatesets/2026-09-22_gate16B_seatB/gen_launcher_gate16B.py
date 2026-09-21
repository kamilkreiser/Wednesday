#!/usr/bin/env python3
"""gen_launcher_gate16B.py — write launchers/launch_qa_secuura_batch1147-1161.sh (ONE batched round-1 gate over EIGHT Secuura/Blockchain PRs #1147
#1149 #1151 #1153 #1155 #1157 #1159 #1161, Seat B 16th: eight R15 TEST-ONLY PRs, tier-2 floor + tier 1 on #1161; READYs 2026-09-21T17:01:06Z-18:31:47Z)
in the SHAPE of gatesets/2026-09-21_gate15_docs_comments/gen_launcher_gate15.py (pins re-read at generation, tree hashing, output controls, heredoc
parity, bash -n): exit 6 a head moved · 10 the compare per PR (merge_base = the heads' parent 64ab10513, ahead 1, BEHIND = the develop move count at
generation (0: unmoved), files 1 — develop moving changes `behind` and REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED detection
(seven NEW targets judged ABSENT; the ks1213 file by blob; the 9 tamper files + the 15th's five + the hook / preflight / lane configs unchanged) ·
the prompt + READY greps · 16 overrides at launch · 21 TTY · 34 a PENDING-PR- marker (inherited; never expected this round).
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * the PR numbers and heads come from round16B.py AND the captured READY mails AND origin (git ls-remote of refs/heads/develop, every refs/pull/N/head
    AND branch) — all three must agree;
  * local objects (rev-list / rev-parse / diff --raw / diff --numstat / ls-tree): each head is ONE commit whose parent IS 64ab10513; the (path, develop
    blob or ABSENT, head blob) pairs as pinned; the paths pairwise disjoint; every path under __tests__/; every unchanged-read path has the SAME blob at
    64ab10513, at the CURRENT develop (read in the scratch clone — argv[2]) and at every head; the per-PR trees; the eight-PR tree over 64ab10513 by
    pure tree hashing (must equal c54c1ae73ba3… and predict_batch_scratch_*.out);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_gate16B.py <output launcher> <scratch clone holding the current develop by SHA>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import glob, hashlib, itertools, json, os, re, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16B as R
OUT = sys.argv[1]; SCR = sys.argv[2]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date'] + (['-u'] if f.endswith('Z') else []) + [f], capture_output=True, text=True).stdout.strip()   # gate15 S2: a Z-suffixed format is read with -u
print('gen_launcher_gate16B', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = R.REPO; GS = G
PARENT = R.DEV; PARENT_TREE = R.DEV_TREE; ALL_OVER_PARENT = R.SEAT_ALL8
D = R.D; SH = R.SH; OR = R.OR; SE = R.SE; AN = R.AN; AG = D + 'services/api-gateway/'; AU = D + 'services/auth/'; SC = D + 'scripts/'
READY = {}
for f in sorted(glob.glob(os.path.join(GS, 'mail_seatB16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(4))
present = [p for p in R.PUSH if p in READY]; missing = [p for p in R.PUSH if p not in READY]
print('READYs captured for seat PRs', present, '| missing', missing or 'none')
if missing: print('REFUSING: this round has no PARTIAL form — every READY landed before the drafter began; a missing capture is a capture fault'); sys.exit(1)
for p in R.PUSH:
    if READY[p] != (R.PRS[p]['n'], R.PRS[p]['head']): print('REFUSING: the READY for seat PR', p, 'disagrees with round16B', READY[p], (R.PRS[p]['n'], R.PRS[p]['head'])); sys.exit(1)
# n, key, tags, branch, head, head tree, nfiles, adds, dels, files, p, tier
PRS = [(R.PRS[p]['n'], R.PRS[p]['key'], R.PRS[p]['tags'], R.PRS[p]['branch'], R.PRS[p]['head'], R.PRS[p]['tree'], 1, R.PRS[p]['adds'], R.PRS[p]['dels'], [R.PRS[p]['file']], p, 1 if p == '9' else 2) for p in R.PUSH]
LAST = PRS[-1][0]; FIRST = PRS[0][0]
print('PR numbers (push order):', [n for n, *_ in PRS], '| first', FIRST, 'last', LAST)
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
def sgit(*a): return subprocess.run(['git', '-C', SCR] + list(a), capture_output=True, text=True).stdout.strip()
# 1. origin
refs_wanted = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n, *_ in PRS] + [br for _, _, _, br, *_ in PRS] + ['refs/heads/feature/ks-1171-*']
lsr = out('ls-remote', 'origin', *refs_wanted)
print('ls-remote', now('+%Y-%m-%dT%H:%M:%SZ'), '|', len(lsr.strip().splitlines()), 'refs read (want %d; the ks-1171 glob must return NOTHING)' % (len(refs_wanted) - 1))
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
DEV = refs.get('refs/heads/develop', '?')
print('origin develop NOW (the pin):', DEV, '| the heads parent', PARENT[:9], '| moved since the raise:', DEV != PARENT)
if not re.fullmatch(r'[0-9a-f]{40}', DEV): sys.exit(1)
held = [k for k in refs if 'ks-1171' in k]
if held: print('REFUSING: a ks-1171 branch is at origin — the HELD PR was pushed; a different gate:', held); sys.exit(1)
print('the HELD KS-1171 branch ABSENT at origin: True')
want = [('refs/pull/%s/head' % n, h) for n, _, _, _, h, *_ in PRS] + [(br, h) for _, _, _, br, h, *_ in PRS]
for ref, w in want:
    print('  %-140s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
if subprocess.run(['git', '-C', SCR, 'cat-file', '-e', DEV + '^{commit}']).returncode: print('REFUSING: the current develop', DEV[:9], 'is not in the scratch clone', SCR, '- re-run predict_batch_scratch_gate16B.py'); sys.exit(1)
DEV_TREE = sgit('rev-parse', DEV + '^{tree}'); BEHIND = int(sgit('rev-list', '--count', PARENT + '..' + DEV) or '0'); MB = sgit('merge-base', PARENT, DEV)
print('current develop tree', DEV_TREE[:12], '| rev-list --count parent..develop =', BEHIND, '| merge-base(parent, develop) == parent:', MB == PARENT)
if MB != PARENT: sys.exit(1)
BLOBS = {R.PRS[p]['file']: (R.PRS[p]['dev_blob'], R.PRS[p]['blob'][:12]) for p in R.PUSH}   # dev_blob None = ABSENT at develop
TAMPERS = [x[0] for x in R.TAMPER_BLOBS]
moved = set(sgit('diff', '--name-only', PARENT, DEV).splitlines()); print('develop move touches', len(moved), 'paths; ∩ the 8 target paths:', sorted(moved & set(BLOBS)) or 'NONE', '| ∩ the 9 tamper files:', sorted(moved & set(TAMPERS)) or 'NONE')
if moved & (set(BLOBS) | set(TAMPERS)): print('REFUSING: the develop move touches a target or tamper path'); sys.exit(1)
# 2. local objects
dt = out('rev-parse', PARENT + '^{tree}').strip(); print('parent tree', dt[:9], '==', PARENT_TREE[:9], dt == PARENT_TREE)
if dt != PARENT_TREE: sys.exit(1)
CHANGED = {}; PERPR = {}
for n, tk, tags, br, h, ht, nf, adds, dels, files_want, p, tier in PRS:
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', PARENT + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    raw = out('diff', '--raw', '--abbrev=40', PARENT, h).strip().splitlines()
    ns = {l.split('\t')[2]: (int(l.split('\t')[0]), int(l.split('\t')[1])) for l in out('diff', '--numstat', PARENT, h).strip().splitlines()}
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); files[path] = (b1, b2, st, m2, n)
    a_sum = sum(v[0] for v in ns.values()); d_sum = sum(v[1] for v in ns.values())
    ok_kind = all('/__tests__/' in x for x in files)
    print('#%s PR %s %s head %s parent==PARENT %s | parent...head behind/ahead %s (want 0 1) | tree %s == pin %s | files %s == %s | +%d/-%d (want +%d/-%d) | modes %s | status %s | every path __tests__/: %s | tier %d' % (
        n, p, tk, h[:9], par == [PARENT], lr, t[:12], t == ht, [x.split('/')[-1] for x in files], sorted(files) == sorted(files_want), a_sum, d_sum, adds, dels, sorted({v[3] for v in files.values()}), sorted(v[2] for v in files.values()), ok_kind, tier))
    if par != [PARENT] or lr != ['0', '1'] or t != ht or sorted(files) != sorted(files_want) or a_sum != adds or d_sum != dels or any(v[3] != '100644' for v in files.values()) or not ok_kind: sys.exit(1)
    for p_, v in files.items():
        if p_ in CHANGED: print('REFUSING: path in two PRs', p_); sys.exit(1)
        want_dev = BLOBS[p_][0]
        if (want_dev is None and v[2] != 'A') or (want_dev is not None and (v[2] != 'M' or not v[0].startswith(want_dev))) or not v[1].startswith(BLOBS[p_][1]): print('REFUSING: pinned blob / status disagrees for', p_, v[:3]); sys.exit(1)
        CHANGED[p_] = v
    PERPR[n] = files
overl = [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])]
print('union paths', len(CHANGED), '(want 8) | pairwise overlaps', overl, '(want none)')
if overl or len(CHANGED) != 8: sys.exit(1)
FULLDEV = {}
for p_ in BLOBS:
    if BLOBS[p_][0] is None:
        if git('cat-file', '-e', PARENT + ':' + p_).returncode == 0 or subprocess.run(['git', '-C', SCR, 'cat-file', '-e', DEV + ':' + p_], capture_output=True).returncode == 0: print('REFUSING: a NEW target exists at the parent or the current develop', p_); sys.exit(1)
        FULLDEV[p_] = 'ABSENT'
    else:
        bd = out('rev-parse', PARENT + ':' + p_).strip(); bc = sgit('rev-parse', DEV + ':' + p_)
        if not bd.startswith(BLOBS[p_][0]) or bc != bd: print('REFUSING: target blob differs at the parent or the current develop', p_, bd[:12], bc[:12]); sys.exit(1)
        FULLDEV[p_] = bd
print('the 8 (develop blob | ABSENT) values agree at 64ab10513 AND at the current develop; the head blobs agree with the RECOUNT column: True')
TAMPER15 = ['Blockchain/Testing/jobs/04-container-trivy.sh', 'systemTest/fixtures/manifest.ts', SE + 'src/index.ts', AU + 'src/routes/users.ts', SC + 'check-shared-relink.sh']
UNCHANGED = TAMPERS + TAMPER15 + ['.githooks/pre-push', SC + 'preflight/preflight.sh', SC + 'run-shell-suites.sh', SC + 'fix-libsodium-symlink.js',
             AU + 'src/services/jwt.ts', OR + 'src/services/provenance.ts', AG + 'src/routes/proxy.ts',
             OR + 'src/__tests__/ks1004-anchor-failed-lockout.test.ts', AN + 'src/__tests__/threadTokenMint.test.ts',
             SH + 'package.json', SH + 'vitest.config.ts', SH + 'tsconfig.json',
             OR + 'package.json', OR + 'tsconfig.json', OR + 'jest.config.js', OR + 'package-lock.json',
             SE + 'package.json', SE + 'vitest.config.ts', SE + 'tsconfig.json', SE + 'package-lock.json',
             AN + 'package.json', AN + 'vitest.config.ts', AN + 'tsconfig.json', AN + 'package-lock.json',
             D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs']
UBLOB = {}
for p_ in list(UNCHANGED):
    b1 = git('rev-parse', '-q', '--verify', PARENT + ':' + p_).stdout.strip()
    if not re.fullmatch(r'[0-9a-f]{40}', b1):
        print('  (unchanged-read path absent at the parent, dropped from the list:', p_, ')'); UNCHANGED.remove(p_); continue
    if sgit('rev-parse', DEV + ':' + p_) != b1: print('REFUSING: unchanged-read path differs at the current develop', p_); sys.exit(1)
    for n, *_r in PRS:
        h = _r[3]
        if out('rev-parse', h + ':' + p_).strip() != b1: print('REFUSING: unchanged-read path differs at a head', p_, n); sys.exit(1)
    UBLOB[p_] = b1
print('unchanged-read paths', len(UNCHANGED), 'all same blob at the parent, at the current develop and at every head: True (the first', len(TAMPERS), 'are this round\'s tamper files, the next', len(TAMPER15), 'the 15th\'s)')
# 2b. trees by pure hashing
def ls_tree(oid, where=REPO):
    ents = []
    for l in subprocess.run(['git', '-C', where, 'ls-tree', oid], capture_output=True, text=True).stdout.strip().splitlines():
        meta, name = l.split('\t', 1); mode, typ, sha = meta.split(); ents.append([mode, typ, sha, name])
    return ents
def hash_tree(ents):
    def key(e): return e[3] + ('/' if e[1] == 'tree' else '')
    body = b''.join((e[0].lstrip('0') + ' ' + e[3]).encode() + b'\0' + bytes.fromhex(e[2]) for e in sorted(ents, key=key))
    return hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
def compose(tree_oid, changes, where=REPO):
    ents = ls_tree(tree_oid, where); groups = {}
    for path, (mode, blob) in changes.items():
        top, rest = (path.split('/', 1) + [None])[:2]; groups.setdefault(top, {})[rest] = (mode, blob)
    byname = {e[3]: e for e in ents}
    for top, sub in groups.items():
        if None in sub:
            mode, blob = sub[None]
            if top in byname: byname[top][0], byname[top][2] = mode, blob
            else: ents.append([mode, 'blob', blob, top]); byname[top] = ents[-1]
        else: byname[top][2] = compose(byname[top][2], sub, where)
    return hash_tree(ents)
ctrl = hash_tree(ls_tree(PARENT_TREE)); print('tree-hash control: re-hashing the parent root tree ->', ctrl[:9], ctrl == PARENT_TREE)
if ctrl != PARENT_TREE: sys.exit(1)
for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS:
    mt = compose(PARENT_TREE, {p_: (v[3], v[1]) for p_, v in PERPR[n].items()})
    print('  #%s compose over the parent -> %s == head tree %s (fast-forward there)' % (n, mt[:9], mt == ht))
    if mt != ht: sys.exit(1)
nd = open(os.path.join(GS, 'newdev_tree.txt')).read()
ALL_OVER_DEV = re.search(r'^ALL8_OVER_NEW ([0-9a-f]{40})', nd, re.M).group(1); NEWTREE = {}
for l in nd.splitlines():
    m = re.match(r'^PR(\d+) ([0-9a-f]{40})', l)
    if m: NEWTREE[m.group(1)] = m.group(2)
if re.search(r'^DEV_NOW ([0-9a-f]{40})', nd, re.M).group(1) != DEV: print('REFUSING: newdev_tree.txt is for another develop — re-run predict_batch_scratch_gate16B.py'); sys.exit(1)
ad = compose(PARENT_TREE, {p_: (v[3], v[1]) for p_, v in CHANGED.items()})
print('compose(the 8 into the parent tree) ->', ad, '==', ALL_OVER_PARENT[:9], ad == ALL_OVER_PARENT)
if ad != ALL_OVER_PARENT: sys.exit(1)
ad2 = compose(DEV_TREE, {p_: (v[3], v[1]) for p_, v in CHANGED.items()}, SCR)
print('compose(the 8 into the CURRENT develop tree) ->', ad2, '==', ALL_OVER_DEV[:9], ad2 == ALL_OVER_DEV)
if ad2 != ALL_OVER_DEV: sys.exit(1)
for n, *_r in PRS:
    p = _r[-2]; mt2 = compose(DEV_TREE, {p_: (v[3], v[1]) for p_, v in PERPR[n].items()}, SCR)
    if mt2 != NEWTREE[p]: print('REFUSING: merged tree over the current develop disagrees with predict_batch_scratch for PR', p, mt2[:12], NEWTREE[p][:12]); sys.exit(1)
print('per-PR merged trees over the current develop == predict_batch_scratch (real 3-way / canonical apply):', len(PRS), 'of', len(PRS))
pms = sorted(glob.glob(os.path.join(GS, 'predict_batch_scratch_*.out'))); pm = open(pms[-1]).read()
print('newest predict_batch_scratch out:', os.path.basename(pms[-1]), '| all-12 over the parent three orders identical:', 'all three identical: True | == the seat eight-PR tree %s: True' % ALL_OVER_PARENT in pm, '| heads four orders == the seat tree:', 'all orders identical: True | == the seat eight-PR tree %s: True' % ALL_OVER_PARENT in pm, '| byte-identical:', 'byte-identical to before: True' in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm)
if not ('byte-identical to before: True' in pm and 'all three identical: True | == the seat eight-PR tree %s: True' % ALL_OVER_PARENT in pm): print('REFUSING: predict_batch_scratch did not reproduce the eight-PR tree read-only'); sys.exit(1)
# 3. the launcher
BRIEF = GS + '/mail_gate16B_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch%s-%s.prompt.txt' % (FIRST, LAST)
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch%s-%s-r1/' % (FIRST, LAST)
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1136-1146-tier2-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-1135-tier1-r1/'
OLDER_R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
for d_ in (PRIOR, EARLIER, OLDER_R):
    if not os.path.isdir(d_): print('REFUSING: report dir absent', d_); sys.exit(1)
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
if 'NOT YET ARRIVED' in brief_txt: print('REFUSING: the combined capture has a section NOT YET ARRIVED'); sys.exit(1)
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-118s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{' + ', '.join('"%s": "%s"' % x for x in landed) + '}') if landed else '{}')
judged = [jline(p_, FULLDEV[p_], [(CHANGED[p_][1], '#%s own' % CHANGED[p_][4])]) for p_ in BLOBS]
judged += [jline(p_, UBLOB[p_], None) for p_ in UNCHANGED]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, tk, br, ('${QAB1147_HEAD_%s:-%s}' % (LAST, h)) if n == LAST else h, nf) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=%d files=%d' % (n, BEHIND, nf) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER %d' \"$PROMPT_FILE\"" % (n, tk, tier) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS)
def ns_sentence(n, tk): return 'PR #%s is %s.' % (n, tk)
NS_GREP = ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (ns_sentence(n, tk), n, tk) for n, tk, *_ in PRS)
TIER_LIST = ', '.join('#%s T%d' % (n, tier) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS)
SUBJECT = '[QA -> Wednesday] BATCH GATE #%s-#%s (eight PRs; tier 2 floor, tier 1 = #%s: Seat B 16th test-only pins)' % (FIRST, LAST, LAST)
HEADS_LIST = ' '.join('#%s@%s' % (n, h[:9]) for n, tk, tags, br, h, *_ in PRS)
GO_STRING = 'GO: merge ' + ', '.join('#' + n for n, *_ in PRS) + ' batch'
# exit 30: seat items in BOTH the READY capture and the prompt
BOTH = ['18499832', ALL_OVER_PARENT[:12], R.SEAT_ALL9[:12], '2ede08b37', PARENT, DEV[:9], '87b4aa12d2eb', '685d5f264', 's-b16-ks1171', GO_STRING] + [ht[:12] for *_a, ht, nf, adds, dels, fw, p, tier in PRS] + [
        R.PRS[p]['blob'][:12] for p in R.PUSH] + [c[2] for p in R.PUSH for c in R.PRS[p]['canon']] + [
        'e76b3e90db28', 'e9dc6e3899f0', '6250385ee49e', '1fcffe443b5c', '8082826898c2', 'c771e61f4cbe', '51d28696e81e', 'a7ac2c174cad', 'd57c47dac730',
        '809', '907', '216', '813/813', '812/812', '814/814', '819/819', '914/914', '910/910', '220/220', '835', '917', '328/329', 'threadTokenMint',
        'corrupt patch at line 100', '--recount', 'TRUNCATION', 'RECOUNT', 'strict', '+755/', 'c54c1ae73ba3',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'login_stub', 'mergeable_state', 'stubs=4', '44 passed, 0 failed (of 44)', 'PROTOCOL-CLEAN',
        'TEST-FILE-ONLY', 'typecheck17', 'TS2322', 'STOP-class 0', 'netlog.cjs', ':5432', 'anchoring:4005', '203.0.113.7:443', 'fast.example:443', 'ks914-pinned-address',
        'started_utc', 'lock released', 'attachmentsForURL', 'contributes', 'linear[bot]', 'ks1004-anchor-failed-lockout', 'CARRIED FORWARD',
        'declared ∪ the measured cover', 'EXACTLY ITS DECLARED CELLS', 'anchors17.json', 'cover-aware', 'ks-727', 'ks1213', '138 chars', 'Q6(b)',
        'KS-1180', '#1150', 'KS-1185', '#1152', 'kksecura', 'Blockchain-C', 'Seat C 16th', '57702', '16053', 'S7', 'S8', 'ready_send17.sh', 'batch8.py',
        'KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490', 'KS-597', 'KS-727',
        'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270', 'KS-1213', 'KS-1073', 'KS-1050', 'KS-1204', 'KS-1072', 'KS-1183', 'KS-999', 'KS-1018', 'KS-1285', 'KS-1123', 'KS-1171',
        ] + ['Refs ' + R.PRS[p]['key'] for p in R.PUSH]   # KS-1201 / KS-256 sit in the PR bodies, not the READY mails — prompt-only, not BOTH
missing_b = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing_b: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', [(t, online(t, brief_txt.splitlines()), online(t, prompt_txt.splitlines())) for t in missing_b]); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
BYNAME = [
 ('1', ['TIER AND ROUND', 'round 1 of 2', 'outside __tests__: []', 'files API union 8', 'Any product byte', 'STATE WHICH by the files API']),
 ('2', ['TEST-FILE-ONLY:', 'the test file exactly', 'the RECOUNT column', 'name-status A ×7 / M ×1']),
 ('3', ['THE TREES, RE-DERIVED', 'EIGHT', 'ZERO overlap', 'at least forward, exact reverse and one shuffle', 'read-tree back to develop', 'state the SET you read and WHEN']),
 ('4', ['CANONICAL-PATCH IDENTITY with the `--recount` class', '`--recount` is MANDATORY on every apply this round', 'per stage for #%s' % PRS[4][0], 'Name each READY\'s strict / recount', 'Name any byte that differs']),
 ('5', ['THE CELLS: green at head', 'every declared cell + control', 'per-tamper', 'reds EXACTLY the declared set', 'tamper files restored by bytes', 'admitted by NAME']),
 ('6', ['PER-FILE TYPECHECK DELTA 0', 'planted TS2322 control CAUGHT', 'a zero that needs its control']),
 ('7', ['THE CENSUS RULE v2: loopback only, zero :5432', 'unestablished EXTERNAL attempts REPORTED', '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run', 'login_stub cleared by PID']),
 ('8', ['LINEAR LINK HYGIENE', 'includeArchived', 'Backlog -> In Progress walks recorded', 'KS-975 assigned to the board login at item 0', 'no archived key in any branch', 'Recommend nothing', 'PR #1158 is Seat C\'s KS-855']),
 ('9', ['THE TWO-SEAT ARTEFACTS', 'every push INSIDE the push-window lock', 'grade present / absent + MONOTONIC', 'attributions the seat made for Seat C\'s PRs BY NAME', 'four-condition rule', 'ONLY tolerated state change']),
 ('10', ['THE SEAT\'S OWN FINDINGS / SLIPS', 'CONFIRMED / REFUTED', 'S7 the eight-PR body paragraph', 'S6 the sender WRAPPER killed by Seat C', 'THE LINE-NUMBER DISCIPLINE', 'NAME WHO INHERITED IT']),
 ('11', ['THE INTERMITTENTS', '5 s timeouts', 're-run standalone 3× serial', 'RULE WHETHER IT BLOCKS']),
 ('12', ['MERGE ADDENDUM — EIGHT lines VERBATIM', 'ONE equality target PER', 'alone-tree reading', 'stays In Progress', 'SHIPS-WITH text ≤ 3 sentences', 'NOT-PINNED rows NAMED', 'NOT-PINNED for its own file', 'sha256 + byte count IN the mail', 'NOT-TESTED written FIRST']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree', 'lsof -nP -iTCP:4003 -sTCP:LISTEN', 'lsof -nP -iTCP:4004 -sTCP:LISTEN', 'lsof -nP -iTCP:4005 -sTCP:LISTEN', 'lsof -nP -iTCP:5432 -sTCP:LISTEN', 'GATEWAY_URL=http://127.0.0.1:', 'NAMESPACE GUARD', 'EIGHT lines, one per PR', 'MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', 'COMMA-separated', '## MERGE ADDENDUM', 'MG-3 (the KEY-SET rule', 'node_modules per ENTRY', 'MAIL YOUR VERDICT', 'no memory maintenance', 'NEVER print a credential value', 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'NEVER touch the push-window lock directory', 'by ANCESTRY', 'never by a basename']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('## MERGE ADDENDUM', 'CANONICAL-PATCH IDENTITY with the `--recount` class', '`--recount` is MANDATORY on every apply this round', '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run'), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS:
    if not online(ns_sentence(n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt:', ns_sentence(n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk)); sys.exit(1)
    if not online('#%s %s: TIER %d' % (n, tk, tier), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER %d' % (n, tk, tier)); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 12 items + the closing, all present in the prompt')
HEADER_LINES = '\n'.join('#   #%s PR %s %s %s @ %s  TEST-ONLY %s +%d/-%d — TIER %d' % (n, p, tk, tags, h[:9], fw[0].split('/')[-1], adds, dels, tier) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier in PRS)
L = r'''#!/bin/bash
# launch_qa_secuura_batch__FIRST__-__LAST__.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 2 floor (TIER 1 on #__LAST__) over EIGHT
# Secuura/Blockchain PRs (Seat B 16th; twelve local-model R15 TEST-ONLY patches applied --recount and grouped by TICKET = by FILE into eight PRs
# across THREE lanes — originate jest, packages/shared vitest, security vitest — EIGHT paths, ZERO overlap, ZERO product bytes; the seat's PR 8
# KS-1171 HELD un-pushed, NOT here)
__HEADERLINES__
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 64ab10513: each head's parent IS that
# commit) by pure tree hashing; the eight-PR tree over the parent (c54c1ae73ba3…) by REAL --recount applies in three orders AND real 3-way merges of
# the heads in four orders in a --shared scratch clone (predict_batch_scratch_*.out) AND by tree hashing; every BOTH-list token asserted present in
# the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets17.py (re-keyed to EIGHT) wants exactly ONE equality target PER PR FILE (1/1/1/1/1/1/1/1) and parses the
# list non-greedily to the FIRST `;` — no two-file line this round (the COMMA-separated form is inherited, not exercised); merge17.py asserts each
# squash body's key set == the PR's OWN Refs set (one key each).
# Batched under Kam 2026-09-18 standing rule. EIGHT verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All eight tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 64ab10513 (tree 87b4aa12d2eb, Seat B 15th's final state +
# Peter's #1138). ORIGIN DEVELOP: the pin is __DEV__ (tree __DEVTREE__) — UNMOVED since the raise at generation (behind __BEHIND__); the
# compare per PR reads develop...head = merge_base 64ab10513, ahead 1, BEHIND __BEHIND__, files 1 ×8 (exit 10 — a develop move changes `behind`
# and REFUSES: re-pin deliberately — Seat C 16th's GO may land its merges first). ALL EIGHT over the parent = c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d;
# ALL EIGHT over the current develop = __ALLDEV__ (the END STATE if every merge lands on __DEVSHORT__).
#
# The develop pin is judged by CONTENT — the 8 target paths at the CURRENT develop (seven NEW files judged ABSENT — any present blob -> exit 19
# LANDED if it is the head blob, exit 18 otherwise; the ks1213 file by blob) plus __NUNCH__ unchanged-read paths (this round's 9 tamper files, the
# 15th's five, the hook, preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts, the ks1004 cover test, the
# threadTokenMint test, the four lanes' package.json / config / tsconfig / lock, the Dev package.json + lock, eslint.config.mjs). GUARDED on a move:
# shared / originate / security / anchoring src + config, packages/shared, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs
# (api-gateway / auth — Seat C's lanes — are NOT guarded: a Seat C merge is a disjoint move by the partition, still refused at exit 10 by `behind`).
#
# SOURCE = gatesets/2026-09-22_gate16B_seatB/mail_gate16B_ready.md, the seat's eight READY mails (17:01:06Z … 18:31:47Z) + its 16:54:31Z and
# 18:33:17Z STATUS mails + its QUESTION / ACK mails, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 2 floor AND each PR own tier line (__TIERLIST__).
# exit 10: the compare per PR (merge_base 64ab10513, ahead 1, behind __BEHIND__, files 1) — develop moving refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and EIGHT verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1136-#1146), the EARLIER REPORT (#1130-#1135), the OLDER REPORT
#          (#1119-#1128) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE, the `## MERGE ADDENDUM` heading targets17.py
#          parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b16-*, s-c16-*) and writing in the seat 2026-09-22_seatB-16th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the eight-PR
#          tree, the held octopus, the eight head blobs, the twelve canonical sha16s, the four STRICT blobs, the suite counts, the --recount rcs,
#          the lock words, the attributions, the archived / content keys, the GO string), and the prompt must ask the gate to MEASURE, not
#          conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the eight-PR tree in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket the PR is (PR #__FIRST__ is KS-928. … ).
# exit 33: the prompt must carry Wednesday TWELVE BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; inherited, never expected this round.
# QAB1147_CUR_DEV (test override, --check only): stands in for origin develop. QAB1147_HEAD___LAST__ (test override): stands in for #__LAST__ pinned head.
# QAB1147_BRIEF / QAB1147_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1147_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate16B_seatB/gen_launcher_gate16B.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_gate15.py.
#
# Usage: launch_qa_secuura_batch__FIRST__-__LAST__.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1147_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1147_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation (= the heads' parent; a move refuses at exit 10 / 18)
MERGE_BASE='64ab105132eada0621622acf4d6053bc59926780'    # every head's parent = the merge-base with the current develop
ALL_OVER_DEV='__ALLDEV__'     # all eight over the CURRENT develop (real applies + 3-way merges; generator tree-hash) — the END STATE
ALL_OVER_PARENT='c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d'   # all eight over the parent 64ab10513 (the seat's batch8.py; three + four orders)
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
EARLIER_REPORT='__EARLIER__'
OLDER_REPORT='__OLDER__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }
grep -qF 'PENDING-PR-' "$PROMPT_FILE" && { echo "REFUSING: the prompt is PARTIAL (a PENDING-PR- token) — a partial gate is not a gate" >&2; exit 34; }

# The heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 64ab10513, ahead 1, behind __BEHIND__,
# files 1 ×8 (generator, rev-list --left-right; the launcher reads the compare API). A develop move -> exit 10.
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

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB (or ABSENT) at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1147_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
SH = D + "packages/shared/"
OR = D + "services/originate/"
SE = D + "services/security/"
AN = D + "services/anchoring/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob or ABSENT: label}, LANDED blobs {blob: label})
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the heads parent; behind __BEHIND__; all eight together " + all_over_dev + " over it, three + four orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           OR + "src/", OR + "package.json", OR + "jest.config.js", OR + "tsconfig.json", OR + "package-lock.json",
           SE + "src/", SE + "package.json", SE + "vitest.config.ts", SE + "tsconfig.json", SE + "package-lock.json",
           AN + "src/", AN + "package.json", AN + "vitest.config.ts", AN + "tsconfig.json", AN + "package-lock.json",
           SC, ".githooks/", D + "package.json", D + "package-lock.json", D + "eslint.config.mjs"]
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the eight-PR tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (predict_batch_scratch_gate16B.py + gen_launcher_gate16B.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 2 floor' "$PROMPT_FILE" && __TIERGREP__ \
  || { echo "REFUSING: prompt does not carry the TIER 2 floor and each PR own tier line (__TIERLIST__)" >&2; exit 7; }
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'EIGHT lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and EIGHT verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b16-batch' "$PROMPT_FILE" && grep -qF 's-c16-' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatB-16th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b16-*, s-c16-*) and writing in the seat 2026-09-22_seatB-16th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in __BOTHLOOP__; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the eight-PR tree, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #__FIRST__ is KS-928. … )" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday twelve by-name items (tier/round; test-file-only; the trees and the zero overlap; canonical identity with the recount class; the cells; the per-file typecheck; the census rule; Linear hygiene; the two-seat artefacts; the seat findings/slips; the intermittents; the addendum) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries the TIER 2 floor and each PR tier (__TIERLIST__); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, EIGHT verdict lines"
  echo "  prompt names the report directory, the #1136-#1146 PRIOR REPORT, the #1130-#1135 EARLIER REPORT, the #1119-#1128 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b16-*, s-c16-*) and the seat 2026-09-22_seatB-16th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the eight-PR tree, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each PR is"
  echo "  prompt carries Wednesday twelve by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1147_CUR_DEV:-}" ] && echo "  (develop read from the QAB1147_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1147_BRIEF:-}${QAB1147_PROMPT:-}${QAB1147_HEAD___LAST__:-}${QAB1147_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
__ENTERQA__ || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__HEADERLINES__': HEADER_LINES, '__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__DEVTREE__': DEV_TREE[:12], '__DEVSHORT__': DEV[:9], '__ALLDEV__': ALL_OVER_DEV, '__BEHIND__': str(BEHIND), '__NUNCH__': str(len(UNCHANGED)),
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__EARLIER__': EARLIER, '__OLDER__': OLDER_R, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME)),
        '__TIERLIST__': TIER_LIST, '__SUBJECT__': SUBJECT, '__LAST__': LAST, '__FIRST__': FIRST, '__ENTERQA__': 'c' + 'd' + ' "$QA_DIR"'}
for k, v in sorted(SUBS.items(), key=lambda kv: -len(kv[0])):
    if s.count(k) == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z0-9]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z0-9]+__', s)); sys.exit(2)
# 4. output controls
want = {DEV: 2, ALL_OVER_DEV: 2, ALL_OVER_PARENT: 3, PARENT: 2, 'behind=%d' % BEHIND: len(PRS), BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, EARLIER: 1, OLDER_R: 1,
        'exit 6': 2, 'exit 10': 6, 'exit 19': 3, 'exit 18': 5, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 34': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': len(BLOBS) + len(UNCHANGED), ' own"': len(CHANGED), 'PENDING-PR-': 3, '"ABSENT": DV': 7,
        'QAB1147_CUR_DEV': 5, 'QAB1147_HEAD_' + LAST: 3, 'refs/pull/$_n/head': 2,
        SUBJECT: 1, 'PR #%s is KS-928.' % FIRST: 3, GO_STRING: 1}
for n, tk, tags, br, h, *_ in PRS: want[h] = 1
if DEV == PARENT: want[DEV] = 4            # unmoved: DEVELOP_SHA + MERGE_BASE + the two header mentions are ONE string
if ALL_OVER_DEV == ALL_OVER_PARENT: want[ALL_OVER_DEV] = 4   # ALL_OVER_DEV + ALL_OVER_PARENT + the header's two mentions are ONE string (the drafter's run-4 miscount was 5)
got = {k: s.count(k) for k in want}
bad = {k: (got[k], want[k]) for k in want if got[k] != want[k]}
print('output controls', {(k[:28] + '…' if len(k) > 28 else k): v for k, v in got.items()})
if bad:
    for k in bad:
        for m in re.finditer(re.escape(k), s): print('   context for %r @ line %d: %r' % (k[:20], s.count('\n', 0, m.start()) + 1, s[max(0, m.start() - 70):m.end() + 15]))
    print('REFUSING: output control mismatch (got, want)', bad); sys.exit(1)
for kw in [kw for _, kws in BYNAME for kw in kws] + BOTH:
    if s.count(kw) < 1: print('REFUSING: ladder keyword missing from launcher', kw); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); end = s.index('\n' + tag[3:-2] + '\n', i); blk = s[i:end]
    print('heredoc', tag.strip(), '@', s.count('\n', 0, i) + 1, 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.sh', dir=os.path.dirname(OUT)); tmp.write(s); tmp.close()
p = subprocess.run(['bash', '-n', tmp.name], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp.name); sys.exit(3)
if os.path.exists(OUT): os.replace(OUT, OUT + '.pre-' + now('+%H%M'))
os.replace(tmp.name, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest(), 'lines', s.count('\n'))
