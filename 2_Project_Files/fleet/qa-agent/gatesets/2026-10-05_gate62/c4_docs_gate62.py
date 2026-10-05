#!/usr/bin/env python3
"""c4_docs_gate62.py — C4 DOCS + the Q-M merge-in rule for #1387 (KS-1388 s1).

docs   --repo <git dir> [--head <sha>] [--develop <sha>]          READ verbs only. Or offline: --flow-base F --flow-head F --cheat-base F --cheat-head F
  D1  skill §4 at develop: SKILL.md blob == kit; it names both platform-k docs and "the host" (the rule the docs are judged by)
  D2  ONE commit carries the test AND both platform-k docs (rev-list develop..head == 1); 0 platform-s docs touched          (repo mode only)
  D3  flow: the ONLY change is ONE contiguous insert immediately before `  </body>` (0 lines removed, the close tag kept byte-equal,
      every pre-existing line byte-identical and in order)
  D4  flow `<h2>N.` numbers: develop [1..13], head [1..14] ascending, no duplicate; the new block's h2 is `14.` with a (KS-1388) key and
      its h3s are 14.x only
  D5  cheat: exactly TWO one-line replacements + ONE contiguous insert before `  </body>`; each replacement is the develop row with the
      kit suffix `, host Kamil's Mac Studio (2)` inserted before `</td></tr>` and NOTHING else (character diff), on the two kit rows
      (N-1380-3 `the three cells`, N-1381-2 `the nine cells`); the block is `<div class="section">`-wrapped, balanced, with the kit h2
      (unnumbered `&mdash; KS-1388`)
  D6  each new block is self-contained: names the test path, a `bash …prometheus_targets.test.sh` run line, a date 2026-10-05 AND a host,
      §5f / live sweep, a NOT-covered note, and that §2 / §3 are untouched
  D7  the "no stated timing" claim re-measured at DEVELOP by `grep -c -i` per doc per term, beside its must-hit control `auth`; prints the
      kit's claimed figures beside the measured ones (a mismatch FAILS: the claim sits in client-facing docs)
  D8  INFO (observation, never a blocker): host spellings per doc at head (`Kamils-Mac-Studio` vs `Kamil's Mac Studio (2)`) and any
      new-block timing row that names a date and host but no duration

predict --repo <OWN scratch clone> --develop-after <D> [--order number|reverse]   WRITE verbs, refused inside /Volumes/DevMASTER/!CODING
  The INDEPENDENT resolution of #1387 onto D: start from D's two docs; carry the two host rows (anchor asserted exactly once); insert the
  head's flow block before the first flow `<h2>N.` with N > 14 (else before `  </body>`), and the cheat block before the first cheat
  section whose KS key has a flow number > 14 (else before `  </body>`); the three non-doc paths take the head's blobs (asserted: D has
  develop's blobs there). Writes the tree with a temp index (in --out) and prints `PREDICTED <tree>`. --order reverse is the CONTROL
  (14. placed AFTER the later blocks: must give a different tree when D carries a later block). Positive control: D == develop → END_TREE.

qm --repo <clone> --merge-in-head <M> --develop-after <D> [--predicted <tree>]       READ verbs (predict is run if --predicted is absent)
  M1 tree(M) == prediction · M2 parents == [head, D] · M3 diff D..M names only kit paths and every non-doc one is at the head's blob ·
  M4 0 trailers (raw 1 byte) and 0 Co-Authored-By · M5 develop is an ancestor of D · M6 develop..D path-disjoint from the kit's three
  non-doc paths · M7 head..M is exactly [M]

--selftest  docs arms on fixture COPIES in fixtures/ (beside this file) + (with --scratch-clone <dir>) predict/qm arms on SIM commits in
            that clone. Every arm must produce a NEW FAIL; the positive control must be clean.
rc 0 all PASS / rc 1 any FAIL or 0 checked / rc 2 refused."""
import difflib, os, re, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate62 import K, git, wgit, Tally, outside_forbidden, HERE, SCRATCH

