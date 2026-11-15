import os,json,urllib.request,re
env=open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env').read()
m=re.search(r'^(?:export\s+)?LINEAR_API_KEY=(.*)$',env,re.M)
k=m.group(1).strip().strip('"\'')
q='{issue(id:"KS-2103"){identifier title state{name} priority priorityLabel assignee{name} createdAt updatedAt description labels{nodes{name}} comments(first:50){nodes{createdAt body user{name}}}}}'
r=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':q}).encode(),{'Authorization':k,'Content-Type':'application/json'})
d=json.load(urllib.request.urlopen(r))
i=d['data']['issue']
cs=sorted(i['comments']['nodes'],key=lambda c:c['createdAt'])
print(i['identifier'],i['title'],i['state']['name'],i['priority'],i['priorityLabel'],i['assignee'],i['createdAt'],i['updatedAt'],[l['name'] for l in i['labels']['nodes']])
print('DESC:',i['description'])
print(len(cs),'comments')
for c in cs: print('---',c['createdAt'],(c['user'] or {}).get('name'),'\n',c['body'][:1500])
