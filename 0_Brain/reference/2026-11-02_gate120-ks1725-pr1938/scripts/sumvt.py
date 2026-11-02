import json,glob,sys,os
L=sys.argv[1]; tot=p=f=0; fails=[]
for fn in sorted(glob.glob(L+'/vt_*.json')):
    try: d=json.load(open(fn))
    except Exception as e: print(fn,'unparseable'); continue
    for s in d['testResults']:
        for a in s['assertionResults']:
            tot+=1
            if a['status']=='passed': p+=1
            elif a['status']=='failed': f+=1; fails.append(os.path.basename(s['name'])+' :: '+a['fullName'][:90])
    print(os.path.basename(fn), d['numPassedTests'],'/',d['numTotalTests'])
print('TOTAL',p,'/',tot,'failed',f)
open(L+'/fails.txt','w').write('\n'.join(fails))
