#!/usr/bin/env python3
"""linear_titles.py — READ-ONLY: title + state + the description lines mentioning a term, for the board-search hits. Key by NAME."""
import json, sys, urllib.request, re
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
key=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key=line.split('=',1)[1].strip().strip('"').strip("'")
assert key
def gql(q, v):
    r=urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query':q,'variables':v}).encode(), headers={'Authorization':key,'Content-Type':'application/json'}), timeout=60)
    j=json.load(r); assert 'errors' not in j, j.get('errors'); return j['data']
Q='''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:5){ nodes{ identifier title state{name} priorityLabel archivedAt createdAt description attachments(first:10){nodes{url}} }}}'''
term=sys.argv[1]
for n in sys.argv[2:]:
    i=gql(Q,{'n':float(n)})['issues']['nodes'][0]
    d=i['description'] or ''
    print(f"{i['identifier']} [{i['state']['name']} {i['priorityLabel']} created {i['createdAt'][:10]} archived={bool(i['archivedAt'])} att={[a['url'].split('/')[-1] for a in i['attachments']['nodes']]}] {i['title']}")
    for l in d.splitlines():
        if term.lower() in l.lower(): print('    |', l.strip()[:260])
