#!/usr/bin/env python3
"""shape_gate18C.py — READ-ONLY local object reads in the Secuura checkout for the Seat C 18th six-PR batch gate (three test-only + three
code_patch). Per captured READY (mail_seatC18_ready*_pr<N>_*.md): PR number / head / branch / tree vs the READY text; parent == develop 8c2f7b3fd;
behind/ahead 0/1; diff --raw blobs / modes / numstat vs round18C (the head blob, the line count) per FILE; the changed set == the declared files
EXACTLY (test-only rows: every path under __tests__/; code_patch rows: the product path(s) + the test file, nothing else); `-` line count; the
file's line count at the head. Static reads at develop: the 11 canonicals (3 run patches + 8 section files: existence, sha256[:16], hunk headers,
`+`/`-` counts, `+++` path, the declared-vs-actual new count — the truncation class the 16th met does NOT recur, measured), the READY fences vs the
run patches (7/7), cat(section_1, section_2) == patch.diff on the four code_patch runs, the `.opts` second line (the ONE accommodation), the 10
distinct targets at develop (5 present at their blobs, 5 ABSENT), the 2 tamper files' blobs at 8c2f7b3fd / 3916eacd1 / 64ab10513 / a1931d2f3, the
anchor-ambiguity `from` counts in index.ts (8 / 3 / 3) and the two verification.ts `from`s (1 / 1), the 6 branch names' ASCII-ness + the ks-733
excision + the ruled KS-1257 tail, the lane's test script, the hook's :76, the checker records (A4 / A5 counts from red_first.json /
green_after.json; the run tips), the KS-947 test file at develop (the PARITY cell — the cover the seat recorded). Never a write verb here (apply /
merge-tree live in predict_batch_scratch_gate18C.py's --shared clone). Writes nothing (stdout). Re-runnable. Derived from
gatesets/2026-09-22_gate16C_seatC/shape_gate16C.py."""
import glob, hashlib, json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18C as R
REPO = R.REPO
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def out(*a):
    rc, o, e = git(*a)
    if rc: print('  (git', a[:2], 'rc', rc, e.strip()[:120], ')')
    return o
print('shape_gate18C', now())
print('--- develop', R.DEV[:9], 'tree', out('rev-parse', R.DEV + '^{tree}').strip()[:12], '== round18C', R.DEV_TREE[:12], out('rev-parse', R.DEV + '^{tree}').strip() == R.DEV_TREE,
      '| parents', out('rev-list', '--parents', '-n1', R.DEV).split()[1:], '(want [3916eacd1]) | rev-list --count --first-parent', R.DEV_PRE1036[:9] + '..' + R.DEV[:9], '=', out('rev-list', '--count', '--first-parent', R.DEV_PRE1036 + '..' + R.DEV).strip(), '(seat: 1)', '| subject:', out('log', '-1', '--format=%s', R.DEV).strip())
print('    3916eacd1 tree', out('rev-parse', R.DEV_PRE1036 + '^{tree}').strip()[:12], '== brief', R.DEV_PRE1036_TREE[:12], out('rev-parse', R.DEV_PRE1036 + '^{tree}').strip() == R.DEV_PRE1036_TREE, '| #1036 head in store:', git('cat-file', '-e', R.PR1036_HEAD + '^{commit}')[0] == 0,
      '| the #1036 squash diff vs 3916eacd1: files', len(out('diff', '--name-only', R.DEV_PRE1036, R.DEV).strip().splitlines()), '(seat: 50) ∩ the 10 paths:', sorted(set(out('diff', '--name-only', R.DEV_PRE1036, R.DEV).strip().splitlines()) & set(R.all_paths())) or 'NONE', '∩ the 2 tamper files:', sorted(set(out('diff', '--name-only', R.DEV_PRE1036, R.DEV).strip().splitlines()) & {x[0] for x in R.TAMPER_BLOBS}) or 'NONE')
