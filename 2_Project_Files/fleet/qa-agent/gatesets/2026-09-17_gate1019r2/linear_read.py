#!/usr/bin/env python3
"""linear_read.py GS IDS — READ-ONLY Linear reads for the #1019 (KS-1187) ROUND 2 set (derived from the round-1 set's linear_read.py). Key by NAME (LINEAR_API_KEY);
never printed. Queries only. Raw JSON under linear/. Issues (state, branchName, attachments with metadata.linkKind, comments with anchor counts),
attachmentsForURL on pull/1019 + controls pull/1017 (KS-1195 contributes) and pull/99999 (0). Comment anchors: pull/1019, the head sha, In Progress, 5f,
edge AND unmeasured, spellings (percent escapes / scheme:// / ;param= / dot segments; regex controls), at-signs."""
import json, re, sys, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G = sys.argv[1]; IDS = sys.argv[2].split(',')
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'; print('LINEAR_API_KEY: set')
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority assignee{name} archivedAt completedAt updatedAt branchName relations{nodes{type relatedIssue{identifier}}} attachments{nodes{url title metadata createdAt updatedAt}} comments(first:50){nodes{id createdAt body}} } }'''
SPELL = re.compile(r'(?i)%[0-9a-f]{2}|(?<![a-z])(?:http|https|ftp)://(?!linear\.app|github\.com)|;[a-z0-9_]+=|/\./|/\.\./|//erasures')
sc = {x: len(SPELL.findall(x)) for x in ('/%65rasures', 'http://h/erasures', 'https://github.com/Secuura/x/pull/1019', '/erasures;x=1', 'plain words')}
print('spelling regex controls', sc); assert sc == {'/%65rasures': 1, 'http://h/erasures': 1, 'https://github.com/Secuura/x/pull/1019': 0, '/erasures;x=1': 1, 'plain words': 0}
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in IDS:
    d = gql(Q, {'id': n})
    if 'errors' in d: print(n, 'ERRORS', d['errors']); continue
    i = d['data']['issue']; json.dump(i, open(f'{G}/linear/{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    print(f"{n}: state={i['state']['name']}/{i['state']['type']} prio={i['priority']} archived={i['archivedAt']} completed={i['completedAt']} comments={len(cs)} branch={i['branchName']!r} relations={[r['type']+':'+r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} title={i['title'][:110]!r}")
    for a in i['attachments']['nodes']:
        md = a.get('metadata') or {}; print(f"   attachment {a['url']} linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']} updated={a['updatedAt']}")
    for c in cs:
        b = c['body']
        anchors = {'pull/1019': 'pull/1019' in b or '#1019' in b, '8b8996f8b': '8b8996f8b' in b, '82f09c8bd': '82f09c8bd' in b, 'fix is #1019': 'the fix is #1019' in b, 'In Progress': 'In Progress' in b, '5f': '5f' in b,
                   'edge&unmeasured': bool(re.search(r'(?i)edge', b) and re.search(r'(?i)unmeasured', b)), 'spellings': SPELL.findall(b), 'at_signs': b.count('@')}
        print(f"   comment {c['id']} {c['createdAt']} chars={len(b)} anchors={anchors}")
AQ = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt updatedAt issue{ identifier state{name} } } } }'''
for u in ['https://github.com/Secuura/Distributed_Secuura/pull/1019', 'https://github.com/Secuura/Distributed_Secuura/pull/1017', 'https://github.com/Secuura/Distributed_Secuura/pull/99999']:
    d = gql(AQ, {'u': u})
    if 'errors' in d: print('attachmentsForURL', u, 'ERRORS', d['errors']); continue
    ns = d['data']['attachmentsForURL']['nodes']; print(f"attachmentsForURL {u.rsplit('/',1)[1]}: {len(ns)}")
    for a in ns:
        md = a.get('metadata') or {}; print(f"   on {a['issue']['identifier']} [{a['issue']['state']['name']}] linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']} updated={a['updatedAt']}")
