#!/usr/bin/env python3
"""c3_run_gate61.py — gate61 C3 RUN for #1383 (KS-1401): the author's suite on a REAL PostgreSQL 15 keg, red-first, three tampers of 049,
the preflight legs that read the new files, and (optional) ks949. Runs ONLY in YOUR scratch worktree (lib guard_scratch refuses anything
under /Volumes/DevMASTER); the worktree must be clean. The suite starts and stops its OWN socket-only cluster in its own mkdtemps
(listen_addresses=''); it never connects to 127.0.0.1:5432. THE DRAFTER NEVER RAN A MODE BELOW (no PostgreSQL was started at drafting):
only --selftest, on synthetic outputs.
MODES
  suite    --worktree <wt> --out <dir> [--runs 3] [--pgbin <keg bin>]
    S1 at the HEAD: rc 0, the summary `KS-1401: 53 passed, 0 failed (of 53 assertions over 11 cells)`, an INDEPENDENT count of PASS lines
       == 53 and of FAIL lines == 0, no SKIP line, the keg line names PostgreSQL 15.x, KS1401_FLOOR=53 set (a dropped cell fails rc 2).
    S2 NON-BYPASS: the suite's own `CONTROL secuura_app is false/false` PASS line is present (the reds bind; rolbypassrls=false,
       rolsuper=false). The gate's probe (c3b) re-measures it independently.
    S3 TIMING: wall-clock per run, the host (`scutil --get LocalHostName`, else uname -n), the UTC date, the keg version — the doc rows'
       "12-13 s on Kamils-Mac-Studio" is a claim; this is the measurement.
  redfirst --repo <clone> --worktree <wt> --out <dir> [--pgbin]
    R1 worktree at DEVELOP (49 migrations, no 049): the HEAD's suite written in (mode 0755) plus a STUB 049 (`SELECT 1;`, kit
       suite.stub_049) so the suite measures the BASE state end to end. The base-state arms PASS (kit red_at_base_pass: the fixture ==
       B 50th, the non-bypass control, the three reds) AND every head-state arm in kit red_at_base_fail FAILS by its own message (no
       backfill reported; charge_events / certifications readings; policy fidelity on charge_events and certifications; the cross-tenant
       leak; no-GUC 8; certifications default-deny; cross-tenant INSERT not refused). All 11 cells ran; no SKIP.
    R1b both planted files MOVED to <out>/quarantine/ (never deleted); `git status --porcelain` empty; the worktree back at the head.
  tamper   --repo --worktree --out [--pgbin]   (at the HEAD; kit suite.tampers T-FORCE, T-QUAL, T-GUARD, each INDEPENDENT)
    Tn each: the anchor occurs EXACTLY once (a unique anchor or the restore is ambiguous); the tamper LANDED (re-read: anchor 0 times,
       replacement present); the suite run; EVERY must_fail message present among the FAIL lines; the file restored BY CONTENT and its
       sha256 == the sha256 of `git show <head>:<049>`; `git status --porcelain` empty. A tamper that reds nothing is a FAIL of the SUITE.
  legs     --worktree --out
    G1 `bash scripts/run-shell-suites.sh --check-unreached` in Blockchain/Dev: rc 0.   G2 `--list` names the ks1401 suite (CONTROL: it
       also names ks949).   (Leg 10's 100755 is C1 P9, read from the tree.)
  ks949    --repo --worktree --out   (OPTIONAL, budget-last: needs `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared`)
    K1 ks949 at develop and at head: rc 0 both; its `deployed shape built: … + <n> main-DB migrations` line: head n == develop n + 1.
--selftest  every judge on SYNTHETIC suite outputs (no PostgreSQL): the real-shaped head output PASSES; a SKIP, 52/53, a missing PASS-line
            count, a bypass control, a red-first with one head arm green, a tamper that reds nothing, a restore that is not byte-equal each FAIL.
Usage: c3_run_gate61.py suite|redfirst|tamper|legs|ks949 --repo <clone> --worktree <wt> --out <dir> [--pgbin dir] [--runs n] | --selftest
rc 0 PASS / 1 FAIL / 2 usage. Prints `CHECKED <n>`; 0 checked is a FAIL."""
import hashlib, os, platform, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, wgit, now, Checks, opt_factory, show, guard_scratch, guard_out, run, has_commit, move_out, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); X = K['suite']
MODE = next((m for m in ('suite', 'redfirst', 'tamper', 'legs', 'ks949') if m in A), None)
REPO = opt('--repo'); WT = opt('--worktree'); OUT = opt('--out'); HEAD = opt('--head', K['head']); DEV = K['develop']


