import subprocess,sys,json,time
G=sys.argv[1]
for T in('base','repo'):
    A=f'{G}/{T}/Blockchain/Dev/services/auth'; s=time.time()
    jf=f'{G}/evidence/q6_whole_cwd_{T}.json'
    r=subprocess.run([f'{G}/repo/Blockchain/Dev/node_modules/.bin/vitest','run','--reporter=json','--outputFile='+jf],cwd=A,capture_output=True,text=True)
    open(f'{G}/evidence/q6_whole_cwd_{T}.log','w').write(r.stdout+r.stderr)
    d=json.load(open(jf))
    print(T,'rc',r.returncode,'secs',int(time.time()-s),'total',d['numTotalTests'],'pass',d['numPassedTests'],'fail',d['numFailedTests'],'files',len(d['testResults']),'failedSuites',d['numFailedTestSuites'],flush=True)
    for f in d['testResults']:
        for a in f['assertionResults']:
            if a['status']=='failed': print('  FAIL',f['name'].split('/')[-1],'::',a['title'][:100],'::',(a['failureMessages'] or [''])[0][:120].replace('\n',' '))
        if f.get('status')=='failed' and not any(a['status']=='failed' for a in f['assertionResults']): print('  FILEFAIL',f['name'].split('/')[-1],f.get('message','')[:200])
