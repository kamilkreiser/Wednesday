#!/usr/bin/env python3
"""drafter_run.py — #1014 (KS-1176) drafter runs in the drafter's OWN clone (drafter_paths.json). Stages:
  probe <tree>...   copy qa1014-drafter-principals.test.ts into the tree, run it alone (vitest JSON), rows -> probe_rows_<tree>.json, then quarantine the copy by rename
  suite <tree>...   the whole api-gateway suite (JSON reporter: files, tests, failed, pending) + project tsc -p . rc
Never rm; stderr kept in the outputs; NODE_ENV popped for the runner (vitest sets test)."""
import subprocess, os, json, sys, datetime, shutil, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'
PATHS = json.load(open(GS + '/drafter_paths.json')); W = PATHS['W']; T = PATHS['trees']
GW = 'Blockchain/Dev/services/api-gateway'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def vitest(tree, files, label, env_extra=None):
    cwd = T[tree] + '/' + GW; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None); env.update(env_extra or {})
    t0 = datetime.datetime.now()
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=cwd, env=env, capture_output=True, text=True)
    dt = (datetime.datetime.now() - t0).total_seconds()
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON rc', p.returncode, 'stderr tail:', p.stderr[-2500:]); return None
    notpassed = [(tr['name'].split('/src/')[-1], a['fullName'], a['status'], (a.get('failureMessages') or [''])[0][:300]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] != 'passed']
    suite_msgs = [(tr['name'].split('/src/')[-1], tr.get('message', '')[:300]) for tr in j['testResults'] if tr.get('message')]
    r = dict(label=label, tree=tree, rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'], pending=j.get('numPendingTests'), failed_suites=j.get('numFailedTestSuites'), success=j.get('success'), secs=round(dt, 1))
    P(ts(), json.dumps(r))
    for x in notpassed: P('   NOT-PASSED', x)
    for x in suite_msgs: P('   SUITE MSG', x)
    if p.returncode != 0 and not notpassed: P('   stderr tail:', p.stderr[-1500:])
    r['notpassed'] = notpassed; json.dump(r, open(GS + '/vt_%s.json' % label, 'w'), indent=1)
    return r
stage, trees = sys.argv[1], sys.argv[2:]
P('drafter_run', stage, trees, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for tree in trees:
    if stage == 'probe':
        dst = T[tree] + '/' + GW + '/src/__tests__/qa1014-drafter-principals.test.ts'
        shutil.copyfile(GS + '/qa1014-drafter-principals.test.ts', dst)
        P('copied probe sha', hashlib.sha256(open(dst, 'rb').read()).hexdigest()[:12], 'into', tree)
        vitest(tree, ['src/__tests__/qa1014-drafter-principals.test.ts'], 'probe_' + tree, {'QA1014_OUT': GS + '/probe_rows_%s.json' % tree})
        qdir = W + '/_quarantine_2026-09-17'; os.makedirs(qdir, exist_ok=True)
        os.rename(dst, qdir + '/%s.%s.qa1014-drafter-principals.test.ts' % (tree, datetime.datetime.now().strftime('%H%M%S')))
        P('quarantined probe copy out of', tree)
    elif stage == 'suite':
        vitest(tree, [], 'suite_' + tree)
        t0 = datetime.datetime.now()
        p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T[tree] + '/' + GW, capture_output=True, text=True)
        P(ts(), 'project tsc -p . tree', tree, 'rc', p.returncode, 'lines', len((p.stdout + p.stderr).splitlines()), 'secs', (datetime.datetime.now() - t0).seconds)
    rc = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True)
    P('tracked porcelain', tree, len(rc.stdout.splitlines()), rc.stderr.strip()[:200])
P('drafter_run end', ts())
