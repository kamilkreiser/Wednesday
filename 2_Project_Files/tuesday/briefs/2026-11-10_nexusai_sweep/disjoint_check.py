# Disjointness of the five lanes by path. Inputs: tree_at_3929b794.txt (size path, line 1 = truncated flag),
# final_assignment.json ([key,lane,basis]), tickets_paths.json ([key, [existing tree paths named in the ticket]]).
# Run: python3 -I disjoint_check.py   (cwd-independent; reads beside itself)
import json,os,fnmatch,collections,sys
H=os.path.dirname(os.path.abspath(__file__))
lines=open(H+'/tree_at_3929b794.txt').read().splitlines()
assert lines[0]=='false','tree listing truncated'
tree=[l.split(' ',1)[1] for l in lines[1:]]
SERVER=['backend/server.js','backend/simpleDb.js','backend/jsonStorage.js','backend/azure-ad.js','backend/services/capabilities.js','scripts/role-capability-inventory.js','docs/ROLE-CAPABILITIES.md']
FRONTX=['docs/BRAND.md','scripts/derive-brand-tokens.js','scripts/propose-dark-retheme.js','scripts/land-brand-retheme.js','scripts/render-palette-proposal.js','scripts/capture-sustainability-screenshots.js']
# Lane globs. __tests__/ and scripts/verify-expected-counts.json are handled below (ticket-keyed / landing-serialised).
G={
 'S':SERVER,
 'F':['static/*','tests/e2e/*']+FRONTX,
 'B':['backend/*'],            # minus S files (subtracted below)
 'T':['scripts/*','.github/*','docs/*','tests/*','bicep/*','azure-marketplace/*','package.json','package-lock.json','jest.config.js','Dockerfile'],
 'R':['HISTORY.md','1_Project_Definition/*'],   # 1_Project_Definition is the project folder, outside the repo tree
}
SUB={'B':SERVER,'F':[],'T':SERVER+FRONTX+['tests/e2e/*','scripts/verify-expected-counts.json']}
def claims(p):
    out=[]
    for l,gs in G.items():
        hit=any(fnmatch.fnmatch(p,g) for g in gs)
        if hit and any(fnmatch.fnmatch(p,s) for s in SUB.get(l,[])): hit=False
        if hit: out.append(l)
    return out
SHARED='scripts/verify-expected-counts.json'
unclaimed=collections.Counter(); multi=[]; per=collections.Counter()
for p in tree:
    if p.startswith('__tests__/') or p==SHARED: continue
    c=claims(p)
    if len(c)>1: multi.append((p,c))
    for l in c: per[l]+=1
    if not c: unclaimed[p.split('/')[0]]+=1
print('tree files',len(tree),'| files claimed per lane (non-test):',dict(per))
print('FILES CLAIMED BY MORE THAN ONE LANE:',len(multi),multi[:5])
print('unclaimed top-level (nobody edits these; fine):',dict(unclaimed))
# control: a planted overlap must be caught
G['F'].append('backend/server.js'); c=claims('backend/server.js'); assert len(c)>1,'CONTROL FAILED'; print('control (planted overlap backend/server.js in F) caught ->',c); G['F'].pop()
# tickets: each non-test path a ticket names must sit inside its lane
fa=json.load(open(H+'/final_assignment.json')); tp=dict(json.load(open(H+'/tickets_paths.json')))
bad=[];borrow=collections.Counter()
lane={k:l for k,l,b in fa}
for k,l,b in fa:
    if l in ('?','R'): continue   # R edits only HISTORY.md + 1_Project_Definition; source paths a landed ticket names are read-only for it
    for p in tp.get(k,[]):
        if p.startswith('__tests__/') or p==SHARED: continue   # SHARED counts file: landing-serialised
        if l not in claims(p): bad.append((k,l,p,claims(p))); 
print('ticket path violations (a ticket names a file outside its lane = BORROW, sequenced):',len(bad),'tickets:',len(set(b[0] for b in bad)))
json.dump(bad,open(H+'/borrow_list.json','w'))
# tests: a test file named by tickets of two different lanes would be a collision
tests=collections.defaultdict(set)
for k,l,b in fa:
    for p in tp.get(k,[]):
        if p.startswith('__tests__/'): tests[p].add(l)
coll={p:sorted(v) for p,v in tests.items() if len(v)>1}
print('existing test files named by tickets of >1 lane:',len(coll),coll)
# new test files: __tests__/rd<N>-* is owned by the lane of ticket N; two lanes cannot own the same N (one lane per ticket)
assert len(set(k for k,l,b in fa))==len(fa),'a ticket sits in two lanes'
print('tickets assigned:',len(fa),'; one lane each: OK; unplaced (lane ?):',sum(1 for k,l,b in fa if l=='?'))
print('shared, landing-serialised (no lane owns it):',SHARED)
