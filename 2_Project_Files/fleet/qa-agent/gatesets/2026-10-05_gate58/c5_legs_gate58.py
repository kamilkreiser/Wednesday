#!/usr/bin/env python3
"""c5_legs_gate58.py — gate58 C5: the pre-push preflight legs the PR exists to keep green past the 2026-10-15 fuse, run by the TESTER in
its OWN worktrees (never the shared checkout, never the builder's s-f1-* worktree). Every rc is captured by subprocess, never through a
pipe; every leg's stdout / stderr / rc lands in <outdir> as separate files.

  plan <repo> <sha>                     READ-ONLY (show / cat-file): the leg files exist at <sha>; both gates read AUDIT_BASELINE_PATH;
                                        S0 SEMANTICS printed with line numbers: `return expires <= today;` in isLapsed and utcToday's
                                        `new Date().toISOString().slice(0, 10)`; expected-case-count value; a nonexistent-path CONTROL.
  parse-selftest <outdir>               the section parser on planted gate output: NEW rows and LAPSED rows are told apart; CLEANUP rows
                                        (stdout, no `[severity]`) and URL lines never count.
  freeze-selftest <devdir> <outdir>     K0 the clock pin PROVED BOTH WAYS: valid FROZEN_NOW_ISO -> node reads 2026-10-15T00:01:00.000Z;
                                        UNSET -> exit 97 REFUSED; unparseable -> exit 97; WITHOUT the preload -> the real UTC day (differs).
                                        K1 the worktree's OWN baseline-contract.mjs under the freeze: utcToday() == 2026-10-15,
                                        isLapsed(2026-10-15) true, isLapsed(2026-10-31) false, isLapsed(2027-01-01) false.
  run <devdir> <label> <outdir> head|base
        <devdir> = <your worktree>/Blockchain/Dev. Installs scripts/audit's OWN lock (`npm ci --ignore-scripts`, X1), then:
        head: leg 2 (lockfile-cleanroom.sh), leg 5 (`npm run audit:contract --silent`; cases == kit expected_case_count 59 AND
              == the worktree's expected-case-count), leg 6 and leg 7 at TODAY's clock AND FROZEN at kit freeze_at. Want every rc 0
              and 0 of the three removed ids named in any FAIL section.
        base: legs 6 + 7 TODAY (control: rc 0 — the rows still protect the base until the 15th) and FROZEN (want rc 1 each; leg 6's
              LAPSED section names all THREE, leg 7's names c83g + 73wf — w9m9 is the root lock's copy, leg 6's corpus only).
        rc 2 from a gate is a SKIP (registry unreachable) and is NEVER a pass; rc 3 is the gate REFUSING.
  bite <devdir> <outdir> [--base <sha>] AT HEAD, today's clock, no tracked file left edited:
        NO-OP CONTROL: an unmodified copy of the head baseline by AUDIT_BASELINE_PATH -> legs 6 + 7 rc 0.
        For EACH kit bite_lock (root, governance): its BASE blob (`git show <base>:<lock>`, read-only) is written over the worktree file,
        legs 6 + 7 run, then the saved head bytes are written back and their sha256 + `git status --porcelain` are asserted clean.
        Want: root reverted -> leg 6 rc 1 naming all three as NEW; governance reverted -> leg 7 rc 1 naming c83g + 73wf as NEW in a
        line that names services/governance.
  install-root <devdir> <outdir>        `npm ci --ignore-scripts --no-audit --no-fund` at Blockchain/Dev from the COMMITTED root lock:
        rc 0, the added-package count, the lock's sha256 IDENTICAL before and after, the five bumped packages AS INSTALLED ON DISK at the
        kit versions (node_modules/<pkg>/package.json), `git status --porcelain --untracked-files=no` empty after.
<devdir> / <outdir> are refused (rc 2, nothing run or created) under the kit forbidden_root (/Volumes/DevMASTER; G58_FORBIDDEN_ROOT
overrides it for a refusal-arm control inside scratch); <outdir> may be under the QA reports root.
Exit: 0 when every expectation of the mode held; 1 when one did not (MISMATCH lines say which); 2 usage / refusal."""
import hashlib, json, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate58 import K, G, git, now, guard_out, guard_worktree

A = sys.argv[1:]
if not A or A[0] in ('--help', '-h'):
    print(__doc__); raise SystemExit(0 if A else 2)
