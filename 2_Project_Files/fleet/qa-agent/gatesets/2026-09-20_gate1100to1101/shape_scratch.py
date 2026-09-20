#!/usr/bin/env python3
"""shape_scratch.py — READ-ONLY local-object reads of #1100 / #1101 against develop e47019878: chain, parents, files, trees, blobs, commit messages."""
import subprocess, re
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV='e470198783bcb1ef0eac94780f87579974051423'
PRS=[(1100,'KS-1230','feature/ks-1230-put-apiadminsettings-stores-a-connectors-n97-1','99ce89e741e6c3cad7457af7c91fb6fea86acdff'),
     (1101,'KS-1282','feature/ks-1282-get-apiplatformtenants-the-requiresuperadmin-guard-n99-1','dc40087e756c598ca8b2957da7fbf1ec01945df8')]
def git(*a): return subprocess.run(['git','-C',REPO]+list(a),capture_output=True,text=True)
rp=lambda x: git('rev-parse','--verify','-q',x).stdout.strip()
print('develop tree', rp(DEV+'^{tree}'))
allfiles=[]
for n,t,br,h in PRS:
    files=sorted(git('diff','--name-only',DEV,h).stdout.splitlines()); allfiles+=files
    chain=git('rev-list','--first-parent',DEV+'..'+h).stdout.split()
    npars=[len(git('rev-list','--parents','-n','1',c).stdout.split())-1 for c in chain]
    mb=git('merge-base',DEV,h).stdout.strip()
    print('#%d %s head %s chain %d parents %s merge-base %s (==develop %s) files %d tree %s'%(n,t,h[:9],len(chain),npars,mb[:9],mb==DEV,len(files),rp(h+'^{tree}')))
    for f in files:
        print('    %s\n      develop blob %s -> head blob %s'%(f,rp(DEV+':'+f),rp(h+':'+f)))
    print('    numstat:',git('diff','--numstat',DEV,h).stdout.strip())
    print('    raw:',git('diff','--raw','--no-abbrev',DEV,h).stdout.strip())
    msg=git('log','-1','--format=%s%n%b',h).stdout
    print('    subject:',msg.splitlines()[0])
    print('    Refs lines:',re.findall(r'^Refs\s+(KS-\d+)\s*$',msg,re.M))
    print('    names KS-%d (own PR number): %s'%(n,('KS-%d'%n) in msg))
    print('    ks1215/ks-1215 in message: %s'%bool(re.search(r'ks-?1215',msg,re.I)))
    print('    all KS keys in message:',sorted(set(re.findall(r'KS-\d+',msg))))
print('files', allfiles, 'distinct', len(set(allfiles)), 'overlap', len(allfiles)-len(set(allfiles)))
