#!/usr/bin/env python3
"""READ-ONLY: compare M55 48e65c435...0b25f823f (GET), list services/auth + api-gateway + shared files that moved; userRepo.ts :681-694 at base. GH_TOKEN by NAME; never printed."""
import json, urllib.request, base64, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok=[l.split('=',1)[1].strip().strip('"').strip("'") for l in open(ENV) if l.startswith('GH_TOKEN=')][0]
base='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(base+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=60))
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
c=get('/commits/48e65c435'); print('M55 resolves to', c['sha'], c['commit']['message'].splitlines()[0][:120])
cm=get(f"/compare/{c['sha']}...0b25f823f6660ac52b665f14055799ff0c3b616d")
print(f"compare M55...0b25f823f: status={cm['status']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])}")
for x in cm['commits']: print('  commit', x['sha'][:9], x['commit']['message'].splitlines()[0][:110])
for f in cm['files']:
    fn=f['filename']
    if any(k in fn for k in ('services/auth/','services/api-gateway/','packages/shared/','vitest','package-lock','package.json')): print('  moved:', f['status'], f"+{f['additions']} -{f['deletions']}", fn)
u=get('/contents/Blockchain/Dev/services/auth/src/repositories/userRepo.ts?ref=0b25f823f6660ac52b665f14055799ff0c3b616d')
lines=base64.b64decode(u['content']).decode().splitlines()
print('userRepo.ts lines at base:', len(lines)); 
for i in range(679,696): print(f'  {i+1}: {lines[i]}')
print('anchor count (ON CONFLICT (email_lookup_hash) WHERE email_lookup_hash IS NOT NULL DO UPDATE SET):', sum(l.count('ON CONFLICT (email_lookup_hash) WHERE email_lookup_hash IS NOT NULL DO UPDATE SET') for l in lines))
print('control count (ON CONFLICT):', sum(l.count('ON CONFLICT') for l in lines))
