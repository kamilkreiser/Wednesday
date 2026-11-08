import re,json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?(LINEAR_API_KEY)=(.*)$',l.rstrip('\n'))
    if m: env[m.group(1)]=m.group(2).strip().strip('"\'')
def q(query,vars):
    rq=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':query,'variables':vars}).encode(),headers={'Authorization':env['LINEAR_API_KEY'],'Content-Type':'application/json'})
    with urllib.request.urlopen(rq,timeout=60) as r: return json.loads(r.read())
Q='query($i:String!){issue(id:$i){identifier title description state{name} updatedAt comments(first:100){nodes{createdAt body user{name}}}}}'
for k in sys.argv[1:]:
    d=q(Q,{'i':k})['data']['issue']
    print('#####',d['identifier'],d['title'],d['state']['name'],d['updatedAt']);print(d['description']);
    for c in sorted(d['comments']['nodes'],key=lambda c:c['createdAt'],reverse=True):
        print('--- comment',c['createdAt'],c['user'] and c['user']['name']);print(c['body'])
