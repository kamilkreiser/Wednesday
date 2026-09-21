#!/usr/bin/env python3
"""shape_gate15.py — READ-ONLY local object reads in the Secuura checkout for the Seat B 15th ten-PR (docs + test-file comments) batch gate:
per captured READY (mail_seatB15_ready*_pr<N>_*.md): the PR number / head / branch vs the READY text, parent == develop 581ed7fa1, behind/ahead
0/1, head tree == the GROUPING table's per-PR tree, diff --raw blobs / modes / numstat == the GROUPING (develop-side blob and head blob), the
changed path set == the GROUPING file(s), DOCS-ONLY / TEST-FILE-ONLY by path, and the COMMENT-ONLY proof on the test-file PRs (`git diff -U0`
develop..head: every changed line begins `//`, `*`, `/*`, `*/` or `#` after the sign; a planted `const x = 1;` control flagged). Static reads
at develop: the 11 target blobs / line counts, the 14 canonical patches (existence, sha256[:16], hunk headers, `+`/`-` counts, `+++` path),
the fences re-extracted from the 14 READY files vs the run patches, the seat's stale-claim findings measured (F4 the CLAUDE.md `-` line at :303
and the `step 6` count; F5 the proxy.ts shape count; F2 is a GitHub read — gh_pr_reads_gate15.py), the hook's path filter (.githooks/pre-push
:4 / :76 / :254). Never a write verb here (apply / merge-tree live in predict_batch_scratch_gate15.py's --shared clone). Writes fences into the
drafter's scratchpad only (argv[1]); stdout otherwise. Re-runnable. Derived from gatesets/2026-09-21_gate1130to1135/shape_1130.py."""
import glob, hashlib, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); S = sys.argv[1]
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
DEV = '581ed7fa124b85c7c2da89ac05d52f99c2502911'; DEV_TREE = '60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b'; ALL = 'a93fe063d28ae66d4a90e1926b78364a7a578ff4'
D = 'Blockchain/Dev/'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def out(*a):
    rc, o, e = git(*a)
    if rc: print('  (git', a[:2], 'rc', rc, e.strip()[:120], ')')
    return o
