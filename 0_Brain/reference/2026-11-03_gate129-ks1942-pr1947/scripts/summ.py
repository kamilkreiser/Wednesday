import json, sys, re
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947/logs/'
for n in sys.argv[1:]:
    j=json.load(open(G+n+'.json'))
    print(f"{n}: suites {j['numTotalTestSuites']} (failed {j['numFailedTestSuites']}), tests {j['numTotalTests']} passed {j['numPassedTests']} failed {j['numFailedTests']}")
    per={}
    kinds={}
    for s in j['testResults']:
        f=s['name'].split('/')[-1]
        if s.get('message') and not s['assertionResults']: print('  SUITE ERROR', f, s['message'][:200])
        for a in s['assertionResults']:
            per.setdefault(f,[0,0]); per[f][0 if a['status']=='passed' else 1]+=1
            if a['status']=='failed':
                m=' '.join(a['failureMessages'])
                k='assertion' if re.search(r'expect\(|toEqual|toBe|toMatchObject|Expected|Received', m) else 'OTHER'
                kinds[k]=kinds.get(k,0)+1
                if k!='assertion': print('  NON-ASSERTION', f, a['title'][:80], m[:200])
    for f,(p,x) in sorted(per.items()):
        if 'ks1942' in f or 'ks1940' in f or f=='governance.test.ts': print(f"  {f}: {p} passed / {x} failed")
    print('  failure kinds', kinds)
