#!/usr/bin/env python3
"""c4_tools_gate79.py — the THREE TOOL FIXES Seat K 2nd made before its push (attack h), each proved able to FAIL (red arm) and to
PASS on the real push. NEW in gate79. Every tool is COPIED into YOUR fresh scratch dir and run there (never in the seat's records,
never under !CODING); each copy's sha256/16 is checked against the READY's figure before it is run. Plants are made only in copies.

  tools --scratch DIR --clone CL --base B --head H --develop D
    TG  gatelinesk2.py (READY 671c737b3fe918ee): exit codes 0 MATCHES / 1 MISMATCH / 3 NOT APPLICABLE / 2 unreadable, and the
        run_shell_suites pin (49,0) -> (59,0).
        G-PASS   the REAL push log s-k1-ks1402-b4933a457f38-push.out -> rc 0, VERDICT MATCHES, run_shell_suites (59, 0) OK
        G-RED1   the log with run_shell_suites' count line rewritten to `49 passed, 0 failed` -> rc 1 (the pin can fail)
        G-RED2   the log + a `FIXTURE BUILD FAILED` line -> rc 1
        G-RED3   the log with pre_push_hook_base's first count `28 passed, 0 failed` -> `27 passed, 1 failed` -> rc 1
        G-NA     a format-gate-only log (no platform block, one `format-gate` line) -> rc 3 (the third state, never 0)
        G-UNREAD a missing path -> rc 2
        G-PRED   CONTROL: the predecessor gatelinesg1.py (b5e7923f605af9da) on the SAME real log -> rc 0 WHILE printing MISMATCH
                 (the no-exit-code defect the fix closes; if it printed MATCHES the (49,0) story is wrong)
        G-PIN    the (59,0) re-pin re-derived: run_shell_suites' first count in EVERY *-push.out under the Blockchain
                 5_Project_History folders dated 2026-10-06..09 (read-only), tallied — the READY says 22 logs, all (59, 0)
    TP  pathgatek2.py (READY d2564222c1cb44b6): PR0_FILES check REMOVED, ACCEPTED_BASE asserted instead.
        P-PASS   (clone, base, head, declared_k2.txt) -> rc 0, 7/7
        P-RED1   base := develop (not the accepted base) -> rc 1 (the hazard the removed PR0 check guarded is now a base assert)
        P-RED2   a declared file with 7 of the 8 lines -> rc 1
        P-RED3   head := develop (a different path set) -> rc 1
        P-RED4   a declared file + a package-lock.json path -> rc 1 (co-tenant / declared-set arms)
        P-PRED   CONTROL: the predecessor pathgateg1.py (K 1st's copy) on the real (base, head) -> its verdict printed (the READY: it
                 false-FAILs documents.ts via PR0_FILES); if it PASSES, the removal's stated reason does not hold
    TN  namecheckk2.py (READY dddc9f2b78ecde4e): MY_FORMS / _planted re-keyed off E 2nd's forms.
        N-PASS   the copy as-is -> rc 0, `24/24 controls fired`
        N-RED1   ROW1_BRANCH's `-k2-1` -> `-g5-1` (a FOREIGN token) -> rc != 0
        N-RED2   MY_FORMS re-keyed BACK to E 2nd's forms (-e2- / s-e2- / seate2 / -e2) — the defect the fix closed -> rc != 0
        N-INFO   its subject-length gate still adds " (#NNNN)" (SUFFIX_ALLOWANCE): SUPERSEDED by STANDING_LINES 2026-10-07 — printed
    TS  pushk2.sh (READY c4389f36fcd7f695), STATIC: the gate-existence + py_compile check precedes the lock take; GLRC is read
        unpiped from a file and DECIDES the exit (case 0 / 3 / *); the seat's push console line `gatelinesk2 rc=0` quoted.
  --selftest   the log rewriters (each lands, asserted), the tally parser.
rc 0 every arm as predicted / 1 an arm did not behave / 2 refused."""
import glob, hashlib, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate79 import K, req, must_be_outside

