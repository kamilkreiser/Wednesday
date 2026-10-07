import hashlib, subprocess, sys, json, os
wt = sys.argv[1]; ev = sys.argv[2]
f = os.path.join(wt, 'systemTest/performance/gate/report.ts')
OLD = '? `${name} ${label} passes=${metric.passes.toLocaleString()} fails=${metric.fails.toLocaleString()}`'
NEW = '? `${name} ${label} passes=${metric.passes} fails=${metric.fails}`'
raw = open(f, encoding='utf-8').read(); h0 = hashlib.sha256(raw.encode()).hexdigest()
n = raw.count(OLD); print('anchor count', n, '(want 1)'); assert n == 1
open(f, 'w', encoding='utf-8').write(raw.replace(OLD, NEW))
t = open(f, encoding='utf-8').read(); print('tamper landed', t.count(NEW) == 1 and t.count(OLD) == 0)
try:
    p = subprocess.run(['npm', '--prefix', os.path.join(wt, 'systemTest/performance'), 'run', 'test:unit', '--',
                        'tests/unit/gate/ks1164-breakdown-counts-are-locale-grouped.test.ts', '--reporter=json', '--outputFile.json=' + ev],
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR='/tmp'))
    print('tampered rc', p.returncode)
finally:
    open(f, 'w', encoding='utf-8').write(raw)
h1 = hashlib.sha256(open(f, 'rb').read()).hexdigest(); print('restored sha256 equal', h0 == h1, h1[:16])
d = json.load(open(ev))
for tr in d['testResults']:
    for a in tr['assertionResults']: print('  ', a['status'], a['title'])
print('tally', d['numPassedTests'], 'passed', d['numFailedTests'], 'failed of', d['numTotalTests'])
st = subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
print('tracked modified after restore:', repr(st))
