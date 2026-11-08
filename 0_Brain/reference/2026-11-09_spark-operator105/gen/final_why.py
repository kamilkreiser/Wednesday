import json,re,os,subprocess,sys
O=sys.argv[1];P='7eda23b34d3b7a413ca8f9c0945c7843708ce9f4'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/';Q=N+'_quarantine_2026-11-09/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
old=json.load(open(O+'/ready_all3.json')); land={r['name']:r for r in old}
ts=json.load(open(O+'/ticket_states.json'))
owed={r['name']:r for r in json.load(open(O+'/owed.json'))}
def git(*a): return subprocess.run(['git','-C',S]+list(a),capture_output=True,text=True).stdout.strip()
def landing(name):
    t=open(Q+'spent/'+name,encoding='utf-8',errors='replace').read()
    m=re.search(r'```diff\n(.*?)\n```',t,re.S); body=m.group(1)
    fs=sorted(set(re.findall(r'^\+\+\+ b/(\S+)',body,re.M)))
    adds=sorted({l[1:].strip() for l in body.split('\n') if l.startswith('+') and not l.startswith('+++') and len(l[1:].strip())>=30},key=len,reverse=True)
    for a in adds[:3]:
        out=git('log','--format=%h %s','--reverse','-S'+a,P,'--',*fs)
        if out: return out.split('\n')[0][:150],'git log -S"%s..." -- files'%a[:40].replace('"',"'")
def clean(s): return re.sub(r'\s+',' ',s or '').replace('|','/')
rows=[]
spent=sorted(os.listdir(Q+'spent'));stale=sorted(os.listdir(Q+'stale'))
L=['','## Operator 105 sweep, 2026-11-09 00:3x AEDT (Spark operator 105 for Wednesday; moved under her commission). Reversible: move back.',
 'Pin: develop 7eda23b34d3b7a413ca8f9c0945c7843708ce9f4 (ls-remote 00:2x and 00:35, unmoved). Instrument = operator 104\'s: first ```diff fence, git apply --cached --check forward then -R against a temp index of the pin tree, PLUS a --unidiff-zero retry (a hunk with leading context and none after is refused by strict apply as "must match at end of file"; 4 READYs were wrongly moved on the strict-only pass and are restored to night/: KS-1240-p6, O84-P2, O89-P6, O90-P3). Script: 0_Brain/reference/2026-11-09_spark-operator105/gen/ready_all_v2.py; results ready_all_v2.json. A READY with no fence but a CANONICAL PATCH path that still exists was checked from that file. FWD-OK, open-PR-named and live-queue READYs were NOT moved. No HOLD-NOTE file sat beside any moved READY (none exists in night/ top level).',
 '(Operator 105 note: the earlier WHY text above this heading is unchanged.)','',
 '### spent/ (REV-OK: the diff is already in the tip). Row: file | class | landing commit (sha subject) | how measured','']
for n in spent:
    r=land.get(n)
    lg=r['land'] if r and r.get('land') else landing(n)
    sha,subj=lg[0].split(' ',1)
    key=re.match(r'READY_(KS-\d+)',n).group(1); st=(ts.get(key) or {}).get('state','NONE')
    L.append(f"- {n} | REV-OK | {sha} {clean(subj)} | reverse apply --check OK at pin; landing by {clean(lg[1])}; ticket {key} {st}")
L+=['','### stale/ (NEITHER drifted/partial, or NODIFF no machine-readable diff). Row: file | class | ticket state | work still owed?','']
for n in stale:
    key=re.match(r'READY_(KS-\d+)',n).group(1); t=ts.get(key) or {}; st=t.get('state','NONE')
    cls='NODIFF' if n in land and land[n]['cls']=='NODIFF' else 'NEITHER'
    if st=='NONE': ow='ticket not found at source (placeholder key): nothing to owe'
    elif st in('Done','Canceled'): ow=f'no ({st}; closed)'
    else:
        o=owed.get(n); h=''
        if o:
            ne=[x for x in o['owed'] if x[1]=='NEWFILE']
            if ne and all('True' in x[3] for x in ne): h='likely landed in another form (its new test file exists at the tip)'
            elif ne: h='POSSIBLY STILL OWED (its new test file is absent at the tip)'
            else: h='unclear (modified-file hunks only)'
        else: h='unclear (no machine-readable diff)'
        nc=t.get('newest'); ow=f"ticket {st}; {h}; newest comment: {clean(nc[1])[:110] if nc else 'none'}"
    L.append(f"- {n} | {cls} | {key} {st} | {ow}")
base=open(O+'/WHY.before_op105_sweep_backup.md').read()
open(Q+'WHY.md','w').write(base.rstrip('\n')+'\n'+'\n'.join(L)+'\n')
print(len(spent),len(stale))
