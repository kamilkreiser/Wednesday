#!/usr/bin/env python3
"""linear_search.py — READ-ONLY board search by SYMBOL/path (title OR description containsIgnoreCase, includeArchived:true). Key by NAME."""
import json, sys, urllib.request, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
key=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key=line.split('=',1)[1].strip().strip('"').strip("'")
assert key
def gql(q, v):
    r=urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query':q,'variables':v}).encode(), headers={'Authorization':key,'Content-Type':'application/json'}), timeout=60)
    j=json.load(r); assert 'errors' not in j, j.get('errors'); return j['data']
S='''query($q:String!){ issues(filter:{team:{key:{eq:"KS"}}, or:[{title:{containsIgnoreCase:$q}},{description:{containsIgnoreCase:$q}}]}, includeArchived:true, first:40){ nodes{ identifier title state{name} archivedAt } } }'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for q in sys.argv[1:]:
    r=gql(S,{'q':q})['issues']['nodes']
    print(f"search {q!r}: {len(r)} -> {[(x['identifier'], x['state']['name'], 'ARCHIVED' if x['archivedAt'] else '') for x in r]}")
