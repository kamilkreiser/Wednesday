#!/usr/bin/env python3
"""linear_titles.py — READ-ONLY: title/state/description head for a few neighbour tickets. Key by NAME."""
import json, sys, urllib.request, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
key=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key=line.split('=',1)[1].strip().strip('"').strip("'")
assert key
def gql(q, v):
    r=urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query':q,'variables':v}).encode(), headers={'Authorization':key,'Content-Type':'application/json'}), timeout=60)
    j=json.load(r); assert 'errors' not in j, j.get('errors'); return j['data']
Q='''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:2){ nodes{ identifier title state{name} priorityLabel archivedAt createdAt description attachments(first:10){nodes{url}} }}}'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in [int(x) for x in sys.argv[1:]]:
    d=gql(Q,{'n':n})['issues']['nodes']
    if not d: print(f'KS-{n}: NOT FOUND'); continue
    i=d[0]; desc=(i['description'] or '').replace('\n',' ')
    print(f"{i['identifier']} [{i['state']['name']}] {i['priorityLabel']} archived={i['archivedAt']} created={i['createdAt'][:10]} PRs={[a['url'].split('/')[-1] for a in i['attachments']['nodes'] if 'github.com' in a['url']]}\n   title: {i['title']}\n   desc[:400]: {desc[:400]}")
