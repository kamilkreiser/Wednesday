import subprocess, sys, os, re, hashlib
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night'
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate133-ks1868-pr1951/repo'
def blocks(text):
    m=re.search(r'```diff\n(.*?)\n```', text, re.S); return m.group(1)
def per_file(d):
    out={}; cur=None
    for ln in d.split('\n'):
        if ln.startswith('diff --git'):
            cur=ln.split(' b/')[-1]; out[cur]=[]
        elif cur is not None: out[cur].append(ln)
    return out
def body(lines):
    # +/-/space lines only, drop headers, index, @@ line numbers
    return [l for l in lines if (l[:1] in '+- ' and not l.startswith('+++') and not l.startswith('---'))]
for g in ['G1','G2']:
    f=[x for x in os.listdir(N) if 'O80-'+g in x][0]
    pf=per_file(blocks(open(os.path.join(N,f)).read()))
    for path,lines in pf.items():
        pr=subprocess.run(['git','-C',R,'diff','1584c0f0ff808fddf35245bee41b6b5f9231054c','6db96b6fe07aa64e44d09ac9b8034488fb07063f','--',path],capture_output=True,text=True).stdout.rstrip('\n').split('\n')
        prf=per_file('\n'.join(pr))[path]
        a=body(lines); b=body(prf)
        ha=[re.sub(r'^@@ -\d+(,\d+)? \+\d+(,\d+)? @@','@@',l) for l in lines if l.startswith('@@')]
        hb=[re.sub(r'^@@ -\d+(,\d+)? \+\d+(,\d+)? @@','@@',l) for l in prf if l.startswith('@@')]
        print(g, path.split('/')[-1], 'held_lines',len(a),'pr_lines',len(b),'EQUAL' if a==b else 'DIFFER', 'sha_held',hashlib.sha256('\n'.join(a).encode()).hexdigest()[:12],'sha_pr',hashlib.sha256('\n'.join(b).encode()).hexdigest()[:12], 'hunk_ctx_equal', ha==hb)
        hn=[l for l in lines if l.startswith('@@')]; hp=[l for l in prf if l.startswith('@@')]
        print('   held hunks', hn); print('   pr   hunks', hp)
        if a!=b:
            import difflib; print('\n'.join(list(difflib.unified_diff(a,b,lineterm=''))[:40]))
