#!/usr/bin/env python3
"""c4_docs_gate59.py — gate59 C4 for #1382 (KS-1005): the §4 doc blocks, and the MERGE-IN (Q-M M1-M4) — the head's own folded merge-in
AND any LATER merge-in (e.g. after #1381 lands block 13.). Git objects only, in YOUR scratch clone; the only writes are commit-tree /
merge-tree / hash-object / a temp index under --out (lib wgit refuses any repo under /Volumes/DevMASTER; never a ref).
MODES
  docs  --repo <clone> [--head sha]
    D1 §4 at develop: the skill blob (kit skill_blob) carries "Every test change updates its platform's two HTML docs, in the same commit"
       and both platform-k paths.
    D2 SAME COMMIT: the built commit (vs its parent) carries the test, users.ts and BOTH platform-k docs; 0 platform-s docs in it or the PR.
    D3 ONE PURE INSERT per doc, develop -> head: 0 deleted / replaced lines (no other block edited), kit block_lines inserted, immediately
       before `  </body>` (i.e. after the KS-1333 block, the last block at develop).
    D4 FLOW NUMBERS: head <h2> numbers == kit flow_numbers_head ([1..12, 19]), ascending; the block's only <h2> is `19.`; its <h3>s are 19.x.
    D5 BYTE-IDENTITY: each inserted block == the BUILT commit's own insert (vs 3ce8cd4026a6), byte for byte, and absent from develop.
    D6 CHEAT CONVENTION: unnumbered <h2> ending `&mdash; KS-1005</h2>`, after KS-1333's; `<div>` balanced; WRAPPED in its own
       `<div class="section">` like its neighbours (KS-1404, KS-1333) — the drafter's run FAILS this (README doubt D2: rule it).
    D7 SELF-CONTAINED per doc: names the test file, how to run it (`npx vitest run`), the §5f live sweep owed, and a NOT-covered note.
       The drafter's run FAILS this on both docs (README doubt D3: rule it).
    D8 STATED TIMINGS: every inserted table row / note carrying a duration also carries a date AND a host (or says "projection"); each
       offending row printed. The duration-proximity instrument re-measured at develop: `services/auth` within 120 chars of a duration in
       (a) CLAUDE.md + systemTest/CLAUDE.md + the skill, (b) the PR body's set (both docs + the skill); must-hit CONTROL: durations within
       120 chars of "Akto" in the same files. PASS iff (a) and (b) are 0 and the control > 0; the docs' "must-hit 3" and the PR body's
       "11" are printed beside the measured control (README doubt D4).
  predict --repo <clone> --out <dir>      (Q-M for the head ITSELF: the folded merge-in, ruling 3)
    M0 `merge-tree --write-tree --name-only develop built` -> rc 1, conflicted paths == EXACTLY the two docs (verbatim CONFLICT lines).
    M1 an INDEPENDENT resolution — develop's doc with the built commit's own block inserted by NUMBER order (before the first <h2> > 19,
       else before `  </body>`; the cheat by the same keys' flow numbers) — written over the conflicted tree -> == kit end_tree.
       CONTROL: the block placed BEFORE KS-1333's (19 above 12) gives a DIFFERENT tree.
    M2 head parents == [built, develop].   M3 `git show --remerge-diff <head>` touches EXACTLY the two docs.   M4 0 trailers.
  qm --repo --out --merge-in-head <M> --develop-after <D>   (a LATER merge-in of #1382 over a develop that moved, e.g. #1381 landed)
    the same M0-M4 with the GATED head kit head in place of the built commit: M1 tree == the prediction recomputed on D; M2 parents ==
    [gated head, D]; M3 remerge-diff only the two docs; M4 0 trailers; M5 D descends from kit develop (develop only moved FORWARD).
  --selftest --repo --out   docs: the real head PASSES D3/D4/D5 (positive control) and planted doc copies FAIL their check — a second
            block edited (D3), 19 renumbered 20 (D4), one byte changed in the block (D5), the cheat h2 numbered (D6). Q-M: a SIM develop-after
            (= #1381's merge-in tree squashed onto develop by commit-tree, never a ref) and SIM merge-ins: the predicted one PASSES; an
            extra users.ts edit (M1+M3), 19 above 13 (M1), a single-parent rewrite (M2), a trailer (M4) each FAIL their named check.
Usage: c4_docs_gate59.py docs|predict|qm --repo <clone> [--out dir] [--head sha] [--merge-in-head M --develop-after D] | --selftest --repo --out
rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, git, wgit, now, Checks, opt_factory, show, has_commit, opcodes, guard_scratch, guard_out, tree, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = guard_scratch(opt('--repo'), 'clone'); HEAD = opt('--head', K['head'])
DEV, BUILT, BP = K['develop'], K['built'], K['built_parent']; DOCS = K['docs']; FLOW, CHEAT = DOCS; ANCH = K['doc_close_anchor']; NUM = K['flow_block_number']
MODE = next((m for m in ('docs', 'predict', 'qm') if m in A), None)
for s in (HEAD, DEV, BUILT, BP):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
ENV = {'GIT_AUTHOR_NAME': 'g59', 'GIT_AUTHOR_EMAIL': 'g59@sim', 'GIT_COMMITTER_NAME': 'g59', 'GIT_COMMITTER_EMAIL': 'g59@sim',
       'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}
DUR = re.compile(r'\b\d+(?:[.,]\d+)?\s?(?:ms|s|sec|secs|seconds|min|mins|minutes|h|hours)\b', re.I)


def insert_block(base_txt, new_txt):
    """the ONE pure insert hunk base -> new: (index, lines) or None"""
    b, n = base_txt.split('\n'), new_txt.split('\n'); ops = opcodes(b, n)
    if len(ops) != 1 or ops[0][0] != 'insert': return None
    return ops[0][1], n[ops[0][3]:ops[0][4]]


def own_block(d, src_rev, base_rev):
    r = insert_block(show(REPO, base_rev, d), show(REPO, src_rev, d))
    return r[1] if r else None


def flow_map(flow_txt):
    """{KS-key: number} from the flow doc's <h2>N. ... (KS-n)</h2> lines"""
    return {m.group(2): int(m.group(1)) for m in re.finditer(r'<h2>(\d+)\.[^\n]*\((KS-\d+)\)</h2>', flow_txt)}


