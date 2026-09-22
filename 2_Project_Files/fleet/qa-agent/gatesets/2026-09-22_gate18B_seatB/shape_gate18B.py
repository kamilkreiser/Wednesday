#!/usr/bin/env python3
r"""shape_gate18B.py — READ-ONLY local object reads in the Secuura checkout for the Seat B 18th seven-PR batch gate (three comment + three
test_only + one code_patch). Per captured READY (mail_seatB18_ready*_pr<N>_*.md): PR number / head / branch / tree vs the READY text; parent ==
the seat's parent 3916eacd1 (NOT develop — the #1036 squash landed between); PARENT...head behind/ahead 0/1 AND develop...head behind/ahead 1/1;
diff --raw blobs / modes / numstat vs round18B per FILE; the changed set == the declared files EXACTLY (comment / test_only rows: every path under
__tests__/; the code_patch row: documents.ts + its test, nothing else; nothing under services/auth that is not a test); `-` line count; the
file's line count at the head; the comment-only proof re-run over `git diff -U0` (every changed line a comment line) on the three comment rows.
Static reads: the 9 apply units (6 run patches + KS-1265's two section files + its whole patch.diff = cat(section_1, section_2)): existence,
sha256[:16], hunk headers, `+`/`-` counts, `+++` path, the declared-vs-actual new count (the 16th's truncation class — measured NOT to recur), the
`.opts` files (empty = strict); the READY fences under local-model/night/ vs the run patches (8/8); the checker records (RESULT lines, the
input.json tips, KS-1265's red_first.json / green_after.json A4 / A5 counts and the red title); the 9 distinct targets at PARENT and at develop
(5 present at their blobs, 4 ABSENT — identical at both tips); the 4 tamper files' blobs at PARENT / develop / 64ab10513; the tamper `from`
counts (substring AND whole-line — the 8J :260 ambiguity: substring 2 / whole-line 1); the #1036 move (`git diff --name-only 3916eacd1 8c2f7b3fd`
— 50 paths) ∩ the 9 paths ∪ 4 tamper files; the 7 branch names' ASCII-ness + the hyphenated-key scanner (`re.findall(r'ks-\d+')` — exactly the
own key each; the ks-1257 `threehunks-1` control reads two) + the two excisions; the lanes' test scripts; the hook's :76; the ks795 cover cell
by name at develop; the ks727 file's `await` at :243 (the seat's F7 TS1378 site); the seat's octopus 5185c65cf in the shared store. Never a write
verb here (apply / merge-tree live in predict_batch_scratch_gate18B.py's --shared clone). Writes nothing (stdout). Re-runnable. Derived from
gatesets/2026-09-22_gate18C_seatC/shape_gate18C.py (itself from gate16C's / gate16B's)."""
import glob, hashlib, json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18B as R
REPO = R.REPO; P = R.PARENT; D = R.DEV
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
def out(*a):
    rc, o, e = git(*a)
    if rc: print('  (git', a[:2], 'rc', rc, e.strip()[:120], ')')
    return o
print('shape_gate18B', now())
print('--- the seat parent', P[:9], 'tree', out('rev-parse', P + '^{tree}').strip()[:12], '== round18B', R.PARENT_TREE[:12], out('rev-parse', P + '^{tree}').strip() == R.PARENT_TREE, '| subject:', out('log', '-1', '--format=%s', P).strip())
print('--- develop', D[:9], 'tree', out('rev-parse', D + '^{tree}').strip()[:12], '== round18B', R.DEV_TREE[:12], out('rev-parse', D + '^{tree}').strip() == R.DEV_TREE,
      '| parents', [x[:9] for x in out('rev-list', '--parents', '-n1', D).split()[1:]], '(want [3916eacd1]) | rev-list --count --first-parent', P[:9] + '..' + D[:9], '=', out('rev-list', '--count', '--first-parent', P + '..' + D).strip(), '| rev-list --count (all) =', out('rev-list', '--count', P + '..' + D).strip(), '| subject:', out('log', '-1', '--format=%s', D).strip())