def parse(out):
    P = [m.group(1) for m in re.finditer(r'(?m)^\s+PASS  (.*)$', out)]; F = [m.group(1) for m in re.finditer(r'(?m)^\s+FAIL  (.*)$', out)]
    s = re.search(X['summary_rx'], out, re.M); keg = re.search(X['keg_rx'], out, re.M)
    cells = len(re.findall(r'(?m)^  --- CELL \d+:', out))
    return {'pass': P, 'fail': F, 'summary': tuple(int(x) for x in s.groups()) if s else None, 'skip': re.search(X['skip_rx'], out) is not None,
            'keg': keg.group(1) if keg else None, 'cells': cells}


def judge_head(C, out, rc, tag='S1 head'):
    p = parse(out); s = p['summary']
    ok = rc == 0 and s == (X['assertions'], 0, X['assertions'], X['cells']) and len(p['pass']) == X['assertions'] and not p['fail'] and not p['skip'] \
        and p['cells'] == X['cells'] and p['keg'] is not None and re.search(r'PostgreSQL\)? 15\.', p['keg'] or '') is not None
    C.chk(tag, ok, 'rc %s | summary %s (want (%d, 0, %d, %d)) | PASS lines counted %d | FAIL lines %d %s | CELL headers %d | SKIP %s | keg %r' % (
        rc, s, X['assertions'], X['assertions'], X['cells'], len(p['pass']), len(p['fail']), p['fail'][:3] or '', p['cells'], p['skip'], p['keg']))
    C.chk(tag.split()[0].replace('1', '2') + ' non-bypass', any(X['nonbypass_line'] in l for l in p['pass']),
          'the suite\'s own `%s` PASS line present: %s' % (X['nonbypass_line'], any(X['nonbypass_line'] in l for l in p['pass'])))
    return p


def judge_red(C, out, rc):
    p = parse(out)
    miss_pass = [w for w in X['red_at_base_pass'] if not any(w in l for l in p['pass'])]
    miss_fail = [w for w in X['red_at_base_fail'] if not any(w in l for l in p['fail'])]
    green_head = [w for w in X['red_at_base_fail'] if any(w in l for l in p['pass'])]
    C.chk('R1 red-first at develop', not miss_pass and not miss_fail and not p['skip'] and p['cells'] == X['cells'] and rc != 0,
          'base-state arms PASS: missing %s | head-state arms FAIL: missing %s | (a head arm that PASSED at base: %s) | cells %d (want %d) | SKIP %s | rc %s (want != 0) | summary %s' % (
              miss_pass or 'NONE', miss_fail or 'NONE', green_head or 'NONE', p['cells'], X['cells'], p['skip'], rc, p['summary']))
    for l in p['fail']:
        print('INFO R1 FAIL line at base: %s' % l[:200])
    return p


def judge_tamper(C, name, out, landed, restored_sha, want_sha, status):
    p = parse(out); mf = X['tampers'][name]['must_fail']
    miss = [w for w in mf if not any(w in l for l in p['fail'])]
    C.chk('%s reds' % name, landed and not miss and not p['skip'], 'tamper landed %s | must-fail arms missing %s | FAIL lines %d: %s' % (landed, miss or 'NONE', len(p['fail']), [l[:90] for l in p['fail'][:6]]))
    C.chk('%s restored' % name, restored_sha == want_sha and status == '', 'restored sha256 %s == git blob sha256 %s: %s | git status %r' % (
        (restored_sha or '')[:16], want_sha[:16], restored_sha == want_sha, status[:80]))


def host():
    try:
        return subprocess.run(['scutil', '--get', 'LocalHostName'], capture_output=True, text=True).stdout.strip() or platform.node()
    except Exception:
        return platform.node()


