#!/usr/bin/env python3
"""c4_docs_gate61.py — gate61 C4 for #1383 (KS-1401): the §4 doc blocks `22.`, the merge-in PREDICTION over a develop that moved (#1381
block 13. merges FIRST; #1382 block 19. may follow), and Q-M for a LATER merge-in head. Git objects only, in YOUR scratch clone; the only
writes are commit-tree / merge-tree / hash-object / a temp index under --out (lib wgit refuses any repo under /Volumes/DevMASTER; never a
ref is written).
MODES
  docs  --repo <clone> [--head sha]
    D1 §4 at develop: the skill blob carries "Every test change updates its platform's two HTML docs, in the same commit" + both paths.
    D2 SAME COMMIT: the head commit carries the suite, 049 and BOTH platform-k docs; 0 platform-s docs.
    D3a ONE BLOCK per doc, develop -> head: the only hunk sits at develop's `  </body>` line; kit block_lines inserted; no other line of
        develop is deleted or replaced (no other block edited).
    D3b CLOSE TAG UNTOUCHED: develop's `  </body>` survives byte-for-byte. The drafter's read FAILS this on BOTH docs: the head rewrites
        `  </body>` (2-space indent) as `</body>` — an edit to an existing line that every co-tenant's block anchors on (README D2).
    D4 FLOW NUMBERS: head <h2> numbers == kit flow_numbers_head [1..12, 22], ascending; the block's only <h2> is `22.`; its <h3>s 22.x.
    D5 NOTHING RENUMBERED: every develop <h2> line is present at head, byte-identical, in the same order.
    D6a CHEAT ORDER: exactly one <h2> in the cheat block, after KS-1333's, <div> balanced.
    D6b CHEAT CONVENTION: unnumbered `<h2>… &mdash; KS-n</h2>` wrapped in its own `<div class="section">` like KS-1404 / KS-1333 (and
        #1381's KS-1345). The drafter's read FAILS this (numbered `22.`, unwrapped, key first): README D5.
    D7 SELF-CONTAINED per doc: names the suite path, how to run it, the §5f live sweep owed, and a NOT-covered note. The drafter's read FAILS
        the cheat block on the live sweep and the NOT-covered note (README D5).
    D8 STATED TIMINGS: every inserted <p>/<tr> carrying a duration also carries a date AND a host (or says "projection"); config values
        (`lock_timeout`, `5 s` beside it) are not timings and are skipped BY NAME, each skip printed.
    D9 THE "NO STATED TIMING" STATEMENT re-measured at develop: both docs carry 0 hits of kit timing_grep.keys_rx, beside the must-hit
       CONTROL `Schemathesis` (> 0); the docs claim 54 — printed beside the measured occurrence AND line counts.
  predict --repo <clone> --out <dir> --develop-after <D> [--anchor carry|keep]
    M0 `merge-tree --write-tree --name-only D head` -> rc 1 on EXACTLY the two docs (or rc 0, nothing conflicted).
    M1 an INDEPENDENT number-order resolution: D's doc with #1383's own block placed before the first flow <h2> numbered > 22 (else before
       the close tag), the cheat by the same keys' flow numbers; the close tag per --anchor (carry = #1383's `</body>`, the 3-way union;
       keep = D's `  </body>`). Prints the predicted tree for BOTH anchors. CONTROL: 22 placed ABOVE the highest block below it -> differs.
  qm --repo --out --merge-in-head <M> --develop-after <D> [--anchor carry]   (Q-M, kit q_m, M1-M7)
    M0/M1 as predict, M (the merge-in) tree == the prediction; M2 parents == [kit head, D]; M3 `git show --remerge-diff M` touches ONLY the
    two docs; M4 0 trailers; M5 kit develop is an ancestor of D; M6 develop's advance kit develop..D touches NONE of kit qm_disjoint_prefixes
    nor kit writer_files (each hit named); M7 `rev-list M ^head ^D` == [M] (one new commit).
  --selftest --repo --out   docs arms on planted doc copies (BASELINE-aware: a check already failing at the real head cannot prove an
            arm) and Q-M arms on a SIM develop-after (#1381's merge-in tree squashed onto develop by commit-tree, never a ref).
Usage: c4_docs_gate61.py docs|predict|qm --repo <clone> [--out dir] [--develop-after D] [--merge-in-head M] [--anchor carry|keep]
       | --selftest --repo --out          rc 0 PASS / 1 FAIL / 2 usage. Prints `CHECKED <n>`; 0 checked is a FAIL."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, git, wgit, now, Checks, opt_factory, show, has_commit, opcodes, guard_scratch, guard_out, tree, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = guard_scratch(opt('--repo'), 'clone'); HEAD = opt('--head', K['head']); DEV = K['develop']
DOCS = K['docs']; FLOW, CHEAT = DOCS; AD, AH = K['doc_close_anchor_develop'], K['doc_close_anchor_head']; NUM = K['flow_block_number']
MODE = next((m for m in ('docs', 'predict', 'qm') if m in A), None)
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
ENV = {'GIT_AUTHOR_NAME': 'g61', 'GIT_AUTHOR_EMAIL': 'g61@sim', 'GIT_COMMITTER_NAME': 'g61', 'GIT_COMMITTER_EMAIL': 'g61@sim',
       'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}
DUR = re.compile(r'\b\d+(?:[.,]\d+)?(?:\s|&nbsp;)?(?:ms|s|sec|secs|seconds|min|mins|minutes|h|hours)\b', re.I)
CLOSE = re.compile(r'^\s*</body>\s*$')


def block_of(dev_txt, head_txt):
    """#1383's own block: (index in develop, block lines WITHOUT the close tag, the close-tag line at head, every op) or None"""
    d, h = dev_txt.split('\n'), head_txt.split('\n'); ops = opcodes(d, h)
    if len(ops) != 1: return None, ops
    tag, i1, i2, j1, j2 = ops[0]; new = h[j1:j2]
    if tag == 'insert': return (i1, new, None), ops
    if tag == 'replace' and i2 - i1 == 1 and CLOSE.match(d[i1]) and new and CLOSE.match(new[-1]): return (i1, new[:-1], new[-1]), ops
    return None, ops