MODE = A[0]
FREEZE = os.path.join(G, 'c5_freeze_clock_gate58.cjs')
IDS = sorted(K['removed_rows']); ROOT_ONLY = 'GHSA-w9m9-85wc-3x92'
CLS = {0: 'PASS', 1: 'FAIL', 2: 'SKIP (not a pass)', 3: 'REFUSED'}


def sh(cmd, out, name, cwd=None, env=None, timeout=1800):
    e = dict(os.environ); e.pop('FROZEN_NOW_ISO', None); e.pop('AUDIT_BASELINE_PATH', None); e.update(env or {})
    try:
        r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout); rc = r.returncode; so, se = r.stdout, r.stderr
    except subprocess.TimeoutExpired as x:
        rc, so, se = 124, x.stdout or '', (x.stderr or '') + '\nTIMEOUT after %ds' % timeout
        so = so.decode() if isinstance(so, bytes) else so; se = se.decode() if isinstance(se, bytes) else se
    for ext, v in (('out', so), ('err', se), ('rc', '%d\n' % rc)):
        open(os.path.join(out, '%s.%s' % (name, ext)), 'w', encoding='utf-8').write(v)
    return rc, so, se


def parse(err):
    """{'NEW': [ids], 'LAPSED': [ids], 'locks': {id: 'in N lock(s): ...'}} from a gate's STDERR; CLEANUP rows live on stdout and carry no [sev]"""
    sec = None; res = {'NEW': [], 'LAPSED': [], 'locks': {}}; last = None
    for l in err.split('\n'):
        if l.startswith('FAIL — '):
            sec = 'LAPSED' if 'LAPSED' in l else 'NEW'; continue
        m = re.match(r'^  - (GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}) \[', l)
        if m and sec:
            res[sec].append(m.group(1)); last = m.group(1); continue
        m = re.match(r'^    in \d+ lock\(s\): (.*)$', l)
        if m and last: res['locks'][last] = m.group(1)
    return res


def gate(dev, out, name, which, frozen, extra_env=None):
    js = os.path.join(dev, 'scripts/audit/%s.mjs' % which)
    cmd = ['node'] + (['--require', FREEZE] if frozen else []) + [js]
    env = dict(extra_env or {})
    if frozen: env['FROZEN_NOW_ISO'] = K['freeze_at']
    rc, so, se = sh(cmd, out, name, cwd=dev, env=env, timeout=600)
    p = parse(se)
    head1 = next((l for l in so.split('\n') if l.startswith(('audit-gate:', 'audit-locks:'))), '')[:200]
    clean = sum(1 for l in so.split('\n') if re.match(r'^  - GHSA-\S+ \(', l))
    clk = next((l for l in se.split('\n') if l.startswith('c5_freeze_clock')), 'real clock (no preload)')
    print('  %-26s rc %d %-18s | %s | FAIL-NEW %s | FAIL-LAPSED %s | CLEANUP rows %d | %s' % (name, rc, CLS.get(rc, 'ERROR'), head1, p['NEW'] or '-', p['LAPSED'] or '-', clean, clk))
    return rc, p, so, se


def check_dev(dev):
    dev = guard_worktree(dev)
    if not (os.path.isfile(os.path.join(dev, 'scripts/audit/audit-gate.mjs')) and os.path.isfile(os.path.join(dev, 'scripts/preflight/lockfile-cleanroom.sh'))):
        print('REFUSING: %s is not a Blockchain/Dev directory' % dev); raise SystemExit(2)
    sha = subprocess.run(['git', '-C', dev, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', '-C', dev, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    if dirty.strip():
        print('REFUSING: tracked changes in %s — the legs must read the committed tree:\n%s' % (dev, dirty)); raise SystemExit(2)
    return dev, sha


def install_audit(dev, out):
    rc, _, _ = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], out, 'install_scripts_audit', cwd=os.path.join(dev, 'scripts/audit'))
    sem = os.path.isdir(os.path.join(dev, 'scripts/audit/node_modules/semver'))
    print('  scripts/audit npm ci rc %d | semver resolvable %s' % (rc, sem))
    return rc == 0 and sem


BAD = []
def want(ok, msg):
    print('  %s %s' % ('OK      ' if ok else 'MISMATCH', msg))
    if not ok: BAD.append(msg)


