#!/usr/bin/env python3
"""drafter_static.py — #1007: tsc -p . (the service program; count __tests__ files in it), an INCLUDING program (tsconfig.qa-including.json:
extends ./tsconfig.json, include src/**/*; placed for the run, moved out by rename), new-error diff base -> head; eslint (flat config) on
the three files at head and system-status.ts at base. Positive controls: (1) the parameter renamed BACK to azureServiceName at head must make
tsc -p report TS6133 (noUnusedParameters is live); (2) an unused const planted in ks864a must be seen by the including tsc and by eslint."""
import sys, os, json, re, subprocess
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007')
from drafterlib import *
NA=GWR+'/src/__tests__/ks864a-dead-estate-helper.test.ts'; NB=GWR+'/src/__tests__/ks864b-dead-estate-portals.test.ts'; SS=GWR+'/src/routes/system-status.ts'
def tsc(tree, cfg, extra=()):
    p=subprocess.run([T[tree]+'/Blockchain/Dev/node_modules/.bin/tsc','--noEmit','-p',cfg,*extra],cwd=T[tree]+'/'+GWR,capture_output=True,text=True)
    return p.returncode, p.stdout+p.stderr
INC='{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}\n'
P('drafter_static start', ts())
errs={}
for t in ('base','head'):
    assert porcelain(t)==FARM, porcelain(t)
    rc,o=tsc(t,'.'); P('tsc -p . tree',t,'rc',rc,'error lines',len(re.findall(r'error TS',o)))
    rc,o=tsc(t,'.',['--listFilesOnly']); P('   service program __tests__ files', sum(1 for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l), '| system-status.ts listed', any(l.endswith('routes/system-status.ts') for l in o.splitlines()))
    cfg=T[t]+'/'+GWR+'/tsconfig.qa-including.json'; open(cfg,'w').write(INC)
    rc,o=tsc(t,'tsconfig.qa-including.json',['--listFilesOnly']); tl=[l for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l]
    P('   including program __tests__ files', len(tl), '| ks864a listed', any('ks864a-dead-estate-helper' in l for l in tl), '| ks864b listed', any('ks864b-dead-estate-portals' in l for l in tl))
    rc,o=tsc(t,'tsconfig.qa-including.json'); e=sorted(set(re.sub(r'\(\d+,\d+\)','(L,C)',l) for l in o.splitlines() if 'error TS' in l)); errs[t]=(rc,e,o)
    P('   including program rc',rc,'error lines',len(re.findall(r'error TS',o)),'distinct (line-normalised)',len(e))
    os.rename(cfg, W+'/_quarantine/tsconfig.qa-including.%s.json'%t)
new=[x for x in errs['head'][1] if x not in errs['base'][1]]; gone=[x for x in errs['base'][1] if x not in errs['head'][1]]
P('NEW distinct errors base -> head:', len(new)); [P('   +', x) for x in new]
P('disappeared:', len(gone)); [P('   -', x) for x in gone]
P('head raw error lines in the ks864 files:'); [P('   ', l) for l in errs['head'][2].splitlines() if 'ks864' in l]
P('head raw error lines in system-status.ts:', sum(1 for l in errs['head'][2].splitlines() if 'system-status' in l))
open(GS+'/tsc_including.out','w').write('BASE\n'+errs['base'][2]+'\nHEAD\n'+errs['head'][2])
def eslint(tree, files):
    p=subprocess.run([T[tree]+'/Blockchain/Dev/node_modules/.bin/eslint','-f','json',*[T[tree]+'/'+f for f in files]],cwd=T[tree]+'/Blockchain/Dev',capture_output=True,text=True)
    try: j=json.loads(p.stdout)
    except Exception: P('eslint NO JSON rc',p.returncode,p.stderr[-600:]); return
    for f in j: P('eslint', tree, f['filePath'].split('/src/')[-1], 'errors', f['errorCount'], 'warnings', f['warningCount'], sorted({str(m.get('ruleId')) for m in f['messages']}))
eslint('head',[NA,NB,SS]); eslint('base',[SS])
P('== control 1: rename the parameter BACK (unused azureServiceName) at head; tsc -p . must report TS6133')
ps=sha(T['head']+'/'+SS)
edit(T['head']+'/'+SS, "localPort: number, _azureServiceName?: string): string => {", "localPort: number, azureServiceName?: string): string => {", [('_azureServiceName',0)])
rc,o=tsc('head','.'); P('   tsc -p . rc', rc, '| TS6133 azureServiceName reported:', bool(re.search(r"system-status\.ts\(\d+,\d+\): error TS6133: 'azureServiceName'", o)), '|', [l for l in o.splitlines() if 'error TS' in l][:2])
restore('head', SS, ps)
rc,o=tsc('head','.'); P('   after restore tsc -p . rc', rc)
P('== control 2: plant an unused const in ks864a (head); the including tsc and eslint must both see it')
pa=sha(T['head']+'/'+NA)
edit(T['head']+'/'+NA, "const savedEnv = { ...process.env };\n", "const savedEnv = { ...process.env };\nconst QA_UNUSED_PLANT = 'x';\n", [('QA_UNUSED_PLANT',1)])
cfg=T['head']+'/'+GWR+'/tsconfig.qa-including.json'; open(cfg,'w').write(INC)
rc,o=tsc('head','tsconfig.qa-including.json'); P('   including tsc sees plant (TS6133):', 'QA_UNUSED_PLANT' in o)
os.rename(cfg, W+'/_quarantine/tsconfig.qa-including.plant.json')
eslint('head',[NA])
restore('head', NA, pa)
P('porcelain head', porcelain('head'))
P('drafter_static end', ts())
