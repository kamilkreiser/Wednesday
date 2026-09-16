#!/usr/bin/env python3
"""READ-ONLY: every ON CONFLICT in services/auth/src at base 0b25f823f (git trees + contents API GET); and the two schema sources' users.email / email_lookup_hash declarations. GH_TOKEN by NAME; never printed."""
import json, urllib.request, base64, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok=[l.split('=',1)[1].strip().strip('"').strip("'") for l in open(ENV) if l.startswith('GH_TOKEN=')][0]
B='https://api.github.com/repos/Secuura/Distributed_Secuura'; REF='0b25f823f6660ac52b665f14055799ff0c3b616d'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(B+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=90))
def blob(path): return base64.b64decode(get('/contents/'+path+'?ref='+REF)['content']).decode('utf-8','replace')
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
tree=get(f'/git/trees/{REF}?recursive=1'); print('tree truncated:', tree['truncated'])
paths=[t['path'] for t in tree['tree'] if t['type']=='blob']
auth=[p for p in paths if p.startswith('Blockchain/Dev/services/auth/src/') and p.endswith('.ts') and '__tests__' not in p]
hits=0
for p in auth:
    s=blob(p)
    for i,l in enumerate(s.splitlines(),1):
        if re.search(r'(?i)on\s+conflict', l): hits+=1; print(f'  {p.split("services/auth/")[1]}:{i}: {l.strip()[:140]}')
print('auth non-test .ts files scanned:', len(auth), 'ON CONFLICT lines:', hits)
for sp in [p for p in paths if p.endswith('docker/init/01-schema.sql') or p.endswith('migrations/001_initial-schema.sql')]:
    s=blob(sp); print('schema source', sp)
    for i,l in enumerate(s.splitlines(),1):
        if re.search(r'(?i)email_lookup_hash|^\s*email\s', l) : print(f'   :{i}: {l.strip()[:150]}')
