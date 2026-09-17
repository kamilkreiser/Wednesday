#!/usr/bin/env python3
"""drafter_run.py STAGE TREE... — #1023 drafter runs in the drafter's own clone (drafter_paths.json). Derived from the #1019r2 drafter_run.py. Stages:
  suite  : whole api-gateway suite (vitest JSON) + project tsc --noEmit -p . rc
  shared : whole packages/shared suite
  probe  : copy qa1023-drafter-probe.test.ts into the tree, run SOLO, rows -> rows/rows_<label>.json, quarantine the copy by rename (QA_STAGES)
  solo   : one api-gateway test file SOLO (QA_FILE)
Cells RAN asserted (0-cell run = INVALID). Never rm; stderr kept per run. NODE_ENV popped (vitest sets test)."""
import subprocess, os, json, sys, datetime, shutil, hashlib
GSD = os.path.dirname(os.path.abspath(__file__)); EV = GSD + '/vt'; os.makedirs(EV, exist_ok=True); os.makedirs(GSD + '/rows', exist_ok=True)
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; T = PA['trees']
GW = 'Blockchain/Dev/services/api-gateway'; SH = 'Blockchain/Dev/packages/shared'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def quarantine(p):
    q = W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True)
    d = q + '/' + datetime.datetime.now().strftime('%H%M%S%f') + '.' + p.replace('/', '__')[-150:]; os.rename(p, d); P('quarantined', p.split('/src/')[-1], '->', d.split('/')[-1])
def vitest(tree, files, label, env_extra=None, pkg=GW):
    cwd = T[tree] + '/' + pkg; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None); env.update(env_extra or {})
    t0 = datetime.datetime.now()
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=cwd, env=env, capture_output=True, text=True)
    open(W + '/stderr_%s.txt' % label, 'w').write(p.stderr); open(W + '/stdout_%s.txt' % label, 'w').write(p.stdout)
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON (INVALID, not a red) rc', p.returncode, 'stderr tail:', p.stderr[-2000:]); return None
    np = [(tr['name'].split('/src/')[-1], a['fullName'], a['status'], (a.get('failureMessages') or [''])[0][:500]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] != 'passed']
    sm = [(tr['name'].split('/src/')[-1], tr.get('message', '')[:400]) for tr in j['testResults'] if tr.get('message')]
    r = dict(label=label, tree=tree, rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'],
             pending=j.get('numPendingTests'), todo=j.get('numTodoTests'), success=j.get('success'), secs=round((datetime.datetime.now() - t0).total_seconds(), 1))
    r['VALID'] = r['tests'] > 0
    P(ts(), json.dumps(r))
    for x in np: P('   NOT-PASSED', x[:3], '|', x[3].split('\n')[0][:300])
    for x in sm: P('   SUITE MSG', x)
    r['notpassed'] = np; json.dump(r, open(EV + '/vt_%s.json' % label, 'w'), indent=1)
    return r
def tsc(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T[tree] + '/' + GW, capture_output=True, text=True)
    P(ts(), 'project tsc --noEmit -p . tree', tree, 'rc', p.returncode, 'lines', len((p.stdout + p.stderr).splitlines()), (p.stdout + p.stderr)[:800]); return p.returncode
def probe(tree, label, env_extra=None):
    h = 'qa1023-drafter-probe.test.ts'; dst = T[tree] + '/' + GW + '/src/__tests__/' + h
    shutil.copyfile(GSD + '/' + h, dst); P('copied', h, 'sha', hashlib.sha256(open(dst, 'rb').read()).hexdigest()[:12], 'into', tree, 'label', label)
    e = {'QA_OUT': GSD + '/rows/rows_%s.json' % label}; e.update(env_extra or {})
    try: return vitest(tree, ['src/__tests__/' + h], 'probe_' + label, e)
    finally: quarantine(dst)
if __name__ == '__main__':
    stage, trees = sys.argv[1], sys.argv[2:]
    P('run', stage, trees, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
    for tree in trees:
        label = os.environ.get('QA_LABEL', tree)
        if stage == 'suite': vitest(tree, [], 'suite_' + tree); tsc(tree)
        elif stage == 'shared': vitest(tree, [], 'shared_' + tree, pkg=SH)
        elif stage == 'probe': probe(tree, label + ('' if len(trees) == 1 else '_' + tree), {'QA_STAGES': os.environ['QA_STAGES']} if os.environ.get('QA_STAGES') else None)
        elif stage == 'solo': vitest(tree, [os.environ['QA_FILE']], 'solo_' + label)
        r = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); P('tracked porcelain', tree, len(r.stdout.splitlines()), r.stdout[:300], r.stderr.strip()[:200])
    P('run end', ts())
