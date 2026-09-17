#!/usr/bin/env python3
"""drafter_probe_1034.py TREE... — write the real-gateway probe (src/qa1034-drafter-probe.template.ts) to <tree>/Blockchain/Dev/qa_probe_1034/ (OUTSIDE
services/api-gateway), run it SOLO through a scratch vitest config (root = the service dir, setupFiles = its vitest.setup.ts, include = the probe's absolute
path) on vitest 4.1.11 (node .../node_modules/vitest/vitest.mjs); assert the probe is NOT in the service's tsc program (--listFilesOnly, control auth.ts
listed) nor in the whole-suite collection (vitest list --filesOnly, control ks1215 listed on head); rows -> out/rows_probe_<tree>.json; quarantine the probe
dir by MOVE. Never rm; stderr kept; NODE_ENV popped."""
import subprocess, os, json, sys, datetime, hashlib, shutil
GSD = os.path.dirname(os.path.abspath(__file__)); OUTD = GSD + '/out'
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; T = PA['trees']
GW = 'Blockchain/Dev/services/api-gateway'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
for tree in sys.argv[1:]:
    D = T[tree] + '/Blockchain/Dev/qa_probe_1034'; os.makedirs(D)
    tpl = open(GSD + '/src/qa1034-drafter-probe.template.ts').read()
    src = tpl.replace('__GW_SRC__', T[tree] + '/' + GW + '/src')
    pf = D + '/qa1034-drafter-probe.test.ts'; open(pf, 'w').write(src)
    cfg = D + '/vitest.qa1034.config.mts'
    open(cfg, 'w').write("import { defineConfig } from 'vitest/config';\nexport default defineConfig({ root: %r, test: { globals: true, environment: 'node', setupFiles: [%r], include: [%r], dir: %r } });\n"
                         % (T[tree] + '/' + GW, T[tree] + '/' + GW + '/vitest.setup.ts', pf, D))
    P(ts(), 'probe', tree, 'written', pf.split('/Blockchain/')[-1], '| template sha256', hashlib.sha256(tpl.encode()).hexdigest()[:16], '| load', load())
    VT = T[tree] + '/Blockchain/Dev/node_modules/vitest/vitest.mjs'
    env = dict(os.environ); env.pop('NODE_ENV', None)
    try:
        p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/typescript/bin/tsc', '--noEmit', '-p', '.', '--listFilesOnly'], cwd=T[tree] + '/' + GW, capture_output=True, text=True)
        P('F-3 control: service tsc program files with qa_probe:', sum('qa_probe' in l for l in p.stdout.splitlines()), '| positive control auth.ts listed:', sum(l.endswith('/src/middleware/auth.ts') for l in p.stdout.splitlines()), '| rc', p.returncode)
        p = subprocess.run(['node', VT, 'list', '--filesOnly'], cwd=T[tree] + '/' + GW, capture_output=True, text=True, env=env)
        L = p.stdout.splitlines()
        P('F-3 control: vitest list --filesOnly with the probe present: files', len(L), '| qa_probe', sum('qa_probe' in l for l in L), '| ks1215 listed', sum('ks1215' in l for l in L), '| rc', p.returncode, p.stderr.strip()[-200:])
        out = OUTD + '/rows_probe_%s.json' % tree; t0 = ts(); l0 = load()
        e2 = dict(env, QA_OUT=out, QA_ROUTES=OUTD + '/mounts_%s.json' % tree)
        p = subprocess.run(['node', VT, 'run', '--config', cfg, '--reporter=json', '--outputFile=' + W + '/probe_%s.json' % tree], cwd=T[tree] + '/' + GW, capture_output=True, text=True, env=e2)
        open(OUTD + '/probe_%s.stderr.txt' % tree, 'w').write(p.stderr); open(OUTD + '/probe_%s.stdout.txt' % tree, 'w').write(p.stdout[-20000:])
        try:
            j = json.load(open(W + '/probe_%s.json' % tree))
            P(ts(), 'probe run', tree, t0, '-> now | load', l0, '->', load(), '| rc', p.returncode, '| tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'],
              [(a['title'], a['status'], (a.get('failureMessages') or [''])[0][:300]) for s in j['testResults'] for a in s['assertionResults']], [s.get('message', '')[:300] for s in j['testResults']])
        except Exception as e:
            P('probe run', tree, 'NO JSON', type(e).__name__, 'rc', p.returncode, p.stderr[-1500:])
        P('   rows file', os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0, '| stderr Unhandled mentions', p.stderr.count('Unhandled'))
    finally:
        q = W + '/_quarantine'; os.makedirs(q, exist_ok=True); dst = q + '/qa_probe_1034.%s.%s' % (tree, datetime.datetime.now().strftime('%H%M%S')); shutil.move(D, dst); P('   probe dir MOVED to', dst.split('/')[-1])
        r = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=all'], capture_output=True, text=True); P('   porcelain (untracked incl.)', len([l for l in r.stdout.splitlines() if 'node_modules' not in l and 'packages/shared/dist' not in l]), r.stdout[:300])
