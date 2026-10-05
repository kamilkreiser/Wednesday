#!/usr/bin/env python3
"""c2_relanded_gate64.py — C2 THROUGH-CODE: what #1389 re-landed from #1250's round-2 blobs byte-for-byte, and what KS-1330 changed on
top, NOTHING ELSE. READ verbs only (lib_gate64.git). Compares by LINES (difflib, no fuzz).

  R1  provenance: #1250's head 2b8dcb824dd2 carries the kit round-2 blobs (runner 8eef1c4877b3, test 9c4a87f0a97c), and develop's two
      blobs == #1250's base 6e2a00bfed57 blobs (develop never moved either path since #1250 was cut, so "re-land" is well defined)
  R2  RUNNER r2 -> head: +/- == kit (20/1); the ONLY non-comment change is the whitespace-only re-indent of the `rss_suite_log=` line
      (kit list, exact); every other changed line is a comment, and the added comments carry the `KS-1330 item 3` header
  R3  TEST r2 -> head: +/- == kit (51/11); the non-comment lines added and removed == the kit's enumerated KS-1330 item 1 / item 2
      code lines EXACTLY (multiset; a stray code line anywhere FAILS)
  R4  ITEM 1 structure at head: 0 `_skip=` carrying `RULE 2`; 0 conditions on `"$_t" = pid`; the INT skip is gated ONLY by
      `[ "$INT_INSTALLABLE" != yes ]` (exactly once); INT_INSTALLABLE comes from `sig_installable INT`; `set -m` sits inside
      `signal_run` BEFORE its backgrounded `run-shell-suites.sh &` launch
  R5  ITEM 1 comments: the old matrix bullet "unreachable by RULE 2, always" is GONE; RULE 2 now reads "ONLY WHILE JOB CONTROL IS
      OFF" (once); the PID bullet says it is reachable because signal_run uses job control
  R6  ITEM 2: T1302S_SLEEP / T1302S_KILL_LATENCY_MAX defined once each, the bound derived from the sleep, the slow fixture uses the
      constant, and the latency cell is its OWN `check` (not folded into the interrupt cell's AND)
  INFO the interrupt cell's exact pass condition (does it assert rc == 130, or only rc != 0?) and the item-3 runner header's two
       MEASURED claims, printed for the gate to rule against what C3 measures; the re-indent of `rss_suite_log=` (column 0 inside the loop)

Usage: c2_relanded_gate64.py --repo <git dir> [--head <sha>]  |  --selftest [--repo <git dir>]
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import collections, difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate64 import K, git, Tally, SCRATCH

RUN, TST = K['runner'], K['test']
P1250 = K['pr1250']


def iscode(l): return bool(l.strip()) and not l.strip().startswith('#')


def delta(a, b):
    A, B = a.split('\n'), b.split('\n')
    add, rem, cadd, crem = [], [], [], []
    for o in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if o[0] == 'equal': continue
        rem += A[o[1]:o[2]]; add += B[o[3]:o[4]]
    cadd = [l for l in add if iscode(l)]; crem = [l for l in rem if iscode(l)]
    return add, rem, cadd, crem


def measure(repo, head):
    b = lambda rev, p: git(repo, 'show', '%s:%s' % (rev, p))
    rp = lambda rev, p: git(repo, 'rev-parse', '%s:%s' % (rev, p)).strip()
    return {'r2_ids_1250': {p: rp(P1250['head'], p) for p in (RUN, TST)},
            'dev_ids': {p: rp(K['develop'], p) for p in (RUN, TST)},
            'base1250_ids': {p: rp(P1250['base_commit'], p) for p in (RUN, TST)},
            'r2': {p: git(repo, 'cat-file', '-p', K['r2_blobs'][p]) for p in (RUN, TST)},
            'head': {p: b(head, p) for p in (RUN, TST)}}


def fn_body(text, name):
    L = text.split('\n'); s = [i for i, l in enumerate(L) if l.startswith(name + '()')]
    if len(s) != 1: return None
    for j in range(s[0] + 1, len(L)):
        if L[j] == '}': return L[s[0]:j + 1]
    return None


def judge(m, t):
    t.check('R1', m['r2_ids_1250'] == K['r2_blobs'] and m['dev_ids'] == m['base1250_ids'],
            "#1250 head blobs %s == kit r2 %s; develop blobs %s == #1250 base blobs %s" % (
                {os.path.basename(p): v[:12] for p, v in m['r2_ids_1250'].items()}, {os.path.basename(p): v[:12] for p, v in K['r2_blobs'].items()},
                {os.path.basename(p): v[:12] for p, v in m['dev_ids'].items()}, {os.path.basename(p): v[:12] for p, v in m['base1250_ids'].items()}))
    # R2 runner
    add, rem, cadd, crem = delta(m['r2'][RUN], m['head'][RUN])
    ws_only = sorted(l.strip() for l in cadd) == sorted(l.strip() for l in crem)
    hdr = any('KS-1330 item 3' in l for l in add if not iscode(l))
    t.check('R2', [len(add), len(rem)] == K['r2_delta_numstat'][RUN] and cadd == K['r2_code_added'][RUN] and crem == K['r2_code_removed'][RUN]
            and ws_only and hdr,
            'runner r2->head +%d/-%d (kit %s); code added %d removed %d, == kit %s, whitespace-only %s; item-3 header %s; code added %s' % (
                len(add), len(rem), K['r2_delta_numstat'][RUN], len(cadd), len(crem),
                cadd == K['r2_code_added'][RUN] and crem == K['r2_code_removed'][RUN], ws_only, hdr, [l[:70] for l in cadd]))
    # R3 test
    add, rem, cadd, crem = delta(m['r2'][TST], m['head'][TST])
    ca, cr = collections.Counter(cadd), collections.Counter(crem)
    ka, kr = collections.Counter(K['r2_code_added'][TST]), collections.Counter(K['r2_code_removed'][TST])
    t.check('R3', [len(add), len(rem)] == K['r2_delta_numstat'][TST] and ca == ka and cr == kr,
            'test r2->head +%d/-%d (kit %s); code lines added %d removed %d; unexpected added %s removed %s; kit lines absent added %s removed %s' % (
                len(add), len(rem), K['r2_delta_numstat'][TST], len(cadd), len(crem), [l[:80] for l in (ca - ka)], [l[:80] for l in (cr - kr)],
                [l[:80] for l in (ka - ca)], [l[:80] for l in (kr - cr)]))
    T = m['head'][TST]; L = T.split('\n'); code = [l for l in L if iscode(l)]
    r2skip = [l for l in code if '_skip=' in l and 'RULE 2' in l]
    pidcond = [l for l in code if re.search(r'\[\s*"\$_t"\s*=\s*pid\s*\]', l)]
    intgate = [l for l in code if l.strip() == 'if [ "$_s" = INT ] && [ "$INT_INSTALLABLE" != yes ]; then']
    inst = [l for l in code if l.strip() == 'INT_INSTALLABLE="$(sig_installable INT)"']
    body = fn_body(T, 'signal_run') or []
    sm = [i for i, l in enumerate(body) if l.strip() == 'set -m']
    bg = [i for i, l in enumerate(body) if re.search(r'bash scripts/run-shell-suites\.sh .*&\s*$', l)]
    t.check('R4', not r2skip and not pidcond and len(intgate) == 1 and len(inst) == 1 and len(sm) == 1 and len(bg) == 1 and sm[0] < bg[0],
            'RULE-2 _skip lines %d; pid conditions %d; RULE-1-only INT gate %d (want 1); INT_INSTALLABLE from sig_installable %d; '
            'signal_run: `set -m` at body+%s, background launch at body+%s' % (len(r2skip), len(pidcond), len(intgate), len(inst), sm, bg))
    old = T.count('unreachable by RULE 2, always'); new = T.count('ONLY WHILE JOB CONTROL IS'); reach = T.count('reachable here, because `signal_run` uses job control')
    t.check('R5', old == 0 and new == 1 and reach == 1, 'old matrix bullet %d (want 0); RULE 2 conditional %d (want 1); PID bullet reachable %d (want 1)' % (old, new, reach))
    sl = [l for l in code if l.startswith('T1302S_SLEEP=')]; mx = [l for l in code if l.startswith('T1302S_KILL_LATENCY_MAX=')]
    usesl = [l for l in code if 'suite_with' in l and '"sleep $T1302S_SLEEP"' in l]
    latchk = [i for i, l in enumerate(L) if l.strip().startswith('check "KS-1330: SIG$_s to the $_t')]
    intr = [i for i, l in enumerate(L) if l.strip().startswith('if [ "$_rc" != 0 ]')]
    t.check('R6', len(sl) == 1 and mx == ['T1302S_KILL_LATENCY_MAX=$(( T1302S_SLEEP / 2 ))'] and len(usesl) == 1 and len(latchk) == 2 and len(intr) == 1
            and all(i > intr[0] for i in latchk) and '_lat' not in L[intr[0]],
            'SLEEP %s; bound %s; slow fixture uses the constant %d; latency check lines %d (OK + FAIL branch) after the interrupt cell %s; '
            'interrupt cell condition mentions _lat: %s' % (sl, mx, len(usesl), len(latchk), intr, any('_lat' in L[i] for i in intr)))
    t.info('ARM-RC', 'the interrupt cell passes on: %r — it asserts rc != 0 (and != 999), NOT rc == 130; the 130/143 the body quotes '
                     'appear only in the cell LABEL (`rc $_rc`)' % (L[intr[0]].strip() if intr else None))
    R = m['head'][RUN].split('\n')
    claims = [l.strip() for l in R if re.search(r'IGNORED in the suite|stdin is /dev/null|MEASURED', l)]
    t.info('ITEM3', 'runner header claims: %s' % claims)
    ind = [l for l in R if l.lstrip().startswith('rss_suite_log="$(mktemp')]
    t.info('INDENT', 'rss_suite_log line(s) at head: %s (r2 had two-space indent inside the for-loop)' % [repr(l[:12]) for l in ind])


def selftest(repo):
    import copy, io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    real = measure(repo, K['head'])
    def run(m):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(m, t)
        return t
    t0 = run(real); ok = int(not t0.fails and t0.n == 6); total = 1
    print('SELFTEST %s T0 the REAL blobs (#1250 r2 vs head a7f5965a7b3f): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    def sub(s, a, b):
        assert s.count(a) == 1, 'tamper anchor must occur EXACTLY once (found %d): %r' % (s.count(a), a[:60]); return s.replace(a, b)
    old_gate = ('  if [ "$_s" = INT ] && [ "$_t" = pid ]; then\n'
                '    _skip="RULE 2: bash ignores SIGINT in a background job (trap -p INT empty there, rc 0), so no handler can exist to signal. A real terminal ^C hits the process GROUP — the arm below."\n'
                '  elif [ "$_s" = INT ] && [ "$INT_INSTALLABLE" != yes ]; then\n')
    arms = [
        ('runner: an extra code line', RUN, lambda s: sub(s, '  rss_suite_pid=$!\n', '  rss_suite_pid=$!\n  echo extra\n'), ['R2']),
        ('runner: item-3 header removed', RUN, lambda s: sub(s, '# KS-1330 item 3 — THE TWO', '# THE TWO'), ['R2']),
        ('runner: a re-landed code line altered', RUN, lambda s: sub(s, '    kill -TERM "$rss_suite_pid" 2>/dev/null\n', '    kill -KILL "$rss_suite_pid" 2>/dev/null\n'), ['R2']),
        ('test: ITEM 1 reverted (the unconditional RULE-2 gate restored)', TST, lambda s: sub(s, '  if [ "$_s" = INT ] && [ "$INT_INSTALLABLE" != yes ]; then\n', old_gate), ['R3', 'R4']),
        ('test: `set -m` removed from signal_run', TST, lambda s: sub(s, '    set -m\n', ''), ['R3', 'R4']),
        ('test: old matrix bullet restored', TST, lambda s: sub(s, "#   * SIGINT to the runner's PID — reachable here, because `signal_run` uses job control\n",
                                                         "#   * SIGINT to the runner's PID — unreachable by RULE 2, always, in this harness.\n"), ['R5']),
        ('test: latency bound hard-coded (not derived)', TST, lambda s: sub(s, 'T1302S_KILL_LATENCY_MAX=$(( T1302S_SLEEP / 2 ))', 'T1302S_KILL_LATENCY_MAX=11'), ['R3', 'R6']),
        ('test: a stray code line outside the KS-1330 items', TST, lambda s: sub(s, 'PRIMARY_ROOT="${ROOTS[0]}"\n', 'PRIMARY_ROOT="${ROOTS[0]}"\n: stray\n'), ['R3']),
    ]
    for name, path, fn, want in arms:
        m = copy.deepcopy(real); m['head'][path] = fn(m['head'][path]); assert m['head'][path] != real['head'][path], 'tamper did not land: ' + name
        p = os.path.join(fx, 'c2_arm_%02d_%s' % (total, os.path.basename(path))); open(p, 'w').write(m['head'][path])
        t = run(m); total += 1; g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s (landed, fixture %s): want FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, t.fails))
    m = copy.deepcopy(real); m['r2_ids_1250'][RUN] = '0' * 40; t = run(m); total += 1; g = 'R1' in t.fails; ok += g
    print('SELFTEST %s #1250 head blob is not the kit r2 blob: want FAIL R1 | got %s' % ('OK' if g else 'MISS', t.fails))
    m = copy.deepcopy(real); m['dev_ids'][TST] = '1' * 40; t = run(m); total += 1; g = 'R1' in t.fails; ok += g
    print("SELFTEST %s develop moved the test since #1250's base: want FAIL R1 | got %s" % ('OK' if g else 'MISS', t.fails))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A or not A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo', K['checkout'])
    if '--selftest' in A: raise SystemExit(selftest(repo))
    head = opt('--head', K['head'])
    print('c2_relanded_gate64 repo %s head %s r2 %s' % (repo, head, {os.path.basename(p): v[:12] for p, v in K['r2_blobs'].items()}))
    t = Tally(); judge(measure(repo, head), t); raise SystemExit(t.end())
