#!/usr/bin/env python3
"""drafter_tally.py — class tallies over rows_probe_{base,head,merged17}.json: rows, upstream hits, door/undetermined rows sent by a principal WITHOUT
subjects:erase and how many were refused 403/400 with 0 upstream hits, the originate non-door route census (200 + 1 hit), and the W-class rows."""
import json, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1019'
print('drafter_tally', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for t in ('base', 'head', 'merged17'):
    j = json.load(open(G + '/rows_probe_%s.json' % t))
    for st in ('test', 'prod'):
        rows = j[st]
        nd = [r for r in rows if r['cls'] in ('door', 'undetermined') and r['tok'] in ('noscope', 'user', 'noemail_noscope')]
        o = [r for r in rows if r['cls'] == 'originate-route']
        w = [r for r in rows if r['cls'] == 'raw-erasures-canon-not-door' and r['tok'] in ('noscope', 'user')]
        print(t, st, '| rows', len(rows), '| upstream hits', sum(len(r['hits']) for r in rows), '| door/undetermined rows without the scope', len(nd), 'refused 403/400 with 0 hits', sum(1 for r in nd if r['status'] in (400, 403) and not r['hits']),
              '| originate non-door route rows', len(o), '200+1hit', sum(1 for r in o if r['status'] == 200 and len(r['hits']) == 1),
              '| W rows without the scope', len(w), 'forwarded (>=1 hit)', sum(1 for r in w if r['hits']))
