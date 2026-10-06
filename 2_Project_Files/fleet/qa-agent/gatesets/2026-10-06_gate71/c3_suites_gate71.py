#!/usr/bin/env python3
r"""c3_suites_gate71.py — the WHOLE SHELL-SUITE SET for #1398 (KS-1136). THE HEAD IS A PARAMETER.

MODES
  list      --wt-base <wt AT the base> --wt-head <wt AT the head>   L1 `run-shell-suites.sh --list` 67 at base, 68 at head; L2 the
            difference is EXACTLY the new suite (1 at head, 0 at base); L3 `--check-unreached` rc 0 at the head.
  full      --wt <wt AT the head> --out <FRESH dir>   runs `bash Blockchain/Dev/scripts/run-shell-suites.sh` (stdout+stderr to a FILE,
            rc read on its own line), then `classify` on that log. Expected: 68 passed, 0 failed, 0 skipped (of 68) — IF the worktree has
            `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared` done (X1); without them the KS-168 six red, as on the
            runner. Every red is then re-run ALONE at the BASE (`--wt-base`): red at base too = pre-existing (named, never a pass);
            green at base and red at head = THIS PR's (BLOCKS).
  classify  --log <a runner log: local, or a CI `Code Security Gates` job log>   attributes every `N passed, M failed` summary to its
            `=== <path> ===` header (the structure the runner prints), reads the verdict line and every `FAILED:` line, and compares the
            failing set with the KS-168 six. A count that agrees while the SET differs is a FAIL. Reports the new suite's own summary.
            CONTROLS: `##[group]` / header count > 0 (the log was read), a fabricated header name absent.
  --selftest  the attribution parser on runner-format text built from the runner's own echo lines (verbatim from run-shell-suites.sh at
            the head: `=== rel ===`, `shell suites: …`, `FAILED: rel`), with planted arms: a passing line that merely contains "failed",
            a seventh red, a count-equal set-different red. Each must be caught.
rc 0 pass / 1 FAIL / 2 refused."""
import os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate71 import K, P, Tally, git, opt

SS = K['shell_suites']; RUNNER = SS['runner']; NEW = K['product']['suite']
VERDICT = re.compile(SS['verdict_rx'], re.M); HEADER = re.compile(SS['header_rx'])
SUMMARY = re.compile(r'^\s*(\d+) passed, (\d+) failed\b')


def stem(path): return os.path.basename(path).replace('.test.sh', '')


def attribute(text):
    """{suite path: (passed, failed) of the LAST per-suite summary line under its header, or None}; verdict; FAILED list; header count."""
    cur = None; per = {}; hdrs = 0
    for l in text.split('\n'):
        l2 = re.sub(r'^\d{4}-\d\d-\d\dT[\d:.]+Z ', '', l)          # a CI log prefixes every line with a timestamp
        h = HEADER.match(l2)
        if h: cur = h.group(1); per[cur] = None; hdrs += 1; continue
        if l2.startswith('shell suites: '): cur = None
        s = SUMMARY.match(l2)
        if s and cur: per[cur] = (int(s.group(1)), int(s.group(2)))
    lines = [re.sub(r'^\d{4}-\d\d-\d\dT[\d:.]+Z ', '', l) for l in text.split('\n')]
    v = [VERDICT.match(l) for l in lines]; v = [m for m in v if m]
    failed = [l[len('FAILED: '):].strip() for l in lines if l.startswith('FAILED: ')]
    return per, (tuple(int(x) for x in v[-1].groups()) if v else None), failed, hdrs


def classify_text(text, t):
    per, verdict, failed, hdrs = attribute(text)
    t.check('X0', hdrs > 0 and 'GATE71-FABRICATED-SUITE' not in per, 'headers read: %d (CONTROL > 0) | fabricated header absent: True' % hdrs)
    t.check('X1', verdict is not None, 'verdict line: %s' % (verdict,))
    if not verdict: return
    p, f, s, n = verdict
    fs = sorted(stem(x) for x in failed); known = sorted(SS['known_runner_reds_ks168'])
    t.check('X2', len(failed) == f and n == SS['count_head'], 'FAILED lines %d == verdict failed %d; denominator %d == %d' % (len(failed), f, n, SS['count_head']))
    seventh = sorted(set(fs) - set(known))
    t.check('X3', not seventh, 'failing SET %s | known KS-168 six %s | NOT in the six (a seventh red BLOCKS unless classified): %s' % (
        fs, 'subset' if set(fs) <= set(known) else 'DIFFERS', seventh or 'none'))
    mine = [k for k in per if k.endswith(os.path.basename(NEW))]
    t.check('X4', len(mine) == 1 and per[mine[0]] == (K['product']['suite_cells'], 0), 'the new suite under its own header: %s' % ([per.get(m) for m in mine] or 'ABSENT'))
    t.info('X5', 'verdict %d passed, %d failed, %d skipped (of %d); cause line %r present: %s' % (p, f, s, n, SS['known_runner_cause_line'], SS['known_runner_cause_line'] in text))


