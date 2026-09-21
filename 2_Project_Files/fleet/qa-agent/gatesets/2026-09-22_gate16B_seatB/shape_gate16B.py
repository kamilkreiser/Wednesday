#!/usr/bin/env python3
"""shape_gate16B.py — READ-ONLY local object reads in the Secuura checkout for the Seat B 16th eight-PR (test-only) batch gate. Per captured
READY (mail_seatB16_ready*_pr<N>_*.md): PR number / head / branch vs the READY text; parent == develop 64ab10513; behind/ahead 0/1; head tree ==
the READY's; diff --raw blobs / modes / numstat vs round16B (the RECOUNT blob, the line count); the changed path set == the ONE test file, under
__tests__/ (TEST-FILE-ONLY); `-` line count; the file's line count at the head. Static reads at develop: the 12 canonical run patches (existence,
sha256[:16], hunk headers, `+`/`-` counts, `+++` path, the declared-vs-actual new count = the TRUNCATION class), the 8 targets at develop (7 ABSENT,
the KS-1229 file at 8082826898c2 / 226), the 9 tamper files' blobs (the seat's item 0), the KS-1004 lockout cell title (the #1153 develop cover),
anchoring's threadTokenMint test (the ONE known develop red), the `ks-727` token in the KS-1181 FILE NAME, rateLimitScope.ts's principalScope
(the security surface), the 8 branch names' ASCII-ness, and the seat's branch tails. Never a write verb here (apply / merge-tree live in
predict_batch_scratch_gate16B.py's --shared clone). Writes nothing (stdout). Re-runnable. Derived from gatesets/2026-09-21_gate15_docs_comments/shape_gate15.py."""
import glob, hashlib, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16B as R
REPO = R.REPO
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def out(*a):
    rc, o, e = git(*a)
    if rc: print('  (git', a[:2], 'rc', rc, e.strip()[:120], ')')
    return o
print('shape_gate16B', now())
print('--- develop', R.DEV[:9], 'tree', out('rev-parse', R.DEV + '^{tree}').strip()[:12], '== round16B', R.DEV_TREE[:12], out('rev-parse', R.DEV + '^{tree}').strip() == R.DEV_TREE,
      '| rev-list --count', R.PARENT15[:9] + '..' + R.DEV[:9], '=', out('rev-list', '--count', R.PARENT15 + '..' + R.DEV).strip(), '(seat: 13)')
print('--- the 12 canonicals (existence, sha256[:16] vs the GROUPING, hunk headers, +/- counts, the declared-vs-actual new count)')
for p in R.PUSH:
    for label, rd, sha16, mode, adds, dels, hunk, sblob, slines, tip in R.PRS[p]['canon']:
        path = R.run_patch(rd); ex = os.path.exists(path); t = open(path, encoding='utf-8').read() if ex else ''
        c16 = hashlib.sha256(t.encode()).hexdigest()[:16] if ex else None
        hunks = re.findall(r'^@@[^\n]*', t, re.M); plus = sum(1 for l in t.splitlines() if l.startswith('+') and not l.startswith('+++')); minus = sum(1 for l in t.splitlines() if l.startswith('-') and not l.startswith('---'))
        ppp = re.findall(r'^\+\+\+ b/(.*)$', t, re.M)
        m = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', hunks[0]) if hunks else None
        declared_new = int(m.group(4)) if m else None
        print('  PR %-2s %-12s run %-36s exists %s | sha16 %s == %s: %s | hunks %s == %s: %s | +%d/-%d (want +%d/-%d) %s | +++ %s == target: %s | declared new=%s vs actual + %d -> %s | mode %s' % (
            p, label, rd, ex, c16, sha16, c16 == sha16, hunks, [hunk], hunks == [hunk], plus, minus, adds, dels, (plus, minus) == (adds, dels), ppp, ppp == [R.PRS[p]['file']], declared_new, plus,
            'TRUNCATION (strict apply writes %s)' % declared_new if (R.PRS[p]['mode'] == 'new' and declared_new is not None and declared_new < plus) else ('MISCOUNT-OVER (strict rc 128)' if (R.PRS[p]['mode'] == 'new' and declared_new is not None and declared_new > plus) else 'header consistent'), mode))
        fence_f = glob.glob(os.path.join(R.LM, 'night', 'READY_%s-%s-R15_*.diff.md' % (R.PRS[p]['key'], label if label != 'UNTYPEDSRCb' else 'UNTYPEDSRCb')))
        if fence_f:
            ft = open(fence_f[0], encoding='utf-8').read(); mm = re.search(r'^```diff\n(.*?)^```', ft, re.S | re.M)
            f16 = hashlib.sha256(mm.group(1).encode()).hexdigest()[:16] if mm else None
            print('      READY file %s | fence sha16 %s == run patch: %s' % (os.path.basename(fence_f[0])[:80], f16, f16 == c16))
        else: print('      READY file for %s-%s NOT FOUND under night/' % (R.PRS[p]['key'], label))