def place(d, doc_txt, block, flow_txt, before_key=None):
    """insert block into doc_txt by NUMBER order (or, for the wrong-order CONTROL, before the block of before_key)"""
    ls = doc_txt.split('\n'); fm = flow_map(flow_txt)
    if d == FLOW:
        if before_key:
            at = next(i for i, l in enumerate(ls) if re.search(r'<h2>\d+\.[^\n]*\(%s\)</h2>' % before_key, l))
        else:
            at = next((i for i, l in enumerate(ls) if (lambda m: m and int(m.group(1)) > NUM)(re.match(r'\s*<h2>(\d+)\.', l))), None)
    else:
        def start_of(i):   # the block's start: its wrapping <div class="section"> line when the h2 sits directly inside one
            return i - 1 if i > 0 and ls[i - 1].strip() == '<div class="section">' else i
        at = None
        for i, l in enumerate(ls):
            m = re.search(r'&mdash; (KS-\d+)</h2>', l)
            if m and ((before_key and m.group(1) == before_key) or (not before_key and fm.get(m.group(1), 0) > NUM)):
                at = start_of(i); break
    if at is None:
        at = [i for i, l in enumerate(ls) if l == ANCH]
        if len(at) != 1: raise SystemExit('REFUSING: %r not found exactly once in %s' % (ANCH, d))
        at = at[0]
    return '\n'.join(ls[:at] + block + ls[at:])


def resolve(base_rev, conflicted_tree, other_rev, gated_rev, gated_base, idx, before_key=None):
    """the conflicted tree with each doc replaced by base_rev's doc + the gated block placed by number; -> tree sha"""
    e = {'GIT_INDEX_FILE': idx}; wgit(REPO, 'read-tree', conflicted_tree, env=e)
    flow_after = show(REPO, base_rev, FLOW)
    for d in DOCS:
        blk = own_block(d, gated_rev, gated_base)
        if blk is None: raise SystemExit('REFUSING: no single insert block for %s in %s vs %s' % (d, gated_rev[:12], gated_base[:12]))
        txt = place(d, show(REPO, base_rev, d), blk, flow_after, before_key)
        sha = wgit(REPO, 'hash-object', '-w', '--stdin', inp=txt).strip()
        wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (sha, d), env=e)
    return wgit(REPO, 'write-tree', env=e).strip()


def merge_tree(a, b):
    rc, o, e = wgit(REPO, 'merge-tree', '--write-tree', '--name-only', a, b, check=False)
    ls = o.split('\n'); ct = ls[0].strip(); conf = sorted(set(l for l in ls[1:] if l and not l.startswith(('Auto-merging', 'CONFLICT'))))
    return rc, ct, conf, [l for l in ls if l.startswith('CONFLICT')]


