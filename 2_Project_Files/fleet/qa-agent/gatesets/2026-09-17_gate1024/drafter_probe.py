#!/usr/bin/env python3
"""drafter_probe.py — copy src/qa1024-drafter-probe.test.ts into src/qa_probe/ of the head and dev trees IN THE DRAFTER CLONE (never the checkout) and run it alone
(--testMatch on qa_probe, so the default __tests__ suite never collects it); rows to out/rows_probe_<tree>.json; a head-vs-dev table."""
import json, subprocess, datetime, os, shutil, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
srcf = GS + '/src/qa1024-drafter-probe.test.ts'; P('probe sha256', hashlib.sha256(open(srcf, 'rb').read()).hexdigest()[:16], datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
res = {}
for name in ('head', 'dev'):
    o = paths['trees'][name] + '/Blockchain/Dev/services/originate'; bin_ = paths['trees'][name] + '/Blockchain/Dev/node_modules/.bin/'
    d = o + '/src/qa_probe'; os.makedirs(d, exist_ok=True); shutil.copyfile(srcf, d + '/qa1024-drafter-probe.test.ts')
    out = GS + '/out/rows_probe_%s.json' % name
    p = subprocess.run([bin_ + 'jest', '--testMatch', '**/qa_probe/*.test.ts', '--json', '--outputFile', GS + '/out/probe_jest_%s.json' % name], cwd=o, capture_output=True, text=True, env=dict(os.environ, QA1024_ROWS_OUT=out, CI='1'))
    j = json.load(open(GS + '/out/probe_jest_%s.json' % name)); P(name, 'jest rc', p.returncode, 'tests', j['numTotalTests'], 'failed', j['numFailedTests'])
    if j['numFailedTests']: P(p.stderr[-2500:])
    res[name] = {(r['principal'], r['id']): r for r in json.load(open(out))}
keys = list(res['head'].keys())
for k in keys:
    h = res['head'][k]; dv = res['dev'].get(k, {})
    f = lambda r: '%s %s saved=%s stored=%s/%s served=%s list=%s' % (r.get('status'), r.get('code'), r.get('saved', r.get('derivedSaved')), r.get('storedType'), r.get('storedDataType'), r.get('servedType'), r.get('listType'))
    P('%-13s %-62s | dev %-90s | head %-90s | predicted head: %s' % (k[0], k[1][:62], f(dv), f(h), h.get('predicted')))
P('end', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