H2N = re.compile(r'^\s*<h2>(\d+)\.')
CLOSE = K['close_tag']
SUFFIX = K['host_fix_suffix']


def lines(s): return s.split('\n')


def flow_numbers(text): return [int(m.group(1)) for m in (H2N.match(l) for l in lines(text)) if m]


def opcodes(a, b):
    return [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != 'equal']


def judge_docs(fb, fh, cb, ch, t, skill=None, commits=None, touched=None, timing=None):
    if skill is not None:
        sb, stext = skill
        t.check('D1', sb == K['skill_blob_at_develop'] and K['flow'] in stext and K['cheat'] in stext and 'the host' in stext,
                'SKILL.md blob %s (want %s); names flow %s, cheat %s, "the host" %s' % (sb[:12], K['skill_blob_at_develop'][:12],
                K['flow'] in stext, K['cheat'] in stext, 'the host' in stext))
    if commits is not None:
        ps = [p for p in touched if p.startswith('docs/platform_s')]
        t.check('D2', commits == 1 and K['flow'] in touched and K['cheat'] in touched and K['test'] in touched and not ps,
                'commits develop..head %d (want 1); test+flow+cheat in that commit %s; platform-s docs touched %s' % (
                    commits, all(p in touched for p in (K['test'], K['flow'], K['cheat'])), ps))
    a, b = lines(fb), lines(fh)
    ops = opcodes(a, b)
    close_a = [i for i, l in enumerate(a) if l == CLOSE]; close_b = [i for i, l in enumerate(b) if l == CLOSE]
    ok3 = (len(ops) == 1 and ops[0][0] == 'insert' and len(close_a) == 1 and len(close_b) == 1 and ops[0][1] == close_a[0])
    t.check('D3', ok3, 'flow non-equal opcodes %s; `  </body>` lines develop %d head %d; insert at develop line %s (close tag at %s)' % (
        [(o[0], o[1] + 1, o[2], o[4] - o[3]) for o in ops], len(close_a), len(close_b), ops[0][1] + 1 if ops else None, close_a[0] + 1 if close_a else None))
    na, nb = flow_numbers(fb), flow_numbers(fh)
    blk = b[ops[0][3]:ops[0][4]] if ops and ops[0][0] == 'insert' else []
    h2s = [l for l in blk if '<h2>' in l]; h3s = re.findall(r'<h3>([\d.]+)', '\n'.join(blk))
    want_a = K['flow_numbers_develop']; want_b = K['flow_numbers_head']
    ok4 = (na == want_a and nb == want_b and len(set(nb)) == len(nb) and len(h2s) == 1 and H2N.match(h2s[0]) and
           int(H2N.match(h2s[0]).group(1)) == K['flow_block_number'] and '(KS-1388)' in h2s[0] and h3s and all(x.startswith('14.') for x in h3s))
    t.check('D4', bool(ok4), 'flow h2 develop %s head %s (want %s / %s, no duplicate); new block h2 %s; h3 %s' % (
        na, nb, want_a, want_b, [h.strip()[:70] for h in h2s], h3s))
    a, b = lines(cb), lines(ch)
    ops = opcodes(a, b)
    reps = [o for o in ops if o[0] == 'replace']; ins = [o for o in ops if o[0] == 'insert']; other = [o for o in ops if o[0] not in ('replace', 'insert')]
    close_a = [i for i, l in enumerate(a) if l == CLOSE]
    rep_ok = []
    for o in reps:
        old, new = a[o[1]:o[2]], b[o[3]:o[4]]
        single = len(old) == 1 and len(new) == 1
        good = False
        if single:
            j = old[0].rfind('</td></tr>')
            good = j > 0 and new[0] == old[0][:j] + SUFFIX + old[0][j:] and any(old[0].lstrip().startswith(r) for r in K['host_fix_rows'])
        rep_ok.append((o[1] + 1, good, (new[0][:0] if not single else '')))
    labels = sorted(r for r in K['host_fix_rows'] if any(a[o[1]].lstrip().startswith(r) for o in reps if o[2] - o[1] == 1))
    blk = b[ins[0][3]:ins[0][4]] if len(ins) == 1 else []
    bt = '\n'.join(blk)
    wrapped = bool(blk) and blk[0].strip() == '<div class="section">' and bt.count('<div') == bt.count('</div>')
    ok5 = (len(reps) == 2 and all(g for _, g, _ in rep_ok) and labels == sorted(K['host_fix_rows']) and len(ins) == 1 and not other and
           len(close_a) == 1 and ins[0][1] == close_a[0] and wrapped and K['cheat_h2_new'] in bt and bt.count('<h2>') == 1)
    t.check('D5', bool(ok5), 'cheat replacements %d %s on rows %s; inserts %d at develop line %s (close tag %s); other ops %d; wrapped+balanced %s; kit h2 present %s; h2 count %d' % (
        len(reps), [(l, g) for l, g, _ in rep_ok], labels, len(ins), ins[0][1] + 1 if ins else None, close_a[0] + 1 if close_a else None,
        len(other), wrapped, K['cheat_h2_new'] in bt, bt.count('<h2>')))
    fblk = '\n'.join(lines(fh)[opcodes(lines(fb), lines(fh))[0][3]:opcodes(lines(fb), lines(fh))[0][4]]) if opcodes(lines(fb), lines(fh)) else ''
    for name, txt in (('flow', fblk), ('cheat', bt)):
        need = {'test path': K['test'] in txt, 'run line': ('bash ' + K['test']) in txt, 'date': '2026-10-05' in txt,
                'host': ("Kamil's Mac Studio" in txt or 'Kamils-Mac-Studio' in txt), 'live sweep': bool(re.search(r'live sweep', txt, re.I)),
                '§5f': ('&sect;5f' in txt or '§5f' in txt), 'not covered': bool(re.search(r'not covered', txt, re.I)),
                '§2/§3 untouched': bool(re.search(r'(&sect;|§)2 and (&sect;|§)3[^.]{0,80}untouched', txt, re.S))}
        miss = [k for k, v in need.items() if not v]
        t.check('D6-' + name, not miss, '%s block (%d chars) self-contained; missing %s' % (name, len(txt), miss))
    if timing is not None:
        rows = []; bad = []
        for term, (cf, cc) in K['timing_claim_base'].items():
            key = term.replace(' (must-hit)', '')
            mf, mc = timing[key]
            rows.append('%s claimed %d/%d measured %d/%d' % (key, cf, cc, mf, mc))
            if (mf, mc) != (cf, cc): bad.append(key)
        ctl = timing['auth']
        t.check('D7', not bad and ctl[0] > 0 and ctl[1] > 0, '`grep -c -i` at develop, flow/cheat: %s; mismatches %s; must-hit control fired %s' % (
            ' | '.join(rows), bad, ctl[0] > 0 and ctl[1] > 0))
    for name, txt in (('flow', fh), ('cheat', ch)):
        t.info('D8-' + name, 'host spellings at head: Kamils-Mac-Studio %d, "Kamil\'s Mac Studio (2)" %d (observation only; builder-flagged, not fixed)' % (
            txt.count('Kamils-Mac-Studio'), txt.count("Kamil's Mac Studio (2)")))
    nodur = [l.strip()[:120] for l in blk if '<tr><td>' in l and '2026-10-05' in l and not re.search(r'\d\s*(ms|s|min)\b|wall', l)]
    t.info('D8-row', 'new cheat rows with a date+host and NO duration: %s' % (nodur or 'none'))


