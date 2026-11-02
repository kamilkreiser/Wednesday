import json
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/logs/'
def cells(n):
    j = json.load(open(W + n + '.json')); d = {}
    for tf in j['testResults']:
        f = tf['name'].split('/services/originate/')[-1]
        for a in tf['assertionResults']: d[(f, a['fullName'])] = a['status']
    return j, d
jb, b = cells('suite_base'); jh, h = cells('suite_head')
print(f"base: files {jb['numTotalTestSuites']} cells {jb['numTotalTests']} passed {jb['numPassedTests']} failed {jb['numFailedTests']}")
print(f"head: files {jh['numTotalTestSuites']} cells {jh['numTotalTests']} passed {jh['numPassedTests']} failed {jh['numFailedTests']}")
van = [k for k in b if k not in h]; new = [k for k in h if k not in b]; chg = [k for k in b if k in h and b[k] != h[k]]
print(f'vanished {len(van)}, new {len(new)}, changed {len(chg)}')
import collections
print('new by file:', dict(collections.Counter(k[0] for k in new)))
for k in van + chg: print('  ', k)
