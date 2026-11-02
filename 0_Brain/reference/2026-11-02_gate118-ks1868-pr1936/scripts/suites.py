import json
L = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate118-ks1868-pr1936/logs/'
def load(n):
    j = json.load(open(L + n + '.json'))
    cells = {}
    for tr in j['testResults']:
        for a in tr['assertionResults']:
            cells[(tr['name'].split('/src/')[-1], a['fullName'])] = a['status']
    return j, cells
for n in ['green_head_1', 'green_head_2', 'green_head_3', 'red_base', 'suite_head', 'suite_base']:
    j, c = load(n)
    print(n, 'files', j['numTotalTestSuites'], 'failedFiles', j['numFailedTestSuites'], 'tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'])
_, r = load('red_base')
for k, v in sorted(r.items()):
    print('  red', v, k[1][:150])
j, rr = load('red_base'); msgs = [m for tr in j['testResults'] for a in tr['assertionResults'] for m in a.get('failureMessages', [])]
print('red failures by expect():', sum('expect(' in m for m in msgs), 'of', len(msgs))
_, h = load('suite_head'); _, b = load('suite_base')
print('vanished', len([k for k in b if k not in h]), 'new', len([k for k in h if k not in b]), 'changed', len([k for k in b if k in h and b[k] != h[k]]))
