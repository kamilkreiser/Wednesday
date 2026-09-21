#!/usr/bin/env python3
"""shape_gate16C.py — READ-ONLY local object reads in the Secuura checkout for the Seat C 16th twelve-PR (test-only) batch gate. Per captured READY
(mail_seatC16_ready*_pr<N>_*.md): PR number / head / branch / tree vs the READY text; parent == develop 64ab10513; behind/ahead 0/1; diff --raw blobs /
modes / numstat vs round16C (the RECOUNT blob, the line count) per FILE; every changed path under __tests__/ (TEST-FILE-ONLY); `-` line count; the
file's line count at the head. Static reads at develop: the 14 canonical run patches + KS-910's two section files (existence, sha256[:16], hunk headers,
`+`/`-` counts, `+++` path, the declared-vs-actual new count = the TRUNCATION class; KS-910's patch.diff sha16 beside its sections), the READY fences
vs the run patches, the 16 targets at develop (11 ABSENT, 5 at their blobs), the 8 tamper files' blobs (the seat's item 0) at 64ab10513 / 581ed7fa1 /
9f0265eb0, the KS-1188-F1A anchor-ambiguity `from` count in mfa.ts (3), the 12 branch names' ASCII-ness + the three excisions, the two lanes' test
scripts, the hook's :76. Never a write verb here (apply / merge-tree live in predict_batch_scratch_gate16C.py's --shared clone). Writes nothing
(stdout). Re-runnable. Derived from gatesets/2026-09-22_gate16B_seatB/shape_gate16B.py (itself from gate15's)."""
import glob, hashlib, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16C as R
REPO = R.REPO
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def out(*a):
    rc, o, e = git(*a)
    if rc: print('  (git', a[:2], 'rc', rc, e.strip()[:120], ')')
    return o
print('shape_gate16C', now())
print('--- develop', R.DEV[:9], 'tree', out('rev-parse', R.DEV + '^{tree}').strip()[:12], '== round16C', R.DEV_TREE[:12], out('rev-parse', R.DEV + '^{tree}').strip() == R.DEV_TREE,
      '| rev-list --count', R.PARENT15[:9] + '..' + R.DEV[:9], '=', out('rev-list', '--count', R.PARENT15 + '..' + R.DEV).strip(), '(seat: 13)', '| subject:', out('log', '-1', '--format=%s', R.DEV).strip())
print('--- the 16 canonicals (14 run patches + KS-910 two sections): existence, sha256[:16] vs the GROUPING, hunk headers, +/- counts, the declared-vs-actual new count')
nrows = 0
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        for label, rd, sha16, mode, adds, dels, hunk, sblob, slines, tip in f['canon']:
            nrows += 1
            path = R.canon_path((label, rd)); ex = os.path.exists(path); t = open(path, encoding='utf-8').read() if ex else ''
            c16 = hashlib.sha256(t.encode()).hexdigest()[:16] if ex else None
            hunks = re.findall(r'^@@[^\n]*', t, re.M); plus = sum(1 for l in t.splitlines() if l.startswith('+') and not l.startswith('+++')); minus = sum(1 for l in t.splitlines() if l.startswith('-') and not l.startswith('---'))
            ppp = re.findall(r'^\+\+\+ b/(.*)$', t, re.M)
            m = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', hunks[0]) if hunks else None
            declared_new = int(m.group(4)) if m else None
            first_hunk = hunks[0][:len(hunk)] if hunks else None
            cls = 'TRUNCATION (strict apply writes %s)' % declared_new if (f['mode'] == 'new' and declared_new is not None and declared_new < plus) else ('MISCOUNT (strict rc 128 expected)' if mode == 'rc128' else 'header consistent')
            print('  PR %-2s %-18s %-36s exists %s | sha16 %s == %s: %s | first hunk %r == %r: %s | hunks %d | +%d/-%d (want +%d/-%d) %s | +++ %s == target: %s | declared new=%s vs actual + %d -> %s | mode %s' % (
                p, label, rd, ex, c16, sha16, c16 == sha16, first_hunk, hunk, first_hunk == hunk, len(hunks), plus, minus, adds, dels, (plus, minus) == (adds, dels), [x.split('/')[-1] for x in ppp], ppp == [f['path']], declared_new, plus, cls, mode))
        # the READY fence for each run row (the fence == the run patch: the brief's BLUF 4, 15/15)
        for label, rd, *_ in f['canon']:
            if rd.startswith('section_'): continue
            key = R.PRS[p]['key']; tag = label if label != 'F1a' and label != 'F1b' else label
            fence_f = glob.glob(os.path.join(R.LM, 'night', 'READY_%s-%s-R15_*.diff.md' % (key, tag))) or glob.glob(os.path.join(R.LM, 'night', 'READY_%s-R15-R15_*.diff.md' % key)) or glob.glob(os.path.join(R.LM, 'night', 'READY_%s-R15_*.diff.md' % key))   # KS-1199's tag IS R15: READY_KS-1199-R15_… (KS-1156's is READY_KS-1156-R15-R15_…) — drafter S2
            fence_f = [x for x in fence_f if not x.endswith('.pre-0922-0254-hold') and '.pre-' not in x]
            if fence_f:
                ft = open(fence_f[0], encoding='utf-8').read(); mm = re.search(r'^```diff\n(.*?)^```', ft, re.S | re.M)
                f16 = hashlib.sha256(mm.group(1).encode()).hexdigest()[:16] if mm else None
                print('      READY file %s | fence sha16 %s == run patch %s: %s' % (os.path.basename(fence_f[0])[:90], f16, [c[2] for c in f['canon'] if c[0] == label][0], f16 == [c[2] for c in f['canon'] if c[0] == label][0]))
            else: print('      READY file for %s-%s NOT FOUND under night/' % (key, tag))