print('--- the 8 targets at develop', R.DEV[:9])
for p in R.PUSH:
    pr = R.PRS[p]; rc, o, e = git('cat-file', '-e', R.DEV + ':' + pr['file'])
    if rc: print('  PR %-2s %-95s ABSENT at develop (want %s): %s' % (p, pr['file'], 'ABSENT' if pr['mode'] == 'new' else pr['dev_blob'], pr['mode'] == 'new'))
    else:
        b = out('rev-parse', R.DEV + ':' + pr['file']).strip(); ln = out('show', R.DEV + ':' + pr['file']).count('\n')
        print('  PR %-2s %-95s develop blob %s == %s: %s | lines %d (want %s)' % (p, pr['file'], b[:12], pr['dev_blob'], b.startswith(pr['dev_blob'] or 'x'), ln, pr['dev_lines']))
print('--- the 9 tamper files at develop (the seat item-0 blobs) and at the 15th parent')
for path, b12 in R.TAMPER_BLOBS:
    b = out('rev-parse', R.DEV + ':' + path).strip(); b15 = out('rev-parse', R.PARENT15 + ':' + path).strip()
    print('  %-80s %s == %s: %s | identical at 581ed7fa1: %s' % (path.replace(R.D, ''), b[:12], b12, b.startswith(b12), b == b15))
print('--- READYs captured')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read(); m = re.search(R.ready_regex(), t)
    br = re.search(r'\bbranch\s*\n?(feature/[^\s,]+)', t); tr = re.search(r'Head tree ([0-9a-f]{40})', t)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), branch=br.group(1) if br else '?', tree=tr.group(1) if tr else '?', file=os.path.basename(f))
present = [p for p in R.PUSH if p in READY]
print('present seat PRs:', present, '| PR numbers', [READY[p]['n'] for p in present], '| missing', [p for p in R.PUSH if p not in READY] or 'none')
CHANGED = {}
for p in present:
    r = READY[p]; pr = R.PRS[p]; h = r['h']
    print('#%s PR %s %s READY head %s == round16B %s: %s | READY PR number %s == %s: %s | READY branch == round16B: %s | READY tree == round16B: %s' % (
        r['n'], p, pr['key'], h[:9], pr['head'][:9], h == pr['head'], r['n'], pr['n'], r['n'] == pr['n'], r['branch'] == pr['branch'].replace('refs/heads/', ''), r['tree'] == pr['tree']))
    if git('cat-file', '-e', h + '^{commit}')[0]: print('   head NOT in the local object store'); continue
    par = out('rev-list', '--parents', '-n1', h).split()[1:]; lr = out('rev-list', '--left-right', '--count', R.DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip(); subj = out('log', '-1', '--format=%s', h).strip(); author = out('log', '-1', '--format=%ae', h).strip()
    raw = out('diff', '--raw', '--abbrev=40', R.DEV, h).strip().splitlines(); ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', R.DEV, h).strip().splitlines()}
    fl = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); fl[path] = (b1, b2, st, m2)
    a_sum = sum(int(v[0]) for v in ns.values()); d_sum = sum(int(v[1]) for v in ns.values())
    print('   parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == %s: %s | subject (%d chars, ascii %s): %s | keys in subject %s | author %s' % (
        par == [R.DEV], lr, t[:12], pr['tree'][:12], t == pr['tree'], len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj), author))
    print('   files %s == [%s]: %s | +%d/-%d (want +%d/-%d) %s | name-status %s | modes %s | every path under __tests__/: %s' % (
        sorted(fl), pr['file'], sorted(fl) == [pr['file']], a_sum, d_sum, pr['adds'], pr['dels'], (a_sum, d_sum) == (pr['adds'], pr['dels']), sorted(v[2] for v in fl.values()), sorted({v[3] for v in fl.values()}), all('/__tests__/' in x for x in fl)))
    for path, (b1, b2, st, m2) in fl.items():
        lines_h = out('show', h + ':' + path).count('\n')
        print('   %-95s develop %s -> head %s (%s, %s) | RECOUNT blob %s: %s | lines at head %d (want %d): %s' % (path, b1[:12], b2[:12], st, m2, pr['blob'][:12], b2 == pr['blob'], lines_h, pr['lines'], lines_h == pr['lines']))
        CHANGED[path] = (b1, b2, st, m2, r['n'], p)
    d0 = out('diff', '-U0', R.DEV, h); minus_lines = [l for l in d0.splitlines() if l.startswith('-') and not l.startswith('---')]
    print('   `-` lines %d (READY declares %d): %s | %s' % (len(minus_lines), pr['dels'], len(minus_lines) == pr['dels'], minus_lines[:1]))
    if pr['mode'] == 'new':
        hb = out('show', h + ':' + pr['file']); hl = hb.count('\n')
        for label, rd, sha16, mode, adds, dels, hunk, sblob, slines, tip in pr['canon']:
            if sblob: print('   TRUNCATION row: the seat\'s STRICT blob %s / %d lines vs the head blob %s / %d lines (the head must be the RECOUNT one): head != strict %s' % (sblob, slines, hb and out('rev-parse', h + ':' + pr['file']).strip()[:12], hl, not out('rev-parse', h + ':' + pr['file']).strip().startswith(sblob)))
