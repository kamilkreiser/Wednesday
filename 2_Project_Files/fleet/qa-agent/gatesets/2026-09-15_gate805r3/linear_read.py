#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear reads for the #805 set (KS-726, KS-705, KS-774, KS-1004, KS-535, KS-679, KS-741). Key by NAME (LINEAR_API_KEY); never printed."""
import json, sys, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G = sys.argv[1]; IDS = sys.argv[2].split(',')
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'; print('LINEAR_API_KEY: set')
def gql(q, v):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    return json.load(r)
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name} priority assignee{name} archivedAt updatedAt branchName description relations{nodes{type relatedIssue{identifier}}} comments(first:50){nodes{id createdAt body}} } }'''
print('read at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
for n in IDS:
    i = gql(Q, {'id': n})['data']['issue']; json.dump(i, open(f'{G}/linear/{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    ats = sum(c['body'].count('@') for c in cs)
    print(f"{n}: state={i['state']['name']} prio={i['priority']} assignee={(i['assignee'] or {}).get('name')} archived={i['archivedAt']} updated={i['updatedAt']} comments={len(cs)} last={cs[-1]['id'][:8] if cs else '-'}@{cs[-1]['createdAt'] if cs else '-'} at_signs_in_comments={ats} desc_chars={len(i['description'] or '')} relations={[r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} title={i['title'][:100]!r}")