print('  canonical rows', nrows, '(want 16 = 14 run patches + 2 KS-910 sections)')
k910 = R.run_patch(R.KS910_RUN); k910t = open(k910, 'rb').read()
print('  KS-910 patch.diff sha16 %s == %s: %s | bytes %d (the READY header says 4093 — off by 4, the brief) | its fence:' % (hashlib.sha256(k910t).hexdigest()[:16], R.KS910_FENCE16, hashlib.sha256(k910t).hexdigest()[:16] == R.KS910_FENCE16, len(k910t)), end=' ')
ff = [x for x in glob.glob(os.path.join(R.LM, 'night', 'READY_KS-910-LEGCOMMENT-R15_*.diff.md')) if '.pre-' not in x]
if ff:
    ft = open(ff[0], encoding='utf-8').read(); mm = re.search(r'^```diff\n(.*?)^```', ft, re.S | re.M); f16 = hashlib.sha256(mm.group(1).encode()).hexdigest()[:16] if mm else None
    print('fence sha16', f16, '== patch.diff:', f16 == R.KS910_FENCE16, '| section_1.diff == section_1.diff.reanchored bytes:', open(R.ks910_section('section_1.diff'), 'rb').read() == open(R.ks910_section('section_1.diff.reanchored'), 'rb').read())
else: print('READY file NOT FOUND')
print('--- the 16 targets at develop', R.DEV[:9])
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        rc, o, e = git('cat-file', '-e', R.DEV + ':' + f['path'])
        if rc: print('  PR %-2s %-100s ABSENT at develop (want ABSENT): %s' % (p, f['path'].replace(R.D, ''), f['mode'] == 'new'))
        else:
            b = out('rev-parse', R.DEV + ':' + f['path']).strip(); ln = out('show', R.DEV + ':' + f['path']).count('\n')
            print('  PR %-2s %-100s develop blob %s == %s: %s | lines %d (want %s): %s' % (p, f['path'].replace(R.D, ''), b[:12], (f['dev_blob'] or '?')[:12], b == f['dev_blob'], ln, f['dev_lines'], ln == f['dev_lines']))
print('--- the 8 tamper files at develop (the seat item-0 blobs), at 581ed7fa1 and at 9f0265eb0')
for path, b40 in R.TAMPER_BLOBS:
    b = out('rev-parse', R.DEV + ':' + path).strip(); b15 = out('rev-parse', R.PARENT15 + ':' + path).strip(); b9 = out('rev-parse', R.TIP9F + ':' + path).strip()
    print('  %-60s %s == item0 %s | identical at 581ed7fa1: %s | at 9f0265eb0: %s' % (path.replace(R.D, ''), b[:12], b == b40, b == b15, b == b9))
