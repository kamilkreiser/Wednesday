import difflib,os,re,subprocess
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
OLD=BR+'ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/'
NEW=BR+'ks_1868_o105_p2_originate_certifications_init_repo_catch_guard_message/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
import sys
PIN=sys.argv[1]
FP='Blockchain/Dev/services/originate/src/routes/certifications.ts'
tip=subprocess.run(['git','-C',S,'show',PIN+':'+FP],capture_output=True,text=True).stdout
L=tip.split('\n')
OLDL="initRepo().catch((err) => logger.error('Failed to init repo', { error: err instanceof Error ? err.message : String(err) }));"
NEWL=["initRepo().catch((err) => {","  let reason: string;","  try {","    reason = err instanceof Error ? err.message : String(err);","  } catch {","    reason = 'unreadable thrown value';","  }","  logger.error('Failed to init repo', { error: reason });","});"]
out=[]
for i,l in enumerate(L,1):
    if i==70:
        assert l==OLDL,l; out+=NEWL
    else: out.append(l)
new='\n'.join(out)
ud=list(difflib.unified_diff(tip.splitlines(True),new.splitlines(True),n=3))
hunks=''.join(ud[2:])
pre='--- a/%s\n+++ b/%s\n'%(FP,FP)
prod=pre+hunks
os.makedirs(NEW,exist_ok=True)
# golden
g=open(OLD+'golden.diff',encoding='utf-8').read()
gi=g.index('diff --git a/Blockchain/Dev/services/originate/src/__tests__/')
test_sec=g[gi:]
def fixtest(t):
    return t
test_sec=fixtest(test_sec)
golden='diff --git a/%s b/%s\n'%(FP,FP)+prod+test_sec
open(NEW+'golden.diff','w',encoding='utf-8').write(golden)
# brief
b=open(OLD+'KS-1868.md',encoding='utf-8').read()
def sub(a,c,count=1):
    global b
    assert b.count(a)>=1,a[:60]
    b=b.replace(a,c)
sub('DRAFT by Spark operator 90 for Wednesday, 2026-11-03.','DRAFT by Spark operator 105 for Wednesday, 2026-11-09 AEDT. ROUND 2 OF 2: this REBRIEFS stale READY KS-1868-O90-P3 (round 1), which no longer applies at the pin (the hunk context drifted; the catch at line 70 is unchanged and the new test file is still absent at the tip, so the fix is still owed). Counter: original + this one rebrief.')
b=re.sub(r'\(the 21 open PRs[^)]*\)\)?','(42 open PRs / 310 file entries read 2026-11-09 through the GitHub API; planted control services/originate present in 7 entries)',b,count=1)
sub('`2d3b3bb3d3865689e3cad843f9ebb90a2f606960` (origin develop;','`%s` (origin develop;'%PIN)
sub('(read whole with `git show` at `2d3b3bb3d386`)','(read whole with `git show` at `%s`)'%PIN[:12])
b=re.sub(r'- Open PRs: 21 read 2026-11-03[^\n]*','- Open PRs: 42 read 2026-11-09 via the GitHub REST API (pulls?state=open, then pulls/N/files); none lists `Blockchain/Dev/services/originate/src/routes/certifications.ts` or the new test file (310 file entries; planted control services/originate appears in 7 file entries).',b)
# replace first product diff fence under "The exact change"
ix=b.index('## The exact change'); f0=b.index('```diff\n',ix)+8; f1=b.index('\n```',f0)
b=b[:f0]+prod.rstrip('\n')+b[f1:]
# test fence: replace with fixed test
t0=b.index('```diff\n',b.index('## The test'))+8; t1=b.index('\n```\n',t0)
old_test=b[t0:t1]; new_test=fixtest(old_test); b=b[:t0]+new_test+b[t1:]
b=re.sub(r'- Open PRs: 21 read 2026-11-03[^\n]*','- Open PRs: 42 read 2026-11-09 via the GitHub REST API (pulls?state=open, then pulls/N/files); none lists `Blockchain/Dev/services/originate/src/services/email.ts` or the new test file (310 file entries; planted control services/originate appears in 7 file entries).',b)
open(NEW+'KS-1868.md','w',encoding='utf-8').write(b)
p=open(OLD+'spark.pins',encoding='utf-8').read()
p=p.replace('KS-1868_site_screened_by_operator_90','KS-1868_site_rebriefed_by_operator_105').replace('21_PRs_268_files_read_2026-11-03_by_op89,_planted_control_services/originate_in_14_entries','42_PRs_310_files_read_2026-11-09_by_op105,_planted_control_services/originate_in_7_entries')
open(NEW+'spark.pins','w',encoding='utf-8').write(p)
print(prod)
