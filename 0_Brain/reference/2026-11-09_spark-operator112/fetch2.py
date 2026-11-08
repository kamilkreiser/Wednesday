import os,json,urllib.request,sys
env={}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip('"\'')
key=env['LINEAR_API_KEY']
def q(query,var=None):
    r=urllib.request.Request('https://api.linear.app/graphql',json.dumps({'query':query,'variables':var or {}}).encode(),{'Authorization':key,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
out=[]
for n in sys.argv[2:]:
    d=q('query($n:Float){issues(filter:{number:{eq:$n}}){nodes{identifier title description state{name} labels{nodes{name}} comments{nodes{body createdAt}}}}}',{'n':float(n)})
    out+=d['data']['issues']['nodes']
json.dump(out,open(sys.argv[1],'w'),indent=1)
