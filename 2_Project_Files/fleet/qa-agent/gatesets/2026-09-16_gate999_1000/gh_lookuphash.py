#!/usr/bin/env python3
"""READ-ONLY: which tracked SQL/TS files at base mention email_lookup_hash or ON CONFLICT (email); userRepo.ts:1375-1392. GH code via trees+contents GET; GH_TOKEN by NAME, never printed."""
import json, urllib.request, base64, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok=[l.split('=',1)[1].strip().strip('"').strip("'") for l in open(ENV) if l.startswith('GH_TOKEN=')][0]
B='https://api.github.com/repos/Secuura/Distributed_Secuura'; REF='0b25f823f6660ac52b665f14055799ff0c3b616d'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(B+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=90))
def blob(path): return base64.b64decode(get('/contents/'+path+'?ref='+REF)['content']).decode('utf-8','replace')
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
paths=[t['path'] for t in get(f'/git/trees/{REF}?recursive=1')['tree'] if t['type']=='blob']
sql=[p for p in paths if p.endswith('.sql') and ('migration' in p.lower() or 'init' in p.lower() or 'schema' in p.lower())]
print('sql files scanned:', len(sql))
for p in sql:
    s=blob(p)
    for i,l in enumerate(s.splitlines(),1):
        if re.search(r'(?i)email_lookup_hash|on\s+conflict\s*\(\s*email\s*\)', l): print(f'  {p}:{i}: {l.strip()[:130]}')
u=blob('Blockchain/Dev/services/auth/src/repositories/userRepo.ts').splitlines()
for i in range(1374,1392): print(f'  userRepo.ts:{i+1}: {u[i]}')
