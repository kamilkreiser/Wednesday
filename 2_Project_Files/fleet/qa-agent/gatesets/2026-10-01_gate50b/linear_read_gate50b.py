#!/usr/bin/env python3
"""linear_read_gate50b.py — ONE read-only Linear GraphQL QUERY per ticket (no mutation) for the ticket sources of ITEM 4 / ITEM 5: KS-1376, KS-1054,
KS-1397, KS-729. Prints identifier, state, assignee, title, description length + sha256 prefix, and the description's markdown HEADINGS only (the
gate reads the text itself under X5). LINEAR_API_KEY is read BY NAME from the Secuura .env and never printed. Usage: linear_read_gate50b.py"""
import json, urllib.request, re, hashlib, datetime
env = open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8').read()
key = re.search(r'^LINEAR_API_KEY=(.*)$', env, re.M).group(1).strip().strip('"').strip("'")
def q(query, v):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': query, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
print('linear_read_gate50b %s (queries only)' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
ok = 0
for k in ['KS-1376', 'KS-1054', 'KS-1397', 'KS-729']:
    d = q('query($id:String!){issue(id:$id){identifier title state{name} assignee{name} updatedAt description}}', {'id': k}).get('data', {}).get('issue')
    if not d: print('MISSING %s' % k); continue
    ok += 1; desc = d['description'] or ''
    print('%s | %s | assignee %s | updated %s | desc %d B sha256 %s | %s' % (d['identifier'], d['state']['name'], (d['assignee'] or {}).get('name'), d['updatedAt'], len(desc.encode()), hashlib.sha256(desc.encode()).hexdigest()[:16], d['title']))
    print('   headings: %s' % [h.strip('# ').strip() for h in re.findall(r'(?m)^#{1,3} .*$', desc)])
print('LINEAR READ OK: %d of 4 tickets read' % ok if ok == 4 else 'LINEAR READ INCOMPLETE: %d of 4' % ok)
