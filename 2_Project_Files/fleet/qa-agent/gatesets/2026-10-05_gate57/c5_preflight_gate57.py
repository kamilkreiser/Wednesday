#!/usr/bin/env python3
"""c5_preflight_gate57.py — gate57 C5: the push preflight legs the seat reported, QUOTED AS PRINTED, and what they do NOT establish.
"12/15 legs ran, 3 SKIPPED" is NOT a pass (preflight.sh says so itself: "This is NOT a pass. Do not quote it as one — say which legs ran").
MODES
  static  --repo <clone> [--ready <READY file>]   (git objects + the READY text; no run)
    L1 QUOTED AS PRINTED: each kit preflight.ready_quotes line is found in the READY, and compared BYTE-FOR-BYTE with the format string the
       base scripts print (preflight.sh's verdict, run-shell-suites.sh:291, run-code-guards.sh:224). A dash where the script prints an EM DASH
       (U+2014) is a transcription, reported by index — the gate rules whether it matters (the figures are what it tests).
    L2 NOT A PASS: the READY's verdict is INCOMPLETE (12 of 15 ran, 3 skipped); the script's own "This is NOT a pass" line is at base.
    L3 THE SKIPPED LEGS ARE PRINTABLE: preflight.sh at base prints, on the line right after the INCOMPLETE verdict, `  legs<N N N> — local
       stack not up…` (stack class) and/or `  legs<N…> — environment…` (advisory class). The READY's "NOT NAMED, on purpose … .githooks/
       pre-push:273" quotes a COMMENT in the hook; the verdict itself names them. FAIL = the READY omits a line the script prints.
    L4 THE CANDIDATES: skip_stack call sites map to legs {3, 4, 8} (exactly 3 at base); skip_advisory sites to {1, 3, 4, 6, 7, 8} plus the
       delegating legs (2, 12). "3 SKIPPED" with "no local stack up" fits {3, 4, 8} IF all three are stack-class — an inference, printed as one.
  run     --repo --worktree <YOUR installed scratch worktree> --out <dir> --head <sha>
    R1 runs `bash scripts/preflight/preflight.sh` in Blockchain/Dev of YOUR worktree at --head (no stack is started: HOLD), captures the
       verdict and the `legs …` lines verbatim, and prints which legs ran / skipped and why. Nothing is pushed. (~6-9 min: leg 14 runs every
       shell suite.)
  --selftest  the L1 / L3 judges on planted READY texts: an em-dash-exact quote, a figure changed (12/15 -> 13/15), the legs line quoted,
              a missing quote.
Usage: c5_preflight_gate57.py static --repo <clone> [--ready f]   |   run --repo --worktree --out --head   |   --selftest --repo <clone>
rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, wgit, now, Checks, opt_factory, show, has_commit, guard_scratch, guard_out, run

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); CUT = K['cut_base']; PF = K['preflight']
READY = opt('--ready', K['seat_ready'])
MODE = next((m for m in ('static', 'run') if m in A), None)
EM = '—'


def base_texts():
    pre = show(REPO, CUT, PF['script']); rss = show(REPO, CUT, 'Blockchain/Dev/scripts/run-shell-suites.sh'); rcg = show(REPO, CUT, 'Blockchain/Dev/scripts/run-code-guards.sh')
    return pre, rss, rcg


def judge_static(C, ready, pre, rss, rcg):
    fmts = [('preflight.sh verdict', re.compile(r'^PREFLIGHT INCOMPLETE — (\d+)/(\d+) legs ran, (\d+) SKIPPED\. Nothing failed\.$'), 'echo "PREFLIGHT INCOMPLETE — $n_ran/$TOTAL_LEGS legs ran, $n_skipped SKIPPED. Nothing failed."' in pre),
            ('run-shell-suites.sh:291', re.compile(r'^shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)$'), 'echo "shell suites: $pass passed, $fail failed, $skip skipped (of ${#reached[@]})"' in rss),
            ('run-code-guards.sh:224', re.compile(r'^OK — (\d+) code guards passed\.$'), 'echo "OK — $ran code guards passed."' in rcg)]
    rows = []; exact = True; found_all = True
    for q, (src, rx, in_base) in zip(PF['ready_quotes'], fmts):
        found = q in ready; found_all &= found and in_base
        m = rx.match(q); m2 = rx.match(q.replace(' - ', ' ' + EM + ' ', 1))
        exact &= m is not None
        idx = [i for i, ch in enumerate(q) if ch == '-' and q[i - 1:i + 2] == ' - ']
        rows.append('%r in READY %s | %s format at base %s | byte-exact %s%s' % (q[:48], found, src, in_base, m is not None,
                    '' if m else (' | matches with an EM DASH at index %s: %s (a TRANSCRIPTION of U+2014 to "-")' % (idx, m2 is not None))))
    C.chk('L1 quoted as printed', found_all and exact, ' || '.join(rows))
    m = re.search(r'PREFLIGHT INCOMPLETE [-—] (\d+)/(\d+) legs ran, (\d+) SKIPPED', ready)
    ran, tot, sk = (int(x) for x in m.groups()) if m else (None, None, None)
    C.chk('L2 NOT a pass', m is not None and ran + sk == tot == PF['total_legs'] and 'echo "  This is NOT a pass.' in pre,
          'READY verdict %s/%s ran, %s skipped (TOTAL_LEGS %d) | preflight.sh prints "This is NOT a pass": %s' % (ran, tot, sk, PF['total_legs'], 'echo "  This is NOT a pass.' in pre))
    prints_legs = 'echo "  legs$SKIPPED_STACK — local stack not up' in pre and 'echo "  legs$SKIPPED_ADVISORY — environment' in pre
    quoted = re.search(r'(?m)^\s*"?\s*legs( \d+)+ [-—] ', ready) is not None
    claim = re.search(r'NOT NAMED', ready) is not None
    C.chk('L3 skipped legs named', quoted, 'preflight.sh at %s PRINTS the skipped legs right after the verdict (stack line + advisory line): %s | the READY quotes a `legs N N N` line: %s | the READY says they are "NOT NAMED, on purpose": %s (it cites .githooks/pre-push:%d, a COMMENT; the verdict names them)' % (
        CUT[:12], prints_legs, quoted, claim, PF['prepush_line']))
    L = pre.split('\n'); leg = None; stack = []; adv = []; deleg = []
    for l in L:
        h = re.match(r'^step "(\d+)/15', l)
        if h: leg = h.group(1)
        if re.match(r'^\s*skip_stack\s*$', l): stack.append(leg)
        if re.match(r'^\s*skip_advisory ', l): adv.append(leg)
        if leg and re.search(r'\brun_delegated\b', l) and not l.startswith('run_delegated()'): deleg.append(leg)
    C.chk('L4 candidate legs', sorted(set(stack)) == PF['stack_legs'] and len(stack) == 3, 'skip_stack sites by leg %s (kit %s) | skip_advisory sites by leg %s | delegating legs (sub-script advisory skips) %s | INFERENCE: "3 SKIPPED" with no stack up fits {3, 4, 8} only if all three are stack-class; NOT MEASURED by the seat' % (
        stack, PF['stack_legs'], sorted(set(adv), key=int), sorted(set(deleg), key=int)))


if '--selftest' in A:
    pre, rss, rcg = base_texts(); ready = open(READY, encoding='utf-8').read(); ok = n = 0
    def arm(name, txt, want):
        global ok, n
        buf = io.StringIO(); C = Checks()
        with contextlib.redirect_stdout(buf): judge_static(C, txt, pre, rss, rcg)
        f = C.failed(); g = (sorted(f) == sorted(want))
        n += 1; ok += g; print('SELFTEST %s %s: want failures %s | got %s' % ('OK' if g else 'MISS', name, want or 'NONE', f or 'NONE'))
        if not g: print(buf.getvalue()[:900])
    q0, q1, q2 = PF['ready_quotes']
    arm('S0 the real READY', ready, ['L1 quoted as printed', 'L3 skipped legs named'])
    em = ready.replace(q0, q0.replace(' - ', ' ' + EM + ' ')).replace(q2, q2.replace(' - ', ' ' + EM + ' ')) + '\n  legs 3 4 8 — local stack not up; you can clear this by starting it.\n'
    saved = PF['ready_quotes'][:]; PF['ready_quotes'] = [q0.replace(' - ', ' ' + EM + ' '), q1, q2.replace(' - ', ' ' + EM + ' ')]
    arm('S1 em-dash-exact quotes + the legs line', em, [])
    PF['ready_quotes'] = saved
    arm('S2 a quote missing from the READY', ready.replace(q1, 'shell suites: (not quoted)'), ['L1 quoted as printed', 'L3 skipped legs named'])
    arm('S3 the verdict says 13/15 with 3 skipped (does not add up)', ready.replace('12/15 legs ran', '13/15 legs ran'), ['L1 quoted as printed', 'L2 NOT a pass', 'L3 skipped legs named'])
    print('SELFTEST %s %d of %d' % ('OK' if ok == n else 'BROKEN', ok, n)); raise SystemExit(0 if ok == n else 1)

if MODE is None:
    print(__doc__); raise SystemExit(2)
print('c5_preflight_gate57 %s %s | repo %s | READY %s' % (MODE, now(), REPO, READY))
C = Checks()
if MODE == 'static':
    pre, rss, rcg = base_texts(); judge_static(C, open(READY, encoding='utf-8').read(), pre, rss, rcg)
    for q in PF['ready_quotes']: print('INFO quoted by the seat: %r' % q)
else:
    WT = guard_scratch(opt('--worktree') or '', 'worktree'); OUT = guard_out(opt('--out')); H = opt('--head')
    if not H or not has_commit(REPO, H): print('REFUSING: --head must be a commit in the clone'); raise SystemExit(2)
    if wgit(WT, 'status', '--porcelain').strip(): print('REFUSING: the worktree is not clean'); raise SystemExit(2)
    wgit(WT, 'checkout', '--quiet', '--detach', H)
    rc, o, e = run(['bash', 'scripts/preflight/preflight.sh'], os.path.join(WT, 'Blockchain', 'Dev'), os.path.join(OUT, 'c5_preflight_%s' % H[:12]), timeout=3600)
    lines = (o + e).split('\n'); v = [l for l in lines if l.startswith('PREFLIGHT ')]; lg = [l for l in lines if re.match(r'^\s+legs( \d+)+ ', l)]
    for l in v + lg: print('VERBATIM %s' % l)
    m = re.search(r'(\d+)/(\d+) legs ran', ' '.join(v))
    C.chk('R1 preflight run', bool(v), 'rc %d | verdict %s | skipped-legs lines %s | legs ran %s of %s (this is the GATE\'s run in its own worktree, no stack started)' % (rc, v, lg, m.group(1) if m else '?', m.group(2) if m else '?'))
    st = wgit(WT, 'status', '--porcelain').strip()
    print('INFO worktree status after the run: %r' % st[:300])
    wgit(WT, 'checkout', '--quiet', '--detach', CUT)
n = C.nfail()
print('C5 PREFLIGHT %s %s: %d FAIL of %d checks' % (MODE.upper(), 'PASS' if n == 0 else 'FAIL', n, len(C.res)))
raise SystemExit(1 if n else 0)