if MODE == 'plan':
    REPO, SHA = A[1], A[2]
    print('c5 plan %s | repo %s | sha %s (read-only)' % (now(), REPO, SHA))
    for k, p in sorted(K['legs'].items()):
        rc, _, _ = git(REPO, 'cat-file', '-e', '%s:%s' % (SHA, p), check=False); want(rc == 0, 'leg %s file %s present (cat-file rc %d)' % (k, p, rc))
    rc, _, _ = git(REPO, 'cat-file', '-e', '%s:Blockchain/Dev/scripts/audit/no-such-file.mjs' % SHA, check=False); want(rc != 0, 'CONTROL nonexistent path: cat-file rc %d (want non-zero)' % rc)
    for p in ('audit-gate.mjs', 'audit-locks.mjs'):
        t = git(REPO, 'show', '%s:Blockchain/Dev/scripts/audit/%s' % (SHA, p)).split('\n')
        ln = [i + 1 for i, l in enumerate(t) if 'process.env.AUDIT_BASELINE_PATH' in l]; want(bool(ln), '%s reads AUDIT_BASELINE_PATH at line(s) %s' % (p, ln))
    bc = git(REPO, 'show', '%s:Blockchain/Dev/scripts/audit/baseline-contract.mjs' % SHA).split('\n')
    a = [i + 1 for i, l in enumerate(bc) if l.strip() == 'return expires <= today;']; b = [i + 1 for i, l in enumerate(bc) if "new Date().toISOString().slice(0, 10)" in l]
    want(len(a) == 1 and len(b) == 1, 'S0 baseline-contract.mjs: `return expires <= today;` at %s; utcToday `new Date().toISOString().slice(0, 10)` at %s (a row is dead ON its date, UTC)' % (a, b))
    ec = git(REPO, 'show', '%s:%s' % (SHA, K['legs']['5'])).strip(); want(ec == str(K['expected_case_count']), 'expected-case-count at %s reads %r (kit %d)' % (SHA[:12], ec, K['expected_case_count']))
    print('PLAN %s' % ('OK' if not BAD else 'MISMATCH')); raise SystemExit(1 if BAD else 0)

if MODE == 'parse-selftest':
    out = guard_out(A[1])
    g_err = '\n'.join(['', 'FAIL — 1 NEW advisory not in the baseline:', '  - GHSA-c83g-rgw3-j3cx [high] browserslist: planted', '    https://github.com/advisories/GHSA-c83g-rgw3-j3cx',
                       '  Triage it: ...', '', 'FAIL — 2 temporary exceptions LAPSED (expires passed, fix ticket unresolved):', '  - GHSA-73wf-gq98-2v4g [high] browserslist — KS-751 (expired 2026-10-15)',
                       '  - GHSA-w9m9-85wc-3x92 [low] postcss-selector-parser — KS-749 (expired 2026-10-15)'])
    l_err = '\n'.join(['', 'FAIL — 1 advisory in standalone locks and NOT in the baseline:', '  - GHSA-73wf-gq98-2v4g [high] browserslist: planted', '    pinned: 4.28.2',
                       '    in 1 lock(s): services/governance', '', 'FAIL — 1 temporary exception(s) LAPSED:', '  - GHSA-c83g-rgw3-j3cx [high] browserslist: planted', '    pinned: 4.28.2', '    in 2 lock(s): a, b', '    KS-751 (expired 2026-10-15)'])
    clean_out = 'CLEANUP (advisory): 1 baseline entry is no longer reported — remove:\n  - GHSA-2mjp-6q6p-2qxm (undici, KS-470)\n'
    open(os.path.join(out, 'parse_plant_gate.err'), 'w').write(g_err); open(os.path.join(out, 'parse_plant_locks.err'), 'w').write(l_err)
    a, b, c = parse(g_err), parse(l_err), parse(clean_out)
    print('c5 parse-selftest | gate plant %s | locks plant %s | cleanup-only plant %s' % (a, b, c))
    want(a['NEW'] == ['GHSA-c83g-rgw3-j3cx'] and a['LAPSED'] == ['GHSA-73wf-gq98-2v4g', ROOT_ONLY], 'audit-gate shape: NEW and LAPSED told apart; the URL line does not count')
    want(b['NEW'] == ['GHSA-73wf-gq98-2v4g'] and b['LAPSED'] == ['GHSA-c83g-rgw3-j3cx'] and b['locks'].get('GHSA-73wf-gq98-2v4g') == 'services/governance', 'audit-locks shape: NEW / LAPSED + the lock attribution line')
    want(c == {'NEW': [], 'LAPSED': [], 'locks': {}}, 'a CLEANUP row (no FAIL header, no [severity]) counts as nothing')
    print('PARSE %s' % ('OK' if not BAD else 'MISMATCH')); raise SystemExit(1 if BAD else 0)

