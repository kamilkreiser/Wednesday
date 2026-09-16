"""drafterlib.py — shared helpers for the #1007 drafter runs (vitest JSON reporter, anchored edits with sha-asserted restore)."""
import subprocess, os, json, datetime, hashlib
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007'
PATHS=json.load(open(GS+'/drafter_paths.json')); W=PATHS['W']; T=PATHS['trees']
GWR='Blockchain/Dev/services/api-gateway'
FARM=['?? Blockchain/Dev/packages/shared/node_modules', '?? Blockchain/Dev/services/api-gateway/node_modules', '?? node_modules']
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def vitest(label, tree, files=(), env_extra=None, save=True):
    gw=T[tree]+'/'+GWR; out=W+'/json_%s.json'%label
    env=dict(os.environ); env.pop('NODE_ENV',None); env.update(env_extra or {})
    t0=datetime.datetime.now()
    p=subprocess.run([T[tree]+'/Blockchain/Dev/node_modules/.bin/vitest','run',*files,'--reporter=json','--outputFile='+out],cwd=gw,env=env,capture_output=True,text=True)
    dt=(datetime.datetime.now()-t0).total_seconds()
    try: j=json.load(open(out))
    except Exception: P(ts(),label,'NO JSON rc',p.returncode,p.stderr[-1500:]); return None
    cells={}; suite_msgs=[]
    for tr in j['testResults']:
        fn=tr['name'].split('/src/')[-1]
        if tr.get('message'): suite_msgs.append((fn,tr['message'][:300]))
        for a in tr['assertionResults']:
            cells[fn+' :: '+a['fullName']]={'status':a['status'],'msg':(a.get('failureMessages') or [''])[0][:300]}
    r={'label':label,'tree':tree,'rc':p.returncode,'files':len(j['testResults']),'tests':j['numTotalTests'],'passed':j['numPassedTests'],'failed':j['numFailedTests'],'secs':round(dt,1),'suite_messages':suite_msgs,'cells':cells}
    P(ts(),'%-34s tree %-6s rc %d FILES %d TESTS %d passed %d failed %d secs %.1f suite_msgs %d'%(label,tree,p.returncode,r['files'],r['tests'],r['passed'],r['failed'],dt,len(suite_msgs)))
    for fn,m in suite_msgs: P('    SUITE MSG', fn, '|', m.split('\n')[0][:200])
    for k,v in cells.items():
        if v['status']!='passed': P('    RED', k, '|', v['msg'].split('\n')[0][:200])
    if save: json.dump(r,open(GS+'/vt_%s.json'%label,'w'),indent=1)
    return r
def edit(path, old, new, markers=()):
    s=open(path).read(); before=sha(path); n=s.count(old)
    assert n==1, 'ANCHOR COUNT %d != 1 for %r'%(n,old[:90])
    s=s.replace(old,new); open(path,'w').write(s); after=sha(path); assert after!=before
    for m,want in markers:
        got=open(path).read().count(m); assert got==want, 'MARKER %r %d != %d'%(m[:60],got,want)
    P('   landed: anchor count 1, sha %s -> %s, markers %s'%(before[:12],after[:12],[(m[:50],w) for m,w in markers]))
def restore(tree, rel, pristine):
    subprocess.run(['git','-C',T[tree],'checkout','--',rel],check=True)
    got=sha(T[tree]+'/'+rel); assert got==pristine, 'RESTORE sha %s != %s'%(got[:12],pristine[:12]); P('   restored sha-identical', got[:12])
def porcelain(tree): return subprocess.run(['git','-C',T[tree],'status','--porcelain','--untracked-files=all'],capture_output=True,text=True).stdout.strip().splitlines()
