#!/usr/bin/env python3
"""READ-ONLY Linear GraphQL (queries only) for the #1002 gate: KS-1123 and KS-1073 (description, state, comments,
attachments WITH metadata.linkKind, relations, history), plus attachmentsForURL on pull/1002 so a link on ANY ticket
is seen. LINEAR_API_KEY / GH_TOKEN read by NAME; never printed or written. No mutations. Usage: linear_read.py <dir>"""
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
r = urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/issues/1002/comments', headers={'Authorization': 'Bearer ' + vals['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60)
for c in json.load(r):
    sums = re.findall(r'<summary><a href="https://linear.app/secuura/issue/(KS-[0-9]+)/', c['body'] or '')
    print(f'PR #1002 comment by {c["user"]["login"]} {c["created_at"]}: linkback summaries={sums}')


def gql(q, v):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60)
    j = json.load(r)
    assert 'errors' not in j, j.get('errors')
    return j['data']


Q = '''query($id:String!){ issue(id:$id){
  identifier title state{name type} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  parent{identifier title} children(first:30){nodes{identifier title state{name}}}
  labels(first:20){nodes{name}}
  attachments(first:30){nodes{url title subtitle sourceType metadata createdAt}}
  relations(first:30){nodes{type relatedIssue{identifier title state{name}}}}
  inverseRelations(first:30){nodes{type issue{identifier title state{name}}}}
  comments(first:80){nodes{id createdAt user{name} body}}
  history(first:80){nodes{createdAt actor{name} fromState{name} toState{name} attachment{url}}} }}'''
for ident in ('KS-1123', 'KS-1073'):
    i = gql(Q, {'id': ident})['issue']
    tag = ident.replace('-', '').lower()
    json.dump(i, open(f'{G}/linear/{tag}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    open(f'{G}/linear/{tag}_description.md', 'w', encoding='utf-8').write(i['description'] or '')
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    for c in cs:
        open(f"{G}/linear/{tag}_comment_{c['createdAt'][:19].replace(':', '')}_{c['id'][:8]}.md", 'w', encoding='utf-8').write(c['body'] or '')
    print(f"\n{i['identifier']} [{i['state']['name']}/{i['state']['type']}] {i['priorityLabel']} assignee={i['assignee']['name'] if i['assignee'] else None} archived={i['archivedAt']} created={i['createdAt']} updated={i['updatedAt']} desc={len(i['description'] or '')}c comments={len(cs)}")
    print('   title:', i['title'])
    print('   parent:', i['parent'], 'children:', [(c['identifier'], c['state']['name']) for c in i['children']['nodes']])
    print('   labels:', [l['name'] for l in i['labels']['nodes']])
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

# every Linear attachment on pull/1002, whichever ticket carries it
QA = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url sourceType metadata createdAt issue{identifier title state{name}} } } }'''
for u in ('https://github.com/Secuura/Distributed_Secuura/pull/1002',):
    try:
        ns = gql(QA, {'u': u})['attachmentsForURL']['nodes']
        print(f"\nattachmentsForURL {u}: {len(ns)}")
        for a in ns:
            md = a.get('metadata') or {}
            print(f"   on {a['issue']['identifier']} [{a['issue']['state']['name']}] linkKind={md.get('linkKind')!r} created={a['createdAt']}")
    except Exception as e:
        print('attachmentsForURL failed:', type(e).__name__, str(e)[:200])
print('done at', now())
