import difflib,os,re,subprocess
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
OLD=BR+'ks_1868_o91_p11_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/'
NEW=BR+'ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
import sys
PIN=sys.argv[1]
FP='Blockchain/Dev/services/originate/src/services/email.ts'
tip=subprocess.run(['git','-C',S,'show',PIN+':'+FP],capture_output=True,text=True).stdout
def guard(ind,var):
    return [ind+'let reason: string | null | undefined;',ind+'try {',ind+'  const m = %s.message;'%var,ind+'  reason = m === undefined || m === null ? m : String(m);',ind+'} catch {',ind+"  reason = 'unreadable thrown value';",ind+'}']
L=tip.split('\n')
def rep(n,old,var,newline):
    i=n-1
    assert L[i]==old,(n,L[i])
    return guard('    ',var)+[newline]
edits={
 139:("    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}`);",'err?',"    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${reason}`);"),
 167:("    console.error(`[Email/ACS] Send threw: ${err?.message}`);",'err?',"    console.error(`[Email/ACS] Send threw: ${reason}`);"),
 210:("    console.error(`[Email/SMTP] Failed to send: ${error.message}`);",'error',"    console.error(`[Email/SMTP] Failed to send: ${reason}`);"),
}
out=[]
for i,l in enumerate(L,1):
    if i in edits:
        o,v,nl=edits[i]; assert l==o,(i,l); out+=rep(i,o,v,nl)
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
    for a,b in [("'[Email/ACS] Send threw for ' + TO + ': '","'[Email/ACS] Send threw: '"),("'[Email/SMTP] Failed to send to ' + TO + ': '","'[Email/SMTP] Failed to send: '"),("(line 166)","(line 167)"),("(line 206)","(line 210)")]:
        assert a in t,a; t=t.replace(a,b)
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
sub('DRAFT by Spark operator 91 for Wednesday, 2026-11-03.','DRAFT by Spark operator 105 for Wednesday, 2026-11-09 AEDT. ROUND 2 OF 2: this REBRIEFS held-then-stale READY KS-1868-O91-P11 (round 1), which no longer applies at the pin because KS-1937 (90b500e19, 2026-11-06) removed the recipient address from these log lines; the fix itself is still owed (the three catches are unchanged at the pin). Counter: original + this one rebrief.')
b=re.sub(r'No open PR lists this file or the new test file name \(the 21 open PRs[^)]*\)\)?','No open PR lists this file or the new test file name (42 open PRs / 310 file entries read 2026-11-09 through the GitHub API; planted control services/originate present in 7 entries)',b,count=1)
sub('`4d1ab2cb6574e2b221353ac3a1de56d515711aaf` (origin develop;','`%s` (origin develop;'%PIN)
sub('line 138-139, 165-166 and 205-206','line 138-139, 166-167 and 209-210')
sub('Three catches of this module interpolate','Three catches of this module (the console.error lines no longer carry the recipient, KS-1937) interpolate')
sub('is logged at error level with the recipient and the message','is logged at error level with the message (the recipient is no longer in these lines, KS-1937)')
sub('the product section has FOUR','the product section has FOUR') if False else None
# replace first product diff fence under "The exact change"
ix=b.index('## The exact change'); f0=b.index('```diff\n',ix)+8; f1=b.index('\n```',f0)
b=b[:f0]+prod.rstrip('\n')+b[f1:]
# test fence: replace with fixed test
t0=b.index('```diff\n',b.index('## The test'))+8; t1=b.index('\n```\n',t0)
old_test=b[t0:t1]; new_test=fixtest(old_test); b=b[:t0]+new_test+b[t1:]
sub('`email.ts` lines 130-142, 144-169 and 195-209 read (read whole with `git show` at `4d1ab2cb6574`)','`email.ts` lines 130-142, 145-172 and 196-212 read (read whole with `git show` at `%s`); the same three catches as round 1, with only the log texts changed by KS-1937'%PIN[:12])
b=re.sub(r'- Open PRs: 21 read 2026-11-03[^\n]*','- Open PRs: 42 read 2026-11-09 via the GitHub REST API (pulls?state=open, then pulls/N/files); none lists `Blockchain/Dev/services/originate/src/services/email.ts` or the new test file (310 file entries; planted control services/originate appears in 7 file entries).',b)
open(NEW+'KS-1868.md','w',encoding='utf-8').write(b)
p=open(OLD+'spark.pins',encoding='utf-8').read()
p=p.replace('operator_91_screen','operator_105_rebrief').replace('21_PRs_118_files_read_2026-11-03_by_op91,_planted_control_services/originate_in_10_entries','42_PRs_310_files_read_2026-11-09_by_op105,_planted_control_services/originate_in_7_entries')
open(NEW+'spark.pins','w',encoding='utf-8').write(p)
print(prod)
