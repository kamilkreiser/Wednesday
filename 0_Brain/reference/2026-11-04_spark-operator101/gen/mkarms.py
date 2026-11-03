import os,shutil,json,subprocess,difflib,re
D='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_spark-operator101/arms'
RC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_KS-1783-originate-l6-real-hash-cells-control'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
inp=json.load(open(RC+'/input.json')); tip=inp['tip']; prod=inp['product_files'][0]
src=subprocess.run(['git','-C',S,'show',f'{tip}:{prod}'],capture_output=True,text=True,check=True).stdout
lines=src.splitlines(True); i=next(k for k,l in enumerate(lines) if l.strip()) ; 
new=lines[:]; new.insert(40,'// arm: product edit\n')
pd=''.join(difflib.unified_diff(lines,new,'a/'+prod,'b/'+prod,n=3))
def mk(name,mut):
    d=f'{D}/{name}'; os.makedirs(d+'/out.md.checker',exist_ok=True)
    for f in ('input.json','checker.out','out.md','round.json'): shutil.copy(f'{RC}/{f}',f'{d}/{f}')
    shutil.copy(f'{RC}/out.md.checker/patch.diff',f'{d}/out.md.checker/patch.diff')
    mut(d)
def addprod(d):
    p=open(d+'/out.md.checker/patch.diff').read(); p=p+pd
    open(d+'/out.md.checker/patch.diff','w').write(p)
    o=open(d+'/out.md').read(); o=o.replace('\n```\n', '\n'+pd.rstrip('\n')+'\n```\n') if False else o
    # rebuild out.md as a single fenced block holding the new patch
    open(d+'/out.md','w').write('```diff\n'+p.rstrip('\n')+'\n```\n')
def addprod_declared(d):
    addprod(d); j=json.load(open(d+'/input.json')); j['test_files'].append(prod); json.dump(j,open(d+'/input.json','w'))
def nonstrictline(d):
    c=open(d+'/checker.out').read(); c=c.replace('PASS A2 the diff applies at the tip (strict)','PASS A2 the diff applies at the tip (--recount --ignore-whitespace accommodation)'); open(d+'/checker.out','w').write(c)
def hdr(d):
    p=open(d+'/out.md.checker/patch.diff').read(); p=re.sub(r'^(@@ -\d+),(\d+)',lambda m:m.group(1)+','+str(int(m.group(2))+1),p,count=1,flags=re.M)
    open(d+'/out.md.checker/patch.diff','w').write(p); open(d+'/out.md','w').write('```diff\n'+p.rstrip('\n')+'\n```\n')
mk('A_product_hunk_appended',addprod); mk('B_product_declared_as_test',addprod_declared); mk('C_a2_not_strict_line',nonstrictline); mk('D_miscounted_hunk_header',hdr)
