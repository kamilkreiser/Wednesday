#!/usr/bin/env python3
"""drafter_setup.py — #1007 drafter substrate. Clone --shared by SHA into a fresh mktemp -d in THIS drafter's scratchpad; worktrees IN THE
CLONE: base = develop 40fe4db69 (the PR parent), head = b28ed490a, merged = head + a LOCAL --no-ff merge of develop 40fe4db69 (never pushed;
tree hash compared to head's). Farm node_modules per ENTRY with @secuura relinked INTO each tree; build packages/shared dist per tree.
Write verbs only inside the clone. Never rm."""
import subprocess, os, tempfile, datetime, json
SCR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fa385b47-2d6c-4cbd-b671-2860bf4a1518/scratchpad'
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007'
SHA=dict(base='40fe4db6963cd11dba06bd46e0b00af39e68ef3a', head='b28ed490ada70df2056763f4512c98443285a694', dev='40fe4db6963cd11dba06bd46e0b00af39e68ef3a')
DEV='Blockchain/Dev'; GW=DEV+'/services/api-gateway'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def run(c,cwd=None): p=subprocess.run(c,cwd=cwd,capture_output=True,text=True); return p.returncode,p.stdout,p.stderr
P('drafter_setup', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc,o,e=run(['git','-C',REPO,'worktree','list','--porcelain']); P('source checkout worktree entries BEFORE', o.count('worktree '))
os.makedirs(SCR, exist_ok=True)
W=tempfile.mkdtemp(prefix='gate1007_draft_', dir=SCR); C=W+'/clone'; P('workdir', W)
rc,o,e=run(['git','clone','--shared','--no-checkout','--quiet',REPO,C]); P('clone rc',rc,e.strip()[:200]); assert rc==0
rc,o,e=run(['git','-C',C,'checkout','--quiet','--detach',SHA['head']]); P('clone checkout head rc',rc); assert rc==0
G=['git','-c','user.name=qa-drafter','-c','user.email=qa-drafter@invalid','-C']
trees={}
for name,base,merges in (('base','base',[]),('head','head',[]),('merged','head',['dev'])):
    wt=W+'/wt_'+name
    rc,o,e=run(['git','-C',C,'worktree','add','--detach','--quiet',wt,SHA[base]]); assert rc==0, e
    for m in merges:
        rc,o,e=run(G+[wt,'merge','--no-ff','--no-edit','-m','qa drafter local merge '+m,SHA[m]]); P('  merge',name,'<-',m,SHA[m][:9],'rc',rc,(o.strip().splitlines() or [''])[-1][:160]); assert rc==0
    rc,o,e=run(['git','-C',wt,'rev-list','--parents','-n','1','HEAD']); P('tree',name,'HEAD+parents',o.strip())
    rc,o,e=run(['git','-C',wt,'rev-parse','HEAD^{tree}','HEAD:'+DEV+'/packages/shared','HEAD:'+GW]); P('   root/shared/api-gateway tree hashes',o.split())
    trees[name]=wt
src_dev_nm=os.path.join(REPO,DEV,'node_modules'); entries=sorted(os.listdir(src_dev_nm))
def farm(root):
    os.symlink(os.path.join(REPO,'node_modules'), os.path.join(root,'node_modules'))
    dnm=os.path.join(root,DEV,'node_modules'); os.mkdir(dnm); rel=0
    for ent in entries:
        s=os.path.join(src_dev_nm,ent)
        if ent=='@secuura':
            os.mkdir(os.path.join(dnm,ent))
            for sub in sorted(os.listdir(s)):
                t=os.readlink(os.path.join(s,sub)); os.symlink(os.path.normpath(os.path.join(dnm,ent,t)), os.path.join(dnm,ent,sub))
        elif os.path.islink(s) and not os.path.isabs(os.readlink(s)):
            os.symlink(os.path.normpath(os.path.join(dnm,os.readlink(s))), os.path.join(dnm,ent)); rel+=1
        else: os.symlink(s, os.path.join(dnm,ent))
    for r in (GW+'/node_modules', DEV+'/packages/shared/node_modules'):
        if os.path.isdir(os.path.join(REPO,r)): os.symlink(os.path.join(REPO,r), os.path.join(root,r))
    return rel
for n,wt in trees.items():
    P('farm',n,'relative links rewritten',farm(wt))
    t0=datetime.datetime.now(); sh=wt+'/'+DEV+'/packages/shared'
    rc,o,e=run([wt+'/'+DEV+'/node_modules/.bin/tsc','-p','.'],cwd=sh); P('  shared dist build',n,'rc',rc,'secs',(datetime.datetime.now()-t0).seconds,(o+e).strip()[-300:])
    rc,o,e=run(['node','-e',"const p=require.resolve('@secuura/shared');const r=require('fs').realpathSync(p);console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', require('vitest/package.json').version, require('typescript/package.json').version, process.version)", wt],cwd=wt+'/'+GW)
    P('  resolve @secuura/shared from',n,'api-gateway:',o.strip(),e.strip()[:300])
rc,o,e=run(['git','-C',REPO,'worktree','list','--porcelain']); P('source checkout worktree entries AFTER', o.count('worktree '))
json.dump({'W':W,'C':C,'trees':trees},open(GS+'/drafter_paths.json','w'),indent=1)
