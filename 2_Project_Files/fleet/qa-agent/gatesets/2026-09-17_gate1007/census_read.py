#!/usr/bin/env python3
"""census_read.py — #1007 Q3: the dead-estate grep (ashypond|westeurope|secuura-staging-) on the base and head blobs of system-status.ts,
counted as LINES (grep -c semantics) and as OCCURRENCES, every hit READ and classified by the line's own text (not by count).
Control: /usr/bin/grep -c -E on the same files must equal the line count."""
import re, subprocess, datetime
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007'
RX=re.compile(r'ashypond|westeurope|secuura-staging-')
print('census_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
def classify(line):
    if re.search(r"getServiceUrl\('[A-Z0-9_]+', \d+, 'secuura-staging-[a-z0-9-]+'\)", line): return 'CALL-SITE ARG (3rd, unused at head)'
    if 'az containerapp revision restart' in line: return 'REMEDIATION HINT (troubleshooting.commands, served in /system/status body)'
    if re.search(r"return `https://\$\{azureServiceName\}\.internal\.ashypond", line): return 'HELPER STAGING RETURN (Part A removes)'
    if re.search(r"'https://secuura-staging-(issuer|verifier|admin)\.ashypond", line): return 'PORTAL STAGING LITERAL (Part B removes)'
    return 'UNCLASSIFIED'
for tree in ('base','head'):
    p=GS+'/src/system-status.%s.ts'%tree; lines=open(p).read().split('\n')
    hits=[(i+1,l) for i,l in enumerate(lines) if RX.search(l)]
    occ=sum(len(RX.findall(l)) for _,l in hits)
    g=subprocess.run(['/usr/bin/grep','-c','-E','ashypond|westeurope|secuura-staging-',p],capture_output=True,text=True).stdout.strip()
    ctl=subprocess.run(['/usr/bin/grep','-c','-E','getServiceUrl',p],capture_output=True,text=True).stdout.strip()
    print('== %s: hit LINES %d (grep -c control %s; positive control grep -c getServiceUrl %s) | OCCURRENCES %d'%(tree,len(hits),g,ctl,occ))
    by={}
    for n,l in hits:
        c=classify(l); by.setdefault(c,[]).append(n)
        print('   :%-4d %-72s | %s'%(n,c,l.strip()[:150]))
    for c,ns in by.items(): print('   CLASS %-72s lines %d: %s'%(c,len(ns),ns))
