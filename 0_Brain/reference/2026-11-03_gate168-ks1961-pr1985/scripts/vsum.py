import json, sys
# Summarise vitest --reporter=json files: totals and failing test names with first failure line.
for p in sys.argv[1:]:
    try:
        d = json.load(open(p))
    except Exception as e:
        print(p.split('/')[-1], 'UNREADABLE', e); continue
    fails = []
    for f in d.get('testResults', []):
        for a in f.get('assertionResults', []):
            if a['status'] == 'failed':
                fails.append((f['name'].split('/')[-1], a['fullName'][:110], (a.get('failureMessages') or [''])[0].split('\n')[0][:140]))
    print(f"{p.split('/')[-1]}: files {d['numTotalTestSuites'] if False else len(d.get('testResults', []))} failedFiles {d['numFailedTestSuites']} tests total {d['numTotalTests']} passed {d['numPassedTests']} failed {d['numFailedTests']} pending {d['numPendingTests']} todo {d.get('numTodoTests', 0)}")
    for x in fails[:40]:
        print('   FAIL', ' | '.join(x))