print('--- the 11 canonicals (3 run patches + 8 section files): existence, sha256[:16], hunk headers, +/- counts, declared-vs-actual new count, the .opts line')
nrows = 0
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        for row in f['canon']:
            label, rd, fn, sha16, opts, adds, dels, hunk = row; nrows += 1
            path = R.canon_path(row); ex = os.path.exists(path); t = open(path, encoding='utf-8').read() if ex else ''
            c16 = hashlib.sha256(t.encode()).hexdigest()[:16] if ex else None
            hunks = re.findall(r'^@@[^\n]*', t, re.M); plus = sum(1 for l in t.splitlines() if l.startswith('+') and not l.startswith('+++')); minus = sum(1 for l in t.splitlines() if l.startswith('-') and not l.startswith('---'))
            ppp = re.findall(r'^\+\+\+ b/(.*)$', t, re.M)
            m = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', hunks[0]) if hunks else None
            declared_new = int(m.group(4)) if m else None
            cls = 'TRUNCATION?' if (f['mode'] == 'new' and declared_new is not None and declared_new < plus) else 'header consistent'
            optsf = path.replace('.diff', '.opts'); optl = open(optsf).read().splitlines() if os.path.exists(optsf) else []
            print('  PR %-2s %-16s %-34s %-14s exists %s | sha16 %s == %s: %s | first hunk %r == %r: %s | hunks %d | +%d/-%d (want +%d/-%d) %s | +++ %s == target: %s | declared new=%s vs actual + %d -> %s | opts line2 %r == pin %r: %s' % (
                p, label, rd, fn, ex, c16, sha16, c16 == sha16, hunks[0][:len(hunk)] if hunks else None, hunk, (hunks[0][:len(hunk)] if hunks else None) == hunk, len(hunks), plus, minus, adds, dels, (plus, minus) == (adds, dels), [x.split('/')[-1] for x in ppp], ppp == [f['path']], declared_new, plus, cls, optl[1] if len(optl) > 1 else ('(no .opts file)' if not optl else ''), opts, (optl[1] if len(optl) > 1 else '') == opts if optl else 'n/a'))
print('  canonical rows', nrows, '(want 11 = 3 run patches + 8 sections)')
print('--- the 7 READY rows: fence == run patch.diff; cat(section_1, section_2) == patch.diff on the code_patch runs; the run tips; checker A4/A5')
RUNS = [('KS-947-F3F4b', '2026-09-22_ks947-ornith35b-night2', '1', None), ('KS-1123-F3b-CAST', '2026-09-22_ks1123-ornith35b-night', '2', None), ('KS-1192-NOQUOTE', '2026-09-22_ks1192-ornith35b-night', '3', None),
        ('KS-1231-PARTA', '2026-09-22_ks1231-ornith35b-night', '4', 'PARTA'), ('KS-1231-PARTB', '2026-09-22_ks1231-ornith35b-night2', '4', 'PARTB'), ('KS-1246-SERVICESBODY', '2026-09-22_ks1246-ornith35b-night', '5', 'SERVICESBODY'), ('KS-1257-THREEHUNKS', '2026-09-22_ks1257-ornith35b-night2', '6', 'THREEHUNKS')]
