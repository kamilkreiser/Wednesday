#!/usr/bin/env python3
"""c4_docs_gate60.py — gate60 C4 for #1384 (KS-1210): the §4 doc blocks (block 18.), the CHAINED merge predictions after #1381 (block 13.)
and #1382 (block 19.) — both ruled to land FIRST — and the Q-M judge for the LATER merge-in head. Git objects only, in YOUR scratch clone;
the only writes are commit-tree / merge-tree / hash-object / a temp index under --out (lib wgit refuses any repo under /Volumes/DevMASTER;
never a ref).
MODES
  docs  --repo <clone> [--head sha] [--body-file f]
    D1 §4 at develop: the skill blob carries "Every test change updates its platform's two HTML docs, in the same commit" + both paths.
    D2 SAME COMMIT: the head commit (single parent == develop) carries the test, routes/oauth.ts and BOTH platform-k docs; 0 platform-s docs.
    D3 ONE PURE INSERT per doc, develop -> head: kit block_lines (84 / 36) inserted immediately before `  </body>`, 0 other lines touched.
    D4 FLOW NUMBERS: head <h2> numbers == [1..12, 18], ascending; the block's only <h2> is `18.`; its <h3>s are 18.x.
    D5 PRESENT ONCE: each block appears exactly once in the head doc and 0 times at develop.
    D6a CHEAT: one unnumbered <h2> == kit cheat_h2, after KS-1333's; <div> balanced.   D6b wrapped in its own <div class="section">.
    D7 SELF-CONTAINED per doc: names the ks1210 test file, `npx vitest run`, the §5f live sweep owed, and a NOT-covered note.
    D8 STATED TIMINGS: every inserted row / paragraph carrying a duration (`5000 ms`, `5000&nbsp;ms`, `1.05 s` …) also carries a date AND a
       host in the SAME unit, or says "projection"; offenders printed.  D8b the §4 timing statement re-measured at develop on the PR's own
       set (flow + cheat + skill) with the PR body's OWN regex: `services/auth` mentions near a duration (120 chars) == 0; must-hit CONTROL
       `Akto` near a duration > 0; the mention counts printed beside the body's claims (7 / 134 / 11).
    D9 FIGURES vs THE PR BODY: the docs' suite figure ("864 passed, 0 failed", "did not recur") against the PR body's Test Evidence at the
       SAME head ("862 passed, 2 failed" on run 1) — a doc that says the ks949 reds did not recur while the body reports them at this head
       FAILS (README doubt D6: whose run the doc reports, and whether a doc may carry the green reading only).
  predict --repo <clone> --out <dir>
    MP0 merge-tree develop x head -> rc 0, tree == kit END_TREE (the control: a no-op merge reproduces the head's own tree).
    MP1 vs #1381's head: rc 1 on EXACTLY the two docs; an INDEPENDENT number-order resolution (13. above 18.) -> a tree; CONTROL 18 above 13
        gives a different tree. INFO: the READY's "predicted tree" 299fd1c2de24 is compared with merge-tree's CONFLICTED toplevel tree (it
        IS that tree, conflict markers and all — measured by the drafter) and with the resolution (it is not).
    MP2 vs #1382's head: same, 18. above 19.; the READY's 7904aab89f15 likewise; CONTROL 18 below 19 differs.
    MP4 vs #1383's head (KS-1401, block 22.; NOT named by the READY — found by the census): same, 18. above 22.
    MP5 vs #1385's head (KS-938, block 20., Seat E 3rd's own row 2, raised after the READY): same, 18. above 20.
    MP3 CHAINED (the ruled order #1381 -> #1382 -> #1384): SIM develop1 = #1381's tree on develop, SIM develop2 = #1382's merge-in resolved
        on develop1 (cross-check: == gate59's SIM prediction df1344507d8c), then #1384's merge-in predicted on develop2 — printed as the
        drafter's prediction; valid ONLY if both land as those trees, squashed. Recompute with `qm` on the REAL develop.
  qm --repo --out --merge-in-head <M> --develop-after <D>   (the LATER merge-in of #1384 — the Q-M rule, kit q_m)
    M0 merge-tree D x gated head: rc 1 on EXACTLY the two docs, or rc 0 (clean);  M1 tree == the prediction recomputed on D (or the clean
    merge tree); CONTROL wrong order differs;  M2 parents == [gated head, D];  M3 remerge-diff touches only the two docs (EMPTY accepted for a
    clean merge — gate59's kit note fixed);  M4 0 trailers;  M5 D descends from kit develop;  M6 `rev-list --count M --not <gated> D` == 1;
    M7 Q-M+(c): develop..D is PATH-DISJOINT from oauth.ts, services/oauth.ts, authenticate.ts, the ks1210/ks431/ks451 tests, and the two
    users.ts role-list declaration lines are byte-identical at D (the drift cells read them).
  --selftest --repo --out   docs: the real head PASSES the structural checks (baseline-aware) and planted copies FAIL — a second block
            edited (D3), 18 renumbered 17 (D4), the block duplicated (D5), the cheat h2 numbered (D6a), the flow live-sweep removed (D7).
            Q-M on SIM develop-afters: the predicted merge-in PASSES; an extra oauth.ts edit (M1+M3), 18 below 19 (M1), a single-parent rewrite
            (M2), a trailer (M4), and a develop advance touching routes/oauth.ts (M7) each FAIL their named check.
Usage: c4_docs_gate60.py docs|predict|qm --repo <clone> [--out dir] [--head sha] [--body-file f] [--merge-in-head M --develop-after D]
       | --selftest --repo --out           rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate60 import K, git, wgit, now, Checks, opt_factory, show, has_commit, opcodes, guard_scratch, guard_out, tree, selftest_arm, GH

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = guard_scratch(opt('--repo'), 'clone'); HEAD = opt('--head', K['head'])
DEV = K['develop']; DOCS = K['docs']; FLOW, CHEAT = DOCS; ANCH = K['doc_close_anchor']; NUM = K['flow_block_number']
O81, O82, O83, O85 = K['reported_overlaps']['1381'], K['reported_overlaps']['1382'], K['reported_overlaps'].get('1383'), K['reported_overlaps'].get('1385')
MODE = next((m for m in ('docs', 'predict', 'qm') if m in A), None)
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
ENV = {'GIT_AUTHOR_NAME': 'g60', 'GIT_AUTHOR_EMAIL': 'g60@sim', 'GIT_COMMITTER_NAME': 'g60', 'GIT_COMMITTER_EMAIL': 'g60@sim',
       'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}
# a bare `s` / `h` unit needs a separator, so `404s` (plural status codes) is not a duration — the drafter's first run flagged it (c4_docs_ex1)
DUR = re.compile(r'\b\d+(?:[.,]\d+)?(?:(?:\s|&nbsp;)?(?:ms|sec|secs|seconds|min|mins|minutes|hours)|(?:\s|&nbsp;)(?:s|h))\b', re.I)
PR_RX = re.compile(r'\b\d+(?:\.\d+)?\s*(ms|s|sec|secs|seconds|m|min|mins|minutes|h|hr|hours)\b')   # the PR body's own printed regex
Q_PATHS = [K['product'], K['service'], K['authenticate'], K['test']] + K['sibling_tests']


def insert_block(base_txt, new_txt):
    b, n = base_txt.split('\n'), new_txt.split('\n'); ops = opcodes(b, n)
    if len(ops) != 1 or ops[0][0] != 'insert': return None
    return ops[0][1], n[ops[0][3]:ops[0][4]]


def flow_map(flow_txt):
    return {m.group(2): int(m.group(1)) for m in re.finditer(r'<h2>(\d+)\.[^\n]*\((KS-\d+)[^)\n]*\)</h2>', flow_txt)}   # `(KS-1401, KS 1376)` too


def place(d, doc_txt, block, flow_txt, num, below_key=None):
    """insert block (whose flow number is num) into doc_txt by NUMBER order; for the wrong-order CONTROL, put it right AFTER below_key's block
    start instead (i.e. above the block that should precede it, or below the one that should follow — the caller picks the key)"""
    ls = doc_txt.split('\n'); fm = flow_map(flow_txt)
    def start_of(i): return i - 1 if i > 0 and ls[i - 1].strip() == '<div class="section">' else i
    at = None
    if d == FLOW:
        for i, l in enumerate(ls):
            m = re.match(r'\s*<h2>(\d+)\.[^\n]*\((KS-\d+)[^)\n]*\)</h2>', l)
            if not m: continue
            if below_key is None and int(m.group(1)) > num: at = i; break
            if below_key is not None and m.group(2) == below_key: at = i; break
    else:
        for i, l in enumerate(ls):
            m = re.search(r'&mdash; (KS-\d+)</h2>', l)
            if not m: continue
            if below_key is None and fm.get(m.group(1), 0) > num: at = start_of(i); break
            if below_key is not None and m.group(1) == below_key: at = start_of(i); break
    if at is None:
        at = [i for i, l in enumerate(ls) if l.strip() == ANCH.strip()]   # #1383 re-indents `  </body>` to `</body>`: match by content
        if len(at) != 1: raise SystemExit('REFUSING: %r not found exactly once in %s' % (ANCH.strip(), d))
        at = at[0]
    return '\n'.join(ls[:at] + block + ls[at:])


def resolve(base_rev, conflicted_tree, src_rev, src_base, num, idx, below_key=None):
    """the conflicted tree with each doc = base_rev's doc + src_rev's own block (vs src_base) placed by number -> tree sha"""
    e = {'GIT_INDEX_FILE': idx}; wgit(REPO, 'read-tree', conflicted_tree, env=e)
    flow_after = show(REPO, base_rev, FLOW)
    for d in DOCS:
        r = insert_block(show(REPO, src_base, d), show(REPO, src_rev, d))
        if r is None: raise SystemExit('REFUSING: no single insert block for %s in %s vs %s' % (d, src_rev[:12], src_base[:12]))
        txt = place(d, show(REPO, base_rev, d), r[1], flow_after, num, below_key)
        sha = wgit(REPO, 'hash-object', '-w', '--stdin', inp=txt).strip()
        wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (sha, d), env=e)
    return wgit(REPO, 'write-tree', env=e).strip()


def merge_tree(a, b):
    rc, o, e = wgit(REPO, 'merge-tree', '--write-tree', '--name-only', a, b, check=False)
    ls = o.split('\n'); ct = ls[0].strip(); conf = sorted(set(l for l in ls[1:] if l and not l.startswith(('Auto-merging', 'CONFLICT'))))
    return rc, ct, conf, [l for l in ls if l.startswith('CONFLICT')]


def wrong_key(dev_after, num):
    """CONTROL key: the block that should sit just BELOW ours (first flow number > num); placing ours below it is wrong order"""
    fm = flow_map(show(REPO, dev_after, FLOW)); above = sorted((n, k) for k, n in fm.items() if n > num); below = sorted((n, k) for k, n in fm.items() if n < num)
    return ('after', above[0][1]) if above else ('before', below[-1][1]) if below else (None, None)


def wrong_place(dev_after, ct, src, base, num, idx):
    how, key = wrong_key(dev_after, num)
    if key is None: return None, 'n/a'
    if how == 'before':   # ours ABOVE the highest-numbered block below it
        return resolve(dev_after, ct, src, base, num, idx, below_key=key), '%d above %s' % (num, key)
    # ours BELOW the next-higher block: place before the block after it, else before </body>
    fm = flow_map(show(REPO, dev_after, FLOW)); nxt = sorted((n, k) for k, n in fm.items() if n > fm[key])
    t = resolve(dev_after, ct, src, base, num, idx, below_key=nxt[0][1]) if nxt else resolve(dev_after, ct, src, base, 10 ** 6, idx)
    return t, '%d below %s' % (num, key)


def judge_qm(C, M, gated, gated_base, dev_after, idx, label, kit_dev=DEV):
    rc, ct, conf, msgs = merge_tree(dev_after, gated)
    C.chk('M0 conflict set', (rc == 1 and conf == sorted(DOCS)) or (rc == 0 and not conf),
          'merge-tree %s x %s rc %d | conflicted %s (want EXACTLY the two docs, or a clean merge) | verbatim %s' % (dev_after[:12], gated[:12], rc, conf, msgs))
    pred = resolve(dev_after, ct, gated, gated_base, NUM, idx) if rc == 1 else ct
    wrong, wl = wrong_place(dev_after, ct, gated, gated_base, NUM, idx) if rc == 1 else (None, 'n/a (clean)')
    mt = tree(REPO, M)
    C.chk('M1 tree == prediction', mt == pred and wrong != pred, '%s tree %s | prediction on %s %s | CONTROL wrong order (%s) -> %s, differs: %s' % (
        label, mt, dev_after[:12], pred, wl, (wrong or 'n/a')[:12], wrong != pred))
    par = git(REPO, 'log', '-1', '--format=%P', M).split()
    C.chk('M2 two parents', par == [gated, dev_after], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], gated[:12], dev_after[:12]))
    rd = sorted(set(l for l in git(REPO, 'show', '--remerge-diff', '--format=', '--name-only', M).split('\n') if l.strip()))
    C.chk('M3 remerge-diff only the docs', set(rd) <= set(DOCS) and (rd or rc == 0), 'git show --remerge-diff %s touches %s (want only the two docs; empty only for a clean merge, rc %d)' % (M[:12], rd or 'NOTHING', rc))
    t = git(REPO, 'log', '-1', '--format=%(trailers)', M).strip()
    C.chk('M4 no trailer', t == '', 'trailers %r' % t)
    r5, _, _ = git(REPO, 'merge-base', '--is-ancestor', kit_dev, dev_after, check=False)
    C.chk('M5 develop moved forward', r5 == 0, 'kit develop %s is an ancestor of %s: %s' % (kit_dev[:12], dev_after[:12], r5 == 0))
    cnt = int(git(REPO, 'rev-list', '--count', M, '--not', gated, dev_after).strip())
    C.chk('M6 one new commit', cnt == 1, 'rev-list --count %s --not %s %s = %d (want 1)' % (M[:12], gated[:12], dev_after[:12], cnt))
    moved = [p for p in git(REPO, 'diff', '--name-only', kit_dev, dev_after).splitlines() if p.strip()]
    hit = sorted(set(moved) & set(Q_PATHS))
    decl = lambda rev: [l for l in (show(REPO, rev, K['users_ts']) or '').split('\n') if any(v in l for v in K['users_ts_decls'].values())]
    dd, da = decl(kit_dev), decl(dev_after)
    C.chk('M7 Q-M+(c) path-disjoint', not hit and dd == da and len(dd) >= 2, 'develop %s..%s moved %d path(s); CHECKED against %d gated path(s): overlap %s | users.ts role-list declarations byte-identical (%d line(s)): %s' % (
        kit_dev[:12], dev_after[:12], len(moved), len(Q_PATHS), hit or 'NONE', len(dd), dd == da))
    return pred


def judge_docs(C, td, th, skill, paths):
    s4 = "Every test change updates its platform's two HTML docs, in the same commit"
    C.chk('D1 §4 at develop', s4 in ' '.join(skill.split()) and all(d in skill for d in DOCS), 'skill carries the §4 sentence: %s | both platform-k paths: %s' % (s4 in ' '.join(skill.split()), all(d in skill for d in DOCS)))
    need = set(DOCS) | {K['test'], K['product']}
    C.chk('D2 same commit', need <= set(paths) and not (set(K['platform_s_docs']) & set(paths)), 'head commit paths %d, carries test + oauth.ts + both docs: %s | platform-s docs: %s' % (
        len(paths), need <= set(paths), sorted(set(K['platform_s_docs']) & set(paths)) or 'NONE'))
    blocks = {}
    for d in DOCS:
        ins = insert_block(td[d], th[d]); dl = td[d].split('\n'); body_at = [i for i, l in enumerate(dl) if l == ANCH]
        ok = ins is not None and len(ins[1]) == K['block_lines'][d] and body_at == [ins[0]]
        C.chk('D3 one pure insert (%s)' % d.split('/')[-1][:24], ok, '%s | develop->head: %s | inserted %s line(s) (kit %d) at develop line %s; `  </body>` at %s' % (
            d.split('/')[-1], 'ONE insert' if ins else 'NOT a single pure insert: %s' % [o[0] for o in opcodes(dl, th[d].split('\n'))][:6],
            len(ins[1]) if ins else '-', K['block_lines'][d], ins[0] + 1 if ins else '-', [b + 1 for b in body_at]))
        blocks[d] = ins[1] if ins else []
        bt = '\n'.join(blocks[d])
        C.chk('D5 present once (%s)' % d.split('/')[-1][:24], bool(bt) and th[d].count(bt) == 1 and td[d].count(bt) == 0, 'block in head %d time(s), at develop %d' % (th[d].count(bt) if bt else -1, td[d].count(bt) if bt else -1))
    fh = th[FLOW]; nums = [int(m) for m in re.findall(r'(?m)^\s*<h2>(\d+)\.', fh)]; fb = '\n'.join(blocks[FLOW])
    h2s = re.findall(r'<h2>(\d+)\.', fb); h3s = re.findall(r'<h3>(\d+)\.(\d+)', fb)
    C.chk('D4 flow numbers', nums == K['flow_numbers_head'] and nums == sorted(nums) and h2s == [str(NUM)] and h3s and all(a == str(NUM) for a, b in h3s),
          'head <h2> numbers %s (kit %s) ascending: %s | the block\'s <h2>s %s (want [%d]) | its <h3>s %s' % (nums, K['flow_numbers_head'], nums == sorted(nums), h2s, NUM, ['%s.%s' % x for x in h3s]))
    cb = blocks[CHEAT]; cbt = '\n'.join(cb); ch = th[CHEAT]
    h2c = re.findall(r'<h2>([^<]*)</h2>', cbt); pos = [ch.find(K['cheat_prev_h2']), ch.find(K['cheat_h2'])]
    bal = cbt.count('<div') == cbt.count('</div>'); wrapped = bool(cb) and cb[0].strip() == '<div class="section">'
    C.chk('D6a cheat h2 / order / balance', len(h2c) == 1 and h2c[0] == K['cheat_h2'] and not re.match(r'\s*\d+\.', h2c[0]) and -1 not in pos and pos == sorted(pos) and bal,
          'h2 %s (unnumbered, kit %r) | after KS-1333\'s: %s | <div> %d open / %d close' % (h2c, K['cheat_h2'], -1 not in pos and pos == sorted(pos), cbt.count('<div'), cbt.count('</div>')))
    C.chk('D6b cheat wrapped in a section', wrapped, 'wrapped in its own <div class="section">: %s' % wrapped)
    for d in DOCS:
        t = '\n'.join(blocks[d]); el = {'test file': 'ks1210' in t, 'how to run (npx vitest run)': 'npx vitest run' in t,
                                       '§5f / live sweep': bool(re.search(r'live sweep', t, re.I)) and ('&sect;5f' in t or '§5f' in t), 'NOT covered note': bool(re.search(r'not covered', t, re.I))}
        for k, v in el.items():
            C.chk('D7 %s: %s' % ('flow' if d == FLOW else 'cheat', k), v, 'present in the %s block: %s' % ('flow' if d == FLOW else 'cheat', v))
    bad = []
    for d in DOCS:
        for unit in re.split(r'(?=<tr>)|(?=<div class="note">)|(?=<p>)', '\n'.join(blocks[d])):
            plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', unit))
            if DUR.search(plain):
                if not (re.search(r'20\d\d-\d\d-\d\d', plain) and re.search(r'(?i)host|macOS|Mac Studio|\bCI\b', plain)) and 'projection' not in plain.lower():
                    bad.append('%s: %s' % (d.split('/')[-1][:12], plain.strip()[:160]))
    for b in bad: print('INFO D8 a duration with no date AND host in its own unit: %s' % b)
    C.chk('D8 stated timings', not bad, '%d inserted unit(s) carry a duration with no date + host (or "projection") — CHECKED %d block line(s)' % (len(bad), sum(len(b) for b in blocks.values())))
    return blocks


def timing_statement(C):
    texts = [show(REPO, DEV, p) or '' for p in (FLOW, CHEAT, K['skill'])]
    def prox(rx_needle, durx):
        ment = near = 0
        for t in texts:
            for m in re.finditer(rx_needle, t):
                ment += 1
                if durx.search(t[max(0, m.start() - 120):m.end() + 120]): near += 1
        return ment, near
    sa, aa = prox(r'services/auth', PR_RX), prox(r'Akto', PR_RX); sk, ak = prox(r'services/auth', DUR), prox(r'Akto', DUR)
    C.chk('D8b §4 timing statement', sa[1] == 0 and aa[1] > 0, 'develop %s, flow + cheat + skill, the PR body\'s regex: services/auth %d mention(s), %d near a duration (want 0; body claims 7 / 0) | must-hit CONTROL Akto %d mention(s), %d near a duration (want > 0; body claims 134 / 11) | the kit\'s regex: services/auth %d/%d, Akto %d/%d' % (
        DEV[:12], sa[0], sa[1], aa[0], aa[1], sk[0], sk[1], ak[0], ak[1]))


def figures_vs_body(C, blocks, body):
    if body is None:
        print('INFO D9 NOT RUN: no PR body (pass --body-file, or run with GH access)'); return
    dt = ' '.join(re.sub(r'<[^>]+>', ' ', '\n'.join(blocks[d])) for d in DOCS); dt = ' '.join(dt.split())
    doc_green = bool(re.search(r'(?i)did not recur', dt)) and bool(re.search(r'864 passed, 0 failed', dt))
    body_red = bool(re.search(r'862 passed, 2 failed', body))
    C.chk('D9 doc figures vs the PR body', not (doc_green and body_red), 'docs say "864 passed, 0 failed" + ks949 "did not recur": %s | the PR body\'s Test Evidence at the SAME head reports run 1 "862 passed, 2 failed" (ks949): %s — whose run do the docs report?' % (doc_green, body_red))


print('c4_docs_gate60 %s %s | clone %s | develop %s | head %s' % (MODE or 'selftest', now(), REPO, DEV[:12], HEAD[:12]))
td = {d: show(REPO, DEV, d) for d in DOCS}; th = {d: show(REPO, HEAD, d) for d in DOCS}
SK = show(REPO, DEV, K['skill']); PATHS = git(REPO, 'diff', '--name-only', DEV, HEAD).splitlines()


def get_body():
    if opt('--body-file'): return open(opt('--body-file'), encoding='utf-8').read()
    try: return GH().get('pulls/' + K['pr']).get('body') or ''
    except SystemExit: return None


def sim_chain(idx):
    """SIM develop1 (#1381 tree on develop) and SIM develop2 (#1382's merge-in resolved on develop1); commit-tree in YOUR clone, never a ref"""
    for h in (O81['head'], O82['head']):
        if not has_commit(REPO, h): print('REFUSING: %s not in the clone — fetch refs/pull/1381/head and refs/pull/1382/head' % h[:12]); raise SystemExit(2)
    d1 = wgit(REPO, 'commit-tree', tree(REPO, O81['head']), '-p', DEV, '-m', 'SIM squash #1381 (gate60 c4)', env=ENV).strip()
    rc, ct, conf, _ = merge_tree(d1, O82['head'])
    t2 = resolve(d1, ct, O82['head'], DEV, 19, idx) if rc == 1 else ct
    d2 = wgit(REPO, 'commit-tree', t2, '-p', d1, '-m', 'SIM squash #1382 merge-in (gate60 c4)', env=ENV).strip()
    return d1, d2, t2, rc, conf


if '--selftest' in A:
    OUT = guard_out(opt('--out') or ''); IDX = os.path.join(OUT, 'c4.index'); st = {'ok': 0, 'n': 0}
    Cb = Checks(True); judge_docs(Cb, td, th, SK, PATHS); BASE = set(Cb.failed())
    print('SELFTEST BASELINE: the real head fails %s — an arm below counts only a NEW failure of its named check' % (sorted(BASE) or 'NOTHING'))
    def docs_arm(mut, d):
        t2 = dict(th); t2[d] = mut(t2[d]); landed = t2[d] != th[d]
        def f(C):
            C.chk('LANDED', landed, 'tamper landed: %s' % landed); judge_docs(C, td, t2, SK, PATHS)
        return f
    def rep(old, new, count=1):
        def f(s):
            assert s.count(old) >= 1, 'plant anchor absent: %r' % old[:60]; return s.replace(old, new, count)
        return f
    def narm(name, fn, want):
        def wrapped(C):
            C2 = Checks(True); fn(C2)
            for tag, ok in C2.tags: C.chk(tag, ok or tag in BASE, '(baseline-aware)')
        return selftest_arm(st, name, wrapped, want)
    fb = '\n'.join(insert_block(td[FLOW], th[FLOW])[1])
    narm('T0 the REAL head, baseline-aware (positive control)', lambda C: judge_docs(C, td, th, SK, PATHS), None)
    narm('T1 a second block edited (KS-1333 h2)', docs_arm(rep('reports blockNumber as a number (KS-1333)</h2>', 'reports blockNumber as a NUMBER (KS-1333)</h2>'), FLOW), 'D3')
    narm('T2 18 renumbered 17', docs_arm(rep('<h2>18. OAuth app scopes', '<h2>17. OAuth app scopes'), FLOW), 'D4')
    narm('T3 the block duplicated', docs_arm(rep(fb + '\n  </body>', fb + '\n' + fb + '\n  </body>'), FLOW), 'D')
    narm('T4 the cheat h2 numbered', docs_arm(rep('<h2>OAuth app scopes and ownership &mdash;', '<h2>18. OAuth app scopes and ownership &mdash;'), CHEAT), 'D6a')
    narm('T5 the flow block loses its live-sweep line', docs_arm(rep('live sweep', 'sweep', -1), FLOW), 'D7 flow: §5f')
    d1, d2, t2, rc2, conf2 = sim_chain(IDX)
    print('INFO SIM develop1 %s (tree %s = #1381) | SIM develop2 %s (tree %s; #1382 x develop1 rc %d conflicts %s)' % (d1[:12], tree(REPO, d1)[:12], d2[:12], t2[:12], rc2, conf2))
    rc, ct, conf, msgs = merge_tree(d2, HEAD); pred = resolve(d2, ct, HEAD, DEV, NUM, IDX) if rc == 1 else ct
    def mk(t, parents, msg='SIM merge develop into KS-1210'):
        a = []
        for p in parents: a += ['-p', p]
        return wgit(REPO, 'commit-tree', t, *a, '-m', msg, env=ENV).strip()
    e = {'GIT_INDEX_FILE': IDX}; wgit(REPO, 'read-tree', pred, env=e)
    bad_src = show(REPO, pred, K['product']) + '\n// sim extra edit\n'
    wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (wgit(REPO, 'hash-object', '-w', '--stdin', inp=bad_src).strip(), K['product']), env=e)
    bad_tree = wgit(REPO, 'write-tree', env=e).strip()
    wrong_tree, wl = wrong_place(d2, ct, HEAD, DEV, NUM, IDX)
    # a develop advance that touches routes/oauth.ts (Q-M+(c)): SIM develop3 = develop2 + an oauth.ts comment; the merge-in over it
    e3 = {'GIT_INDEX_FILE': IDX}; wgit(REPO, 'read-tree', tree(REPO, d2), env=e3)
    o3 = (show(REPO, d2, K['product']) or '') + '\n// sim develop edit\n'
    wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (wgit(REPO, 'hash-object', '-w', '--stdin', inp=o3).strip(), K['product']), env=e3)
    d3 = mk(wgit(REPO, 'write-tree', env=e3).strip(), [d2], 'SIM develop touching oauth.ts')
    rc3, ct3, _, _ = merge_tree(d3, HEAD); pred3 = resolve(d3, ct3, HEAD, DEV, NUM, IDX) if rc3 == 1 else ct3
    arms = [('Q0 the predicted merge-in (positive control)', mk(pred, [HEAD, d2]), d2, None),
            ('Q1 an extra oauth.ts edit in the merge-in', mk(bad_tree, [HEAD, d2]), d2, 'M1'),
            ('Q2 the block placed out of number order (%s)' % wl, mk(wrong_tree, [HEAD, d2]), d2, 'M1'),
            ('Q3 a single-parent rewrite (a rebase)', mk(pred, [d2]), d2, 'M2'),
            ('Q4 a trailer on the merge-in', mk(pred, [HEAD, d2], 'SIM merge\n\nCo-Authored-By: Sim <s@x>'), d2, 'M4'),
            ('Q5 develop advanced through routes/oauth.ts', mk(pred3, [HEAD, d3]), d3, 'M7')]
    for name, M, D_, want in arms:
        selftest_arm(st, name, lambda C, M=M, D_=D_: judge_qm(C, M, HEAD, DEV, D_, IDX, 'SIM merge-in'), want)
    selftest_arm(st, 'Q6 the extra oauth.ts edit also fails M3', lambda C: judge_qm(C, arms[1][1], HEAD, DEV, d2, IDX, 'SIM merge-in'), 'M3')
    print('INFO SIM chained prediction: #1384 merge-in over SIM develop2 -> tree %s (merge-tree rc %d, conflicts %s)' % (pred, rc, conf))
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
if MODE is None:
    print(__doc__); raise SystemExit(2)