def flow_map(flow_txt):
    return {m.group(2): int(m.group(1)) for m in re.finditer(r'<h2>(\d+)\.[^\n]*?\((KS-\d+)[,)]', flow_txt)}


def place(d, doc_txt, block, close_line, flow_txt, anchor='carry', above_key=None):
    ls = doc_txt.split('\n'); fm = flow_map(flow_txt)
    ci = [i for i, l in enumerate(ls) if CLOSE.match(l)]
    if len(ci) != 1: raise SystemExit('REFUSING: the close tag is not exactly once in %s (%d)' % (d, len(ci)))
    def start_of(i): return i - 1 if i > 0 and ls[i - 1].strip() == '<div class="section">' else i
    at = None
    for i, l in enumerate(ls):
        if d == FLOW:
            m = re.match(r'\s*<h2>(\d+)\.[^\n]*?\((KS-\d+)', l)
            if m and ((above_key and m.group(2) == above_key) or (not above_key and int(m.group(1)) > NUM)): at = i; break
        else:
            m = re.search(r'<h2>[^<]*\b(KS-\d+)\b[^<]*</h2>', l)
            if m and ((above_key and m.group(1) == above_key) or (not above_key and fm.get(m.group(1), 0) > NUM)): at = start_of(i); break
    at = ci[0] if at is None else at
    if anchor == 'carry' and close_line is not None: ls[ci[0]] = close_line
    return '\n'.join(ls[:at] + block + ls[at:])


def resolve(base_rev, conflicted_tree, idx, anchor='carry', above_key=None, blocks=None):
    e = {'GIT_INDEX_FILE': idx}; wgit(REPO, 'read-tree', conflicted_tree, env=e); fl = show(REPO, base_rev, FLOW)
    for d in DOCS:
        bl, ops = blocks[d] if blocks else block_of(show(REPO, DEV, d), show(REPO, HEAD, d))
        if bl is None: raise SystemExit('REFUSING: #1383\'s change to %s is not one block (%s)' % (d, [o[0] for o in ops]))
        txt = place(d, show(REPO, base_rev, d), bl[1], bl[2], fl, anchor, above_key)
        sha = wgit(REPO, 'hash-object', '-w', '--stdin', inp=txt).strip()
        wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (sha, d), env=e)
    return wgit(REPO, 'write-tree', env=e).strip()