for tag, rd, p, a4k in RUNS:
    pd = R.run_dir(rd) + '/out.md.checker/patch.diff'; pt = open(pd, 'rb').read(); p16 = hashlib.sha256(pt).hexdigest()[:16]
    ff = [x for x in glob.glob(os.path.join(R.LM, 'night', 'READY_%s-R16_*.diff.md' % tag)) if '.pre-' not in x]
    f16 = None
    if ff:
        ft = open(ff[0], encoding='utf-8').read(); mm = re.search(r'^```diff\n(.*?)^```', ft, re.S | re.M); f16 = hashlib.sha256(mm.group(1).encode()).hexdigest()[:16] if mm else None
    inp = json.load(open(R.run_dir(rd) + '/input.json')); tip = inp.get('tip', '?')[:9]
    co = open(R.run_dir(rd) + '/checker.out', encoding='utf-8').read(); res = re.search(r'^RESULT: (.*)$', co, re.M)
    line = '  %-20s %-34s patch.diff sha16 %s | READY file %s | fence sha16 %s == patch: %s | input.json tip %s (want %s) | checker %s' % (tag, rd, p16, os.path.basename(ff[0])[:70] if ff else 'NOT FOUND', f16, f16 == p16, tip, R.PRS[p]['tip'], res.group(1) if res else '?')
    s1 = R.run_dir(rd) + '/out.md.checker/section_1.diff'
    if os.path.exists(s1):
        cat = open(s1, 'rb').read() + open(R.run_dir(rd) + '/out.md.checker/section_2.diff', 'rb').read()
        rf = json.load(open(R.run_dir(rd) + '/out.md.checker/red_first.json')); ga = json.load(open(R.run_dir(rd) + '/out.md.checker/green_after.json'))
        reds = sorted(a['title'] for tr in rf['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed')
        want = R.PRS[p]['a4'][a4k]
        line += ' | cat(s1,s2) == patch.diff: %s | A4 red_first %d failed / %d run (pin %d / %d) %s | A5 green_after %d failed / %d run | A4 red titles == pin: %s' % (cat == pt, rf['numFailedTests'], rf['numTotalTests'], want[0], want[1], (rf['numFailedTests'], rf['numTotalTests']) == (want[0], want[1]), ga['numFailedTests'], ga['numTotalTests'], reds == sorted(want[2]))
        a2 = re.search(r'^PASS A2 (.*)$', co, re.M); line += ' | A2: %s' % (a2.group(1)[:110] if a2 else '?')
        tsct = re.search(r'^INFO tsc on the test file alone.*?rc=(\d+) \((\d+) lines', co, re.M); line += ' | checker tsc-on-test-file-alone rc %s (%s lines)' % (tsct.group(1), tsct.group(2)) if tsct else ''
    else:
        gt = json.load(open(R.run_dir(rd) + '/out.md.checker/green_tip.json')); line += ' | T5 green_tip %d passed / %d total' % (gt['numPassedTests'], gt['numTotalTests'])
        for tj in sorted(glob.glob(R.run_dir(rd) + '/out.md.checker/tamper_*.verdict.out')):
            v = json.load(open(tj)); line += ' | %s red %d == declared %d: %s' % (os.path.basename(tj).split('_')[1].split('.')[0], len(v['red']), len(v['declared']), sorted(v['red']) == sorted(v['declared']))
    print(line)
print('--- the 10 distinct targets at develop', R.DEV[:9])
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        rc, o, e = git('cat-file', '-e', R.DEV + ':' + f['path'])
        if rc: print('  PR %-2s %-7s %-100s ABSENT at develop (want ABSENT): %s' % (p, f['kind'], f['path'].replace(R.D, ''), f['mode'] == 'new'))
        else:
            b = out('rev-parse', R.DEV + ':' + f['path']).strip(); ln = out('show', R.DEV + ':' + f['path']).count('\n')
            print('  PR %-2s %-7s %-100s develop blob %s == %s: %s | lines %d (want %s): %s' % (p, f['kind'], f['path'].replace(R.D, ''), b[:12], (f['dev_blob'] or '?')[:12], b == f['dev_blob'], ln, f['dev_lines'], ln == f['dev_lines']))
print('--- the 2 tamper files at develop (the seat item-0 blobs), at 3916eacd1, 64ab10513 and a1931d2f3')
for path, b40 in R.TAMPER_BLOBS:
    b = out('rev-parse', R.DEV + ':' + path).strip()
    print('  %-60s %s == item0 %s | identical at 3916eacd1: %s | at 64ab10513: %s | at a1931d2f3: %s' % (path.replace(R.D, ''), b[:12], b == b40, b == out('rev-parse', R.DEV_PRE1036 + ':' + path).strip(), b == out('rev-parse', R.TIP64 + ':' + path).strip(), b == out('rev-parse', R.TIPA19 + ':' + path).strip()))
print('--- the 5 existing targets at the four tips (the checkers verdicts carry only if the bytes do)')
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        if f['dev_blob']:
            print('  %-90s dev %s | 3916eacd1 same %s | 64ab10513 same %s | a1931d2f3 same %s' % (f['path'].replace(R.D, ''), f['dev_blob'][:12], out('rev-parse', R.DEV_PRE1036 + ':' + f['path']).strip() == f['dev_blob'], out('rev-parse', R.TIP64 + ':' + f['path']).strip() == f['dev_blob'], out('rev-parse', R.TIPA19 + ':' + f['path']).strip() == f['dev_blob']))
print('--- the tamper `from` counts at develop (whole-line, exact case; the anchor-ambiguity rows are KS-947 x3)')
FILES = {}
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        for label, path, line, cnt, reds, cover in f['tampers']:
            if path not in FILES: FILES[path] = out('show', R.DEV + ':' + path).splitlines()
            inp = json.load(open(R.run_dir(f['canon'][0][1]) + '/input.json')); frm = [t for t in inp['tampers'] if t['id'] == label][0]['from']
            lines = FILES[path]; n = sum(1 for l in lines if l == frm); at = [i + 1 for i, l in enumerate(lines) if l == frm]
            print('  PR %-2s %-8s %-40s :%-5d whole-line count %d (want %d): %s | at lines %s | :%d is the `from`: %s | reds declared %d | cover cells %d | %r' % (p, label, path.replace(R.D, ''), line, n, cnt, n == cnt, at, line, len(lines) >= line and lines[line - 1] == frm, len(reds), len(cover), frm[:60]))
idx = FILES.get(R.AG + 'src/index.ts', out('show', R.DEV + ':' + R.AG + 'src/index.ts').splitlines())
print('  index.ts lines %d | :991 %r | :1016 %r (the two rateLimit mounts above the F4AUTH / F4USERS `max` lines) | :1017-:1020 %s' % (len(idx), idx[990][:60], idx[1015][:60], [idx[i][:40] for i in range(1016, 1020)]))
print('--- READYs captured')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read(); m = re.search(R.ready_regex(), t)
    br = re.search(r'\bbranch\s*\n?(feature/[^\s,]+)', t); tr = re.search(r'Head tree ([0-9a-f]{40})', t)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), branch=br.group(1) if br else '?', tree=tr.group(1) if tr else '?', file=os.path.basename(f))
