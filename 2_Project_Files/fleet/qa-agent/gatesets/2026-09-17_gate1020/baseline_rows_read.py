import json,os,urllib.request,base64
tok=os.environ['GH_TOKEN']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r))
tree=gh('/git/trees/develop?recursive=1')
paths=[t['path'] for t in tree['tree'] if t['path'].endswith('audit-baseline.json')]
print('baseline files:',paths)
for p in paths:
    c=gh('/contents/'+p+'?ref=develop'); j=json.loads(base64.b64decode(c['content']))
    def walk(o,path=''):
        if isinstance(o,dict):
            e=o.get('expires')
            if isinstance(e,str) and e<='2026-09-30':
                print(e, path, {k:(str(v)[:70]) for k,v in o.items() if k in ('id','ghsa','advisory','package','name','severity','ticket','reason','lock','source')})
            for k,v in o.items(): walk(v,path+'/'+str(k))
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,path+'[%d]'%i)
    walk(j)
