import json,re,subprocess,sys
O=sys.argv[1];P='7eda23b34d3b7a413ca8f9c0945c7843708ce9f4'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/_quarantine_2026-11-09/stale/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
rows=json.load(open(O+'/perfile.json'))
for r in rows:
    t=open(N+r['name'],encoding='utf-8',errors='replace').read()
    m=re.search(r'```diff\n(.*?)\n```',t,re.S)
    body=m.group(1) if m else open(re.search(r'CANONICAL PATCH = `([^`]+)`',t).group(1),errors='replace').read()
    res=[]
    for pt in re.split(r'(?m)^(?=--- (?:a/|/dev/null))',body):
        mm=re.search(r'^\+\+\+ b/(\S+)',pt,re.M)
        if not mm: continue
        f=mm.group(1)
        if re.search(r'^--- /dev/null',pt,re.M): res.append((f.split('/')[-1],'NEWFILE','',f'exists={subprocess.run(["git","-C",S,"cat-file","-e",P+":"+f],capture_output=True).returncode==0}')); continue
        tip=subprocess.run(['git','-C',S,'show',P+':'+f],capture_output=True,text=True,errors='replace').stdout.split('\n')
        ts={l.strip() for l in tip}
        mi=[l[1:].strip() for l in pt.split('\n') if l.startswith('-') and not l.startswith('---') and len(l[1:].strip())>=12]
        pl=[l[1:].strip() for l in pt.split('\n') if l.startswith('+') and not l.startswith('+++') and len(l[1:].strip())>=12]
        res.append((f.split('/')[-1],'-%d/%d'%(sum(x in ts for x in mi),len(mi)),'+%d/%d'%(sum(x in ts for x in pl),len(pl)),''))
    r['owed']=res
json.dump(rows,open(O+'/owed.json','w'),indent=1)
