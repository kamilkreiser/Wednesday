#!/usr/bin/env python3
"""drafter_suites_1032r2.py — #1032 ROUND 2 (KS-1194) in the drafter clone only (cwd inside the clone; from ../2026-09-17_gate1032/drafter_suites_1032.py, re-pinned):
1. WHOLE auth vitest (json) at develop 3961c2add and head 430672697, at DEFAULT ceilings and at --testTimeout=60000 --hookTimeout=60000; reds split
   ASSERTION vs TIMEOUT per file; load read per run. The ks949-platform-admin-seed-identity file alone at default ceilings on both trees.
2. Project tsc --noEmit -p . rc on both trees.
3. THE TEST-INCLUDING tsc program: a scratch tsconfig.qa1032-with-tests.json beside auth's tsconfig (extends it, exclude only node_modules + dist), on both
   trees: rc, error lines, error lines per file; --listFilesOnly proof the ks1194 test is IN it (head) and NOT in the project program; a planted type error
   in the ks1194 test must add errors; restored by bytes + sha256 + git diff --quiet. The scratch tsconfig is MOVED aside after (never rm).
4. eslint (Dev eslint.config.mjs) by rule AND message on users.ts (both trees) and the ks1194 test (head), with a firing control (a planted unused variable in
   the ks1194 test), restored by sha."""
