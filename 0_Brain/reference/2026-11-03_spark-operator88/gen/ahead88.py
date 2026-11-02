import re,json,urllib.request,urllib.parse,sys
tok=None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',encoding='utf-8'):
    m=re.match(r'^\s*(?:export\s+)?GH_TOKEN=(.*)$',l.rstrip('\n'))
    if m: tok=m.group(1).strip().strip('"\'')
def get(u):
    rq=urllib.request.Request(u,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json','User-Agent':'op88'})
    with urllib.request.urlopen(rq,timeout=60) as r: return json.loads(r.read())
R='https://api.github.com/repos/Secuura/Distributed_Secuura'
br=[l.split('refs/heads/')[1].strip() for l in open(sys.argv[1]) if re.search(r'ks-1868|ks-19[3-9]\d',l)]
for b in br:
    try:
        c=get(R+'/compare/develop...'+urllib.parse.quote(b,safe='/'))
        if c['ahead_by']>0:
            print(b[-60:],'ahead',c['ahead_by'],[f['filename'].replace('Blockchain/Dev/','') for f in c['files']][:12])
    except Exception as e: print(b,'ERR',e)
print('checked',len(br))
