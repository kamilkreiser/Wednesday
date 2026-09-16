#!/usr/bin/env python3
"""drafter_f3.py — F-3: the WHOLE packages/shared suite at head under the fast-RST net redirect (pre-existing exposure vs the PR's)."""
import json, os, shutil, subprocess, datetime
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-16_gate1004'
P = json.load(open(SCR + '/gate1004_draft_paths.json')); C = P['C']; W = P['W']; SH = C + '/Blockchain/Dev/packages/shared'
for f in ('qa-netredirect.setup.ts', 'qa-netredirect.config.ts'): shutil.copyfile(G + '/' + f, SH + '/' + f)
print('scratch __tests__ files present:', [x for x in os.listdir(SH + '/src/__tests__') if x.startswith('qa1004') and not x.endswith('.quarantined')])
for mode in ('rst', 'silent'):
    out = W + '/vt_shared_full_net_' + mode + '.json'; e = dict(os.environ); e['QA1004_NET'] = mode
    p = subprocess.run(['npx', 'vitest', 'run', '--config', 'qa-netredirect.config.ts', '--reporter=json', '--outputFile=' + out], cwd=SH, env=e, capture_output=True, text=True, timeout=600)
    j = json.load(open(out)); shutil.copyfile(out, G + '/vt_shared_full_net_' + mode + '.json')
    print(datetime.datetime.now().astimezone().strftime('%H:%M:%S'), mode, 'rc', p.returncode, 'files', len(j['testResults']), 'tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'])
    for tr in j['testResults']:
        for a in tr['assertionResults']:
            if a['status'] == 'failed': print('   RED', tr['name'].split('/')[-1], '|', a['title'][:80], '|', (a.get('failureMessages') or [''])[0][:140].replace('\n', ' '))
            elif 'ks914-shipped' in tr['name'] or 'ks932' in tr['name']: print('   green', tr['name'].split('/')[-1], round(a.get('duration') or 0), a['title'][:80])
for f in ('qa-netredirect.setup.ts', 'qa-netredirect.config.ts'): os.rename(SH + '/' + f, SH + '/' + f + '.quarantined2')
