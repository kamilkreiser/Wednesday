import json,sys
for p in sys.argv[1:]:
    d=json.load(open(p))
    fails=[]
    for f in d['testResults']:
        for a in f.get('assertionResults',[]):
            if a['status'] not in ('passed','pending','skipped','todo'): fails.append((f['name'].split('/src/')[-1],a.get('fullName') or a.get('title'),a['status']))
        if f.get('status')=='failed' and not any(x[0]==f['name'].split('/src/')[-1] for x in fails): fails.append((f['name'].split('/src/')[-1],'(file-level) '+(f.get('message') or '')[:200],'failed'))
    print(p.split('/')[-1], 'files',len(d['testResults']),'total',d['numTotalTests'],'passed',d['numPassedTests'],'failed',d['numFailedTests'],'pending',d.get('numPendingTests'),'failedSuites',d.get('numFailedTestSuites'))
    for x in fails: print('  FAIL',x)