if '--selftest' in A:
    st = {'ok': 0, 'n': 0}

    def synth(passes, fails, summary=None, skip=False, cells=None):
        lines = ['KS-1401: keg /opt/homebrew/opt/postgresql@15/bin — postgres (PostgreSQL) 15.14 (Homebrew)']
        for i in range(cells if cells is not None else X['cells']): lines.append('  --- CELL %d: synthetic' % (i + 1))
        lines += ['    PASS  %s' % x for x in passes] + ['    FAIL  %s' % x for x in fails]
        if skip: lines = ['KS-1401: SKIP — no PostgreSQL keg found (set KS1401_PG_BIN to one).', 'KS-1401: 0/0 cells run. This is a SKIP, not a pass.']
        np_, nf = len(passes), len(fails)
        s = summary or (np_, nf, np_ + nf, cells if cells is not None else X['cells'])
        if not skip: lines += ['', 'KS-1401: %d passed, %d failed (of %d assertions over %d cells)' % s, 'KS-1401: keg postgres (PostgreSQL) 15.14 (Homebrew)']
        return '\n'.join(lines) + '\n'
    keyp = X['red_at_base_pass'] + [w + ' x' for w in ('tracker recorded 49 migrations', 'certifications @head = certifications|17|true|true|true|1')]
    head_pass = [X['nonbypass_line'] + ' — RLS binds it'] + ['synthetic pass %d' % i for i in range(X['assertions'] - 1)]
    selftest_arm(st, 'S-0 the real-shaped head output (positive control)', lambda C: judge_head(C, synth(head_pass, []), 0), None)
    selftest_arm(st, 'S-1 a SKIP (no keg) is not a pass', lambda C: judge_head(C, synth([], [], skip=True), 0), 'S1')
    selftest_arm(st, 'S-2 52 of 53 (one FAIL)', lambda C: judge_head(C, synth(head_pass[:-1], ['cross-tenant leak persists: 3']), 1), 'S1')
    selftest_arm(st, 'S-3 a summary that lies (53 claimed, 52 PASS lines printed)', lambda C: judge_head(C, synth(head_pass[:-1], [], summary=(53, 0, 53, 11)), 0), 'S1')
    selftest_arm(st, 'S-4 the non-bypass control FAILED (a bypass role: every red vacuous)', lambda C: judge_head(C, synth(['x'] * X['assertions'], ['CONTROL secuura_app is true/false — RLS would not bind'], summary=(53, 0, 53, 11)), 0), 'S2')
    selftest_arm(st, 'S-5 a cell went missing (10 cells)', lambda C: judge_head(C, synth(head_pass, [], cells=10), 0), 'S1')
    red_fail = [w + ' (synthetic)' for w in X['red_at_base_fail']]
    selftest_arm(st, 'R-0 the expected base shape (positive control)', lambda C: judge_red(C, synth(keyp, red_fail), 1), None)
    selftest_arm(st, 'R-1 the cross-tenant arm GREEN at base (049 not the cause)', lambda C: judge_red(C, synth(keyp + ['tenant B\'s rows are now INVISIBLE'], [f for f in red_fail if 'leak persists' not in f]), 1), 'R1')
    selftest_arm(st, 'R-2 the fixture is not B 50th\'s (a base arm FAILS)', lambda C: judge_red(C, synth(keyp[1:], red_fail + [X['red_at_base_pass'][0]]), 1), 'R1')
    selftest_arm(st, 'R-3 a SKIP at base', lambda C: judge_red(C, synth([], [], skip=True), 0), 'R1')
    selftest_arm(st, 'R-4 the base run returned rc 0', lambda C: judge_red(C, synth(keyp, red_fail), 0), 'R1')
    for tn, tv in X['tampers'].items():
        good = [w + ' (synthetic)' for w in tv['must_fail']]
        selftest_arm(st, '%s-0 the tamper reds its arms, restore byte-equal (positive control)' % tn, lambda C, g=good, tn=tn: judge_tamper(C, tn, synth(head_pass[:-len(g)], g), True, 'a' * 64, 'a' * 64, ''), None)
        selftest_arm(st, '%s-1 the tamper reds NOTHING' % tn, lambda C, tn=tn: judge_tamper(C, tn, synth(head_pass, []), True, 'a' * 64, 'a' * 64, ''), tn + ' reds')
        selftest_arm(st, '%s-2 the tamper never landed' % tn, lambda C, g=good, tn=tn: judge_tamper(C, tn, synth(head_pass, g), False, 'a' * 64, 'a' * 64, ''), tn + ' reds')
        selftest_arm(st, '%s-3 the restore is not byte-equal' % tn, lambda C, g=good, tn=tn: judge_tamper(C, tn, synth(head_pass, g), True, 'b' * 64, 'a' * 64, ''), tn + ' restored')
    selftest_arm(st, 'T-4 the worktree left dirty after a restore', lambda C: judge_tamper(C, 'T-FORCE', synth(head_pass, [w + ' x' for w in X['tampers']['T-FORCE']['must_fail']]), True, 'a' * 64, 'a' * 64, ' M Blockchain/Dev/migrations/049'), 'T-FORCE restored')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)

