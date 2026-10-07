import json, os, sys, urllib.request
T = None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if l.startswith('GH_TOKEN='): T = l.split('=',1)[1].strip().strip('"').strip("'")
def get(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + p, headers={'Authorization': 'Bearer ' + T})
    return json.load(urllib.request.urlopen(r, timeout=60))
for sha in sys.argv[1:]:
    runs = get('actions/runs?head_sha=%s&per_page=100' % sha)['workflow_runs']
    print('==', sha[:12], len(runs), 'runs')
    for r in runs:
        if r['conclusion'] != 'failure': continue
        js = get('actions/runs/%s/jobs?per_page=100' % r['id'])['jobs']
        f = sorted(j['name'] for j in js if j['conclusion'] == 'failure')
        steps = {j['name']: [s['name'] for s in j.get('steps', []) if s.get('conclusion') == 'failure'] for j in js if j['conclusion'] == 'failure'}
        print('  ', r['name'], f, steps if r['name'] == 'Security Scanning' else '')
