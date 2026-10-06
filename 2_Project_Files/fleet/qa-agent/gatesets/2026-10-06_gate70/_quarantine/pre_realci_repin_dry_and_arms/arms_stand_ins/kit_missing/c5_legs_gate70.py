#!/usr/bin/env python3
"""c5_legs_gate70.py — RUNS the repo's own gates in the TESTER'S OWN worktrees (never a builder's, never the shared checkout).
Every command's stdout / stderr / rc goes to SEPARATE files under --out; the rc is read from the process, never through a pipe.
Network: npm registry (X1). Refuses a worktree under the forbidden root.

  legs      --wt WT --expect fail|pass --out DIR     leg 6 `node scripts/audit/audit-gate.mjs` + leg 7 `node scripts/audit/audit-locks.mjs`
            from WT/Blockchain/Dev (scripts/audit deps installed first with `npm ci --ignore-scripts` IN WT/Blockchain/Dev/scripts/audit
            only if absent). rc 2 is COULD-NOT-CHECK (a SKIP): NOT RUN, never a pass. --expect fail (the BASE): both rc 1 AND the five
            ids printed > 0 times (the base control). --expect pass (the HEAD): both rc 0 AND the 3 FIXED ids printed 0 times beside
            the base's count (a discriminating zero).
  contract  --wt WT --out DIR    `npm run audit:contract`: rc 0, TAP `# pass` == WT's scripts/audit/expected-case-count (59), `# fail` 0
  cleanroom --wt WT --out DIR    leg 2 `bash scripts/preflight/lockfile-cleanroom.sh`: rc 0, the "All N standalone lock(s) pass" line,
            and `git status --porcelain` of WT identical before and after (it modified no tracked file)
  install   --wt WT --out DIR    `npm ci --ignore-scripts` at WT/Blockchain/Dev from the COMMITTED root lock: rc 0, root-lock sha256
            identical before and after, package count quoted
  nc        --wt WT --repo CLONE --out DIR [--base B]     NEGATIVE CONTROLS on the HEAD worktree; each tamper is ASSERTED LANDED (sha
            changed + the marker read back) before its result is read, then restored BY CONTENT and sha256-verified:
            NC1 one proxy-addr entry reverted to 2.0.7 (the first changed standalone lock whose BASE pins 2.0.7) -> leg 7 rc 1 naming GHSA-jqcg
            NC2 the GHSA-hp3w-g68c-fv3c row removed from the baseline        -> leg 6 or 7 rc 1 naming sprintf-js / GHSA-hp3w
            NC3 postcss-selector-parser 7.1.4 planted back in api-explorer    -> leg 7 STAYS rc 0 (the GHSA-keyed row MASKS it) while
                `c2_locks_gate70.py parse --dir WT --expect-clean` FAILS with psp7 == 1: the parse, not the gate, is the guard
  --selftest   TAP parsing, id counting, the rc classification (rc 2 -> NOT RUN), on synthetic text.
rc 0 / 1 (a FAIL or a NOT RUN)."""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate70 import K, Tally, git_bytes, outside_forbidden, detect_indent

HERE = os.path.dirname(os.path.abspath(__file__))
LG = K['legs']; FIVE = K['five_ids']; FIXED = K['fixed_ids']
TIMEOUT = int(os.environ.get('G70_LEG_TIMEOUT', '1200'))


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def run(cmd, cwd, out, tag, env=None):
    e = dict(os.environ); e.pop('GIT_SSH_COMMAND', None); e.update(env or {})
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT, env=e)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as x:
        rc, so, se = 124, x.stdout or '', (x.stderr or '') + '\nTIMEOUT %ds' % TIMEOUT
        so = so.decode() if isinstance(so, bytes) else so; se = se.decode() if isinstance(se, bytes) else se
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, tag + '.out'), 'w').write(so); open(os.path.join(out, tag + '.err'), 'w').write(se)
    open(os.path.join(out, tag + '.rc'), 'w').write('%d\n' % rc)
    print('RAN %s rc %d (%s in %s) -> %s/%s.{out,err,rc}' % (tag, rc, ' '.join(cmd), cwd, out, tag))
    return rc, so + '\n' + se


def count_ids(text, ids): return dict((i, text.count(i)) for i in ids)


