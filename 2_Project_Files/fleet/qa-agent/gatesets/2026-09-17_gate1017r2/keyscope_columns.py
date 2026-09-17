#!/usr/bin/env python3
"""keyscope_columns.py — the round-1 gate's cross-tenant keyscope stage (its harness VERBATIM, sha fd4026582f12) as four columns: base 7e89318bc / r1 cbe29597d /
head a067d4e3e / merged (head x develop fa887f382), from rows/<tree>.json; plus the ROUND-1 GATE's own rows (its evidence/rows/head.json = r1, merged.json) as
an external control column: my r1 column must equal the gate's r1 rows, or my instrument is not the gate's."""
import json, subprocess
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017r2'
EV = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/evidence/rows'
print('keyscope_columns', subprocess.run(['date', '+%Y-%m-%d %H:%M:%S %Z'], capture_output=True, text=True).stdout.strip())
cols = {t: json.load(open(GS + '/rows/%s.json' % t)) for t in ('base', 'r1', 'head', 'merged')}
g = {'gate_r1': json.load(open(EV + '/head.json')), 'gate_r1_merged': json.load(open(EV + '/merged.json'))}
labels = [x['label'] for x in cols['head']['keyscope']]
for lab in labels:
    print('==', lab)
    per = {t: next(x for x in c['keyscope'] if x['label'] == lab)['steps'] for t, c in {**cols, **g}.items() if any(x['label'] == lab for x in c['keyscope'])}
    n = max(len(v) for v in per.values())
    for i in range(n):
        print('   step', i, ' | '.join('%s %s' % (t, per[t][i] if i < len(per[t]) else '-') for t in per))
print('-- instrument control: my r1 keyscope == round-1 gate r1 keyscope:', json.dumps(cols['r1']['keyscope'], sort_keys=True) == json.dumps(g['gate_r1']['keyscope'], sort_keys=True))
print('-- my r1 census rows == round-1 gate r1 census rows (verb,url,K statuses+remaining, D remaining):',
      sorted((r['verb'], r['url'], tuple(x[0] for x in r['K']), tuple(x[3] for x in r['K']), r['D'][3]) for r in cols['r1']['census']) == sorted((r['verb'], r['url'], tuple(x[0] for x in r['K']), tuple(x[3] for x in r['K']), r['D'][3]) for r in g['gate_r1']['census']))
print('-- head == merged keyscope:', json.dumps(cols['head']['keyscope'], sort_keys=True) == json.dumps(cols['merged']['keyscope'], sort_keys=True))
for t in cols:
    C = cols[t]['census']; f = [r for r in C if r['K'][0][2] is not None]
    print('census', t, 'routes', len(C), 'fires', len(f), 'D999', sum(1 for r in C if r['D'][3] == '999'), 'D998', sum(1 for r in C if r['D'][3] == '998'),
          'non-machine P with header', sum(1 for r in C for v in r['P'].values() if v[1] is not None), 'N/I/M header', sum(1 for r in C if r['N'][1] or r['I'][1] or r['M'][1]))
