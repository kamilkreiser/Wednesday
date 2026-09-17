#!/usr/bin/env python3
"""drafter_suites_1035.py — #1035 (KS-1204) checks in the drafter clone only (cwd inside the clone). Copied from the previous gate drafter suites script (asserted substitutions).
1. WHOLE api-gateway vitest 4.1.11 (node <tree>/Blockchain/Dev/node_modules/vitest/vitest.mjs; the version printed per run) at develop 732c13459 and head
   4b1fb0621, at DEFAULT ceilings and at --testTimeout=60000 --hookTimeout=60000; reds split ASSERT / TIMEOUT / OTHER per file; load beside every run.
2. Project tsc --noEmit -p . rc on both trees.
3. THE TEST-INCLUDING tsc program (the gateway tsconfig excludes src/__tests__), from a scratch tsconfig OUTSIDE services/ (#1029's R-1029-7):
   <tree>/Blockchain/Dev/qa_tsc_1035/tsconfig.json extends ../services/api-gateway/tsconfig.json, include ../services/api-gateway/src/**/*; rc, error
   lines, per file; --listFilesOnly proof the ks1204 test is IN it and NOT in the project program; a planted type error in the ks1204 test must add
   errors; restored by bytes + sha + git diff --quiet. The scratch dir is MOVED to WORKDIR/_quarantine after (never rm).
4. eslint (Dev eslint.config.mjs) by rule AND message on routes/verification.ts (both trees) and the ks1204 test (head), with a firing control, restored by sha."""
import json, subprocess, datetime, os, hashlib, re, shutil, sys
GS = os.path.dirname(os.path.abspath(__file__))
PA = json.load(open(GS + '/out/drafter_paths.json')); W = PA['W']; T = PA['trees']
DEV = 'Blockchain/Dev'; GW = DEV + '/services/api-gateway'
TESTREL = 'src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts'
os.makedirs(GS + '/out/suites', exist_ok=True)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def vitest(tree, tag, extra, files=()):
    out = GS + '/out/suites/suite_%s.json' % tag; err = GS + '/out/suites/suite_%s.stderr' % tag
    env = dict(os.environ, CI='1'); env.pop('NODE_ENV', None)
    with open(err, 'w') as fe:
        p = subprocess.run(['node', tree + '/' + DEV + '/node_modules/vitest/vitest.mjs', 'run', '--reporter=json', '--outputFile=' + out] + extra + list(files), cwd=tree + '/' + GW, stdout=subprocess.PIPE, stderr=fe, text=True, env=env)
    j = json.load(open(out)); reds = {}
    for s in j['testResults']:
        f = [a for a in s['assertionResults'] if a['status'] == 'failed']
        if f or s['status'] != 'passed':
            kinds = ['TIMEOUT' if 'timed out' in (a.get('failureMessages') or [''])[0] else ('ASSERT' if (a.get('failureMessages') or [''])[0].startswith('AssertionError') else 'OTHER') for a in f]
            reds[s['name'].split('/src/')[-1]] = dict(n=len(f), kinds=kinds, cells=[(a['title'][:60], a.get('duration'), re.sub(r'\s+', ' ', (a.get('failureMessages') or [''])[0])[:120]) for a in f][:4], msg=(s.get('message') or '')[:160])
    ks = [a for s in j['testResults'] if s['name'].endswith(TESTREL.split('/')[-1]) for a in s['assertionResults']]
    errtxt = open(err).read()
    return dict(rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'], pending=j['numPendingTests'],
                ks1204=(sum(a['status'] == 'passed' for a in ks), len(ks)), unhandled_in_stderr=len(re.findall(r'Unhandled', errtxt)), process_exit_in_stderr=len(re.findall(r'process\.exit', errtxt))), reds
