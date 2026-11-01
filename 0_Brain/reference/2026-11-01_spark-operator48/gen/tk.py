import re,json,urllib.request
key=None
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    m=re.match(r'\s*(?:export\s+)?(LINEAR[A-Z_]*KEY[A-Z_]*)\s*=\s*(.*)',l)
    if m and m.group(2).strip().strip('"\''): key=m.group(2).strip().strip('"\''); break
assert key
q={'query':'query($n:Float){issues(filter:{number:{eq:$n},team:{key:{eq:"KS"}}}){nodes{identifier title state{name} description comments{nodes{body createdAt}}}}}','variables':{'n':1926}}
r=urllib.request.Request('https://api.linear.app/graphql',json.dumps(q).encode(),{'Authorization':key,'Content-Type':'application/json'})
print(json.dumps(json.load(urllib.request.urlopen(r)),indent=1)[:7000])