def judge_qm(C, M, gated, gated_base, dev_after, idx, label):
    rc, ct, conf, msgs = merge_tree(dev_after, gated)
    fm = flow_map(show(REPO, dev_after, FLOW)); below = sorted((n, k) for k, n in fm.items() if n < NUM)
    K['wrong_order_key'] = below[-1][1] if below else 'KS-1333'   # CONTROL: KS-1005's block placed ABOVE the highest-numbered block below 19
    C.chk('M0 conflict set', (rc == 1 and conf == sorted(DOCS)) or (rc == 0 and not conf),
          'merge-tree %s x %s rc %d | conflicted paths %s (want EXACTLY the two docs, or a clean merge) | verbatim %s' % (dev_after[:12], gated[:12], rc, conf, msgs))
    pred = resolve(dev_after, ct, None, gated, gated_base, idx) if rc == 1 else ct
    wrong = resolve(dev_after, ct, None, gated, gated_base, idx, before_key=K.get('wrong_order_key', 'KS-1333')) if rc == 1 else None
    mt = tree(REPO, M)
    C.chk('M1 tree == prediction', mt == pred and wrong != pred, '%s tree %s | prediction on %s %s | CONTROL wrong order (KS-1005 above %s) -> %s, differs: %s' % (
        label, mt, dev_after[:12], pred, K.get('wrong_order_key', 'KS-1333'), (wrong or 'n/a')[:12], wrong != pred))
    par = git(REPO, 'log', '-1', '--format=%P', M).split()
    C.chk('M2 two parents', par == [gated, dev_after], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], gated[:12], dev_after[:12]))
    rd = git(REPO, 'show', '--remerge-diff', '--format=', '--name-only', M).split('\n')
    rd = sorted(set(l for l in rd if l.strip()))
    C.chk('M3 remerge-diff only the docs', rd and set(rd) <= set(DOCS), 'git show --remerge-diff %s touches %s (want only the two docs)' % (M[:12], rd or 'NOTHING'))
    t = git(REPO, 'log', '-1', '--format=%(trailers)', M).strip()
    C.chk('M4 no trailer', t == '', 'trailers %r' % t)
    return pred


