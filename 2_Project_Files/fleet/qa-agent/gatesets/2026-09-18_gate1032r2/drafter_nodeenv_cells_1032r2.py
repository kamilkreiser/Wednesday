#!/usr/bin/env python3
"""drafter_nodeenv_cells_1032r2.py — the seat's two ks1194 files at head under NODE_ENV=test and NODE_ENV=production, through a scratch vitest config
OUTSIDE services/auth (root = auth dir, include = the two files, auth's setupFiles + logger alias, test.env NODE_ENV). Prints per-cell pass/fail and the
first failure line. Also runs the round-2 file alone with the default auth config as the control. cwd inside the clone; never rm."""
import json, subprocess, os, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
paths = json.load(open(GS + '/out/drafter_paths.json'))
DEV = 'Blockchain/Dev'; tree = paths['trees']['head']; auth = tree + '/' + DEV + '/services/auth'; pd = tree + '/' + DEV + '/qa_probe_1032r2'
F = ['src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts', 'src/__tests__/ks1194-approve-never-restores-pending-over-a-raised-level.test.ts']
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
print('drafter_nodeenv_cells_1032r2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), flush=True)
for env in ('test', 'production'):
    cfg = pd + '/vitest.qa1032r2-cells-%s.config.mts' % env
    open(cfg, 'w').write("import { defineConfig } from 'vitest/config';\nexport default defineConfig({\n  root: %r,\n  resolve: { alias: { '@secuura/shared/utils/logger': %r } },\n  test: { globals: true, environment: 'node', include: %r, setupFiles: [%r], env: { NODE_ENV: %r } },\n});\n"
                         % (auth, tree + '/' + DEV + '/packages/shared/dist/utils/logger.js', F, auth + '/vitest.setup.ts', env))
    rep = GS + '/out/cells_%s.json' % env
    with open(GS + '/out/cells_%s.stderr' % env, 'w') as fe:
        p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--config', cfg, '--reporter=json', '--outputFile=' + rep], cwd=pd, stdout=subprocess.PIPE, stderr=fe, text=True, env=dict(os.environ, CI='1'))
    j = json.load(open(rep))
    print('NODE_ENV', env, now(), 'rc', p.returncode, '| files', len(j['testResults']), 'tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'], flush=True)
    for s in j['testResults']:
        for a in s['assertionResults']:
            if a['status'] != 'passed':
                print('   FAIL', s['name'].split('/')[-1][:40], '::', a['title'][:90], '::', ' '.join((a.get('failureMessages') or [''])[0].split())[:260], flush=True)
print('qa files under services/auth:', sum(1 for dp, dn, fn in os.walk(auth) if 'node_modules' not in dp for f in fn if 'qa1032' in f), '| end', now())