mfa = out('show', R.DEV + ':' + R.AU + 'src/routes/mfa.ts').splitlines()
print('--- KS-1188-F1A anchor ambiguity: mfa.ts lines %d | :138 %r | :143 %r | :166 %r | :397 %r | count of the :143 line text in the file: %d (seat: 3)' % (
    len(mfa), mfa[137][:60] if len(mfa) > 137 else '?', mfa[142][:70] if len(mfa) > 142 else '?', mfa[165][:70] if len(mfa) > 165 else '?', mfa[396][:70] if len(mfa) > 396 else '?', sum(1 for l in mfa if l == mfa[142]) if len(mfa) > 142 else -1))
print('--- READYs captured')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read(); m = re.search(R.ready_regex(), t)
    br = re.search(r'\bbranch\s*\n?(feature/[^\s,]+)', t); tr = re.search(r'Head tree ([0-9a-f]{40})', t)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), branch=br.group(1) if br else '?', tree=tr.group(1) if tr else '?', file=os.path.basename(f))
present = [p for p in R.PUSH if p in READY]
print('present seat PRs:', present, '| PR numbers', [READY[p]['n'] for p in present], '| missing', [p for p in R.PUSH if p not in READY] or 'none')
CHANGED = {}
for p in present:
    r = READY[p]; pr = R.PRS[p]; h = r['h']
    print('#%s PR %s %s READY head %s == round16C %s: %s | READY PR number %s == %s: %s | READY branch == round16C: %s | READY tree == round16C: %s' % (
        r['n'], p, pr['key'], h[:9], pr['head'][:9], h == pr['head'], r['n'], pr['n'], r['n'] == pr['n'], r['branch'] == pr['branch'].replace('refs/heads/', ''), r['tree'] == pr['tree']))
    if git('cat-file', '-e', h + '^{commit}')[0]: print('   head NOT in the local object store'); continue
    par = out('rev-list', '--parents', '-n1', h).split()[1:]; lr = out('rev-list', '--left-right', '--count', R.DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip(); subj = out('log', '-1', '--format=%s', h).strip(); author = out('log', '-1', '--format=%ae', h).strip()
    raw = out('diff', '--raw', '--abbrev=40', R.DEV, h).strip().splitlines(); ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', R.DEV, h).strip().splitlines()}
    fl = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); fl[path] = (b1, b2, st, m2)
    a_sum = sum(int(v[0]) for v in ns.values()); d_sum = sum(int(v[1]) for v in ns.values())
    want_paths = sorted(f['path'] for f in pr['files'])
    print('   parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == %s: %s | subject (%d chars, ascii %s): %s | keys in subject %s | author %s' % (
        par == [R.DEV], lr, t[:12], pr['tree'][:12], t == pr['tree'], len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj), author))
    print('   files %s == want: %s | +%d/-%d (want +%d/-%d) %s | name-status %s | modes %s | every path under __tests__/: %s' % (
        [x.split('/')[-1] for x in sorted(fl)], sorted(fl) == want_paths, a_sum, d_sum, pr['adds'], pr['dels'], (a_sum, d_sum) == (pr['adds'], pr['dels']), sorted(v[2] for v in fl.values()), sorted({v[3] for v in fl.values()}), all('/__tests__/' in x for x in fl)))
    for f in pr['files']:
        path = f['path']; b1, b2, st, m2 = fl.get(path, ('?', '?', '?', '?')); lines_h = out('show', h + ':' + path).count('\n')
        print('   %-100s develop %s -> head %s (%s, %s) | RECOUNT blob %s: %s | lines at head %d (want %d): %s | dev blob == pin: %s' % (path.replace(R.D, ''), b1[:12], b2[:12], st, m2, f['blob'][:12], b2 == f['blob'], lines_h, f['lines'], lines_h == f['lines'], (b1 == (f['dev_blob'] or '0' * 40))))
        CHANGED[path] = (b1, b2, st, m2, r['n'], p)
        for label, rd, sha16, mode, adds, dels, hunk, sblob, slines, tip in f['canon']:
            if sblob: print('      TRUNCATION row %s: the seat\'s STRICT blob %s / %d lines vs the head blob %s / %d lines (the head must be the RECOUNT one): head != strict %s' % (label, sblob, slines, b2[:12], lines_h, not b2.startswith(sblob)))
    d0 = out('diff', '-U0', R.DEV, h); minus_lines = [l for l in d0.splitlines() if l.startswith('-') and not l.startswith('---')]
    print('   `-` lines %d (READY declares %d): %s | %s' % (len(minus_lines), pr['dels'], len(minus_lines) == pr['dels'], [x[:70] for x in minus_lines[:3]]))