mv = out('diff', '--name-only', P, D).strip().splitlines()
print('--- THE #1036 MOVE 3916eacd1 -> 8c2f7b3fd: files', len(mv), '(seat: 50) | package.json', sum(1 for x in mv if x.endswith('/package.json') or x == 'Blockchain/Dev/package.json'), 'package-lock.json', sum(1 for x in mv if x.endswith('package-lock.json')), 'other', [x for x in mv if not x.endswith('package.json') and not x.endswith('package-lock.json')],
      '| shortstat', out('diff', '--shortstat', P, D).strip(), '| ∩ the 9 paths:', sorted(set(mv) & set(R.all_paths())) or 'NONE', '| ∩ the 4 tamper files:', sorted(set(mv) & {x[0] for x in R.TAMPER_BLOBS}) or 'NONE', '| #1036 head in store:', git('cat-file', '-e', R.PR1036_HEAD + '^{commit}')[0] == 0)
print('    the move under the four lanes\' src/ or config:', [x for x in mv if any(x.startswith(l + 'src/') for l in (R.OR, R.AN, R.AU, R.SH))] or 'NONE', '| touching a lane package.json:', [x.replace(R.D, '') for x in mv if x in (R.OR + 'package.json', R.AN + 'package.json', R.AU + 'package.json', R.SH + 'package.json', R.OR + 'package-lock.json', R.AN + 'package-lock.json', R.AU + 'package-lock.json', R.D + 'package.json', R.D + 'package-lock.json')])
print('--- the 9 apply units (6 run patches + 2 KS-1265 sections; + the whole KS-1265 patch.diff): existence, sha256[:16], hunk headers, +/- counts, declared-vs-actual new count, the .opts file')
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
            print('  PR %-2s %-14s %-34s %-14s exists %s | sha16 %s == %s: %s | first hunk %r%s | hunks %d | +%d/-%d (want +%d/-%d) %s | +++ %s == target: %s | declared new=%s vs actual + %d -> %s | .opts lines %r (want empty = strict)' % (
                p, label, rd, fn, ex, c16, sha16, c16 == sha16, hunks[0][:22] if hunks else None, (' == %r: %s' % (hunk, (hunks[0][:len(hunk)] if hunks else None) == hunk)) if hunk else '', len(hunks), plus, minus, adds, dels, (plus, minus) == (adds, dels), [x.split('/')[-1] for x in ppp], ppp == [f['path']], declared_new, plus, cls, optl[1:] if len(optl) > 1 else optl))
print('  apply units', nrows, '(want 8 = 6 run patches + 2 sections)')
cf = R.PRS['3']['canon_full']; pd = R.run_dir(cf[1]) + '/out.md.checker/patch.diff'; pt = open(pd, 'rb').read()
s1 = open(R.run_dir(cf[1]) + '/out.md.checker/section_1.diff', 'rb').read(); s2 = open(R.run_dir(cf[1]) + '/out.md.checker/section_2.diff', 'rb').read()
print('  KS-1265 whole patch.diff sha16 %s == pin %s: %s | cat(section_1, section_2) == patch.diff: %s | sections.json: %s' % (hashlib.sha256(pt).hexdigest()[:16], cf[3], hashlib.sha256(pt).hexdigest()[:16] == cf[3], s1 + s2 == pt, json.load(open(R.run_dir(cf[1]) + '/out.md.checker/sections.json')) if os.path.exists(R.run_dir(cf[1]) + '/out.md.checker/sections.json') else '?'))
for v in ('section_2.decl.diff', 'section_2.tdz.diff'):
    vp = R.run_dir(cf[1]) + '/out.md.checker/' + v
    print('  KS-1265 %s byte-identical to section_2.diff: %s' % (v, open(vp, 'rb').read() == s2 if os.path.exists(vp) else 'ABSENT'))