if MODE == 'freeze-selftest':
    dev, sha = check_dev(A[1]); out = guard_out(A[2])
    print('c5 freeze-selftest %s | tree %s | node %s | preload %s' % (now(), sha, subprocess.run(['node', '-v'], capture_output=True, text=True).stdout.strip(), FREEZE))
    probe = "process.stdout.write(new Date().toISOString())"
    rc, so, se = sh(['node', '--require', FREEZE, '-e', probe], out, 'k0_valid', env={'FROZEN_NOW_ISO': K['freeze_at']}); want(rc == 0 and so == K['freeze_at'], 'K0 valid: rc %d, clock reads %s (want %s)' % (rc, so, K['freeze_at']))
    rc, so, se = sh(['node', '--require', FREEZE, '-e', probe], out, 'k0_unset'); want(rc == 97 and so == '', 'K0 UNSET: rc %d (want 97 REFUSED), stdout %r' % (rc, so))
    rc, so, se = sh(['node', '--require', FREEZE, '-e', probe], out, 'k0_garbage', env={'FROZEN_NOW_ISO': 'not-a-date'}); want(rc == 97, 'K0 unparseable: rc %d (want 97)' % rc)
    rc, so, se = sh(['node', '-e', probe], out, 'k0_real'); real = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    want(rc == 0 and so[:10] == real and so[:10] != K['freeze_day'], 'K0 CONTROL no preload: clock reads %s (real UTC day %s, differs from the frozen day)' % (so, real))
    bc = os.path.join(dev, 'scripts/audit/baseline-contract.mjs')
    p2 = ("import(%s).then(m=>{const t=m.utcToday();process.stdout.write(JSON.stringify({today:t,l15:m.isLapsed({expires:'2026-10-15'},t),l31:m.isLapsed({expires:'2026-10-31'},t),l27:m.isLapsed({expires:'2027-01-01'},t)}))})" % json.dumps('file://' + bc))
    rc, so, se = sh(['node', '--require', FREEZE, '-e', p2], out, 'k1_contract', env={'FROZEN_NOW_ISO': K['freeze_at']})
    try: j = json.loads(so)
    except ValueError: j = {}
    want(rc == 0 and j == {'today': '2026-10-15', 'l15': True, 'l31': False, 'l27': False}, 'K1 the worktree\'s own baseline-contract.mjs under the freeze: %s' % (j or (rc, se.strip()[-200:])))
    rc, so, se = sh(['node', '-e', p2], out, 'k1_contract_real');
    try: j2 = json.loads(so)
    except ValueError: j2 = {}
    want(rc == 0 and j2.get('today') == real and j2.get('l15') is (real >= '2026-10-15'), 'K1 CONTROL real clock: %s' % j2)
    print('FREEZE %s' % ('OK' if not BAD else 'MISMATCH')); raise SystemExit(1 if BAD else 0)

