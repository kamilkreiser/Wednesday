#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear reads for the #1018 (KS-1050) TIER 2 ROUND 1 drafter set. LINEAR_API_KEY by NAME from the Secuura .env; never printed.
Queries only. Raw JSON under linear/. KS-1050 (state, attachments linkKind, relations, comments whole to linear/KS-1202.comments.md) and attachmentsForURL
pull/1018 + controls pull/1021 (KS-1211 contributes) and pull/99999 (0)."""
import json, re, sys, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'; print('LINEAR_API_KEY: set')
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority archivedAt completedAt updatedAt branchName description relations{nodes{type relatedIssue{identifier}}} attachments{nodes{url title metadata createdAt updatedAt}} comments(first:100){nodes{id createdAt body user{name} botActor{name}}} } }'''
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?)\b[:\s]+(?:KS-[0-9]+|#[0-9]+)')
assert [len(CLOSE.findall(x)) for x in ('Fixes KS-1050', 'Refs KS-1050')] == [1, 0]
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in sys.argv[1].split(','):
    d = gql(Q, {'id': n})
    if 'errors' in d: print(n, 'ERRORS', d['errors']); continue
    i = d['data']['issue']; json.dump(i, open(f'{G}/out/linear/{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    print(f"{n}: state={i['state']['name']}/{i['state']['type']} prio={i['priority']} comments={len(cs)} branch={i['branchName']!r} relations={[r['type']+':'+r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} title={i['title'][:120]!r}")
    for a in i['attachments']['nodes']:
        md = a.get('metadata') or {}; print(f"   attachment {a['url']} linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']}")
    with open(f'{G}/out/linear/{n}.comments.md', 'w', encoding='utf-8') as fh:
        fh.write('# DESCRIPTION\n' + (i.get('description') or '') + '\n')
        for c in cs:
            who = (c.get('user') or {}).get('name') or (c.get('botActor') or {}).get('name')
            fh.write(f"\n\n# COMMENT {c['id']} {c['createdAt']} {who}\n{c['body']}\n")
            print(f"   comment {c['id'][:8]} {c['createdAt']} {who} chars={len(c['body'])} at_signs={c['body'].count('@')} closing={CLOSE.findall(c['body'])} first={c['body'][:90]!r}")
AQ = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }'''
for u in ['https://github.com/Secuura/Distributed_Secuura/pull/1018', 'https://github.com/Secuura/Distributed_Secuura/pull/1021', 'https://github.com/Secuura/Distributed_Secuura/pull/99999']:
    d = gql(AQ, {'u': u}); ns = d['data']['attachmentsForURL']['nodes']; print(f"attachmentsForURL {u.rsplit('/',1)[1]}: {len(ns)}")
    for a in ns:
        md = a.get('metadata') or {}; print(f"   on {a['issue']['identifier']} [{a['issue']['state']['name']}] linkKind={md.get('linkKind')!r} created={a['createdAt']}")