print('shape_gate15', now())
# seat PR -> (keys, item tags, files, per-PR tree12, {path: (develop blob12, head blob12, lines after)}, adds, dels, lane)
SEAT = {
 '1': (['KS-1035', 'KS-1036'], 'D + item3', [D + 'docs/DEV-PROCESS.md'], '4cd290a2c80e', {D + 'docs/DEV-PROCESS.md': ('c9cd41d588a2', 'ab9a70f13e3c', 278)}, 12, 0, 'docs'),
 '2': (['KS-1037', 'KS-1049'], 'R15 + A', [D + 'CONTRIBUTING.md'], '0edbb8341e60', {D + 'CONTRIBUTING.md': ('953067eb7aa7', 'b3cc10a40089', 690)}, 10, 0, 'docs'),
 '3': (['KS-1045'], 'A + B', [D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md'], 'd1ba6f8882fd', {D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md': ('bbd5bbf78778', '5ba84caf2e30', 174)}, 3, 3, 'docs'),
 '4': (['KS-1097'], 'Da', ['CLAUDE.md'], '4f0a8c67f95f', {'CLAUDE.md': ('dd782eab7435', 'ef2f8fc2e4cb', 494)}, 1, 1, 'docs'),
 '5': (['KS-890'], 'R15', [D + 'deployment/DEPLOYMENT-ARCHITECTURE.md'], '374c0328a8c5', {D + 'deployment/DEPLOYMENT-ARCHITECTURE.md': ('daabe1087bb9', '622c0e505278', 194)}, 8, 0, 'docs'),
 '6': (['KS-1140'], 'GF2GF4', [D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts'], '99a9adaf3151', {D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts': ('7f0ac617f675', '9ce9e852ae44', 284)}, 2, 2, 'shared'),
 '7': (['KS-1152'], 'R1c + R1d', [D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts', D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts'], '6e95645e29fb',
       {D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts': ('ab8e46d795d2', '6a51358e3619', 459), D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts': ('eb7782db8816', '57de2c6753e4', 293)}, 5, 3, 'shared+originate'),
 '8': (['KS-979'], 'R15', [D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts'], '366ec698c266', {D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts': ('9bb899a10677', 'bed97468d499', 204)}, 6, 2, 'originate'),
 '9': (['KS-1120'], 'F3', [D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts'], '07d01c8ae4f5', {D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts': ('eb0e5305c815', 'b7949520cf03', 257)}, 5, 3, 'vc-issuer'),
 '10': (['KS-1156'], 'A3', [D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts'], '9fdeab78e610', {D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts': ('548e1ec1217e', '595bed15d859', 125)}, 1, 1, 'api-gateway'),
}
PUSH = [str(i) for i in range(1, 11)]
# the 14 canonicals: (READY file under night/, canonical = 'run:<run dir>' or 'fence', sha16, apply mode, seat PR)
CANON = [
 ('READY_KS-1035-D_ornith35b-q4_DOCPATCH-REANCHORED-PASS-6of6_2026-09-15.diff.md', 'run:2026-09-15_ks1035-ornith35b-night', '849507a10f99b9ab', 'strict', '1'),
 ('READY_KS-1036-item3_ornith35b-q4_DOCPATCH-REBRIEF-PASS-8of8_2026-09-16.diff.md', 'run:2026-09-16_ks1036-ornith35b-night2', '8a49e7c68318cb58', 'strict', '1'),
 ('READY_KS-1037_ornith35b-q4_DOCPATCH-PASS-6of6_2026-09-15.diff.md', 'fence', 'b9ed6eb6bac788a7', '--recount', '2'),
 ('READY_KS-1049-A_ornith35b-q4_DOCPATCH-PLACED-BY-WEDNESDAY-D8-PASS_2026-09-16.diff.md', 'run:2026-09-16_ks1049-ornith35b-night2', 'd5a07523e6a450f7', 'strict', '2'),
 ('READY_KS-1045-A_ornith35b-q4_DOCPATCH-RECHECK-PASS-7of7_2026-09-15.diff.md', 'fence', '2497bea61ff7789f', '--recount', '3'),
 ('READY_KS-1045-B_ornith35b-q4_DOCPATCH-PASS-7of7_2026-09-15.diff.md', 'fence', '66aa75dfcf5ea1f3', '--recount', '3'),
 ('READY_KS-1097-Da_ornith35b-q4_DOCPATCH-STRICT-PASS-7of7_2026-09-15.diff.md', 'fence', 'd41e4136c612bac5', 'strict', '4'),
 ('READY_KS-890_ornith35b-q4_DOCPATCH-ANCHORRESTORED-PASS-8of8_2026-09-16.diff.md', 'fence', '3b8d82cf560c2605', 'strict', '5'),
 ('READY_KS-1140-GF2GF4_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md', 'run:2026-09-17_ks1140-ornith35b-night', '42486061ffa4448e', 'strict', '6'),
 ('READY_KS-1152-R1c_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md', 'run:2026-09-17_ks1152-ornith35b-night3', '31ae771c8a5f8fe5', 'strict', '7'),
 ('READY_KS-1152-R1d_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md', 'run:2026-09-17_ks1152-ornith35b-night4', '7ddcf0309e15ba55', 'strict', '7'),
 ('READY_KS-979_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md', 'run:2026-09-17_ks979-ornith35b-night', '1c0121de5b00ce95', 'strict', '8'),
 ('READY_KS-1120-F3_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md', 'run:2026-09-17_ks1120-ornith35b-night', 'ee3c484b2aff8ff0', 'strict', '9'),
 ('READY_KS-1156-A3_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md', 'run:2026-09-17_ks1156-ornith35b-night3', '8d60c7b67227561c', 'strict', '10'),
]
FD = os.path.join(S, 'fences15'); os.makedirs(FD, exist_ok=True)
print('--- the 14 canonicals (existence, sha256[:16] vs the GROUPING, fence vs run patch)')
CANON_TXT = {}
for rf, src, sha16, mode, p in CANON:
    rp = os.path.join(LM, 'night', rf); t = open(rp, encoding='utf-8').read() if os.path.exists(rp) else None
    fence = None
    if t is not None:
        m = re.search(r'^```diff\n(.*?)^```', t, re.S | re.M)
        if m: fence = m.group(1)
    fpath = os.path.join(FD, rf.replace('.md', '.fence.diff'))
    if fence is not None: open(fpath, 'w', encoding='utf-8').write(fence)
    run_txt = None; run_path = None
    if src.startswith('run:'):
        run_path = os.path.join(LM, 'runs', src[4:], 'out.md.checker', 'patch.diff')
        run_txt = open(run_path, encoding='utf-8').read() if os.path.exists(run_path) else None
    canon = run_txt if src.startswith('run:') else fence
    CANON_TXT[rf] = (canon, mode, p, run_path if src.startswith('run:') else fpath)
    c16 = hashlib.sha256(canon.encode()).hexdigest()[:16] if canon is not None else None
    f16 = hashlib.sha256(fence.encode()).hexdigest()[:16] if fence is not None else None
    hunks = re.findall(r'^@@[^\n]*', canon or '', re.M); plus = sum(1 for l in (canon or '').splitlines() if l.startswith('+') and not l.startswith('+++')); minus = sum(1 for l in (canon or '').splitlines() if l.startswith('-') and not l.startswith('---'))
    ppp = re.findall(r'^\+\+\+ b/(.*)$', canon or '', re.M)
    print('  PR %-2s %-78s READY exists %s | canonical %s | sha16 %s == GROUPING %s: %s | fence sha16 %s fence==canonical %s | hunks %s | +%d/-%d | +++ %s | mode %s' % (
        p, rf[:78], t is not None, 'RUN ' + src[4:] if src.startswith('run:') else 'FENCE', c16, sha16, c16 == sha16, f16, fence == canon, hunks, plus, minus, ppp, mode))