T = K['tools']; HDR = re.compile(r'^===\s+(\S+)\s+===\s*$'); CNT = re.compile(r'(?:^|\s)(\d+)\s+passed,\s*(\d+)\s+failed')


def sha16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def run(args, cwd=None):
    e = dict(os.environ); e.pop('GIT_SSH_COMMAND', None); e['PYTHONDONTWRITEBYTECODE'] = '1'
    p = subprocess.run(args, capture_output=True, cwd=cwd, env=e, timeout=600)
    return p.returncode, p.stdout.decode('utf-8', 'replace') + p.stderr.decode('utf-8', 'replace')


def rewrite_block_count(text, block, new):
    """replace the FIRST count line inside the named `=== block ===` with `new` ('N passed, M failed'); asserts it landed."""
    L = text.split('\n'); cur = None
    for i, l in enumerate(L):
        m = HDR.match(l)
        if m: cur = os.path.basename(m.group(1)); continue
        if cur == block and CNT.search(l):
            L[i] = CNT.sub(' ' + new, l, count=1); out = '\n'.join(L)
            assert out != text and new in out, 'rewrite did not land'
            return out
    raise AssertionError('block %s has no count line' % block)


def first_count(text, block):
    cur = None
    for l in text.split('\n'):
        m = HDR.match(l)
        if m: cur = os.path.basename(m.group(1)); continue
        if cur == block:
            c = CNT.search(l)
            if c: return (int(c.group(1)), int(c.group(2)))
    return None


