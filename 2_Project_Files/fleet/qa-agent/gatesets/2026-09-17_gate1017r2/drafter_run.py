#!/usr/bin/env python3
"""drafter_run.py STAGE TREE... — #1017 ROUND 2 drafter runs in the drafter's OWN clone (drafter_paths.json). Derived from the round-1 GATE's run.py.
Stages: suite (whole api-gateway suite JSON + project tsc --noEmit -p . rc), shared (whole packages/shared), probe (copy the harness named by QA_HARNESS
[default r1gate_qa1017-gate-probe.test.ts, the round-1 gate's harness VERBATIM] into the tree under its original basename, run SOLO, rows ->
rows/<label>.json, quarantine by rename). Never rm; stderr kept per run; NODE_ENV popped (vitest sets test). Asserts cells RAN."""
import subprocess, os, json, sys, datetime, shutil, hashlib
GS = os.path.dirname(os.path.abspath(__file__))
PA = json.load(open(GS + '/drafter_paths.json')); W = PA['W']; T = PA['T']
GW = 'Blockchain/Dev/services/api-gateway'; SH = 'Blockchain/Dev/packages/shared'
os.makedirs(GS + '/vt', exist_ok=True); os.makedirs(GS + '/rows', exist_ok=True); os.makedirs(W + '/stderr', exist_ok=True)
def ts(): return subprocess.run(['date', '+%H:%M:%S %Z'], capture_output=True, text=True).stdout.strip()
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def quarantine(p):
    q = W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True)
    d = q + '/' + datetime.datetime.now().strftime('%H%M%S%f') + '.' + os.path.basename(p); os.rename(p, d); P('quarantined', os.path.basename(p), '->', d.split('/')[-1])
def vitest(tree, files, label, env_extra=None, pkg=GW):
    cwd = T[tree] + '/' + pkg; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None); env.update(env_extra or {})
    t0 = datetime.datetime.now()
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=cwd, env=env, capture_output=True, text=True)
    open(W + '/stderr/%s.txt' % label, 'w').write(p.stderr + '\n--- stdout ---\n' + p.stdout[-20000:])
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON (load failure, NOT a red) rc', p.returncode, 'stderr tail:', p.stderr[-2500:]); return None
    np = [(tr['name'].split('/src/')[-1], a['fullName'], a['status'], (a.get('failureMessages') or [''])[0][:500]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] != 'passed']
    sm = [(tr['name'].split('/src/')[-1], tr.get('message', '')[:500]) for tr in j['testResults'] if tr.get('message')]
    r = dict(label=label, tree=tree, rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'], pending=j.get('numPendingTests'), todo=j.get('numTodoTests'), failed_suites=j.get('numFailedTestSuites'), success=j.get('success'), secs=round((datetime.datetime.now() - t0).total_seconds(), 1))
    P(ts(), json.dumps(r))
    if r['tests'] == 0: P('   INVALID: 0 cells ran')
    for x in np: P('   NOT-PASSED', x[:3], x[3][:300].replace('\n', ' | '))
    for x in sm: P('   SUITE MSG', x)
    r['notpassed'] = np; r['suite_msgs'] = sm; json.dump(r, open(GS + '/vt/%s.json' % label, 'w'), indent=1); return r
def tsc(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T[tree] + '/' + GW, capture_output=True, text=True)
    P(ts(), 'project tsc --noEmit -p . tree', tree, 'rc', p.returncode, 'lines', len((p.stdout + p.stderr).splitlines()), (p.stdout + p.stderr)[:800]); return p.returncode
def probe(tree, label, env_extra=None, harness=None):
    src = harness or os.environ.get('QA_HARNESS', 'r1gate_qa1017-gate-probe.test.ts')
    base = src.replace('r1gate_', '')
    dst = T[tree] + '/' + GW + '/src/__tests__/' + base
    assert not os.path.exists(dst)
    shutil.copyfile(GS + '/' + src, dst); P('copied', src, 'as', base, 'sha', hashlib.sha256(open(dst, 'rb').read()).hexdigest()[:12], 'into', tree, 'label', label)
    e = {'QA_OUT': GS + '/rows/%s.json' % label}; e.update(env_extra or {})
    r = vitest(tree, ['src/__tests__/' + base], 'probe_' + label, e)
    quarantine(dst); return r
def porcelain(tree):
    r = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); P('tracked porcelain', tree, len(r.stdout.splitlines()), r.stdout[:300], r.stderr.strip()[:200]); return r.stdout
if __name__ == '__main__':
    stage, trees = sys.argv[1], sys.argv[2:]
    P('drafter_run', stage, trees, subprocess.run(['date', '+%Y-%m-%d %H:%M:%S %Z'], capture_output=True, text=True).stdout.strip())
    for tree in trees:
        label = os.environ.get('QA_LABEL', tree)
        if stage == 'suite': vitest(tree, [], 'suite_' + tree); tsc(tree)
        elif stage == 'shared': vitest(tree, [], 'shared_' + tree, pkg=SH)
        elif stage == 'probe':
            env = {k: v for k, v in os.environ.items() if k.startswith('QA_') and k not in ('QA_LABEL', 'QA_OUT', 'QA_HARNESS')}
            probe(tree, label, env)
        porcelain(tree)
    P('drafter_run end', ts())
