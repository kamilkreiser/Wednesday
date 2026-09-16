#!/usr/bin/env python3
"""drafter_probe.py — copies qa1015-drafter-probe.test.ts into the base and head scratch trees, runs it, quarantines it by rename, prints rows."""
import sys, os, shutil, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1015')
from drafterlib import *
P('drafter_probe start', ts())
res = {}
for tree in ('base', 'head'):
    dst = T[tree] + '/Blockchain/Dev/services/auth/src/__tests__/qa1015-drafter-probe.test.ts'
    shutil.copyfile(GS + '/qa1015-drafter-probe.test.ts', dst)
    env = dict(os.environ); env.pop('NODE_ENV', None); env['QA_PROBE_OUT'] = GS + '/probe_rows_%s.json' % tree
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', 'src/__tests__/qa1015-drafter-probe.test.ts'], cwd=T[tree] + '/Blockchain/Dev/services/auth', env=env, capture_output=True, text=True)
    open(GS + '/probe_%s.vitest.out' % tree, 'w').write(p.stdout + p.stderr)
    P(tree, 'vitest rc', p.returncode, (p.stdout + p.stderr).strip().splitlines()[-4:])
    os.rename(dst, os.path.dirname(T[tree]) + '/QUARANTINE_qa1015-drafter-probe.%s.test.ts.txt' % tree)
    res[tree] = json.load(open(GS + '/probe_rows_%s.json' % tree))
for b, h in zip(res['base'], res['head']):
    assert b['scn'] == h['scn']
    P('\n' + b['scn'])
    for lab, r in (('base', b), ('head', h)):
        P('  %s %d %s | inserts %s | userWrites %s | errorLogs %s | warn %s | pendingRowsForCaller %d | retry-after %s%s' % (lab, r['status'], r['body'][:120], r['inserts'], r['userWrites'], r['errorLogs'], r['warnLogs'], r['pendingRowsForCaller'], r['retryAfter'], (' | tableStatusAfter ' + r['tableStatusAfter']) if 'tableStatusAfter' in r else ''))
    if b['headers'] != h['headers']: P('  HEADERS differ', b['headers'], h['headers'])
P('\nheaders on a head 503 row:', [r['headers'] for r in res['head'] if r['status'] == 503][:1])
P('porcelain base', porcelain('base'), 'head', porcelain('head'))
P('drafter_probe end', ts())
