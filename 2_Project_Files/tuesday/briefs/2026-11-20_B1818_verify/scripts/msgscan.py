import re,sys,subprocess
_STD='/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md'
NAMES=[w.strip() for w in re.search(r'Ban list: ([^.]*?), plus',open(_STD,encoding='utf-8').read()).group(1).split(',')]
def scan(t):
    hits=[]
    for n in NAMES:
        for m in re.finditer(r'(?<![A-Za-z])'+n+r'(?![a-z])',t): hits.append(('name',n))
    for m in re.finditer(r'\b[Bb]\d{3,4}\b',t): hits.append(('brief',m.group()))
    for m in re.finditer(r'\b(SEAT|seat)-?[A-Z]?\d+',t): hits.append(('seat',m.group()))
    for m in re.finditer(r'\b[A-Z][A-Z0-9]+-\d+\b',t): hits.append(('ticket',m.group()))
    for m in re.finditer(r'\bC-\d+\b',t): hits.append(('card',m.group()))
    for m in re.finditer(r'[​-‏‪-‮⁠-⁤﻿]',t): hits.append(('Cf',hex(ord(m.group()))))
    trailers=len(re.findall(r'^Co-Authored-By: ',t,re.M))
    return hits,trailers
if __name__=='__main__':
    t=open(sys.argv[1],encoding='utf-8').read() if len(sys.argv)>1 and sys.argv[1]!='-' else sys.stdin.read()
    h,tr=scan(t); print('hits',len(h),h,'trailers',tr)
    hc,_=scan(t+'\nplanted _by_Paul_ B1803 SEAT-C106 PCOMP-66\n'); print('control hits',len(hc))
