import json, sys, re
for f in sys.argv[1:]:
    j = json.load(open(f))
    print(f"{f.split('/')[-1]}: suites {j['numPassedTestSuites']}/{j['numTotalTestSuites']} tests passed {j['numPassedTests']} failed {j['numFailedTests']} total {j['numTotalTests']}")
    for tr in j['testResults']:
        fails = [a for a in tr['assertionResults'] if a['status'] == 'failed']
        if not fails and tr.get('status') == 'passed': continue
        name = tr['name'].split('/')[-1]
        kinds = {}
        for a in fails:
            m = ' '.join(a.get('failureMessages') or [])
            k = 'assertion' if ('expect(' in m or 'Expected' in m or 'toBe' in m or 'toEqual' in m or 'toMatch' in m) else 'OTHER:' + m[:120].replace('\n', ' ')
            kinds[k] = kinds.get(k, 0) + 1
        print(f"  {name}: {len(fails)} failed {kinds} suiteStatus={tr.get('status')} {('msg=' + tr.get('message','')[:200].replace(chr(10),' ')) if not tr['assertionResults'] else ''}")
        if '--names' in sys.argv[0:1] or True:
            for a in fails: print('     -', a['title'][:150])