P('drafter_suites_1035 start', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for name in ('dev', 'head'):
    tree = T[name]
    P('vitest version', name, subprocess.run(['node', tree + '/' + DEV + '/node_modules/vitest/vitest.mjs', '--version'], cwd=tree + '/' + GW, capture_output=True, text=True).stdout.strip())
    for tag, extra in (('default', []), ('t60', ['--testTimeout=60000', '--hookTimeout=60000'])):
        l0 = load(); t0 = now(); d, reds = vitest(tree, name + '_' + tag, extra)
        P('SUITE', name, tag, t0, '->', now(), 'load start', l0, 'end', load(), '|', d, '| non-passing', reds)
    p = subprocess.run([tree + '/' + DEV + '/node_modules/typescript/bin/tsc', '--noEmit', '-p', '.'], cwd=tree + '/' + GW, capture_output=True, text=True)
    P('PROJECT tsc', name, 'rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    qd = tree + '/' + DEV + '/qa_tsc_1035'; os.makedirs(qd); cfg = qd + '/tsconfig.json'
    open(cfg, 'w').write(json.dumps({'extends': '../services/api-gateway/tsconfig.json', 'compilerOptions': {'noEmit': True}, 'include': ['../services/api-gateway/src/**/*'], 'exclude': ['../services/api-gateway/node_modules', '../services/api-gateway/dist']}, indent=1))
    TSC = tree + '/' + DEV + '/node_modules/typescript/bin/tsc'
    lf = subprocess.run([TSC, '-p', cfg, '--listFilesOnly'], cwd=qd, capture_output=True, text=True).stdout.splitlines()
    lp = subprocess.run([TSC, '-p', '.', '--listFilesOnly'], cwd=tree + '/' + GW, capture_output=True, text=True).stdout.splitlines()
    P('TEST-INCLUDING program', name, '(config OUTSIDE services/: Blockchain/Dev/qa_tsc_1035) | files', len(lf), '__tests__ files', sum('/src/__tests__/' in x for x in lf), '| ks1204 test in it', any(x.endswith(TESTREL) for x in lf),
      '| project program files', len(lp), '__tests__', sum('/src/__tests__/' in x for x in lp), 'ks1204 in project', any(x.endswith(TESTREL) for x in lp), '| control verification.ts in project', any(x.endswith('src/routes/verification.ts') for x in lp),
      '| qa_tsc files in project program', sum('qa_tsc' in x for x in lp))
    def tsc_tests(tag):
        p = subprocess.run([TSC, '-p', cfg], cwd=qd, capture_output=True, text=True)
        errs = [l for l in (p.stdout + p.stderr).splitlines() if re.search(r'error TS\d+', l)]
        per = {}
        for l in errs: k = l.split('(')[0].split('/src/')[-1]; per[k] = per.get(k, 0) + 1
        P('TEST-INCLUDING tsc', name, tag, 'rc', p.returncode, 'error lines', len(errs), '| files with errors', len(per), '| per file', per, '| first', [e[:160] for e in errs[:3]])
        return len(errs), per
    base, per = tsc_tests('as-is')
    if name == 'head':
        tf = tree + '/' + GW + '/' + TESTREL; orig = open(tf, 'rb').read(); s0 = sha(tf)
        open(tf, 'wb').write(orig + b"\nconst qa1035Plant: number = 'not a number'; // QA-PLANT\nexport { qa1035Plant };\n")
        planted, per2 = tsc_tests('PLANT (a string assigned to number in the ks1204 test)')
        open(tf, 'wb').write(orig); P('   plant restored sha equal', sha(tf) == s0, '| git diff --quiet', subprocess.run(['git', '-C', tree, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode, '| plant added', planted - base, '| ks1204 lines as-is', per.get(TESTREL, 0))
    q = W + '/_quarantine'; os.makedirs(q, exist_ok=True); dst = q + '/qa_tsc_1035.%s.%s' % (name, datetime.datetime.now().strftime('%H%M%S')); shutil.move(qd, dst); P('   scratch tsc dir MOVED to', dst.split('/')[-1])
def eslint(tree, files, tag):
    p = subprocess.run(['node', tree + '/' + DEV + '/node_modules/eslint/bin/eslint.js', '-f', 'json'] + files, cwd=tree + '/' + DEV, capture_output=True, text=True)
    try:
        j = json.loads(p.stdout)
        P('ESLINT', tag, 'rc', p.returncode, [(r['filePath'].split('/')[-1][:40], r['errorCount'], r['warningCount'], [(m.get('ruleId'), m.get('severity'), m.get('line'), m['message'][:80]) for m in r['messages']][:6]) for r in j], '| stderr', p.stderr.strip()[:200])
    except Exception as e:
        P('ESLINT', tag, 'rc', p.returncode, 'unparsed', type(e).__name__, p.stdout[:300], p.stderr[:300])
eslint(T['dev'], ['services/api-gateway/src/routes/verification.ts'], 'develop verification.ts')
eslint(T['head'], ['services/api-gateway/src/routes/verification.ts', 'services/api-gateway/' + TESTREL], 'head verification.ts + ks1204 test')
tf = T['head'] + '/' + GW + '/' + TESTREL; orig = open(tf, 'rb').read(); s0 = sha(tf)
open(tf, 'wb').write(orig + b"\nexport function qa1035Unused(): void { const qa1035Never = 1; } // QA-PLANT eslint control\n")
eslint(T['head'], ['services/api-gateway/' + TESTREL], 'CONTROL planted unused in ks1204 test')
open(tf, 'wb').write(orig); P('   eslint plant restored sha equal', sha(tf) == s0, '| git diff --quiet', subprocess.run(['git', '-C', T['head'], 'diff', '--quiet', 'HEAD'], capture_output=True).returncode)
P('drafter_suites_1035 end', now(), 'load', load())
