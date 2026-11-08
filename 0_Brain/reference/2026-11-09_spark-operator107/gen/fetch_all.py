import re,json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?(LINEAR_API_KEY|LINEAR_TEAM_ID)=(.*)$',l.rstrip('\n'))
    if m: env[m.group(1)]=m.group(2).strip().strip('"\'')
def q(query,vars):
    rq=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':query,'variables':vars}).encode(),headers={'Authorization':env['LINEAR_API_KEY'],'Content-Type':'application/json'})
    with urllib.request.urlopen(rq,timeout=90) as r: return json.loads(r.read())
Q='''query($t:ID!,$a:String){issues(first:40,after:$a,filter:{team:{id:{eq:$t}},state:{type:{in:["backlog","unstarted","started"]}}}){pageInfo{hasNextPage endCursor} nodes{identifier title description priority updatedAt state{name type} labels{nodes{name}} comments(first:50){nodes{createdAt body user{name}}}}}}'''
out=[];a=None
while True:
    d=q(Q,{'t':env['LINEAR_TEAM_ID'],'a':a})
    if 'errors' in d: print(d['errors']); sys.exit(1)
    i=d['data']['issues']; out+=i['nodes']
    if not i['pageInfo']['hasNextPage']: break
    a=i['pageInfo']['endCursor']
out.sort(key=lambda x:-int(x['identifier'].split('-')[1]))
json.dump(out,open(sys.argv[1],'w'))
print(len(out))
for x in out: print(x['identifier'],x['state']['name'],len(x['comments']['nodes']),x['title'][:110])
