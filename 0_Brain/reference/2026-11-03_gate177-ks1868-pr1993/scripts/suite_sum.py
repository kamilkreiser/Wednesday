import sys
K = sys.argv[1]
import json, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/results/'
fails = {}
for t in [f'{K}_base', f'{K}_head']:
    d = json.load(open(W + f'suite_{t}.json'))
    files = d['testResults']; nload = [f for f in files if not f['assertionResults']]
    print(t, 'files', len(files), 'tests', d['numTotalTests'], 'passed', d['numPassedTests'], 'failed', d['numFailedTests'], 'skipped/pending', d['numPendingTests'] + d.get('numTodoTests', 0), 'files with 0 tests (load failures)', len(nload))
    fails[t] = set()
    for f in files:
        for a in f['assertionResults']:
            if a['status'] == 'failed':
                fails[t].add((f['name'].split('/Blockchain/Dev/')[-1], a['fullName'][:90], 'timeout' if any('timed out' in m for m in a['failureMessages']) else 'assert/other'))
    for f in nload: fails[t].add((f['name'].split('/Blockchain/Dev/')[-1], '<file failed to load>', (f.get('message') or '')[:80].replace('\n', ' ')))
for t in [f'{K}_base', f'{K}_head']:
    print('--', t, 'failures', len(fails[t]))
    for x in sorted(fails[t]): print('  ', *x)
print('only base:', sorted(fails[f'{K}_base'] - fails[f'{K}_head']))
print('only head:', sorted(fails[f'{K}_head'] - fails[f'{K}_base']))
