import re,subprocess
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908/repo'
d=subprocess.run(['git','-C',R,'diff','-U0','refs/gate/pr1908^','refs/gate/pr1908','--','Blockchain/Dev/services/security/src/index.ts'],capture_output=True,text=True).stdout
hunks=re.split(r'^@@.*$',d,flags=re.M)[1:]
heads=re.findall(r'^@@.*$',d,flags=re.M)
print('hunks',len(hunks),heads)
EXPR='err instanceof Error ? err.message : String(err)'
shapes=[]
for i,hk in enumerate(hunks):
    minus=[l[1:] for l in hk.splitlines() if l.startswith('-')]
    plus=[l[1:] for l in hk.splitlines() if l.startswith('+')]
    print(f'hunk {i}: -{len(minus)} +{len(plus)}')
    for l in minus: print('  -',l)
    for l in plus: print('  +',l)
    guard=[l.strip() for l in plus[:6]]
    ok_guard=guard==['let reason: string;','try {',f'reason = {EXPR};','} catch {',"reason = 'unreadable thrown value';",'}']
    ok_swap=len(minus)==1 and len(plus)==7 and minus[0].replace(f'error: {EXPR},','error: reason,')==plus[6]
    print('  guard block exact:',ok_guard,' removed line == added log line with only error: EXPR -> reason:',ok_swap)
    shapes.append([len(l)-len(l.lstrip()) for l in plus])
print('indent shapes',shapes, 'relative-identical:', [ [x-s[0] for x in s] for s in shapes][0]==[[x-s[0] for x in s] for s in shapes][1])
st=subprocess.run(['git','-C',R,'diff','--shortstat','refs/gate/pr1908^','refs/gate/pr1908','--','Blockchain/Dev/services/security/src/index.ts'],capture_output=True,text=True).stdout
print('index.ts shortstat:',st.strip())
print('product files in diff (non-test, non-fragment):',[f for f in subprocess.run(['git','-C',R,'diff','--name-only','refs/gate/pr1908^','refs/gate/pr1908'],capture_output=True,text=True).stdout.split() if '__tests__' not in f and 'fragments' not in f and f.strip()])
print('--- paired per site (U0 splits each site into guard-insert + log-line swap)')
for s,(g,sw) in enumerate([(0,1),(2,3)]):
    plus=[l[1:] for l in hunks[g].splitlines() if l.startswith('+')]
    m=[l[1:] for l in hunks[sw].splitlines() if l.startswith('-')]; p=[l[1:] for l in hunks[sw].splitlines() if l.startswith('+')]
    print(f'site {s+1}: guard exact', [l.strip() for l in plus]==['let reason: string;','try {',f'reason = {EXPR};','} catch {',"reason = 'unreadable thrown value';",'}'],
          '| relative indent',[len(l)-len(l.lstrip())-(len(plus[0])-len(plus[0].lstrip())) for l in plus],
          '| swap is exactly EXPR->reason:', len(m)==1 and len(p)==1 and m[0].replace(f'error: {EXPR},','error: reason,')==p[0])