present = [p for p in R.PUSH if p in READY]
print('present seat PRs:', present, '| PR numbers', [READY[p]['n'] for p in present], '| missing', [p for p in R.PUSH if p not in READY] or 'none')
CHANGED = {}
for p in present:
    r = READY[p]; pr = R.PRS[p]; h = r['h']
    print('#%s PR %s %s %s READY head %s == round18C %s: %s | READY PR number %s == %s: %s | READY branch == round18C: %s | READY tree == round18C: %s' % (
        r['n'], p, pr['key'], pr['kind'], h[:9], pr['head'][:9], h == pr['head'], r['n'], pr['n'], r['n'] == pr['n'], r['branch'] == pr['branch'].replace('refs/heads/', ''), r['tree'] == pr['tree']))
    if git('cat-file', '-e', h + '^{commit}')[0]: print('   head NOT in the local object store'); continue
    par = out('rev-list', '--parents', '-n1', h).split()[1:]; lr = out('rev-list', '--left-right', '--count', R.DEV + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip(); subj = out('log', '-1', '--format=%s', h).strip(); author = out('log', '-1', '--format=%ae', h).strip()
    raw = out('diff', '--raw', '--abbrev=40', R.DEV, h).strip().splitlines(); ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', R.DEV, h).strip().splitlines()}
    fl = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); fl[path] = (b1, b2, st, m2)
    a_sum = sum(int(v[0]) for v in ns.values()); d_sum = sum(int(v[1]) for v in ns.values())
    want_paths = sorted(f['path'] for f in pr['files']); prod = sorted(f['path'] for f in pr['files'] if f['kind'] == 'product')
    print('   parent==DEV %s | develop...head behind/ahead %s (want 0 1) | tree %s == %s: %s | subject (%d chars, ascii %s): %s | keys in subject %s | author %s' % (
        par == [R.DEV], lr, t[:12], pr['tree'][:12], t == pr['tree'], len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj), author))
    print('   files %s == want: %s | +%d/-%d (want +%d/-%d) %s | name-status %s | modes %s | paths outside __tests__/: %s == the declared PRODUCT set %s: %s | nothing under services/auth/: %s' % (
        [x.split('/')[-1] for x in sorted(fl)], sorted(fl) == want_paths, a_sum, d_sum, pr['adds'], pr['dels'], (a_sum, d_sum) == (pr['adds'], pr['dels']), sorted(v[2] for v in fl.values()), sorted({v[3] for v in fl.values()}), [x.split('/')[-1] for x in sorted(fl) if '/__tests__/' not in x], [x.split('/')[-1] for x in prod], sorted(x for x in fl if '/__tests__/' not in x) == prod, not any(x.startswith(R.AU) for x in fl)))
    for f in pr['files']:
        path = f['path']; b1, b2, st, m2 = fl.get(path, ('?', '?', '?', '?')); lines_h = out('show', h + ':' + path).count('\n')
        print('   %-7s %-100s develop %s -> head %s (%s, %s) | head blob %s: %s | lines at head %d (want %d): %s | dev blob == pin: %s' % (f['kind'], path.replace(R.D, ''), b1[:12], b2[:12], st, m2, f['blob'][:12], b2 == f['blob'], lines_h, f['lines'], lines_h == f['lines'], (b1 == (f['dev_blob'] or '0' * 40))))
        CHANGED.setdefault(path, []).append((b1, b2, st, m2, r['n'], p))
    d0 = out('diff', '-U0', R.DEV, h); minus_lines = [l for l in d0.splitlines() if l.startswith('-') and not l.startswith('---')]
    print('   `-` lines %d (READY declares %d): %s | %s' % (len(minus_lines), pr['dels'], len(minus_lines) == pr['dels'], [x[:70] for x in minus_lines[:4]]))