if MODE == 'run':
    dev, sha = check_dev(A[1]); label = A[2]; out = guard_out(A[3]); exp = A[4] if len(A) > 4 else ''
    if exp not in ('head', 'base'): print('usage: run <devdir> <label> <outdir> head|base'); raise SystemExit(2)
    print('c5 run %s (%s) %s | tree %s | node %s | npm %s | freeze %s | outdir %s' % (label, exp, now(), sha, subprocess.run(['node', '-v'], capture_output=True, text=True).stdout.strip(),
          subprocess.run(['npm', '-v'], capture_output=True, text=True).stdout.strip(), K['freeze_at'], out))
    if not install_audit(dev, out): print('LEGS %s: scripts/audit install failed — legs 5/7 cannot run (NOT a pass)' % label); raise SystemExit(1)
    if exp == 'head':
        rc2, so, se = sh(['bash', os.path.join(dev, 'scripts/preflight/lockfile-cleanroom.sh')], out, 'leg2', cwd=dev, timeout=3600)
        print('  %-26s rc %d %-18s | last line: %s' % ('leg2 cleanroom', rc2, CLS.get(rc2, 'ERROR'), (so.strip().split('\n') or [''])[-1][:160]))
        rc5, so, se = sh(['npm', 'run', 'audit:contract', '--silent'], out, 'leg5', cwd=dev, timeout=1800)
        m = re.findall(r' tests (\d+)', so + se); cases = int(m[-1]) if m else None
        fl = re.findall(r' fail (\d+)', so + se); fails = int(fl[-1]) if fl else None
        ec = open(os.path.join(dev, 'scripts/audit/expected-case-count')).read().strip()
        print('  %-26s rc %d %-18s | tests %s | fail %s | expected-case-count in the tree %s (kit %d)' % ('leg5 audit:contract', rc5, CLS.get(rc5, 'ERROR'), cases, fails, ec, K['expected_case_count']))
        want(rc2 == 0, 'leg 2 rc %d (want 0)' % rc2)
        want(rc5 == 0 and cases == K['expected_case_count'] and ec == str(K['expected_case_count']) and fails == 0, 'leg 5 rc %d, %s cases (want %d == the tree\'s expected-case-count %s), fail %s' % (rc5, cases, K['expected_case_count'], ec, fails))
    res = {}
    for which, leg in (('audit-gate', '6'), ('audit-locks', '7')):
        for fz in (False, True):
            res[(leg, fz)] = gate(dev, out, 'leg%s_%s' % (leg, 'frozen' if fz else 'today'), which, fz)
    named = lambda leg, fz, sec: [i for i in res[(leg, fz)][1][sec] if i in IDS]
    if exp == 'head':
        for leg in ('6', '7'):
            for fz in (False, True):
                rc, p = res[(leg, fz)][0], res[(leg, fz)][1]
                want(rc == 0 and not [i for i in p['NEW'] + p['LAPSED'] if i in IDS], 'HEAD leg %s %s: rc %d (want 0), removed ids named in a FAIL section %s (want none)' % (
                    leg, 'FROZEN' if fz else 'today', rc, [i for i in p['NEW'] + p['LAPSED'] if i in IDS]))
        for leg in ('6', '7'):
            so = res[(leg, False)][2] + res[(leg, False)][3]; print('  INFO head leg %s today: the three ids appear %d time(s) anywhere in its output' % (leg, sum(so.count(i) for i in IDS)))
    else:
        want(res[('6', False)][0] == 0 and res[('7', False)][0] == 0, 'BASE today CONTROL: legs 6 / 7 rc %d / %d (want 0 / 0 — the rows still protect the base before the 15th)' % (res[('6', False)][0], res[('7', False)][0]))
        l6, l7 = named('6', True, 'LAPSED'), named('7', True, 'LAPSED')
        want(res[('6', True)][0] == 1 and sorted(l6) == IDS, 'BASE FROZEN leg 6: rc %d (want 1, not 2), LAPSED names %s (want all three %s)' % (res[('6', True)][0], sorted(l6), IDS))
        want(res[('7', True)][0] == 1 and sorted(l7) == sorted(set(IDS) - {ROOT_ONLY}), 'BASE FROZEN leg 7: rc %d (want 1), LAPSED names %s (want c83g + 73wf; w9m9 is leg 6\'s corpus only)' % (res[('7', True)][0], sorted(l7)))
    print('LEGS %s %s: %s' % (label, exp, 'OK' if not BAD else 'MISMATCH (%d)' % len(BAD))); raise SystemExit(1 if BAD else 0)

