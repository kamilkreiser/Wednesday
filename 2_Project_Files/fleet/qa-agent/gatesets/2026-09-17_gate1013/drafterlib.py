"""drafterlib.py — shared helpers for the #1013 (KS-999) drafter runs (vitest JSON reporter, anchored edits with sha-asserted restore). Adapted from the #1010 set."""
import subprocess, os, json, datetime, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013'
PATHS = json.load(open(GS + '/drafter_paths.json')); W = PATHS['W']; T = PATHS['trees']
PKG = {'shared': 'Blockchain/Dev/packages/shared', 'auth': 'Blockchain/Dev/services/auth'}
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def vitest(label, tree, pkg, files=(), save=True):
    cwd = T[tree] + '/' + PKG[pkg]; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None)
    t0 = datetime.datetime.now()
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=cwd, env=env, capture_output=True, text=True)
    dt = (datetime.datetime.now() - t0).total_seconds()
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON rc', p.returncode, p.stderr[-1500:]); return None
    cells = {}
    for tr in j['testResults']:
        fn = tr['name'].split('/src/')[-1]
        for a in tr['assertionResults']:
            cells[fn + ' :: ' + a['fullName']] = {'status': a['status'], 'msg': (a.get('failureMessages') or [''])[0][:400]}
    r = {'label': label, 'tree': tree, 'pkg': pkg, 'rc': p.returncode, 'files': len(j['testResults']), 'tests': j['numTotalTests'], 'passed': j['numPassedTests'], 'failed': j['numFailedTests'], 'pending': j.get('numPendingTests'), 'failed_suites': j.get('numFailedTestSuites'), 'success': j.get('success'), 'secs': round(dt, 1), 'cells': cells, 'stderr_tail': p.stderr[-2000:]}
    P(ts(), '%-26s tree %-4s pkg %-6s rc %d FILES %d TESTS %d passed %d failed %d pending %s failed_suites %s success %s secs %.1f' % (label, tree, pkg, p.returncode, r['files'], r['tests'], r['passed'], r['failed'], r['pending'], r['failed_suites'], r['success'], dt))
    for k, v in cells.items():
        if v['status'] != 'passed': P('    NOT-PASSED', v['status'], k[:200], '|', v['msg'].split('\n')[0][:200])
    if save: json.dump(r, open(GS + '/vt_%s.json' % label, 'w'), indent=1)
    return r
def tsc_project(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', 'services/auth'], cwd=T[tree] + '/Blockchain/Dev', capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)
def porcelain(tree): return subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip().splitlines()