def run_list(wtb, wth):
    t = Tally(); out = {}
    for side, wt in (('base', wtb), ('head', wth)):
        p = subprocess.run(['bash', os.path.join(wt, RUNNER), '--list'], capture_output=True, text=True)
        out[side] = [l for l in p.stdout.split('\n') if l]
        print('LIST %s rc %d: %d suites' % (side, p.returncode, len(out[side])))
    t.check('L1', len(out['base']) == SS['count_base'] and len(out['head']) == SS['count_head'], '%d -> %d (kit %d -> %d)' % (len(out['base']), len(out['head']), SS['count_base'], SS['count_head']))
    t.check('L2', sorted(set(out['head']) - set(out['base'])) == [NEW] and not set(out['base']) - set(out['head']), 'difference == exactly %s' % NEW)
    p = subprocess.run(['bash', os.path.join(wth, RUNNER), '--check-unreached'], capture_output=True, text=True)
    t.check('L3', p.returncode == 0 and 'OK' in p.stdout, '--check-unreached at the head rc %d: %s' % (p.returncode, p.stdout.strip().split('\n')[-1][:120]))
    return t.end()


def run_full(wt, wtb, out):
    t = Tally(); log = os.path.join(out, 'run_shell_suites_head.log')
    t0 = time.time()
    with open(log, 'wb') as fo:
        rc = subprocess.run(['bash', os.path.join(wt, RUNNER)], cwd=wt, stdout=fo, stderr=subprocess.STDOUT).returncode
    open(log + '.rc', 'w').write('%d\n' % rc)
    print('RUN rc %d in %.0f s, log %s' % (rc, time.time() - t0, log))
    text = open(log, encoding='utf-8', errors='replace').read()
    classify_text(text, t)
    per, verdict, failed, _ = attribute(text)
    t.check('F1', verdict is not None and verdict[:3] == (SS['count_head'], 0, 0) and rc == 0, 'want 68 passed, 0 failed, 0 skipped (of 68), rc 0: got %s rc %d' % (verdict, rc))
    for rel in failed:
        if not wtb: t.info('F2', 'red %s NOT re-run at base (no --wt-base)' % rel); continue
        p = subprocess.run(['bash', os.path.join(wtb, rel)], cwd=wtb, capture_output=True, text=True)
        open(os.path.join(out, 'base_%s.log' % stem(rel)), 'w').write(p.stdout + p.stderr)
        t.check('F2-%s' % stem(rel), p.returncode != 0, 'red at the head; ALONE at the BASE rc %d -> %s' % (p.returncode, 'PRE-EXISTING (named, not a pass)' if p.returncode else 'GREEN AT BASE: THIS PR CAUSED IT'))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    six = SS['known_runner_reds_ks168']
    def mk(reds, extra_pass_line=False, ts=False):
        L = ['git environment: cleared for the suites: (none were set)']
        suites = ['Blockchain/Dev/scripts/__tests__/%s.test.sh' % s for s in six + ['a', 'b']] + [NEW]
        for s in suites:
            L += ['', '=== %s ===' % s]
            if extra_pass_line and stem(s) == 'a': L += ['  ok   the retry failed once then passed']
            r = stem(s) in reds
            L += ['', '  %d passed, %d failed' % ((5, 1) if r else ((6, 0) if s == NEW else (4, 0)))]
        L += ['', 'shell suites: %d passed, %d failed, 0 skipped (of %d)' % (len(suites) - len(reds), len(reds), SS['count_head'])]
        L += ['FAILED: Blockchain/Dev/scripts/__tests__/%s.test.sh' % s for s in reds]
        if ts: L = ['2026-10-06T12:00:00.0000000Z ' + l for l in L]
        return '\n'.join(L)
    def verdict(text):
        t = Tally()
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): classify_text(text, t)
        return t.fails
    rep(not verdict(mk(six)), 'the known six red, my suite 6/0: classified, 0 FAIL')
    rep(not verdict(mk(six, ts=True)), 'the same with CI timestamps on every line: 0 FAIL')
    rep(not verdict(mk(six, extra_pass_line=True)), 'a PASSING line containing the word "failed" does not invent a red (R 3rd self-caught #4)')
    rep('X3' in verdict(mk(six + ['a'])), 'PLANTED seventh red FAILS X3')
    rep('X3' in verdict(mk(six[:5] + ['a'])), 'PLANTED count-equal (6) but SET-different red FAILS X3')
    rep('X1' in verdict('=== x ===\n  1 passed, 0 failed\n'), 'a log with NO verdict line FAILS X1')
    rep('X0' in verdict('nothing here'), 'an unread / empty log FAILS X0 (0 headers)')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    if A[0] == 'list':
        if not (opt(A, '--wt-base') and opt(A, '--wt-head')): print(__doc__); return 2
        return run_list(opt(A, '--wt-base'), opt(A, '--wt-head'))
    if A[0] == 'full':
        wt, out = opt(A, '--wt'), opt(A, '--out')
        if not (wt and out): print(__doc__); return 2
        os.makedirs(out, exist_ok=True)
        if os.listdir(out): print('REFUSED: --out %s not empty' % out); return 2
        head = opt(A, '--head', P['head_expected'])
        if git(wt, 'rev-parse', 'HEAD').strip() != head: print('REFUSED: --wt is not AT %s' % head[:12]); return 2
        return run_full(wt, opt(A, '--wt-base'), out)
    if A[0] == 'classify':
        if not opt(A, '--log'): print(__doc__); return 2
        t = Tally(); classify_text(open(opt(A, '--log'), encoding='utf-8', errors='replace').read(), t); return t.end()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
