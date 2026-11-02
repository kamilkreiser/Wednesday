# Gate 145 mutants: product only, the two new test files run, sha256 restored + verified after every run.
import hashlib, json, os, re, subprocess, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate145-ks1868-pr1961'
O = W + '/repo/Blockchain/Dev/services/originate'
P = {'query': O + '/src/services/errorTrackingService.ts', 'codec': O + '/src/utils/lifecyclePayloadCodec.ts'}
T = {'query': O + '/src/__tests__/ks1868-error-tracking-get-recent-errors-catch-unreadable-throw.test.ts',
     'codec': O + '/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts'}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
Q_OK = "      reason = err instanceof Error ? err.message : String(err);\n"
C_OK = "          reason = String(err instanceof Error ? err.message : err);\n"
M = [
 ('query', 'M0 revert to base (unguarded read in the log call)', lambda s: s.replace("""    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('Failed to query errors', { error: reason });""", "    logger.error('Failed to query errors', { error: err instanceof Error ? err.message : String(err) });")),
 ('query', 'M1 inner catch rethrows', lambda s: s.replace("    } catch {\n      reason = 'unreadable thrown value';", "    } catch (e2) {\n      throw e2;")),
 ('query', 'M2 constant always', lambda s: s.replace(Q_OK, "      reason = 'unreadable thrown value';\n")),
 ('query', 'M3 wrong fallback text', lambda s: s.replace("      reason = 'unreadable thrown value';", "      reason = 'unknown';")),
 ('query', 'M4 log line dropped', lambda s: s.replace("    logger.error('Failed to query errors', { error: reason });", "    void reason;")),
 ('query', 'M5 log drops error field', lambda s: s.replace("{ error: reason }", "{}")),
 ('query', 'M6 String() for all (coerce message)', lambda s: s.replace(Q_OK, "      reason = String(err instanceof Error ? err.message : err);\n")),
 ('query', 'M7 instanceof replaced by message-presence', lambda s: s.replace(Q_OK, "      reason = err && err.message !== undefined ? err.message : String(err);\n")),
 ('query', 'M8 empty answer replaced by rethrow after logging', lambda s: s.replace("    logger.error('Failed to query errors', { error: reason });\n    return { errors: [], total: 0 };", "    logger.error('Failed to query errors', { error: reason });\n    throw err;")),
 ('codec', 'M0 revert to base (unguarded read in the log call)', lambda s: s.replace("""        let reason: string;
        try {
          reason = String(err instanceof Error ? err.message : err);
        } catch {
          reason = 'unreadable thrown value';
        }
""", "").replace("          error: reason,", "          error: err instanceof Error ? err.message : String(err),")),
 ('codec', 'M1 inner catch rethrows', lambda s: s.replace("        } catch {\n          reason = 'unreadable thrown value';", "        } catch (e2) {\n          throw e2;")),
 ('codec', 'M2 constant always', lambda s: s.replace(C_OK, "          reason = 'unreadable thrown value';\n")),
 ('codec', 'M3 wrong fallback text', lambda s: s.replace("          reason = 'unreadable thrown value';", "          reason = 'unknown';")),
 ('codec', 'M4 String() dropped (message as is)', lambda s: s.replace(C_OK, "          reason = err instanceof Error ? err.message : String(err);\n")),
 ('codec', 'M5 log drops error field', lambda s: s.replace("          error: reason,\n", "")),
 ('codec', 'M6 log drops eventId', lambda s: s.replace("          eventId,\n          error: reason,", "          error: reason,")),
 ('codec', 'M7 marker replaced by {} (erasure would treat as empty)', lambda s: s.replace("        return { payloadUnavailable: true };", "        return {};")),
 ('codec', 'M8 marker replaced by rethrow (base abort shape)', lambda s: s.replace("        return { payloadUnavailable: true };", "        throw err;")),
]
jest = W + '/scripts/jest.js'
rows = []
H = {k: sha(v) for k, v in P.items()}
for site, name, f in M:
    src = open(P[site]).read(); mut = f(src)
    if mut == src:
        rows.append({'site': site, 'mutant': name, 'result': 'NOT APPLIED'}); continue
    open(P[site], 'w').write(mut)
    try:
        r = subprocess.run(['node', jest, '--runTestsByPath', T[site], '--json', '--outputFile', W + '/logs/mut_tmp.json'], capture_output=True, text=True, timeout=600)
        j = json.load(open(W + '/logs/mut_tmp.json'))
        failed = [a['title'].split(':')[0] for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
        kinds = set()
        for tr in j['testResults']:
            for a in tr['assertionResults']:
                for m in a.get('failureMessages', []):
                    kinds.add('timeout' if 'Exceeded timeout' in m else ('assertion' if ('expect(' in m or 'Expected' in m) else 'other'))
        if j['numRuntimeErrorTestSuites']: kinds.add('suite-error')
        res = ('KILLED ' + ' '.join(failed)) if failed or j['numRuntimeErrorTestSuites'] else 'SURVIVED'
        rows.append({'site': site, 'mutant': name, 'result': res, 'kinds': sorted(kinds)})
    finally:
        open(P[site], 'w').write(src)
        rows[-1]['restore'] = sha(P[site]) == H[site]
for r in rows: print(f"{r['site']:6} {r['mutant']:55} {r['result']:45} {','.join(r.get('kinds', []))} restore={r.get('restore')}")
print('killed', sum(r['result'].startswith('KILLED') for r in rows), 'survived', sum(r['result'] == 'SURVIVED' for r in rows), 'not applied', sum(r['result'] == 'NOT APPLIED' for r in rows))
