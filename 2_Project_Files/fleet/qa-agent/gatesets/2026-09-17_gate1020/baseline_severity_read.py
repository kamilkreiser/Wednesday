import json,os,urllib.request,base64
tok=os.environ['GH_TOKEN']
r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/scripts/audit/audit-baseline.json?ref=develop',headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
j=json.loads(base64.b64decode(json.load(urllib.request.urlopen(r))['content']))
for k,v in j['accepted'].items():
    if isinstance(v,dict) and v.get('expires') and str(v.get('expires'))<='2026-09-30':
        sev=[f'{kk}={str(vv)[:12]}' for kk,vv in v.items() if 'sever' in kk.lower()]
        rs=v.get('reason','')
        hint=[w for w in ('HIGH','high','moderate','MODERATE','critical','low') if w in rs]
        print(v.get('expires'),k,v.get('package'),sev,'reason-words:',hint)
