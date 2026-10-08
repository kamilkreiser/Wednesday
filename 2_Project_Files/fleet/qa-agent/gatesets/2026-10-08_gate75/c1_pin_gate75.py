#!/usr/bin/env python3
r"""c1_pin_gate75.py — PIN checks for gate75's ONE row (#1426 KS-1450, a GUARD change). EVERY PR-specific value is a REQUIRED argument
compared with kit.json; nothing defaults. Carried in shape from c1_pin_gate74.py and re-keyed by the gate75 drafter.
#1426's head sits DIRECTLY ON develop (its one parent IS develop ddea005553bf at draft), so base == develop at draft and the squash tree
is predicted == END_TREE.
Usage: c1_pin_gate75.py --pr 1426 --repo <YOUR clone> --head <40-hex> --base <40-hex> --parents-n 1 --end-tree <40-hex> --develop <40-hex>
       |   --selftest --repo <clone>
  P1  the head == kit head_expected
  P2a is a commit; P2b EXACT parent count == --parents-n; P2c the parent == --base
  P3  the changed-path SET and each path's +/- == kit numstat
  P4  tree(head) == --end-tree == kit end_tree
  P5  trailers: `%(trailers)` raw bytes at the head == the kit's MEASURED pin (55 at draft: ONE Co-Authored-By trailer) against the
      CONTROL commit (55 B, one trailer) — a PIN, not an approval: the branch commit CARRIES a trailer (FINDING, RULINGS Q-TRAILER75)
  P6  Co-Authored-By lines in the head message == the kit's measured pin (1) (CONTROL: a planted line adds exactly one)
  P7  head subject == kit subject; its ASCII-ness and length are REPORTED (the head subject is NOT the squash subject: RULINGS Q-SUBJ75)
  P8  hyphenated keys in the head message == the kit's measured set; 0 closing-family words on any key (BINDING; CONTROL `Fixes KS-1`)
  P9  modes base -> head == kit modes per code path (the guard stays 100755)
  P10 NO-NEW-LEG: every kit tooling path identical base == head EXCEPT exactly the row's declared changed tooling (the guard and the
      baseline); the PR changing any OTHER tooling path, or NOT changing a declared one, FAILS
  P12 develop descends from the base; base..develop paths REPORTED; any of the row's paths moved by develop FAILS (the squash prediction
      would be void)
  P13 PRE-EXISTING MISMATCH files byte-identical base == head == develop == the kit's blob prefixes
  P14 GUARD-ONLY: every changed path is in {the guard, the baseline, the two platform docs}; 0 `Blockchain/Dev/` paths
  P15 THE FIX'S OWN INVARIANTS at the head: `$generated.from_runs` byte-equal (as parsed JSON) base == head; PROVENANCE_FILE and
      PROVENANCE_LINE_RE each assigned exactly ONCE in the guard; the jq-required branch present; the baseline parses as JSON at base and
      head (CONTROL: a 3-byte-truncated copy does not)
rc 0 all PASS / 1 any FAIL / 2 refused by name / 11 a required argument != kit.json."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate75 import K, ROWS, BASE, Tally, git, git_bytes, refuse_absent, opt, obj_at, mode_at, row_arg


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
    t.check('P5', tb == R['branch_trailer_bytes'] and cb > 1,
            'trailers raw bytes at the head %d == kit pin %d | CONTROL %s %d raw bytes (> 1: the reader is not blind)%s' % (
                tb, R['branch_trailer_bytes'], K['trailer_control'][:12], cb,
                ' | FINDING: the BRANCH commit carries a trailer (STANDING_LINES :371 "keep branch commits trailer-free"); RULINGS Q-TRAILER75' if tb > 1 else ''))
    msg = git(repo, 'log', '-1', '--format=%B', head)
    co = len(re.findall(r'(?im)^co-authored-by:', msg)); coc = len(re.findall(r'(?im)^co-authored-by:', msg + '\nCo-Authored-By: planted <p@x>\n'))
    t.check('P6', co == R['branch_coauthor_lines'] and coc == co + 1, 'Co-Authored-By lines %d == kit pin %d | CONTROL planted line found %d%s' % (
        co, R['branch_coauthor_lines'], coc, ' | FINDING (Q-TRAILER75): the LANDED squash must carry 0' if co else ''))
    subj = git(repo, 'log', '-1', '--format=%s', head).rstrip('\n')
    t.check('P7', subj == R['subject'], 'head subject == kit: %s | %d chars, ASCII %s, `(#` %s (REPORTED: the head subject is NOT the squash subject; Q-SUBJ75)' % (
        subj == R['subject'], len(subj), subj.isascii(), '(#' in subj))
    hy = sorted(set(re.findall(r'\bKS-\d+\b', msg))); cl = re.findall(K['closing_rx'], msg, re.I); clc = re.findall(K['closing_rx'], msg + '\nFixes KS-1\n', re.I)
    t.check('P8', hy == sorted(R['branch_keys_hyphenated']) and not cl and len(clc) == 1,
            'hyphenated keys in the head message %s == kit pin %s | closing-family on a key %d (BINDING) | CONTROL planted `Fixes KS-1` %d | own key %s; foreign hyphenated %s (they ATTACH: STANDING_LINES :278; the SQUASH body de-hyphenates them, Q-KEYS75)' % (
                hy, R['branch_keys_hyphenated'], len(cl), len(clc), R['ticket'], sorted(set(hy) - set(R['own_keys_default']))))
    md = {p: [mode_at(repo, base, p), mode_at(repo, head, p)] for p in R['modes']}
    t.check('P9', md == R['modes'], 'modes base->head %s == kit: %s' % ({os.path.basename(p): '%s->%s' % tuple(v) for p, v in md.items()}, md == R['modes']))
    declared = set(K['tooling_changed_by_row'][r]); bad, changed, devmoved, n = [], set(), [], 0
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
    bdev = [p for p in bd if p.startswith('Blockchain/Dev/')]
    t.check('P12', anc and not moved, 'develop %s descends from the base: %s | base..develop %d path(s), %d under Blockchain/Dev/ | row paths moved by develop: %s%s' % (
        dev[:12], anc, len(bd), len(bdev), moved or 'none', ' => develop == base: squash tree == END_TREE' if dev == base else ' => c4 `merged` re-predicts'))
    pm = K['preexisting_mismatch']['files']; bad13 = []
    for p, pre in pm.items():
        b, h, d = obj_at(repo, base, p), obj_at(repo, head, p), obj_at(repo, dev, p)
        if not (b and b == h == d and b.startswith(pre)): bad13.append('%s base %s head %s develop %s kit %s' % (p, b[:12], h[:12], d[:12], pre))
    t.check('P13', not bad13, 'PRE-EXISTING MISMATCH files byte-identical base == head == develop == kit prefixes (%d files)%s' % (len(pm), '' if not bad13 else ': ' + '; '.join(bad13)))
    allowed = {K['leg14']['suite'], K['leg14']['file'], K['docs']['flow'], K['docs']['cheat']}
    outside = sorted(set(R['numstat']) - allowed); bc = [p for p in ns if p.startswith('Blockchain/Dev/')]
    t.check('P14', not outside and not bc and set(ns) <= allowed, 'GUARD-ONLY: changed paths outside {guard, baseline, 2 docs}: %s | Blockchain/Dev paths %s' % (outside or 'none', bc or 'none'))
    bj = {}; ok_json = True
    for rev in (base, head):
        try: bj[rev] = json.loads(git_bytes(repo, rev, K['leg14']['file']))
        except Exception: ok_json = False
    ctl_bad = True
    try: json.loads(git_bytes(repo, head, K['leg14']['file'])[:-3])
    except Exception: ctl_bad = False
    fr_eq = ok_json and bj[base]['$generated']['from_runs'] == bj[head]['$generated']['from_runs']
    g = git_bytes(repo, head, K['leg14']['suite']).decode('utf-8')
    n_pf = len(re.findall(r'(?m)^PROVENANCE_FILE=', g)); n_re = len(re.findall(r'(?m)^PROVENANCE_LINE_RE=', g))
    jq_req = 'jq is required to bound the provenance exemption' in g
    t.check('P15', ok_json and not ctl_bad and fr_eq and n_pf == 1 and n_re == 1 and jq_req,
            'baseline parses at base+head %s (CONTROL a 3-byte-truncated copy REFUSED by the parser: %s) | $generated.from_runs equal base==head %s (%d ids) | PROVENANCE_FILE= x%d, PROVENANCE_LINE_RE= x%d | jq-required branch %s' % (
                ok_json, not ctl_bad, fr_eq, len(bj.get(head, {}).get('$generated', {}).get('from_runs', [])), n_pf, n_re, jq_req))
    return t.end()


def selftest(repo):
    import io, contextlib
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def quiet(*a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): rc = run(*a)
        return rc, buf.getvalue()
    R = ROWS['1426']; DEV = K['develop_at_draft']
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, R['end_tree'], DEV)
    rep(rc == 0, 'GREEN #1426 at its pins on develop %s: rc %d (%s)' % (DEV[:12], rc, ' '.join(l for l in o.split('\n') if l.startswith(('CHECKED', '0 FAIL', '1 FAIL', '2 FAIL')))))
    rc, o = quiet(repo, '1426', BASE, BASE, 1, R['end_tree'], DEV)
    rep(rc == 1 and 'FAIL P1 ' in o and 'FAIL P3 ' in o, 'PLANTED wrong head (develop itself) for #1426: P1 + P3 FAIL')
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 2, R['end_tree'], DEV)
    rep(rc == 1 and 'FAIL P2b ' in o, 'PLANTED --parents-n 2: P2b FAILS')
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, K['develop_tree_at_draft'], DEV)
    rep(rc == 1 and 'FAIL P4 ' in o, 'PLANTED wrong --end-tree (develop\'s tree): P4 FAILS')
    parent = git(repo, 'rev-parse', BASE + '^1').strip()
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, R['end_tree'], parent)
    rep(rc == 1 and 'FAIL P12 ' in o, 'PLANTED ancestor develop %s: P12 FAILS (does not descend)' % parent[:12])
    keep = K['tooling_changed_by_row']['1426']; K['tooling_changed_by_row']['1426'] = keep[:1]
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, R['end_tree'], DEV)
    K['tooling_changed_by_row']['1426'] = keep
    rep(rc == 1 and 'FAIL P10 ' in o, 'PLANTED: the baseline left undeclared -> P10 FAILS (an undeclared tooling change)')
    keep = R['branch_trailer_bytes']; R['branch_trailer_bytes'] = 1
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, R['end_tree'], DEV)
    R['branch_trailer_bytes'] = keep
    rep(rc == 1 and 'FAIL P5 ' in o, 'PLANTED a trailer-free pin (1 B) against the real head: P5 FAILS (the reader sees the trailer)')
    keep = R['branch_keys_hyphenated']; R['branch_keys_hyphenated'] = ['KS-1450']
    rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, R['end_tree'], DEV)
    R['branch_keys_hyphenated'] = keep
    rep(rc == 1 and 'FAIL P8 ' in o, 'PLANTED own-key-only pin against the real message: P8 FAILS (KS-1386 / KS-1451 are hyphenated)')
    keep = K['leg14']['file']; K['leg14']['file'] = K['docs']['flow']
    try:
        rc, o = quiet(repo, '1426', R['head_expected'], BASE, 1, R['end_tree'], DEV)
    except SystemExit as e:
        rc, o = 1, 'FAIL P15 (raised %s)' % e
    K['leg14']['file'] = keep
    rep(rc == 1 and ('FAIL P15 ' in o or 'FAIL P14 ' in o), 'PLANTED the baseline path pointed at an HTML doc: P14/P15 FAIL')
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