if MODE == 'bite':
    dev, sha = check_dev(A[1]); out = guard_out(A[2]); base = A[A.index('--base') + 1] if '--base' in A else K['base']
    top = subprocess.run(['git', '-C', dev, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    print('c5 bite %s | tree %s | base for reverts %s | outdir %s' % (now(), sha, base[:12], out))
    if not install_audit(dev, out): print('BITE: install failed'); raise SystemExit(1)
    blp = os.path.join(dev, 'scripts/audit/audit-baseline.json'); cp = os.path.join(out, 'baseline_copy.json'); open(cp, 'wb').write(open(blp, 'rb').read())
    r6 = gate(dev, out, 'bite_noop_leg6', 'audit-gate', False, {'AUDIT_BASELINE_PATH': cp}); r7 = gate(dev, out, 'bite_noop_leg7', 'audit-locks', False, {'AUDIT_BASELINE_PATH': cp})
    want(r6[0] == 0 and r7[0] == 0, 'NO-OP CONTROL (unmodified baseline copy by AUDIT_BASELINE_PATH): legs 6 / 7 rc %d / %d (want 0 / 0)' % (r6[0], r7[0]))
    for lock in K['bite_locks']:
        rel = lock[len('Blockchain/Dev/'):]; fp = os.path.join(dev, rel); tag = rel.replace('/', '_').replace('-', '_')
        saved = open(fp, 'rb').read(); hs = hashlib.sha256(saved).hexdigest()
        bb = subprocess.run(['git', '-C', top, 'show', '%s:%s' % (base, lock)], capture_output=True).stdout
        if not bb: print('REFUSING: base blob %s:%s unreadable in %s' % (base[:12], lock, top)); raise SystemExit(2)
        open(fp, 'wb').write(bb)
        try:
            b6 = gate(dev, out, 'bite_%s_leg6' % tag, 'audit-gate', False); b7 = gate(dev, out, 'bite_%s_leg7' % tag, 'audit-locks', False)
        finally:
            open(fp, 'wb').write(saved)
        back = hashlib.sha256(open(fp, 'rb').read()).hexdigest() == hs
        dirty = subprocess.run(['git', '-C', dev, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip()
        want(back and not dirty, 'restore %s: head bytes back (sha256 %s) %s | git status clean %s' % (rel, hs[:16], back, not dirty))
        if lock == 'Blockchain/Dev/package-lock.json':
            n6 = sorted(i for i in b6[1]['NEW'] if i in IDS)
            want(b6[0] == 1 and n6 == IDS, 'BITE root reverted: leg 6 rc %d (want 1) naming as NEW %s (want all three); leg 7 rc %d (its corpus excludes the root)' % (b6[0], n6, b7[0]))
        else:
            n7 = sorted(i for i in b7[1]['NEW'] if i in IDS); att = [b7[1]['locks'].get(i, '') for i in n7]
            want(b7[0] == 1 and n7 == sorted(set(IDS) - {ROOT_ONLY}) and all('services/governance' in a for a in att),
                 'BITE %s reverted: leg 7 rc %d (want 1) naming as NEW %s (want c83g + 73wf) in lock lines %s (want services/governance named)' % (rel, b7[0], n7, att))
    print('BITE %s' % ('OK' if not BAD else 'MISMATCH (%d)' % len(BAD))); raise SystemExit(1 if BAD else 0)

if MODE == 'install-root':
    dev, sha = check_dev(A[1]); out = guard_out(A[2]); lp = os.path.join(dev, 'package-lock.json')
    h0 = hashlib.sha256(open(lp, 'rb').read()).hexdigest()
    print('c5 install-root %s | tree %s | root lock sha256 before %s' % (now(), sha, h0))
    rc, so, se = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], out, 'install_root', cwd=dev, timeout=3600)
    h1 = hashlib.sha256(open(lp, 'rb').read()).hexdigest(); m = re.findall(r'added (\d+) packages?', so + se)
    disk = {}
    for n, P in sorted(K['packages'].items()):
        pj = os.path.join(dev, 'node_modules', n, 'package.json'); disk[n] = json.load(open(pj)).get('version') if os.path.isfile(pj) else 'ABSENT'
    dirty = subprocess.run(['git', '-C', dev, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip()
    print('  npm ci rc %d | added %s | lock sha256 after %s | on disk %s | tracked changes after: %s' % (rc, m[-1] if m else '?', h1, json.dumps(disk), dirty or 'NONE'))
    want(rc == 0 and bool(m), 'npm ci rc %d (want 0) with an added-package count %s' % (rc, m[-1] if m else 'NONE'))
    want(h0 == h1, 'the committed root lock is byte-identical after npm ci (npm did not rewrite it)')
    want(all(disk[n] == P['to'] for n, P in K['packages'].items()), 'the five bumped packages AS INSTALLED at the kit versions: %s' % json.dumps(disk))
    want(not dirty, 'git status --porcelain --untracked-files=no empty after the install')
    print('INSTALL-ROOT %s' % ('OK' if not BAD else 'MISMATCH (%d)' % len(BAD))); raise SystemExit(1 if BAD else 0)

print(__doc__); raise SystemExit(2)