print('--- disjointness over the captured heads')
print('union paths', len(CHANGED), '(want 10) | paths in two PRs:', {k.split('/')[-1]: [v[4] for v in vs] for k, vs in CHANGED.items() if len(vs) > 1} or 'NONE', '(want exactly health.ts in #1171 + #1173)', '| name-status', sorted(v[2] for vs in CHANGED.values() for v in vs), '(want 5 A + 6 M over 11 rows)')
hp = R.AG + 'src/services/health.ts'
if hp in CHANGED and len(CHANGED[hp]) == 2:
    print('the health.ts pair: #%s blob %s / #%s blob %s (both from develop %s); the PAIR blob %s / %d lines is neither (measured in predict)' % (CHANGED[hp][0][4], CHANGED[hp][0][1][:12], CHANGED[hp][1][4], CHANGED[hp][1][1][:12], CHANGED[hp][0][0][:12], R.PAIR_BLOB[:12], R.PAIR_LINES))
print('∩ Seat B 18th dirs:', [x for x in CHANGED if any(x.startswith(d) for d in R.SEATB_DIRS)] or 'NONE', '| ∩ Seat B READY paths (4 PRs so far):', sorted(set(CHANGED) & {p_ for x in R.SEATB for p_ in x[3]}) or 'NONE', '| ∩ Seat B brief paths (9):', sorted(set(CHANGED) & set(R.SEATB_BRIEF_PATHS)) or 'NONE', '| every path under api-gateway:', all(x.startswith(R.AG) for x in CHANGED))
print('--- static reads at develop for the seat findings')
for p in R.PUSH:
    br = R.PRS[p]['branch'].replace('refs/heads/', ''); ex = R.PRS[p]['excised']
    print('branch PR %-2s %-95s ascii %s len %3d | own key once: %s | excised %s present: %s | scanner ks-\\d+ (not own): %s | archived key form: %s' % (
        p, br[:95], br.isascii(), len(br), br.count(R.PRS[p]['key'].lower() + '-') == 1, ex, (ex + '-') in br if ex else 'n/a', [x for x in re.findall(r'ks-\d+', br) if x != R.PRS[p]['key'].lower()] or 'NONE', [k for k in R.ARCHIVED if k.lower() + '-' in br] or 'NONE'))
print('the WITHDRAWN KS-1257 tail control: scanner on `…-admin-write-r16-threehunks-1` ->', re.findall(r'ks-\d+', 'feature/ks-1257-after-platform-settings-has-expired-a-partial-admin-write-r16-threehunks-1'), '(the seat: [ks-1257, ks-1])')
pjt = out('show', R.DEV + ':' + R.AG + 'package.json'); m = re.search(r'"test"\s*:\s*"([^"]*)"', pjt); print('lane api-gateway scripts.test = %r' % (m.group(1) if m else '?'))
hook = out('show', R.DEV + ':.githooks/pre-push').splitlines()
print('hook .githooks/pre-push lines %d | :76 %r' % (len(hook), hook[75][:80] if len(hook) > 75 else '?'))
print('scripts/__tests__ *.test.sh at develop: %d (the in-hook shell-suite corpus the seat reports as 45 of 45 — the 16th added the 45th)' % sum(1 for x in out('ls-tree', '-r', '--name-only', R.DEV, R.SC + '__tests__/').splitlines() if x.endswith('.test.sh')))
print('--- the KS-947 test file at develop (ks733-users-mfa-rate-limit-mount.test.ts, 99 lines): the PARITY cell the seat recorded as develop cover for F4AUTH / F4USERS')
k733 = out('show', R.DEV + ':' + R.AG + 'src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts').splitlines()
print('  lines %d | it(/test( cells at develop: %s' % (len(k733), [(i + 1, l.strip()[:90]) for i, l in enumerate(k733) if re.match(r'\s*(it|test)\(', l)]))
print('--- the health.ts hunk sites at develop (Part B @@ -45,8 / KS-1246 @@ -212,4): the pair at different hunks')
h = out('show', R.DEV + ':' + R.AG + 'src/services/health.ts').splitlines()
print('  health.ts lines %d | :45-:52 %s | :212-:215 %s | :40 %r (the TS2339 site the temp-tsconfig type-check reads at develop AND head)' % (len(h), [x[:50] for x in h[44:52]], [x[:60] for x in h[211:215]], h[39][:80]))
print('done', now())
