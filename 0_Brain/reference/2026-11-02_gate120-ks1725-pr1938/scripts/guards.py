import subprocess,re,sys
R=sys.argv[1]
out=subprocess.check_output(['git','-C',R,'diff','-U0','8f313815f415...pr1938','--','Blockchain/Dev'],text=True)
files=re.findall(r'^\+\+\+ b/(.*)$',out,re.M)
cur=None; ln=0
res=[]
for line in out.splitlines():
    if line.startswith('+++ b/'): cur=line[6:]
    m=re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)',line)
    if m: ln=int(m.group(1))
    elif line.startswith('+') and not line.startswith('+++') and '.issues' in line and cur.endswith('.ts') and '__tests__' not in cur:
        src=subprocess.check_output(['git','-C',R,'show',f'pr1938:{cur}'],text=True).splitlines()
        # search upward for guard
        guard='NONE'
        for i in range(ln-1,max(0,ln-14),-1):
            s=src[i-1] if i-1<len(src) else ''
            if re.search(r'instanceof\s+(z\.)?ZodError|safeParse|\.success|isZodError|ZodError',s):
                guard=f'{i}: {s.strip()[:90]}';break
        res.append((cur.replace('Blockchain/Dev/',''),ln,guard))
        ln+=1
    elif line.startswith("+") and not line.startswith("+++"): ln+=1
for r in res: print(*r,sep=' | ')