print('--- disjointness over the captured heads')
owners = {}
for path, v in CHANGED.items(): owners.setdefault(path, []).append(v[4])
print('union paths', len(CHANGED), '(want 8) | any path in two PRs:', {k: v for k, v in owners.items() if len(v) > 1} or 'NONE', '| name-status', sorted(v[2] for v in CHANGED.values()), '(want 7 A + 1 M)')
print('∩ Seat C 16th dirs:', [x for x in CHANGED if any(x.startswith(d) for d in R.SEATC_DIRS)] or 'NONE', '| ∩ Seat C pushed paths:', sorted(set(CHANGED) & {x[3] for x in R.SEATC}) or 'NONE')
print('--- static reads at develop for the seat findings')
ks1004 = out('show', R.DEV + ':' + R.OR + 'src/__tests__/ks1004-anchor-failed-lockout.test.ts')
print('#1153 cover: ks1004-anchor-failed-lockout.test.ts exists at develop: %s | "CARRIED FORWARD" count %d | "markDocumentAnchorFailed reaches a hashed document" count %d' % (bool(ks1004), ks1004.count('CARRIED FORWARD'), ks1004.count('markDocumentAnchorFailed reaches a hashed document')))
ass = out('show', R.DEV + ':' + R.OR + 'src/services/anchorStateSync.ts').splitlines()
print('   anchorStateSync.ts lines %d; :155 %r | :166 %r' % (len(ass), ass[154][:70] if len(ass) > 154 else '?', ass[165][:70] if len(ass) > 165 else '?'))
ttm = out('ls-tree', '-r', '--name-only', R.DEV, R.AN + 'src/__tests__/').splitlines()
print('anchoring __tests__ files at develop: %d | threadTokenMint: %s' % (len(ttm), [x.split('/')[-1] for x in ttm if 'threadTokenMint' in x]))
print('KS-1181 FILE NAME carries `ks-727`: %s (the ARCHIVED key with a hyphen — Q6(b): a path token is a path) | its tamper file ks727-errorhandler-class-guard.test.ts is a TEST file (a tamper on a test file, not a product file): %s' % ('ks-727' in R.PRS['7']['file'], '__tests__' in R.PRS['7']['tampers'][0][1]))
rls = out('show', R.DEV + ':' + R.SE + 'src/rateLimitScope.ts').splitlines()
print('security surface rateLimitScope.ts at develop: lines %d | :112 %r | :118 %r | `export function principalScope(` count %d' % (len(rls), rls[111][:70] if len(rls) > 111 else '?', rls[117][:70] if len(rls) > 117 else '?', sum(1 for l in rls if 'export function principalScope(' in l)))
ac = out('show', R.DEV + ':' + R.OR + 'src/routes/adminConfig.ts').splitlines()
print('adminConfig.ts lines %d | :1892 %r | :1897 %r' % (len(ac), ac[1891][:70] if len(ac) > 1891 else '?', ac[1896][:70] if len(ac) > 1896 else '?'))
dc = out('show', R.DEV + ':' + R.OR + 'src/routes/documents.ts').splitlines()
print('documents.ts lines %d | :1993 %r | :2609 %r | :2878 %r' % (len(dc), dc[1992][:60] if len(dc) > 1992 else '?', dc[2608][:60] if len(dc) > 2608 else '?', dc[2877][:60] if len(dc) > 2877 else '?'))
ssrf = out('show', R.DEV + ':' + R.SH + 'src/security/ssrf-guard.ts').splitlines()
print('ssrf-guard.ts lines %d | :477 %r | :478 %r' % (len(ssrf), ssrf[476][:70] if len(ssrf) > 476 else '?', ssrf[477][:70] if len(ssrf) > 477 else '?'))
k727 = out('show', R.DEV + ':' + R.SH + 'src/__tests__/ks727-errorhandler-class-guard.test.ts').splitlines()
print('ks727-errorhandler-class-guard.test.ts lines %d | :32 %r' % (len(k727), k727[31][:80] if len(k727) > 31 else '?'))
for p in R.PUSH:
    br = R.PRS[p]['branch'].replace('refs/heads/', ''); print('branch PR %s %s ascii %s len %d | own key once: %s | archived key form in branch: %s' % (p, br[:60], br.isascii(), len(br), br.count(R.PRS[p]['key'].lower()) == 1, [k for k in R.ARCHIVED if k.lower() + '-' in br or k.lower() == br]))
for lane, pj in (('originate', R.OR + 'package.json'), ('shared', R.SH + 'package.json'), ('security', R.SE + 'package.json'), ('anchoring', R.AN + 'package.json')):
    pjt = out('show', R.DEV + ':' + pj); m = re.search(r'"test"\s*:\s*"([^"]*)"', pjt); print('lane %-10s scripts.test = %r' % (lane, m.group(1) if m else '?'))
print('hook .githooks/pre-push :76 %r' % out('show', R.DEV + ':.githooks/pre-push').splitlines()[75][:80])
print('done', now())
