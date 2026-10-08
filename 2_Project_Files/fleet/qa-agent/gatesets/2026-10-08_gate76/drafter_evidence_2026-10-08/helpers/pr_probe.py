import json, urllib.request, hashlib, sys, re
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok=[l.split('=',1)[1].strip().strip('"').strip("'") for l in open(ENV) if l.startswith('GH_TOKEN=')][0]
def get(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r,timeout=60))
OUT=sys.argv[1]
for n in sys.argv[2:]:
    p=get('pulls/'+n); b=(p.get('body') or '').encode()
    json.dump(p,open("%s/pr_%s.json"%(OUT,n),"w"))
    open('%s/body_%s.md'%(OUT,n),'wb').write(b)
    print(n, 'state',p['state'],'merged',p.get('merged'),'base',p['base']['ref'],p['base']['sha'][:12],'head',p['head']['sha'],'commits',p['commits'],'files',p['changed_files'],'+%d -%d'%(p['additions'],p['deletions']),'mergeable',p.get('mergeable'),p.get('mergeable_state'))
    print('  title %d chars ascii %s: %s'%(len(p['title']),p['title'].isascii(),p['title']))
    print('  body %d B sha256/16 %s'%(len(b),hashlib.sha256(b).hexdigest()[:16]))
    t=p['title']+'\n'+p.get('body','')
    print('  hyphenated',sorted(set(re.findall(r'\bKS-\d+\b',t))),'Refs',sorted(set(re.findall(r'Refs:?\s+(KS-\d+)',t))))
    print('  closing', re.findall(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b\s*:?\s*KS-\d+', t, re.I), 'broad', re.findall(r'(clos(?:e|es|ed)|fix(?:es|ed)?|resolv(?:e|es|ed))\s+KS-\d+',t,re.I))
