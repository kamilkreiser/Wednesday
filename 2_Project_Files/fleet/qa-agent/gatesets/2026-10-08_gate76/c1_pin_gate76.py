#!/usr/bin/env python3
r"""c1_pin_gate76.py — PIN checks for gate76's TWO rows (#1427 KS-1274, #1428 KS-593). EVERY PR-specific value is a REQUIRED argument
compared with kit.json; nothing defaults. Carried in shape from c1_pin_gate75.py and re-keyed by the gate76 drafter: two rows (no default
row), P14 a per-row SCOPE (was GUARD-ONLY), P15 per-row FIX INVARIANTS (was the leg-14 baseline), P8 carries #1428's CLOSING-ADJACENCY
residue as a PIN OF A FINDING (the pushed commit message says `does not close KS-593`).
Both heads sit DIRECTLY ON develop (one parent == develop 0a6177ea5482 at draft): base == develop, each squash ALONE == its END_TREE.
Usage: c1_pin_gate76.py --pr <1427|1428> --repo <YOUR clone> --head <40-hex> --base <40-hex> --parents-n 1 --end-tree <40-hex> --develop <40-hex>
       |   --selftest --repo <clone>
  P1  the head == kit head_expected
  P2a is a commit; P2b EXACT parent count == --parents-n; P2c the parent == --base (three reads: STANDING_LINES :421)
  P3  the changed-path SET and each path's +/- == kit numstat
  P4  tree(head) == --end-tree == kit end_tree
  P5  trailers: `%(trailers)` raw bytes at the head == the kit's MEASURED pin (1 B = NONE, both rows) against the CONTROL commit (55 B, one
      trailer: the reader is not blind)
  P6  Co-Authored-By lines in the head message == the kit's pin (0) (CONTROL: a planted line adds exactly one)
  P7  head subject == kit subject; ASCII-ness and length REPORTED (#1427's head subject de-hyphenates its own key `KS 1274:` — it cannot be
      the squash subject as written: the R-lane builder requires the subject to OPEN with the hyphenated own key; RULINGS Q-SUBJ76)
  P8  hyphenated keys in the head message == the kit's measured set; closing-family ADJACENCY on a key == the kit's measured list. #1427: []
      (BINDING). #1428: ['close KS-593'] — the negation `does not close KS-593` is a PIN OF A FINDING (RULINGS Q-CLOSE593), not an approval:
      the squash composes a NEW message that must carry 0, and the merge seat must confirm KS-593 does not walk to Done. CONTROL `Fixes KS-1`.
  P9  modes base -> head == kit modes per code path (#1427's job stays 100755; #1428's three new test files are 100644)
  P10 NO-NEW-LEG: every kit tooling path identical base == head EXCEPT exactly the row's declared changed tooling
  P12 develop descends from the base; base..develop paths REPORTED; any of the row's paths moved by develop FAILS
  P13 PRE-EXISTING MISMATCH files byte-identical base == head == develop == the kit's blob prefixes
  P14 SCOPE: every changed path is under the row's allowed set (1427: the trivy job + the three container_trivy_* suites + the two docs;
      1428: services/originate/src/routes/{adminConfig,documents,signatories}.ts + services/originate/src/__tests__/ + the two docs); and 0
      paths of the OTHER row's set (file-disjoint except the docs)
  P15 THE FIX'S OWN INVARIANTS at the head (each with its base count, so a vacuous read cannot pass):
      1427: the jq predicate `has("Results") or has("ArtifactName")` x1 in the job (base 0); the new RED cell and the CONTROL cell x1 each in
            the failed-scan suite; the CLEAN stub `{"Results":[]}` in all three suites; a bare `echo '{}'` survives ONLY as the `bare)` arm.
      1428: documents.ts `!r || typeof r !== 'object'` x1 (base 0) AND, inside the `/:id/share` handler, the guard sits AFTER the 401, the
            `documents:share` role/scope gate and the tenant-scoped NOT_FOUND (line order read from the head blob); adminConfig `if (offset < 0)`
            x2 (base 0), both after `adminConfigRouter.use(authenticate(), requireRole(`; signatories `.isUUID()` x3 (base 0) after
            `signatoriesRouter.use(authenticate())`; the KS-1293 SUBJECTS gains exactly ONE line.
rc 0 all PASS / 1 any FAIL / 2 refused by name / 11 a required argument != kit.json."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate76 import K, ROWS, BASE, Tally, git, git_bytes, refuse_absent, opt, obj_at, mode_at, row_arg

DOCS = {K['docs']['flow'], K['docs']['cheat']}
JOB = 'Blockchain/Testing/jobs/04-container-trivy.sh'
TRIVY_SUITES = ['Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh',
                'Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh',
                'Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh']
ORIG = 'Blockchain/Dev/services/originate/src/'
SCOPE = {'1427': lambda p: p == JOB or p in TRIVY_SUITES or p in DOCS,
         '1428': lambda p: p in DOCS or p in (ORIG + 'routes/adminConfig.ts', ORIG + 'routes/documents.ts', ORIG + 'routes/signatories.ts')
                 or (p.startswith(ORIG + '__tests__/') and p.endswith('.test.ts'))}


def txt(repo, rev, p):
    return git_bytes(repo, rev, p).decode('utf-8') if obj_at(repo, rev, p) else ''


def inv_1427(repo, head):
    j_h, j_b = txt(repo, head, JOB), txt(repo, BASE, JOB)
    pred = 'has("Results") or has("ArtifactName")'
    fs = txt(repo, head, TRIVY_SUITES[1])
    red = '🔴 KS-1274 a trivy that exits 0 with a bare {} is recorded as scan-failed and the job exits 1'
    ctl = 'CONTROL KS-1274 a clean report with ArtifactName and no Results stays clean: rc 0, no error'
    clean = [txt(repo, head, s).count('{"Results":[]}') + txt(repo, head, s).count('{\\"Results\\":[]}') for s in TRIVY_SUITES]
    bare_lines = [l.strip() for s in TRIVY_SUITES for l in txt(repo, head, s).split('\n') if re.search(r"echo '\{\}'", l) and not l.strip().startswith('#')]  # CODE lines only: a comment quoting the old shape is not a stub
    ok = (j_h.count(pred) == 1 and j_b.count(pred) == 0 and fs.count(red) >= 1 and fs.count(ctl) >= 1 and all(c >= 1 for c in clean)
          and bare_lines == ["bare) echo '{}'; exit 0 ;;"])
    return ok, 'job predicate x%d (base x%d) | RED cell title x%d, CONTROL cell title x%d | clean stub per suite %s | surviving bare `echo \'{}\'` lines %s' % (
        j_h.count(pred), j_b.count(pred), fs.count(red), fs.count(ctl), clean, bare_lines)


def inv_1428(repo, head):
    d_h, d_b = txt(repo, head, ORIG + 'routes/documents.ts'), txt(repo, BASE, ORIG + 'routes/documents.ts')
    g = "!r || typeof r !== 'object'"
    L = d_h.split('\n'); i0 = next((i for i, l in enumerate(L) if "'/:id/share'" in l), -1)
    def after(pat):
        return next((i for i in range(i0, len(L)) if pat in L[i]), -1) if i0 >= 0 else -1
    pos = {'401': after('status(401)'), 'scope': after("'documents:share'"), '404': after("'NOT_FOUND'"), 'guard': after(g)}
    order = i0 >= 0 and -1 not in pos.values() and pos['401'] < pos['scope'] < pos['404'] < pos['guard']
    a_h, a_b = txt(repo, head, ORIG + 'routes/adminConfig.ts'), txt(repo, BASE, ORIG + 'routes/adminConfig.ts')
    aL = a_h.split('\n'); au = next((i for i, l in enumerate(aL) if 'adminConfigRouter.use(authenticate(), requireRole(' in l), -1)
    og = [i for i, l in enumerate(aL) if 'if (offset < 0)' in l]
    s_h, s_b = txt(repo, head, ORIG + 'routes/signatories.ts'), txt(repo, BASE, ORIG + 'routes/signatories.ts')
    sL = s_h.split('\n'); su = next((i for i, l in enumerate(sL) if 'signatoriesRouter.use(authenticate())' in l), -1)
    uu = [i for i, l in enumerate(sL) if '.isUUID()' in l]
    nu = s_h.count('.isUUID()')
    hm = 'Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts'
    sub = lambda t: re.findall(r"^\s*'[^']+\.test\.ts',\s*$", t, re.M)
    sh, sb = sub(txt(repo, head, hm)), sub(txt(repo, BASE, hm))
    ok = (d_h.count(g) == 1 and d_b.count(g) == 0 and order and len(og) == 2 and a_b.count('if (offset < 0)') == 0 and au >= 0 and all(i > au for i in og)
          and nu == 3 and s_b.count('.isUUID()') == 0 and su >= 0 and all(i > su for i in uu) and len(sh) == len(sb) + 1)
    return ok, ('documents.ts guard x%d (base x%d); in /:id/share (line %d): 401 :%d < documents:share :%d < NOT_FOUND :%d < guard :%d -> %s | '
                'adminConfig `if (offset < 0)` x%d (base x%d) at %s, router auth at :%d | signatories .isUUID() x%d (base x%d) at %s, router auth at :%d | '
                'KS-1293 SUBJECTS %d -> %d' % (d_h.count(g), d_b.count(g), i0 + 1, pos['401'] + 1, pos['scope'] + 1, pos['404'] + 1, pos['guard'] + 1, order,
                                               len(og), a_b.count('if (offset < 0)'), [i + 1 for i in og], au + 1, nu, s_b.count('.isUUID()'), [i + 1 for i in uu], su + 1,
                                               len(sb), len(sh)))


INVARIANTS = {'1427': inv_1427, '1428': inv_1428}


def run(repo, r, head, base, npar, tree, dev):
    R = ROWS[r]; t = Tally()
    print('ROW #%s (%s) head %s base %s develop %s' % (r, R['ticket'], head[:12], base[:12], dev[:12]))
    t.check('P1', head == R['head_expected'], 'head %s == kit head_expected %s' % (head[:12], R['head_expected'][:12]))
    typ = git(repo, 'cat-file', '-t', head).strip()
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    t.check('P2a', typ == 'commit', 'object type %s' % typ)
    t.check('P2b', len(par) == npar, 'parent count %d == --parents-n %d (whole %%P read)' % (len(par), npar))
    t.check('P2c', par[:1] == [base], 'parent %s == --base %s' % ([p[:12] for p in par], base[:12]))
    ns = {}
    for l in git(repo, 'diff', '--numstat', base, head).strip().split('\n'):
        if l: a, d, p = l.split('\t', 2); ns[p] = [int(a), int(d)]
    want = R['numstat']
    t.check('P3', ns == want, 'numstat %d paths == kit %d: %s%s' % (len(ns), len(want), ns == want,
            '' if ns == want else ' | extra %s missing %s differing %s' % (sorted(set(ns) - set(want)), sorted(set(want) - set(ns)),
                                                                          sorted(p for p in ns if p in want and ns[p] != want[p]))))
    ht = git(repo, 'rev-parse', head + '^{tree}').strip()
    t.check('P4', ht == tree == R['end_tree'], 'tree %s == --end-tree %s == kit %s' % (ht[:12], tree[:12], R['end_tree'][:12]))
    tb = len(git(repo, 'log', '-1', '--format=%(trailers)', head).encode()); cb = len(git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control']).encode())
    t.check('P5', tb == R['branch_trailer_bytes'] and cb == K['trailer_control_raw_bytes'] and cb > 1,
            'trailers raw bytes at the head %d == kit pin %d (1 B = none) | CONTROL %s %d raw bytes == kit %d (> 1: the reader is not blind)' % (
                tb, R['branch_trailer_bytes'], K['trailer_control'][:12], cb, K['trailer_control_raw_bytes']))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    co = len(re.findall(r'(?im)^co-authored-by:', msg)); coc = len(re.findall(r'(?im)^co-authored-by:', msg + '\nCo-Authored-By: planted <p@x>\n'))
    t.check('P6', co == R['branch_coauthor_lines'] and coc == co + 1, 'Co-Authored-By lines %d == kit pin %d | CONTROL planted line found %d' % (
        co, R['branch_coauthor_lines'], coc))
    subj = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n')
    t.check('P7', subj == R['subject'], 'head subject == kit: %s | %d chars, ASCII %s, `(#` %s, opens with the HYPHENATED own key %s (REPORTED: Q-SUBJ76)' % (
        subj == R['subject'], len(subj), subj.isascii(), '(#' in subj, subj.startswith(R['ticket'] + ':')))
    hy = sorted(set(re.findall(r'\bKS-\d+\b', msg)))
    adj = re.findall(r'(?i)\b(?:clos(?:e|es|ed)|fix(?:es|ed)?|resolv(?:e|es|ed))\s+KS-\d+', msg)
    adjc = re.findall(r'(?i)\b(?:clos(?:e|es|ed)|fix(?:es|ed)?|resolv(?:e|es|ed))\s+KS-\d+', msg + '\nFixes KS-1\n')
    neg = [m for m in re.findall(r'(?i)(\bnot\s+close\s+KS-\d+)', msg)]
    t.check('P8', hy == sorted(R['branch_keys_hyphenated']) and adj == R['branch_closing_adjacency'] and len(adjc) == len(adj) + 1,
            'hyphenated keys in the head message %s == kit pin %s | closing ADJACENCY %s == kit pin %s (negated: %s) | CONTROL planted `Fixes KS-1` %d%s' % (
                hy, R['branch_keys_hyphenated'], adj, R['branch_closing_adjacency'], neg, len(adjc),
                ' | FINDING (Q-CLOSE593): the PUSHED message carries the adjacency; the SQUASH body must carry 0 and KS-593 must not walk to Done' if adj else ''))
    md = {p: [mode_at(repo, base, p), mode_at(repo, head, p)] for p in R['modes']}
    t.check('P9', md == R['modes'], 'modes base->head %s == kit: %s' % ({os.path.basename(p): '%s->%s' % tuple(v) for p, v in md.items()}, md == R['modes']))
    declared = set(K['tooling_changed_by_row'][r]); changed, devmoved, n = set(), [], 0
    for p in K['tooling_paths']:
        b, h, d = obj_at(repo, base, p), obj_at(repo, head, p), obj_at(repo, dev, p); n += 1
        if b != h: changed.add(p)
        if b != d: devmoved.append(os.path.basename(p))
    extra, missing = sorted(changed - declared), sorted(declared - changed)
    t.check('P10', not extra and not missing, 'NO-NEW-LEG: %d tooling paths; changed by the PR %s == declared %s%s' % (
        n, sorted(changed), sorted(declared), (' | UNDECLARED %s | DECLARED BUT UNCHANGED %s' % (extra, missing)) if extra or missing else ''))
    t.info('P10d', 'develop moved %d tooling path(s) since the base: %s' % (len(devmoved), devmoved or 'none'))
    anc = git(repo, 'merge-base', '--is-ancestor', base, dev, check=False)[0] == 0
    moved = [p for p in R['numstat'] if obj_at(repo, base, p) != obj_at(repo, dev, p)]
    bd = [l for l in git(repo, 'diff', '--name-only', base, dev).split('\n') if l]
    t.check('P12', anc and not [p for p in moved if p not in DOCS], 'develop %s descends from the base: %s | base..develop %d path(s), %d under Blockchain/Dev/ | row CODE paths moved by develop: %s | row DOC paths moved: %s%s' % (
        dev[:12], anc, len(bd), len([p for p in bd if p.startswith('Blockchain/Dev/')]), [p for p in moved if p not in DOCS] or 'none',
        [os.path.basename(p) for p in moved if p in DOCS] or 'none',
        ' => develop == base: squash ALONE == END_TREE' if dev == base else ' => c4 `chain` re-predicts (a docs move is a keep-both merge-in, a CODE move is a RE-GATE)'))
    pm = K['preexisting_mismatch']['files']; bad13 = []
    for p, pre in pm.items():
        b, h, d = obj_at(repo, base, p), obj_at(repo, head, p), obj_at(repo, dev, p)
        if not (b and b == h == d and b.startswith(pre)): bad13.append('%s base %s head %s develop %s kit %s' % (p, b[:12], h[:12], d[:12], pre))
    t.check('P13', not bad13, 'PRE-EXISTING MISMATCH files byte-identical base == head == develop == kit prefixes (%d files)%s' % (len(pm), '' if not bad13 else ': ' + '; '.join(bad13)))
    other = [o for o in ROWS if o != r][0]
    outside = sorted(p for p in ns if not SCOPE[r](p)); cross = sorted(p for p in ns if p not in DOCS and SCOPE[other](p))
    t.check('P14', ns and not outside and not cross, 'SCOPE #%s: changed paths outside its allowed set %s | non-doc paths in #%s\'s set %s (file-disjoint except the docs)' % (
        r, outside or 'none', other, cross or 'none'))
    ok15, msg15 = INVARIANTS[r](repo, head)
    t.check('P15', ok15, msg15)
    return t.end()


def selftest(repo):
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def quiet(*a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): rc = run(*a)
        return rc, buf.getvalue()
    DEV = K['develop_at_draft']
    for r in ROWS:
        R = ROWS[r]
        rc, o = quiet(repo, r, R['head_expected'], BASE, 1, R['end_tree'], DEV)
        rep(rc == 0, 'GREEN #%s at its pins on develop %s: rc %d (%s)' % (r, DEV[:12], rc, ' '.join(l for l in o.split('\n') if l.startswith(('CHECKED', '0 FAIL', '1 FAIL', '2 FAIL')))))
    A, B = ROWS['1427'], ROWS['1428']
    rc, o = quiet(repo, '1427', B['head_expected'], BASE, 1, A['end_tree'], DEV)
    rep(rc == 1 and 'FAIL P1 ' in o and 'FAIL P3 ' in o and 'FAIL P14 ' in o, 'PLANTED the OTHER row\'s head (#1428) under #1427: P1 + P3 + P14 FAIL')
    rc, o = quiet(repo, '1428', B['head_expected'], BASE, 2, B['end_tree'], DEV)
    rep(rc == 1 and 'FAIL P2b ' in o, 'PLANTED --parents-n 2: P2b FAILS')
    rc, o = quiet(repo, '1428', B['head_expected'], BASE, 1, K['develop_tree_at_draft'], DEV)
    rep(rc == 1 and 'FAIL P4 ' in o, 'PLANTED wrong --end-tree (develop\'s tree): P4 FAILS')
    parent = git(repo, 'rev-parse', BASE + '^1').strip()
    rc, o = quiet(repo, '1427', A['head_expected'], BASE, 1, A['end_tree'], parent)
    rep(rc == 1 and 'FAIL P12 ' in o, 'PLANTED ancestor develop %s: P12 FAILS (does not descend)' % parent[:12])
    keep = K['tooling_changed_by_row']['1428']; K['tooling_changed_by_row']['1428'] = []
    rc, o = quiet(repo, '1428', B['head_expected'], BASE, 1, B['end_tree'], DEV)
    K['tooling_changed_by_row']['1428'] = keep
    rep(rc == 1 and 'FAIL P10 ' in o, 'PLANTED: the KS-1293 manifest left undeclared -> P10 FAILS (an undeclared tooling change)')
    keep = K['trailer_control_raw_bytes']; K['trailer_control_raw_bytes'] = 1
    rc, o = quiet(repo, '1427', A['head_expected'], BASE, 1, A['end_tree'], DEV)
    K['trailer_control_raw_bytes'] = keep
    rep(rc == 1 and 'FAIL P5 ' in o, 'PLANTED a blind-reader pin (control 1 B) against the real 55-B control: P5 FAILS')
    keep = B['branch_closing_adjacency']; B['branch_closing_adjacency'] = []
    rc, o = quiet(repo, '1428', B['head_expected'], BASE, 1, B['end_tree'], DEV)
    B['branch_closing_adjacency'] = keep
    rep(rc == 1 and 'FAIL P8 ' in o, 'PLANTED a clean-message pin for #1428: P8 FAILS (the reader SEES `does not close KS-593`)')
    keep = A['branch_closing_adjacency']; A['branch_closing_adjacency'] = ['close KS-1274']
    rc, o = quiet(repo, '1427', A['head_expected'], BASE, 1, A['end_tree'], DEV)
    A['branch_closing_adjacency'] = keep
    rep(rc == 1 and 'FAIL P8 ' in o, 'PLANTED an adjacency pin #1427 does not have: P8 FAILS (no false adjacency)')
    # P15 is load-bearing: run each row's invariant at the BASE (the fix absent) -> FALSE
    for r in ROWS:
        ok, m = INVARIANTS[r](repo, BASE)
        rep(not ok, 'P15 #%s invariant read AT THE BASE (the fix absent) is FALSE: %s' % (r, m[:150]))
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]; repo = opt(A, '--repo')
    if not repo: print(__doc__); return 2
    if '--selftest' in A: return selftest(repo)
    r = row_arg(); R = ROWS[r]
    head, base, npar, tree, dev = opt(A, '--head'), opt(A, '--base'), opt(A, '--parents-n'), opt(A, '--end-tree'), opt(A, '--develop')
    miss = [k for k, v in (('--head', head), ('--base', base), ('--parents-n', npar), ('--end-tree', tree), ('--develop', dev)) if not v]
    if miss: print('REFUSED: required argument(s) missing: %s' % miss); return 2
    for k, v, want in (('--base', base, R['parents'][0]), ('--parents-n', npar, str(R['parent_count'])), ('--end-tree', tree, R['end_tree'])):
        if v != want: print('REFUSED: WRONG VALUE %s %s != kit.json %s' % (k, v, want)); return 11
    rc = refuse_absent(repo, [('--head', head), ('--base', base), ('--develop', dev), ('trailer control', K['trailer_control'])])
    return rc or run(repo, r, head, base, int(npar), tree, dev)


if __name__ == '__main__':
    sys.exit(main())
