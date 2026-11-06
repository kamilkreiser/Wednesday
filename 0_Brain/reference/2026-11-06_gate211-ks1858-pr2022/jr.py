import json,sys
d=json.load(open(sys.argv[1]))
print('files',len(d['testResults']),'total',d['numTotalTests'],'pass',d['numPassedTests'],'fail',d['numFailedTests'])
for f in d['testResults']:
    for t in f['assertionResults']:
        if t['status']!='passed':
            print(f['name'].split('/')[-1][:44],'|',t['title'][:70],'|',(t['failureMessages'] or [''])[0].split('\n')[0][:130])