import json, subprocess, datetime, os, hashlib, re, shutil
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
paths = json.load(open(GS + '/out/drafter_paths.json'))
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
TESTREL = 'src/__tests__/ks1194-approve-never-restores-pending-over-a-raised-level.test.ts'
TESTREL1 = 'src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return subprocess.run(['uptime'], capture_output=True, text=True).stdout.split('load averages:')[-1].strip()
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def vitest(tree, tag, extra, files=()):
    out = GS + '/out/suite_%s.json' % tag; err = GS + '/out/suite_%s.stderr' % tag
    with open(err, 'w') as fe:
        p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--reporter=json', '--outputFile=' + out] + extra + list(files), cwd=tree + '/' + A, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI='1'))
    j = json.load(open(out)); reds = {}
    for s in j['testResults']:
        f = [a for a in s['assertionResults'] if a['status'] == 'failed']
        if f or s['status'] != 'passed':
            kinds = ['TIMEOUT' if ('Test timed out' in (a.get('failureMessages') or [''])[0] or 'timed out' in (a.get('failureMessages') or [''])[0]) else ('ASSERT' if (a.get('failureMessages') or [''])[0].startswith('AssertionError') else 'OTHER') for a in f]
            reds[s['name'].split('/src/')[-1]] = dict(n=len(f), kinds=kinds, cells=[(a['title'][:60], a.get('duration'), re.sub(r'\s+', ' ', (a.get('failureMessages') or [''])[0])[:120]) for a in f][:4], msg=(s.get('message') or '')[:160])
    return dict(rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'], pending=j['numPendingTests']), reds
P('drafter_suites_1032r2 start', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for name in ('dev', 'head'):
    tree = paths['trees'][name]
    for tag, extra in (('default', []), ('t60', ['--testTimeout=60000', '--hookTimeout=60000'])):
        l0 = load(); t0 = now(); d, reds = vitest(tree, name + '_' + tag, extra)
        P('SUITE', name, tag, t0, '->', now(), 'load at start', l0, '|', d, '| non-passing', reds)
    l0 = load(); d, reds = vitest(tree, name + '_ks949_default', [], ['src/__tests__/ks949-platform-admin-seed-identity.test.ts'])
    P('KS949 FILE ALONE', name, 'default ceilings load', l0, '|', d, '| non-passing', reds)
    if name == 'head':
        l0 = load(); d, reds = vitest(tree, name + '_ks1194_both_default', [], [TESTREL, TESTREL1])
        P('KS1194 BOTH FILES', name, 'load', l0, '|', d, '| non-passing', reds)
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=tree + '/' + A, capture_output=True, text=True)
    P('PROJECT tsc', name, 'rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    ad = tree + '/' + A
    os.makedirs(tree + '/' + DEV + '/qa_probe_1032r2', exist_ok=True)
    cfg = tree + '/' + DEV + '/qa_probe_1032r2/tsconfig.qa1032r2-with-tests.json'
    open(cfg, 'w').write(json.dumps({'extends': ad + '/tsconfig.json', 'compilerOptions': {'noEmit': True}, 'include': [ad + '/src/**/*'], 'exclude': [ad + '/node_modules', ad + '/dist']}, indent=1))
    lf = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/tsc', '-p', cfg, '--listFilesOnly'], cwd=ad, capture_output=True, text=True).stdout.splitlines()
    lp = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.', '--listFilesOnly'], cwd=ad, capture_output=True, text=True).stdout.splitlines()
    P('TEST-INCLUDING program', name, '| files', len(lf), '__tests__ files', sum('/src/__tests__/' in x for x in lf), '| ks1194 test in it', any(x.endswith(TESTREL) for x in lf), 'r1 test in it', any(x.endswith(TESTREL1) for x in lf),
      '| project program files', len(lp), '__tests__', sum('/src/__tests__/' in x for x in lp), 'ks1194 in project', any(x.endswith(TESTREL) for x in lp), '| control users.ts in project', any(x.endswith('src/routes/users.ts') for x in lp))
    def tsc_tests(tag):
        p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/tsc', '-p', cfg], cwd=ad, capture_output=True, text=True)
        errs = [l for l in (p.stdout + p.stderr).splitlines() if re.search(r'error TS\d+', l)]
        per = {}
        for l in errs: per[l.split('(')[0].split('/src/')[-1]] = per.get(l.split('(')[0].split('/src/')[-1], 0) + 1
        P('TEST-INCLUDING tsc', name, tag, 'rc', p.returncode, 'error lines', len(errs), '| per file', per, '| first', [e[:160] for e in errs[:3]])
        return len(errs)
    base = tsc_tests('as-is')
    if name == 'head':
        tf = ad + '/' + TESTREL; orig = open(tf, 'rb').read(); s0 = sha(tf)
        open(tf, 'wb').write(orig + b"\nconst qa1032Plant: number = 'not a number'; // QA-PLANT\nexport { qa1032Plant };\n")
        planted = tsc_tests('PLANT (a string assigned to number in the ks1194 test)')
        open(tf, 'wb').write(orig); P('   plant restored sha equal', sha(tf) == s0, '| git diff --quiet', subprocess.run(['git', '-C', tree, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode, '| plant added', planted - base)
    P('   scratch tsconfig lives OUTSIDE services/auth:', cfg, '| qa files under services/auth:', sum(1 for dp, dn, fn in os.walk(ad) if 'node_modules' not in dp for f in fn if 'qa1032' in f))
# eslint
def eslint(tree, files, tag):
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/eslint', '-f', 'json'] + files, cwd=tree + '/' + DEV, capture_output=True, text=True)
    try:
        j = json.loads(p.stdout)
        P('ESLINT', tag, 'rc', p.returncode, [(r['filePath'].split('/')[-1][:40], r['errorCount'], r['warningCount'], [(m.get('ruleId'), m['message'][:80]) for m in r['messages']][:4]) for r in j], '| stderr', p.stderr.strip()[:200])
    except Exception as e:
        P('ESLINT', tag, 'rc', p.returncode, 'unparsed', type(e).__name__, p.stdout[:300], p.stderr[:300])
eslint(paths['trees']['dev'], ['services/auth/src/routes/users.ts'], 'develop users.ts')
eslint(paths['trees']['head'], ['services/auth/src/routes/users.ts', 'services/auth/' + TESTREL, 'services/auth/' + TESTREL1], 'head users.ts + both ks1194 tests')
tf = paths['trees']['head'] + '/' + A + '/' + TESTREL; orig = open(tf, 'rb').read(); s0 = sha(tf)
open(tf, 'wb').write(orig + b"\nfunction qa1032Unused(): void { const qa1032Never = 1; } // QA-PLANT eslint control\n")
eslint(paths['trees']['head'], ['services/auth/' + TESTREL], 'CONTROL planted unused in ks1194 test')
open(tf, 'wb').write(orig); P('   eslint plant restored sha equal', sha(tf) == s0, '| git diff --quiet', subprocess.run(['git', '-C', paths['trees']['head'], 'diff', '--quiet', 'HEAD'], capture_output=True).returncode)
P('drafter_suites_1032r2 end', now(), 'load', load())