def tools(scr, clone, base, head, develop):
    must_be_outside(scr, 'scratch'); os.makedirs(scr, exist_ok=False); bad = []
    def arm(aid, rc, out, want_rc, must=None, mustnot=None):
        ok = (rc in want_rc if isinstance(want_rc, (list, tuple, set)) else rc == want_rc) and (must is None or must in out) and (mustnot is None or mustnot not in out)
        print('%-5s %-9s rc %s (want %s)%s%s | %s' % ('OK' if ok else 'BAD', aid, rc, want_rc, (' must %r' % must) if must else '', (' mustnot %r' % mustnot) if mustnot else '',
              ' / '.join(l.strip() for l in out.strip().split('\n') if re.search(r'VERDICT|run_shell_suites|CHECKED|controls fired|FAIL |PASS |REFUSED|NAMECHECK|POSITIVE CONTROL FIRED|BLIND on', l))[:400]))
        if not ok: bad.append(aid)
    cp = {}
    for name, want in T['sha256_16'].items():
        src = os.path.join(T['dir'], name)
        if name == 'gatelinesg1.py': src = os.path.join(T['dir'], name)
        dst = os.path.join(scr, name); shutil.copy2(src, dst); cp[name] = dst
        got = sha16(dst); print('COPY %-16s sha256/16 %s == READY %s: %s' % (name, got, want, got == want))
        if got != want: bad.append('COPY-' + name)
    pg1 = os.path.join(K['pr']['builder_records_k1'], 'tools', 'pathgateg1.py'); cp['pathgateg1.py'] = os.path.join(scr, 'pathgateg1.py'); shutil.copy2(pg1, cp['pathgateg1.py'])
    print('COPY pathgateg1.py (K 1st) sha256/16 %s' % sha16(cp['pathgateg1.py']))
    log = open(T['push_log'], encoding='utf-8', errors='replace').read(); print('PUSH LOG %s sha256/16 %s, %d lines' % (T['push_log'], hashlib.sha256(log.encode()).hexdigest()[:16], log.count('\n')))
    def L(name, text): p = os.path.join(scr, name); open(p, 'w').write(text); return p
    rc, o = run(['python3', cp['gatelinesk2.py'], T['push_log']]); arm('G-PASS', rc, o, 0, 'VERDICT: MATCHES', None)
    print('      run_shell_suites in the real log: %s' % (first_count(log, 'run_shell_suites.test.sh'),))
    rc, o = run(['python3', cp['gatelinesk2.py'], L('red1.out', rewrite_block_count(log, 'run_shell_suites.test.sh', '49 passed, 0 failed'))]); arm('G-RED1', rc, o, 1, 'MISMATCH')
    rc, o = run(['python3', cp['gatelinesk2.py'], L('red2.out', log + '\nFIXTURE BUILD FAILED planted by gate79\n')]); arm('G-RED2', rc, o, 1, 'MISMATCH')
    rc, o = run(['python3', cp['gatelinesk2.py'], L('red3.out', rewrite_block_count(log, 'pre_push_hook_base.test.sh', '27 passed, 1 failed'))]); arm('G-RED3', rc, o, 1, 'MISMATCH')
    rc, o = run(['python3', cp['gatelinesk2.py'], L('na.out', 'remote: x\nformat-gate: 3 files checked, OK\n')]); arm('G-NA', rc, o, 3, 'NOT APPLICABLE')
    rc, o = run(['python3', cp['gatelinesk2.py'], os.path.join(scr, 'no-such.out')]); arm('G-UNREAD', rc, o, 2, 'UNREADABLE')
    rc, o = run(['python3', cp['gatelinesg1.py'], T['push_log']]); arm('G-PRED', rc, o, 0, 'MISMATCH')
    tally = {}; logs = []
    for d in sorted(glob.glob(os.path.join(os.path.dirname(T['dir'].rstrip('/').rsplit('/', 1)[0]), '2026-10-0[6-9]*'))):
        logs += glob.glob(os.path.join(d, '**', '*-push.out'), recursive=True)
    for p in sorted(set(logs)):
        fc = first_count(open(p, encoding='utf-8', errors='replace').read(), 'run_shell_suites.test.sh'); tally[str(fc)] = tally.get(str(fc), 0) + 1
    print('G-PIN run_shell_suites first count over %d *-push.out logs dated 2026-10-06..09: %s (READY: 22 logs, all (59, 0); None = the block is absent)' % (len(set(logs)), tally))
    decl = T['declared']; dl = [l for l in open(decl).read().split('\n') if l.strip()]
    rc, o = run(['python3', cp['pathgatek2.py'], clone, base, head, decl]); arm('P-PASS', rc, o, 0, 'VERDICT: PASS')
    rc, o = run(['python3', cp['pathgatek2.py'], clone, develop, head, decl]); arm('P-RED1', rc, o, 1, 'VERDICT: FAIL')
    rc, o = run(['python3', cp['pathgatek2.py'], clone, base, head, L('decl7.txt', '\n'.join(dl[:-1]) + '\n')]); arm('P-RED2', rc, o, 1, 'VERDICT: FAIL')
    rc, o = run(['python3', cp['pathgatek2.py'], clone, base, develop, decl]); arm('P-RED3', rc, o, 1, 'VERDICT: FAIL')
    rc, o = run(['python3', cp['pathgatek2.py'], clone, base, head, L('decl9.txt', '\n'.join(dl + ['Blockchain/Dev/package-lock.json']) + '\n')]); arm('P-RED4', rc, o, 1, 'VERDICT: FAIL')
    rc, o = run(['python3', cp['pathgateg1.py'], clone, base, head, decl])
    print('INFO  P-PRED    predecessor pathgateg1.py on the real (base, head): rc %d | %s' % (rc, ' / '.join(l.strip() for l in o.split('\n') if re.search(r'PR0|VERDICT|FAIL', l))[:400]))
    rc, o = run(['python3', cp['namecheckk2.py']], cwd=scr); arm('N-PASS', rc, o, 0, '24/24 controls fired')
    src = open(cp['namecheckk2.py'], encoding='utf-8').read()
    a = 'ROW1_BRANCH = "feature/ks-1402-originate-resolves-holder-email-itself-k2-1"'
    assert src.count(a) == 1, 'N-RED1 anchor'
    r1 = os.path.join(scr, 'namecheck_red1.py'); open(r1, 'w').write(src.replace(a, a.replace('-k2-1"', '-g5-1"')))
    rc, o = run(['python3', r1], cwd=scr); arm('N-RED1', rc, o, (1, 2), 'POSITIVE CONTROL FIRED', None)
    forms = [('"branch segment":   "-k2-"', '"branch segment":   "-e2-"'), ('"worktree prefix":  "s-k2-"', '"worktree prefix":  "s-e2-"'),
             ('"ref namespace":    "seatk2"', '"ref namespace":    "seate2"'), ('"argv tag":         "-k2"', '"argv tag":         "-e2"')]
    s2 = src
    for x, y in forms:
        assert s2.count(x) == 1, 'N-RED2 anchor %r' % x; s2 = s2.replace(x, y)
    r2 = os.path.join(scr, 'namecheck_red2.py'); open(r2, 'w').write(s2)
    rc, o = run(['python3', r2], cwd=scr); arm('N-RED2', rc, o, (1, 2), 'BLIND on', None)
    print('INFO  N-INFO    namecheckk2 SUFFIX_ALLOWANCE line: %s (STANDING_LINES 2026-10-07: the length rule is len(declared) <= 92, no (#n))' %
          [l.strip() for l in src.split('\n') if l.startswith('SUFFIX_ALLOWANCE')])
    ps = open(cp['pushk2.sh'], encoding='utf-8').read().split('\n')
    def idx(rx): return next((i for i, l in enumerate(ps) if re.search(rx, l)), -1)
    i_gl, i_comp, i_take, i_rc, i_case = idx(r'push gate \$GL is ABSENT'), idx(r'py_compile "\$GL"'), idx(r'lockk2\.sh" take'), idx(r'GLRC=\$\?'), idx(r'^case "\$GLRC" in')
    ok = 0 <= i_gl < i_take and 0 <= i_comp < i_take and 0 <= i_rc < i_case
    print('%-5s TS-ORDER  pushk2.sh: absent-gate refusal :%d, py_compile :%d BEFORE lock take :%d; GLRC read :%d BEFORE `case "$GLRC"` :%d' % ('OK' if ok else 'BAD', i_gl + 1, i_comp + 1, i_take + 1, i_rc + 1, i_case + 1))
    if not ok: bad.append('TS-ORDER')
    pc = os.path.join(K['pr']['builder_records'], 'boot', 'push_console.txt')
    q = [l.strip() for l in open(pc, encoding='utf-8', errors='replace') if 'gatelinesk2 rc=' in l or 'RESULT:' in l] if os.path.isfile(pc) else ['push_console.txt ABSENT']
    print('INFO  TS-LOG    %s' % q[:3])
    print('ARMS %d bad %s' % (len(bad), bad or ''))
    return 1 if bad else 0


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    log = '=== a/run_shell_suites.test.sh ===\nrun_shell_suites: 59 passed, 0 failed\n=== pre_push_hook_base.test.sh ===\n28 passed, 0 failed\n'
    rep(first_count(log, 'run_shell_suites.test.sh') == (59, 0), 'first_count reads a block by basename')
    r = rewrite_block_count(log, 'run_shell_suites.test.sh', '49 passed, 0 failed'); rep(first_count(r, 'run_shell_suites.test.sh') == (49, 0), 'rewrite lands in its own block')
    rep(first_count(r, 'pre_push_hook_base.test.sh') == (28, 0), 'rewrite does not touch a sibling block')
    try: rewrite_block_count(log, 'absent.test.sh', '1 passed, 0 failed'); rep(False, 'an absent block was rewritten')
    except AssertionError: rep(True, 'PLANTED absent block REFUSES (no silent no-op)')
    try: must_be_outside('/Volumes/DevMASTER/!CODING/x', 'scratch'); rep(False, '!CODING scratch accepted')
    except SystemExit: rep(True, 'a !CODING scratch dir REFUSES')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if not A: print(__doc__); return 2
    if A[0] == '--selftest': return selftest()
    try:
        if A[0] == 'tools':
            return tools(req(A, '--scratch'), req(A, '--clone'), req(A, '--base', True), req(A, '--head', True), req(A, '--develop', True))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
