#!/usr/bin/env python3
"""drafter_probe.py — copy the probe into base and head (untracked), run it alone per tree, quarantine by rename, print the row table."""
import sys, os, shutil, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013')
from drafterlib import *
P('drafter_probe start', ts())
for tree in ('base', 'head'):
    dst = T[tree] + '/Blockchain/Dev/services/auth/src/__tests__/qa1013-drafter-probe.test.ts'
    shutil.copyfile(GS + '/qa1013-drafter-probe.test.ts', dst)
    rows = GS + '/probe_rows_%s.json' % tree
    env = dict(os.environ); env.pop('NODE_ENV', None); env['QA1013_ROWS'] = rows
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', 'src/__tests__/qa1013-drafter-probe.test.ts'], cwd=T[tree] + '/Blockchain/Dev/services/auth', env=env, capture_output=True, text=True)
    os.rename(dst, os.path.dirname(T[tree]) + '/QUARANTINE_%s_qa1013-drafter-probe.test.ts.txt' % tree)
    P(ts(), 'tree', tree, 'vitest rc', p.returncode, (p.stdout + p.stderr)[-1500:] if p.returncode else '')
    if os.path.exists(rows):
        for r in json.load(open(rows)):
            if 'status' in r: P('  %-5s %s %-46s %d RA=%s body=%s hits=%s errlogs=%s uid_body=%s uid_logs=%s stack_logs=%s' % (tree, r['cond'], r['route'], r['status'], r['retryAfter'], r['body'][:110], r['hits'], [e['msg'] for e in r['errorLogs']], r['bodyHasUid'], r['logsHaveUid'], r['logsHaveStack']))
            else: P('  %-5s %s %-30s %s errlogs=%s' % (tree, r['cond'], r['route'], r['outcome'], r['errorLogs']))
    P('porcelain', tree, porcelain(tree))
P('drafter_probe end', ts())
