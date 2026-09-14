#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear GraphQL reads for the #912 ROUND-2 + #937 stacked gate set. Key sourced by NAME (LINEAR_API_KEY) from the Secuura .env; never printed.
comments(first:50) sorted client-side by createdAt; never last:N. includeArchived:true everywhere."""
import json, sys, urllib.request, datetime, re
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G=sys.argv[1]
key=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key=line.split('=',1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'
def gql(q, v):
    r=urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query':q,'variables':v}).encode(), headers={'Authorization':key,'Content-Type':'application/json'}), timeout=60)
    j=json.load(r)
    assert 'errors' not in j, j.get('errors')
    return j['data']
Q='''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:5){ nodes{
  identifier title state{name} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  attachments(first:20){nodes{url title}}
  relations(first:20){nodes{type relatedIssue{identifier}}}
  inverseRelations(first:20){nodes{type issue{identifier}}}
  comments(first:50){nodes{id createdAt user{name} body bodyData}} }}}'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
HEAD='609c44c55'; R1='ae8751f38'; H937='6fd3a8bec'
WANT={'f43c0944','2be90dbd','639e4790','744a7fa5','e165121a','3e27f051'}
for n in [1004,1059,1058,1057,1071,1070,1069,1068,1067,535,587,520,685,485,772,1130,1123,1124,1074,1024]:
    d=gql(Q,{'n':n})['issues']['nodes']
    if not d: print(f'KS-{n}: NOT FOUND'); continue
    i=d[0]
    json.dump(i, open(f'{G}/linear/ks{n}.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)
    cs=sorted(i['comments']['nodes'], key=lambda c:c['createdAt'])
    att=[a['url'].split('/')[-1] for a in i['attachments']['nodes'] if 'github.com' in a['url']]
    desc=i['description'] or ''
    print(f"{i['identifier']} [{i['state']['name']}] {i['priorityLabel']} assignee={i['assignee']['name'] if i['assignee'] else None} archived={i['archivedAt']} created={i['createdAt']} updated={i['updatedAt']} PRs={att} attachments={len(i['attachments']['nodes'])} comments={len(cs)} desc={len(desc)}c at-signs={desc.count('@')} branch={i['branchName'][:70]!r} title={i['title'][:90]!r}")
    print('   related:', [(r['type'],r['relatedIssue']['identifier']) for r in i['relations']['nodes']], 'inverse:', [(r['type'],r['issue']['identifier']) for r in i['inverseRelations']['nodes']])
    if n in (1004, 1059):
        open(f'{G}/linear/ks{n}_desc.md','w',encoding='utf-8').write(desc)
        print('   desc KS ids:', sorted(set(re.findall(r'KS-\d+', desc))), 'PR refs:', sorted(set(re.findall(r'#\d{3,4}', desc))), 'BLUF first:', desc.lstrip().startswith('## BLUF'), '| searched-line present:', ('search' in desc.lower()), '| CORPUS/ks781 named:', ('ks781' in desc), ('CORPUS' in desc))
    for c in cs:
        b=c['body'] or ''; bd=c['bodyData'] or ''
        mention=bd.count('suggestion_userMentions')
        flag='  <<< named id' if c['id'][:8] in WANT else ''
        if c['id'][:8] in WANT: open(f"{G}/linear/ks{n}_comment_{c['id'][:8]}.md",'w',encoding='utf-8').write(b)
        print(f"   comment {c['id'][:8]} {c['createdAt']} {c['user']['name'] if c['user'] else 'bot'} chars={len(b)} at-signs={b.count('@')} mention-nodes={mention} head={HEAD in b} r1={R1 in b} h937={H937 in b} KS={sorted(set(re.findall(r'KS-\d+', b)))}{flag}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
