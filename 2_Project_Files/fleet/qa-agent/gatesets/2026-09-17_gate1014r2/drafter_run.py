#!/usr/bin/env python3
"""drafter_run.py STAGE TREE... — #1014 ROUND 2 drafter runs in the drafter's OWN clone (drafter_paths.json). Derived from the round-1 GATE's run.py
(evidence/run.py of the r1 report, READ, not edited there). Stages:
  suite  : whole api-gateway suite (vitest JSON reporter; files/tests/failed/pending) + project tsc --noEmit -p . rc
  rbg    : copy head's ks1176 test (blob 43cebf8d7) into the named tree (r1 / base), run it alone, quarantine by rename
  census : copy the ROUND-1 GATE's census harness (qa1014-gate-census.test.ts, copied VERBATIM into this set) into the tree, run alone, rows -> rows_census_<label>.json
  spell  : copy qa1014r2-drafter-spellings.test.ts into the tree, run alone, rows -> rows_spell_<label>.json
Never rm; stderr kept per run in the workdir; NODE_ENV popped (vitest sets test)."""
import subprocess, os, json, sys, datetime, shutil, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'
PA = json.load(open(GS + '/drafter_paths.json')); W = PA['W']; T = PA['trees']
GW = 'Blockchain/Dev/services/api-gateway'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def quarantine(p):
    q = W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True)
    d = q + '/' + datetime.datetime.now().strftime('%H%M%S%f') + '.' + p.replace('/', '__')[-150:]; os.rename(p, d); P('quarantined', p.split('/src/')[-1], '->', d.split('/')[-1])
def vitest(tree, files, label, env_extra=None):
    cwd = T[tree] + '/' + GW; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None); env.update(env_extra or {})
    t0 = datetime.datetime.now()
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=cwd, env=env, capture_output=True, text=True)
    open(W + '/stderr_%s.txt' % label, 'w').write(p.stderr)
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON rc', p.returncode, 'stderr tail:', p.stderr[-2500:]); return None
    np = [(tr['name'].split('/src/')[-1], a['fullName'], a['status'], (a.get('failureMessages') or [''])[0][:400]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] != 'passed']
    sm = [(tr['name'].split('/src/')[-1], tr.get('message', '')[:400]) for tr in j['testResults'] if tr.get('message')]
    r = dict(label=label, tree=tree, rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'], pending=j.get('numPendingTests'), todo=j.get('numTodoTests'), failed_suites=j.get('numFailedTestSuites'), success=j.get('success'), secs=round((datetime.datetime.now() - t0).total_seconds(), 1))
    P(ts(), json.dumps(r))
    for x in np: P('   NOT-PASSED', x)
    for x in sm: P('   SUITE MSG', x)
    r['notpassed'] = np; json.dump(r, open(GS + '/vt_%s.json' % label, 'w'), indent=1); return r
def tsc(tree):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T[tree] + '/' + GW, capture_output=True, text=True)
    P(ts(), 'project tsc --noEmit -p . tree', tree, 'rc', p.returncode, 'lines', len((p.stdout + p.stderr).splitlines()), (p.stdout + p.stderr)[:600]); return p.returncode
def probe(tree, harness, label, outname, env_extra=None):
    dst = T[tree] + '/' + GW + '/src/__tests__/' + harness
    shutil.copyfile(GS + '/' + harness, dst); P('copied', harness, 'sha', hashlib.sha256(open(dst, 'rb').read()).hexdigest()[:12], 'into', tree, 'label', label)
    e = {'QA_OUT': GS + '/' + outname}; e.update(env_extra or {})
    r = vitest(tree, ['src/__tests__/' + harness], label, e)
    quarantine(dst); return r
if __name__ == '__main__':
    stage, trees = sys.argv[1], sys.argv[2:]
    P('drafter_run', stage, trees, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
    for tree in trees:
        label = os.environ.get('QA_LABEL', tree)
        if stage == 'suite':
            vitest(tree, [], 'suite_' + tree); tsc(tree)
        elif stage == 'rbg':
            src = T['head'] + '/' + GW + '/src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts'
            dst = T[tree] + '/' + GW + '/src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts'
            saved = open(dst, 'rb').read() if os.path.exists(dst) else None
            shutil.copyfile(src, dst); b = subprocess.run(['git', 'hash-object', dst], capture_output=True, text=True).stdout.strip(); P('copied ks1176 blob', b, 'into', tree, '(replacing tracked copy)' if saved else '(new file)'); assert b.startswith('43cebf8d7')
            for f in ('services/enforcement.ts', 'routes/verification.ts'):
                P('  tree', f, 'blob', subprocess.run(['git', '-C', T[tree], 'rev-parse', 'HEAD:' + GW + '/src/' + f], capture_output=True, text=True).stdout.strip()[:9])
            vitest(tree, ['src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts'], 'rbg_' + tree)
            if saved is None: quarantine(dst)
            else:
                open(dst, 'wb').write(saved); P('restored tracked ks1176 in', tree, 'git diff --quiet rc', subprocess.run(['git', '-C', T[tree], 'diff', '--quiet'], capture_output=True).returncode)
        elif stage == 'census':
            probe(tree, 'qa1014-gate-census.test.ts', 'census_' + label, 'rows_census_%s.json' % label)
        elif stage == 'spell':
            probe(tree, 'qa1014r2-drafter-spellings.test.ts', 'spell_' + label, 'rows_spell_%s.json' % label)
        r = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); P('tracked porcelain', tree, len(r.stdout.splitlines()), r.stdout[:300], r.stderr.strip()[:200])
    P('drafter_run end', ts())