def merge_tree(a, b):
    rc, o, e = wgit(REPO, 'merge-tree', '--write-tree', '--name-only', a, b, check=False)
    ls = o.split('\n'); ct = ls[0].strip(); conf = sorted(set(l for l in ls[1:] if l and not l.startswith(('Auto-merging', 'CONFLICT'))))
    return rc, ct, conf, [l for l in ls if l.startswith('CONFLICT')]


def predict(C, D, idx, anchor):
    rc, ct, conf, msgs = merge_tree(D, HEAD)
    C.chk('M0 conflict set', (rc == 1 and conf == sorted(DOCS)) or (rc == 0 and not conf), 'merge-tree %s x %s rc %d | conflicted %s (want EXACTLY the two docs, or clean) | verbatim %s' % (D[:12], HEAD[:12], rc, conf, msgs))
    if rc != 1: return ct, ct, None
    fm = flow_map(show(REPO, D, FLOW)); below = sorted((n, k) for k, n in fm.items() if n < NUM)
    wk = below[-1][1] if below else 'KS-1333'
    pred = resolve(D, ct, idx, anchor); other = resolve(D, ct, idx, 'keep' if anchor == 'carry' else 'carry'); wrong = resolve(D, ct, idx, anchor, above_key=wk)
    print('INFO prediction on %s: anchor=%s %s | the other anchor %s | CONTROL 22 placed above %s -> %s (differs: %s)' % (D[:12], anchor, pred, other, wk, wrong, wrong != pred))
    for d in DOCS:
        t = show(REPO, pred, d); hs = re.findall(r'<h2>([^<]{0,60})', t)
        print('INFO   %s block order (last 4 <h2>): %s | close tag %r' % (d.split('/')[-1][:24], hs[-4:], next((l for l in t.split('\n') if CLOSE.match(l)), None)))
    return pred, other, wrong


def judge_qm(C, M, D, idx, anchor):
    pred, other, wrong = predict(C, D, idx, anchor); mt = tree(REPO, M)
    C.chk('M1 tree == prediction', mt == pred and wrong != pred, 'merge-in %s tree %s | prediction (%s) %s | the other anchor %s%s | CONTROL wrong order differs: %s' % (
        M[:12], mt, anchor, pred, (other or '')[:12], ' (== the merge-in: rule the close tag)' if mt == other and mt != pred else '', wrong != pred))
    par = git(REPO, 'log', '-1', '--format=%P', M).split()
    C.chk('M2 two parents', par == [HEAD, D], 'parents %s (want [gated head %s, develop %s])' % ([p[:12] for p in par], HEAD[:12], D[:12]))
    rd = sorted(set(l for l in git(REPO, 'show', '--remerge-diff', '--format=', '--name-only', M).split('\n') if l.strip()))
    C.chk('M3 remerge-diff only the docs', rd and set(rd) <= set(DOCS), 'git show --remerge-diff %s touches %s' % (M[:12], rd or 'NOTHING'))
    t = git(REPO, 'log', '-1', '--format=%(trailers)', M).strip()
    C.chk('M4 no trailer', t == '', 'trailers %r' % t)
    rc, _, _ = git(REPO, 'merge-base', '--is-ancestor', DEV, D, check=False)
    C.chk('M5 develop moved forward', rc == 0, 'kit develop %s ancestor of %s: %s' % (DEV[:12], D[:12], rc == 0))
    adv = [l for l in git(REPO, 'diff', '--name-only', DEV, D).split('\n') if l.strip()]
    hits = [p for p in adv if any(p.startswith(x) for x in K['qm_disjoint_prefixes']) or p in K['writer_files']]
    C.chk('M6 develop advance path-disjoint', not hits, 'develop %s..%s changed %d path(s) | touching migrations/ / ks1401* / docker/init/ / a charge_events writer: %s' % (DEV[:12], D[:12], len(adv), hits or 'NONE'))
    new = [l for l in git(REPO, 'rev-list', M, '^' + HEAD, '^' + D).split('\n') if l.strip()]
    C.chk('M7 one new commit', new == [M], 'rev-list %s ^head ^develop -> %s' % (M[:12], [x[:12] for x in new]))


