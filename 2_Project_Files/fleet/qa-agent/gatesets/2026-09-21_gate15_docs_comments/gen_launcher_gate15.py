#!/usr/bin/env python3
"""gen_launcher_gate15.py — write launchers/launch_qa_secuura_batch1136-<last>.sh (ONE batched tier-2-floor round-1 gate over TEN Secuura/Blockchain
PRs #1136 … #<last>, Seat B 15th: five DOCS-ONLY + five TEST-FILE-COMMENT-ONLY PRs; READYs 2026-09-21T12:34:14Z-…) in the SHAPE of
gatesets/2026-09-21_gate1130to1135/gen_launcher_1130.py (pins re-read at generation, tree hashing, output controls, heredoc parity, bash -n):
exit 6 a head moved · 10 the compare per PR (merge_base = the heads' parent 581ed7fa1, ahead 1, BEHIND = the develop move count at generation (3:
#1138), files — develop moving AGAIN changes `behind` and REFUSES) · 18/19 the develop pin judged by CONTENT with LANDED detection · 34 a PARTIAL
prompt (any `PENDING-PR-` token) refuses both --check and the launch · the prompt + READY greps · 16 overrides at launch · 21 TTY.
Pins are RE-READ at generation, READ-ONLY throughout — no git write verb in the Secuura checkout:
  * the PR numbers and heads come from the captured READY mails (mail_seatB15_ready*_pr<N>_*.md) and are asserted against the pinned trees; with
    FEWER than ten captured the generator writes a PARTIAL launcher (launch_qa_secuura_batch15_partial.sh) that pins the present heads and refuses
    at exit 34 — a record, not a launch;
  * origin: git ls-remote of refs/heads/develop (the CURRENT tip = the pin), every present refs/pull/N/head AND branch — all must equal the pins;
  * local objects (rev-list / rev-parse / diff --raw / diff --numstat / ls-tree): each head is ONE commit whose parent IS 581ed7fa1; the (path,
    develop blob, head blob) pairs as pinned; the paths pairwise disjoint; every path `.md` or under __tests__/; every unchanged-read path has the
    SAME blob at 581ed7fa1, at the CURRENT develop (read in the scratch clone that fetched it by SHA — argv[2]) and at every head; the per-PR trees;
    the all-ten tree over 581ed7fa1 by pure tree hashing (must equal a93fe063d28a… and predict_batch_scratch_*.out);
  * every value the launcher carries is asserted present in its output exactly as often as intended (output controls), every BOTH-list token is
    asserted present in BOTH the READY capture and the prompt, heredoc quote/paren parity is checked, and `bash -n` must pass, or nothing is written.
Usage: gen_launcher_gate15.py <output launcher> <scratch clone holding the current develop by SHA>
Exit: 0 written · 1 pin/control disagreed · 2 residual token · 3 bash -n"""
import glob, hashlib, itertools, json, os, re, subprocess, sys, tempfile, urllib.request
OUT = sys.argv[1]; SCR = sys.argv[2]
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date'] + (['-u'] if f.endswith('Z') else []) + [f], capture_output=True, text=True).stdout.strip()   # S2: a Z-suffixed format must be read with -u
print('gen_launcher_gate15', now(), now('+%Y-%m-%dT%H:%M:%SZ'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments'
PARENT = '581ed7fa124b85c7c2da89ac05d52f99c2502911'; PARENT_TREE = '60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b'
ALL_OVER_PARENT = 'a93fe063d28ae66d4a90e1926b78364a7a578ff4'
D = 'Blockchain/Dev/'; SH = D + 'packages/shared/'; OR = D + 'services/originate/'; VC = D + 'services/vc-issuer/'; AG = D + 'services/api-gateway/'; SC = D + 'scripts/'
# seat PR -> (ticket(s), tags, branch, head tree (= tree over the parent), file count, adds, dels, files)
SEAT = {
  '1': (['KS-1035', 'KS-1036'], 'D + item3', 'refs/heads/feature/ks-1035-the-merge-gate-cannot-see-a-withdrawn-approval-813-reads-r15-d-item3-1', '4cd290a2c80eaad2028e45d2d54628898a7d9db7', 1, 12, 0, [D + 'docs/DEV-PROCESS.md']),
  '2': (['KS-1037', 'KS-1049'], 'R15 + A', 'refs/heads/feature/ks-1037-the-no-force-push-rule-exists-only-in-githookspre-push-and-r15-a-1', '0edbb8341e603ab864115c0cd3980fc5bee2eb76', 1, 10, 0, [D + 'CONTRIBUTING.md']),
  '3': (['KS-1045'], 'A + B', 'refs/heads/feature/ks-1045-kintsugi-dev-server-planmd-still-says-the-vm-has-not-been-r15-a-b-1', 'd1ba6f8882fd', 1, 3, 3, [D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md']),
  '4': (['KS-1097'], 'Da', 'refs/heads/feature/ks-1097-merge-rule-docs-after-957-the-v4-footer-and-two-gate-r15-da-1', '4f0a8c67f95f', 1, 1, 1, ['CLAUDE.md']),
  '5': (['KS-890'], 'R15', 'refs/heads/feature/ks-890-runbook-a-code-first-deploy-leg-must-use-docker-compose-up-d-r15-1', '374c0328a8c5', 1, 8, 0, [D + 'deployment/DEPLOYMENT-ARCHITECTURE.md']),
  '6': (['KS-1140'], 'GF2GF4', 'refs/heads/feature/ks-1140-ks879-guard-the-cell-walks-the-tree-on-its-own-r15-gf2gf4-1', '99a9adaf3151', 1, 2, 2, [SH + 'src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts']),
  '7': (['KS-1152'], 'R1c + R1d', 'refs/heads/feature/ks-1152-l5-gate-records-799880985-jwtts-citation-x5-security-log-r15-r1c-r1d-1', '6e95645e29fb', 2, 5, 3, [SH + 'src/__tests__/ks764-key-revoke-call-site-guard.test.ts', OR + 'src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts']),
  '8': (['KS-979'], 'R15', 'refs/heads/feature/ks-979-own-bind-test-file-repeats-two-claims-that-were-r15-1', '366ec698c266', 1, 6, 2, [OR + 'src/__tests__/ks597-issuer-org-bind.test.ts']),
  '9': (['KS-1120'], 'F3', 'refs/heads/feature/ks-1120-get-apipresentationsid-exact-or-404-the-memory-path-prefix-r15-f3-1', '07d01c8ae4f5', 1, 5, 3, [VC + 'src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts']),
  '10': (['KS-1156'], 'A3', 'refs/heads/feature/ks-1156-auth4-gate-records-983-r2-984-r2-986-987-h-limiter-r15-a3-1', '9fdeab78e610', 1, 1, 1, [AG + 'src/__tests__/ks835-oauth-token-scope-gate.test.ts']),
}
BLOBS = {D + 'docs/DEV-PROCESS.md': ('c9cd41d588a2', 'ab9a70f13e3c'), D + 'CONTRIBUTING.md': ('953067eb7aa7', 'b3cc10a40089'), D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md': ('bbd5bbf78778', '5ba84caf2e30'),
         'CLAUDE.md': ('dd782eab7435', 'ef2f8fc2e4cb'), D + 'deployment/DEPLOYMENT-ARCHITECTURE.md': ('daabe1087bb9', '622c0e505278'),
         SH + 'src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts': ('7f0ac617f675', '9ce9e852ae44'), SH + 'src/__tests__/ks764-key-revoke-call-site-guard.test.ts': ('ab8e46d795d2', '6a51358e3619'),
         OR + 'src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts': ('eb7782db8816', '57de2c6753e4'), OR + 'src/__tests__/ks597-issuer-org-bind.test.ts': ('9bb899a10677', 'bed97468d499'),
         VC + 'src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts': ('eb0e5305c815', 'b7949520cf03'), AG + 'src/__tests__/ks835-oauth-token-scope-gate.test.ts': ('548e1ec1217e', '595bed15d859')}
PUSH = [str(i) for i in range(1, 11)]
READY = {}
for f in sorted(glob.glob(os.path.join(GS, 'mail_seatB15_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 15th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (m.group(3), m.group(4))
present = [p for p in PUSH if p in READY]; missing = [p for p in PUSH if p not in READY]; PARTIAL = bool(missing)
print('READYs captured for seat PRs', present, '| missing', missing or 'none', '| PARTIAL' if PARTIAL else '| COMPLETE')
# n, ticket(s), tags, branch, head, head tree, nfiles, adds, dels, files — in push order, present only
PRS = [(READY[p][0], SEAT[p][0], SEAT[p][1], SEAT[p][2], READY[p][1], SEAT[p][3], SEAT[p][4], SEAT[p][5], SEAT[p][6], SEAT[p][7], p) for p in present]
N = {p: READY[p][0] for p in present}; LAST = max(N.values(), key=int)
print('PR numbers (push order):', [n for n, *_ in PRS], '| last', LAST)
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
def out(*a):
    p = git(*a)
    if p.returncode: print('REFUSING: git', a[:3], p.stderr.strip()[:200]); sys.exit(1)
    return p.stdout
def sgit(*a): return subprocess.run(['git', '-C', SCR] + list(a), capture_output=True, text=True).stdout.strip()
# 1. origin
refs_wanted = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n, *_ in PRS] + [br for _, _, _, br, *_ in PRS]
lsr = out('ls-remote', 'origin', *refs_wanted)
print('ls-remote', now('+%Y-%m-%dT%H:%M:%SZ'), '|', len(lsr.strip().splitlines()), 'refs read (want %d)' % len(refs_wanted))
refs = dict((l.split('\t')[1], l.split('\t')[0]) for l in lsr.strip().splitlines())
DEV = refs.get('refs/heads/develop', '?')
print('origin develop NOW (the pin):', DEV, '| the heads parent', PARENT[:9], '| moved since the raise:', DEV != PARENT)
if not re.fullmatch(r'[0-9a-f]{40}', DEV): sys.exit(1)
want = [('refs/pull/%s/head' % n, h) for n, _, _, _, h, *_ in PRS] + [(br, h) for _, _, _, br, h, *_ in PRS]
for ref, w in want:
    print('  %-122s %s %s' % (ref, refs.get(ref, '?')[:9], 'OK' if refs.get(ref) == w else 'MOVED'))
    if refs.get(ref) != w: print('REFUSING: pin moved at origin'); sys.exit(1)
if subprocess.run(['git', '-C', SCR, 'cat-file', '-e', DEV + '^{commit}']).returncode: print('REFUSING: the current develop', DEV[:9], 'is not in the scratch clone', SCR, '- re-run predict_batch_scratch_gate15.py'); sys.exit(1)
DEV_TREE = sgit('rev-parse', DEV + '^{tree}'); BEHIND = int(sgit('rev-list', '--count', PARENT + '..' + DEV) or '0'); MB = sgit('merge-base', PARENT, DEV)
print('current develop tree', DEV_TREE[:12], '| rev-list --count parent..develop =', BEHIND, '| merge-base(parent, develop) == parent:', MB == PARENT)
if MB != PARENT: sys.exit(1)
moved = set(sgit('diff', '--name-only', PARENT, DEV).splitlines()); print('develop move touches', len(moved), 'paths; ∩ the 11 target paths:', sorted(moved & set(BLOBS)) or 'NONE')
if moved & set(BLOBS): print('REFUSING: the develop move touches a target path'); sys.exit(1)
# 2. local objects
dt = out('rev-parse', PARENT + '^{tree}').strip(); print('parent tree', dt[:9], '==', PARENT_TREE[:9], dt == PARENT_TREE)
if dt != PARENT_TREE: sys.exit(1)
CHANGED = {}; PERPR = {}
for n, tk, tags, br, h, ht, nf, adds, dels, files_want, p in PRS:
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', PARENT + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    raw = out('diff', '--raw', '--abbrev=40', PARENT, h).strip().splitlines()
    ns = {l.split('\t')[2]: (int(l.split('\t')[0]), int(l.split('\t')[1])) for l in out('diff', '--numstat', PARENT, h).strip().splitlines()}
    files = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); files[path] = (b1, b2, st, m2, n)
    a_sum = sum(v[0] for v in ns.values()); d_sum = sum(v[1] for v in ns.values())
    ok_kind = all(x.endswith('.md') or '/__tests__/' in x for x in files)
    print('#%s PR %s %s head %s parent==PARENT %s | parent...head behind/ahead %s (want 0 1) | tree %s == pin %s | files %s == %s | +%d/-%d (want +%d/-%d) | modes %s | every path .md or __tests__/: %s' % (
        n, p, '+'.join(tk), h[:9], par == [PARENT], lr, t[:12], t.startswith(ht), sorted(files), sorted(files) == sorted(files_want), a_sum, d_sum, adds, dels, sorted({v[3] for v in files.values()}), ok_kind))
    if par != [PARENT] or lr != ['0', '1'] or not t.startswith(ht) or sorted(files) != sorted(files_want) or a_sum != adds or d_sum != dels or any(v[3] != '100644' for v in files.values()) or any(v[2] != 'M' for v in files.values()) or not ok_kind: sys.exit(1)
    for p_, v in files.items():
        if p_ in CHANGED: print('REFUSING: path in two PRs', p_); sys.exit(1)
        if not v[0].startswith(BLOBS[p_][0]) or not v[1].startswith(BLOBS[p_][1]): print('REFUSING: pinned blob disagrees for', p_, v[:2]); sys.exit(1)
        CHANGED[p_] = v
    PERPR[n] = files
overl = [(a, b) for a, b in itertools.combinations(PERPR, 2) if set(PERPR[a]) & set(PERPR[b])]
print('union paths', len(CHANGED), '(want %d) | pairwise overlaps' % sum(nf for *_a, nf, adds, dels, fw, p in PRS), overl, '(want none)')
if overl: sys.exit(1)
FULLDEV = {}
for p_ in BLOBS:
    bd = out('rev-parse', PARENT + ':' + p_).strip(); bc = sgit('rev-parse', DEV + ':' + p_)
    if not bd.startswith(BLOBS[p_][0]) or bc != bd: print('REFUSING: target blob differs at the parent or the current develop', p_, bd[:12], bc[:12]); sys.exit(1)
    FULLDEV[p_] = bd
print('the 11 (develop blob) values agree at 581ed7fa1 AND at the current develop; the landed head blobs agree with the GROUPING: True')
TAMPER14 = ['Blockchain/Testing/jobs/04-container-trivy.sh', 'systemTest/fixtures/manifest.ts', D + 'services/security/src/index.ts', D + 'services/auth/src/routes/users.ts', SC + 'check-shared-relink.sh']
UNCHANGED = TAMPER14 + ['.githooks/pre-push', SC + 'preflight/preflight.sh', SC + 'run-shell-suites.sh', SC + 'fix-libsodium-symlink.js',
             D + 'services/auth/src/services/jwt.ts', OR + 'src/services/provenance.ts', AG + 'src/routes/proxy.ts',
             SH + 'package.json', SH + 'vitest.config.ts', SH + 'tsconfig.json',
             OR + 'package.json', OR + 'tsconfig.json', OR + 'jest.config.js', OR + 'package-lock.json',
             VC + 'package.json', VC + 'vitest.config.ts', VC + 'tsconfig.json', VC + 'package-lock.json',
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
print('unchanged-read paths', len(UNCHANGED), 'all same blob at the parent, at the current develop and at every landed head: True (the first', len(TAMPER14), 'are the 14th tamper files)')
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
for n, tk, tags, br, h, ht, nf, adds, dels, fw, p in PRS:
    mt = compose(PARENT_TREE, {p_: (v[3], v[1]) for p_, v in PERPR[n].items()})
    print('  #%s compose over the parent -> %s == head tree %s (fast-forward there)' % (n, mt[:9], mt.startswith(ht)))
    if not mt.startswith(ht): sys.exit(1)
nd = open(os.path.join(GS, 'newdev_tree.txt')).read()
ALL_OVER_DEV = re.search(r'^ALL14_OVER_NEW ([0-9a-f]{40})', nd, re.M).group(1); NEWTREE = {}
for l in nd.splitlines():
    m = re.match(r'^PR(\d+) ([0-9a-f]{40})', l)
    if m: NEWTREE[m.group(1)] = m.group(2)
if re.search(r'^DEV_NOW ([0-9a-f]{40})', nd, re.M).group(1) != DEV: print('REFUSING: newdev_tree.txt is for another develop — re-run predict_batch_scratch_gate15.py'); sys.exit(1)
allp = {p_: ('100644', git('rev-parse', PARENT + ':' + p_).stdout.strip()) for p_ in BLOBS}
# the all-ten over the parent from the GROUPING head blobs (landed ones from the objects; the rest by prefix are asserted when they land)
if not PARTIAL:
    ad = compose(PARENT_TREE, {p_: (v[3], v[1]) for p_, v in CHANGED.items()})
    print('compose(the 10 into the parent tree) ->', ad, '==', ALL_OVER_PARENT[:9], ad == ALL_OVER_PARENT)
    if ad != ALL_OVER_PARENT: sys.exit(1)
    ad2 = compose(DEV_TREE, {p_: (v[3], v[1]) for p_, v in CHANGED.items()}, SCR)
    print('compose(the 10 into the CURRENT develop tree) ->', ad2, '==', ALL_OVER_DEV[:9], ad2 == ALL_OVER_DEV)
    if ad2 != ALL_OVER_DEV: sys.exit(1)
else:
    print('PARTIAL: the all-ten compose is asserted only when all ten heads have landed; the all-14 canonical tree over the current develop is', ALL_OVER_DEV[:12], '(predict_batch_scratch)')
for n, *_r in PRS:
    p = _r[-1]; mt2 = compose(DEV_TREE, {p_: (v[3], v[1]) for p_, v in PERPR[n].items()}, SCR)
    if mt2 != NEWTREE[p]: print('REFUSING: merged tree over the current develop disagrees with predict_batch_scratch for PR', p, mt2[:12], NEWTREE[p][:12]); sys.exit(1)
print('per-PR merged trees over the current develop == predict_batch_scratch (real 3-way / canonical apply):', len(PRS), 'of', len(PRS))
pms = sorted(glob.glob(os.path.join(GS, 'predict_batch_scratch_*.out'))); pm = open(pms[-1]).read()
print('newest predict_batch_scratch out:', os.path.basename(pms[-1]), '| all-14 over the parent three orders:', 'all three identical: True | == the seat/drafter all-14 tree %s: True' % ALL_OVER_PARENT in pm, '| byte-identical:', 'byte-identical to before: True' in pm, '| empty-repo rc=128:', 'rc=128 (want 128)' in pm)
# 3. the launcher
BRIEF = GS + '/mail_gate15_ready.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/' + ('2026-09-21_secuura-batch15_partial.prompt.txt' if PARTIAL else '2026-09-21_secuura-batch1136-%s.prompt.txt' % LAST)
REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1136-%s-tier2-r1/' % (LAST + '-PARTIAL' if PARTIAL else LAST)
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-1135-tier1-r1/'
EARLIER = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
OLDER_R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
for d_ in (PRIOR, EARLIER, OLDER_R):
    if not os.path.isdir(d_): print('REFUSING: report dir absent', d_); sys.exit(1)
brief_txt = open(BRIEF, encoding='utf-8').read(); prompt_txt = open(PROMPT, encoding='utf-8').read()
if not PARTIAL and 'NOT YET ARRIVED' in brief_txt: print('REFUSING: the combined capture has a section NOT YET ARRIVED'); sys.exit(1)
def online(kw, lines): return any(kw in l for l in lines)
def jline(path, ok, landed):
    return '  %-118s (%s, %s),' % ('"' + path + '":', '{"%s": DV}' % ok, ('{' + ', '.join('"%s": "%s"' % x for x in landed) + '}') if landed else '{}')
judged = [jline(p_, FULLDEV[p_], [(CHANGED[p_][1], '#%s own' % CHANGED[p_][4])] if p_ in CHANGED else []) for p_ in BLOBS]
judged += [jline(p_, UBLOB[p_], None) for p_ in UNCHANGED]
JUDGED_BLOCK = '\n'.join(judged)
PRS_BLOCK = '\n'.join('  "%s|%s|%s|%s|%d"' % (n, '+'.join(tk), br, ('${QAB1136_HEAD_%s:-%s}' % (LAST, h)) if n == LAST else h, nf) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p in PRS)
WANT_COMPARE = '\n'.join('%s $MERGE_BASE ahead=1 behind=%d files=%d' % (n, BEHIND, nf) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p in PRS)
TIER_GREP = ' && '.join("grep -qF '#%s %s: TIER 2' \"$PROMPT_FILE\"" % (n, ' + '.join(tk)) for n, tk, *_ in PRS)
def ns_sentence(n, tk): return 'PR #%s is %s.' % (n, ' + '.join(tk))
NS_GREP = ' && '.join("grep -qF '%s' \"$PROMPT_FILE\" && grep -F '#%s' \"$BRIEF\" | grep -qF '%s'" % (ns_sentence(n, tk), n, tk[0]) for n, tk, *_ in PRS)
TIER_LIST = ', '.join('#%s T2' % n for n, *_ in PRS)
SUBJECT = '[QA -> Wednesday] BATCH GATE #1136-#%s (ten PRs; tier 2 floor: five docs + five test-file comments)' % (LAST + '-PARTIAL' if PARTIAL else LAST)
HEADS_LIST = ' '.join('#%s@%s' % (n, h[:9]) for n, tk, tags, br, h, *_ in PRS)
# exit 30: seat items in BOTH the READY capture and the prompt
BOTH = ['18499832', ALL_OVER_PARENT, '60bd96e7078c', PARENT, 'a39d35b05', DEV[:9]] + [ht[:12] for *_a, ht, nf, adds, dels, fw, p in PRS] + [
        'ab9a70f13e3c', 'b3cc10a40089', '5ba84caf2e30', 'ef2f8fc2e4cb', '622c0e505278', '9ce9e852ae44', '6a51358e3619', '57de2c6753e4', 'bed97468d499', 'b7949520cf03', '595bed15d859',
        '849507a10f99b9ab', '8a49e7c68318cb58', 'b9ed6eb6bac788a7', 'd5a07523e6a450f7', '2497bea61ff7789f', '66aa75dfcf5ea1f3', 'd41e4136c612bac5', '3b8d82cf560c2605',
        '42486061ffa4448e', '31ae771c8a5f8fe5', '7ddcf0309e15ba55', '1c0121de5b00ce95', 'ee3c484b2aff8ff0', '8d60c7b67227561c',
        '907/907', '809/809', '123/123', '697/697', 'corrupt patch at line 16', 'corrupt patch at line 19', 'corrupt patch at line 10', 'DEV-PROCESS.md:224', '--recount',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'login_stub', 'mergeable_state', 'stubs=4', '44 passed, 0 failed (of 44)', 'PROTOCOL-CLEAN',
        'DOCS-ONLY', 'const x = 1;', 'IDENTICAL', 'tsc', 'eslint', 'TS2322', 'typecheck16', 'STOP-class 0', 'netlog.cjs', ':5432',
        'az vm show', 'SECUURA-DEMO-RG', 'secuura02-kintsugi-vm', 'ResourceNotFound', 'Enabled', 'step 6', ':303', 'seven times', 'generateAccessToken', 'provenance.ts:109',
        'F1', 'F2', 'F4', 'F5', 'F8', 'S1', 'linear[bot]', 'attachmentsForURL', 'contributes', 'Refs KS-1035', 'Refs KS-1036', 'Refs KS-1037', 'Refs KS-1049',
        'KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490', 'KS-597', 'KS-727',
        'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-869', 'KS-601', 'KS-973', 'KS-1118', 'KS-1158', 'KS-1181',
        'x5', 'ks879', 'Deviation from verbatim', '<= 92 chars', '#920', '#887', 'b192ffd4a', 'MOVED', 'Live-but-foreign']
if not PARTIAL: BOTH += ['GO: merge ' + ', '.join('#' + n for n, *_ in PRS) + ' batch']   # the seat's READY 10 lists the numbers (non-contiguous: #1138 is foreign)
missing_b = [t for t in BOTH if not online(t, brief_txt.splitlines()) or not online(t, prompt_txt.splitlines())]
if missing_b: print('REFUSING: BOTH-list token(s) absent from the READY capture or the prompt:', [(t, online(t, brief_txt.splitlines()), online(t, prompt_txt.splitlines())) for t in missing_b]); sys.exit(1)
print('BOTH-list tokens', len(BOTH), 'all present in the READY capture AND the prompt')
BOTH_LOOP = ' \\\n          '.join(("'" + t + "'") if not re.fullmatch(r'[\w./:-]+', t) else t for t in BOTH)
BYNAME = [
 ('1', ['TIER AND ROUND', 'round 1 of 2', 'outside __tests__ and *.md: []', 'files API union 11', 'Any product byte anywhere = a NO GO']),
 ('2', ['THE TREES, RE-DERIVED', 'ELEVEN', 'ZERO overlap', 'at least forward, exact reverse and one shuffle', 'read-tree back to develop', 'every count from the RUNNER']),
 ('3', ['CANONICAL-PATCH IDENTITY', 'RE-EXTRACTED by you', 'Name any byte that differs', 'THREE by `--recount`']),
 ('4', ['COMMENT-ONLY PROOF', 'PLANTED `const x = 1;` control', 'IDENTICAL by TITLE', 'eslint 0/0 on the six files with a firing control']),
 ('5', ['DOCS-ONLY PROOF', 'exactly the one `.md`', 'GRADE THE SEAT\'S STATEMENT']),
 ('6', ['THE STALE-CLAIM FINDINGS', 'Minor SHIPS-WITH', 'dangling', 'who inherited it']),
 ('7', ["KS-1045-A's DONE row", 'PROVENANCE', 'present / absent', 'does NOT run `az`']),
 ('8', ['BRANCH NAMES', '`ks-597s-` ABSENT', 'no non-ASCII byte in ANY of the ten branch names', 'ONE `Refs` on a', 'ASCII and <= 92 chars']),
 ('9', ['LINEAR LINK HYGIENE', 'includeArchived', 'KS-1136', 'KS-1147', 'EXCEPT KS-1140 for pull/', 'Recommend nothing', 'PR #1036 is OPEN and is KS-763']),
 ('10', ['THE CENSUS RULE (v2)', 'ALLOW set', '"port":5432,', 'login_stub cleared by PID']),
 ('11', ['THE INTERMITTENTS', '5 s timeouts', 're-run standalone 3× serial', 'RULE WHETHER IT BLOCKS']),
 ('12', ['MERGE ADDENDUM — TEN lines VERBATIM', 'ONE equality target PER', 'TWO comma-separated = MG-2', 'alone-tree reading', 'stays In Progress', 'SHIPS-WITH text ≤ 3 sentences', 'NOT-PINNED rows: NONE EXPECTED', 'sha256 + byte count IN the mail']),
 ('13', ["THE SEAT'S SLIPS S1-S4 + F8 as measured", 'CONFIRMED / REFUTED', 'THE LINE-NUMBER DISCIPLINE', 'NAME', 'WHO INHERITED IT']),
 ('closing', ['NOT-TESTED.written-first.md', 'GO, GO WITH FINDINGS, or NO GO', 'Majors <n> / Minors <m>', 'NOTHING ABOUT O-1', 'must not recommend pinning either', 'GRADE THE HEADS', 'MEASURE, not conclude', 'CLOSED / STILL OPEN / NEW', 'WRITE report.md BEFORE THE MAIL', 'END EVERY LISTENER YOUR RUNS START, BY PID', 'TCP LISTEN census', 'Never enter any seat worktree', 'lsof -nP -iTCP:4003 -sTCP:LISTEN', 'lsof -nP -iTCP:4004 -sTCP:LISTEN', 'lsof -nP -iTCP:5432 -sTCP:LISTEN', 'GATEWAY_URL=http://127.0.0.1:', 'NAMESPACE GUARD', 'TEN lines, one per PR', 'MERGE ADDENDUM line PER PR', 'ONE equality target PER PR FILE', 'COMMA-separated', '## MERGE ADDENDUM', 'MG-3 (the KEY-SET rule', 'node_modules per ENTRY', 'MAIL YOUR VERDICT', 'no memory maintenance', 'NEVER print a credential value', 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout']),
]
def shq(kw):
    assert not re.search(r'[$`\\]', kw) or kw in ('## MERGE ADDENDUM', 'PLANTED `const x = 1;` control', 'exactly the one `.md`', 'THREE by `--recount`', 'does NOT run `az`', '`ks-597s-` ABSENT', 'ONE `Refs` on a'), kw
    if "'" in kw: return '"' + kw.replace('`', '\\`').replace('$', '\\$') + '"'
    return "'" + kw + "'"
plines = prompt_txt.splitlines(); blines = brief_txt.splitlines()
for n, tk, *_ in PRS:
    if not online(ns_sentence(n, tk), plines): print('REFUSING: namespace sentence wrapped or absent in the prompt:', ns_sentence(n, tk)); sys.exit(1)
    if not any(('#' + n) in l and tk[0] in l for l in blines): print('REFUSING: the READY capture has no line carrying both #%s and %s' % (n, tk[0])); sys.exit(1)
    if not online('#%s %s: TIER 2' % (n, ' + '.join(tk)), plines): print('REFUSING: tier line absent in the prompt: #%s %s: TIER 2' % (n, ' + '.join(tk))); sys.exit(1)
print('namespace + tier lines present, one line each, in the prompt (and the pairs in the READY capture): True')
bad = [kw for _, kws in BYNAME for kw in kws if not online(kw, plines)]
if bad: print('REFUSING: by-name keyword(s) absent from the prompt:', bad); sys.exit(1)
BYNAME_GREP = ' && '.join('grep -qF -- %s "$PROMPT_FILE"' % shq(kw) for _, kws in BYNAME for kw in kws)
print('by-name ladder keywords', sum(len(k) for _, k in BYNAME), 'across 13 items + the closing, all present in the prompt')
HEADER_LINES = '\n'.join('#   #%s PR %s %s %s @ %s  %s — TIER 2' % (n, p, ' + '.join(tk), tags, h[:9], ('DOCS-ONLY ' + fw[0].split('/')[-1] + ' +%d/-%d' % (adds, dels)) if fw[0].endswith('.md') else ('TEST-FILE-COMMENT-ONLY ' + ' + '.join(x.split('/')[-1] for x in fw) + ' +%d/-%d' % (adds, dels))) for n, tk, tags, br, h, ht, nf, adds, dels, fw, p in PRS)
L = r'''#!/bin/bash
# launch_qa_secuura_batch1136-__SUFFIX__.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 2 floor over TEN Secuura/Blockchain PRs
# (Seat B 15th; fourteen local-model DOC / COMMENT patches grouped by FILE into ten PRs across FIVE lanes — docs, packages/shared vitest,
# originate jest, vc-issuer vitest, api-gateway vitest — ELEVEN paths, ZERO overlap, ZERO product bytes)
__HEADERLINES__
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 581ed7fa1: each head's parent IS that
# commit) by pure tree hashing; the all-ten tree over the parent (a93fe063d28a…) and over the CURRENT develop by REAL applies + 3-way merges in a
# --shared scratch clone (predict_batch_scratch_*.out) AND by tree hashing; every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets16.py wants exactly ONE equality target PER PR FILE (1/1/1/1/1/1/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` — the two-file PR 7 addendum line carries TWO targets COMMA-separated (exit 25); merge16.py asserts each squash body's key set ==
# the PR's OWN Refs set (two keys on #1136 and #1137 only).
# Batched under Kam 2026-09-18 standing rule. TEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All twelve tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 581ed7fa1 (tree 60bd96e7078c, Seat B 14th's final state).
# ORIGIN DEVELOP HAS MOVED SINCE (PR #1138 KS-1285, a MERGE commit at 12:44:19Z, 3 commits / 7 files under systemTest/ + Projects Documents/, none
# of this round's 11 paths, none of the paths the gate reads): the pin is the CURRENT develop __DEV__ (tree __DEVTREE__); the compare per PR reads
# develop...head = merge_base 581ed7fa1, ahead 1, BEHIND __BEHIND__, files 1/1/1/1/1/1/2/1/1/1 (exit 10 — a FURTHER develop move changes `behind` and
# REFUSES: re-pin deliberately). ALL TEN over the parent = a93fe063d28ae66d4a90e1926b78364a7a578ff4; ALL TEN over the current develop = __ALLDEV__
# (the END STATE if every merge lands on __DEVSHORT__).
#
# The develop pin is judged by CONTENT — the 11 target paths by blob at the CURRENT develop (any at a head blob -> exit 19 LANDED, naming the PR;
# any other blob -> exit 18 GUARDED) plus __NUNCH__ unchanged-read paths (the 14th's five tamper files, the hook, preflight.sh, run-shell-suites.sh,
# fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts, the four lanes' package.json / config / tsconfig / lock, the Dev package.json + lock,
# eslint.config.mjs). GUARDED on a further move: shared / originate / vc-issuer / api-gateway src + config, packages/shared, scripts/, .githooks/,
# docs/, deployment/, CONTRIBUTING.md, CLAUDE.md, the Dev package.json + lock, eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate15_docs_comments/mail_gate15_ready.md, the seat's READY mails (12:34:14Z …) + the 12:30:09Z STATUS mail + the
# 12:02:12Z plan-confirmation QUESTION, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 2 floor AND each PR own tier line (__TIERLIST__).
# exit 10: the compare per PR (merge_base 581ed7fa1, ahead 1, behind __BEHIND__, files) — develop moving AGAIN refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and TEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1130-#1135), the EARLIER REPORT (#1119-#1128), the OLDER REPORT
#          (#1112-#1118) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (TWO for PR 7, comma-separated),
#          the `## MERGE ADDENDUM` heading targets16.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b15-*) and writing in the seat 2026-09-21_seatB-15th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the all-ten
#          tree, the eleven head blobs, the 14 canonical sha16s, the suite counts, the --recount rcs, the VM read words, the stale-claim words, the
#          archived / content keys, the branch-name findings, the develop move), and the prompt must ask the gate to MEASURE, not conclude, and to
#          RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-ten trees in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket(s) the PR is (PR #1136 is KS-1035 + KS-1036. … ).
# exit 33: the prompt must carry Wednesday THIRTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; a record, never a gate.
# QAB1136_CUR_DEV (test override, --check only): stands in for origin develop. QAB1136_HEAD___LAST__ (test override): stands in for #__LAST__ pinned head.
# QAB1136_BRIEF / QAB1136_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1136_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate15_docs_comments/gen_launcher_gate15.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1130.py.
#
# Usage: launch_qa_secuura_batch1136-__SUFFIX__.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1136_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QAB1136_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket(s)|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
__PRS__
)
DEVELOP_SHA='__DEV__'   # the pin = origin develop at generation (MOVED off the heads' parent by #1138; a FURTHER move refuses at exit 10 / 18)
MERGE_BASE='581ed7fa124b85c7c2da89ac05d52f99c2502911'    # every head's parent = the merge-base with the current develop
ALL_OVER_DEV='__ALLDEV__'     # all ten over the CURRENT develop (real 3-way + canonical apply, three orders; generator tree-hash) — the END STATE
ALL_OVER_PARENT='a93fe063d28ae66d4a90e1926b78364a7a578ff4'   # all ten over the parent 581ed7fa1 (the seat's octopus; three orders)
REPORT_DIR='__REPORT__'
PRIOR_REPORT='__PRIOR__'
EARLIER_REPORT='__EARLIER__'
OLDER_REPORT='__OLDER__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }
grep -qF 'PENDING-PR-' "$PROMPT_FILE" && { echo "REFUSING: the prompt is PARTIAL (a PENDING-PR- token) — re-fill once every READY is captured (README.md section 8); a partial gate is not a gate" >&2; exit 34; }

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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 581ed7fa1, ahead 1, behind __BEHIND__ (the
# #1138 move), files 1/1/1/1/1/1/2/1/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A FURTHER develop move -> exit 10.
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

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved
# further — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1136_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
VC = D + "services/vc-issuer/"
AG = D + "services/api-gateway/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the post-#1138 tip; every head parent is 581ed7fa1, behind __BEHIND__; all ten together " + all_over_dev + " over it, three orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           OR + "src/", OR + "package.json", OR + "jest.config.js", OR + "tsconfig.json", OR + "package-lock.json",
           VC + "src/", VC + "package.json", VC + "vitest.config.ts", VC + "tsconfig.json", VC + "package-lock.json",
           AG + "src/", AG + "package.json", AG + "vitest.config.ts", AG + "tsconfig.json", AG + "package-lock.json",
           SC, ".githooks/", D + "docs/", D + "deployment/", D + "CONTRIBUTING.md", "CLAUDE.md",
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-ten tree"
print("OK " + state + " | origin develop MOVED AGAIN %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_gate15.py + predict_batch_scratch_gate15.py + prompt)" >&2
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
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'TEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and TEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF 'TWO comma-separated = MG-2' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (PR 7 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b15-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-15th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b15-*) and writing in the seat 2026-09-21_seatB-15th history" >&2; exit 28; }
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
  || { echo "REFUSING: prompt does not name the all-ten trees, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
__NSGREP__ \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1136 is KS-1035 + KS-1036. … )" >&2; exit 32; }
__BYNAME_GREP__ \
  || { echo "REFUSING: the prompt does not carry Wednesday thirteen by-name items (tier/round; the trees and the zero overlap; canonical identity; the comment-only proof; the docs-only proof; the stale-claim findings; the VM provenance; branch names; Linear hygiene; the census rule; the intermittents; the addendum; the seat slips + F8 + the line-number discipline) or the standard closing" >&2; exit 33; }

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
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, TEN verdict lines"
  echo "  prompt names the report directory, the #1130-#1135 PRIOR REPORT, the #1119-#1128 EARLIER REPORT, the #1112-#1118 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (PR 7 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b15-*) and the seat 2026-09-21_seatB-15th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (__NBOTH__ tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the all-ten trees, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each PR is"
  echo "  prompt carries Wednesday thirteen by-name items and the standard closing (__NBYNAME__ keywords)"
  [ -n "${QAB1136_CUR_DEV:-}" ] && echo "  (develop read from the QAB1136_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1136_BRIEF:-}${QAB1136_PROMPT:-}${QAB1136_HEAD___LAST__:-}${QAB1136_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
__ENTERQA__ || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
s = L
SUBS = {'__HEADERLINES__': HEADER_LINES, '__BRIEF__': BRIEF, '__PROMPT__': PROMPT, '__PRS__': PRS_BLOCK, '__DEV__': DEV, '__DEVTREE__': DEV_TREE[:12], '__DEVSHORT__': DEV[:9], '__ALLDEV__': ALL_OVER_DEV, '__BEHIND__': str(BEHIND), '__NUNCH__': str(len(UNCHANGED)),
        '__REPORT__': REPORT, '__PRIOR__': PRIOR, '__EARLIER__': EARLIER, '__OLDER__': OLDER_R, '__WANTCOMPARE__': WANT_COMPARE, '__JUDGED__': JUDGED_BLOCK,
        '__TIERGREP__': TIER_GREP, '__NSGREP__': NS_GREP, '__BOTHLOOP__': BOTH_LOOP, '__BYNAME_GREP__': BYNAME_GREP, '__NBOTH__': str(len(BOTH)), '__NBYNAME__': str(sum(len(k) for _, k in BYNAME)),
        '__TIERLIST__': TIER_LIST, '__SUBJECT__': SUBJECT, '__LAST__': LAST, '__SUFFIX__': LAST if not PARTIAL else LAST + '-PARTIAL', '__ENTERQA__': 'c' + 'd' + ' "$QA_DIR"'}
for k, v in SUBS.items():
    if s.count(k) == 0: print('REFUSING: token absent', k); sys.exit(1)
    s = s.replace(k, v)
if re.search(r'__[A-Z0-9]+__', s): print('REFUSING: residual token', re.findall(r'__[A-Z0-9]+__', s)); sys.exit(2)
# 4. output controls
want = {DEV: 2, ALL_OVER_DEV: 2, ALL_OVER_PARENT: 3, PARENT: 2, 'behind=%d' % BEHIND: len(PRS), BRIEF: 2, PROMPT: 1, REPORT: 1, PRIOR: 1, EARLIER: 1, OLDER_R: 1,
        'exit 6': 2, 'exit 10': 5, 'exit 19': 3, 'exit 18': 5, 'exit 30': 4, 'exit 32': 2, 'exit 33': 2, 'exit 34': 2, 'exit 16': 3, 'exit 21': 3, '[ -t 0 ]': 1,
        'exec claude --dangerously-skip-permissions': 1, 'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': len(BLOBS) + len(UNCHANGED), ' own"': len(CHANGED), 'PENDING-PR-': 3,   # one label per landed FILE (PR 7 carries two)
        'QAB1136_CUR_DEV': 5, 'QAB1136_HEAD_' + LAST: 3, 'refs/pull/$_n/head': 2,
        SUBJECT: 1, 'PR #1136 is KS-1035 + KS-1036.': 3}
for n, tk, tags, br, h, *_ in PRS: want[h] = 1
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
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'), '| PARTIAL' if PARTIAL else '| COMPLETE')