print('fences written (byte-exact, the text between the ```diff and ``` lines) to', FD)
print('--- the 11 target paths at develop', DEV[:9], '(blob, lines) vs the GROUPING')
for p in PUSH:
    for path, (b1, b2, lines_after) in SEAT[p][4].items():
        bd = out('rev-parse', DEV + ':' + path).strip(); ln = out('show', DEV + ':' + path).count('\n')
        print('  PR %-2s %-100s develop blob %s == %s: %s | lines %d' % (p, path, bd[:12], b1, bd.startswith(b1), ln))
print('--- READYs captured')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB15_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read()
    m = re.search(r'READY FOR QA \(Seat B 15th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', t)
    br = re.search(r'\bbranch\s*\n?(feature/[^\s,]+)', t)
    tr = re.search(r'Head tree ([0-9a-f]{40})', t)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), branch=br.group(1) if br else '?', tree=tr.group(1) if tr else '?', file=os.path.basename(f))
present = [p for p in PUSH if p in READY]
print('present seat PRs:', present, '| PR numbers', [READY[p]['n'] for p in present])
CHANGED = {}
for p in present:
    r = READY[p]; h = r['h']; keys, tags, files, tree12, blobs, adds, dels, lane = SEAT[p]
    if git('cat-file', '-e', h + '^{commit}')[0]: print('#%s PR %s head %s NOT in the local object store (the seat pushes from its worktree; the checkout may not hold it yet)' % (r['n'], p, h[:9])); continue
    par = out('rev-list', '--parents', '-n1', h).split()[1:]
    lr = out('rev-list', '--left-right', '--count', DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip()
    subj = out('log', '-1', '--format=%s', h).strip()
    raw = out('diff', '--raw', '--abbrev=40', DEV, h).strip().splitlines()
    ns = {l.split('\t')[2]: (int(l.split('\t')[0]), int(l.split('\t')[1])) for l in out('diff', '--numstat', DEV, h).strip().splitlines()}
    fl = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); fl[path] = (b1, b2, st, m2)
    a_sum = sum(v[0] for v in ns.values()); d_sum = sum(v[1] for v in ns.values())
    print('#%s PR %s %s head %s | parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == GROUPING %s: %s | READY tree %s == %s | branch (READY) %s' % (
        r['n'], p, '+'.join(keys), h[:9], par == [DEV], lr, t[:12], tree12, t.startswith(tree12), r['tree'][:12], r['tree'] == t, r['branch']))
    print('   subject (%d chars, ascii %s): %s | keys in subject %s' % (len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj)))
    print('   files %s == GROUPING %s: %s | +%d/-%d (want +%d/-%d) %s | name-status %s | modes %s' % (sorted(fl), sorted(files), sorted(fl) == sorted(files), a_sum, d_sum, adds, dels, (a_sum, d_sum) == (adds, dels), sorted(v[2] for v in fl.values()), sorted({v[3] for v in fl.values()})))
    for path, (b1, b2, st, m2) in fl.items():
        want = blobs.get(path); lines_h = out('show', h + ':' + path).count('\n')
        print('   %-100s develop %s -> head %s (%s) | GROUPING (%s -> %s / %s lines): %s | lines at head %d' % (path, b1[:12], b2[:12], m2, want[0] if want else '?', want[1] if want else '?', want[2] if want else '?', bool(want) and b1.startswith(want[0]) and b2.startswith(want[1]) and lines_h == want[2], lines_h))
        CHANGED[path] = (b1, b2, st, m2, r['n'], p)
    docs_only = all(x.endswith('.md') for x in fl); tests_only = all('/__tests__/' in x for x in fl)
    print('   DOCS-ONLY (every path .md): %s | TEST-FILE-ONLY (every path under __tests__/): %s | lane %s' % (docs_only, tests_only, lane))
    if lane != 'docs':
        d0 = out('diff', '-U0', DEV, h)
        changed = [l for l in d0.splitlines() if (l.startswith('+') or l.startswith('-')) and not l.startswith('+++') and not l.startswith('---')]
        def is_comment(l):
            s = l[1:].strip(); return s == '' or s.startswith('//') or s.startswith('*') or s.startswith('/*') or s.startswith('*/') or s.startswith('#')
        non = [l for l in changed if not is_comment(l)]
        ctrl = [l for l in changed + ['+const x = 1;'] if not is_comment(l)]
        print('   COMMENT-ONLY proof (diff -U0): changed lines %d | non-comment %d %s | control (+const x = 1; planted) flagged %d (want 1)' % (len(changed), len(non), non[:3] if non else '', len(ctrl)))