def judge_docs(C, td, th, skill, pr_paths):
    s4 = "Every test change updates its platform's two HTML docs, in the same commit"
    C.chk('D1 §4 at develop', s4 in ' '.join(skill.split()) and all(d in skill for d in DOCS), 'skill carries the §4 sentence: %s | both platform-k paths: %s' % (s4 in ' '.join(skill.split()), all(d in skill for d in DOCS)))
    need = set(DOCS) | {K['test'], K['migration']}
    C.chk('D2 same commit', need <= set(pr_paths) and not (set(K['platform_s_docs']) & set(pr_paths)), 'head commit paths %d, carries suite + 049 + both docs: %s | platform-s docs: %s' % (
        len(pr_paths), need <= set(pr_paths), sorted(set(K['platform_s_docs']) & set(pr_paths)) or 'NONE'))
    blocks = {}
    for d in DOCS:
        nm = d.split('/')[-1][:24]; bl, ops = block_of(td[d], th[d]); dl = td[d].split('\n'); ci = [i for i, l in enumerate(dl) if l == AD]
        C.chk('D3a one block (%s)' % nm, bl is not None and len(bl[1]) == K['block_lines'][d] and ci == [bl[0]], 'ops develop->head %s | block %s line(s) (kit %d) at develop line %s; `%s` at %s' % (
            [o[0] for o in ops][:6], len(bl[1]) if bl else '-', K['block_lines'][d], bl[0] + 1 if bl else '-', AD, [c + 1 for c in ci]))
        C.chk('D3b close tag untouched (%s)' % nm, bl is not None and bl[2] is None, 'develop %r -> head %r (an edit to an existing line every co-tenant anchors on)' % (AD, bl[2] if bl and bl[2] is not None else AD))
        blocks[d] = bl[1] if bl else []
    fh = th[FLOW]; nums = [int(m) for m in re.findall(r'(?m)^\s*<h2>(\d+)\.', fh)]; fb = '\n'.join(blocks[FLOW])
    h2s = re.findall(r'<h2>(\d+)\.', fb); h3s = re.findall(r'<h3>(\d+)\.(\d+)', fb)
    C.chk('D4 flow numbers', nums == K['flow_numbers_head'] and nums == sorted(nums) and h2s == [str(NUM)] and h3s and all(a == str(NUM) for a, b in h3s),
          'head <h2> numbers %s (kit %s) ascending %s | block <h2>s %s | <h3>s %s' % (nums, K['flow_numbers_head'], nums == sorted(nums), h2s, ['%s.%s' % x for x in h3s]))
    for d in DOCS:
        dh = [l for l in td[d].split('\n') if '<h2>' in l]; hh = [l for l in th[d].split('\n') if '<h2>' in l]
        C.chk('D5 nothing renumbered (%s)' % d.split('/')[-1][:24], hh[:len(dh)] == dh, 'develop <h2> lines %d, the first %d at head byte-identical in order: %s' % (len(dh), len(dh), hh[:len(dh)] == dh))
    cb = blocks[CHEAT]; cbt = '\n'.join(cb); ch = th[CHEAT]; h2c = re.findall(r'<h2>([^<]*)</h2>', cbt)
    pos = [ch.find(K['cheat_prev_h2']), ch.find(K['cheat_h2'])]; bal = cbt.count('<div') == cbt.count('</div>')
    C.chk('D6a cheat order', len(h2c) == 1 and -1 not in pos and pos == sorted(pos) and bal, 'h2 %s | after KS-1333\'s: %s | <div> %d open / %d close' % (h2c, -1 not in pos and pos == sorted(pos), cbt.count('<div'), cbt.count('</div>')))
    conv = {'unnumbered': bool(h2c) and not re.match(r'\s*\d+\.', h2c[0]), 'ends `&mdash; KS-n`': bool(h2c) and re.search(r'&mdash; KS-\d+\s*$', h2c[0]) is not None,
            'wrapped in <div class="section">': bool(cb) and cb[0].strip() == '<div class="section">'}
    C.chk('D6b cheat convention', all(conv.values()), ' | '.join('%s: %s' % kv for kv in conv.items()))
    for d in DOCS:
        t = '\n'.join(blocks[d]); w = 'flow' if d == FLOW else 'cheat'
        el = {'suite path': 'ks1401_049_tenant_isolation_after_039.test.sh' in t, 'how to run (bash …ks1401)': bool(re.search(r'bash\s+Blockchain/Dev/scripts/__tests__/ks1401', t)),
              '§5f / live sweep': bool(re.search(r'live sweep|&sect;5f|§5f|not move to Done|offline green', t, re.I)), 'NOT covered note': bool(re.search(r'not covered', t, re.I))}
        for k, v in el.items():
            C.chk('D7 %s: %s' % (w, k), v, 'present in the %s block: %s' % (w, v))
    bad = []; skipped = []
    for d in DOCS:
        for unit in re.split(r'(?=<p>)|(?=<tr>)|(?=<div class="note">)', '\n'.join(blocks[d])):
            plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', unit)).replace('&nbsp;', ' ').replace('&ndash;', '-')
            durs = [m for m in DUR.finditer(plain)]
            real = [m for m in durs if not re.search(r'lock_timeout', plain[max(0, m.start() - 60):m.end() + 60])]
            for m in durs:
                if m not in real: skipped.append('%s: %r (beside lock_timeout: a config value)' % (d.split('/')[-1][:10], plain[max(0, m.start() - 30):m.end() + 10]))
            if real and not (re.search(r'20\d\d-\d\d-\d\d', plain) and re.search(r'(?i)host|Mac-Studio|Mac Studio|\bCI\b', plain)) and 'projection' not in plain.lower():
                bad.append('%s: %s' % (d.split('/')[-1][:10], plain.strip()[:150]))
    for s in skipped: print('INFO D8 skipped %s' % s)
    for b in bad: print('INFO D8 a duration with no date AND host in its own unit: %s' % b)
    C.chk('D8 stated timings', not bad, '%d inserted unit(s) carry a duration without a date and a host; %d config value(s) skipped by name' % (len(bad), len(skipped)))


