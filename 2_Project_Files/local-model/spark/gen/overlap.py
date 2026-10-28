#!/usr/bin/env python3
"""overlap.py <brief_dir_name> ... - golden.diff file set of each brief vs (a) the files of the 23 held passes (the READY_* files in night/),
(b) every OPEN Secuura PR's files (gh, project GH_TOKEN from the Secuura .env in a scratch GH_CONFIG_DIR; token never printed).
Prints OVERLAP lines or 'ok'. Develop moves are checked by ls-remote separately (see README)."""
import os,sys,re,glob,json,subprocess,tempfile
NIGHT=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'local-model','night') if False else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','night'))
def files_of(diff): return set(re.findall(r'^\+\+\+ b/(\S+)',diff,re.M))
held={}
import time
TODAY=time.mktime(time.strptime(os.environ.get('HELD_SINCE','2026-10-28'),'%Y-%m-%d'))
for f in glob.glob(NIGHT+'/READY_*.diff.md'):
    if os.path.getmtime(f)<TODAY: continue  # the held passes are today's READY files (HELD_SINCE=YYYY-MM-DD to change)
    t=open(f,encoding='utf-8',errors='replace').read()
    tag=re.search(r'READY_(KS-\d+)-.*?-(ks_\w+?)_spark',os.path.basename(f))
    for p in files_of(t): held.setdefault(p,set()).add(os.path.basename(f)[:40])
def open_pr_files():
    env={}
    for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
        if l.startswith('GH_TOKEN='): env['GH_TOKEN']=l.split('=',1)[1].strip().strip('"\'')
    d=tempfile.mkdtemp()
    e=dict(os.environ,GH_CONFIG_DIR=d,**env)
    out=subprocess.run(['gh','pr','list','-R','Secuura/Distributed_Secuura','--state','open','--limit','200','--json','number,files'],capture_output=True,text=True,env=e)
    if out.returncode: sys.exit('gh failed: '+out.stderr[:200])
    r={}
    for pr in json.loads(out.stdout):
        for f in pr['files']: r.setdefault(f['path'],[]).append(pr['number'])
    print('open PRs files:',len(r),file=sys.stderr); return r
prs=open_pr_files()
print('held files:',len(held),file=sys.stderr)
bad=0
for b in sys.argv[1:]:
    g=os.path.join(NIGHT,'briefs',b,'golden.diff')
    for p in sorted(files_of(open(g,encoding='utf-8').read())):
        if p in prs: print('OVERLAP open PR',prs[p],b,p); bad+=1
        if p in held: print('OVERLAP held',held[p],b,p); bad+=1
print('ok' if not bad else 'OVERLAPS: %d'%bad)