def judge_docs(C, texts_dev, texts_head, texts_built, texts_bp, skill, built_paths, pr_paths, body=None):
    s4 = "Every test change updates its platform's two HTML docs, in the same commit"
    C.chk('D1 §4 at develop', s4.replace('\n', ' ') in ' '.join(skill.split()) and all(d in skill for d in DOCS),
          'skill blob carries the §4 sentence: %s | both platform-k paths named: %s' % (s4.replace('\n', ' ') in ' '.join(skill.split()), all(d in skill for d in DOCS)))
    need = set(DOCS) | {K['test'], K['product']}
    C.chk('D2 same commit', need <= set(built_paths) and not (set(K['platform_s_docs']) & (set(built_paths) | set(pr_paths))),
          'built commit paths %d, carries test + users.ts + both docs: %s | platform-s docs in the built commit or the PR: %s' % (len(built_paths), need <= set(built_paths), sorted(set(K['platform_s_docs']) & (set(built_paths) | set(pr_paths))) or 'NONE'))
    blocks = {}
    for d in DOCS:
        ins = insert_block(texts_dev[d], texts_head[d]); dl = texts_dev[d].split('\n'); body_at = [i for i, l in enumerate(dl) if l == ANCH]
        ok = ins is not None and len(ins[1]) == K['block_lines'][d] and body_at == [ins[0]]
        C.chk('D3 one pure insert (%s)' % d.split('/')[-1][:24], ok, '%s | ops develop->head: %s | inserted %s line(s) (kit %d) at develop line %s; `  </body>` at %s' % (
            d.split('/')[-1], 'ONE insert' if ins else 'NOT a single pure insert: %s' % [o[0] for o in opcodes(dl, texts_head[d].split('\n'))][:6],
            len(ins[1]) if ins else '-', K['block_lines'][d], ins[0] + 1 if ins else '-', [b + 1 for b in body_at]))
        blocks[d] = ins[1] if ins else []
        bb = insert_block(texts_bp[d], texts_built[d])
        C.chk('D5 byte-identity (%s)' % d.split('/')[-1][:24], bb is not None and bb[1] == blocks[d] and '\n'.join(blocks[d]) not in texts_dev[d],
              'the head block == the BUILT commit\'s own insert vs %s: %s | absent from develop: %s' % (BP[:12], bb is not None and bb[1] == blocks[d], '\n'.join(blocks[d]) not in texts_dev[d] if blocks[d] else '-'))
    fh = texts_head[FLOW]; nums = [int(m) for m in re.findall(r'(?m)^\s*<h2>(\d+)\.', fh)]; fb = '\n'.join(blocks[FLOW])
    h2s = re.findall(r'<h2>(\d+)\.', fb); h3s = re.findall(r'<h3>(\d+)\.(\d+)', fb)
    C.chk('D4 flow numbers', nums == K['flow_numbers_head'] and nums == sorted(nums) and h2s == [str(NUM)] and h3s and all(a == str(NUM) for a, b in h3s),
          'head <h2> numbers %s (kit %s) ascending: %s | the block\'s <h2>s %s (want [%d]) | its <h3>s %s' % (nums, K['flow_numbers_head'], nums == sorted(nums), h2s, NUM, ['%s.%s' % x for x in h3s]))
    cb = blocks[CHEAT]; cbt = '\n'.join(cb); ch = texts_head[CHEAT]
    h2c = re.findall(r'<h2>([^<]*)</h2>', cbt); pos = [ch.find(K['cheat_prev_h2']), ch.find(K['cheat_h2'])]
    bal = cbt.count('<div') == cbt.count('</div>'); wrapped = bool(cb) and cb[0].strip() == '<div class="section">'
    C.chk('D6a cheat h2 / order / balance', len(h2c) == 1 and h2c[0] == K['cheat_h2'] and not re.match(r'\s*\d+\.', h2c[0]) and -1 not in pos and pos == sorted(pos) and bal,
          'h2 %s (unnumbered, kit %r) | after KS-1333\'s: %s | <div> balanced (%d open / %d close): %s' % (h2c, K['cheat_h2'], -1 not in pos and pos == sorted(pos), cbt.count('<div'), cbt.count('</div>'), bal))
    C.chk('D6b cheat wrapped in a section', wrapped, 'wrapped in its own <div class="section"> like KS-1404 / KS-1333: %s (first line %r)' % (wrapped, cb[0].strip()[:50] if cb else ''))
    for d in DOCS:
        t = '\n'.join(blocks[d]); el = {'test file': 'ks1005' in t, 'how to run (npx vitest run)': 'npx vitest run' in t, '§5f / live sweep': bool(re.search(r'live sweep', t, re.I)) and ('&sect;5f' in t or '§5f' in t),
                                       'NOT covered note': bool(re.search(r'not covered', t, re.I))}
        for k, v in el.items():
            C.chk('D7 %s: %s' % ('flow' if d == FLOW else 'cheat', k), v, 'self-contained element present in the %s block: %s' % ('flow' if d == FLOW else 'cheat', v))
    bad = []
    for d in DOCS:
        for unit in re.split(r'(?=<tr>)|(?=<div class="note">)', '\n'.join(blocks[d])):
            if DUR.search(re.sub(r'<[^>]+>', '', unit)):
                plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', unit))
                if not (re.search(r'20\d\d-\d\d-\d\d', plain) and re.search(r'(?i)host|macOS|Mac Studio|\bCI\b', plain)) and 'projection' not in plain.lower():
                    bad.append('%s: %s' % (d.split('/')[-1][:12], plain.strip()[:140]))
    for b in bad: print('INFO D8 a duration with no date AND host in its own row: %s' % b)
    return bad


def prox(texts, needle_rx, win=120):
    n = 0
    for t in texts:
        for m in re.finditer(needle_rx, t):
            if DUR.search(t[max(0, m.start() - win):m.end() + win]): n += 1
    return n


def timing_statement(C, bad):
    a = [show(REPO, DEV, p) or '' for p in K['timing_sources']]; b = [show(REPO, DEV, p) or '' for p in (FLOW, CHEAT, K['skill'])]
    aa, ab = prox(a, r'services/auth'), prox(b, r'services/auth'); ca, cb = prox(a, r'Akto'), prox(b, r'Akto')
    C.chk('D8 stated timings', not bad and aa == 0 and ab == 0 and ca > 0 and cb > 0,
          'inserted rows with a duration and no date+host: %d | services/auth within 120 chars of a duration at develop: (a) CLAUDE.md+systemTest/CLAUDE.md+skill %d, (b) both docs+skill %d | must-hit CONTROL "Akto": (a) %d, (b) %d | the docs claim must-hit "3", the PR body "11"' % (len(bad), aa, ab, ca, cb))