def timing_statement(C):
    tg = K['timing_grep']; td_ = [show(REPO, DEV, d) or '' for d in DOCS]
    keys = sum(len(re.findall(tg['keys_rx'], t)) for t in td_); occ = sum(len(re.findall(tg['control_rx'], t)) for t in td_)
    lines = sum(sum(1 for l in t.split('\n') if re.search(tg['control_rx'], l)) for t in td_)
    var = {}
    for nm, t in zip(('flow', 'cheat'), td_):
        for ci, fl in (('case', 0), ('-i', re.I)):
            var['%s lines %s' % (nm, ci)] = sum(1 for l in t.split('\n') if re.search(tg['control_rx'], l, fl))
            var['%s occurrences %s' % (nm, ci)] = len(re.findall(tg['control_rx'], t, fl))
    for ci, fl in (('case', 0), ('-i', re.I)):
        var['both lines %s' % ci] = sum(sum(1 for l in t.split('\n') if re.search(tg['control_rx'], l, fl)) for t in td_)
    repro = sorted(k for k, v in var.items() if v == tg['control_claimed'])
    C.chk('D9 no-stated-timing statement', keys == 0 and occ > 0, 'at develop %s: %r hits %d across BOTH docs (want 0) | must-hit CONTROL %r across both: occurrences %d, lines %d | the docs claim %d: reproduced ONLY by %s (the zero is claimed over both docs: rule the scope)' % (
        DEV[:12], tg['keys_rx'], keys, tg['control_rx'], occ, lines, tg['control_claimed'], repro or 'NO VARIANT'))
    print('INFO D9 control variants %s' % var)


