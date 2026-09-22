#!/usr/bin/env python3
"""gen_launcher_gate18C.py — write launchers/launch_qa_secuura_batch1167-1175.sh (ONE batched round-1 gate over SIX Secuura/Blockchain PRs #1167
#1168 #1169 #1171 #1173 #1175, Seat C 18th: three R16 TEST-ONLY PRs + three R16 CODE_PATCH PRs with PRODUCT bytes on api-gateway (7 READYs, 10 paths,
the health.ts PAIR), tier 1 on #1167 #1171 #1173 #1175, tier 2 on #1168 #1169; READYs 2026-09-21T23:37:46Z-2026-09-22T00:32:55Z)
in the SHAPE of gatesets/2026-09-22_gate16C_seatC/gen_launcher_gate16C.py (pins re-read at generation, tree hashing, output controls, heredoc
parity, bash -n): exit 6 a head moved · 10 the compare per PR (merge_base = the heads' parent 8c2f7b3fd, ahead 1, BEHIND = the develop move count at
generation (0: unmoved), files 1/1/1/4/2/2 — develop moving changes `behind` and REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED
detection (five NEW targets judged ABSENT; the five MODIFIED targets by blob — health.ts LANDED on EITHER alone blob OR the PAIR blob; the tamper file
index.ts + the 16th's other tamper files + the hook / preflight / lane configs unchanged) · the prompt + READY greps · 16 overrides at launch · 21
TTY · 34 a PENDING-PR- marker (inherited; never expected this round) · 35 the PAIR (`--pair-blob` + the pair blob + `alone blob` in the prompt).
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * the PR numbers and heads come from round18C.py AND the captured READY mails AND origin (git ls-remote of refs/heads/develop, every refs/pull/N/head
    AND branch) — all three must agree;
  * local objects (rev-list / rev-parse / diff --raw / diff --numstat / ls-tree): each head is ONE commit whose parent IS 8c2f7b3fd; the (path, develop
    blob or ABSENT, head blob) pairs as pinned; the paths pairwise disjoint EXCEPT the ONE expected pair (health.ts: #1171 + #1173); test-only rows
    under __tests__/ only, code_patch rows' non-test paths == the declared PRODUCT set; every unchanged-read path has the SAME blob at 8c2f7b3fd, at
    the CURRENT develop (read in the scratch clone — argv[2]) and at every head; the per-PR trees; the all-6 tree over 8c2f7b3fd by pure tree hashing
    with health.ts at the PAIR blob (must equal 52853c8bf6c4… and predict_batch_scratch_*.out);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_gate18C.py <output launcher> <scratch clone holding the current develop by SHA>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import glob, hashlib, itertools, json, os, re, shutil, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18C as R
OUT = sys.argv[1]; SCR = sys.argv[2]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date'] + (['-u'] if f.endswith('Z') else []) + [f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_gate18C', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = R.REPO; GS = G
PARENT = R.DEV; PARENT_TREE = R.DEV_TREE; ALL_OVER_PARENT = R.SEAT_ALL6
D = R.D; SH = R.SH; OR = R.OR; SE = R.SE; AN = R.AN; AG = R.AG; AU = R.AU; SC = R.SC; HP = AG + 'src/services/health.ts'
READY = {}
for f in sorted(glob.glob(os.path.join(GS, 'mail_seatC18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(4))
present = [p for p in R.PUSH if p in READY]; missing = [p for p in R.PUSH if p not in READY]
print('READYs captured for seat PRs', present, '| missing', missing or 'none')
if missing: print('REFUSING: this round has no PARTIAL form — every READY landed before the drafters began; a missing capture is a capture fault'); sys.exit(1)
for p in R.PUSH:
    if READY[p] != (R.PRS[p]['n'], R.PRS[p]['head']): print('REFUSING: the READY for seat PR', p, 'disagrees with round18C', READY[p], (R.PRS[p]['n'], R.PRS[p]['head'])); sys.exit(1)
# n, key, tags, branch, head, head tree, nfiles, adds, dels, files, p, tier, kind, product paths
PRS = [(R.PRS[p]['n'], R.PRS[p]['key'], R.PRS[p]['tags'], R.PRS[p]['branch'], R.PRS[p]['head'], R.PRS[p]['tree'], len(R.PRS[p]['files']), R.PRS[p]['adds'], R.PRS[p]['dels'], [f['path'] for f in R.PRS[p]['files']], p, R.PRS[p]['tier'], R.PRS[p]['kind'], sorted(f['path'] for f in R.PRS[p]['files'] if f['kind'] == 'product')) for p in R.PUSH]
LAST = PRS[-1][0]; FIRST = PRS[0][0]
print('PR numbers (push order):', [n for n, *_ in PRS], '| first', FIRST, 'last', LAST)
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
def sgit(*a): return subprocess.run(['git', '-C', SCR] + list(a), capture_output=True, text=True).stdout.strip()
# 1. origin
refs_wanted = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n, *_ in PRS] + [br for _, _, _, br, *_ in PRS] + ['refs/heads/feature/ks-1123-*-r15-*']
lsr = out('ls-remote', 'origin', *refs_wanted)
print('ls-remote', now('+%Y-%m-%dT%H:%M:%SZ'), '|', len(lsr.strip().splitlines()), 'refs read (want %d; the ks-1123 r15 glob (the 16th\'s HELD branch) must return NOTHING)' % (len(refs_wanted) - 1))
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
DEV = refs.get('refs/heads/develop', '?')
print('origin develop NOW (the pin):', DEV, '| the heads parent', PARENT[:9], '| moved since the raise:', DEV != PARENT)
if not re.fullmatch(r'[0-9a-f]{40}', DEV): sys.exit(1)
held = [k for k in refs if 'ks-1123' in k and '-r15-' in k]
if held: print('REFUSING: a ks-1123 r15 branch is at origin — the 16th\'s HELD PR was pushed; a different gate:', held); sys.exit(1)
print('the 16th\'s HELD KS-1123 r15 branch ABSENT at origin: True')
want = [('refs/pull/%s/head' % n, h) for n, _, _, _, h, *_ in PRS] + [(br, h) for _, _, _, br, h, *_ in PRS]
for ref, w in want:
    print('  %-140s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
if subprocess.run(['git', '-C', SCR, 'cat-file', '-e', DEV + '^{commit}']).returncode: print('REFUSING: the current develop', DEV[:9], 'is not in the scratch clone', SCR, '- re-run predict_batch_scratch_gate18C.py'); sys.exit(1)
DEV_TREE = sgit('rev-parse', DEV + '^{tree}'); BEHIND = int(sgit('rev-list', '--count', PARENT + '..' + DEV) or '0'); MB = sgit('merge-base', PARENT, DEV)
print('current develop tree', DEV_TREE[:12], '| rev-list --count parent..develop =', BEHIND, '| merge-base(parent, develop) == parent:', MB == PARENT)
if MB != PARENT: sys.exit(1)
# path -> (dev blob or None, {head blob12: label})
BLOBS = {}
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        BLOBS.setdefault(f['path'], [f['dev_blob'], {}])[1][f['blob'][:12]] = '#%s own' % R.PRS[p]['n']
BLOBS[HP][1][R.PAIR_BLOB[:12]] = 'the PAIR (#1171 + #1173)'
TAMPERS = [x[0] for x in R.TAMPER_BLOBS]   # index.ts + verification.ts; verification.ts is ALSO a target (Part A) — judged as a target, not as unchanged
moved = set(sgit('diff', '--name-only', PARENT, DEV).splitlines()); print('develop move touches', len(moved), 'paths; ∩ the 10 target paths:', sorted(moved & set(BLOBS)) or 'NONE', '| ∩ the 2 tamper files:', sorted(moved & set(TAMPERS)) or 'NONE')
if moved & (set(BLOBS) | set(TAMPERS)): print('REFUSING: the develop move touches a target or tamper path'); sys.exit(1)
# 2. local objects
dt = out('rev-parse', PARENT + '^{tree}').strip(); print('parent tree', dt[:9], '==', PARENT_TREE[:9], dt == PARENT_TREE)
if dt != PARENT_TREE: sys.exit(1)
CHANGED = {}; PERPR = {}
for n, tk, tags, br, h, ht, nf, adds, dels, files_want, p, tier, kind, prod in PRS:
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', PARENT + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    raw = out('diff', '--raw', '--abbrev=40', PARENT, h).strip().splitlines()
    ns = {l.split('\t')[2]: (int(l.split('\t')[0]), int(l.split('\t')[1])) for l in out('diff', '--numstat', PARENT, h).strip().splitlines()}
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); files[path] = (b1, b2, st, m2, n)
    a_sum = sum(v[0] for v in ns.values()); d_sum = sum(v[1] for v in ns.values())
    outside = sorted(x for x in files if '/__tests__/' not in x); ok_kind = (outside == prod) and not any(x.startswith(AU) for x in files)
    print('#%s PR %s %s %s head %s parent==PARENT %s | parent...head behind/ahead %s (want 0 1) | tree %s == pin %s | files %s == %s | +%d/-%d (want +%d/-%d) | modes %s | status %s | outside __tests__ %s == PRODUCT set %s: %s | tier %d' % (
        n, p, tk, kind, h[:9], par == [PARENT], lr, t[:12], t == ht, [x.split('/')[-1] for x in files], sorted(files) == sorted(files_want), a_sum, d_sum, adds, dels, sorted({v[3] for v in files.values()}), sorted(v[2] for v in files.values()), [x.split('/')[-1] for x in outside], [x.split('/')[-1] for x in prod], ok_kind, tier))
    if par != [PARENT] or lr != ['0', '1'] or t != ht or sorted(files) != sorted(files_want) or a_sum != adds or d_sum != dels or any(v[3] != '100644' for v in files.values()) or not ok_kind: sys.exit(1)
    for p_, v in files.items():
        want_dev = BLOBS[p_][0]
        if (want_dev is None and v[2] != 'A') or (want_dev is not None and (v[2] != 'M' or not v[0].startswith(want_dev))) or v[1][:12] not in BLOBS[p_][1]: print('REFUSING: pinned blob / status disagrees for', p_, v[:3]); sys.exit(1)
        CHANGED.setdefault(p_, []).append(v)
    PERPR[n] = files
overl = [(a, b, sorted(set(PERPR[a]) & set(PERPR[b]))) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])]
print('union paths', len(CHANGED), '(want 10) | pairwise overlaps', overl, '(want exactly [(1171, 1173, [health.ts])])')
if overl != [('1171', '1173', [HP])] or len(CHANGED) != 10: sys.exit(1)
FULLDEV = {}
for p_ in BLOBS:
    if BLOBS[p_][0] is None:
        if git('cat-file', '-e', PARENT + ':' + p_).returncode == 0 or subprocess.run(['git', '-C', SCR, 'cat-file', '-e', DEV + ':' + p_], capture_output=True).returncode == 0: print('REFUSING: a NEW target exists at the parent or the current develop', p_); sys.exit(1)
        FULLDEV[p_] = 'ABSENT'
    else:
        bd = out('rev-parse', PARENT + ':' + p_).strip(); bc = sgit('rev-parse', DEV + ':' + p_)
        if not bd.startswith(BLOBS[p_][0][:12]) or bc != bd: print('REFUSING: target blob differs at the parent or the current develop', p_, bd[:12], bc[:12]); sys.exit(1)
        FULLDEV[p_] = bd
LANDED40 = {}
for p_ in BLOBS:
    LANDED40[p_] = {}
    for b12, label in BLOBS[p_][1].items():
        b40 = R.PAIR_BLOB if b12 == R.PAIR_BLOB[:12] else [f['blob'] for p in R.PUSH for f in R.PRS[p]['files'] if f['path'] == p_ and f['blob'][:12] == b12][0]
        if git('cat-file', '-e', b40).returncode: print('REFUSING: a LANDED blob is not in the store', p_, b40); sys.exit(1)
        LANDED40[p_][b40] = label
print('the 10 (develop blob | ABSENT) values agree at 8c2f7b3fd AND at the current develop; the head blobs (+ the PAIR blob on health.ts) agree with the GROUPING column: True')
TAMPER16 = [AG + 'src/routes/system-status.ts', AU + 'src/services/oauth.ts', AU + 'src/auth.openapi.ts', AU + 'src/routes/auth.ts', AU + 'src/routes/mfa.ts', AU + 'src/routes/users.ts', AU + 'src/repositories/userRepo.ts']
TAMPER15 = ['Blockchain/Testing/jobs/04-container-trivy.sh', 'systemTest/fixtures/manifest.ts', SE + 'src/index.ts', AU + 'src/routes/users.ts', SC + 'check-shared-relink.sh']
UNCHANGED = [AG + 'src/index.ts'] + TAMPER16 + [x for x in TAMPER15 if x not in TAMPER16] + ['.githooks/pre-push', SC + 'preflight/preflight.sh', SC + 'run-shell-suites.sh', SC + 'fix-libsodium-symlink.js', SC + 'audit/audit-baseline.json',
             AG + 'src/routes/proxy.ts', AG + 'src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts', AG + 'src/__tests__/ks815-verification-router-guards-its-own-body.test.ts',
             AG + 'src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts', AG + 'src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts',
             SH + 'package.json', SH + 'vitest.config.ts', SH + 'tsconfig.json',
             AG + 'package.json', AG + 'vitest.config.ts', AG + 'tsconfig.json', AG + 'package-lock.json',
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
print('unchanged-read paths', len(UNCHANGED), 'all same blob at the parent, at the current develop and at every head: True (index.ts this round\'s tamper file; the 16th\'s seven other tamper files; the 15th\'s; the hook / preflight / lane configs / audit-baseline.json)')
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
for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier, kind, prod in PRS:
    mt = compose(PARENT_TREE, {p_: (v[3], v[1]) for p_, v in PERPR[n].items()})
    print('  #%s compose over the parent -> %s == head tree %s (fast-forward there)' % (n, mt[:9], mt == ht))
    if mt != ht: sys.exit(1)
nd = open(os.path.join(GS, 'newdev_tree.txt')).read()
ALL_OVER_DEV = re.search(r'^ALL6_OVER_NEW ([0-9a-f]{40})', nd, re.M).group(1); NEWTREE = {}
for l in nd.splitlines():
    m = re.match(r'^PR(\d+) ([0-9a-f]{40})', l)
    if m: NEWTREE[m.group(1)] = m.group(2)
if re.search(r'^DEV_NOW ([0-9a-f]{40})', nd, re.M).group(1) != DEV: print('REFUSING: newdev_tree.txt is for another develop — re-run predict_batch_scratch_gate18C.py'); sys.exit(1)
ALLCH = {p_: (vs[0][3], vs[0][1]) for p_, vs in CHANGED.items()}; ALLCH[HP] = ('100644', R.PAIR_BLOB)
ad = compose(PARENT_TREE, ALLCH)
print('compose(the 10 into the parent tree, health.ts at the PAIR blob) ->', ad, '==', ALL_OVER_PARENT[:9], ad == ALL_OVER_PARENT)
if ad != ALL_OVER_PARENT: sys.exit(1)
ad2 = compose(DEV_TREE, ALLCH, SCR)
print('compose(the 10 into the CURRENT develop tree) ->', ad2, '==', ALL_OVER_DEV[:9], ad2 == ALL_OVER_DEV)
if ad2 != ALL_OVER_DEV: sys.exit(1)
for n, *_r in PRS:
    p = _r[-4]; mt2 = compose(DEV_TREE, {p_: (v[3], v[1]) for p_, v in PERPR[n].items()}, SCR)
    if mt2 != NEWTREE[p]: print('REFUSING: merged tree over the current develop disagrees with predict_batch_scratch for PR', p, mt2[:12], NEWTREE[p][:12]); sys.exit(1)
print('per-PR merged trees over the current develop == predict_batch_scratch (real 3-way / canonical apply):', len(PRS), 'of', len(PRS))
pms = sorted(glob.glob(os.path.join(GS, 'predict_batch_scratch_[0-9]*.out'))); pm = open(pms[-1]).read()
print('newest predict_batch_scratch out:', os.path.basename(pms[-1]), '| all-11 canonicals over the parent three orders identical:', 'all three identical: True | == the seat all-6 tree %s: True' % ALL_OVER_PARENT in pm, '| heads four orders == the seat tree:', 'all orders identical: True | == the seat all-6 tree %s: True' % ALL_OVER_PARENT in pm, '| byte-identical:', 'byte-identical to before: True' in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm, '| cwd guard live:', 'under the scratchpad: True' in pm)
if not ('byte-identical to before: True' in pm and 'all three identical: True | == the seat all-6 tree %s: True' % ALL_OVER_PARENT in pm and 'under the scratchpad: True' in pm): print('REFUSING: predict_batch_scratch did not reproduce the all-6 tree read-only under the cwd guard'); sys.exit(1)
# 3. the launcher
BRIEF = GS + '/mail_gate18C_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch%s-%s.prompt.txt' % (FIRST, LAST)
REPORT = R.REPORT_DIR; PRIOR = R.PRIOR_REPORT; EARLIER = R.EARLIER_REPORT; OLDER_R = R.OLDER_REPORT
for d_ in (PRIOR, EARLIER, OLDER_R):
    if not os.path.isdir(d_) or not os.path.isfile(d_ + 'report.md'): print('REFUSING: report dir or its report.md absent', d_); sys.exit(1)
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
if 'NOT YET ARRIVED' in brief_txt: print('REFUSING: the combined capture has a section NOT YET ARRIVED'); sys.exit(1)
if 'deadbeef' in prompt_txt.lower(): print('REFUSING: a deadbeef literal in the prompt'); sys.exit(1)
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-118s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{' + ', '.join('"%s": "%s"' % x for x in landed) + '}') if landed else '{}')
judged = [jline(p_, FULLDEV[p_], list(LANDED40[p_].items())) for p_ in BLOBS]
judged += [jline(p_, UBLOB[p_], None) for p_ in UNCHANGED]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, tk, br, ('${QAB1167_HEAD_%s:-%s}' % (LAST, h)) if n == LAST else h, nf) for n, tk, tags, br, h, ht, nf, *_ in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=%d files=%d' % (n, BEHIND, nf) for n, tk, tags, br, h, ht, nf, *_ in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER %d' \"$PROMPT_FILE\"" % (n, tk, tier) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier, kind, prod in PRS)
def ns_sentence(n, tk): return 'PR #%s is %s.' % (n, tk)
NS_GREP = ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (ns_sentence(n, tk), n, tk) for n, tk, *_ in PRS)
TIER_LIST = ', '.join('#%s T%d' % (n, tier) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier, kind, prod in PRS)
SUBJECT = '[QA -> Wednesday] BATCH GATE #%s-#%s (six PRs; tier 1 = %s: Seat C 18th — KS-947 auth-surface pin + three code_patch product PRs; tier 2 = %s)' % (FIRST, LAST, ', '.join('#' + R.PRS[p]['n'] for p in R.TIER1), ', '.join('#' + R.PRS[p]['n'] for p in R.PUSH if p not in R.TIER1))
HEADS_LIST = ' '.join('#%s@%s' % (n, h[:9]) for n, tk, tags, br, h, *_ in PRS)
GO_STRING = R.GO_STRING
# exit 30: seat items in BOTH the READY capture and the prompt
BOTH = ['18499832', ALL_OVER_PARENT[:12], PARENT, DEV[:9], '04b05e093ad8', '3916eacd1', '4b251997a', 'c28f7a2f538c', 'a3becc4c37a9', '1b956c660f7c', GO_STRING] + [ht[:12] for *_a, ht, nf, adds, dels, fw, p, tier, kind, prod in PRS] + [
        f['blob'][:12] for p in R.PUSH for f in R.PRS[p]['files']] + [c[3] for p in R.PUSH for f in R.PRS[p]['files'] for c in f['canon']] + [R.PAIR_BLOB, R.PAIR_BLOB[:12], 'f98e22a73561', 'f888e8cd0bd1', '7bedc074583d', '893879a19950', '20c8a088f5dc',
        '710/710', '716/716', '714/714', '717/717', '715/715', '742/742', '1008 insertions', '15 deletions', '--pair-blob', 'PAIR blob', 'alone blob', 'RED-FIRST', 'GREEN-AFTER', 'A4', 'A5', 'code_patch', 'PRODUCT BYTES',
        '--recount --ignore-whitespace', 'strict', 'section_1.diff', 'section_2.diff', 'DEVELOP COVER', 'cover-aware', 'PARITY', 'anchor-ambiguity', 'suggested_test_file', 'no-useless-assignment',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'login_stub', 'mergeable_state', 'stubs=4', '45 passed, 0 failed (of 45)', 'PROTOCOL-CLEAN',
        'TEST-FILE-ONLY', 'typecheck18', 'TS2322', 'STOP-class 0', 'netlog.cjs', ':5432', 'anchoring:4005', 'localhost:6000', 'ks1072-the-latest-anchor-selector-docume', 'ks815-verification-router-guards-its-own',
        'LOCK TAKEN', 'LOCK RELEASED', 'push-lock-18', 'lock18.sh', 'push18.sh', 'series18.py', 'ATTRIBUTED', 'attrib18.json', 'attachmentsForURL', 'contributes', 'linear[bot]',
        'measure18b', 'measure18.py', 'MG-10', 'lockproof18', 'a4titles', 's2path', 'loadintermittent', 'batch_tampers18', 'settingsdefaults', 'threehunks', 'ks-733', 'ks871', 'ks-1',
        'kksecura', 'Seat B 18th', 'merge18b.py', 'targets18.py', 'dry18.sh', 'go18.sh', 'postmerge18.py', '--ruling', 'cwd guard', 'audit-baseline.json', 'KS-763', 'KS-775',
        'KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490', 'KS-597', 'KS-727',
        'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270', 'KS-549', 'KS-733', 'KS-815', 'KS-1013', 'KS-1058', 'KS-1103',
        'KS-1230', 'KS-1072', 'KS-999', 'KS-871', 'KS-1227', 'KS-1213', 'KS-1073', 'KS-1050', 'KS-1204', 'KS-1183', 'KS-1018', 'KS-1285', 'KS-1031', 'KS-1175', 'KS-1250', 'KS-1273', 'KS-958', 'KS-1185', 'KS-1280', 'KS-730', 'KS-692',
        'KS-1118', 'KS-1158', 'KS-1265', 'KS-1171', 'KS-811', 'KS-1188', 'KS-1181',
        ] + ['Refs ' + R.PRS[p]['key'] for p in R.PUSH]   # KS-1201 / KS-256 sit in the PR bodies, not the READY mails — prompt-only, not BOTH; drafter S2: `x-ratelimit-max` / `TS18046` / `Blockchain-B` are prompt-only too (the READYs truncate the F4 title at 50 chars; the 16th's TS18046 and the pane tag are not in this seat's mails)
missing_b = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing_b: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', [(t, online(t, brief_txt.splitlines()), online(t, prompt_txt.splitlines())) for t in missing_b]); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
BYNAME = [
 ('1', ['TIER AND ROUND', 'round 1 of 2', 'outside __tests__` == the declared PRODUCT set', 'files API union 10', 'Any product byte OUTSIDE the declared set', 'STATE WHICH by the files API', 'a declared product byte the test does not prove red-first']),
 ('2', ['TEST-FILE-ONLY / PRODUCT-AS-DECLARED:', 'the test file(s) exactly on', 'the declared product file(s) + test file(s) EXACTLY', 'name-status A ×5 / M ×6', 'nothing else moved on any PR']),
 ('3', ['THE TREES, RE-DERIVED', 'TEN', 'exactly ONE PR pair overlapping', 'ZERO overlap with Seat B 18th', 'at least forward, exact reverse and one shuffle', 'read-tree back to develop', 'state the SET you read and', 'the health.ts PAIR (#1171 + #1173) by real merges in BOTH', 'say which hunk each alone blob lacks']),
 ('4', ['CANONICAL-PATCH IDENTITY, STRICT', 'the EIGHT section files', 'applied THREE ways', 'Name any byte that differs', 'The section `.opts` files are TWO lines']),
 ('5', ['THE CELLS — two protocols', 'every declared cell + control', 'per-tamper', 'reds EXACTLY the declared set', 'tamper files restored by bytes', 'THE ANCHOR-AMBIGUITY ROWS', 'THE RED/GREEN PROTOCOL', 'head-minus-product', 'assert BOTH blobs after each step', 'MODIFY-IN-PLACE test', 'SECOND PIN']),
 ('6', ['PER-FILE TYPECHECK DELTA 0', 'planted TS2322 control CAUGHT', 'a zero that needs its control', 'DELTA 0 with a PRE-EXISTING error', 'AND the THREE product files']),
 ('7', ['THE CENSUS RULE v2 + the (b) ruling', 'against the ALLOW set', 'count BARE', 'census from the PRELOAD run', '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run', 'login_stub cleared by PID', 'a FOURTH row would be a STOP']),
 ('8', ['LINEAR LINK HYGIENE', 'includeArchived', 'Backlog -> In Progress walks recorded', 'KS-1246 and KS-1257', 'assigned to the board login at item 0', 'EXCISION', 'RUN the scanner', 'no archived key in any branch', 'Recommend nothing', 'PR #1171 is KS-1231 (KS-1171 is Seat B', 'PR #1173 is KS-1246 (KS-1173 is a foreign']),
 ('9', ['THE TWO-SEAT ARTEFACTS', 'INSIDE the push-window lock', 'grade present / absent + MONOTONIC', 'TWENTY-FIVE windows', 'the lock POLLS', 'THE MID-TAKE ARM (MG-10', 'attributions the seat made for Seat B', 'four-condition', 'ONLY tolerated state change', 'THE PROCESS-NAMESPACE RULE', 'THE COUNT-OBJECTS ACCOUNT']),
 ('10', ['THE SEAT\'S OWN FINDINGS / SLIPS', 'CONFIRMED / REFUTED', 'the SECOND PINS', 'S1 the merge-tree in the shared checkout', 'THE LINE-NUMBER DISCIPLINE', 'NAME WHO INHERITED IT']),
 ('11', ['THE INTERMITTENTS', 'RED-FIRST timeout under load 17', 're-run standalone 3× serial', 'RULE WHETHER IT BLOCKS']),
 ('12', ['MERGE ADDENDUM — SIX lines VERBATIM', 'ONE equality target PER', 'ELEVEN targets over TEN paths', 'alone-tree reading', 'stays In Progress', 'SHIPS-WITH text ≤ 3 sentences each and KEY-FREE', 'NOT-PINNED rows NAMED', 'NOT-PINNED for its own', 'READ THE WHOLE TEST FILE before proposing a cell', 'sha256 + byte count IN the mail', 'NOT-TESTED written FIRST', 'the CONTEXT RULE: at ctx 80 write report.md']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree', 'lsof -nP -iTCP:4003 -sTCP:LISTEN', 'lsof -nP -iTCP:4004 -sTCP:LISTEN', 'lsof -nP -iTCP:4005 -sTCP:LISTEN', 'lsof -nP -iTCP:6000 -sTCP:LISTEN', 'lsof -nP -iTCP:5432 -sTCP:LISTEN', 'GATEWAY_URL=http://127.0.0.1:', 'NAMESPACE GUARD', 'SIX lines, one per PR', 'MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', 'COMMA-separated', '## MERGE ADDENDUM', 'MG-3 (the KEY-SET rule', 'node_modules per ENTRY', 'MAIL YOUR VERDICT', 'no memory maintenance', 'NEVER print a credential value', 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'NEVER touch the push-window lock directory', 'by ANCESTRY', 'never by a basename', 'RED-FIRST', 'first act asserts', 'the END STATE is yours to name']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('## MERGE ADDENDUM', '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run', 'outside __tests__` == the declared PRODUCT set', 'The section `.opts` files are TWO lines'), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier, kind, prod in PRS:
    if not online(ns_sentence(n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt:', ns_sentence(n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk)); sys.exit(1)
    if not online('#%s %s: TIER %d' % (n, tk, tier), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER %d' % (n, tk, tier)); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 12 items + the closing, all present in the prompt')
HEADER_LINES = '\n'.join('#   #%s PR %s %s %s @ %s  %s %s +%d/-%d — TIER %d' % (n, p, tk, tags, h[:9], 'TEST-ONLY' if kind == 'test_only' else 'CODE_PATCH (product: %s)' % ' + '.join(x.split('/')[-1] for x in prod), ' + '.join(x.split('/')[-1] for x in fw), adds, dels, tier) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p, tier, kind, prod in PRS)
L = r'''#!/bin/bash
# launch_qa_secuura_batch__FIRST__-__LAST__.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate over SIX Secuura/Blockchain PRs (Seat C 18th):
# TIER 1 on FOUR (__TIERONES__ — KS-947 the MFA-limiter auth-surface pin + the THREE code_patch PRs with PRODUCT bytes on api-gateway), TIER 2 on
# the two test-only pins; seven local-model R16 ROUND-2 READYs (three run patches strict + four code_patch runs applied per SECTION file, the ONE
# .opts accommodation on KS-1231 Part B section 1) grouped by TICKET = by FILE into six PRs on ONE lane — api-gateway vitest — TEN paths, the ONE
# same-file PAIR health.ts (#1171 Part B + #1173: the merging seat passes --pair-blob on #1173 after #1171), ZERO overlap with Seat B 18th's nine.
__HEADERLINES__
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 8c2f7b3fd: each head's parent IS that
# commit) by pure tree hashing; the all-6 tree over the parent (52853c8bf6c4…) by REAL applies of the 11 canonicals in three orders AND real
# 3-way merges of the heads in four orders in a --shared scratch clone under a cwd guard (predict_batch_scratch_*.out) AND by tree hashing with
# health.ts at the PAIR blob; every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets18.py wants exactly ONE equality target PER PR FILE (1/1/1/4/2/2 = ELEVEN over TEN paths) and parses the
# list non-greedily to the FIRST `;` — three multi-file lines this round (#1171 four, #1173 two, #1175 two: the COMMA-separated MG-2 form is
# EXERCISED); #1173's health.ts target is the ALONE blob bca1d9500aa3 by construction and is REWRITTEN to the PAIR blob ae6017a84cf7… at merge
# time (--pair-blob, the 2026-09-21 21:02 ruling); merge18b.py asserts each squash body's key set == the PR's OWN Refs set (one key each).
# Batched under Kam 2026-09-18 standing rule. SIX verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All six tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 8c2f7b3fd (tree 04b05e093ad8 — the #1036 KS-763 squash the
# seat itself wrote FIRST on Wednesday's separate GO, over 3916eacd1). ORIGIN DEVELOP: the pin is __DEV__ (tree __DEVTREE__) — UNMOVED since
# the raise at generation (behind __BEHIND__); the compare per PR reads develop...head = merge_base 8c2f7b3fd, ahead 1, BEHIND __BEHIND__, files
# 1/1/1/4/2/2 (exit 10 — a develop move changes `behind` and REFUSES: re-pin deliberately — Seat B 18th's GO may land its seven merges first).
# ALL SIX over the parent = 52853c8bf6c4ff43585cdade61c637ff8cbaa5d0; ALL SIX over the current develop = __ALLDEV__ (the END STATE if every merge
# lands on __DEVSHORT__).
#
# The develop pin is judged by CONTENT — the 10 target paths at the CURRENT develop (five NEW files judged ABSENT — any present blob -> exit 19
# LANDED if it is the head blob, exit 18 otherwise; the five MODIFIED files by blob — health.ts LANDED on EITHER alone blob OR the PAIR blob) plus
# __NUNCH__ unchanged-read paths (index.ts — this round's other tamper file; the 16th's seven other tamper files; the 15th's five; the hook,
# preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, audit-baseline.json (#1036's), proxy.ts, the ks1072 / ks815 / ks1123-f2 /
# ks1123-f3 test files the census and the covers name, api-gateway's package.json / vitest.config.ts / tsconfig.json / lock, packages/shared's
# package.json / config, the Dev package.json + lock, eslint.config.mjs). GUARDED on a move: api-gateway src + config, packages/shared src +
# config, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs (originate / anchoring / auth — Seat B 18th's lanes — are NOT
# guarded: a Seat B merge is a disjoint move by the partition, still refused at exit 10 by `behind`).
#
# SOURCE = gatesets/2026-09-22_gate18C_seatC/mail_gate18C_ready.md, the seat's six READY mails (23:37:46Z … 00:32:55Z; PR 4's carries BOTH KS-1231
# READY rows) + its 22:55:59Z, 23:26:38Z and 00:42:07Z STATUS mails + its two QUESTION mails, each captured verbatim by message id from
# wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry TIER 1 on FOUR of the six AND each PR own tier line (__TIERLIST__).
# exit 10: the compare per PR (merge_base 8c2f7b3fd, ahead 1, behind __BEHIND__, files 1/1/1/4/2/2) — develop moving refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SIX verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1148-#1166), the EARLIER REPORT (#1147-#1161), the OLDER REPORT
#          (#1036 KS-763) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE, the `## MERGE ADDENDUM` heading targets18.py
#          parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-c18-*, s-b18-*) and writing in the seat 2026-09-22_seatC-18th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 / :4005 / :6000 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the all-6
#          tree, the pair / trio trees, the eleven head blobs + the PAIR blob, the eleven canonical sha16s, the five develop blobs, the suite
#          counts, the red/green words, the lock words, the attributions, the archived / content keys, the GO string), and the prompt must ask the
#          gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-6 tree in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket the PR is (PR #__FIRST__ is KS-947. … ).
# exit 33: the prompt must carry Wednesday SIX-PR BY-NAME items (twelve), each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; inherited, never expected this round.
# exit 35: the prompt must carry the PAIR: `--pair-blob`, the pair blob ae6017a84cf7aff42e17e1fe06ed66032e513d8c in full, and `alone blob`.
# QAB1167_CUR_DEV (test override, --check only): stands in for origin develop. QAB1167_HEAD___LAST__ (test override): stands in for #__LAST__ pinned head.
# QAB1167_BRIEF / QAB1167_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1167_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate18C_seatC/gen_launcher_gate18C.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_gate16C.py / gen_launcher_gate15.py.
#
# Usage: launch_qa_secuura_batch__FIRST__-__LAST__.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..35 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1167_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1167_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation (= the heads' parent; a move refuses at exit 10 / 18)
MERGE_BASE='8c2f7b3fd4fde915b2a24542bc32259b24e092a0'    # every head's parent = the merge-base with the current develop (the #1036 squash)
ALL_OVER_DEV='__ALLDEV__'     # all six over the CURRENT develop (real applies + 3-way merges; generator tree-hash) — the END STATE
ALL_OVER_PARENT='52853c8bf6c4ff43585cdade61c637ff8cbaa5d0'   # all six over the parent 8c2f7b3fd (the seat's measure18b; three + four orders)
PAIR_BLOB='ae6017a84cf7aff42e17e1fe06ed66032e513d8c'   # health.ts with BOTH hunks — #1173's --pair-blob target after #1171
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 8c2f7b3fd, ahead 1, behind __BEHIND__,
# files 1/1/1/4/2/2 (generator, rev-list --left-right; the launcher reads the compare API). A develop move -> exit 10.
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
CUR_DEV="${QAB1167_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
AG = D + "services/api-gateway/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob or ABSENT: label}, LANDED blobs {blob: label})
JUDGED = {
__JUDGED__
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob or the PAIR blob, exit 19).
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the heads parent; behind __BEHIND__; all six together " + all_over_dev + " over it, three + four orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           AG + "src/", AG + "package.json", AG + "vitest.config.ts", AG + "tsconfig.json", AG + "package-lock.json",
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-6 tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (predict_batch_scratch_gate18C.py + gen_launcher_gate18C.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 1 on FOUR' "$PROMPT_FILE" && __TIERGREP__ \
  || { echo "REFUSING: prompt does not carry TIER 1 on FOUR of the six and each PR own tier line (__TIERLIST__)" >&2; exit 7; }
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
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qF -- '--pair-blob' "$PROMPT_FILE" && grep -qF "$PAIR_BLOB" "$PROMPT_FILE" && grep -qF 'alone blob' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the PAIR (--pair-blob, the pair blob $PAIR_BLOB in full, 'alone blob')" >&2; exit 35; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-c18-batch' "$PROMPT_FILE" && grep -qF 's-b18-' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatC-18th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-c18-*, s-b18-*) and writing in the seat 2026-09-22_seatC-18th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:6000 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 / :4005 / :6000 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in __BOTHLOOP__; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-6 tree, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #__FIRST__ is KS-947. … )" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday twelve by-name items (tier/round; product-as-declared; the trees, the pair and the zero overlap; canonical identity strict; the cells with the red/green protocol; the per-file typecheck; the census rule; Linear hygiene; the two-seat artefacts; the seat findings/slips; the intermittents; the addendum) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries TIER 1 on FOUR and each PR tier (__TIERLIST__); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SIX verdict lines"
  echo "  prompt names the report directory, the #1148-#1166 PRIOR REPORT, the #1147-#1161 EARLIER REPORT, the #1036 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt carries the PAIR (--pair-blob, the pair blob in full, the alone blob)"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-c18-*, s-b18-*) and the seat 2026-09-22_seatC-18th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 / :4005 / :6000 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the all-6 tree, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each PR is"
  echo "  prompt carries Wednesday twelve by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1167_CUR_DEV:-}" ] && echo "  (develop read from the QAB1167_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1167_BRIEF:-}${QAB1167_PROMPT:-}${QAB1167_HEAD___LAST__:-}${QAB1167_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
__ENTERQA__ || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__HEADERLINES__': HEADER_LINES, '__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__DEVTREE__': DEV_TREE[:12], '__DEVSHORT__': DEV[:9], '__ALLDEV__': ALL_OVER_DEV, '__BEHIND__': str(BEHIND), '__NUNCH__': str(len(UNCHANGED)),
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__EARLIER__': EARLIER, '__OLDER__': OLDER_R, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME)),
        '__TIERLIST__': TIER_LIST, '__SUBJECT__': SUBJECT, '__LAST__': LAST, '__FIRST__': FIRST, '__ENTERQA__': 'c' + 'd' + ' "$QA_DIR"', '__TIERONES__': ' '.join('#' + R.PRS[p]['n'] for p in R.TIER1)}
for k, v in sorted(SUBS.items(), key=lambda kv: -len(kv[0])):
    if s.count(k) == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z0-9]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z0-9]+__', s)); sys.exit(2)
# 4. output controls
want = {DEV: 2, ALL_OVER_DEV: 2, ALL_OVER_PARENT: 3, PARENT: 2, R.PAIR_BLOB: 4, 'behind=%d' % BEHIND: len(PRS), BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, EARLIER: 1, OLDER_R: 1,
        'exit 6': 2, 'exit 10': 6, 'exit 19': 3, 'exit 18': 5, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 34': 2, 'exit 35': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': len(BLOBS) + len(UNCHANGED), ' own"': 11, 'the PAIR (#1171 + #1173)"': 1, 'PENDING-PR-': 3, '"ABSENT": DV': 5,
        'QAB1167_CUR_DEV': 5, 'QAB1167_HEAD_' + LAST: 3, 'refs/pull/$_n/head': 2,
        SUBJECT: 1, 'PR #%s is KS-947.' % FIRST: 3, GO_STRING: 1}
for n, tk, tags, br, h, *_ in PRS: want[h] = 1
if DEV == PARENT: want[DEV] = 4            # unmoved: DEVELOP_SHA + MERGE_BASE + the two header mentions are ONE string
if ALL_OVER_DEV == ALL_OVER_PARENT: want[ALL_OVER_DEV] = 4   # ALL_OVER_DEV + ALL_OVER_PARENT + the header's two mentions are ONE string
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
tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.sh', prefix='gen18C.bashn.', dir=os.path.dirname(os.path.dirname(os.path.realpath(SCR)))); tmp.write(s); tmp.close()   # the bash -n copy lives in the drafter's scratchpad, never in launchers/
p = subprocess.run(['bash', '-n', tmp.name], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp.name); sys.exit(3)
if os.path.exists(OUT): shutil.copy2(OUT, OUT + '.pre-' + now('+%H%M'))   # a COPY beside, never a rename
open(OUT, 'w', encoding='utf-8').write(s); os.chmod(OUT, 0o755)   # the bash -n tmp stays in the scratchpad (never deleted, never renamed)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest(), 'lines', s.count('\n'))