print('c4_docs_gate59 %s %s | clone %s | develop %s | head %s' % (MODE or 'selftest', now(), REPO, DEV[:12], HEAD[:12]))
td = {d: show(REPO, DEV, d) for d in DOCS}; th = {d: show(REPO, HEAD, d) for d in DOCS}; tb = {d: show(REPO, BUILT, d) for d in DOCS}; tp = {d: show(REPO, BP, d) for d in DOCS}
SK = show(REPO, DEV, K['skill']); BPATHS = git(REPO, 'diff', '--name-only', BP, BUILT).splitlines(); PPATHS = git(REPO, 'diff', '--name-only', DEV, HEAD).splitlines()
if '--selftest' in A:
    OUT = guard_out(opt('--out') or '/tmp/g59_c4_selftest'); IDX = os.path.join(OUT, 'c4.index'); st = {'ok': 0, 'n': 0}
    def docs_arm(mut, d):
        t2 = dict(th); t2[d] = mut(t2[d]); return lambda C: judge_docs(C, td, t2, tb, tp, SK, BPATHS, PPATHS)
    def rep(old, new, count=1):
        def f(s):
            assert s.count(old) >= 1, 'plant anchor absent: %r' % old[:60]; return s.replace(old, new, count)
        return f
    def sub_arm(C, prefix, fn):
        C2 = Checks(); fn(C2)
        for tag, ok in C2.tags:
            if tag.startswith(prefix): C.chk(tag, ok, '(%s)' % prefix)
    Cb = Checks(True); judge_docs(Cb, td, th, tb, tp, SK, BPATHS, PPATHS); BASE = set(Cb.failed())
    print('SELFTEST BASELINE: the real head fails %s — an arm below counts only a NEW failure of its named check (a check already failing at the real head cannot prove an arm)' % (sorted(BASE) or 'NOTHING'))
    def narm(name, fn, want):
        def wrapped(C):
            C2 = Checks(True); fn(C2)
            for tag, ok in C2.tags: C.chk(tag, ok or tag in BASE, '(baseline-aware)')
        return selftest_arm(st, name, wrapped, want)
    narm('T0 the REAL head, baseline-aware (positive control)', lambda C: judge_docs(C, td, th, tb, tp, SK, BPATHS, PPATHS), None)
    narm('T1 a second block edited (KS-1333 line)', docs_arm(rep('<h2>12. GET /api/anchors/:id reports blockNumber as a number (KS-1333)</h2>', '<h2>12. GET /api/anchors/:id reports blockNumber as a NUMBER (KS-1333)</h2>'), FLOW), 'D3')
    narm('T2 19 renumbered 20', docs_arm(rep('<h2>19. change-password', '<h2>20. change-password'), FLOW), 'D4')
    narm('T3 one byte changed inside the block', docs_arm(rep('wholly non-functional', 'wholly non-functionaL'), FLOW), 'D5')
    narm('T4 the cheat h2 numbered', docs_arm(rep('<h2>change-password reads its own hash', '<h2>19. change-password reads its own hash'), CHEAT), 'D6a')
    narm('T5 the flow block loses its live-sweep line', docs_arm(rep('live sweep', 'sweep', -1), FLOW), 'D7 flow: \u00a75f')
    # Q-M arms on a SIM develop-after: #1381's merge-in tree squashed onto develop (commit-tree in YOUR clone; never a ref)
    M81 = K['reported_overlaps']['1381']['head']
    if has_commit(REPO, M81):
        sim_dev = wgit(REPO, 'commit-tree', tree(REPO, M81), '-p', DEV, '-m', 'SIM squash #1381 (gate59 c4 selftest)', env=ENV).strip()
        rc, ct, conf, msgs = merge_tree(sim_dev, HEAD)
        pred = resolve(sim_dev, ct, None, HEAD, DEV, IDX)
        print('INFO SIM develop-after %s (tree of #1381 merge-in %s on develop) | merge-tree x #1382 rc %d conflicts %s | predicted #1382 merge-in tree %s' % (sim_dev, M81[:12], rc, conf, pred))
        def mk(t, parents, msg='SIM merge develop into KS-1005'):
            a = []
            for p in parents: a += ['-p', p]
            return wgit(REPO, 'commit-tree', t, *a, '-m', msg, env=ENV).strip()
        e = {'GIT_INDEX_FILE': IDX}; wgit(REPO, 'read-tree', pred, env=e)
        bad_src = show(REPO, pred, K['product']) + '\n// sim extra edit\n'
        wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (wgit(REPO, 'hash-object', '-w', '--stdin', inp=bad_src).strip(), K['product']), env=e)
        bad_tree = wgit(REPO, 'write-tree', env=e).strip()
        wrong_tree = resolve(sim_dev, ct, None, HEAD, DEV, IDX, before_key='KS-1345')
        arms = [('Q0 the predicted merge-in (positive control)', mk(pred, [HEAD, sim_dev]), None),
                ('Q1 an extra users.ts edit', mk(bad_tree, [HEAD, sim_dev]), 'M1'),
                ('Q2 19 placed ABOVE 13', mk(wrong_tree, [HEAD, sim_dev]), 'M1'),
                ('Q3 a single-parent rewrite (a rebase)', mk(pred, [sim_dev]), 'M2'),
                ('Q4 a trailer on the merge-in', mk(pred, [HEAD, sim_dev], 'SIM merge\n\nCo-Authored-By: Sim <s@x>'), 'M4')]
        for name, M, want in arms:
            selftest_arm(st, name, lambda C, M=M: judge_qm(C, M, HEAD, DEV, sim_dev, IDX, 'SIM merge-in'), want)
        selftest_arm(st, 'Q5 the extra users.ts edit also fails M3', lambda C: judge_qm(C, arms[1][1], HEAD, DEV, sim_dev, IDX, 'SIM merge-in'), 'M3')
    else:
        print('SELFTEST NOTE: #1381 merge-in %s not in the clone: the Q-M arms were NOT RUN (fetch refs/pull/1381/head)' % M81[:12])
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
if MODE is None:
    print(__doc__); raise SystemExit(2)