def timing_counts(fb, cb):
    out = {}
    for key in [k.replace(' (must-hit)', '') for k in K['timing_claim_base']]:
        rx = re.compile(re.escape(key), re.I)
        out[key] = (sum(1 for l in lines(fb) if rx.search(l)), sum(1 for l in lines(cb) if rx.search(l)))
    return out


def docs_repo(repo, head, dev, t):
    fb, fh = git(repo, 'show', '%s:%s' % (dev, K['flow'])), git(repo, 'show', '%s:%s' % (head, K['flow']))
    cb, ch = git(repo, 'show', '%s:%s' % (dev, K['cheat'])), git(repo, 'show', '%s:%s' % (head, K['cheat']))
    sb = git(repo, 'rev-parse', '%s:%s' % (dev, K['skill'])).strip(); st = git(repo, 'show', '%s:%s' % (dev, K['skill']))
    commits = len(git(repo, 'rev-list', '%s..%s' % (dev, head)).split())
    touched = git(repo, 'diff', '--name-only', dev, head).splitlines()
    judge_docs(fb, fh, cb, ch, t, skill=(sb, st), commits=commits, touched=touched, timing=timing_counts(fb, cb))


# ---------------- predict / qm ----------------

def ks_of_flow(text):
    m = {}
    for l in lines(text):
        g = re.match(r'^\s*<h2>(\d+)\..*\((KS-\d+)\)\s*</h2>', l)
        if g: m[g.group(2)] = int(g.group(1))
    return m