print('c4_docs_gate61 %s %s | clone %s | develop %s | head %s' % (MODE or 'selftest', now(), REPO, DEV[:12], HEAD[:12]))
td = {d: show(REPO, DEV, d) for d in DOCS}; th = {d: show(REPO, HEAD, d) for d in DOCS}; SK = show(REPO, DEV, K['skill'])
PPATHS = [l for l in git(REPO, 'diff', '--name-only', DEV, HEAD).splitlines() if l.strip()]
if '--selftest' in A:
    OUT = guard_out(opt('--out') or '/tmp/g61_c4_selftest'); IDX = os.path.join(OUT, 'c4.index'); st = {'ok': 0, 'n': 0}
    Cb = Checks(True); judge_docs(Cb, td, th, SK, PPATHS); BASE = set(Cb.failed())
    print('SELFTEST BASELINE: the real head fails %s — an arm counts only a NEW failure of its named check' % (sorted(BASE) or 'NOTHING'))
    def narm(name, fn, want):
        def wrapped(C):
            C2 = Checks(True); fn(C2)
            for tag, ok in C2.tags: C.chk(tag, ok or tag in BASE, '(baseline-aware)')
        return selftest_arm(st, name, wrapped, want)
    def docs_arm(mut, d):
        t2 = dict(th); t2[d] = mut(t2[d]); return lambda C: judge_docs(C, td, t2, SK, PPATHS)
    def rep(old, new, count=1):
        def f(s):
            assert s.count(old) >= 1, 'plant anchor absent: %r' % old[:60]; return s.replace(old, new, count)
        return f
    narm('T0 the REAL head, baseline-aware (positive control)', lambda C: judge_docs(C, td, th, SK, PPATHS), None)
    narm('T1 a second block edited (KS-1333 h2)', docs_arm(rep('reports blockNumber as a number (KS-1333)</h2>', 'reports blockNumber as a NUMBER (KS-1333)</h2>'), FLOW), 'D3a')
    narm('T2 22 renumbered 23', docs_arm(rep('<h2>22. Migration 049', '<h2>23. Migration 049'), FLOW), 'D4')
    narm('T3 the cheat block loses its h2', docs_arm(rep(K['cheat_h2'], '<p>no heading</p>'), CHEAT), 'D6a')
    narm('T4 the flow block loses its suite path', docs_arm(rep('ks1401_049_tenant_isolation_after_039.test.sh', 'the suite', -1), FLOW), 'D7 flow')
    narm('T5 the flow timing row loses its host', docs_arm(rep('three consecutive runs, 2026-10-05, host <code>Kamils-Mac-Studio</code>', 'three consecutive runs'), FLOW), 'D8')
    narm('T6 an earlier block renumbered (12 -> 14)', docs_arm(rep('<h2>12. GET /api/anchors', '<h2>14. GET /api/anchors'), FLOW), 'D5')
    # the D3b check fires on the REAL head; its POSITIVE control is a SIM head whose close tag is untouched
    def fixed(d): return th[d].replace('\n' + AH + '\n', '\n' + AD + '\n', 1)
    t2 = {d: fixed(d) for d in DOCS}
    selftest_arm(st, 'T7 D3b positive control: the same blocks with `  </body>` kept PASS D3a/D3b', lambda C: [C.chk(t, ok, '') for t, ok in (lambda C2: (judge_docs(C2, td, t2, SK, PPATHS), C2.tags)[1])(Checks(True)) if t.startswith('D3')], None)
    # Q-M arms on a SIM develop-after = #1381's merge-in tree squashed onto develop (commit-tree in YOUR clone; never a ref)
    M81 = K['reported_overlaps']['1381']['head']
    if has_commit(REPO, M81):
        def mk(t, parents, msg='SIM merge develop into KS-1401'):
            a = []
            for p in parents: a += ['-p', p]
            return wgit(REPO, 'commit-tree', t, *a, '-m', msg, env=ENV).strip()
        sim_dev = mk(tree(REPO, M81), [DEV], 'SIM squash #1381 (gate61 c4 selftest)')
        Cp = Checks(True); pred, other, wrong = predict(Cp, sim_dev, IDX, 'carry')
        print('INFO SIM develop-after %s (#1381 merge-in tree %s on develop) | PREDICTED #1383 merge-in tree carry %s / keep %s' % (sim_dev[:12], M81[:12], pred, other))
        e = {'GIT_INDEX_FILE': IDX}; wgit(REPO, 'read-tree', pred, env=e)
        bad_src = show(REPO, pred, K['migration_039']) + '\n-- sim extra edit\n'
        wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (wgit(REPO, 'hash-object', '-w', '--stdin', inp=bad_src).strip(), K['migration_039']), env=e)
        bad_tree = wgit(REPO, 'write-tree', env=e).strip()
        e2 = {'GIT_INDEX_FILE': IDX}; wgit(REPO, 'read-tree', tree(REPO, sim_dev), env=e2)
        wgit(REPO, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (wgit(REPO, 'hash-object', '-w', '--stdin', inp='SELECT 1;\n').strip(), 'Blockchain/Dev/migrations/050_sim.sql'), env=e2)
        sim_dev2 = mk(wgit(REPO, 'write-tree', env=e2).strip(), [sim_dev], 'SIM a later develop adds migration 050')
        Cp2 = Checks(True); pred2, _, _ = predict(Cp2, sim_dev2, IDX, 'carry')
        mid = mk(tree(REPO, HEAD), [HEAD], 'SIM an extra commit on the branch')
        arms = [('Q0 the predicted merge-in, carry (positive control)', mk(pred, [HEAD, sim_dev]), sim_dev, 'carry', None),
                ('Q0b the keep-anchor merge-in judged with --anchor keep (positive control)', mk(other, [HEAD, sim_dev]), sim_dev, 'keep', None),
                ('Q1 an extra 039 edit in the merge-in', mk(bad_tree, [HEAD, sim_dev]), sim_dev, 'carry', 'M1'),
                ('Q2 22 placed ABOVE 13', mk(wrong, [HEAD, sim_dev]), sim_dev, 'carry', 'M1'),
                ('Q3 a single-parent rewrite (a rebase)', mk(pred, [sim_dev]), sim_dev, 'carry', 'M2'),
                ('Q4 a trailer on the merge-in', mk(pred, [HEAD, sim_dev], 'SIM merge\n\nCo-Authored-By: Sim <s@x>'), sim_dev, 'carry', 'M4'),
                ('Q5 develop advanced into migrations/ (050)', mk(pred2, [HEAD, sim_dev2]), sim_dev2, 'carry', 'M6'),
                ('Q6 two new commits (an extra branch commit)', mk(pred, [mid, sim_dev]), sim_dev, 'carry', 'M7'),
                ('Q7 the keep-anchor merge-in judged with the default carry', mk(other, [HEAD, sim_dev]), sim_dev, 'carry', 'M1')]
        for name, M, D, anc, want in arms:
            selftest_arm(st, name, lambda C, M=M, D=D, anc=anc: judge_qm(C, M, D, IDX, anc), want)
        selftest_arm(st, 'Q8 the extra 039 edit also fails M3', lambda C: judge_qm(C, arms[2][1], sim_dev, IDX, 'carry'), 'M3')
    else:
        print('SELFTEST NOTE: #1381 merge-in %s not in the clone: the Q-M arms were NOT RUN (fetch refs/pull/1381/head)' % M81[:12])
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)
if MODE is None:
    print(__doc__); raise SystemExit(2)
C = Checks(); ANC = opt('--anchor', 'carry')
if MODE == 'docs':
    judge_docs(C, td, th, SK, PPATHS); timing_statement(C)
else:
    OUT = guard_out(opt('--out') or ''); IDX = os.path.join(OUT, 'c4.index'); D = opt('--develop-after')
    if not D or not has_commit(REPO, D): print('REFUSING: --develop-after <commit in the clone> is required'); raise SystemExit(2)
    if MODE == 'predict':
        pred, other, wrong = predict(C, D, IDX, ANC)
        print('PREDICTED merge-in tree of #1383 over %s: %s (anchor %s); other anchor %s' % (D[:12], pred, ANC, other))
    else:
        M = opt('--merge-in-head')
        if not M or not has_commit(REPO, M): print('REFUSING: --merge-in-head <commit in the clone> is required'); raise SystemExit(2)
        judge_qm(C, M, D, IDX, ANC)
n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C4 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 and C.res else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n or not C.res else 0)
