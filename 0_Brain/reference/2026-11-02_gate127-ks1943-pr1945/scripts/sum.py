import json, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/logs/'
for n in sys.argv[1:]:
    j = json.load(open(W + n + '.json'))
    print(f"{n}: files {j['numTotalTestSuites']} (failed {j['numFailedTestSuites']}), cells {j['numTotalTests']} passed {j['numPassedTests']} failed {j['numFailedTests']} pending {j['numPendingTests']}")
    if n.startswith('red'):
        red = ctl = 0; bad = []
        for tf in j['testResults']:
            if not tf['assertionResults']: print('  SUITE ERROR:', tf.get('message', '')[:300])
            for a in tf['assertionResults']:
                t = a['title']; msg = ' '.join(a.get('failureMessages') or [])
                isred = t.startswith('RED')
                byassert = 'expect(' in msg
                if isred and a['status'] == 'failed' and byassert: red += 1
                elif (not isred) and a['status'] == 'passed': ctl += 1
                else: bad.append((a['status'], t[:90], msg[:160].replace('\n', ' ')))
        print(f'  RED failing by assertion: {red}; controls passing: {ctl}; other: {len(bad)}')
        for b in bad[:12]: print('   ', b)
