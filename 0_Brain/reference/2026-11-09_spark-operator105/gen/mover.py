import json,os,re,shutil,sys
O=sys.argv[1]
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
Q=N+'_quarantine_2026-11-09/'
rows=json.load(open(O+'/ready_all3.json')); ts=json.load(open(O+'/ticket_states.json'))
os.makedirs(Q+'spent',exist_ok=True); os.makedirs(Q+'stale',exist_ok=True)
before=len([f for f in os.listdir(N) if f.startswith('READY_')])
spent=[];stale=[]
for r in rows:
    if r['pr'] or r['live']: continue
    if r['cls']=='REV-OK': spent.append(r)
    elif r['cls'] in('NEITHER','NODIFF'): stale.append(r)
def clean(s): return re.sub(r'\s+',' ',s or '').replace('|','/')
L=['','## Operator 105 sweep, 2026-11-09 00:3x AEDT (Spark operator 105 for Wednesday; moved under her commission). Reversible: move back.',
 'Pin: develop 7eda23b34d3b7a413ca8f9c0945c7843708ce9f4 (ls-remote 00:2x). Instrument = operator 104\'s: first ```diff fence, git apply --cached --check forward then -R, against a temp index of the pin tree (0_Brain/reference/2026-11-09_spark-operator105/gen/ready_all.py; results ready_all.json). Extension: a READY with no fence but a CANONICAL PATCH path that still exists was checked from that file. FWD-OK, open-PR-named and live-queue READYs were NOT moved.','',
 '### spent/ (REV-OK: the diff is already in the tip). Row: file | class | landing commit (sha subject) | how measured','']
for r in spent:
    sha,subj=r['land'][0].split(' ',1)
    L.append(f"- {r['name']} | REV-OK | {sha} {clean(subj)} | reverse apply --check OK at pin; landing by {clean(r['land'][1])}; ticket {r['key']} {r['state']}")
    shutil.move(N+r['name'],Q+'spent/'+r['name'])
L+=['','### stale/ (NEITHER drifted/partial, or NODIFF no machine-readable diff). Row: file | class | ticket state | work still owed?','']
for r in stale:
    t=ts.get(r['key']) or {}
    st=r['state']
    if st=='NONE': owed='ticket not found at source (key placeholder or deleted): nothing to owe'
    elif st in('Done','Canceled'): owed=f'no ({st}; closed)'
    else:
        nc=t.get('newest'); 
        owed=f"POSSIBLY (ticket {st}); newest comment: {clean(nc[1])[:140] if nc else 'none'}"
    L.append(f"- {r['name']} | {r['cls']} | {r['key']} {st} | {owed}")
    shutil.move(N+r['name'],Q+'stale/'+r['name'])
open(Q+'WHY.md','a').write('\n'.join(L)+'\n')
after=len([f for f in os.listdir(N) if f.startswith('READY_')])
sp=len(os.listdir(Q+'spent'));stl=len(os.listdir(Q+'stale'))
print('before',before,'after',after,'moved',len(spent)+len(stale),'spent dir',sp,'stale dir',stl)
assert before-after==len(spent)+len(stale)==sp+stl, 'conservation'
