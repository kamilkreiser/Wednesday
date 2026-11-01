# Operator 49, task 4 (KS-1841): code_patch2: Dockerfile hunk + MODIFIED ks1823 test + NEW ks1841 fixture test.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP=os.environ.get('GEN_TIP','d7691f35312ea158f043e87a3227e477cccb183d')
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
G='Blockchain/Dev/services/api-gateway/'
DF=G+'Dockerfile'
OLDT=G+'src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts'
NEWT=G+'src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts'
REF=G+'src/__tests__/ks1054-startup-migration-failure-on-health.test.ts'
DIR='ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec'
dfo=mk.rd(DF)
dfn=dfo.replace("""# KS-1823: the host directory can also hold rollback copies of the spec; the gateway reads secuura-api.yaml only.
RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*
""","""# KS-1841 (it replaces KS-1823's two name globs): the host directory can hold backups of the spec under any name; the gateway reads secuura-api.yaml only, so keep that file and nothing else.
RUN find ./docs/openapi -mindepth 1 -maxdepth 1 ! -name secuura-api.yaml -exec rm -rf {} +
""")
assert dfn!=dfo
to=mk.rd(OLDT); tn=to
EDITS=[
("const RM_LINE = 'RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*';",
 "const RM_LINE = 'RUN find ./docs/openapi -mindepth 1 -maxdepth 1 ! -name secuura-api.yaml -exec rm -rf {} +';"),
("""  it('RED KS-1823 R1 the builder stage removes the pre-ks508 style rollback copies', () => {
    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.pre-*'))).toBe(true);
  });

  it('RED KS-1823 R2 the builder stage removes the rollback-dated copies', () => {
    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.rollback-*'))).toBe(true);
  });
""","""  it('RED KS-1823 R1 the builder stage removes every file but the spec with a find that spares secuura-api.yaml by name (KS-1841)', () => {
    expect(DOCKERFILE.some((l) => l.startsWith('RUN find ./docs/openapi') && l.includes('! -name secuura-api.yaml'))).toBe(true);
  });
  // KS-1841: R2 is the other half of R1, the two name globs of the first fix are gone.
  it('RED KS-1823 R2 the two name globs of the first fix are gone (KS-1841)', () => {
    expect(DOCKERFILE.some((l) => l.includes('*.pre-*') || l.includes('*.rollback-*'))).toBe(false);
  });
"""),
("    const rmLines = DOCKERFILE.filter((l) => /\\brm\\b/.test(l) && l.includes('docs/openapi'));",
 "    const rmLines = DOCKERFILE.filter((l) => l.startsWith('RUN rm') && l.includes('docs/openapi'));"),
]
for o,n in EDITS:
    assert tn.count(o)==1,o[:60]; tn=tn.replace(o,n)
import difflib
def udiff2(path,a,b,n=1):
    A=a.splitlines(keepends=True);B=b.splitlines(keepends=True)
    body=list(difflib.unified_diff(A,B,n=n))[2:]
    return ''.join([f'diff --git a/{path} b/{path}\n',f'--- a/{path}\n',f'+++ b/{path}\n']+mk.trim(body))
pd=udiff2(DF,dfo,dfn); td_old=udiff2(OLDT,to,tn)
newsrc=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator49/gen/t4_newtest.ts.txt').read()
td_new=mk.udiff(NEWT,'',newsrc,True)
golden=pd+td_old+td_new
d=BR+DIR; os.makedirs(d,exist_ok=True)
open(d+'/golden.diff','w',encoding='utf-8').write(golden)
open(d+'/spark.pins','w').write("# code_patch2: api-gateway Dockerfile (1 hunk) + MODIFIED ks1823 source-text test + a NEW ks1841 fixture test; ref = shape only; line = first changed Dockerfile line.\ntier=code_patch2\nref=%s\nline=34\nctx=65536\n"%REF)
open(d+'/_parts.txt','w').write('')
os.remove(d+'/_parts.txt')
import json
json.dump(dict(pd=pd.split('\n',1)[1],td_old=td_old.split('\n',1)[1],td_new=td_new.split('\n',1)[1],n_new=len(newsrc.splitlines())),open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator49/gen/t4_parts.json','w'))
print(pd); print(td_old)