C = Checks()
if MODE == 'docs':
    bad = judge_docs(C, td, th, tb, tp, SK, BPATHS, PPATHS); timing_statement(C, bad)
else:
    OUT = guard_out(opt('--out') or ''); IDX = os.path.join(OUT, 'c4.index')
    if MODE == 'predict':
        rc, ct, conf, msgs = merge_tree(DEV, BUILT)
        C.chk('M0 conflict set', rc == 1 and conf == sorted(DOCS), 'merge-tree develop x built rc %d | conflicted %s | verbatim %s' % (rc, conf, msgs))
        pred = resolve(DEV, ct, None, BUILT, BP, IDX); wrong = resolve(DEV, ct, None, BUILT, BP, IDX, before_key='KS-1333'); ht = tree(REPO, HEAD)
        C.chk('M1 tree == prediction', pred == K['end_tree'] == ht and wrong != pred, 'prediction %s | kit END_TREE %s | head tree %s | CONTROL 19 above 12 -> %s differs: %s' % (pred, K['end_tree'], ht, wrong[:12], wrong != pred))
        par = git(REPO, 'log', '-1', '--format=%P', HEAD).split()
        C.chk('M2 two parents', par == [BUILT, DEV], 'parents %s (want [built %s, develop %s])' % ([p[:12] for p in par], BUILT[:12], DEV[:12]))
        rd = sorted(set(l for l in git(REPO, 'show', '--remerge-diff', '--format=', '--name-only', HEAD).split('\n') if l.strip()))
        C.chk('M3 remerge-diff only the docs', rd == sorted(DOCS), 'git show --remerge-diff %s touches %s' % (HEAD[:12], rd))
        t = git(REPO, 'log', '-1', '--format=%(trailers)', HEAD).strip()
        C.chk('M4 no trailer', t == '', 'trailers %r' % t)
    elif MODE == 'qm':
        M, D = opt('--merge-in-head'), opt('--develop-after')
        if not (M and D and has_commit(REPO, M) and has_commit(REPO, D)):
            print('REFUSING: qm needs --merge-in-head and --develop-after, both commits in the clone'); raise SystemExit(2)
        judge_qm(C, M, HEAD, DEV, D, IDX, 'merge-in %s' % M[:12])
        rc, _, _ = git(REPO, 'merge-base', '--is-ancestor', DEV, D, check=False)
        C.chk('M5 develop moved forward', rc == 0, 'kit develop %s is an ancestor of %s: %s' % (DEV[:12], D[:12], rc == 0))
n = C.nfail()
print('C4 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