print('--- the 8 READY rows: fence == run patch.diff; the run tips; checker RESULT; KS-1265 A4 / A5')
RUNS = [('KS-1118-F3b', '2026-09-17_ks1118-ornith35b-night2', '1'), ('KS-1158-R5b', '2026-09-17_ks1158-ornith35b-night', '2'), ('KS-1265-EARLYGUARD-R16', '2026-09-22_ks1265-ornith35b-night', '3'),
        ('KS-1171-8J-TSFIX-R16', '2026-09-22_ks1171-ornith35b-night', '4'), ('KS-1171-GUARD3S-TSFIX-R16', '2026-09-22_ks1171-ornith35b-night2', '4'), ('KS-811-F7SETPIN-R16', '2026-09-22_ks811-ornith35b-night', '5'),
        ('KS-1188-MFASIBLINGS-R16', '2026-09-22_ks1188-ornith35b-night4', '6'), ('KS-1181-F3w', '2026-09-17_ks1181-ornith35b-night2', '7')]
for tag, rd, p in RUNS:
    pd = R.run_dir(rd) + '/out.md.checker/patch.diff'; pt = open(pd, 'rb').read(); p16 = hashlib.sha256(pt).hexdigest()[:16]
    ff = [x for x in glob.glob(os.path.join(R.LM, 'night', 'READY_%s_*.diff.md' % tag)) if '.pre-' not in x]
    f16 = None
    if ff:
        ft = open(ff[0], encoding='utf-8').read(); mm = re.search(r'^```diff\n(.*?)^```', ft, re.S | re.M); f16 = hashlib.sha256(mm.group(1).encode()).hexdigest()[:16] if mm else None
    inp = json.load(open(R.run_dir(rd) + '/input.json')); tip = (inp.get('tip') or '?')[:9]
    co = open(R.run_dir(rd) + '/checker.out', encoding='utf-8').read(); res = re.search(r'^RESULT: (.*)$', co, re.M)
    line = '  %-26s %-34s patch.diff sha16 %s | READY file %s | fence sha16 %s == patch: %s | input.json tip %s (want %s): %s | task_type %s | tampers %s | checker %s' % (
        tag, rd, p16, os.path.basename(ff[0])[:60] if ff else 'NOT FOUND', f16, f16 == p16, tip, R.PRS[p]['tip'], tip == R.PRS[p]['tip'], inp.get('task_type'), [(t.get('id'), t.get('file', '').split('/')[-1], t.get('line')) for t in inp.get('tampers', [])], res.group(1) if res else '?')
    if p == '3':
        rf = json.load(open(R.run_dir(rd) + '/out.md.checker/red_first.json')); ga = json.load(open(R.run_dir(rd) + '/out.md.checker/green_after.json'))
        reds = sorted(a['title'] for tr in rf['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed'); want = R.PRS[p]['a4']['EARLYGUARD']
        line += ' | A4 red_first %d failed / %d run (pin %d / %d) %s | A5 green_after %d failed / %d run | A4 red title == pin: %s %r' % (rf['numFailedTests'], rf['numTotalTests'], want[0], want[1], (rf['numFailedTests'], rf['numTotalTests']) == (want[0], want[1]), ga['numFailedTests'], ga['numTotalTests'], reds == sorted(want[2]), reds[:1])
        a4 = re.search(r'^PASS A4 (.*)$', co, re.M); line += ' | A4 line: %s' % (a4.group(1)[:120] if a4 else '?')
    elif R.PRS[p]['kind'] == 'test_only':
        gt = json.load(open(R.run_dir(rd) + '/out.md.checker/green_tip.json')); line += ' | green_tip %d passed / %d total' % (gt['numPassedTests'], gt['numTotalTests'])
        for tj in sorted(glob.glob(R.run_dir(rd) + '/out.md.checker/tamper_*.verdict.out')):
            v = json.load(open(tj)); line += ' | %s red %d == declared %d: %s' % (os.path.basename(tj).split('_')[1].split('.')[0], len(v['red']), len(v['declared']), sorted(v['red']) == sorted(v['declared']))
        po = R.run_dir(rd) + '/out.md.checker/plant.out'
        if os.path.exists(po): line += ' | plant.out sha12s %s' % re.findall(r'\b([0-9a-f]{12})[0-9a-f]{52}\b', open(po).read())[:4]
    else:
        c4 = re.search(r'^PASS C4 (.*)$', co, re.M); line += ' | C4: %s' % (c4.group(1)[:100] if c4 else '?')
    print(line)
print('--- the 9 distinct targets at PARENT', P[:9], 'and at develop', D[:9])
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        rc, o, e = git('cat-file', '-e', P + ':' + f['path']); rcd = git('cat-file', '-e', D + ':' + f['path'])[0]
        if rc: print('  PR %-2s %-7s %-95s ABSENT at PARENT (want ABSENT): %s | ABSENT at develop: %s' % (p, f['kind'], f['path'].replace(R.D, ''), f['mode'] == 'new', rcd != 0))
        else:
            b = out('rev-parse', P + ':' + f['path']).strip(); ln = out('show', P + ':' + f['path']).count('\n'); bd = out('rev-parse', D + ':' + f['path']).strip()
            print('  PR %-2s %-7s %-95s PARENT blob %s == %s: %s | lines %d (want %s): %s | same at develop: %s | at 64ab10513: %s' % (p, f['kind'], f['path'].replace(R.D, ''), b[:12], (f['dev_blob'] or '?')[:12], b == f['dev_blob'], ln, f['dev_lines'], ln == f['dev_lines'], bd == b, out('rev-parse', R.TIP64 + ':' + f['path']).strip() == b))
print('--- the 4 tamper files (the seat item-0 blobs) at PARENT, develop, 64ab10513')
for path, b40 in R.TAMPER_BLOBS:
    b = out('rev-parse', P + ':' + path).strip()
    print('  %-50s %s == item0 %s | identical at develop: %s | at 64ab10513: %s' % (path.replace(R.D, ''), b[:12], b == b40, b == out('rev-parse', D + ':' + path).strip(), b == out('rev-parse', R.TIP64 + ':' + path).strip()))
print('--- the tamper `from` counts at PARENT (substring AND whole-line; the 8J ambiguity: substring 2 / whole-line 1 at :260, the :401 occurrence deeper-indented)')
FILES = {}; seen = set()
for p in R.PUSH:
    for f in R.PRS[p]['files']:
        for label, path, line, cnt_sub, cnt_wl, reds, cover, sline, stext in f['tampers']:
            if (label, path) in seen: continue
            seen.add((label, path))
            if path not in FILES: FILES[path] = out('show', P + ':' + path).splitlines()
            inp = json.load(open(R.run_dir(f['canon'][0][1]) + '/input.json')); frm = [t for t in inp['tampers'] if t['id'] == label][0]['from']
            lines = FILES[path]; fl = frm.split('\n'); n_wl = 0; at = []
            for i in range(len(lines) - len(fl) + 1):
                if lines[i:i + len(fl)] == fl: n_wl += 1; at.append(i + 1)
            n_sub = sum(1 for l in lines if fl[0].strip() and fl[0].strip() in l)
            print('  PR %-2s %-13s %-30s :%-5d whole-line count %d (want %d): %s at %s | substring count (first from-line, stripped) %d (want %d) | :%d is the `from`: %s | scope :%s %r present: %s | reds declared %d | cover %d | from %r' % (
                p, label, path.replace(R.D, ''), line, n_wl, cnt_wl, n_wl == cnt_wl, at, n_sub, cnt_sub, line, lines[line - 1:line - 1 + len(fl)] == fl, sline, (stext or '')[:40], (lines[sline - 1].strip().startswith(stext.strip()[:30]) if sline else 'n/a'), len(reds), len(cover), frm[:60].replace('\n', '\\n')))
print('--- READYs captured')
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    t = open(f, encoding='utf-8').read(); m = re.search(R.ready_regex(), t)
    br = re.search(r'\bbranch\s*\n?(feature/[^\s,]+)', t); tr = re.search(r'Head tree ([0-9a-f]{40})', t); dv = re.search(r'Develop at origin at READY:\s*\n?([0-9a-f]{40})', t)
    if m: READY[m.group(1)] = dict(n=m.group(3), h=m.group(4), key=m.group(2), branch=br.group(1) if br else '?', tree=tr.group(1) if tr else '?', dev=dv.group(1) if dv else '?', file=os.path.basename(f))
present = [p for p in R.PUSH if p in READY]
print('present seat PRs:', present, '| PR numbers', [READY[p]['n'] for p in present], '| missing', [p for p in R.PUSH if p not in READY] or 'none', '| develop at every READY == 8c2f7b3fd:', all(READY[p]['dev'] == D for p in present))
CHANGED = {}
def is_comment_line(s):
    s = s.strip(); return s.startswith('//') or s.startswith('/*') or s.startswith('*') or s.startswith('*/') or s == ''
for p in present:
    r = READY[p]; pr = R.PRS[p]; h = r['h']
    print('#%s PR %s %s %s READY head %s == round18B %s: %s | READY PR number %s == %s: %s | READY branch == round18B: %s | READY tree == round18B: %s' % (
        r['n'], p, pr['key'], pr['kind'], h[:9], pr['head'][:9], h == pr['head'], r['n'], pr['n'], r['n'] == pr['n'], r['branch'] == pr['branch'].replace('refs/heads/', ''), r['tree'] == pr['tree']))
    if git('cat-file', '-e', h + '^{commit}')[0]: print('   head NOT in the local object store'); continue
    par = out('rev-list', '--parents', '-n1', h).split()[1:]; lr = out('rev-list', '--left-right', '--count', P + '...' + h).split(); lrd = out('rev-list', '--left-right', '--count', D + '...' + h).split()
    t = out('rev-parse', h + '^{tree}').strip(); subj = out('log', '-1', '--format=%s', h).strip(); author = out('log', '-1', '--format=%ae', h).strip(); mb = out('merge-base', D, h).strip()
    raw = out('diff', '--raw', '--abbrev=40', P, h).strip().splitlines(); ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in out('diff', '--numstat', P, h).strip().splitlines()}
    fl = {}
    for l in raw:
        meta, path = l.split('\t', 1); m1, m2, b1, b2, st = meta.split(); fl[path] = (b1, b2, st, m2)
    a_sum = sum(int(v[0]) for v in ns.values()); d_sum = sum(int(v[1]) for v in ns.values())
    want_paths = sorted(f['path'] for f in pr['files']); prod = sorted(f['path'] for f in pr['files'] if f['kind'] == 'product')
    print('   parent==PARENT %s | PARENT...head behind/ahead %s (want 0 1) | develop...head behind/ahead %s (want 1 1 — the #1036 squash) | merge-base(develop, head) == PARENT: %s | tree %s == %s: %s | subject (%d chars, ascii %s): %s | keys in subject %s | author %s' % (
        par == [P], lr, lrd, mb == P, t[:12], pr['tree'][:12], t == pr['tree'], len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj), author))
    print('   files %s == want: %s | +%d/-%d (want +%d/-%d) %s | name-status %s | modes %s | paths outside __tests__/: %s == the declared PRODUCT set %s: %s | nothing under services/auth/ that is not a test: %s | diff vs develop same set: %s' % (
        [x.split('/')[-1] for x in sorted(fl)], sorted(fl) == want_paths, a_sum, d_sum, pr['adds'], pr['dels'], (a_sum, d_sum) == (pr['adds'], pr['dels']), sorted(v[2] for v in fl.values()), sorted({v[3] for v in fl.values()}), [x.split('/')[-1] for x in sorted(fl) if '/__tests__/' not in x], [x.split('/')[-1] for x in prod], sorted(x for x in fl if '/__tests__/' not in x) == prod, not any(x.startswith(R.AU) and '/__tests__/' not in x for x in fl), sorted(out('diff', '--name-only', D, h).strip().splitlines()) == sorted(fl)))
    for f in pr['files']:
        path = f['path']; b1, b2, st, m2 = fl.get(path, ('?', '?', '?', '?')); lines_h = out('show', h + ':' + path).count('\n')
        print('   %-7s %-95s PARENT %s -> head %s (%s, %s) | head blob %s: %s | lines at head %d (want %d): %s | PARENT blob == pin: %s' % (f['kind'], path.replace(R.D, ''), b1[:12], b2[:12], st, m2, f['blob'][:12], b2 == f['blob'], lines_h, f['lines'], lines_h == f['lines'], (b1 == (f['dev_blob'] or '0' * 40))))
        CHANGED.setdefault(path, []).append((b1, b2, st, m2, r['n'], p))
    d0 = out('diff', '-U0', P, h); minus_lines = [l for l in d0.splitlines() if l.startswith('-') and not l.startswith('---')]; plus_lines = [l for l in d0.splitlines() if l.startswith('+') and not l.startswith('+++')]
    print('   `-` lines %d (READY declares %d): %s | `+` lines %d | %s' % (len(minus_lines), pr['dels'], len(minus_lines) == pr['dels'], len(plus_lines), [x[:70] for x in minus_lines[:3]]))
    if pr['kind'] == 'comment':
        viol = [l for l in minus_lines + plus_lines if not is_comment_line(l[1:])]
        print('   COMMENT-ONLY proof over `git diff -U0`: changed lines %d (seat %d), non-comment changed lines %d (want 0): %s | control: `+const x = 1;` -> violations %d (want 1)' % (len(minus_lines) + len(plus_lines), pr['comment_lines'], len(viol), len(viol) == 0, len([l for l in ['+const x = 1;'] if not is_comment_line(l[1:])])))
    if pr['kind'] == 'code_patch':
        prod_hunk = out('diff', '-U0', P, h, '--', prod[0]); hh = re.findall(r'^@@[^\n]*', prod_hunk, re.M); pl = [l for l in prod_hunk.splitlines() if l.startswith('+') and not l.startswith('+++')]; ml = [l for l in prod_hunk.splitlines() if l.startswith('-') and not l.startswith('---')]
        print('   PRODUCT hunk on documents.ts: hunks %s | +%d/-%d (seat +8/-0) | the 8 lines: %s' % (hh, len(pl), len(ml), [x[1:].strip()[:60] for x in pl]))
