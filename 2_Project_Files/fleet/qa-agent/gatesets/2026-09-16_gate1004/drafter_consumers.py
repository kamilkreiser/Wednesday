#!/usr/bin/env python3
"""drafter_consumers.py — consumer suites at head in the scratch clone, @secuura/shared resolved to the CLONE's dist built at head
(asserted before each run: realpath inside the clone AND the dist contains Promise.race). m365-integration (vitest) and originate (jest)."""
import json, os, subprocess, datetime
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-16_gate1004'
P = json.load(open(SCR + '/gate1004_draft_paths.json')); C = P['C']; W = P['W']; DEV = C + '/Blockchain/Dev'
now = lambda: datetime.datetime.now().astimezone().strftime('%H:%M:%S')
for svc, cmd in (('m365-integration', ['npx', 'vitest', 'run', '--reporter=json', '--outputFile=' + W + '/vt_m365.json']),
                 ('originate', ['npx', 'jest', '--json', '--outputFile=' + W + '/jest_originate.json'])):
    cwd = DEV + '/services/' + svc
    rp = subprocess.run(['node', '-e', "const f=require('fs');const p=f.realpathSync(require.resolve('@secuura/shared',{paths:[process.cwd()]}));console.log(p, f.readFileSync(p.replace(/index\\.js$/,'security/ssrf-guard.js'),'utf8').includes('Promise.race'))"], cwd=cwd, capture_output=True, text=True).stdout.strip()
    print(now(), svc, 'resolves @secuura/shared ->', rp, '| inside clone', rp.startswith(C))
    assert rp.startswith(C) and rp.endswith('true'), 'consumer would not load the head dist'
    t = datetime.datetime.now(); p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1500)
    print(now(), svc, 'rc', p.returncode, '%.0fs' % (datetime.datetime.now() - t).total_seconds())
    out = W + ('/vt_m365.json' if svc.startswith('m365') else '/jest_originate.json')
    if os.path.exists(out):
        j = json.load(open(out)); print('   suites total %s passed %s failed %s | tests total %s passed %s failed %s' % (j.get('numTotalTestSuites'), j.get('numPassedTestSuites'), j.get('numFailedTestSuites'), j['numTotalTests'], j['numPassedTests'], j['numFailedTests']))
        for tr in j['testResults']:
            bad = [a['title'] for a in tr['assertionResults'] if a['status'] == 'failed']
            if bad or tr.get('status') == 'failed': print('   FAILED file', tr['name'].replace(C, '<clone>'), bad[:5], (tr.get('message') or '')[:300].replace('\n', ' '))
    else: print('   NO JSON', p.stderr[-800:])
