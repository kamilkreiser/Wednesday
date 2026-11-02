import json,sys,re
for p in sys.argv[1:]:
    try: j=json.load(open(p))
    except Exception as e: print(p.split('/')[-1],'NOJSON',e); continue
    fails=[]
    for t in j['testResults']:
        for a in t['assertionResults']:
            if a['status']=='failed':
                fm=' '.join(a.get('failureMessages') or [])
                kind='assert' if re.search(r'AssertionError|expect\(|toBe|toEqual|toHaveLength',fm) else fm[:80].replace('\n',' ')
                fails.append((t['name'].split('/')[-1],a['title'][:70],kind))
    print(p.split('/')[-1],'files',len(j['testResults']),'tests',j['numTotalTests'],'passed',j['numPassedTests'],'failed',j['numFailedTests'])
    for f in fails: print('   FAIL',f)
