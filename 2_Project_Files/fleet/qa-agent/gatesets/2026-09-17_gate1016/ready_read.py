import re, hashlib, subprocess, datetime, difflib
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
READY='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1072_ornith35b-q4_PASS-7of7_2026-09-15.diff.md'
print('ready_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
t=open(READY).read()
print('READY sha256', hashlib.sha256(t.encode()).hexdigest()[:16], 'bytes', len(t))
body=t.split('```diff\n',1)[1].rsplit('```',1)[0]
files=re.split(r'(?m)^(?=--- )', body)
files=[f for f in files if f.strip()]
print('file sections', len(files))
secs={}
for f in files:
    name=f.splitlines()[1]
    hunks=re.findall(r'(?m)^@@ .*$', f)
    lines=f.splitlines()
    # body lines after first @@
    i=[k for k,l in enumerate(lines) if l.startswith('@@')][0]
    b=lines[i+1:]
    plus=sum(1 for l in b if l.startswith('+')); minus=sum(1 for l in b if l.startswith('-')); ctx=sum(1 for l in b if l.startswith(' '))
    other=sum(1 for l in b if not l[:1] in '+- ')
    print(name, '| headers', hunks, '| + %d - %d ctx %d other %d' % (plus, minus, ctx, other))
    secs[name]=b
# control: the header's declared new-count
T=[k for k in secs if 'ks1072' in k][0]
ready_test='\n'.join(l[1:] for l in secs[T])+'\n'
print('READY test content lines', ready_test.count('\n'), 'sha256', hashlib.sha256(ready_test.encode()).hexdigest()[:16])
head_test=open(G+'/src/ks1072_head.test.ts').read()
print('HEAD test lines', head_test.count('\n'), 'sha256', hashlib.sha256(head_test.encode()).hexdigest()[:16])
d=list(difflib.unified_diff(ready_test.splitlines(), head_test.splitlines(), 'READY-test', 'head-test', n=0, lineterm=''))
print('READY->head test delta: +%d -%d' % (sum(1 for l in d if l.startswith('+') and not l.startswith('+++')), sum(1 for l in d if l.startswith('-') and not l.startswith('---'))))
open(G+'/ready_to_head_test.diff','w').write('\n'.join(d)+'\n')
# product hunk: READY + lines present verbatim & contiguous at head?
P=[k for k in secs if 'verification.ts' in k][0]
rp=[l[1:] for l in secs[P] if l.startswith('+')]
rm=[l[1:] for l in secs[P] if l.startswith('-')]
hv=open(G+'/src/verification_head.ts').read().splitlines()
bv=open(G+'/src/verification_base.ts').read().splitlines()
def find(block, lines):
    return [i+1 for i in range(len(lines)-len(block)+1) if lines[i:i+len(block)]==block]
print('READY + block (%d lines) found at head lines' % len(rp), find(rp, hv), '| at base', find(rp, bv))
print('READY - block (%d lines) found at base lines' % len(rm), find(rm, bv), '| at head', find(rm, hv))
ctx=[l[1:] for l in secs[P] if l.startswith(' ')]
print('READY context first line found at base', find(ctx[:1], bv), 'READY hunk header', [l for l in body.splitlines() if l.startswith('@@') and '285' in l])