if MODE is None or not WT or not OUT or (MODE in ('redfirst', 'tamper', 'ks949') and not REPO):
    print(__doc__); raise SystemExit(2)
WT = guard_scratch(WT, 'worktree'); OUT = guard_out(OUT)
if REPO:
    for s in (HEAD, DEV):
        if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s):
            print('REFUSING: %s is not a 40-hex commit present in %s' % (s, REPO)); raise SystemExit(2)
if wgit(WT, 'status', '--porcelain').strip():
    print('REFUSING: the worktree is not clean'); raise SystemExit(2)
ENV = {'KS1401_FLOOR': str(X['assertions'])}
if opt('--pgbin'): ENV['KS1401_PG_BIN'] = opt('--pgbin')
DEVDIR = os.path.join(WT, K['install_dir']); TP = os.path.join(WT, K['test']); MP = os.path.join(WT, K['migration'])
print('c3_run_gate61 %s %s | worktree %s | develop %s | head %s | host %s | env %s' % (MODE, now(), WT, DEV[:12], HEAD[:12], host(), ENV))
C = Checks()


def suite_once(prefix, env=ENV):
    t0 = time.time(); rc, o, e = run(['bash', TP], WT, prefix, env=env, timeout=900); dt = time.time() - t0
    print('INFO run %s rc %d wall-clock %.1f s at %s on %s' % (os.path.basename(prefix), rc, dt, now(), host()))
    return rc, o + e, dt


if MODE == 'suite':
    if REPO: wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
    times = []
    for i in range(int(opt('--runs', '1'))):
        rc, out, dt = suite_once(os.path.join(OUT, 'c3_suite_head_run%d' % (i + 1))); times.append(dt)
        judge_head(C, out, rc, 'S1 head run %d' % (i + 1))
    p = parse(out)
    print('INFO S3 TIMING %s s over %d run(s) | %s | host %s | keg %s' % (' / '.join('%.0f' % t for t in times), len(times), now()[:10], host(), p['keg']))
elif MODE == 'redfirst':
    wgit(WT, 'checkout', '--quiet', '--detach', DEV)
    if os.path.exists(TP) or os.path.exists(MP):
        print('REFUSING: the suite or 049 already exists at develop — the red-first premise (NEW files) is false'); raise SystemExit(2)
    open(TP, 'w', encoding='utf-8').write(show(REPO, HEAD, K['test'])); os.chmod(TP, 0o755)
    open(MP, 'w', encoding='utf-8').write(X['stub_049'])
    try:
        rc, out, dt = suite_once(os.path.join(OUT, 'c3_redfirst_develop_stub049'))
        judge_red(C, out, rc)
    finally:
        q1 = move_out(TP, os.path.join(OUT, 'quarantine'), 'ks1401.develop.%s.test.sh' % now().replace(':', ''))
        q2 = move_out(MP, os.path.join(OUT, 'quarantine'), '049.stub.develop.%s.sql' % now().replace(':', ''))
    stt = wgit(WT, 'status', '--porcelain').strip()
    C.chk('R1b moved out', not stt and not os.path.exists(TP) and not os.path.exists(MP), 'git status --porcelain %r | quarantined %s, %s' % (stt[:100], q1, q2))
