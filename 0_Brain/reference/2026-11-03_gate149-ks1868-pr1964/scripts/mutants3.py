# Gate 149 mutant re-check: M6' (log field replaced, compiles) and M7 (answer 500 + unhandled rejection) with full jest output kept.
import hashlib, json, subprocess
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964'
O = W + '/repo/Blockchain/Dev/services/originate'
P = O + '/src/routes/documents.ts'
T = [O + '/src/__tests__/ks1868-documents-lookup-routes-message-coercion-unreadable-throw.test.ts',
     O + '/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts']
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
GUARD = "      let reason: string;\n      try {\n        reason = String(error instanceof Error ? error.message : error);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n"
SITES = ['signRequest', 'sign', 'lifecycle', 'signCert', 'signWallet', 'sigJson']
MUTS = [
 ('M7b answers 500 AND leaks a READABLE unhandled rejection only for unreadable values', lambda g, tail: (g.replace("        reason = 'unreadable thrown value';\n", "        reason = 'unreadable thrown value';\n        void Promise.reject(new Error('g149 leak'));\n"), tail)),
]
src0 = open(P).read(); H = sha(P); parts = src0.split(GUARD); assert len(parts) == 7
rows = []
for k, site in enumerate(SITES):
    for name, f in MUTS:
        g, tail = f(GUARD, parts[k + 1])
        mut = GUARD.join(parts[:k + 1]) + g + tail + ''.join(GUARD + p for p in parts[k + 2:])
        open(P, 'w').write(mut)
        try:
            out = W + '/logs/mut3_tmp.json'; tag = name.split(' ')[0]
            r = subprocess.run(['node', W + '/scripts/jest.js', '--runTestsByPath', *T, '--json', '--outputFile', out], capture_output=True, text=True, timeout=900)
            open(f'{W}/logs/mut3_{site}_{tag}.log', 'w').write(r.stdout + r.stderr)
            j = json.load(open(out))
            failed = [a['title'].split(' ')[2] for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
            suitemsg = [tr.get('message', '')[:300].replace('\n', ' ') for tr in j['testResults'] if tr.get('status') == 'failed']
            rows.append({'site': site, 'mutant': name, 'failedCells': failed, 'passed': j['numPassedTests'], 'total': j['numTotalTests'], 'suiteFailed': j['numFailedTestSuites'], 'runtimeErr': j['numRuntimeErrorTestSuites'], 'rc': r.returncode, 'suiteMsg': suitemsg})
        finally:
            open(P, 'w').write(src0); rows[-1]['restore'] = sha(P) == H
with open(W + '/logs/mutants3_table.log', 'w') as fh:
    for x in rows: fh.write(json.dumps(x) + '\n')
