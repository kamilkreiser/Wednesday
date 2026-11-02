# Gate 149 mutants: routes/documents.ts only (tests untouched), both new test files run, sha256 restored + verified after every run.
import hashlib, json, subprocess
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964'
O = W + '/repo/Blockchain/Dev/services/originate'
P = O + '/src/routes/documents.ts'
T = [O + '/src/__tests__/ks1868-documents-lookup-routes-message-coercion-unreadable-throw.test.ts',
     O + '/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts']
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
GUARD = "      let reason: string;\n      try {\n        reason = String(error instanceof Error ? error.message : error);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n"
SITES = ['signRequest', 'sign', 'lifecycle', 'signCert', 'signWallet', 'sigJson']
def guard_mut(new):
    return lambda g, tail: (new, tail)
MUTS = [
 ('M0 revert to base read (unguarded, no String())', guard_mut("      const reason = error instanceof Error ? error.message : String(error);\n")),
 ('M1 inner catch rethrows', guard_mut(GUARD.replace("      } catch {\n        reason = 'unreadable thrown value';", "      } catch (e2) {\n        throw e2;"))),
 ('M2 constant always', guard_mut(GUARD.replace("reason = String(error instanceof Error ? error.message : error);", "reason = 'unreadable thrown value';"))),
 ('M3 wrong fallback text', guard_mut(GUARD.replace("reason = 'unreadable thrown value';", "reason = 'unknown';"))),
 ('M4 String() dropped (message as is)', guard_mut(GUARD.replace("reason = String(error instanceof Error ? error.message : error);", "reason = (error instanceof Error ? error.message : error) as string;"))),
 ('M5 instanceof dropped (String(error))', guard_mut(GUARD.replace("reason = String(error instanceof Error ? error.message : error);", "reason = String(error);"))),
 ('M6 logged error field replaced', lambda g, tail: (g, tail.replace("error: reason", "error: 'x'", 1))),
 ('M7 answers 500 AND leaves an unhandled rejection', guard_mut(GUARD + "      void Promise.reject(error);\n")),
]
src0 = open(P).read(); H = sha(P)
parts = src0.split(GUARD)
assert len(parts) == 7, len(parts)
rows = []
for k, site in enumerate(SITES):
    for name, f in MUTS:
        g, tail = f(GUARD, parts[k + 1])
        mut = GUARD.join(parts[:k + 1]) + g + tail + ''.join(GUARD + p for p in parts[k + 2:])
        if mut == src0:
            rows.append({'site': site, 'mutant': name, 'result': 'NOT APPLIED'}); continue
        open(P, 'w').write(mut)
        try:
            out = W + '/logs/mut_tmp.json'
            subprocess.run(['node', W + '/scripts/jest.js', '--runTestsByPath', *T, '--json', '--outputFile', out], capture_output=True, text=True, timeout=900)
            j = json.load(open(out))
            failed = [a['title'].split(' ')[2] for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
            files = sorted({('lookup' if 'lookup' in tr['name'] else 'signing') for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed'})
            kinds = set()
            for tr in j['testResults']:
                for a in tr['assertionResults']:
                    for m in a.get('failureMessages', []):
                        kinds.add('timeout' if 'Exceeded timeout' in m else ('null-answer' if 'Received: null' in m else ('assertion' if ('expect(' in m or 'Expected' in m) else 'other')))
                if tr.get('status') == 'failed' and not tr['assertionResults']: kinds.add('suite-error')
            res = ('KILLED ' + ','.join(files) + ' ' + ' '.join(failed)) if failed or j['numRuntimeErrorTestSuites'] else 'SURVIVED'
            rows.append({'site': site, 'mutant': name, 'result': res, 'kinds': sorted(kinds), 'passed': j['numPassedTests'], 'total': j['numTotalTests']})
        finally:
            open(P, 'w').write(src0)
            rows[-1]['restore'] = sha(P) == H
with open(W + '/logs/mutants_table.log', 'w') as fh:
    for r in rows:
        fh.write(f"{r['site']:11} {r['mutant']:50} {r['result']:48} {','.join(r.get('kinds', []))} pass={r.get('passed')}/{r.get('total')} restore={r.get('restore')}\n")
    fh.write(f"killed {sum(r['result'].startswith('KILLED') for r in rows)} survived {sum(r['result'] == 'SURVIVED' for r in rows)} not-applied {sum(r['result'] == 'NOT APPLIED' for r in rows)} of {len(rows)}\n")
open(W + '/logs/mutants.done', 'w').write('done\n')