def classify(rc):
    return {0: 'PASS', 1: 'FAIL-FINDINGS', 2: 'COULD-NOT-CHECK (NOT RUN)', 3: 'MALFORMED-BASELINE', 124: 'TIMEOUT (NOT RUN)'}.get(rc, 'rc %d' % rc)


def tap(text):
    g = lambda k: int(m.group(1)) if (m := re.search(r'^(?:#|\u2139) %s (\d+)' % k, text, re.M)) else None   # TAP `# pass N` or spec `\u2139 pass N`
    return {'tests': g('tests'), 'pass': g('pass'), 'fail': g('fail'), 'skipped': g('skipped'), 'todo': g('todo')}


def dev(wt): return os.path.join(wt, LG['cwd'])


def base_ok(r6, r7, text): return r6 == 1 and r7 == 1 and sum(text.count(i) for i in FIVE) > 0


def head_ok(r6, r7, text): return r6 == 0 and r7 == 0 and sum(text.count(i) for i in FIXED) == 0


def guard(wt):
    if not outside_forbidden(wt):
        raise SystemExit('REFUSED: %s is under %s — run in YOUR OWN worktree' % (wt, K['forbidden_root']))
    if not os.path.isdir(dev(wt)):
        raise SystemExit('REFUSED: %s has no %s (a --no-checkout clone is not a worktree)' % (wt, LG['cwd']))


def audit_deps(wt, out):
    d = os.path.join(wt, LG['audit_deps_dir'])
    if os.path.isdir(os.path.join(d, 'node_modules', 'semver')):
        print('DEPS scripts/audit/node_modules/semver present'); return 0
    return run(['npm', 'ci', '--ignore-scripts'], d, out, 'auditdeps_npm_ci')[0]


def legs(wt, expect, out, t):
    if audit_deps(wt, out) != 0:
        t.check('LEGS', False, 'scripts/audit deps did not install: LOAD FAILURE, NOT RUN'); return {}
    r6, o6 = run(LG['leg6'], dev(wt), out, 'leg6'); r7, o7 = run(LG['leg7'], dev(wt), out, 'leg7')
    c6, c7 = count_ids(o6, FIVE), count_ids(o7, FIVE)
    m = re.search(r'audit-locks: (\d+) standalone lockfiles', o7); pk = re.search(r'(\d+) distinct packages pinned', o7)
    mb = re.search(r'(\d+) advisories match, (\d+) already baselined', o7)
    print('LEG6 rc %d %s | ids %s' % (r6, classify(r6), c6))
    print('LEG7 rc %d %s | ids %s | %s locks, %s packages, %s match / %s baselined (author: base 10 / 5, head 7 / 7)' % (
        r7, classify(r7), c7, m and m.group(1), pk and pk.group(1), mb and mb.group(1), mb and mb.group(2)))
    if expect == 'fail':
        t.check('G-BASE', base_ok(r6, r7, o6 + o7),
                'BASE CONTROL: leg 6 rc %d, leg 7 rc %d (want 1 / 1, never 2) | the five ids printed %d times (want > 0)' % (r6, r7, sum(c6.values()) + sum(c7.values())))
    else:
        z = sum(c6.get(i, 0) + c7.get(i, 0) for i in FIXED)
        t.check('G-HEAD', head_ok(r6, r7, o6 + o7), 'HEAD: leg 6 rc %d, leg 7 rc %d (want 0 / 0) | the 3 FIXED ids printed %d times (want 0; the base control is the other half)' % (r6, r7, z))
    return {'r6': r6, 'r7': r7, 'c6': c6, 'c7': c7}


def contract(wt, out, t):
    if audit_deps(wt, out) != 0:
        t.check('C5', False, 'deps did not install: NOT RUN'); return
    rc, o = run(LG['leg5'], dev(wt), out, 'leg5_contract')
    want = int(open(os.path.join(wt, LG['audit_deps_dir'], 'expected-case-count')).read().strip())
    tp = tap(o)
    t.check('C5', rc == 0 and tp['pass'] == want == K['expected_case_count'] and tp['fail'] == 0 and tp['tests'] == want,
            'audit:contract rc %d | TAP %s | expected-case-count file %d (kit %d)' % (rc, tp, want, K['expected_case_count']))


def porcelain(wt):
    return subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout


def cleanroom(wt, out, t):
    before = porcelain(wt)
    rc, o = run(LG['leg2'], dev(wt), out, 'leg2_cleanroom')
    after = porcelain(wt); m = re.search(r'All (\d+) standalone lock\(s\) pass', o)
    t.check('C2R', rc == 0 and m is not None and before == after, 'lockfile-cleanroom rc %d | "%s" | tracked-file status identical before/after: %s (%d / %d lines)' % (
        rc, m.group(0) if m else 'the All-N line ABSENT', before == after, before.count('\n'), after.count('\n')))


def install(wt, out, t):
    lock = os.path.join(dev(wt), 'package-lock.json'); a = sha(lock)
    rc, o = run(['npm', 'ci', '--ignore-scripts'], dev(wt), out, 'install_npm_ci')
    b = sha(lock); m = re.search(r'added (\d+) packages?', o)
    t.check('INST', rc == 0 and a == b, 'npm ci --ignore-scripts rc %d | root lock sha256 before %s after %s identical %s | %s' % (
        rc, a[:16], b[:16], a == b, m.group(0) if m else 'no "added N packages" line'))


def _rewrite_entry(path, key, fields):
    raw = open(path, 'rb').read(); n = detect_indent(raw.decode()); j = json.loads(raw)
    j['packages'][key].update(fields)
    open(path, 'wb').write((json.dumps(j, indent=n, ensure_ascii=False) + '\n').encode())
    return raw


