import json,re,subprocess,os,sys
O=sys.argv[1]; PIN='7eda23b34d3b7a413ca8f9c0945c7843708ce9f4'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
rows=json.load(open(O+'/ready_all2.json'))
def git(*a):
    return subprocess.run(['git','-C',S]+list(a),capture_output=True,text=True).stdout.strip()
for r in rows:
    if r['cls']!='REV-OK' or r['pr'] or r['live']: continue
    t=open(N+r['name'],encoding='utf-8',errors='replace').read()
    m=re.search(r'```diff\n(.*?)\n```',t,re.S)
    body=m.group(1) if m else ''
    if not m:
        c=re.search(r'CANONICAL PATCH = `([^`]+)`',t); body=open(c.group(1),errors='replace').read()
    adds=[l[1:].strip() for l in body.split('\n') if l.startswith('+') and not l.startswith('+++')]
    adds=sorted({a for a in adds if len(a)>=30},key=len,reverse=True)
    fs=r['files']; land=None
    for a in adds[:3]:
        out=git('log','--format=%h %s','--reverse','-S'+a,PIN,'--',*fs) if fs else ''
        if out:
            land=(out.split('\n')[0][:150],'git log -S"%s..." -- files'%a[:40].replace('"',"'")); break
    if not land:
        out=git('log','--format=%h %s','--reverse','-E','--grep',r['key']+r'([^0-9]|$)',PIN,'--',*fs) if fs else ''
        if out: land=(out.split('\n')[0][:150],'git log --grep %s -- files (no pickaxe line >=30 chars found)'%r['key'])
    r['land']=land
json.dump(rows,open(O+'/ready_all3.json','w'),indent=1)
print(sum(1 for r in rows if r['cls']=='REV-OK' and not r['pr'] and not r['live'] and r.get('land')),'with landing /',sum(1 for r in rows if r['cls']=='REV-OK' and not r['pr'] and not r['live']))
