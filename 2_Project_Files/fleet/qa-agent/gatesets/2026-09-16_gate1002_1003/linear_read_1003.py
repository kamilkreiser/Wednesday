#!/usr/bin/env python3
"""READ-ONLY Linear GraphQL (queries only) for the #1002+#1003 gate: KS-1165 and KS-1177 (description, state, comments,
attachments WITH metadata.linkKind, relations, history), and attachmentsForURL on pull/1002 AND pull/1003 so a link on
ANY ticket is seen. Keys read by NAME; never printed or written. No mutations. Usage: linear_read_1003.py <dir>"""
import json, sys, os, urllib.request, re, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
os.makedirs(f'{G}/linear', exist_ok=True)
vals = {}
for line in open(ENV, encoding='utf-8'):
    for k in ('GH_TOKEN', 'LINEAR_API_KEY'):
        if line.startswith(k + '='):
            vals[k] = line.split('=', 1)[1].strip().strip('"').strip("'")
assert vals.get('GH_TOKEN') and vals.get('LINEAR_API_KEY'), 'key(s) not found by name'


def now():
    return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')


print('read at', now())
for n in (1002, 1003):
    r = urllib.request.urlopen(urllib.request.Request(f'https://api.github.com/repos/Secuura/Distributed_Secuura/issues/{n}/comments', headers={'Authorization': 'Bearer ' + vals['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60)
    for c in json.load(r):
        sums = re.findall(r'<summary><a href="https://linear.app/secuura/issue/(KS-[0-9]+)/', c['body'] or '')
        print(f'PR #{n} comment by {c["user"]["login"]} {c["created_at"]}: linkback summaries={sums}')


def gql(q, v):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60)
    j = json.load(r)
    assert 'errors' not in j, j.get('errors')
    return j['data']


Q = '''query($id:String!){ issue(id:$id){
  identifier title state{name type} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  attachments(first:30){nodes{url title sourceType metadata createdAt}}
  relations(first:30){nodes{type relatedIssue{identifier title state{name}}}}
  inverseRelations(first:30){nodes{type issue{identifier title state{name}}}}
  comments(first:80){nodes{id createdAt user{name} body}}
  history(first:80){nodes{createdAt actor{name} fromState{name} toState{name} attachment{url}}} }}'''
for ident in ('KS-1165', 'KS-1177'):
    try:
        i = gql(Q, {'id': ident})['issue']
    except Exception as e:
        print(f'\n{ident}: query failed {type(e).__name__} {str(e)[:160]}')
        continue
    tag = ident.replace('-', '').lower()
    json.dump(i, open(f'{G}/linear/{tag}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    open(f'{G}/linear/{tag}_description.md', 'w', encoding='utf-8').write(i['description'] or '')
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    for c in cs:
        open(f"{G}/linear/{tag}_comment_{c['createdAt'][:19].replace(':', '')}_{c['id'][:8]}.md", 'w', encoding='utf-8').write(c['body'] or '')
    print(f"\n{i['identifier']} [{i['state']['name']}/{i['state']['type']}] {i['priorityLabel']} archived={i['archivedAt']} created={i['createdAt']} updated={i['updatedAt']} desc={len(i['description'] or '')}c comments={len(cs)}")
    print('   title:', i['title'])
    for a in i['attachments']['nodes']:
        md = a.get('metadata') or {}
        print(f"   attachment {a['url']} sourceType={a.get('sourceType')} linkKind={md.get('linkKind')!r} status={md.get('status')!r} created={a['createdAt']}")
    print('   relations:', [(x['type'], x['relatedIssue']['identifier'], x['relatedIssue']['state']['name']) for x in i['relations']['nodes']])
    print('   inverse:', [(x['type'], x['issue']['identifier'], x['issue']['state']['name']) for x in i['inverseRelations']['nodes']])
    for c in cs:
        print(f"   comment {c['id'][:8]} {c['createdAt']} {c['user']['name'] if c['user'] else 'bot/integration'} chars={len(c['body'] or '')}")
    for h in sorted(i['history']['nodes'], key=lambda h: h['createdAt']):
        if h['fromState'] or h['toState'] or h['attachment']:
            print(f"   history {h['createdAt']} actor={h['actor']['name'] if h['actor'] else 'integration/none'} {h['fromState']['name'] if h['fromState'] else ''} -> {h['toState']['name'] if h['toState'] else ''} attachment={h['attachment']['url'] if h['attachment'] else ''}")

QA = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url sourceType metadata createdAt issue{identifier title state{name}} } } }'''
for n in (1002, 1003):
    u = f'https://github.com/Secuura/Distributed_Secuura/pull/{n}'
    ns = gql(QA, {'u': u})['attachmentsForURL']['nodes']
    print(f"\nattachmentsForURL pull/{n}: {len(ns)}")
    for a in ns:
        md = a.get('metadata') or {}
        print(f"   on {a['issue']['identifier']} [{a['issue']['state']['name']}] linkKind={md.get('linkKind')!r} created={a['createdAt']}")
print('done at', now())
