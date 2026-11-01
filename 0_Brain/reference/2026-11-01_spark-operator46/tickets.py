import os,re,subprocess,json,urllib.request
envf='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
key=None
for l in open(envf):
    m=re.match(r'\s*(?:export\s+)?(LINEAR[A-Z_]*KEY[A-Z_]*)\s*=\s*(.*)',l)
    if m and m.group(2).strip().strip('"\''): key=m.group(2).strip().strip('"\''); break
assert key
for n in (1903,1902,1884):
    q={'query':'query($n:Float){issues(filter:{number:{eq:$n},team:{key:{eq:"KS"}}}){nodes{identifier title state{name} description comments{nodes{body createdAt}}}}}','variables':{'n':n}}
    r=urllib.request.Request('https://api.linear.app/graphql',json.dumps(q).encode(),{'Authorization':key,'Content-Type':'application/json'})
    d=json.load(urllib.request.urlopen(r))
    print(json.dumps(d,indent=1)[:6000]); print('=========')
