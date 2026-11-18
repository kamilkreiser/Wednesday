import re,sys,subprocess
# usage: scan.py <repo> <base> <head>   -- scans ADDED lines of the diff (and commit messages), case-insensitive
repo,base,head=sys.argv[1:4]
pats={
 'person':r'\b(kam|kamil|kreiser|anupam|baidya|philip|cuff)\b',
 'account/email':r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|\bkamilkreiser\b|\bkreiser\.org\b|\bdatasecau\b',
 'machine':r'\b(macbook|imac|mac-?studio|laptop-dev|devmaster)\b|\.local\b',
 'drive/volume':r'/volumes/|\bt9\b|laptop-dev|devmaster',
 'home path':r'/users/[a-z]|/home/[a-z]|c:\\\\users|/private/tmp/claude-|claude-501',
 'client':r'\b(datasec|secuura|nexusai|cypherkey|mypki)\b',
 'seat/agent name':r'\b(friday|wednesday|tuesday)\b',
}
diff=subprocess.run(['git','-C',repo,'diff','-U0',base,head],capture_output=True,text=True).stdout
msgs=subprocess.run(['git','-C',repo,'log','--format=%B',f'{base}..{head}'],capture_output=True,text=True).stdout
f=None;ln=0;tot={}
for line in diff.splitlines():
    if line.startswith('+++ '): f=line[6:]; continue
    m=re.match(r'@@ -\S+ \+(\d+)',line)
    if m: ln=int(m.group(1)); continue
    if line.startswith('+'):
        for c,p in pats.items():
            if re.search(p,line[1:],re.I):
                print(f'{f}:{ln}\t{c}'); tot[c]=tot.get(c,0)+1
        ln+=1
for i,line in enumerate(msgs.splitlines()):
    for c,p in pats.items():
        if re.search(p,line,re.I): print(f'commit-msg:{i+1}\t{c}'); tot[c]=tot.get(c,0)+1
print('TOTAL',sum(tot.values()),tot)
