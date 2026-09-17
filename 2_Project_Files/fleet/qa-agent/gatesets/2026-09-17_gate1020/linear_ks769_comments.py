#!/usr/bin/env python3
"""linear_ks769_comments.py — READ-ONLY: KS-769 comments (date, author, first 300 chars) and whether any records the dormant ruling. LINEAR_API_KEY by NAME, never printed."""
import json, urllib.request, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
k = [l.split('=', 1)[1].strip().strip('"').strip("'") for l in open(ENV) if l.startswith('LINEAR_API_KEY=')][0]
q = 'query{ issue(id:"KS-769"){ identifier description comments(first:50){nodes{id createdAt user{name} botActor{name} body}} } }'
d = json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q}).encode(), headers={'Authorization': k, 'Content-Type': 'application/json'}), timeout=60))
i = d['data']['issue']
print('description mentions dormant:', bool(re.search(r'(?i)dormant', i['description'] or '')), '| control word "mobile" in description:', bool(re.search(r'(?i)mobile', i['description'] or '')))
for c in sorted(i['comments']['nodes'], key=lambda c: c['createdAt']):
    print(c['createdAt'], c['id'][:8], (c['user'] or {}).get('name'), (c['botActor'] or {}).get('name'), '| dormant:', bool(re.search(r'(?i)dormant', c['body'])), '|', c['body'][:300].replace('\n', ' '))
