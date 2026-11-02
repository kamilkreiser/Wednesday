# Gate 146 mutants: product only (approvalWorkflowService.ts), the PR's test file run, sha256 restored + verified after every run.
import hashlib, json, subprocess
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962'
T = W + '/repo/Blockchain/Dev/services/transfer'
P = T + '/src/services/approvalWorkflowService.ts'
TN = 'src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def block(ind, line):
    i = ' ' * ind
    return (f"{i}let reason: string | null | undefined;\n{i}try {{\n{i}  const m = err?.message;\n{i}  reason = m === undefined || m === null ? m : String(m);\n"
            f"{i}}} catch {{\n{i}  reason = 'unreadable thrown value';\n{i}}}\n{i}{line}\n")
SITES = {
 'seed': (6, "console.error(`[approvalWorkflowService] Failed to seed workflow ${wf.id}:`, reason);", "console.error(`[approvalWorkflowService] Failed to seed workflow ${wf.id}:`, err?.message);"),
 'probe': (4, "console.warn('[approvalWorkflowService] DB tables not ready:', reason);", "console.warn('[approvalWorkflowService] DB tables not ready:', err?.message);"),
 'sweep': (6, "console.error('[approvalWorkflowService] processEscalations error:', reason);", "console.error('[approvalWorkflowService] processEscalations error:', err?.message);"),
}
def mk(site, kind):
    ind, line, baseline = SITES[site]; i = ' ' * ind; b = block(ind, line)
    def f(s):
        assert s.count(b) == 1, site
        nb = b
        if kind == 'M0': nb = f"{i}{baseline}\n"
        elif kind == 'M1': nb = b.replace(f"{i}}} catch {{\n{i}  reason = 'unreadable thrown value';", f"{i}}} catch (e2) {{\n{i}  throw e2;")
        elif kind == 'M2': nb = b.replace(f"{i}  reason = m === undefined || m === null ? m : String(m);", f"{i}  void m; reason = 'unreadable thrown value';")
        elif kind == 'M3': nb = b.replace("reason = 'unreadable thrown value';", "reason = 'unknown';")
        elif kind == 'M4': nb = b.replace("? m : String(m);", "? m : (m as any);")
        elif kind == 'M5': nb = b.replace(f"{i}{line}\n", f"{i}void reason;\n")
        elif kind == 'M6': nb = b.replace("reason = m === undefined || m === null ? m : String(m);", "reason = String(m);")
        elif kind == 'M7': nb = b + f"{i}throw err;\n"
        elif kind == 'M8': nb = b + f"{i}return;\n"   # seed: stop the loop after the first failure (base's 1-of-4 shape for every value)
        elif kind == 'M9': nb = b.replace(f"{i}  reason = 'unreadable thrown value';\n", f"{i}  reason = 'unreadable thrown value';\n{i}  throw err;\n")
        return s.replace(b, nb)
    return f
NAMES = {'M0': 'revert to base (unguarded read)', 'M1': 'inner catch rethrows', 'M2': 'constant always', 'M3': 'wrong fallback text',
         'M4': 'String() dropped (message as is)', 'M5': 'log line removed', 'M6': 'undefined/null passthrough -> String() always',
         'M7': 'rethrow after logging (every value)', 'M8': 'seed only: stop the loop after the first failure', 'M9': 'rethrow only when unreadable'}
PLAN = [(s, k) for s in ('seed', 'probe', 'sweep') for k in ('M0','M1','M2','M3','M4','M5','M6','M7','M9')] + [('seed', 'M8')]
H = sha(P); rows = []
for site, k in PLAN:
    src = open(P).read(); mut = mk(site, k)(src)
    if mut == src: rows.append({'site': site, 'mutant': k, 'result': 'NOT APPLIED'}); continue
    open(P, 'w').write(mut)
    try:
        out = W + '/logs/mut_tmp.json'
        r = subprocess.run(['node', W + '/scripts/vt.cjs', TN, '--reporter=json', '--outputFile=' + out], capture_output=True, text=True, timeout=600)
        open(f"{W}/logs/mut_{site}_{k}.log", 'w').write(r.stdout + r.stderr)
        try: j = json.load(open(out))
        except Exception: j = {'testResults': [], 'numFailedTestSuites': 1}
        failed = [a['title'].split(':')[0].replace('RED ks1868 ', '').replace('control ks1868 ', '') for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
        kinds = set()
        for tr in j['testResults']:
            if tr.get('status') == 'failed' and not tr['assertionResults']: kinds.add('suite-error')
            for a in tr['assertionResults']:
                for m in a.get('failureMessages', []):
                    kinds.add('timeout' if 'timed out' in m else ('assertion' if ('AssertionError' in m or 'expected' in m) else 'other'))
        res = ('KILLED ' + ' '.join(failed)) if failed or 'suite-error' in kinds else 'SURVIVED'
        rows.append({'site': site, 'mutant': k, 'name': NAMES[k], 'result': res, 'kinds': sorted(kinds)})
    finally:
        open(P, 'w').write(src); rows[-1]['restore'] = sha(P) == H
for r in rows: print(f"{r['site']:6} {r['mutant']:3} {r.get('name',''):50} {r['result']:40} {','.join(r.get('kinds', []))} restore={r.get('restore')}")
print('killed', sum(r['result'].startswith('KILLED') for r in rows), 'survived', sum(r['result'] == 'SURVIVED' for r in rows), 'not applied', sum(r['result'] == 'NOT APPLIED' for r in rows))