def nc(wt, repo, base, out, t):
    guard(wt)
    head = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    if audit_deps(wt, out) != 0:
        t.check('NC', False, 'deps did not install: NOT RUN'); return
    # NC1
    key = 'node_modules/proxy-addr'; lock_rel = None
    for l in sorted(subprocess.run(['git', '-C', repo, 'diff', '--name-only', base, head], capture_output=True, text=True).stdout.split()):
        if l.endswith('package-lock.json') and l != K['root_lock']:
            e = json.loads(git_bytes(repo, base, l)).get('packages', {}).get(key)
            if e and e.get('version') == K['plan']['proxy-addr']['old']: lock_rel = l; break
    print('NC1 lock chosen FROM THE BASE (first changed standalone lock whose base proxy-addr is 2.0.7): %s' % lock_rel)
    p = os.path.join(wt, lock_rel); orig = open(p, 'rb').read(); h0 = sha(p)
    be = json.loads(git_bytes(repo, base, lock_rel))['packages'][key]
    _rewrite_entry(p, key, dict((f, be[f]) for f in ('version', 'resolved', 'integrity') if f in be))
    landed = sha(p) != h0 and json.loads(open(p, 'rb').read())['packages'][key]['version'] == '2.0.7'
    r7, o7 = run(LG['leg7'], dev(wt), out, 'nc1_leg7') if landed else (None, '')
    open(p, 'wb').write(orig); rest = sha(p) == h0
    t.check('NC1', landed and r7 == 1 and 'GHSA-jqcg-44mw-7w3h' in o7 and rest, 'proxy-addr 2.0.7 planted in %s (landed %s) -> leg 7 rc %s naming GHSA-jqcg %s | restored sha256-identical %s' % (
        lock_rel, landed, r7, 'GHSA-jqcg-44mw-7w3h' in o7, rest))
    # NC2
    bp = os.path.join(wt, K['baseline_path']); orig = open(bp, 'rb').read(); h0 = sha(bp)
    j = json.loads(orig); j['accepted'].pop('GHSA-hp3w-g68c-fv3c', None)
    open(bp, 'wb').write((json.dumps(j, indent=2, ensure_ascii=False) + '\n').encode())
    landed = sha(bp) != h0 and b'GHSA-hp3w-g68c-fv3c' not in open(bp, 'rb').read()
    r6, o6 = run(LG['leg6'], dev(wt), out, 'nc2_leg6') if landed else (None, '')
    r7, o7 = run(LG['leg7'], dev(wt), out, 'nc2_leg7') if landed else (None, '')
    open(bp, 'wb').write(orig); rest = sha(bp) == h0
    named = ('sprintf-js' in o6 + o7) or ('GHSA-hp3w-g68c-fv3c' in o6 + o7)
    t.check('NC2', landed and (r6 == 1 or r7 == 1) and named and rest, 'GHSA-hp3w row removed (landed %s) -> leg 6 rc %s, leg 7 rc %s, sprintf-js/hp3w named %s | restored sha256-identical %s' % (
        landed, r6, r7, named, rest))
    # NC3
    lock_rel = 'systemTest/api-explorer/package-lock.json'; key = 'node_modules/postcss-selector-parser'
    p = os.path.join(wt, lock_rel); orig = open(p, 'rb').read(); h0 = sha(p)
    be = json.loads(git_bytes(repo, base, lock_rel))['packages'][key]
    _rewrite_entry(p, key, dict((f, be[f]) for f in ('version', 'resolved', 'integrity') if f in be))
    landed = sha(p) != h0 and json.loads(open(p, 'rb').read())['packages'][key]['version'] == '7.1.4'
    r7, o7 = run(LG['leg7'], dev(wt), out, 'nc3_leg7') if landed else (None, '')
    pr, po = run([sys.executable, os.path.join(HERE, 'c2_locks_gate70.py'), 'parse', '--dir', wt, '--expect-clean'], wt, out, 'nc3_c2parse') if landed else (None, '')
    open(p, 'wb').write(orig); rest = sha(p) == h0
    psp7 = re.search(r"'psp7': (\d+)", po)
    t.check('NC3', landed and r7 == 0 and pr == 1 and psp7 and psp7.group(1) == '1' and rest,
            'psp 7.1.4 planted in %s (landed %s) -> leg 7 rc %s (want 0: MASKED by the rj75 row) | c2 parse rc %s psp7 %s (want 1 / 1) | restored sha256-identical %s' % (
                lock_rel, landed, r7, pr, psp7.group(1) if psp7 else None, rest))


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(tap('# tests 59\n# pass 59\n# fail 0\n') == {'tests': 59, 'pass': 59, 'fail': 0, 'skipped': None, 'todo': None}, 'TAP summary parsed')
    rep(tap('\u2139 tests 59\n\u2139 pass 59\n\u2139 fail 0\n')['pass'] == 59, 'spec-reporter summary (\u2139 pass N, what node 24 prints) parsed')
    rep(tap('ok 1\n')['pass'] is None, 'PLANTED a TAP with no summary yields None (C5 then FAILS, never passes)')
    rep(classify(2).endswith('(NOT RUN)') and classify(124).endswith('(NOT RUN)'), 'rc 2 (COULD-NOT-CHECK) and a timeout classify as NOT RUN')
    rep(count_ids('x GHSA-jqcg-44mw-7w3h y GHSA-jqcg-44mw-7w3h', FIVE)['GHSA-jqcg-44mw-7w3h'] == 2, 'id counting')
    rep(head_ok(0, 0, 'OK no advisories'), 'a clean head output passes G-HEAD')
    rep(not head_ok(0, 0, 'GHSA-68fv-2mgg-jv7q'), 'PLANTED a head output still naming a fixed id FAILS G-HEAD')
    rep(not head_ok(2, 0, ''), 'PLANTED leg 6 rc 2 (COULD-NOT-CHECK) FAILS G-HEAD')
    rep(base_ok(1, 1, 'GHSA-jqcg-44mw-7w3h') and not base_ok(2, 1, 'GHSA-jqcg-44mw-7w3h') and not base_ok(1, 1, 'nothing'),
        'G-BASE: rc 1/1 with the ids passes; rc 2 (a SKIP) and a SILENT rc 1 both FAIL')
    rep(not outside_forbidden(K['forbidden_root'] + '/x') and outside_forbidden('/private/tmp/x'), 'the worktree guard refuses the forbidden root')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if '--selftest' in A: return selftest()
    if not A or not opt('--wt') or not opt('--out'): print(__doc__); return 2
    wt = os.path.abspath(opt('--wt')); out = os.path.abspath(opt('--out')); guard(wt); t = Tally()
    head = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    print('C5 %s in worktree %s at HEAD %s' % (A[0], wt, head))
    if A[0] == 'legs':
        if opt('--expect') not in ('fail', 'pass'): print('REFUSED: --expect fail|pass'); return 2
        legs(wt, opt('--expect'), out, t)
    elif A[0] == 'contract': contract(wt, out, t)
    elif A[0] == 'cleanroom': cleanroom(wt, out, t)
    elif A[0] == 'install': install(wt, out, t)
    elif A[0] == 'nc':
        if not opt('--repo'): print('REFUSED: --repo <your clone> required (the base entries are read from it)'); return 2
        nc(wt, opt('--repo'), opt('--base', K['pr']['parents'][0]), out, t)
    else:
        print(__doc__); return 2
    return t.end()


if __name__ == '__main__':
    sys.exit(main())
