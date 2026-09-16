#!/usr/bin/env python3
"""drafter_merged2.py — develop moved to 93629700c (#1005's squash) during drafting. In the drafter's clone only: a worktree at head b28ed490a with a
LOCAL --no-ff merge of 93629700c (never pushed), farmed like the others, shared dist built; then the whole api-gateway suite and the parity probe
on it, compared cell-by-cell with the untampered head probe. Never rm."""
import sys, os, json, shutil, subprocess
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007')
import drafterlib as L
from drafterlib import P, ts
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; DEV='Blockchain/Dev'; GW=L.GWR
NEWDEV='93629700c3d219c1d8ca61d69150bb9b623fc1be'; HEAD='b28ed490ada70df2056763f4512c98443285a694'
def run(c,cwd=None): p=subprocess.run(c,cwd=cwd,capture_output=True,text=True); return p.returncode,p.stdout,p.stderr
P('drafter_merged2 start', ts())
wt=L.W+'/wt_merged2'
rc,o,e=run(['git','-C',L.PATHS['C'],'worktree','add','--detach','--quiet',wt,HEAD]); assert rc==0, e
rc,o,e=run(['git','-c','user.name=qa-drafter','-c','user.email=qa-drafter@invalid','-C',wt,'merge','--no-ff','--no-edit','-m','qa drafter local merge develop 93629700c',NEWDEV]); P('merge rc',rc,(o.strip().splitlines() or [''])[-1][:160]); assert rc==0
rc,o,e=run(['git','-C',wt,'rev-list','--parents','-n','1','HEAD']); P('merged2 HEAD+parents', o.strip())
rc,o,e=run(['git','-C',wt,'diff','--name-status',NEWDEV,'HEAD']); P('merged2 vs develop 93629700c:', o.strip().replace('\n',' | '))
rc,o,e=run(['git','-C',wt,'diff','--name-status',HEAD,'HEAD']); P('merged2 vs head:', o.strip().replace('\n',' | '))
src_dev_nm=os.path.join(REPO,DEV,'node_modules')
os.symlink(os.path.join(REPO,'node_modules'), os.path.join(wt,'node_modules'))
dnm=os.path.join(wt,DEV,'node_modules'); os.mkdir(dnm)
for ent in sorted(os.listdir(src_dev_nm)):
    s=os.path.join(src_dev_nm,ent)
    if ent=='@secuura':
        os.mkdir(os.path.join(dnm,ent))
        for sub in sorted(os.listdir(s)):
            t=os.readlink(os.path.join(s,sub)); os.symlink(os.path.normpath(os.path.join(dnm,ent,t)), os.path.join(dnm,ent,sub))
    elif os.path.islink(s) and not os.path.isabs(os.readlink(s)): os.symlink(os.path.normpath(os.path.join(dnm,os.readlink(s))), os.path.join(dnm,ent))
    else: os.symlink(s, os.path.join(dnm,ent))
for r in (GW+'/node_modules', DEV+'/packages/shared/node_modules'):
    if os.path.isdir(os.path.join(REPO,r)): os.symlink(os.path.join(REPO,r), os.path.join(wt,r))
rc,o,e=run([wt+'/'+DEV+'/node_modules/.bin/tsc','-p','.'],cwd=wt+'/'+DEV+'/packages/shared'); P('shared dist build rc',rc)
L.T['merged2']=wt; paths=json.load(open(L.GS+'/drafter_paths.json')); paths['trees']['merged2']=wt; json.dump(paths,open(L.GS+'/drafter_paths.json','w'),indent=1)
assert L.porcelain('merged2')==L.FARM, L.porcelain('merged2')
r=L.vitest('suite_merged2','merged2')
SRC=L.GS+'/qa1007-drafter-parity.test.ts'; REL=GW+'/src/__tests__/qa1007-drafter-parity.test.ts'
dst=wt+'/'+REL; shutil.copyfile(SRC,dst); out=L.W+'/parity_merged2.jsonl'; open(out,'w').close()
L.vitest('parity_merged2','merged2',files=['src/__tests__/qa1007-drafter-parity.test.ts'],env_extra={'QA_OUT':out},save=False)
os.rename(dst, L.W+'/_quarantine/qa1007-drafter-parity.merged2.test.ts')
assert L.porcelain('merged2')==L.FARM, L.porcelain('merged2')
m={json.loads(l)['id']:json.loads(l) for l in open(out)}; h={json.loads(l)['id']:json.loads(l) for l in open(L.W+'/parity_head.jsonl')}
keys=('statusHash','apiStatusHash','simpleHash','statusCode','apiStatusCode','simpleCode','fetchedStatus','nodeEnvSeenInBody')
same=sum(all(m[i][k]==h[i][k] for k in keys) for i in h)
P('parity merged2 (head + develop 93629700c) vs head: identical %d/%d cells'%(same,len(h)))
P('drafter_merged2 end', ts())
