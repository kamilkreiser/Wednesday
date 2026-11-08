import re,json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?(LINEAR_API_KEY)=(.*)$',l.rstrip('\n'))
    if m: env[m.group(1)]=m.group(2).strip().strip('"\'')
def q(query,vars):
    rq=urllib.request.Request('https://api.linear.app/graphql',data=json.dumps({'query':query,'variables':vars}).encode(),headers={'Authorization':env['LINEAR_API_KEY'],'Content-Type':'application/json'})
    with urllib.request.urlopen(rq,timeout=60) as r: return json.loads(r.read())
rows=json.load(open(sys.argv[1]))
keys=sorted({re.match(r'READY_(KS-\d+)',r['name']).group(1) for r in rows},key=lambda k:int(k[3:]))
Q='query($i:String!){issue(id:$i){identifier title state{name type} updatedAt comments(first:50){nodes{createdAt body}}}}'
out={}
for k in keys:
    try:
        d=q(Q,{'i':k})
        i=d['data']['issue']
        if not i: out[k]=None; continue
        cs=sorted(i['comments']['nodes'],key=lambda c:c['createdAt'],reverse=True)
        out[k]=dict(title=i['title'],state=i['state']['name'],type=i['state']['type'],upd=i['updatedAt'],ncom=len(cs),newest=(cs[0]['createdAt'],cs[0]['body'][:400]) if cs else None)
    except Exception as e:
        out[k]={'err':str(e)[:100]}
json.dump(out,open(sys.argv[2],'w'),indent=1)
print(len(keys))
