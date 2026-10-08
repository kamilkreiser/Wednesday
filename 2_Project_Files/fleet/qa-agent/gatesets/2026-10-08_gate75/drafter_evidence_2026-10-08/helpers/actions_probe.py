import sys, json
sys.path.insert(0, sys.argv[1]); from ghget import get
def runs(sha):
    r = get('actions/runs?head_sha=%s&per_page=100' % sha); return r.get('workflow_runs', [])
out = {}
for name, sha in (('head', sys.argv[2]), ('develop', sys.argv[3]), ('FABRICATED-CONTROL', '0123456789abcdef0123456789abcdef01234567')):
    rs = runs(sha); out[name] = []
    print('==', name, sha[:12], 'runs', len(rs))
    for w in sorted(rs, key=lambda w: (w['name'], w['run_attempt'])):
        jobs = get('actions/runs/%d/jobs?per_page=100' % w['id']).get('jobs', [])
        fails = sorted(j['name'] for j in jobs if j['conclusion'] not in ('success', 'skipped', 'neutral'))
        print('  %-34s ev=%-12s status=%-10s concl=%-9s jobs=%d failing=%s created=%s' % (w['name'], w['event'], w['status'], w['conclusion'], len(jobs), fails, w['created_at']))
        for j in jobs:
            if j['conclusion'] not in ('success','skipped','neutral'):
                fs = [s['name'] for s in j.get('steps', []) if s.get('conclusion') == 'failure']
                print('      job %s concl=%s failed steps=%s id=%d' % (j['name'], j['conclusion'], fs, j['id']))
        out[name].append({'wf': w['name'], 'event': w['event'], 'status': w['status'], 'conclusion': w['conclusion'], 'failing': fails, 'id': w['id']})
json.dump(out, open(sys.argv[4], 'w'), indent=1)
