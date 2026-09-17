#!/usr/bin/env python3
"""drafter_table_1032r2.py <tag> — one line per row x tree x NODE_ENV from out/rows_<tag>_<tree>_<env>.json; asserts test == production per tree
(status, code, message, row, level, seq, error/warn line messages+keys) and prints the differences, if any."""
import json, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1032r2'
TAG = sys.argv[1]
def load(t, e): return {r['id']: r for r in json.load(open('%s/out/rows_%s_%s_%s.json' % (GS, TAG, t, e)))['rows']}
D = {(t, e): load(t, e) for t in ('head', 'r1', 'dev') for e in ('test', 'production')}
def key(r):
    if r.get('kind') == 'follow-up': return json.dumps([r['first'], r['steps']], sort_keys=True)
    return json.dumps([r['status'], r['code'], r['message'], r['dataStatus'], r['requestRow'], r['level'], r['seq'], [(l['msg'], l['keys']) for l in r['errorLines']], [(l['msg'], l['keys']) for l in r['warnLines']]], sort_keys=True)
for t in ('head', 'r1', 'dev'):
    diff = [rid for rid in D[(t, 'test')] if key(D[(t, 'test')][rid]) != key(D[(t, 'production')].get(rid, {'kind': 'follow-up', 'first': None, 'steps': None}))]
    print('NODE_ENV test == production on %s: %d / %d rows equal; differing: %s' % (t, len(D[(t, 'test')]) - len(diff), len(D[(t, 'test')]), diff))
def short(r):
    if r.get('kind') == 'follow-up':
        f = r['first']; s = '; '.join('%s -> %s' % (x['step'], ' '.join(str(x.get(k)) for k in ('status', 'message', 'dataStatus', 'currentLevel', 'requests') if x.get(k) not in (None, ''))) + (' row=%s level=%s' % ((x.get('requestRow') or {}).get('status'), x.get('level')) if 'requestRow' in x else '') for x in r['steps'])
        return 'first %s row=%s level=%s | %s' % (f['status'], (f['requestRow'] or {}).get('status'), f['level'], s)
    rq = r['requestRow'] or {}
    msg = {'Authentication service temporarily unavailable, please retry': 'generic-503', 'Verification approved': 'approved'}.get(r['message'], r['message'][:48])
    el = ['E:' + l['msg'].split(': ', 1)[-1][:60] + '{' + ','.join(k for k in l['keys'] if k in ('requestId', 'userId', 'targetLevel', 'levelNow', 'readError')) + '}' for l in r['errorLines']]
    wl = ['W:' + l['msg'].split(': ', 1)[-1][:60] for l in r['warnLines'] if 'Verification approve' in l['msg']]
    return '%s %s | row %s/%s | level %s | %s' % (r['status'], msg, rq.get('status'), rq.get('reviewed_by'), r['level'], el + wl)
for rid in D[('head', 'test')]:
    print('ROW', rid, '| expect:', D[('head', 'test')][rid].get('expect', 'follow-up'))
    for t in ('head', 'r1', 'dev'):
        print('   %-4s %s' % (t, short(D[(t, 'test')][rid])))
