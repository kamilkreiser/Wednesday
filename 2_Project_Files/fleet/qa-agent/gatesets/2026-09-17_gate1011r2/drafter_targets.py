#!/usr/bin/env python3
"""drafter_targets.py — #1011 ROUND 2 drafter SAMPLE: (a) whole api-gateway suite on base 1125607e9 and merged (head + no-ff 79432c797);
(b) request-target forms that might still steer action/resource_type, through the ROUND-1 GATE's census instrument (qa1011-census.test.ts, copied
unchanged from its evidence/), on base and head, NODE_ENV test and production (same env stubs as its census_run.py). PREDICTIONS. Never rm."""
import sys, os, json, re, glob, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafterlib import *
GWR = 'Blockchain/Dev/services/api-gateway'
P('drafter_targets start', ts())
for t in ('base', 'merged'): vitest('suite_' + t, t, 'gw')
R = []
def add(label, method, target, **kw): R.append(dict(i=len(R), label=label, method=method, target=target, **kw))
add('CONTROL POST /api/logs', 'POST', '/api/logs')
for tgt in ('/api/LOGS', '/API/logs', '/api/%6cogs', '/api/logs%2f', '/api/v1//logs', '/API/V1/logs', '/api/V1/logs', '/api/v1/v1/logs', '/api/x/../logs', '/api/./logs',
            '/api/logs;x=1', '/api/logs?next=/api/v1/qa', 'http://h/api/v1/logs', 'HTTP://h/api/logs', '/api/qa-attacker-chosen/x', '/api/v1'):
    add('T ' + tgt, 'POST', tgt)
ENF = {'SUBJECTS_ERASE_SCOPE_ENFORCED': 'true'}
for tgt in ('/api/gdpr/erasures', '/api/GDPR/erasures', '/api/gdpr/%65rasures', '/api/v1/GDPR/erasures', 'http://h/api/v1/gdpr/erasures', '/api/gdpr/erasures/.', '/api/gdpr/x/../erasures'):
    add('G ' + tgt, 'POST', tgt, auth='conn', env=ENF)
add('G connscope admitted /api/gdpr/erasures', 'POST', '/api/gdpr/erasures', auth='connscope', env=ENF)
reqf = GS + '/targets_requests.json'; json.dump(R, open(reqf, 'w'), indent=0)
svc = sorted(set(re.findall(r'process\.env\.([A-Z0-9_]+_SERVICE_URL)\b', ''.join(open(f).read() for f in glob.glob(T['head'] + '/' + GWR + '/src/**/*.ts', recursive=True) if '__tests__' not in f)))) + ['TENANT_PROVISIONING_URL']
os.makedirs(W + '/_quarantine', exist_ok=True)
for nodeenv in ('test', 'production'):
    for t in ('base', 'head'):
        dst = T[t] + '/' + GWR + '/src/__tests__/qa1011-census.test.ts'
        open(dst, 'w').write(open(GS + '/qa1011-census.r1gate-copy.test.ts').read())
        env = dict(os.environ); env.pop('NODE_ENV', None)
        for k in ('ENABLE_TEST_TOKENS', 'ENABLE_MOCK_ENDPOINTS', 'DATABASE_URL', 'REDIS_URL'): env.pop(k, None)
        if nodeenv == 'production': env.update(NODE_ENV='production', CSRF_SECRET='qa1011r2-drafter-stub-not-a-secret', DATABASE_URL='postgres://qa:qa@127.0.0.1:1/qa', REDIS_URL='redis://127.0.0.1:1')
        out = GS + '/targets_%s_%s.json' % (nodeenv, t)
        env.update(QA1011_REQ=reqf, QA1011_OUT=out, QA1011_SVC_ENVS=','.join(svc), RATE_LIMIT_MAX_REQUESTS='100000', VERIFICATION_RATE_LIMIT_MAX='100000', LOGIN_RATE_LIMIT='4')
        p = subprocess.run([T[t] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', 'src/__tests__/qa1011-census.test.ts'], cwd=T[t] + '/' + GWR, env=env, capture_output=True, text=True)
        os.rename(dst, W + '/_quarantine/qa1011-census.%s.%s.%d.test.ts' % (nodeenv, t, len(os.listdir(W + '/_quarantine'))))
        o = json.load(open(out)); P(ts(), nodeenv, t, 'vitest rc', p.returncode, 'meta', o['meta'])
    ob = json.load(open(GS + '/targets_%s_base.json' % nodeenv)); oh = json.load(open(GS + '/targets_%s_head.json' % nodeenv))
    def by(o):
        d = collections.defaultdict(list)
        for a in o['inserts']: d[a['ua'].split('~')[0]].append((a['action'], a['resourceType'], a['details'].get('path') if isinstance(a['details'], dict) else None))
        return d
    bb, bh = by(ob), by(oh)
    P('== %s ==' % nodeenv)
    for rb, rh in zip(ob['results'], oh['results']):
        P('  %-44s hops %-12s | base %s | head %s | up %s' % (rb['label'][:44], [h['status'] for h in rh['hops']], bb[rb['ua']], bh[rh['ua']], sum(1 for u in oh['upSeen'] if u['ua'].split('~')[0] == rh['ua'])))
P('drafter_targets end', ts())