def resolve(dev_flow, dev_cheat, base_flow, base_cheat, head_flow, head_cheat, order='number'):
    n = K['flow_block_number']
    fo = opcodes(lines(base_flow), lines(head_flow)); assert len(fo) == 1 and fo[0][0] == 'insert', 'flow change is not one insert'
    fblk = lines(head_flow)[fo[0][3]:fo[0][4]]
    co = opcodes(lines(base_cheat), lines(head_cheat))
    reps = [(lines(base_cheat)[o[1]], lines(head_cheat)[o[3]]) for o in co if o[0] == 'replace']
    cins = [o for o in co if o[0] == 'insert']; assert len(cins) == 1, 'cheat change is not one insert'
    cblk = lines(head_cheat)[cins[0][3]:cins[0][4]]
    F = lines(dev_flow)
    later = [i for i, l in enumerate(F) if H2N.match(l) and int(H2N.match(l).group(1)) > n]
    close = [i for i, l in enumerate(F) if l == CLOSE]; assert len(close) == 1, 'flow close tag count %d' % len(close)
    at = (later[0] if later else close[0]) if order == 'number' else close[0]
    F = F[:at] + fblk + F[at:]
    C = lines(dev_cheat)
    for old, new in reps:
        idx = [i for i, l in enumerate(C) if l == old]; assert len(idx) == 1, 'host row anchor found %d times: %r' % (len(idx), old[:60])
        C[idx[0]] = new
    fmap = ks_of_flow(dev_flow)
    cands = []
    for i, l in enumerate(C):
        g = re.search(r'&mdash; (KS-\d+)</h2>', l)
        if g and fmap.get(g.group(1), 0) > n and i > 0 and C[i - 1].strip() == '<div class="section">':
            cands.append(i - 1)
    close = [i for i, l in enumerate(C) if l == CLOSE]; assert len(close) == 1, 'cheat close tag count %d' % len(close)
    at = (cands[0] if cands else close[0]) if order == 'number' else close[0]
    C = C[:at] + cblk + C[at:]
    return '\n'.join(F), '\n'.join(C)