print('--- disjointness over the captured heads')
print('union paths', len(CHANGED), '(want 9) | paths in two PRs:', {k.split('/')[-1]: [v[4] for v in vs] for k, vs in CHANGED.items() if len(vs) > 1} or 'NONE', '(want NONE)', '| name-status', sorted(v[2] for vs in CHANGED.values() for v in vs), '(want 4 A + 5 M)', '| product paths:', [x.split('/')[-1] for x in CHANGED if '/__tests__/' not in x], '(want [documents.ts])')
print('∩ Seat C 18th dirs (api-gateway):', [x for x in CHANGED if any(x.startswith(d) for d in R.SEATC_DIRS)] or 'NONE', '| ∩ Seat C READY paths (6 PRs, 10 paths):', sorted(set(CHANGED) & {p_ for x in R.SEATC for p_ in x[3]}) or 'NONE', '| ∩ Seat C tamper files:', sorted(set(CHANGED) & set(R.SEATC_TAMPERS)) or 'NONE', '| our 4 tamper files ∩ Seat C paths:', sorted({x[0] for x in R.TAMPER_BLOBS} & {p_ for x in R.SEATC for p_ in x[3]}) or 'NONE', '| Seat C distinct paths', len({p_ for x in R.SEATC for p_ in x[3]}), 'all under api-gateway:', all(p_.startswith(R.AG) for x in R.SEATC for p_ in x[3]))
print('lanes:', sorted({('originate' if x.startswith(R.OR) else 'anchoring' if x.startswith(R.AN) else 'auth' if x.startswith(R.AU) else 'shared' if x.startswith(R.SH) else '?') for x in CHANGED}))
print('--- static reads for the seat findings')
for p in R.PUSH:
    br = R.PRS[p]['branch'].replace('refs/heads/', ''); ex = R.PRS[p]['excised']; sc = re.findall(r'ks-\d+', br)
    print('branch PR %-2s %-100s ascii %s len %3d | scanner ks-\\d+ -> %s == [own]: %s | excised %s present: %s | archived key form: %s | 815s (PR-number form, KS-811): %s' % (
        p, br[:100], br.isascii(), len(br), sc, sc == [R.PRS[p]['key'].lower()], ex, (ex + '-') in br if ex else 'n/a', [k for k in R.ARCHIVED if k.lower() + '-' in br] or 'NONE', '815s' in br))
