# P2 provenance: compare PR 1911's P2 (login) product hunk change lines with the golden.diff and with the -r2 and first-round section_1.diff; also the test file.
import glob,hashlib,re,subprocess
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo'
RU='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_p2_auth_login_publish_event_unreadable_throw'
B=glob.glob('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o50_p2_*')
print('brief dirs:',B)
F='Blockchain/Dev/services/auth/src/routes/auth.ts'
sh=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
d=subprocess.run(['git','-C',R,'diff','-U0','refs/gate/develop','refs/gate/pr1911','--',F],capture_output=True,text=True).stdout
h=re.split(r'^(?=@@)',d,flags=re.M)[1:]
login=[l for l in h[1].splitlines()[1:] if l[:1] in '+-']   # hunk 2 in file order = login (landing check in sections.log)
def chg(text,path=None):
    out=[];cur=None
    for l in text.splitlines():
        m=re.match(r'^\+\+\+ b/(\S+)',l)
        if m: cur=m.group(1); continue
        if l.startswith('---') or l.startswith('diff ') or l.startswith('@@'): continue
        if l[:1] in '+-' and (path is None or cur==path): out.append(l)
    return out
src={'golden':B[0]+'/golden.diff' if B else None,'r2_section_1':RU+'-r2/out.md.checker/section_1.diff','round1_section_1':RU+'/out.md.checker/section_1.diff',
     'r2_patch':RU+'-r2/out.md.checker/patch.diff','round1_patch':RU+'/out.md.checker/patch.diff'}
for k,p in src.items():
    if not p: print(k,'MISSING'); continue
    t=open(p).read(); c=chg(t,F) if 'golden' in k or 'patch' in k else chg(t)
    print(f'{k:18} sha256 {sh(p)[:12]}  product change lines {len(c)}  == PR login hunk: {"EQUAL" if c==login else "DIFFERENT"}')
# test file: golden vs r2 section_2 vs PR file
T='Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts'
pr=subprocess.run(['git','-C',R,'show','refs/gate/pr1911:'+T],capture_output=True,text=True).stdout.splitlines()
for k,p in [('golden',src['golden']),('r2_section_2',RU+'-r2/out.md.checker/section_2.diff'),('round1_section_2',RU+'/out.md.checker/section_2.diff')]:
    t=open(p).read(); body=[l[1:] for l in chg(t,T if k=='golden' else None) if l.startswith('+')]
    print(f'{k:18} test file == PR test file: {"EQUAL" if body==pr else "DIFFERENT"} ({len(body)} vs {len(pr)} lines)')
