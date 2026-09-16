#!/usr/bin/env python3
"""ready_vs_head.py — #1007: the seat's claim that each committed test file is byte-identical to its READY '+' lines, and that the product
hunks match what the READY proposed. Reads the local READY diff.md files and the head blobs saved by git_read.sh."""
import datetime, difflib, re
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
print('ready_vs_head', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
def newfile_plus(path):
    L=open(path,encoding='utf-8').read().split('\n'); out=[]; on=False; hdr=None
    for l in L:
        if l.startswith('+++ ') and '__tests__' in l: on=True; continue
        if on and l.startswith('@@'): hdr=l; continue
        if on and hdr:
            if l.startswith('+'): out.append(l[1:])
            else: break
    return hdr, out
for part, ready, head in (('A', 'READY_KS-864-PartA-helper_ornith35b-q8_PASS-7of7_2026-09-15.diff.md', 'ks864a-dead-estate-helper.test.ts'),
                          ('B', 'READY_KS-864-PartB-portals_ornith35b-q4_PASS-7of7_2026-09-15.diff.md', 'ks864b-dead-estate-portals.test.ts')):
    hdr, plus = newfile_plus(N+ready); h=open(GS+'/src/'+head,encoding='utf-8').read()
    hl=h.split('\n');
    if hl and hl[-1]=='': hl=hl[:-1]
    print('Part %s: READY hunk header %r, READY + lines %d, head file lines %d, identical %s'%(part, hdr, len(plus), len(hl), plus==hl))
    if plus!=hl:
        for d in list(difflib.unified_diff(plus, hl, 'READY+', 'head', lineterm='', n=0))[:30]: print('   ', d[:160])