print('the KS-1257 control: scanner on `feature/ks-1257-after-platform-settings-has-expired-a-partial-admin-write-r16-threehunks-1` ->', re.findall(r'ks-\d+', 'feature/ks-1257-after-platform-settings-has-expired-a-partial-admin-write-r16-threehunks-1'), '(want two: ks-1257, ks-1)')
for lane, d_ in (('originate', R.OR), ('anchoring', R.AN), ('auth', R.AU), ('shared', R.SH)):
    pjt = out('show', P + ':' + d_ + 'package.json'); m = re.search(r'"test"\s*:\s*"([^"]*)"', pjt); print('lane %-9s scripts.test = %r | package.json same at develop: %s' % (lane, m.group(1) if m else '?', out('rev-parse', P + ':' + d_ + 'package.json').strip() == out('rev-parse', D + ':' + d_ + 'package.json').strip()))
hook = out('show', P + ':.githooks/pre-push').splitlines()
print('hook .githooks/pre-push lines %d | :76 %r | same blob at develop: %s' % (len(hook), hook[75][:80] if len(hook) > 75 else '?', out('rev-parse', P + ':.githooks/pre-push').strip() == out('rev-parse', D + ':.githooks/pre-push').strip()))
print('scripts/__tests__ *.test.sh at PARENT: %d (the in-hook shell-suite corpus the seat reports as 45 of 45)' % sum(1 for x in out('ls-tree', '-r', '--name-only', P, R.SC + '__tests__/').splitlines() if x.endswith('.test.sh')))
k795 = out('show', P + ':' + R.AU + 'src/__tests__/ks795-social-link-verified-email.test.ts').splitlines()
hits = [(i + 1, l.strip()[:120]) for i, l in enumerate(k795) if 'refuses terminally when the provider supplies no email' in l]
print('--- the ks795 cover cell (KS-811 ROUTECOLLAPSE): ks795-social-link-verified-email.test.ts at PARENT lines %d | the cell by title: %s | exact title present (\"…nothing matched by identity\"): %s' % (len(k795), hits, any('nothing matched by identity' in l for l in k795)))
k727 = out('show', P + ':' + R.SH + 'src/__tests__/ks727-errorhandler-class-guard.test.ts').splitlines()
print('--- the ks727 file (KS-1181 F3w; the seat F7 TS1378 site): lines %d | :243 %r (top-level await?) %s | header comment lines with \"handler\": %s' % (len(k727), k727[242][:90] if len(k727) > 242 else '?', 'await' in (k727[242] if len(k727) > 242 else ''), [(i + 1, l.strip()[:90]) for i, l in enumerate(k727[:40]) if 'handler' in l.lower()][:6]))
k727h = out('show', R.PRS['7']['head'] + ':' + R.SH + 'src/__tests__/ks727-errorhandler-class-guard.test.ts').splitlines()
print('    the F3w changed line at head vs PARENT:', [(i + 1, a.strip()[:80], b.strip()[:80]) for i, (a, b) in enumerate(zip(k727, k727h)) if a != b])
print('--- the seat octopus %s in the shared store: %s | its tree == the all-7 %s: %s | parents %d' % (R.SEAT_OCTOPUS, git('cat-file', '-e', R.SEAT_OCTOPUS + '^{commit}')[0] == 0, R.SEAT_ALL7[:12], out('rev-parse', R.SEAT_OCTOPUS + '^{tree}').strip() == R.SEAT_ALL7, len(out('rev-list', '--parents', '-n1', R.SEAT_OCTOPUS).split()) - 1))
print('--- the documents.ts hunk site at PARENT (@@ -611,6): :605-:618')
dts = out('show', P + ':' + R.OR + 'src/routes/documents.ts').splitlines(); print('  documents.ts lines %d | %s' % (len(dts), [(i + 1, dts[i].strip()[:70]) for i in range(604, 618)]))
print('done', now())
