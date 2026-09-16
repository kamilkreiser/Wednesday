#!/usr/bin/env python3
"""drafter_realapp.py — #1007 Q9: run the real-app probe at head (probe copied in, moved out by rename). Prints each route's status code,
fetch hits (the handler's own witness), top-level keys and per-entry keys, and environment.env."""
import sys, os, json, shutil
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007')
from drafterlib import *
SRC=GS+'/qa1007-drafter-realapp.test.ts'; REL=GWR+'/src/__tests__/qa1007-drafter-realapp.test.ts'
P('drafter_realapp start', ts())
assert porcelain('head')==FARM, porcelain('head')
dst=T['head']+'/'+REL; shutil.copyfile(SRC, dst); out=W+'/realapp_head.jsonl'; open(out,'w').close()
r=vitest('realapp_head','head',files=['src/__tests__/qa1007-drafter-realapp.test.ts'],env_extra={'QA_OUT':out},save=False)
os.rename(dst, W+'/_quarantine/qa1007-drafter-realapp.head.test.ts')
assert porcelain('head')==FARM, porcelain('head')
for l in open(out):
    d=json.loads(l); P('== NODE_ENV', d['nodeEnv'])
    for p in ('/system/status','/api/system/status','/system/status/simple','/api/documents'):
        x=d[p]; P('   %-24s code %s fetchHits %s env %s topKeys %s serviceEntryKeys %s dependencyEntryKeys %s | %s'%(p,x['code'],x['fetchHits'],x['environmentEnv'],x['topKeys'],x['serviceEntryKeys'],x['dependencyEntryKeys'], x['bodyHead'][:70] if x['code']>=400 else ''))
P('drafter_realapp end', ts())
