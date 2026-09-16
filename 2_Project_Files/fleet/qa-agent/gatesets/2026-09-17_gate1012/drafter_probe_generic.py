#!/usr/bin/env python3
"""drafter_probe_generic.py — usage: <probe file> <package> <trees...>; place qa1012-drafter-probe.test.ts into services/security/src/__tests__ of each clone tree, run it SOLO, collect rows, MOVE it out
(quarantine by rename; never rm). Porcelain asserted back to baseline."""
import subprocess, os, shutil, json, datetime, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1012'
PATHS = json.load(open(GS + '/drafter_paths.json')); W = PATHS['W']; T = PATHS['trees']
NAME = sys.argv[1]; PKG = sys.argv[2]; REL = 'Blockchain/Dev/services/%s/src/__tests__/%s' % (PKG, NAME)
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def porc(t): return subprocess.run(['git', '-C', T[t], 'status', '--porcelain', '--untracked-files=all'], capture_output=True, text=True).stdout.strip().splitlines()
P('drafter_probe', datetime.datetime.now().astimezone().strftime('%H:%M:%S'))
for t in sys.argv[3:]:
    b = len(porc(t)); dst = T[t] + '/' + REL; shutil.copyfile(GS + '/' + NAME, dst)
    out = GS + '/probe_rows_%s_%s.json' % (NAME.split('.')[0], t); env = dict(os.environ); env.pop('NODE_ENV', None); env['PROBE_OUT'] = out
    p = subprocess.run([T[t] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', 'src/__tests__/' + NAME, '--reporter=json', '--outputFile=' + W + '/probe_%s_%s.json' % (NAME.split('.')[0], t)], cwd=T[t] + '/Blockchain/Dev/services/' + PKG, env=env, capture_output=True, text=True)
    q = W + '/_quarantine_%s_%s_%s.ts' % (NAME.split('.')[0], t, datetime.datetime.now().strftime('%H%M%S')); os.rename(dst, q)
    P('tree', t, 'vitest rc', p.returncode, 'moved out ->', q, '| porcelain back to baseline', len(porc(t)) == b)
    P('  stderr tail:', p.stderr[-800:].replace('\n', ' | '))
    try:
        for r in json.load(open(out)): P('  ROW', json.dumps(r)[:700])
    except Exception as e: P('  NO ROWS', e)
P('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S'))
