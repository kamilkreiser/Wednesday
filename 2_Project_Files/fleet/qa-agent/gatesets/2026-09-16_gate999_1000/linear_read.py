#!/usr/bin/env python3
"""READ-ONLY: GitHub linear[bot] comments on #999/#1000 (GET) + Linear GraphQL issue queries for KS-1130, KS-960, KS-1129. Keys by NAME from the Secuura .env; never printed. No mutations."""
import json, sys, os, urllib.request, datetime, re
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]; os.makedirs(f'{G}/linear', exist_ok=True)
vals={}
for line in open(ENV, encoding='utf-8'):
    for k in ('GH_TOKEN','LINEAR_API_KEY'):
        if line.startswith(k+'='): vals[k]=line.split('=',1)[1].strip().strip('"').strip("'")
assert vals.get('GH_TOKEN') and vals.get('LINEAR_API_KEY'), 'key(s) not found by name'
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in (999,1000):
    r=urllib.request.urlopen(urllib.request.Request(f'https://api.github.com/repos/Secuura/Distributed_Secuura/issues/{n}/comments',headers={'Authorization':'Bearer '+vals['GH_TOKEN'],'Accept':'application/vnd.github+json'}),timeout=60)
    for c in json.load(r):
        print(f'PR #{n} comment by {c["user"]["login"]} {c["created_at"]}: KS ids={sorted(set(re.findall(r"KS-[0-9]+", c["body"] or "")))}')
        print('   ', (c['body'] or '')[:600].replace('\n',' | '))
def gql(q, v):
    r=urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query':q,'variables':v}).encode(), headers={'Authorization':vals['LINEAR_API_KEY'],'Content-Type':'application/json'}), timeout=60)
    j=json.load(r); assert 'errors' not in j, j.get('errors'); return j['data']
Q='''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:5){ nodes{
  identifier title state{name type} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  attachments(first:20){nodes{url title subtitle}}
  relations(first:20){nodes{type relatedIssue{identifier}}}
  inverseRelations(first:20){nodes{type issue{identifier}}}
  comments(first:50){nodes{id createdAt user{name} body}} }}}'''
for n in (1130, 960, 1129):
    d=gql(Q,{'n':n})['issues']['nodes']
    if not d: print(f'KS-{n}: NOT FOUND'); continue
    i=d[0]; json.dump(i, open(f'{G}/linear/ks{n}.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)
    open(f'{G}/linear/ks{n}_description.md','w',encoding='utf-8').write(i['description'] or '')
    cs=sorted(i['comments']['nodes'], key=lambda c:c['createdAt'])
    for c in cs: open(f"{G}/linear/ks{n}_comment_{c['createdAt'][:19].replace(':','')}_{c['id'][:8]}.md",'w',encoding='utf-8').write(c['body'] or '')
    print(f"\n{i['identifier']} [{i['state']['name']}/{i['state']['type']}] {i['priorityLabel']} assignee={i['assignee']['name'] if i['assignee'] else None} archived={i['archivedAt']} created={i['createdAt']} updated={i['updatedAt']} desc={len(i['description'] or '')}c comments={len(cs)}")
    print('   title:', i['title'])
    print('   attachments:', [(a['url'], a['title'], a['subtitle']) for a in i['attachments']['nodes']])
    print('   relations:', [(r['type'],r['relatedIssue']['identifier']) for r in i['relations']['nodes']], 'inverse:', [(r['type'],r['issue']['identifier']) for r in i['inverseRelations']['nodes']])
    for c in cs: print(f"   comment {c['id'][:8]} {c['createdAt']} {c['user']['name'] if c['user'] else 'bot/integration'} chars={len(c['body'] or '')}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
