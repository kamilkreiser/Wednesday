#!/usr/bin/env python3
"""drafter_suites.py — originate whole jest suite (json) + project tsc -p rc on head and dev in the drafter clone; cwd inside the clone only."""
import json, subprocess, datetime, os
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
for name in ('head', 'dev'):
    o = paths['trees'][name] + '/Blockchain/Dev/services/originate'; bin_ = paths['trees'][name] + '/Blockchain/Dev/node_modules/.bin/'
    t0 = datetime.datetime.now().astimezone().strftime('%H:%M:%S')
    out = GS + '/out/suite_%s.json' % name
    p = subprocess.run([bin_ + 'jest', '--json', '--outputFile', out, '--silent'], cwd=o, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    try:
        j = json.load(open(out)); P(name, t0, 'jest rc', p.returncode, 'suites', j['numTotalTestSuites'], 'failedSuites', j['numFailedTestSuites'], 'tests', j['numTotalTests'], 'failed', j['numFailedTests'], 'pending', j['numPendingTests'], 'passed', j['numPassedTests'])
        for s in j['testResults']:
            if s['status'] != 'passed': P('   non-passed suite', s['name'].split('/src/')[-1], s['status'], (s.get('message') or '')[:300])
    except Exception as e:
        P(name, 'jest rc', p.returncode, 'json unreadable', type(e).__name__, p.stderr[-1500:])
    p = subprocess.run([bin_ + 'tsc', '--noEmit', '-p', '.'], cwd=o, capture_output=True, text=True); P(name, 'tsc --noEmit -p . rc', p.returncode, (p.stdout + p.stderr).strip()[-400:])
P('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