print('--- disjointness over the captured heads')
import itertools
owners = {}
for path, v in CHANGED.items(): owners.setdefault(path, []).append(v[4])
print('union paths', len(CHANGED), '| any path in two PRs:', {k: v for k, v in owners.items() if len(v) > 1} or 'NONE', '| every path M:', all(v[2] == 'M' for v in CHANGED.values()))
print('--- static reads at develop for the seat findings (F4, F5) and the hook')
cl = out('show', DEV + ':CLAUDE.md').splitlines()
mn = [i + 1 for i, l in enumerate(cl) if l.startswith('**The gate is approval + a Test Evidence block filled from LOCAL runs**')]
print('F4a CLAUDE.md: the `-` line "**The gate is approval + a Test Evidence block…" at develop line(s)', mn, '(count %d; the fence header says @@ -292,4)' % len(mn))
mf = [i + 1 for i, l in enumerate(cl) if l.strip().lower().startswith('## merge flow') or l.strip().lower().startswith('### merge flow') or re.match(r'^#+\s*merge flow', l, re.I)]
print('F4b CLAUDE.md: "Merge flow" heading line(s)', mf, '| `step 6` count in the whole file %d | `We approve our own work` count %d' % (sum(l.count('step 6') for l in cl), sum(l.count('We approve our own work') for l in cl)))
px = out('show', DEV + ':' + D + 'services/api-gateway/src/routes/proxy.ts')
three = len(re.findall(r'authenticateToken\((true|false)\),\s*attachScopes,\s*requireScope\(', px))
print('F5 proxy.ts at develop: three-part shape `authenticateToken(true|false), attachScopes, requireScope(` count %d (seat: 6) | attachScopes tokens %d (seat: 8) | requireScope( tokens %d (seat: 6) | lines %d' % (three, px.count('attachScopes'), px.count('requireScope('), px.count('\n')))
ag = out('show', DEV + ':' + D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts').splitlines()
print('   the ks835 test at develop :57-:58:', [l for l in ag[56:58]])
hk = out('show', DEV + ':.githooks/pre-push').splitlines()
for i in (4, 76, 254):
    print('   .githooks/pre-push :%d: %s' % (i, hk[i - 1] if i <= len(hk) else '?'))
print('   hook lines %d | grep "^Blockchain/Dev/" count %d | "docs-only" mentions %d' % (len(hk), sum(1 for l in hk if "grep '^Blockchain/Dev/'" in l), sum(1 for l in hk if 'docs-only' in l.lower() or 'docs only' in l.lower())))
dp = out('show', DEV + ':' + D + 'docs/DEV-PROCESS.md').splitlines()
print('   DEV-PROCESS.md at develop lines %d; :188 %r | :225 %r' % (len(dp), dp[187][:80], dp[224][:80]))
ct = out('show', DEV + ':' + D + 'CONTRIBUTING.md').splitlines()
print('   CONTRIBUTING.md at develop lines %d; :105 %r | :577 %r' % (len(ct), ct[104][:80], ct[576][:80]))
print('   ALL-14 tree per the seat/drafter: %s (re-derived by predict_batch_scratch_gate15.py once heads land); develop tree %s == %s' % (ALL, out('rev-parse', DEV + '^{tree}').strip()[:12], DEV_TREE[:12]))
print('done', now())