print('--- disjointness over the captured heads')
owners = {}
for path, v in CHANGED.items(): owners.setdefault(path, []).append(v[4])
print('union paths', len(CHANGED), '(want 16) | any path in two PRs:', {k: v for k, v in owners.items() if len(v) > 1} or 'NONE', '| name-status', sorted(v[2] for v in CHANGED.values()), '(want 11 A + 5 M)')
print('∩ Seat B 16th dirs:', [x for x in CHANGED if any(x.startswith(d) for d in R.SEATB_DIRS)] or 'NONE', '| ∩ Seat B pushed paths:', sorted(set(CHANGED) & {x[3] for x in R.SEATB}) or 'NONE', '| every path under api-gateway / auth / scripts/__tests__:', all(x.startswith((R.AG, R.AU, R.SC + '__tests__/')) for x in CHANGED))
print('the HELD KS-1123 file %s at develop: %s (want ABSENT) | in any head: %s' % (R.HELD['file'].split('/')[-1], 'ABSENT' if git('cat-file', '-e', R.DEV + ':' + R.HELD['file'])[0] else 'PRESENT', [p for p in present if git('cat-file', '-e', READY[p]['h'] + ':' + R.HELD['file'])[0] == 0] or 'NONE'))
print('--- static reads at develop for the seat findings')
for p in R.PUSH:
    br = R.PRS[p]['branch'].replace('refs/heads/', ''); ex = R.PRS[p]['excised']
    print('branch PR %-2s %-75s ascii %s len %3d | own key once: %s | excised %s present: %s | archived key form in branch: %s | foreign ks- keys: %s' % (
        p, br[:75], br.isascii(), len(br), br.count(R.PRS[p]['key'].lower() + '-') == 1, ex, (ex + '-') in br if ex else 'n/a', [k for k in R.ARCHIVED if k.lower() + '-' in br], [x for x in re.findall(r'ks-\d{3,4}', br) if x != R.PRS[p]['key'].lower()] or 'NONE'))
for lane, pj in (('api-gateway', R.AG + 'package.json'), ('auth', R.AU + 'package.json')):
    pjt = out('show', R.DEV + ':' + pj); m = re.search(r'"test"\s*:\s*"([^"]*)"', pjt); print('lane %-12s scripts.test = %r' % (lane, m.group(1) if m else '?'))
hook = out('show', R.DEV + ':.githooks/pre-push').splitlines()
print('hook .githooks/pre-push lines %d | :76 %r' % (len(hook), hook[75][:80] if len(hook) > 75 else '?'))
rss = out('show', R.DEV + ':' + R.SC + 'run-shell-suites.sh')
print('run-shell-suites.sh exists at develop: %s | scripts/__tests__ files at develop: %d (the 44 shell suites live where? count of *.test.sh under scripts/__tests__: %d)' % (bool(rss), len(out('ls-tree', '-r', '--name-only', R.DEV, R.SC + '__tests__/').splitlines()), sum(1 for x in out('ls-tree', '-r', '--name-only', R.DEV, R.SC + '__tests__/').splitlines() if x.endswith('.test.sh'))))
base = out('show', R.DEV + ':' + R.SC + '__tests__/pre_push_hook_base.test.sh').splitlines()
print('pre_push_hook_base.test.sh at develop: lines %d | :46-:54 (the section_1 hunk site, the model header -46,9; reanchored at 49):' % len(base))
for i in range(45, 55): print('   :%d %r' % (i + 1, base[i][:100] if len(base) > i else '?'))
print('   count of "leg 12" (case-insensitive) %d | "leg 14" %d | "12" in :46-:54 lines: %s' % (sum(1 for l in base if 'leg 12' in l.lower()), sum(1 for l in base if 'leg 14' in l.lower()), [i + 1 for i in range(45, 54) if len(base) > i and '12' in base[i]]))
print('done', now())
