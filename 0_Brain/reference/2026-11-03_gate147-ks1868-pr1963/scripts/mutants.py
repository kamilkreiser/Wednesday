# Gate 147 mutants: product only (userErasedSubscriber.ts per service), the PR's new test file for that service run, sha256 restored + verified after every run.
import hashlib, json, subprocess
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate147-ks1868-pr1963'
D = W + '/repo/Blockchain/Dev/services'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
GUARD = """        let reason: string | null | undefined;
        try {
          const m = err?.message;
          reason = m === undefined || m === null ? m : String(m);
        } catch {
          reason = 'unreadable thrown value';
        }
"""
OKL = "          reason = m === undefined || m === null ? m : String(m);\n"
def rethrow(site): return "        throw err; // let bus retry + dead-letter\n" if site == 'kyc' else "        throw err;\n"
def M(site):
    rt = rethrow(site)
    return [
     ('M0 revert to base (unguarded read in the log call)', lambda s: s.replace(GUARD, '').replace('          error: reason,', '          error: err?.message,')),
     ('M1 inner catch rethrows', lambda s: s.replace("        } catch {\n          reason = 'unreadable thrown value';", "        } catch (e2) {\n          throw e2;")),
     ('M2 constant always', lambda s: s.replace(OKL, "          void m; reason = 'unreadable thrown value';\n")),
     ('M3 wrong fallback text', lambda s: s.replace("          reason = 'unreadable thrown value';", "          reason = 'unknown';")),
     ('M4 failure log line dropped', lambda s: s.replace("        log('error', '[cascade] user.erased handler failed', {", "        void ({")),
     ('M5 log drops error field', lambda s: s.replace("          error: reason,\n", "          reasonLen: typeof reason,\n")),
     ('M6 String() dropped (message as is)', lambda s: s.replace(OKL, "          reason = m as any;\n")),
     ('M7 undefined/null passthrough dropped (String always)', lambda s: s.replace(OKL, "          reason = String(m);\n")),
     ('M8 rethrow a new Error (identity changes)', lambda s: s.replace(rt, "        throw new Error(String(reason));\n")),
     ('M9 rethrow dropped (handler swallows: bus would ack as handled)', lambda s: s.replace(rt, "        return;\n")),
     ('M10 swallow only when unreadable', lambda s: s.replace(rt, "        if (reason === 'unreadable thrown value') return;\n" + rt)),
    ]
rows = []
for site, svc in (('kyc', 'kyc'), ('wc', 'wallet-connector')):
    P = f'{D}/{svc}/src/userErasedSubscriber.ts'
    T = f'src/__tests__/ks1868-{svc}-user-erased-handler-failed-catch-unreadable-throw.test.ts'
    H = sha(P); orig = open(P).read()
    for name, f in M(site):
        mut = f(orig)
        if mut == orig:
            rows.append({'site': svc, 'mutant': name, 'result': 'NOT APPLIED'}); continue
        open(P, 'w').write(mut)
        try:
            out = f'{W}/logs/mut_tmp.json'
            r = subprocess.run(['node', W + '/scripts/vt.js', svc, T, '--reporter=json', '--outputFile', out], capture_output=True, text=True, timeout=600)
            j = json.load(open(out))
            failed = [a['title'].split(':')[0] for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
            kinds = set()
            for tr in j['testResults']:
                if tr.get('status') == 'failed' and not tr['assertionResults']: kinds.add('suite-error:' + tr.get('message', '')[:80])
                for a in tr['assertionResults']:
                    for m in a.get('failureMessages', []):
                        kinds.add('timeout' if 'Timed out' in m or 'timeout' in m.lower() else ('assertion' if 'AssertionError' in m or 'expected' in m else 'other:' + m[:60]))
            res = 'KILLED' if failed or j.get('numFailedTestSuites') else 'SURVIVED'
            rows.append({'site': svc, 'mutant': name, 'result': res, 'failed': failed, 'kinds': sorted(kinds), 'rc': r.returncode})
        finally:
            open(P, 'w').write(orig)
            rows[-1]['restore'] = sha(P) == H
for r in rows: print(json.dumps(r))