def predict(repo, D, out, order='number', head=None, dev=None):
    head = head or K['head']; dev = dev or K['develop']
    if not outside_forbidden(repo):
        print('REFUSED: predict writes objects; %s is inside %s — use your OWN scratch clone' % (repo, K['forbidden_root'])); raise SystemExit(2)
    for p in K['qm_disjoint_paths']:
        a = git(repo, 'rev-parse', '%s:%s' % (dev, p)).strip(); b = git(repo, 'rev-parse', '%s:%s' % (D, p)).strip()
        if a != b:
            print('PREDICT REFUSED: develop-after changed %s (M6 fails: re-gate)' % p); return None
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    nf, nc = resolve(g(D, K['flow']), g(D, K['cheat']), g(dev, K['flow']), g(dev, K['cheat']), g(head, K['flow']), g(head, K['cheat']), order)
    os.makedirs(out, exist_ok=True)
    idx = os.path.join(out, 'predict.index.%d' % os.getpid())
    env = {'GIT_INDEX_FILE': idx}
    rc, o, e = wgit(repo, 'read-tree', D, env=env); assert rc == 0, e
    for path, text in ((K['flow'], nf), (K['cheat'], nc)):
        rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=text.encode('utf-8')); assert rc == 0, e
        rc, o, e = wgit(repo, 'update-index', '--cacheinfo', '100644,%s,%s' % (sha.strip(), path), env=env); assert rc == 0, e
    for p in K['qm_disjoint_paths']:
        sha = git(repo, 'rev-parse', '%s:%s' % (head, p)).strip()
        rc, o, e = wgit(repo, 'update-index', '--cacheinfo', '%s,%s,%s' % (K['modes'][p], sha, p), env=env); assert rc == 0, e
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    shutil.move(idx, os.path.join(out, '_quarantine_index_%s' % os.path.basename(idx)))  # quarantine, never rm
    tree = tree.strip(); print('PREDICTED %s (order %s, develop-after %s)' % (tree, order, D[:12])); return tree


def qm(repo, M, D, pred, t, head=None, dev=None):
    head = head or K['head']; dev = dev or K['develop']
    tm = git(repo, 'rev-parse', M + '^{tree}').strip()
    t.check('M1', pred is not None and tm == pred, 'tree(M) %s vs predicted %s' % (tm[:12], str(pred)[:12]))
    par = git(repo, 'log', '-1', '--format=%P', M).split()
    t.check('M2', par == [head, D], 'parents %s (want [%s, %s])' % ([p[:12] for p in par], head[:12], D[:12]))
    names = git(repo, 'diff', '--name-only', D, M).splitlines()
    bad = [p for p in names if p not in K['files']]
    drift = [p for p in K['qm_disjoint_paths'] if git(repo, 'rev-parse', '%s:%s' % (M, p)).strip() != git(repo, 'rev-parse', '%s:%s' % (head, p)).strip()]
    t.check('M3', not bad and not drift, 'D..M paths %s; non-kit %s; non-doc paths off the head blob %s' % (names, bad, drift))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', M).encode()); co = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', M)))
    t.check('M4', tb == 1 and co == 0, 'M trailers raw %d byte(s), Co-Authored-By %d (want 1 / 0)' % (tb, co))
    rc, _, _ = git(repo, 'merge-base', '--is-ancestor', dev, D, check=False)
    t.check('M5', rc == 0 and D != dev, 'develop %s is an ancestor of D %s: %s; D moved: %s' % (dev[:12], D[:12], rc == 0, D != dev))
    adv = git(repo, 'diff', '--name-only', dev, D).splitlines(); hit = sorted(set(adv) & set(K['qm_disjoint_paths']))
    t.check('M6', not hit, "develop's advance touches %d path(s); kit non-doc paths among them %s" % (len(adv), hit))
    new = git(repo, 'rev-list', '%s..%s' % (head, M), '^' + D).split()
    t.check('M7', new == [M], 'commits in head..M not on D: %s (want exactly [M])' % [c[:12] for c in new])


# ---------------- self-test ----------------

