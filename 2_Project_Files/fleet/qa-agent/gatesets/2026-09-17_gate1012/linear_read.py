#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear reads for the #1012 set (KS-745). Key by NAME (LINEAR_API_KEY); never printed. Raw JSON under linear/. Reads attachments.metadata.linkKind, plus attachmentsForURL on pull/1012."""
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
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority assignee{name} archivedAt completedAt updatedAt branchName description relations{nodes{type relatedIssue{identifier}}} inverseRelations{nodes{type issue{identifier}}} attachments{nodes{url title metadata createdAt}} comments(first:50){nodes{id createdAt body}} } }'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in IDS:
    d = gql(Q, {'id': n})
    if 'errors' in d: print(n, 'ERRORS', d['errors']); continue
    i = d['data']['issue']; json.dump(i, open(f'{G}/linear/{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    print(f"{n}: state={i['state']['name']}/{i['state']['type']} prio={i['priority']} assignee={(i['assignee'] or {}).get('name')} archived={i['archivedAt']} completed={i['completedAt']} updated={i['updatedAt']} comments={len(cs)} desc_chars={len(i['description'] or '')} relations={[r['type']+':'+r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} inverse={[r['type']+':'+r['issue']['identifier'] for r in i['inverseRelations']['nodes']]} title={i['title']!r}")
    for a in i['attachments']['nodes']:
        md = a.get('metadata') or {}
        print(f"   attachment {a['url']} linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']}")
    for c in cs: print(f"   comment {c['id']} {c['createdAt']} chars={len(c['body'])} at_signs={c['body'].count('@')}")
AQ = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }'''
for u in ['https://github.com/Secuura/Distributed_Secuura/pull/1012']:
    d = gql(AQ, {'u': u})
    if 'errors' in d: print('attachmentsForURL', u, 'ERRORS', d['errors']); continue
    ns = d['data']['attachmentsForURL']['nodes']
    print(f"attachmentsForURL {u.rsplit('/',1)[1]}: {len(ns)}")
    for a in ns:
        md = a.get('metadata') or {}
        print(f"   on {a['issue']['identifier']} [{a['issue']['state']['name']}] linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']}")
