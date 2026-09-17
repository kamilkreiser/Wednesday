import json,os,sys,urllib.request,subprocess,datetime
tok=os.environ['GH_TOKEN']
def get(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r))
print('read_at', datetime.datetime.now().strftime('%H:%M:%S'))
pr=get('/pulls/1021'); print('#1021 head', pr['head']['sha'], 'state', pr['state'], 'merged', pr['merged'], 'base', pr['base']['ref'])
dv=get('/branches/develop'); print('develop', dv['commit']['sha'])
for n in (1022,1023,1024):
    p=get('/pulls/%d'%n); print('#%d head'%n, p['head']['sha'], p['state'])
fl=get('/pulls/1021/files'); print('files', [(f['filename'],f['additions'],f['deletions']) for f in fl])
# control: a known-wrong PR number must 404
try: get('/pulls/99999'); print('control: 99999 FOUND (bad)')
except Exception as e: print('control: 99999 ->', str(e)[:40])
