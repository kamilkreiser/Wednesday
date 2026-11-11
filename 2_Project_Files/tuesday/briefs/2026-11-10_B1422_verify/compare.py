import json,sys
def load(p):
    d=json.load(open(p)); s={}
    for f in d['testResults']:
        n=f['name'].split('/repo/')[-1]
        for t in f['assertionResults']: s[(n,t['fullName'])]=t['status']
    return d,s
da,a=load(sys.argv[1]); db,b=load(sys.argv[2])
c=lambda d:(d['numTotalTestSuites'] and None, d['numPassedTests'],d['numFailedTests'],d['numPendingTests'],d['numTotalTests'],len(d['testResults']))
print('main  passed/failed/pending/total/files',c(da)[1:]); print('head  passed/failed/pending/total/files',c(db)[1:])
lost=sorted(set(a)-set(b)); added=sorted(set(b)-set(a)); chg=[k for k in set(a)&set(b) if a[k]!=b[k]]
print('lost',len(lost),'added',len(added),'status-changed',len(chg))
for k in lost: print(' LOST ',k[0].split('/')[-1],'|',k[1],'|',a[k])
for k in added: print(' ADDED',k[0].split('/')[-1],'|',k[1],'|',b[k])
for k in chg: print(' CHG',k,a[k],b[k])