C = Checks()
if MODE == 'docs':
    blocks = judge_docs(C, td, th, SK, PATHS); timing_statement(C); figures_vs_body(C, blocks, get_body())
else:
    OUT = guard_out(opt('--out') or ''); IDX = os.path.join(OUT, 'c4.index')
    if MODE == 'predict':
        rc, ct, conf, msgs = merge_tree(DEV, HEAD)
        C.chk('MP0 no-op merge reproduces END_TREE', rc == 0 and ct == K['end_tree'] == tree(REPO, HEAD), 'merge-tree develop x head rc %d tree %s | kit END_TREE %s' % (rc, ct, K['end_tree']))
        legs = [('MP1 vs #1381', O81, 13, K['author_predictions']['vs_1381_head']), ('MP2 vs #1382', O82, 19, K['author_predictions']['vs_1382_head'])]
        if O83: legs.append(('MP4 vs #1383', O83, 22, 'none-given-by-the-READY'))   # unreported by the READY; found by the drafter's census
        if O85: legs.append(('MP5 vs #1385', O85, 20, 'none-given-by-the-READY'))   # Seat E 3rd's own row 2, raised after the READY
        for tag, o, num_other, ap in legs:
            if not has_commit(REPO, o['head']): print('REFUSING: %s not in the clone' % o['head'][:12]); raise SystemExit(2)
            rc, ct, conf, msgs = merge_tree(o['head'], HEAD)
            pred = resolve(o['head'], ct, HEAD, DEV, NUM, IDX) if rc == 1 else ct
            wrong, wl = wrong_place(o['head'], ct, HEAD, DEV, NUM, IDX) if rc == 1 else (None, 'n/a')
            mk_ct = sum((show(REPO, ct, d) or '').count('<<<<<<< ') for d in DOCS)
            C.chk(tag, rc == 1 and conf == sorted(DOCS) and wrong not in (None, pred) and pred != ct,
                  'merge-tree %s x head rc %d | conflicted %s (want EXACTLY the two docs) | independent number-order RESOLUTION %s | CONTROL wrong order (%s) -> %s differs: %s' % (
                      o['head'][:12], rc, conf, pred, wl, (wrong or 'n/a')[:12], wrong not in (None, pred)))
            print('INFO %s the READY\'s "predicted tree" %s == merge-tree\'s CONFLICTED toplevel tree %s: %s (that tree carries %d conflict-marker line(s) in the docs — it is NOT a resolution) | == the resolution: %s' % (
                tag.split()[0], ap[:12], ct[:12], ct == ap, mk_ct, pred == ap))
        d1, d2, t2, rc2, conf2 = sim_chain(IDX)
        rc, ct, conf, msgs = merge_tree(d2, HEAD); pred = resolve(d2, ct, HEAD, DEV, NUM, IDX) if rc == 1 else ct
        g59 = 'df1344507d8cc13d23a767914ee85046c019a30c'
        fl = show(REPO, pred, FLOW) or ''; nums = [int(m) for m in re.findall(r'(?m)^\s*<h2>(\d+)\.', fl)]
        C.chk('MP3 chained #1381 -> #1382 -> #1384', rc == 1 and conf == sorted(DOCS) and t2 == g59 and nums == sorted(nums) and {13, 18, 19} <= set(nums),
              'SIM develop1 %s (= #1381 tree %s) | SIM develop2 %s tree %s == gate59\'s SIM prediction %s: %s | #1384 x develop2 rc %d conflicts %s | PREDICTED merge-in tree %s | its flow <h2> numbers %s ascending: %s' % (
                  d1[:12], O81['tree'][:12], d2[:12], t2, g59[:12], t2 == g59, rc, conf, pred, nums, nums == sorted(nums)))
    elif MODE == 'qm':
        M, D = opt('--merge-in-head'), opt('--develop-after')
        if not (M and D and has_commit(REPO, M) and has_commit(REPO, D)):
            print('REFUSING: qm needs --merge-in-head and --develop-after, both commits in the clone'); raise SystemExit(2)
        judge_qm(C, M, HEAD, DEV, D, IDX, 'merge-in %s' % M[:12])
n = C.nfail()
print('C4 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n else 0)