elif MODE == 'tamper':
    wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
    want = hashlib.sha256(show(REPO, HEAD, K['migration']).encode('utf-8')).hexdigest()
    for tn, tv in X['tampers'].items():
        orig = open(MP, 'rb').read(); src = orig.decode('utf-8'); n_anchor = src.count(tv['anchor'])
        if n_anchor != 1:
            C.chk('%s reds' % tn, False, 'anchor occurs %d time(s) (want exactly 1: a restore needs a unique anchor)' % n_anchor); continue
        try:
            open(MP, 'w', encoding='utf-8').write(src.replace(tv['anchor'], tv['replace'], 1))
            back = open(MP, encoding='utf-8').read(); landed = back.count(tv['anchor']) == 0 and (tv['replace'] == '' or tv['replace'] in back) and back != src
            rc, out, dt = suite_once(os.path.join(OUT, 'c3_tamper_%s' % tn))
        finally:
            open(MP, 'wb').write(orig)
        got = hashlib.sha256(open(MP, 'rb').read()).hexdigest(); stt = wgit(WT, 'status', '--porcelain').strip()
        judge_tamper(C, tn, out, landed, got, want, stt)
elif MODE == 'legs':
    rc, o, e = run(['bash', 'scripts/run-shell-suites.sh', '--check-unreached'], DEVDIR, os.path.join(OUT, 'c3_leg12_check_unreached'))
    C.chk('G1 leg 12 --check-unreached', rc == 0, 'rc %d | %s' % (rc, ' '.join((o + e).split())[-200:]))
    rc2, o2, e2 = run(['bash', 'scripts/run-shell-suites.sh', '--list'], DEVDIR, os.path.join(OUT, 'c3_leg14_list'))
    lst = o2.splitlines(); has = [l for l in lst if 'ks1401_049_tenant_isolation_after_039.test.sh' in l]; ctl = [l for l in lst if 'ks949_main_seed_idempotence.test.sh' in l]
    C.chk('G2 leg 14 reaches the suite', rc2 == 0 and len(has) == 1 and len(ctl) == 1, 'rc %d | --list %d suites | ks1401 listed %s | CONTROL ks949 listed %s' % (rc2, len(lst), has, ctl))
elif MODE == 'ks949':
    dist = os.path.join(WT, K['shared_dist'])
    if not (os.path.isfile(dist) and os.path.getsize(dist) > 0):
        print('REFUSING: %s missing — npm ci --ignore-scripts + build packages/shared first' % dist); raise SystemExit(2)
    res = {}
    for name, sha in (('develop', DEV), ('head', HEAD)):
        wgit(WT, 'checkout', '--quiet', '--detach', sha)
        rc, o, e = run(['bash', os.path.join(WT, K['ks949'])], WT, os.path.join(OUT, 'c3_ks949_' + name), env=({'KS949_PG_BIN': opt('--pgbin')} if opt('--pgbin') else {}), timeout=1200)
        m = re.search(r'\+ (\d+) main-DB migrations', o + e); res[name] = (rc, int(m.group(1)) if m else None, 'SKIP' in (o + e))
        print('INFO ks949 %s at %s rc %d main-DB migrations %s SKIP %s' % (name, sha[:12], rc, res[name][1], res[name][2]))
    C.chk('K1 ks949 base + 1', res['develop'][0] == 0 and res['head'][0] == 0 and not res['develop'][2] and not res['head'][2] and res['develop'][1] is not None and res['head'][1] == res['develop'][1] + 1,
          'develop rc %s n %s | head rc %s n %s (want rc 0 both, n head == n develop + 1, no SKIP)' % (res['develop'][0], res['develop'][1], res['head'][0], res['head'][1]))
if REPO:
    wgit(WT, 'checkout', '--quiet', '--detach', HEAD)
n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C3 %s %s: %d FAIL of %d checks | head %s' % (MODE.upper(), 'PASS' if n == 0 and C.res else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n or not C.res else 0)