def selftest(scratch=None):
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    R = K['checkout']; ok = total = 0
    real = {k: git(R, 'show', '%s:%s' % (rev, K[doc])) for k, rev, doc in
            (('fb', K['develop'], 'flow'), ('fh', K['head'], 'flow'), ('cb', K['develop'], 'cheat'), ('ch', K['head'], 'cheat'))}
    for k, v in real.items(): open(os.path.join(fx, 'real_%s.html' % k), 'w', encoding='utf-8').write(v)
    def run(d, timing=None):
        t = Tally(); buf = io.StringIO()
        with contextlib.redirect_stdout(buf): judge_docs(d['fb'], d['fh'], d['cb'], d['ch'], t, timing=timing)
        return t
    T = timing_counts(real['fb'], real['cb'])
    t0 = run(real, T)
    print('SELFTEST %s T0 positive control (the REAL blobs, fixture copies in fixtures/real_*.html): %d checked, fails %s' % (
        'OK' if not t0.fails else 'MISS', t0.n, t0.fails)); ok += not t0.fails; total += 1
    host_old = '<tr><td>the nine cells</td>'
    def sub(s, a, b, n=1):
        assert s.count(a) == 1, 'tamper anchor must occur EXACTLY once (found %d): %r' % (s.count(a), a[:60])
        return s.replace(a, b, n)
    arms = [
        ('flow 14. renumbered 15.', 'fh', lambda s: sub(s, '<h2>14. ', '<h2>15. '), ['D4']),
        ('flow duplicate 13.', 'fh', lambda s: sub(s, '<h2>14. ', '<h2>13. '), ['D4']),
        ('flow an older block line edited', 'fh', lambda s: sub(s, "dispatchEvent</code>'s", "dispatchEvent</code> s"), ['D3']),
        ('flow close tag rewritten `</body>`', 'fh', lambda s: sub(s, '\n  </body>', '\n</body>'), ['D3']),
        ('cheat host suffix misspelt', 'ch', lambda s: sub(s, "0.36&ndash;0.55 s wall, three runs, 2026-10-05, host Kamil's Mac Studio (2)</td></tr>", "0.36&ndash;0.55 s wall, three runs, 2026-10-05, host Kamils-Mac-Studio</td></tr>"), ['D5']),
        ('cheat a THIRD row edited', 'ch', lambda s: sub(s, '<tr><td>new reds</td><td>0</td></tr>', '<tr><td>new reds</td><td>0 </td></tr>'), ['D5']),
        ('cheat block unwrapped', 'ch', lambda s: sub(s, '    <div class="section">\n      <h2>Observability', '      <h2>Observability'), ['D5']),
        ('cheat block numbered', 'ch', lambda s: sub(s, '<h2>Observability nginx', '<h2>14. Observability nginx'), ['D5']),
        ('cheat live sweep removed', 'ch', lambda s: sub(s, 'No live sweep (&sect;5f), so KS-1388', 'Nothing (&sect;5f), so KS-1388'), ['D6-cheat']),
        ('flow run line removed', 'fh', lambda s: sub(s, '<pre><code>bash Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh   # 6 cells', '<pre><code>run the suite   # 6 cells'), ['D6-flow']),
    ]
    for name, key, fn, want in arms:
        d = dict(real); d[key] = fn(d[key]); assert d[key] != real[key], 'tamper did not land: ' + name
        p = os.path.join(fx, 'arm_%02d_%s.html' % (total, key)); open(p, 'w', encoding='utf-8').write(d[key])
        t = run(d, T); total += 1; new = set(t.fails) - set(t0.fails); g = set(want) <= new; ok += g
        print('SELFTEST %s %s (landed, fixture %s): want NEW FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, sorted(new)))
    Tbad = dict(T); Tbad['auth'] = (0, 0)
    t = run(real, Tbad); total += 1; g = 'D7' in t.fails; ok += g
    print('SELFTEST %s timing must-hit control blind (auth 0/0): want FAIL D7 | got %s' % ('OK' if g else 'MISS', t.fails))
    Tbad = dict(T); Tbad['prometheus_targets'] = (0, 2)
    t = run(real, Tbad); total += 1; g = 'D7' in t.fails; ok += g
    print('SELFTEST %s timing claim mismatch (prometheus_targets 0/2): want FAIL D7 | got %s' % ('OK' if g else 'MISS', t.fails))
    if scratch:
        a, b = selftest_qm(scratch); ok += a; total += b
    else:
        print('SELFTEST NOTE predict/qm arms NOT run (no --scratch-clone given)')
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


def sim_commit(repo, parents, edits, msg, base, out):
    """a SIM commit in the scratch clone: base tree + edits {path: text|('blob', sha, mode)}"""
    idx = os.path.join(out, 'sim.index.%d' % os.getpid()); env = {'GIT_INDEX_FILE': idx}
    assert wgit(repo, 'read-tree', base, env=env)[0] == 0
    for p, v in edits.items():
        if isinstance(v, tuple): sha, mode = v[1], v[2]
        else:
            rc, sha, e = wgit(repo, 'hash-object', '-w', '--stdin', input_bytes=v.encode('utf-8')); assert rc == 0, e; sha = sha.strip(); mode = '100644'
        assert wgit(repo, 'update-index', '--cacheinfo', '%s,%s,%s' % (mode, sha, p), env=env)[0] == 0
    rc, tree, e = wgit(repo, 'write-tree', env=env); assert rc == 0, e
    shutil.move(idx, os.path.join(out, '_quarantine_sim_index_%d_%s' % (os.getpid(), tree.strip()[:8])))
    args = ['commit-tree', tree.strip()]
    for p in parents: args += ['-p', p]
    rc, c, e = wgit(repo, *args, env={'GIT_AUTHOR_NAME': 'SIM', 'GIT_AUTHOR_EMAIL': 'sim@invalid', 'GIT_COMMITTER_NAME': 'SIM',
                                     'GIT_COMMITTER_EMAIL': 'sim@invalid', 'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'},
                    input_bytes=msg.encode()); assert rc == 0, e
    return c.strip(), tree.strip()


def selftest_qm(repo):
    import io, contextlib
    if not outside_forbidden(repo):
        print('SELFTEST REFUSED scratch clone inside the forbidden root'); return 0, 1
    out = os.path.join(SCRATCH, 'sim'); os.makedirs(out, exist_ok=True)
    h, dv = K['head'], K['develop']; ok = total = 0
    g = lambda r, p: git(repo, 'show', '%s:%s' % (r, p))
    # positive control: D == develop -> END_TREE
    with contextlib.redirect_stdout(io.StringIO()): p0 = predict(repo, dv, out)
    total += 1; c = p0 == K['end_tree']; ok += c
    print('SELFTEST %s predict on the UNMOVED develop == END_TREE: %s vs %s' % ('OK' if c else 'MISS', str(p0)[:12], K['end_tree'][:12]))
    # SIM develop-after: a synthetic block 18. (KS-1210 key) appended to both docs, as a later PR would land
    fl = g(dv, K['flow']).replace('\n' + CLOSE, '\n    <h2>18. SIM later block (KS-1210)</h2>\n    <p>SIM</p>\n' + CLOSE, 1)
    ce = g(dv, K['cheat']).replace('\n' + CLOSE, '\n    <div class="section">\n      <h2>SIM later &mdash; KS-1210</h2>\n      <p>SIM</p>\n    </div>\n' + CLOSE, 1)
    Dsim, _ = sim_commit(repo, [dv], {K['flow']: fl, K['cheat']: ce}, 'SIM develop: KS-1210 lands first (block 18.)\n', dv, out)
    with contextlib.redirect_stdout(io.StringIO()):
        P = predict(repo, Dsim, out); Prev = predict(repo, Dsim, out, order='reverse')
    total += 1; c = P and Prev and P != Prev; ok += bool(c)
    print('SELFTEST %s order control: number-order %s != reverse-order %s' % ('OK' if c else 'MISS', str(P)[:12], str(Prev)[:12]))
    pf = git(repo, 'show', '%s:%s' % (P, K['flow'])) if False else None
    Mgood, _ = sim_commit(repo, [h, Dsim], {}, 'Merge develop into KS-1388: both platform-k doc blocks in number order\n', P, out)
    def runqm(M, D, pred):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): qm(repo, M, D, pred, t)
        return t
    t = runqm(Mgood, Dsim, P); total += 1; c = not t.fails and t.n == 7; ok += c
    print('SELFTEST %s Q-M positive control (SIM merge-in at the predicted tree): fails %s' % ('OK' if c else 'MISS', t.fails))
    arms = []
    Mrev, _ = sim_commit(repo, [h, Dsim], {}, 'Merge develop into KS-1388\n', Prev, out); arms.append(('14. below 18. (reverse order tree)', Mrev, Dsim, P, ['M1']))
    M1p, _ = sim_commit(repo, [Dsim], {}, 'squash-shaped\n', P, out); arms.append(('single parent', M1p, Dsim, P, ['M2']))
    Mx, _ = sim_commit(repo, [h, Dsim], {'README.md': 'SIM extra\n'}, 'Merge develop into KS-1388\n', P, out); arms.append(('an extra non-kit path', Mx, Dsim, P, ['M1', 'M3']))
    Mt, _ = sim_commit(repo, [h, Dsim], {}, 'Merge develop into KS-1388\n\nCo-Authored-By: X <x@invalid>\n', P, out); arms.append(('a Co-Authored-By trailer', Mt, Dsim, P, ['M4']))
    Dbad, _ = sim_commit(repo, [dv], {'observability/.env.example': 'SIM\n'}, 'SIM develop touches an env example\n', dv, out)
    Mb, _ = sim_commit(repo, [h, Dbad], {}, 'Merge develop into KS-1388\n', P, out); arms.append(("develop's advance touches observability/.env.example", Mb, Dbad, None, ['M6']))
    Mi, _ = sim_commit(repo, [h], {}, 'SIM intermediate\n', h, out)
    M2c, _ = sim_commit(repo, [Mi, Dsim], {}, 'Merge develop into KS-1388\n', P, out); arms.append(('two new commits', M2c, Dsim, P, ['M2', 'M7']))
    for name, M, D, pred, want in arms:
        t = runqm(M, D, pred); total += 1; c = set(want) <= set(t.fails); ok += c
        print('SELFTEST %s Q-M %s: want FAIL %s | got %s' % ('OK' if c else 'MISS', name, want, t.fails))
    with contextlib.redirect_stdout(io.StringIO()): pb = predict(repo, Dbad, out)
    total += 1; c = pb is None; ok += c
    print('SELFTEST %s predict REFUSES a develop that changed a kit non-doc path: %s' % ('OK' if c else 'MISS', 'refused' if pb is None else pb[:12]))
    print('SELFTEST NOTE SIM develop %s, SIM merge-in %s, predicted %s (objects in %s only; no ref written)' % (Dsim[:12], Mgood[:12], str(P)[:12], repo))
    return ok, total


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if A[0] == '--selftest' or '--selftest' in A: raise SystemExit(selftest(opt('--scratch-clone')))
    cmd = A[0]; repo = opt('--repo')
    if cmd == 'docs':
        t = Tally()
        if opt('--flow-base'):
            rd = lambda k: open(opt(k), encoding='utf-8').read()
            judge_docs(rd('--flow-base'), rd('--flow-head'), rd('--cheat-base'), rd('--cheat-head'), t)
        else:
            docs_repo(repo, opt('--head', K['head']), opt('--develop', K['develop']), t)
        raise SystemExit(t.end())
    if cmd == 'predict':
        tr = predict(repo, opt('--develop-after'), opt('--out', os.path.join(SCRATCH, 'sim')), opt('--order', 'number'))
        raise SystemExit(0 if tr else 1)
    if cmd == 'qm':
        D = opt('--develop-after'); pred = opt('--predicted') or predict(repo, D, opt('--out', os.path.join(SCRATCH, 'sim')))
        t = Tally(); qm(repo, opt('--merge-in-head'), D, pred, t); raise SystemExit(t.end())
    print(__doc__); raise SystemExit(2)
