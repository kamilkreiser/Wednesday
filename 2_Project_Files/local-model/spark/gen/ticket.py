#!/usr/bin/env python3
"""ticket.py KS-n [KS-m ...] - print Linear ticket text (read only). LINEAR_API_KEY must be in the env (source the Secuura .env; never printed)."""
import os,sys,json,urllib.request
key=os.environ.get('LINEAR_API_KEY') or sys.exit('LINEAR_API_KEY unset')
for ident in sys.argv[1:]:
    team,num=ident.split('-')
    q={"query":"query($t:String!,$n:Float!){issues(filter:{team:{key:{eq:$t}},number:{eq:$n}}){nodes{identifier title description state{name} assignee{name} comments{nodes{body user{name}}}}}}","variables":{"t":team,"n":float(num)}}
    r=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps(q).encode(),headers={"Content-Type":"application/json","Authorization":key})
    n=json.load(urllib.request.urlopen(r,timeout=60))['data']['issues']['nodes'][0]
    print('=====',n['identifier'],n['title'],'['+n['state']['name']+']','assignee:',(n['assignee'] or {}).get('name'))
    print(n['description']); 
    for c in n['comments']['nodes']: print('--comment',(c.get('user') or {}).get('name'),':',c['body'][:800])
