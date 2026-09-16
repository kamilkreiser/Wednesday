#!/usr/bin/env python3
"""drafter_static.py — #1005: tsc -p (service program, count __tests__ files in it), an INCLUDING program (tsconfig.qa-including.json:
extends ./tsconfig.json, include src/**/*; placed for the run, moved out by rename), new-error diff base -> head; eslint (flat config) on
the two files at head and verification.ts at base. A planted unused const in the new test file is the positive control for both tools."""
import sys, os, json, re, subprocess
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1005')
from drafterlib import *
NEWT=GWR+'/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts'; V=GWR+'/src/routes/verification.ts'
def tsc(tree, cfg, extra=()):
    gw=T[tree]+'/'+GWR
    p=subprocess.run([T[tree]+'/Blockchain/Dev/node_modules/.bin/tsc','--noEmit','-p',cfg,*extra],cwd=gw,capture_output=True,text=True)
    return p.returncode, p.stdout+p.stderr
INC='{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}\n'
P('drafter_static start', ts())
errs={}
for t in ('base','head'):
    rc,o=tsc(t,'.'); P('tsc -p . tree',t,'rc',rc,'error lines',len(re.findall(r'error TS',o)))
    rc,o=tsc(t,'.',['--listFilesOnly']); P('   service program __tests__ files', sum(1 for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l))
    cfg=T[t]+'/'+GWR+'/tsconfig.qa-including.json'; open(cfg,'w').write(INC)
    rc,o=tsc(t,'tsconfig.qa-including.json',['--listFilesOnly']); tl=[l for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l]
    P('   including program __tests__ files', len(tl), '| ks1073 file listed', any('ks1073-tier-2' in l for l in tl))
    rc,o=tsc(t,'tsconfig.qa-including.json'); e=sorted(set(re.sub(r'\(\d+,\d+\)','(L,C)',l) for l in o.splitlines() if 'error TS' in l)); errs[t]=(rc,e,o)
    P('   including program rc',rc,'distinct errors (line-normalised)',len(e))
    os.rename(cfg, W+'/_quarantine/tsconfig.qa-including.%s.json'%t)
new=[x for x in errs['head'][1] if x not in errs['base'][1]]; gone=[x for x in errs['base'][1] if x not in errs['head'][1]]
P('NEW errors base -> head:', len(new)); [P('   +', x) for x in new]
P('disappeared:', len(gone)); [P('   -', x) for x in gone]
P('head errors in the ks1073 file (raw lines):'); [P('   ', l) for l in errs['head'][2].splitlines() if 'ks1073-tier-2' in l]
open(GS+'/tsc_including.out','w').write('BASE\n'+errs['base'][2]+'\nHEAD\n'+errs['head'][2])
def eslint(tree, files):
    p=subprocess.run([T[tree]+'/Blockchain/Dev/node_modules/.bin/eslint','-f','json',*[T[tree]+'/'+f for f in files]],cwd=T[tree]+'/Blockchain/Dev',capture_output=True,text=True)
    try: j=json.loads(p.stdout)
    except Exception: P('eslint NO JSON rc',p.returncode,p.stderr[-600:]); return
    for f in j: P('eslint', tree, f['filePath'].split('/src/')[-1], 'errors', f['errorCount'], 'warnings', f['warningCount'], sorted({m.get('ruleId') for m in f['messages']}))
eslint('head',[NEWT,V]); eslint('base',[V])
P('== positive control: plant an unused const in the new test file (head), both tools must see it')
pn=sha(T['head']+'/'+NEWT)
edit(T['head']+'/'+NEWT, "const DOC_ID = 'doc-ks1073';\n", "const DOC_ID = 'doc-ks1073';\nconst QA_UNUSED_PLANT = 'a'.repeat(64);\n", [('QA_UNUSED_PLANT',1)])
cfg=T['head']+'/'+GWR+'/tsconfig.qa-including.json'; open(cfg,'w').write(INC)
rc,o=tsc('head','tsconfig.qa-including.json',['--noUnusedLocals']); P('   including tsc --noUnusedLocals sees plant:', 'QA_UNUSED_PLANT' in o)
os.rename(cfg, W+'/_quarantine/tsconfig.qa-including.plant.json')
eslint('head',[NEWT])
restore('head', NEWT, pn)
P('porcelain head', porcelain('head'))
P('drafter_static end', ts())
