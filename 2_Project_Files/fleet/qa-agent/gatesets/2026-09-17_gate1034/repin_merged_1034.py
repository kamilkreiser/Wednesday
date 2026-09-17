#!/usr/bin/env python3
"""repin_merged_1034.py — the MERGED tree e4624218b x develop 34cdcfb26 (#1035 landed during the re-pin): commit-tree + worktree IN THE CLONE, per-ENTRY
farm (repin_farm_1034.py logic), whole api-gateway vitest 4.1.11 at default and 60 s, project tsc, and the new develop's own suite for the denominator.
Never rm, never cd."""
import json, os, subprocess, sys, datetime, importlib.util
GS = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GS + '/repin_paths.json')); C = PA['C']; W = PA['W']
H = PA['sha']['head']; N = '34cdcfb2663b9e4c31025044e6f842ad2c5a10a3'; MT = 'f1c78bbb888f5c0f875a7ab11ee09d810126f72a'
def run(c, cwd=None, env=None): p = subprocess.run(c, capture_output=True, text=True, cwd=cwd, env=env); return p.returncode, p.stdout.strip(), p.stderr.strip()
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
rc, t, e = run(['git', '-C', C, 'merge-tree', '--write-tree', H, N]); assert rc == 0 and t.split('\n')[0] == MT, (rc, t, e)
env = dict(os.environ, GIT_AUTHOR_NAME='qa1034r', GIT_AUTHOR_EMAIL='qa1034r@invalid', GIT_COMMITTER_NAME='qa1034r', GIT_COMMITTER_EMAIL='qa1034r@invalid', GIT_AUTHOR_DATE='2026-09-18T02:00:00+10:00', GIT_COMMITTER_DATE='2026-09-18T02:00:00+10:00')
rc, mc, e = run(['git', '-C', C, 'commit-tree', MT, '-p', H, '-p', N, '-m', 'qa1034r merged probe (never pushed)'], env=env); assert rc == 0, e
print('merged commit (clone only)', mc, 'tree', MT)
trees = {}
for name, sha in (('merged', mc), ('newdev', N)):
    wt = W + '/wt_' + name; rc, o, e = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, sha]); assert rc == 0, e; trees[name] = wt
PA['trees'].update(trees); PA['sha']['merged'] = mc; PA['sha']['newdev'] = N; json.dump(PA, open(GS + '/repin_paths.json', 'w'), indent=1)
p = subprocess.run(['python3', GS + '/repin_farm_1034.py', 'merged', 'newdev'], capture_output=True, text=True); print(p.stdout[-3000:], p.stderr[-500:])
DEV = 'Blockchain/Dev'; GW = DEV + '/services/api-gateway'
for name in ('newdev', 'merged'):
    tree = trees[name]
    for tag, extra in (('default', []), ('t60', ['--testTimeout=60000', '--hookTimeout=60000'])):
        out = GS + '/out_repin/suites/suite_%s_%s.json' % (name, tag); l0 = '%.1f' % os.getloadavg()[0]; t0 = now()
        e2 = dict(os.environ, CI='1'); e2.pop('NODE_ENV', None)
        with open(out.replace('.json', '.stderr'), 'w') as fe:
            pr = subprocess.run(['node', tree + '/' + DEV + '/node_modules/vitest/vitest.mjs', 'run', '--reporter=json', '--outputFile=' + out] + extra, cwd=tree + '/' + GW, stdout=subprocess.PIPE, stderr=fe, text=True, env=e2)
        j = json.load(open(out)); fails = [(s['name'].split('/')[-1], a['title'][:60]) for s in j['testResults'] for a in s['assertionResults'] if a['status'] == 'failed']
        ks = {k: sum(1 for s in j['testResults'] if k in s['name'] for a in s['assertionResults'] if a['status'] == 'passed') for k in ('ks1215', 'ks1204')}
        print('SUITE', name, tag, t0, '->', now(), 'load', l0, '| rc', pr.returncode, 'files', len(j['testResults']), 'tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'], 'pending', j['numPendingTests'], '| passed ks1215 / ks1204 cells', ks, '| fails', fails[:5])
    rc, o, e = run([tree + '/' + DEV + '/node_modules/typescript/bin/tsc', '--noEmit', '-p', '.'], cwd=tree + '/' + GW); print('PROJECT tsc', name, 'rc', rc, (o + e)[-200:])
    print('porcelain', name, len(run(['git', '-C', tree, 'status', '--porcelain', '--untracked-files=no'])[1].splitlines()))
